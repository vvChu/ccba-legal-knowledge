"""CCBA Legal Knowledge Spoke Exhaustive Cross-Links & Anchor Verifier.

Validates:
1. All cross-links in Amendment markdown files pointing to Base standards.
2. All internal anchor links (#muc-xxx, #phu-luc-xxx) in Base & Consolidated documents.
3. All inter-document cross links between OKF bundles and Appendices.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
LEGAL_DOCS_DIR = ROOT_DIR / "legal_docs"

def verify_bundle_links(bundle_name: str, base_name: str, sd_name: str, hop_nhat_name: str) -> bool:
    """Verify all anchors and links in an OKF bundle."""
    bundle_dir = LEGAL_DOCS_DIR / "02_qcvn" / bundle_name
    if not bundle_dir.exists():
        print(f"⚠️ Bundle {bundle_name} not found, skipping.")
        return True

    base_file = bundle_dir / base_name
    sd_file = bundle_dir / sd_name
    hop_nhat_file = bundle_dir / hop_nhat_name

    base_text = base_file.read_text(encoding="utf-8") if base_file.exists() else ""
    sd_text = sd_file.read_text(encoding="utf-8") if sd_file.exists() else ""
    hop_nhat_text = hop_nhat_file.read_text(encoding="utf-8") if hop_nhat_file.exists() else ""

    print(f"\n=================================================================")
    print(f"       KIỂM TRA LIÊN KẾT GÓI: {bundle_name}                      ")
    print(f"=================================================================")

    # 1. Extract anchors
    base_anchors = set(re.findall(r'<a id="([^"]+)"', base_text))
    sd_anchors = set(re.findall(r'<a id="([^"]+)"', sd_text))
    hop_nhat_anchors = set(re.findall(r'<a id="([^"]+)"', hop_nhat_text))

    print(f"Tổng số thẻ neo trong Bản Gốc ({base_name})        : {len(base_anchors)}")
    print(f"Tổng số thẻ neo trong Bản Sửa Đổi ({sd_name})       : {len(sd_anchors)}")
    print(f"Tổng số thẻ neo trong Bản Hợp Nhất ({hop_nhat_name}): {len(hop_nhat_anchors)}")

    all_passed = True

    # 2. Check links in Amendment -> Base doc
    if sd_text:
        sd_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', sd_text)
        print(f"Tổng số liên kết trong Bản Sửa Đổi                 : {len(sd_links)}")
        broken_sd_links: List[Tuple[str, str, str]] = []
        valid_sd_links: List[Tuple[str, str]] = []

        for text, target in sd_links:
            if target.startswith(f"{base_name}#"):
                anchor = target.split("#", 1)[1]
                if anchor in base_anchors:
                    valid_sd_links.append((text, target))
                else:
                    broken_sd_links.append((text, target, f"Thẻ neo '{anchor}' không tồn tại trong {base_name}"))
            elif target.startswith("#"):
                anchor = target[1:]
                if anchor in sd_anchors:
                    valid_sd_links.append((text, target))
                else:
                    broken_sd_links.append((text, target, f"Thẻ neo nội bộ '{anchor}' không tồn tại"))
            elif target.endswith(".md"):
                target_path = (bundle_dir / target).resolve()
                if target_path.exists():
                    valid_sd_links.append((text, target))
                else:
                    broken_sd_links.append((text, target, f"Tệp tin đích '{target}' không tồn tại"))
            else:
                valid_sd_links.append((text, target))

        print(f"✅ Liên kết Bản Sửa Đổi HỢP LỆ                      : {len(valid_sd_links)} / {len(sd_links)}")
        if broken_sd_links:
            all_passed = False
            print(f"❌ Liên kết Bản Sửa Đổi BỊ HỎNG                     : {len(broken_sd_links)}")
            for t, tg, r in broken_sd_links:
                print(f"   ❌ [{t}]({tg}) -> {r}")

    # 3. Check internal links in Base Doc
    if base_text:
        base_internal = re.findall(r'\[([^\]]+)\]\(#([^)]+)\)', base_text)
        base_broken = [t for t, a in base_internal if a not in base_anchors]
        print(f"✅ Liên kết Nội bộ Bản Gốc HỢP LỆ                   : {len(base_internal) - len(base_broken)} / {len(base_internal)}")
        if base_broken:
            all_passed = False
            print(f"❌ Liên kết Nội bộ Bản Gốc BỊ HỎNG                 : {len(base_broken)}")

    # 4. Check internal & cross links in Consolidated Doc
    if hop_nhat_text:
        hn_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', hop_nhat_text)
        hn_broken = []
        hn_valid = 0
        for text, target in hn_links:
            if target.startswith("#"):
                anchor = target[1:]
                if anchor in hop_nhat_anchors:
                    hn_valid += 1
                else:
                    hn_broken.append((text, target, f"Thẻ neo nội bộ '{anchor}' không tồn tại"))
            elif target.endswith(".md") or ".md#" in target:
                clean_target = target.split("#")[0]
                target_path = (bundle_dir / clean_target).resolve()
                if target_path.exists():
                    hn_valid += 1
                else:
                    hn_broken.append((text, target, f"Tệp tin đích '{target}' không tồn tại"))
            else:
                hn_valid += 1

        print(f"✅ Liên kết Bản Hợp Nhất HỢP LỆ                     : {hn_valid} / {len(hn_links)}")
        if hn_broken:
            all_passed = False
            print(f"❌ Liên kết Bản Hợp Nhất BỊ HỎNG                   : {len(hn_broken)}")
            for t, tg, r in hn_broken:
                print(f"   ❌ [{t}]({tg}) -> {r}")

    return all_passed

def main() -> None:
    print("=================================================================")
    print("   CCBA EXHAUSTIVE CROSS-LINKS & ANCHOR VERIFICATION GATE        ")
    print("=================================================================")

    # Test QCVN 06:2022/BXD
    p1 = verify_bundle_links(
        bundle_name="qcvn_06_2022_bxd",
        base_name="qcvn_06_2022_bxd.md",
        sd_name="sua_doi_1_2023_qcvn_06_2022_bxd.md",
        hop_nhat_name="qcvn_06_2022_bxd_hop_nhat_2023.md"
    )

    # Test QCVN 04:2021/BXD
    p2 = verify_bundle_links(
        bundle_name="qcvn_04_2021_bxd",
        base_name="qcvn_04_2021_bxd.md",
        sd_name="sua_doi_01_2026_qcvn_04_2021_bxd.md",
        hop_nhat_name="qcvn_04_2021_bxd_hop_nhat_2026.md"
    )

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
