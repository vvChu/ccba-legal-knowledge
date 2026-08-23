"""CCBA Table of Contents & Single Clause Note Formatter.

1. Fixes Table of Contents at the top of the file: converts pseudo-headings into clickable markdown links.
2. Removes duplicated anchors in TOC so anchor jumps to actual body sections.
3. Formats single clause notes into clean single-line italic paragraphs '_CHÚ THÍCH: ..._', eliminating duplicate headers.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"

def format_single_notes(text: str) -> str:
    # Pattern:
    # _CHÚ THÍCH:_
    # - **CHÚ THÍCH:** <text>
    # (where there's only ONE bullet with **CHÚ THÍCH:**)
    
    # Replace duplicated single notes
    def rep_single(m):
        content = m.group(1).strip()
        return f"_CHÚ THÍCH: {content}_"

    # Match _CHÚ THÍCH:_\n- \*\*CHÚ THÍCH:\*\* ([^\n]+) when not followed by another bullet
    pattern = r"_CHÚ THÍCH:_\n-\s+\*\*CHÚ THÍCH:\*\*\s+([^\n]+)(?!\n-\s+)"
    text = re.sub(pattern, rep_single, text)
    
    return text

def format_toc(text: str) -> str:
    # Find MỤC LỤC section at top
    toc_match = re.search(r"MỤC LỤC\s*\n(.*?)(?=Lời nói đầu|##\s*1\s*QUY ĐỊNH CHUNG|###\s*1\s*QUY ĐỊNH CHUNG)", text, re.DOTALL)
    if not toc_match:
        return text

    toc_raw = toc_match.group(1)
    
    # Build clean TOC
    clean_toc_lines = [
        "## MỤC LỤC\n",
        "- [1  QUY ĐỊNH CHUNG](#muc-1)",
        "- [2  PHÂN LOẠI KỸ THUẬT VỀ CHÁY](#muc-2)",
        "- [3  BẢO ĐẢM AN TOÀN CHO NGƯỜI](#muc-3)",
        "- [4  NGĂN CHẶN CHÁY LAN](#muc-4)",
        "- [5  CẤP NƯỚC CHỮA CHÁY](#muc-5)",
        "- [6  CHỮA CHÁY VÀ CỨU NẠN](#muc-6)",
        "- [7  TỔ CHỨC THỰC HIỆN](#muc-7)",
        "- [PHỤ LỤC A (quy định) QUY ĐỊNH BỔ SUNG ĐỐI VỚI MỘT SỐ NHÓM NHÀ CỤ THỂ](#phu-luc-a)",
        "- [PHỤ LỤC B (quy định) PHÂN LOẠI VẬT LIỆU XÂY DỰNG THEO ĐẶC TÍNH KỸ THUẬT VỀ CHÁY VÀ YÊU CẦU VỀ AN TOÀN CHÁY ĐỐI VỚI VẬT LIỆU](#phu-luc-b)",
        "- [PHỤ LỤC C (quy định) HẠNG NGUY HIỂM CHÁY VÀ CHÁY NỔ CỦA NHÀ, CÔNG TRÌNH VÀ CÁC GIAN PHÒNG CÓ CÔNG NĂNG SẢN XUẤT VÀ KHO](#phu-luc-c)",
        "- [PHỤ LỤC D (quy định) BẢO VỆ CHỐNG KHÓI](#phu-luc-d)",
        "- [PHỤ LỤC E (quy định) KHOẢNG CÁCH PHÒNG CHÁY CHỐNG CHÁY](#phu-luc-e)",
        "- [PHỤ LỤC F (quy định) GIỚI HẠN CHỊU LỬA DANH ĐỊNH CỦA MỘT SỐ CẤU KIỆN](#phu-luc-f)",
        "- [PHỤ LỤC G (quy định) KHOẢNG CÁCH ĐẾN CÁC LỐI RA THOÁT NẠN VÀ CHIỀU RỘNG LỐI RA THOÁT NẠN](#phu-luc-g)",
        "- [PHỤ LỤC H (quy định) BẬC CHỊU LỬA VÀ CÁC YÊU CẦU BẢO ĐẢM AN TOÀN CHÁY CHO NHÀ, CÔNG TRÌNH, KHOANG CHÁY](#phu-luc-h)",
        "- [PHỤ LỤC I (tham khảo) CÁC HÌNH MINH HỌA](#phu-luc-i)\n"
    ]
    clean_toc = "\n".join(clean_toc_lines)

    # Replace MỤC LỤC block
    text = text[:toc_match.start()] + clean_toc + text[toc_match.end():]
    return text

def process_file(fpath: Path) -> None:
    text = fpath.read_text(encoding="utf-8")
    text = format_toc(text)
    text = format_single_notes(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    fpath.write_text(text, encoding="utf-8")
    print(f"✅ Đã chuẩn hóa Mục lục và Chú thích đơn cho: {fpath.name}")

def main() -> None:
    for fn in ["qcvn_06_2022_bxd.md", "qcvn_06_2022_bxd_hop_nhat_2023.md", "sua_doi_1_2023_qcvn_06_2022_bxd.md"]:
        fp = BUNDLE_DIR / fn
        if fp.exists():
            process_file(fp)

if __name__ == "__main__":
    main()
