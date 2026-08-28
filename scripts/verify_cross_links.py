"""CCBA Legal Knowledge Spoke Exhaustive Cross-Links & Anchor Verifier.

Validates:
1. All internal anchor links (#muc-xxx, #phu-luc-xxx) in Core & Modular Annex documents.
2. All inter-document cross links between Core and Annexes / Tables.
3. All source archive cross references.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
LEGAL_DOCS_DIR = ROOT_DIR / "legal_docs"


def _check_local_anchor(
    anchor: str,
    rel_key: str,
    file_anchors: Dict[str, Set[str]],
) -> bool:
    """Checks if anchor exists in current file or any file in bundle."""
    if anchor in file_anchors.get(rel_key, set()):
        return True
    return any(anchor in anc_set for anc_set in file_anchors.values())


def _check_relative_link(
    target_clean: str,
    rel_key: str,
    bundle_dir: Path,
    file_anchors: Dict[str, Set[str]],
) -> tuple[bool, str]:
    """Validates relative file link and optional anchor target."""
    parts = target_clean.split("#", 1)
    target_rel_path = parts[0]
    target_anchor = parts[1] if len(parts) > 1 else None

    current_dir = (bundle_dir / rel_key).parent
    target_file_path = (current_dir / target_rel_path).resolve()

    if not target_file_path.exists():
        # Fallback check in bundle's sources/ directory for binary assets (ADR 0036)
        sources_candidate = bundle_dir / "sources" / Path(target_rel_path).name
        if sources_candidate.exists():
            target_file_path = sources_candidate
        else:
            return False, f"Tệp tin đích '{target_rel_path}' không tồn tại"

    if target_anchor:
        target_rel_key = (
            str(target_file_path.relative_to(bundle_dir)).replace("\\", "/")
            if target_file_path.is_relative_to(bundle_dir)
            else None
        )
        if target_rel_key and target_rel_key in file_anchors:
            if target_anchor not in file_anchors[target_rel_key]:
                return False, f"Thẻ neo '#{target_anchor}' không tồn tại trong {target_rel_key}"

    return True, ""


def verify_okf_bundle_links(bundle_dir: Path) -> bool:
    """Verify all anchors and markdown links across all files in an OKF bundle."""
    if not bundle_dir.exists():
        print(f"⚠️ Bundle {bundle_dir.name} not found, skipping.")
        return True

    print("\n=================================================================")
    print(f"       KIỂM TRA LIÊN KẾT GÓI: {bundle_dir.name}                  ")
    print("=================================================================")

    md_files = list(bundle_dir.rglob("*.md"))
    file_anchors: Dict[str, Set[str]] = {}
    file_contents: Dict[str, str] = {}

    total_anchors = 0
    for md_f in md_files:
        rel_key = str(md_f.relative_to(bundle_dir)).replace("\\", "/")
        try:
            text = md_f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        anchors = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
        file_anchors[rel_key] = anchors
        file_contents[rel_key] = text
        total_anchors += len(anchors)

    print(f"Tổng số tệp Markdown kiểm tra   : {len(md_files)}")
    print(f"Tổng số thẻ neo ghi nhận        : {total_anchors}")

    total_links, valid_links = 0, 0
    broken_links: List[Tuple[str, str, str, str]] = []

    for rel_key, text in file_contents.items():
        for link_text, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text):
            total_links += 1
            target_clean = target.strip()
            if target_clean.startswith(("http://", "https://", "mailto:")):
                valid_links += 1
                continue

            if target_clean.startswith("#"):
                anchor = target_clean[1:]
                if _check_local_anchor(anchor, rel_key, file_anchors):
                    valid_links += 1
                else:
                    broken_links.append((rel_key, link_text, target, f"Thẻ neo '#{anchor}' không tồn tại trong tệp"))
            else:
                ok, reason = _check_relative_link(target_clean, rel_key, bundle_dir, file_anchors)
                if ok:
                    valid_links += 1
                else:
                    broken_links.append((rel_key, link_text, target, reason))

    print(f"✅ Liên kết HỢP LỆ                      : {valid_links} / {total_links}")
    if broken_links:
        print(f"❌ Liên kết BỊ HỎNG                     : {len(broken_links)}")
        for f, t, tg, r in broken_links:
            print(f"   ❌ [{f}] -> [{t}]({tg}): {r}")

    return len(broken_links) == 0


def discover_bundles(root_legal_docs: Path, filter_name: str | None = None) -> list[Path]:
    """Find all OKF bundle directories across 01_vbpl, 02_qcvn, and 03_tcvn."""
    bundles: list[Path] = []
    for cat in ["01_vbpl", "02_qcvn", "03_tcvn"]:
        cat_dir = root_legal_docs / cat
        if not cat_dir.exists():
            continue
        for child in sorted(cat_dir.iterdir()):
            if child.is_dir() and not child.name.startswith("."):
                if filter_name and filter_name not in child.name:
                    continue
                bundles.append(child)
    return bundles


def main() -> int:
    """CLI dispatcher to verify links across bundles."""
    parser = argparse.ArgumentParser(description="CCBA Exhaustive Cross-Links & Anchor Verifier")
    parser.add_argument("-b", "--bundle", type=str, default=None, help="Filter by specific bundle name")
    args = parser.parse_args()

    print("=================================================================")
    print("   CCBA EXHAUSTIVE CROSS-LINKS & ANCHOR VERIFICATION GATE        ")
    print("=================================================================")

    bundles = discover_bundles(LEGAL_DOCS_DIR, filter_name=args.bundle)
    if not bundles:
        print("⚠️ Không tìm thấy gói văn bản nào để kiểm tra.")
        return 0

    print(f"Đã phát hiện {len(bundles)} gói văn bản tri thức.")
    all_passed = True
    for bundle in bundles:
        passed = verify_okf_bundle_links(bundle)
        if not passed:
            all_passed = False

    print("\n-----------------------------------------------------------------")
    if all_passed:
        print("🎉 TẤT CẢ LIÊN KẾT TRÊN TOÀN BỘ KHO TRI THỨC ĐỀU CHÍNH XÁC NƠI ĐÍCH 100%!")
        print("=================================================================")
        return 0
    else:
        print("❌ PHÁT HIỆN LIÊN KẾT BỊ HỎNG TRONG SPOKE!")
        print("=================================================================")
        return 1


if __name__ == "__main__":
    sys.exit(main())

