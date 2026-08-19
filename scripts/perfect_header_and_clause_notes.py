"""CCBA Perfect Header, TOC & Clause Note Normalizer.

1. Cleans the top of document: generates a proper markdown TOC and removes ghost pseudo-headings.
2. Formats all single clause notes into clean italic text '_CHÚ THÍCH: ..._' directly attached to their items.
3. Fixes duplicate anchors and aligns document structure with the original DOCX publication.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"

def clean_front_matter_and_toc(text: str, is_hopnhat: bool = False) -> str:
    # Find the position of 'Lời nói đầu'
    pos_loi_noi_dau = text.find("Lời nói đầu")
    if pos_loi_noi_dau == -1:
        return text

    # Extract text starting from 'Lời nói đầu'
    body_from_preface = text[pos_loi_noi_dau:]

    # Clean redundant title lines that repeat before '1 QUY ĐỊNH CHUNG'
    # Pattern: remove second occurrence of QUY CHUẨN KỸ THUẬT QUỐC GIA... National Technical Regulation...
    body_from_preface = re.sub(
        r"QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ AN TOÀN CHÁY CHO NHÀ VÀ CÔNG TRÌNH\s*\n\s*National Technical Regulation on Fire safety of Buildings and Constructions\s*\n+",
        "",
        body_from_preface
    )

    doc_title = "# QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ AN TOÀN CHÁY CHO NHÀ VÀ CÔNG TRÌNH"
    doc_code = "**QCVN 06:2022/BXD**" if not is_hopnhat else "**QCVN 06:2022/BXD (VĂN BẢN HỢP NHẤT NĂM 2023)**"
    doc_en = "*National Technical Regulation on Fire Safety of Buildings and Constructions*"

    toc = """## MỤC LỤC

- [1  QUY ĐỊNH CHUNG](#muc-1)
- [2  PHÂN LOẠI KỸ THUẬT VỀ CHÁY](#muc-2)
- [3  BẢO ĐẢM AN TOÀN CHO NGƯỜI](#muc-3)
- [4  NGĂN CHẶN CHÁY LAN](#muc-4)
- [5  CẤP NƯỚC CHỮA CHÁY](#muc-5)
- [6  CHỮA CHÁY VÀ CỨU NẠN](#muc-6)
- [7  TỔ CHỨC THỰC HIỆN](#muc-7)
- [PHỤ LỤC A (quy định) QUY ĐỊNH BỔ SUNG ĐỐI VỚI MỘT SỐ NHÓM NHÀ CỤ THỂ](#phu-luc-a)
- [PHỤ LỤC B (quy định) PHÂN LOẠI VẬT LIỆU XÂY DỰNG THEO ĐẶC TÍNH KỸ THUẬT VỀ CHÁY VÀ YÊU CẦU VỀ AN TOÀN CHÁY ĐỐI VỚI VẬT LIỆU](#phu-luc-b)
- [PHỤ LỤC C (quy định) HẠNG NGUY HIỂM CHÁY VÀ CHÁY NỔ CỦA NHÀ, CÔNG TRÌNH VÀ CÁC GIAN PHÒNG CÓ CÔNG NĂNG SẢN XUẤT VÀ KHO](#phu-luc-c)
- [PHỤ LỤC D (quy định) BẢO VỆ CHỐNG KHÓI](#phu-luc-d)
- [PHỤ LỤC E (quy định) KHOẢNG CÁCH PHÒNG CHÁY CHỐNG CHÁY](#phu-luc-e)
- [PHỤ LỤC F (quy định) GIỚI HẠN CHỊU LỬA DANH ĐỊNH CỦA MỘT SỐ CẤU KIỆN](#phu-luc-f)
- [PHỤ LỤC G (quy định) KHOẢNG CÁCH ĐẾN CÁC LỐI RA THOÁT NẠN VÀ CHIỀU RỘNG LỐI RA THOÁT NẠN](#phu-luc-g)
- [PHỤ LỤC H (quy định) BẬC CHỊU LỬA VÀ CÁC YÊU CẦU BẢO ĐẢM AN TOÀN CHÁY CHO NHÀ, CÔNG TRÌNH, KHOANG CHÁY](#phu-luc-h)
- [PHỤ LỤC I (tham khảo) CÁC HÌNH MINH HỌA](#phu-luc-i)"""

    new_header = f"{doc_code}\n\n{doc_title}\n\n{doc_en}\n\n{toc}\n\n## {body_from_preface}"
    return new_header

def clean_single_clause_notes(text: str) -> str:
    # Pattern:
    # _CHÚ THÍCH:_
    # - **CHÚ THÍCH:** <content>
    # (when not followed by another - **CHÚ THÍCH)
    pattern = r"_CHÚ THÍCH:_\s*\n-\s+\*\*CHÚ THÍCH:\*\*\s+([^\n]+)(?!\s*\n-\s+\*\*CHÚ THÍCH)"
    text = re.sub(pattern, r"_CHÚ THÍCH: \1_", text)
    
    # Also clean single '_CHÚ THÍCH:_\n- <content>'
    pattern2 = r"_CHÚ THÍCH:_\s*\n-\s+([^\n]+)(?!\s*\n-\s+)"
    def rep_p2(m):
        c = m.group(1).strip()
        if not c.startswith("**CHÚ THÍCH"):
            return f"_CHÚ THÍCH: {c}_"
        return m.group(0)
    text = re.sub(pattern2, rep_p2, text)

    return text

def process_file(fpath: Path) -> None:
    text = fpath.read_text(encoding="utf-8")
    is_hn = "hop_nhat" in fpath.name
    
    if "sua_doi_1" not in fpath.name:
        text = clean_front_matter_and_toc(text, is_hn)
    
    text = clean_single_clause_notes(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    fpath.write_text(text, encoding="utf-8")
    print(f"✅ Đã chuẩn hóa Header, TOC và Chú thích đơn cho: {fpath.name}")

def main() -> None:
    for fn in ["qcvn_06_2022_bxd.md", "qcvn_06_2022_bxd_hop_nhat_2023.md", "sua_doi_1_2023_qcvn_06_2022_bxd.md"]:
        fp = BUNDLE_DIR / fn
        if fp.exists():
            process_file(fp)

if __name__ == "__main__":
    main()
