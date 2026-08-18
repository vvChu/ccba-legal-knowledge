"""CCBA Master Consolidated Legal Text (VBHN) Builder for QCVN 06:2022/BXD.

Generates qcvn_06_2022_bxd_hop_nhat_2023.md integrating 100% of amendments
from TT 09/2023/TT-BXD into the base document with standard GFM callouts.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

sys.stdout.reconfigure(encoding="utf-8")

BUNDLE_DIR = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
BASE_MD = BUNDLE_DIR / "qcvn_06_2022_bxd.md"
SD1_MD = BUNDLE_DIR / "sua_doi_1_2023_qcvn_06_2022_bxd.md"
CLAUSES_SD1_JSON = BUNDLE_DIR / "clauses_sd1.json"
TARGET_VBHN_MD = BUNDLE_DIR / "qcvn_06_2022_bxd_hop_nhat_2023.md"
INDEX_MD = BUNDLE_DIR / "index.md"


def parse_sd1_sections() -> Dict[str, Dict[str, str]]:
    """Extracts all amendment blocks from sua_doi_1_2023_qcvn_06_2022_bxd.md keyed by target clause."""
    sd_text = SD1_MD.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=####\s+<a id=\"sd1-)", sd_text)

    sd_map = {}
    for b in blocks:
        if not b.startswith("####"):
            continue
        lines = b.strip().splitlines()
        header = lines[0]
        body = "\n".join(lines[1:]).strip()

        # Clean header markdown links
        clean_h = re.sub(r"<[^>]+>", "", header)
        clean_h = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean_h).strip("# ").strip()

        # Determine target clause
        m_tbl = re.search(r"Bảng\s+([A-Z0-9.]+)", clean_h, re.IGNORECASE)
        m_app = re.search(r"Phụ lục\s+([A-Z])", clean_h, re.IGNORECASE)
        m_sec = re.search(r"((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)", clean_h)

        key = None
        if m_tbl:
            key = f"bang-{m_tbl.group(1).lower().replace('.', '-')}"
        elif m_app:
            key = f"phu-luc-{m_app.group(1).lower()}"
        elif m_sec:
            key = f"muc-{m_sec.group(1).lower().replace('.', '-')}"

        if key:
            sd_map[key] = {
                "header": clean_h,
                "body": body,
                "raw_block": b.strip()
            }
    return sd_map


def build_consolidated_markdown() -> str:
    sd_map = parse_sd1_sections()
    base_text = BASE_MD.read_text(encoding="utf-8")

    out_lines: List[str] = []

    # 1. Official VBHN Header
    out_lines.append("# QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ AN TOÀN CHÁY CHO NHÀ VÀ CÔNG TRÌNH\n")
    out_lines.append("## (VĂN BẢN HỢP NHẤT — CẬP NHẬT SỬA ĐỔI 1:2023 THEO THÔNG TƯ 09/2023/TT-BXD)\n\n")
    out_lines.append("> [!IMPORTANT]\n")
    out_lines.append("> **VĂN BẢN HỢP NHẤT TOÀN VĂN QUY CHUẨN QCVN 06:2022/BXD:**\n")
    out_lines.append("> - **Văn bản Gốc:** Ban hành kèm theo Thông tư số 06/2022/TT-BXD ngày 30/11/2022 (Hiệu lực từ 16/01/2023).\n")
    out_lines.append("> - **Sửa đổi 1:2023:** Ban hành kèm theo Thông tư số 09/2023/TT-BXD ngày 16/10/2023 (Hiệu lực từ 01/12/2023).\n")
    out_lines.append("> - **Quy ước Hợp nhất:** Các điều khoản, bảng biểu được sửa đổi, bổ sung hoặc bãi bỏ đều được đóng khung ghi chú `> [!NOTE]` nổi bật kèm trích dẫn pháp lý.\n\n")
    out_lines.append("---\n\n")

    # 2. Iterate Base Sections & Inject Callouts
    base_lines = base_text.splitlines()
    in_repealed_clause = False
    in_table_10 = False

    for line in base_lines:
        l = line.strip()

        # Check if line is a Heading with anchor
        m_h = re.match(r"^(#{1,6})\s+<a id=\"([^\"]+)\"[^>]*></a>(.+)$", l)
        if m_h:
            hashes = m_h.group(1)
            slug = m_h.group(2)
            title = m_h.group(3).strip()

            out_lines.append(f"\n{hashes} <a id=\"{slug}\" name=\"{slug}\"></a>{title}\n\n")

            # Check if this slug has an amendment
            if slug in sd_map:
                sd_info = sd_map[slug]
                action_hdr = sd_info["header"]
                action_body = sd_info["body"]

                if "bãi bỏ" in action_hdr.lower():
                    out_lines.append(f"> [!WARNING]\n")
                    out_lines.append(f"> **Đã bãi bỏ theo Sửa đổi 1:2023 (Thông tư 09/2023/TT-BXD)**\n\n")
                else:
                    out_lines.append(f"> [!NOTE]\n")
                    out_lines.append(f"> **{action_hdr} (Thông tư số 09/2023/TT-BXD):**\n")
                    # Indent body into callout
                    for b_line in action_body.splitlines():
                        out_lines.append(f"> {b_line}\n")
                    out_lines.append("\n")

            # Special case for Table 10 replacement
            if slug == "bang-10":
                in_table_10 = True
                continue
            continue

        if in_table_10:
            # Skip old table 10 lines until next heading
            if l.startswith("#"):
                in_table_10 = False
            else:
                continue

        out_lines.append(f"{line}\n")

    # 3. Add Thư mục tài liệu tham khảo at the end if present
    if "sd1-thu-muc-tai-lieu-tham-khao" in sd_map or any("THƯ MỤC TÀI LIỆU THAM KHẢO" in x for x in sd_map):
        out_lines.append("\n\n## <a id=\"thu-muc-tai-lieu-tham-khao\" name=\"thu-muc-tai-lieu-tham-khao\"></a>THƯ MỤC TÀI LIỆU THAM KHẢO\n\n")
        out_lines.append("> [!NOTE]\n")
        out_lines.append("> **Bổ sung Thư mục tài liệu tham khảo theo Sửa đổi 1:2023 (Thông tư số 09/2023/TT-BXD):**\n")
        out_lines.append("> [1] NFPA 5000: Building Construction and Safety Code.\n")
        out_lines.append("> [2] TCVN 13456:2021 Phòng cháy chữa cháy - Phương tiện chiếu sáng sự cố và chỉ dẫn thoát nạn - Yêu cầu thiết kế, lắp đặt.\n")
        out_lines.append("> [3] TCVN 3890:2023 Phòng cháy chữa cháy - Phương tiện phòng cháy và chữa cháy cho nhà và công trình - Trang bị, bố trí.\n")
        out_lines.append("> [4] SP 1.13130.2020 Hệ thống bảo vệ chống cháy - Lối thoát nạn và đường thoát nạn.\n")
        out_lines.append("> [5] SP 2.13130.2020 Hệ thống bảo vệ chống cháy - Bảo đảm bậc chịu lửa cho đối tượng bảo vệ.\n\n")

    full_text = "".join(out_lines)
    full_text = re.sub(r"\n{3,}", "\n\n", full_text)
    return full_text


def update_index_md() -> None:
    content = """# MỤC LỤC BỘ TÀI LIỆU QCVN 06:2022/BXD (OKF BUNDLE)

- [✨ **QCVN 06:2022/BXD (BẢN HỢP NHẤT MỚI NHẤT 2023)**](qcvn_06_2022_bxd_hop_nhat_2023.md) — *Khuyên dùng cho Fast-RAG & Thẩm tra Thiết kế*
- [🔥 QCVN 06:2022/BXD — Toàn văn Quy chuẩn Kỹ thuật Quốc gia Gốc](qcvn_06_2022_bxd.md) — *Ban hành theo Thông tư 06/2022/TT-BXD (Hiệu lực từ 16/01/2023)*
- [⚡ Sửa đổi 1:2023 QCVN 06:2022/BXD — Văn bản Sửa đổi độc lập](sua_doi_1_2023_qcvn_06_2022_bxd.md) — *Ban hành theo Thông tư 09/2023/TT-BXD (Hiệu lực từ 01/12/2023)*
- [📊 Bản đồ Chỉ mục & Tra cứu 64 Bảng Kỹ thuật](tables/README.md) — *Phân loại 10 nhóm bảng, tích hợp cờ Sửa đổi 1:2023 và Ma trận Footnote*
"""
    INDEX_MD.write_text(content, encoding="utf-8")
    print("✅ Đã cập nhật index.md MOC router.")


def main() -> None:
    print("=================================================================")
    print("      BUILDING CONSOLIDATED LEGAL TEXT (VBHN) QCVN 06           ")
    print("=================================================================")

    vbhn_text = build_consolidated_markdown()
    TARGET_VBHN_MD.write_text(vbhn_text, encoding="utf-8")
    print(f"✅ Đã tạo qcvn_06_2022_bxd_hop_nhat_2023.md: {len(vbhn_text):,} ký tự, {len(vbhn_text.splitlines())} dòng.")

    update_index_md()
    print("=================================================================")


if __name__ == "__main__":
    main()
