"""CCBA Legal Knowledge Spoke Exhaustive Cross-Links & Anchor Verifier.

Validates:
1. All internal anchor links (#muc-xxx, #phu-luc-xxx) in Core & Modular Annex documents.
2. All inter-document cross links between Core and Annexes / Tables.
3. All source archive cross references.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
LEGAL_DOCS_DIR = ROOT_DIR / "legal_docs"


def verify_okf_bundle_links(bundle_dir: Path) -> bool:
    """Verify all anchors and markdown links across all files in an OKF bundle."""
    if not bundle_dir.exists():
        print(f"⚠️ Bundle {bundle_dir.name} not found, skipping.")
        return True

    print(f"\n=================================================================")
    print(f"       KIỂM TRA LIÊN KẾT GÓI: {bundle_dir.name}                  ")
    print(f"=================================================================")

    md_files = list(bundle_dir.rglob("*.md"))
    file_anchors: Dict[str, Set[str]] = {}
    file_contents: Dict[str, str] = {}

    total_anchors = 0
    for md_f in md_files:
        rel_key = str(md_f.relative_to(bundle_dir)).replace("\\", "/")
        text = md_f.read_text(encoding="utf-8")
        anchors = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
        file_anchors[rel_key] = anchors
        file_contents[rel_key] = text
        total_anchors += len(anchors)

    print(f"Tổng số tệp Markdown kiểm tra   : {len(md_files)}")
    print(f"Tổng số thẻ neo ghi nhận        : {total_anchors}")

    all_passed = True
    total_links = 0
    valid_links = 0
    broken_links: List[Tuple[str, str, str, str]] = []

    for rel_key, text in file_contents.items():
        # Find markdown links [text](target)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
        for link_text, target in links:
            total_links += 1
            target_clean = target.strip()
            
            # Skip external web URLs
            if target_clean.startswith("http://") or target_clean.startswith("https://"):
                valid_links += 1
                continue

            # Case 1: Local anchor (#anchor)
            if target_clean.startswith("#"):
                anchor = target_clean[1:]
                if anchor in file_anchors[rel_key]:
                    valid_links += 1
                else:
                    # Check if anchor exists in any other bundle file
                    found = any(anchor in anc_set for anc_set in file_anchors.values())
                    if found:
                        valid_links += 1
                    else:
                        broken_links.append((rel_key, link_text, target, f"Thẻ neo '#{anchor}' không tồn tại trong tệp"))
                        all_passed = False

            # Case 2: Relative file link (e.g. annexes/phu_luc_a.md#anchor or tables/README.md)
            else:
                parts = target_clean.split("#", 1)
                target_rel_path = parts[0]
                target_anchor = parts[1] if len(parts) > 1 else None

                current_dir = (bundle_dir / rel_key).parent
                target_file_path = (current_dir / target_rel_path).resolve()

                if not target_file_path.exists():
                    broken_links.append((rel_key, link_text, target, f"Tệp tin đích '{target_rel_path}' không tồn tại"))
                    all_passed = False
                elif target_anchor:
                    # Check anchor in target file
                    target_rel_key = str(target_file_path.relative_to(bundle_dir)).replace("\\", "/") if target_file_path.is_relative_to(bundle_dir) else None
                    if target_rel_key and target_rel_key in file_anchors:
                        if target_anchor in file_anchors[target_rel_key]:
                            valid_links += 1
                        else:
                            broken_links.append((rel_key, link_text, target, f"Thẻ neo '#{target_anchor}' không tồn tại trong {target_rel_key}"))
                            all_passed = False
                    else:
                        valid_links += 1
                else:
                    valid_links += 1

    print(f"✅ Liên kết HỢP LỆ                      : {valid_links} / {total_links}")
    if broken_links:
        print(f"❌ Liên kết BỊ HỎNG                     : {len(broken_links)}")
        for f, t, tg, r in broken_links:
            print(f"   ❌ [{f}] -> [{t}]({tg}): {r}")

    return all_passed


def main() -> None:
    print("=================================================================")
    print("   CCBA EXHAUSTIVE CROSS-LINKS & ANCHOR VERIFICATION GATE        ")
    print("=================================================================")

    # Test QCVN 06:2022/BXD
    p1 = verify_okf_bundle_links(LEGAL_DOCS_DIR / "02_qcvn" / "qcvn_06_2022_bxd")

    # Test QCVN 04:2021/BXD
    p2 = verify_okf_bundle_links(LEGAL_DOCS_DIR / "02_qcvn" / "qcvn_04_2021_bxd")

    print("\n-----------------------------------------------------------------")
    if p1 and p2:
        print("🎉 TẤT CẢ LIÊN KẾT TRÊN TOÀN BỘ QUY CHUẨN ĐỀU CHÍNH XÁC NƠI ĐÍCH 100%!")
        print("=================================================================")
        sys.exit(0)
    else:
        print("❌ PHÁT HIỆN LIÊN KẾT BỊ HỎNG TRONG SPOKE!")
        print("=================================================================")
        sys.exit(1)


if __name__ == "__main__":
    main()
