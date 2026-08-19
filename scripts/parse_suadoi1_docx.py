"""Extract and standardize Sửa đổi 01:2026 QCVN 04:2021/BXD from authentic docx to OKF v2.0 Markdown."""

import json
import re
import sys
from pathlib import Path
from docx import Document

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCX_FILE = ROOT_DIR / ".md" / "extracted_docs" / "qcvn_04_2021_bxd" / "sua_doi_01_2026_qcvn_04_2021_bxd.docx"
MD_OUT = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_04_2021_bxd" / "sua_doi_01_2026_qcvn_04_2021_bxd.md"

def extract_docx_to_okf():
    doc = Document(str(DOCX_FILE))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    lines = []
    lines.append("# SỬA ĐỔI 01:2026 QCVN 04:2021/BXD")
    lines.append("")
    lines.append("## QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ NHÀ CHUNG CƯ")
    lines.append("")
    lines.append("*Amendment 01:2026 QCVN 04:2021/BXD*  ")
    lines.append("*National technical regulation on apartment buildings*")
    lines.append("")
    lines.append("### Lời nói đầu")
    lines.append("")
    lines.append("Sửa đổi 01:2026 QCVN 04:2021/BXD do Viện Khoa học công nghệ xây dựng biên soạn, Cục Quản lý nhà và thị trường bất động sản trình thẩm định, Vụ Khoa học công nghệ môi trường và Vật liệu xây dựng thẩm định, Bộ Xây dựng ban hành kèm theo Thông tư số 31/2026/TT-BXD ngày 15 tháng 06 năm 2026 của Bộ trưởng Bộ Xây dựng (có hiệu lực từ ngày 15 tháng 12 năm 2026).")
    lines.append("")
    lines.append("Sửa đổi 01:2026 QCVN 04:2021/BXD chỉ bao gồm nội dung sửa đổi, bổ sung một số quy định của [QCVN 04:2021/BXD](qcvn_04_2021_bxd.md). Các nội dung không được nêu tại Sửa đổi 01:2026 QCVN 04:2021/BXD thì tiếp tục áp dụng theo QCVN 04:2021/BXD ban hành kèm theo Thông tư số 03/2021/TT-BXD ngày 19 tháng 5 năm 2021 của Bộ trưởng Bộ Xây dựng.")
    lines.append("")
    lines.append("---")
    lines.append("")

    current_section = ""
    in_body = False

    for idx, p in enumerate(paragraphs):
        # Skip Circular preamble headers
        if "1. QUY ĐỊNH CHUNG" in p:
            in_body = True
            lines.append("### <a id=\"sd1-chuong-1\" name=\"sd1-chuong-1\"></a>1  QUY ĐỊNH CHUNG")
            lines.append("")
            continue
        elif "2. QUY ĐỊNH KỸ THUẬT" in p:
            lines.append("---")
            lines.append("")
            lines.append("### <a id=\"sd1-chuong-2\" name=\"sd1-chuong-2\"></a>2  QUY ĐỊNH KỸ THUẬT")
            lines.append("")
            continue
        elif "3. QUY ĐỊNH VỀ QUẢN LÝ" in p:
            lines.append("---")
            lines.append("")
            lines.append("### <a id=\"sd1-chuong-3\" name=\"sd1-chuong-3\"></a>3  QUY ĐỊNH VỀ QUẢN LÝ")
            lines.append("")
            continue
        elif "4. TRÁCH NHIỆM CỦA TỔ CHỨC, CÁ NHÂN" in p:
            lines.append("---")
            lines.append("")
            lines.append("### <a id=\"sd1-chuong-4\" name=\"sd1-chuong-4\"></a>4  TRÁCH NHIỆM CỦA TỔ CHỨC, CÁ NHÂN")
            lines.append("")
            continue

        if not in_body:
            continue

        # Format sub-headings
        if re.match(r"^2\.\d+(\.\d+)*\b", p):
            anchor = "sd1-muc-" + p.split()[0].replace(".", "-")
            lines.append(f"#### <a id=\"{anchor}\" name=\"{anchor}\"></a>{p}")
            lines.append("")
        elif p.startswith("Bổ sung") or p.startswith("Sửa đổi"):
            lines.append(f"**{p}**")
            lines.append("")
        elif p.startswith("“") or p.startswith("”"):
            lines.append(p)
            lines.append("")
        elif p.startswith("+") or p.startswith("●") or p.startswith("a)") or p.startswith("b)") or p.startswith("c)") or p.startswith("d)") or p.startswith("e)") or p.startswith("f)") or p.startswith("g)") or p.startswith("h)") or p.startswith("i)") or p.startswith("j)") or p.startswith("k)"):
            lines.append(p)
            lines.append("")
        else:
            lines.append(p)
            lines.append("")

    MD_OUT.parent.mkdir(parents=True, exist_ok=True)
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Extracted full Sửa đổi 01:2026 OKF Markdown: {MD_OUT} ({MD_OUT.stat().st_size:,} bytes)")

if __name__ == "__main__":
    extract_docx_to_okf()
