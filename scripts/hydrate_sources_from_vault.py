"""CCBA Legal Spoke — Universal Tri-Tier Cloud Vault Hydration & Sync Engine (ADR 0035 / ADR 0059).

Manages physical binary assets (.pdf, .docx, .doc) between local `sources/` directories
and the Google Drive Cloud Vault (`CCBA_Legal_Vault`).

Usage:
    # 1. Dry-run push (inspect what needs uploading without writing)
    python scripts/hydrate_sources_from_vault.py --push --dry-run

    # 2. Push all local sources to Google Drive Cloud Vault
    python scripts/hydrate_sources_from_vault.py --push

    # 3. Verify integrity of all source assets against metadata and vault
    python scripts/hydrate_sources_from_vault.py --verify-only

    # 4. Hydrate (pull/download) missing source files on a fresh clone
    python scripts/hydrate_sources_from_vault.py --all
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Root directory of the repository
ROOT_DIR = Path(__file__).resolve().parent.parent
LEGAL_DOCS_DIR = ROOT_DIR / "legal_docs"
CATEGORIES = ["01_vbpl", "02_qcvn", "03_tcvn"]
SOURCE_EXTENSIONS = {".pdf", ".docx", ".doc"}
DEFAULT_REMOTE = "gdrive:"
DEFAULT_VAULT_ROOT = "CCBA_Legal_Vault"

# Operating system artifacts to exclude
SYSTEM_IGNORE_FILES = {"desktop.ini", "thumbs.db", ".ds_store", ".gitkeep"}


def detect_gdrive_mount() -> Optional[Path]:
    """Detects local Google Drive mount point dynamically to avoid machine coupling."""
    env_path = os.getenv("CCBA_VAULT_MOUNT_PATH")
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p

    # Standard Windows Google Drive mounted letters
    candidates = [Path(f"{drive}:/My Drive") for drive in ("H", "G", "I")]
    for c in candidates:
        if c.exists():
            return c

    return None


def compute_sha256(filepath: Path) -> str:
    """Computes the SHA-256 hash of a local file in 64KB chunks."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest().lower()


def find_rclone_cmd() -> Optional[str]:
    """Finds rclone executable in PATH or standard user directories."""
    rclone_path = shutil.which("rclone")
    if rclone_path:
        return rclone_path

    # Check common Windows winget installation path
    winget_pkg_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    if winget_pkg_dir.exists():
        for rpath in winget_pkg_dir.glob("**/rclone.exe"):
            if rpath.is_file():
                return str(rpath)

    # Check AppData or Program Files
    prog_files = os.environ.get("ProgramFiles")
    user_prof = os.environ.get("USERPROFILE")
    candidates = []
    if prog_files:
        candidates.append(Path(prog_files) / "rclone" / "rclone.exe")
    if user_prof:
        candidates.append(Path(user_prof) / "bin" / "rclone.exe")

    for c in candidates:
        if c.is_file():
            return str(c)

    return None


class VaultHydrationEngine:
    """Orchestrates asset discovery, checksum validation, and bi-directional sync."""

    def __init__(
        self,
        root_dir: Path = ROOT_DIR,
        remote: str = DEFAULT_REMOTE,
        vault_root: str = DEFAULT_VAULT_ROOT,
        category: Optional[str] = None,
        bundle: Optional[str] = None,
        dry_run: bool = False,
        verbose: bool = False,
    ) -> None:
        self.root_dir = root_dir
        self.legal_docs_dir = root_dir / "legal_docs"
        self.remote = remote.rstrip(":") + ":"
        self.vault_root = vault_root.strip("/")
        self.category_filter = category
        self.bundle_filter = bundle
        self.dry_run = dry_run
        self.verbose = verbose
        self.rclone_bin = find_rclone_cmd()

        # Dynamic Google Drive mount detection
        self.local_gdrive_mount = detect_gdrive_mount()
        self.local_vault_root: Optional[Path] = None
        if self.local_gdrive_mount:
            self.local_vault_root = self.local_gdrive_mount / self.vault_root

        # Remote vault cache
        self._vault_files_cache: Optional[Set[str]] = None

    def get_bundle_dirs(self) -> List[Tuple[str, str, Path]]:
        """Discovers all bundle directories matching filters."""
        results: List[Tuple[str, str, Path]] = []
        for cat in CATEGORIES:
            if self.category_filter and cat != self.category_filter:
                continue
            cat_dir = self.legal_docs_dir / cat
            if not cat_dir.exists():
                continue
            for doc_dir in sorted(cat_dir.iterdir()):
                if not doc_dir.is_dir() or doc_dir.name.startswith("."):
                    continue
                if self.bundle_filter and doc_dir.name != self.bundle_filter:
                    continue
                results.append((cat, doc_dir.name, doc_dir))
        return results

    def get_remote_target(self, category: str, doc_slug: str, filename: str, metadata: Dict[str, Any]) -> str:
        """Determines the exact vault path according to ADR 0035 / metadata.yaml."""
        source_assets = metadata.get("source_assets", {})
        if isinstance(source_assets, dict):
            for key, asset_info in source_assets.items():
                if isinstance(asset_info, dict) and "vault_path" in asset_info:
                    vp = str(asset_info["vault_path"]).replace("\\", "/")
                    if vp.endswith(filename) or Path(vp).name == filename:
                        return f"{self.remote}{vp}"

        return f"{self.remote}{self.vault_root}/{category}/{doc_slug}/{filename}"

    def get_local_vault_file_path(self, category: str, doc_slug: str, filename: str, metadata: Dict[str, Any]) -> Optional[Path]:
        """Returns the local filesystem path on mounted Google Drive if available."""
        if not self.local_vault_root:
            return None

        source_assets = metadata.get("source_assets", {})
        if isinstance(source_assets, dict):
            for key, asset_info in source_assets.items():
                if isinstance(asset_info, dict) and "vault_path" in asset_info:
                    vp = str(asset_info["vault_path"]).replace("\\", "/")
                    if vp.endswith(filename) or Path(vp).name == filename:
                        rel = vp
                        if rel.startswith(self.vault_root + "/"):
                            rel = rel[len(self.vault_root) + 1:]
                        return self.local_vault_root / rel

        return self.local_vault_root / category / doc_slug / filename

    def get_remote_vault_files(self) -> Set[str]:
        """Loads list of all files in Vault via fast in-memory bulk scan."""
        if self._vault_files_cache is not None:
            return self._vault_files_cache

        files: Set[str] = set()
        if self.local_vault_root and self.local_vault_root.exists():
            for f in self.local_vault_root.rglob("*"):
                if f.is_file() and f.name.lower() not in SYSTEM_IGNORE_FILES:
                    rel = f.relative_to(self.local_vault_root).as_posix()
                    files.add(f"{self.vault_root}/{rel}".lower())
            self._vault_files_cache = files
            return files

        if self.rclone_bin:
            cmd = [self.rclone_bin, "lsf", "-R", "--files-only", f"{self.remote}{self.vault_root}"]
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, check=False)
                if res.returncode == 0:
                    for line in res.stdout.splitlines():
                        line = line.strip().replace("\\", "/")
                        if line and Path(line).name.lower() not in SYSTEM_IGNORE_FILES:
                            files.add(f"{self.vault_root}/{line}".lower())
            except Exception as e:
                if self.verbose:
                    print(f"      [rclone scan error]: {e}")

        self._vault_files_cache = files
        return files

    def execute_rclone_copy(self, src: str, dst: str) -> bool:
        """Copies a file using rclone copyto."""
        if self.rclone_bin:
            cmd = [self.rclone_bin, "copyto", src, dst]
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, check=False)
                if res.returncode == 0:
                    return True
                if self.verbose:
                    print(f"      [rclone stderr]: {res.stderr.strip()}")
            except Exception as e:
                if self.verbose:
                    print(f"      [rclone error]: {e}")
        return False

    def push_sources(self) -> bool:
        """Pushes all local physical source files to Google Drive Cloud Vault."""
        bundle_dirs = self.get_bundle_dirs()
        print("=================================================================")
        print("      CCBA LEGAL SPOKE — CLOUD VAULT PUSH & UPLOAD PIPELINE      ")
        print("=================================================================")
        print(f"Target Spoke : {self.root_dir}")
        print(f"Remote Vault : {self.remote}{self.vault_root}")
        print(f"Local Drive  : {self.local_vault_root or 'Not mounted locally (rclone mode)'}")
        print(f"Mode         : {'DRY-RUN (Simulation Only)' if self.dry_run else 'OFFICIAL PUSH (Live Upload)'}")
        print(f"Bundles Found: {len(bundle_dirs)}\n")

        total_files = 0
        up_to_date_count = 0
        uploaded_count = 0
        failed_count = 0

        remote_vault_files = self.get_remote_vault_files()

        for cat, slug, b_dir in bundle_dirs:
            sources_dir = b_dir / "sources"
            if not sources_dir.exists():
                continue

            meta_file = b_dir / "metadata.yaml"
            metadata: Dict[str, Any] = {}
            if meta_file.exists():
                try:
                    metadata = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
                except Exception:
                    pass

            source_files = [
                f for f in sorted(sources_dir.iterdir())
                if f.is_file()
                and f.suffix.lower() in SOURCE_EXTENSIONS
                and not f.name.startswith(".")
                and f.name.lower() not in SYSTEM_IGNORE_FILES
            ]

            for s_file in source_files:
                total_files += 1
                file_sha = compute_sha256(s_file)
                file_size_kb = round(s_file.stat().st_size / 1024, 1)
                remote_target = self.get_remote_target(cat, slug, s_file.name, metadata)
                local_vault_file = self.get_local_vault_file_path(cat, slug, s_file.name, metadata)

                # Check if identical in local mount or remote cache
                is_identical = False
                if local_vault_file and local_vault_file.exists():
                    if local_vault_file.stat().st_size == s_file.stat().st_size:
                        is_identical = True
                else:
                    target_rel = remote_target.replace(self.remote, "").lower()
                    if target_rel in remote_vault_files:
                        is_identical = True

                rel_src = s_file.relative_to(self.root_dir)
                if is_identical:
                    up_to_date_count += 1
                    if self.verbose:
                        print(f"  ✅ Up-to-Date: {rel_src} ({file_size_kb} KB) -> {remote_target}")
                    continue

                if self.dry_run:
                    uploaded_count += 1
                    print(f"  📤 [DRY-RUN] Uploaded dự kiến: {rel_src} ({file_size_kb} KB) -> {remote_target}")
                else:
                    print(f"  🚀 Uploading: {rel_src} ({file_size_kb} KB) -> {remote_target}")
                    success = False

                    # Try rclone copyto
                    if self.rclone_bin:
                        success = self.execute_rclone_copy(str(s_file), remote_target)

                    # Fallback to local mount copy
                    if not success and local_vault_file:
                        try:
                            local_vault_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(str(s_file), str(local_vault_file))
                            success = True
                            if self.verbose:
                                print(f"    [Local Mount Copy]: Synced to {local_vault_file}")
                        except Exception as e:
                            print(f"    ❌ Error copying to local mount: {e}")

                    if success:
                        uploaded_count += 1
                        print(f"    ✅ Done: {s_file.name} -> {remote_target}")
                    else:
                        failed_count += 1
                        print(f"    ❌ Failed to upload: {rel_src} -> {remote_target}")

        print("\n-----------------------------------------------------------------")
        print("PUSH EXECUTION SUMMARY:")
        print(f"  Total physical files inspected : {total_files}")
        print(f"  Already Up-to-Date in Vault   : {up_to_date_count}")
        action_label = "Pending upload (dry-run)" if self.dry_run else "Successfully Uploaded"
        print(f"  {action_label:<30}: {uploaded_count}")
        if not self.dry_run:
            print(f"  Failed uploads                 : {failed_count}")
        print("-----------------------------------------------------------------")

        if self.dry_run:
            print("✅ Dry-run completed successfully. No changes made.")
            return True

        if failed_count == 0:
            print("✅ All source assets successfully pushed to Google Drive Vault!")
            return True

        print("❌ Some assets failed to push.")
        return False

    def verify_sources(self) -> bool:
        """Verifies integrity of local and vault assets against metadata."""
        bundle_dirs = self.get_bundle_dirs()
        print("=================================================================")
        print("     CCBA LEGAL SPOKE — CLOUD VAULT INTEGRITY VERIFICATION       ")
        print("=================================================================")
        print(f"Target Spoke : {self.root_dir}")
        print(f"Remote Vault : {self.remote}{self.vault_root}")
        print(f"Local Drive  : {self.local_vault_root or 'Not mounted locally (rclone mode)'}")
        print(f"Bundles Found: {len(bundle_dirs)}\n")

        total_assets = 0
        verified_count = 0
        missing_local_count = 0
        missing_vault_count = 0
        mismatch_count = 0

        remote_vault_files = self.get_remote_vault_files()

        for cat, slug, b_dir in bundle_dirs:
            meta_file = b_dir / "metadata.yaml"
            if not meta_file.exists():
                continue

            try:
                metadata = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
            except Exception:
                continue

            sources_dir = b_dir / "sources"
            source_assets = metadata.get("source_assets", {})

            if isinstance(source_assets, dict) and source_assets:
                for asset_type, info in source_assets.items():
                    if not isinstance(info, dict):
                        continue
                    total_assets += 1
                    status = str(info.get("status", "verified")).lower()
                    expected_sha = info.get("sha256", "").strip().lower()
                    vault_path = str(info.get("vault_path", "")).replace("\\", "/")
                    filename = Path(vault_path).name if vault_path else f"{slug}.{asset_type}"

                    local_file = sources_dir / filename
                    local_vault_file = self.get_local_vault_file_path(cat, slug, filename, metadata)

                    # 1. Local Verification
                    local_ok = False
                    if local_file.exists():
                        actual_sha = compute_sha256(local_file)
                        if expected_sha and actual_sha != expected_sha:
                            mismatch_count += 1
                            print(f"  ❌ Mismatch [{slug}/{filename}]: Expected {expected_sha[:8]} != Actual {actual_sha[:8]}")
                        else:
                            local_ok = True
                    elif status in {"pending_acquisition", "missing_upstream"}:
                        local_ok = True
                    else:
                        missing_local_count += 1

                    # 2. Vault Verification
                    vault_ok = False
                    if status in {"pending_acquisition", "missing_upstream"}:
                        vault_ok = True  # Explicitly documented exception
                    elif local_vault_file and local_vault_file.exists():
                        vault_ok = True
                    else:
                        target_key = vault_path.lower()
                        if target_key in remote_vault_files:
                            vault_ok = True

                    if not vault_ok:
                        missing_vault_count += 1
                        print(f"  ❌ Missing in Vault [{slug}/{filename}]: {vault_path}")

                    if local_ok and vault_ok:
                        verified_count += 1

        print("\n-----------------------------------------------------------------")
        print("VERIFICATION SUMMARY:")
        print(f"  Total source assets declared : {total_assets}")
        print(f"  Verified assets (local+vault): {verified_count}")
        print(f"  Missing locally (gitignored) : {missing_local_count}")
        print(f"  Missing in Vault             : {missing_vault_count}")
        print(f"  SHA-256 Mismatches           : {mismatch_count}")
        print("-----------------------------------------------------------------")

        if missing_local_count > 0:
            print(f"  ℹ️ Notice: {missing_local_count} source assets not hydrated locally. Run 'python scripts/hydrate_sources_from_vault.py --all' to download.")

        if mismatch_count == 0 and missing_vault_count == 0:
            print("✅ All source assets verified without corruption or mismatch!")
            return True

        print(f"❌ Integrity issues detected: {missing_vault_count} missing in Vault, {mismatch_count} SHA mismatches.")
        return False

    def hydrate_all(self) -> bool:
        """Pulls / hydrates missing source files from Google Drive Vault with Self-Healing."""
        bundle_dirs = self.get_bundle_dirs()
        print("=================================================================")
        print("       CCBA LEGAL SPOKE — CLOUD VAULT HYDRATION PIPELINE         ")
        print("=================================================================")
        print(f"Target Spoke : {self.root_dir}")
        print(f"Remote Vault : {self.remote}{self.vault_root}")
        print(f"Bundles Found: {len(bundle_dirs)}\n")

        downloaded_count = 0
        failed_count = 0

        for cat, slug, b_dir in bundle_dirs:
            meta_file = b_dir / "metadata.yaml"
            if not meta_file.exists():
                continue
            try:
                metadata = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
            except Exception:
                continue

            sources_dir = b_dir / "sources"
            sources_dir.mkdir(parents=True, exist_ok=True)

            source_assets = metadata.get("source_assets", {})
            if isinstance(source_assets, dict):
                for asset_type, info in source_assets.items():
                    if not isinstance(info, dict):
                        continue
                    status = str(info.get("status", "verified")).lower()
                    if status in {"pending_acquisition", "missing_upstream"}:
                        continue

                    expected_sha = info.get("sha256", "").strip().lower()
                    vault_path = str(info.get("vault_path", "")).replace("\\", "/")
                    if not vault_path:
                        continue
                    filename = Path(vault_path).name
                    local_file = sources_dir / filename

                    # Self-Healing Check: Already present and valid?
                    if local_file.exists():
                        actual_sha = compute_sha256(local_file)
                        if expected_sha and actual_sha == expected_sha:
                            continue  # Clean & verified
                        elif not expected_sha and local_file.stat().st_size > 0:
                            continue
                        else:
                            print(f"  ⚠️ Corrupt local file detected for [{slug}]: {filename}. Re-downloading...")

                    remote_src = f"{self.remote}{vault_path}"
                    local_vault_file = self.get_local_vault_file_path(cat, slug, filename, metadata)

                    print(f"  📥 Hydrating [{slug}]: {remote_src} -> {local_file.name}")
                    success = False

                    # Try direct copy from local mount first (fast path)
                    if local_vault_file and local_vault_file.exists():
                        try:
                            shutil.copy2(str(local_vault_file), str(local_file))
                            success = True
                        except Exception:
                            pass

                    # Try rclone copyto
                    if not success and self.rclone_bin:
                        success = self.execute_rclone_copy(remote_src, str(local_file))

                    # Post-Download Cryptographic Verification (ADR 0059)
                    if success and local_file.exists():
                        actual_sha = compute_sha256(local_file)
                        if expected_sha and actual_sha != expected_sha:
                            print(f"    ❌ Downloaded file SHA mismatch! Removing corrupt file {filename}")
                            local_file.unlink(missing_ok=True)
                            success = False

                    if success:
                        downloaded_count += 1
                        print(f"    ✅ Hydrated & Verified: {filename}")
                    else:
                        failed_count += 1
                        print(f"    ❌ Failed to hydrate: {filename}")

        print("\n-----------------------------------------------------------------")
        print(f"HYDRATION COMPLETE: Downloaded: {downloaded_count} | Failed: {failed_count}")
        print("-----------------------------------------------------------------")
        return failed_count == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="CCBA Legal Spoke — Cloud Vault Hydration & Sync Engine")
    parser.add_argument("--push", action="store_true", help="Push local sources to Google Drive Cloud Vault")
    parser.add_argument("--all", action="store_true", help="Hydrate (download) all missing sources from Cloud Vault")
    parser.add_argument("--verify-only", action="store_true", help="Verify integrity of local sources and vault")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without writing or uploading")
    parser.add_argument("--remote", default=DEFAULT_REMOTE, help="Rclone remote prefix (default: gdrive:)")
    parser.add_argument("--vault-root", default=DEFAULT_VAULT_ROOT, help="Remote vault root directory")
    parser.add_argument("--category", choices=CATEGORIES, help="Filter by category")
    parser.add_argument("--bundle", help="Filter by specific bundle slug")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    engine = VaultHydrationEngine(
        remote=args.remote,
        vault_root=args.vault_root,
        category=args.category,
        bundle=args.bundle,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )

    if args.push:
        success = engine.push_sources()
    elif args.verify_only:
        success = engine.verify_sources()
    elif args.all:
        success = engine.hydrate_all()
    else:
        success = engine.verify_sources()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
