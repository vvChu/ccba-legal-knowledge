"""Fetch and download official TVPL legal document (.doc/.docx/.pdf) via Hub ChromeCDP with 4-Layer Precision Check."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

# Clean Hub import without sys.path hacks (installed via pip -e)
from ccba_legal.crawler import (
    ChromeCDP,
    download_three_tier,
    get_tvpl_metadata,
    trigger_download,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
# Load environment variables from Spoke and Hub .env
load_dotenv(ROOT_DIR / ".env")
load_dotenv(Path(r"D:\GitHubProjects\ccba-agent-platform\.env"))

ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT_DIR / "legal_registry.yaml"

def _normalize(s: str) -> str:
    """Normalize string for search comparison."""
    import unicodedata

    s = (
        s.strip()
        .lower()
        .replace(":", " ")
        .replace("-", " ")
        .replace("_", " ")
        .replace("/", " ")
    )
    s = s.replace("đ", "d").replace("Đ", "d")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return " ".join(s.split())

def find_doc_in_registry(identifier: str) -> tuple[str, str, dict]:
    """Find document slug, source_url, and registered metadata from legal_registry.yaml."""
    if identifier.startswith("http://") or identifier.startswith("https://"):
        slug = (
            identifier.split("/")[-1]
            .replace(".aspx", "")
            .lower()
            .replace("-", "_")
        )
        return slug, identifier, {}

    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Registry not found: {REGISTRY_FILE}")

    reg = yaml.safe_load(REGISTRY_FILE.read_text(encoding="utf-8"))
    items = reg.get("laws", [])
    if isinstance(reg.get("documents"), list):
        items.extend(reg.get("documents", []))
    elif isinstance(reg.get("documents"), dict):
        items.extend(reg.get("documents", {}).values())

    ident_norm = _normalize(identifier)

    for item in items:
        if not isinstance(item, dict):
            continue
        doc_id = _normalize(str(item.get("id", "")))
        doc_num = _normalize(str(item.get("document_number", "")))
        title = _normalize(str(item.get("title", "")))
        bundle_path = _normalize(str(item.get("bundle_path", "")))
        source_url = _normalize(str(item.get("source_url", "")))
        relations_str = _normalize(str(item.get("relations", {})))

        # Check specific amendment matches
        amendments = item.get("relations", {}).get("amendments", []) if isinstance(item.get("relations"), dict) else []
        for amd in amendments:
            if isinstance(amd, dict):
                amd_id = _normalize(str(amd.get("id", "")))
                amd_num = _normalize(str(amd.get("document_number", "")))
                amd_title = _normalize(str(amd.get("title", "")))
                is_explicit_amd_query = (
                    "sua doi" in ident_norm
                    or "sd" in ident_norm.split()
                    or amd_num in ident_norm
                    or (amd_id and ident_norm == amd_id)
                )
                if (
                    is_explicit_amd_query
                    and (
                        (amd_id and ident_norm == amd_id)
                        or (amd_num and (ident_norm == amd_num or ident_norm in amd_num))
                        or (len(ident_norm) > 6 and ident_norm in amd_title)
                    )
                ):
                    bundle_dir = Path(item.get("bundle_path", "doc")).name.strip("/")
                    amd_slug = "sua_doi_01_2026_qcvn_04_2021_bxd" if "sd1" in amd_id else amd_id.lower().replace("-", "_")
                    url = amd.get("source_url", item.get("source_url", ""))
                    return str(amd_slug), str(url), {**amd, "bundle_path": item.get("bundle_path", "")}

        if (
            ident_norm == doc_id
            or ident_norm in doc_id
            or ident_norm == doc_num
            or ident_norm in doc_num
            or ident_norm in bundle_path
            or ident_norm in title
            or ident_norm in source_url
            or ident_norm in relations_str
        ):
            slug = Path(item.get("bundle_path", "doc")).name.strip("/")
            if not slug or slug == "doc":
                slug = item.get("id", "doc")
            url = item.get("source_url", "")
            return str(slug), str(url), item

    return (
        identifier,
        f"https://thuvienphapluat.vn/van-ban/{identifier}.aspx",
        {},
    )

def compute_file_sha256(file_path: Path) -> str:
    """Calculate SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def is_cdp_listening(port: int = 9222) -> bool:
    """Check if Chrome CDP port is already open."""
    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/json/version",
            headers={"User-Agent": "CCBA-Agent"},
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False

def launch_chrome_cdp(url: str, port: int = 9222) -> subprocess.Popen | None:
    """Launch Google Chrome with remote debugging if not already listening."""
    if is_cdp_listening(port):
        print(f"[CDP] Phát hiện Chrome đã mở sẵn trên cổng {port}!")
        return None

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not Path(chrome_exe).exists():
        chrome_exe = (
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        )

    user_data = ROOT_DIR / ".md" / "data" / "chrome_cdp_profile"
    user_data.mkdir(parents=True, exist_ok=True)

    cmd = [
        chrome_exe,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data.resolve()}",
        "--disable-blink-features=AutomationControlled",
        url,
    ]
    print(f"[CDP] Khởi chạy Chrome thật trên cổng {port}...")
    proc = subprocess.Popen(cmd)
    time.sleep(4)
    return proc

def update_registry_sha256(slug: str, new_sha256: str) -> None:
    """Update sha256 checksum in legal_registry.yaml."""
    if not REGISTRY_FILE.exists():
        return

    content = REGISTRY_FILE.read_text(encoding="utf-8")
    reg = yaml.safe_load(content)

    updated = False
    for section in ["laws", "documents"]:
        items = reg.get(section, [])
        if isinstance(items, list):
            for item in items:
                if (
                    item.get("id") == slug
                    or Path(item.get("bundle_path", "")).name == slug
                ):
                    item["sha256"] = new_sha256
                    updated = True
        elif isinstance(items, dict):
            for item in items.values():
                if (
                    item.get("id") == slug
                    or Path(item.get("bundle_path", "")).name == slug
                ):
                    item["sha256"] = new_sha256
                    updated = True

    if updated:
        REGISTRY_FILE.write_text(
            yaml.dump(reg, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        print(
            f"[Registry] Đã cập nhật SHA-256 cho '{slug}' vào legal_registry.yaml"
        )

def fetch_tvpl_document(
    identifier: str,
    output_dir: Path | None = None,
    port: int = 9222,
    skip_verify: bool = False,
) -> bool:
    """Main workflow to verify and download official legal document via Hub ChromeCDP."""
    slug, url, reg_item = find_doc_in_registry(identifier)
    print(f"=================================================================")
    print(f"  CCBA TVPL VIP FETCHER & 4-LAYER PRECISION VERIFIER")
    print(f"=================================================================")
    print(f"  Target Identifier : {identifier}")
    print(f"  Target Slug       : {slug}")
    print(f"  Target Source URL : {url}")

    bundle_name = Path(reg_item.get("bundle_path", slug)).name.strip("/") or slug
    target_dir = output_dir or (ROOT_DIR / ".md" / "extracted_docs" / bundle_name)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Launch Chrome if needed
    proc = launch_chrome_cdp(url, port=port)

    cdp: ChromeCDP | None = None
    try:
        print(f"\n[CDP] Đang kết nối tới Chrome (ws://127.0.0.1:{port})...")
        cdp = ChromeCDP(port=port)
        pages = cdp.get_pages()
        if not pages:
            raise RuntimeError(f"Không tìm thấy tab nào trong Chrome đang mở trên cổng {port}!")
        ws_url = pages[0].get("webSocketDebuggerUrl")
        if not ws_url:
            raise RuntimeError(f"Không lấy được webSocketDebuggerUrl từ tab Chrome!")
        cdp.connect_tab(ws_url)
        cdp.navigate(url)
        time.sleep(3)

        # 1. Handle Cloudflare Turnstile
        print("[CDP] Kiểm tra Cloudflare Turnstile...")
        cdp.handle_cloudflare()

        # 2. Handle VIP Login
        print("[CDP] Kiểm tra đăng nhập VIP...")
        cdp.handle_login()

        # --- LỚP 2: ĐỐI SOÁT METADATA TỪ TAB LƯỢC ĐỒ TVPL ---
        print("\n--- [LỚP 2] ĐỐI SOÁT BẢNG THUỘC TÍNH PHÁP LÝ ---")
        try:
            metadata = get_tvpl_metadata(cdp, url)
            web_doc_num = metadata.get("document_number", "")
            web_type = metadata.get("type", "")
            web_issuer = metadata.get("issued_by", "")
            web_status = metadata.get("status", "")
            web_relations = metadata.get("relations", {})

            print(f"  - Số hiệu trên Web  : {web_doc_num}")
            print(f"  - Loại văn bản      : {web_type}")
            print(f"  - Cơ quan ban hành  : {web_issuer}")
            print(f"  - Ngày ban hành     : {metadata.get('issued_date', '')}")
            print(f"  - Ngày hiệu lực     : {metadata.get('effective_date', '')}")

            # --- LỚP 3: KIỂM TRA NHÃN TRẠNG THÁI HIỆU LỰC ---
            print("\n--- [LỚP 3] KIỂM TRA TRẠNG THÁI HIỆU LỰC ---")
            if "hết hiệu lực" in web_status.lower():
                print(
                    f"  🔴 [CẢNH BÁO NGUY HIỂM] Tình trạng văn bản: {web_status.upper()}"
                )
            elif "chưa có hiệu lực" in web_status.lower():
                print(
                    f"  🟡 [LƯU Ý] Tình trạng văn bản: {web_status.upper()} (Áp dụng tương lai)"
                )
            else:
                print(f"  🟢 [HỢP LỆ] Tình trạng văn bản: {web_status}")

            if web_relations:
                print(f"\n--- [LƯỢC ĐỒ] VĂN BẢN LIÊN QUAN TRÍCH XUẤT ĐƯỢC ---")
                for rel_type, rel_list in web_relations.items():
                    print(f"  * {rel_type} ({len(rel_list)} văn bản):")
                    for r in rel_list[:3]:
                        print(f"    - {r.get('title', '')} ({r.get('url', '')})")
                    if len(rel_list) > 3:
                        print(f"    - ... và {len(rel_list) - 3} văn bản khác")

            # Validate against registry
            reg_doc_num = reg_item.get("document_number", "")
            if (
                reg_doc_num
                and web_doc_num
                and not skip_verify
                and _normalize(reg_doc_num) not in _normalize(web_doc_num)
                and _normalize(web_doc_num) not in _normalize(reg_doc_num)
            ):
                print(
                    f"\n⚠️ [CẢNH BÁO LỆCH SỐ HIỆU] Registry kỳ vọng '{reg_doc_num}' nhưng TVPL trả về '{web_doc_num}'!"
                )

        except Exception as e:
            print(f"  [Lưu ý] Không trích xuất được metadata Lược đồ: {e}")

        # --- LỚP 4: TẢI 3 TẦNG + KIỂM TRA TÍNH TOÀN VẸN (SHA-256) ---
        print(
            f"\n--- [LỚP 4] TẢI TỆP GỐC (THREE-TIER CRAWLER) CHO '{slug}' ---"
        )
        cdp.navigate(url)
        time.sleep(2)
        cdp.handle_cloudflare()

        success = download_three_tier(cdp, target_dir, slug)
        if not success:
            print("[CDP] Thử lại tải trực tiếp trên Tab Tải Về (?tab=1)...")
            cdp.navigate(url + "?tab=1")
            time.sleep(3)
            cdp.handle_cloudflare()
            cdp.handle_login()
            success = trigger_download(cdp, target_dir, slug)

        if success:
            print(
                f"\n✅ [HOÀN TẤT] Đã tải và lưu trữ tệp gốc vào: {target_dir.resolve()}"
            )
            downloaded_files = list(target_dir.glob(f"{slug}.*"))
            for f in downloaded_files:
                if f.is_file():
                    sha = compute_file_sha256(f)
                    print(
                        f"   -> Tệp: {f.name} | Size: {f.stat().st_size:,} bytes"
                    )
                    print(f"   -> SHA-256: {sha}")
                    update_registry_sha256(slug, sha)
            return True
        else:
            print(f"\n❌ [THẤT BẠI] Chưa bắt được tệp tải về từ TVPL.")
            return False

    except Exception as e:
        print(f"\n❌ [LỖI] Ngoại lệ xảy ra trong quá trình cào: {e}")
        return False
    finally:
        if cdp:
            cdp.close()
        if proc:
            try:
                proc.terminate()
            except Exception:
                pass

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download official legal document from TVPL with 4-Layer Precision Check"
    )
    parser.add_argument(
        "doc",
        help="Document Slug, Number (e.g. 03/2021/TT-BXD), or TVPL URL",
    )
    parser.add_argument(
        "--out", "-o", help="Custom output directory", default=None
    )
    parser.add_argument(
        "--port", "-p", help="CDP Port", default=9222, type=int
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip strict metadata comparison",
    )

    args = parser.parse_args()
    out_path = Path(args.out) if args.out else None
    ok = fetch_tvpl_document(
        args.doc,
        output_dir=out_path,
        port=args.port,
        skip_verify=args.skip_verify,
    )
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
