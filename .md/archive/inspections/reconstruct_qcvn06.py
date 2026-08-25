import sys
import os
import re
import docx
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import Table

sys.stdout.reconfigure(encoding="utf-8")

docx_path = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx"
target_md_path = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"

doc = docx.Document(docx_path)

def table_to_gfm(tbl: Table) -> str:
    """Convert python-docx Table into clean GFM pipe table string."""
    if not tbl.rows:
        return ""
    
    cleaned_matrix = []
    for r_idx, row in enumerate(tbl.rows):
        cleaned_row = []
        seen_cells = set()
        for c_idx, cell in enumerate(row.cells):
            cell_elem_id = id(cell._tc)
            if cell_elem_id not in seen_cells:
                seen_cells.add(cell_elem_id)
                # Normalize spaces in cell text and escape pipes
                txt = " ".join(cell.text.split()).replace("|", "\\|")
                cleaned_row.append(txt)
        cleaned_matrix.append(cleaned_row)
        
    max_cols = max(len(r) for r in cleaned_matrix) if cleaned_matrix else 0
    if max_cols == 0:
        return ""
        
    for r in cleaned_matrix:
        if len(r) < max_cols:
            r.extend([""] * (max_cols - len(r)))
            
    header_row = cleaned_matrix[0]
    delimiter_row = ["---"] * max_cols
    data_rows = cleaned_matrix[1:]
    
    lines = [
        "| " + " | ".join(header_row) + " |",
        "| " + " | ".join(delimiter_row) + " |"
    ]
    for r in data_rows:
        lines.append("| " + " | ".join(r) + " |")
        
    return "\n".join(lines)

# Regex patterns for heading detection
re_doc_title = re.compile(r"^QCVN\s+06:2022/BXD", re.IGNORECASE)
re_loi_noi_dau = re.compile(r"^Lời nói đầu$", re.IGNORECASE)
re_chapter = re.compile(r"^([1-7])\s+([A-ZĐÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐĨŨƠƯẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴÝỶỸ\s]+)$")
re_appendix = re.compile(r"^(PHỤ LỤC\s+([A-I]))(?:\s*\((quy định|tham khảo)\))?\s*(.*)$", re.IGNORECASE)
re_table_title = re.compile(r"^(Bảng\s+([A-Za-z0-9\.]+))\s*[-–:]\s*(.*)$")
re_figure_title = re.compile(r"^(Hinh|Hình)\s+([A-Za-z0-9\.]+)\s*[-–:]\s*(.*)$")

# Section patterns
re_sec_l2 = re.compile(r"^((?:[1-7]|[A-I])\.\d+)\s+(.*)$")
re_sec_l3 = re.compile(r"^((?:[1-7]|[A-I])\.\d+\.\d+)\s+(.*)$")
re_sec_l4 = re.compile(r"^((?:[1-7]|[A-I])\.\d+\.\d+\.\d+)\s+(.*)$")
re_sec_l5 = re.compile(r"^((?:[1-7]|[A-I])\.\d+\.\d+\.\d+\.\d+)\s+(.*)$")

# Section 1.4 standalone number pattern like "1.4.17", "1.4 16", "1.4.1"
re_1_4_num = re.compile(r"^1\.4[\.\s](\d+)$")

def generate_anchor(num_str: str) -> str:
    slug = num_str.lower().replace(".", "-").replace(" ", "-")
    return f'<a id="muc-{slug}"></a>'

def generate_table_anchor(tbl_num: str) -> str:
    slug = tbl_num.lower().replace(".", "-").replace(" ", "-")
    return f'<a id="bang-{slug}"></a>'

# Parse all body elements
body = doc._body._element
output_blocks = []

# State variables
in_toc = False
toc_passed = False
in_1_4 = False

idx = 0
total_elements = len(body)

while idx < total_elements:
    elem = body[idx]
    
    if isinstance(elem, CT_Tbl):
        tbl = Table(elem, doc)
        gfm_tbl = table_to_gfm(tbl)
        if gfm_tbl:
            output_blocks.append(f"\n{gfm_tbl}\n")
        idx += 1
        continue
        
    if not isinstance(elem, CT_P):
        idx += 1
        continue
        
    p = docx.text.paragraph.Paragraph(elem, doc)
    text = p.text.strip()
    
    if not text:
        idx += 1
        continue
        
    # Check MỤC LỤC
    if text == "MỤC LỤC":
        in_toc = True
        idx += 1
        continue
        
    if in_toc:
        if text == "Lời nói đầu" or re_loi_noi_dau.match(text) or text.startswith("QCVN 06:2022/BXD do"):
            in_toc = False
            toc_passed = True
        else:
            # Skip TOC items
            idx += 1
            continue
            
    # Document Title
    if re_doc_title.match(text):
        output_blocks.append(f"# {text}")
        idx += 1
        continue
        
    if text == "QUY CHUẨN KỸ THUẬT QUỐC GIA VÀ AN TOÀN CHÁY CHO NHÀ VÀ CÔNG TRÌNH" or text == "QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ AN TOÀN CHÁY CHO NHÀ VÀ CÔNG TRÌNH":
        output_blocks.append(f"## {text}")
        idx += 1
        continue
        
    if text.startswith("National Technical Regulation on Fire safety"):
        output_blocks.append(f"*{text}*")
        idx += 1
        continue
        
    # Lời nói đầu
    if re_loi_noi_dau.match(text):
        output_blocks.append(f"## {text}")
        idx += 1
        continue
        
    # Chapter headings
    m_chap = re_chapter.match(text)
    if m_chap:
        chap_num = m_chap.group(1)
        chap_title = m_chap.group(2)
        anchor = f'<a id="chuong-{chap_num}"></a>'
        output_blocks.append(f"\n{anchor}\n## {chap_num}  {chap_title}")
        in_1_4 = False
        idx += 1
        continue
        
    # Appendix headings
    m_app = re_appendix.match(text)
    if m_app:
        app_code = m_app.group(2).upper()
        app_type = m_app.group(3) or ""
        app_title = m_app.group(4) or ""
        type_str = f" ({app_type})" if app_type else ""
        title_str = f" {app_title}" if app_title else ""
        full_title = f"PHỤ LỤC {app_code}{type_str}{title_str}".strip()
        anchor = f'<a id="phu-luc-{app_code.lower()}"></a>'
        output_blocks.append(f"\n{anchor}\n## {full_title}")
        in_1_4 = False
        idx += 1
        continue
        
    # Section 1.4 detection
    if text == "1.4  Giải thích từ ngữ" or text == "1.4 Giải thích từ ngữ":
        in_1_4 = True
        anchor = generate_anchor("1-4")
        output_blocks.append(f"\n{anchor}\n### 1.4  Giải thích từ ngữ")
        idx += 1
        continue
    elif in_1_4 and (text.startswith("1.5") or text.startswith("2 ") or text.startswith("2.")):
        in_1_4 = False
        
    # In Section 1.4, check definition number e.g. "1.4.1", "1.4.17", "1.4 16"
    if in_1_4:
        m_1_4 = re_1_4_num.match(text)
        if m_1_4:
            def_num = int(m_1_4.group(1))
            norm_num_str = f"1.4.{def_num}"
            anchor = generate_anchor(norm_num_str)
            # Check next paragraph for term name
            next_term = ""
            if idx + 1 < total_elements:
                next_elem = body[idx + 1]
                if isinstance(next_elem, CT_P):
                    p_next = docx.text.paragraph.Paragraph(next_elem, doc)
                    next_term = p_next.text.strip()
            
            # If original was "1.4 16", preserve comment for exact search compatibility
            orig_comment = f" <!-- {text} -->" if " " in text else ""
            
            if next_term and not re_1_4_num.match(next_term) and not next_term.startswith("1.5"):
                # Next paragraph is term name
                output_blocks.append(f"\n{anchor}\n#### {norm_num_str}  {next_term}{orig_comment}")
                idx += 2 # consumed both number and term
                continue
            else:
                output_blocks.append(f"\n{anchor}\n#### {norm_num_str}{orig_comment}")
                idx += 1
                continue
                
    # Table title
    m_tbl = re_table_title.match(text)
    if m_tbl:
        tbl_full_num = m_tbl.group(2)
        tbl_rest = m_tbl.group(3)
        tbl_clean_num = tbl_full_num.replace(" ", "")
        anchor = generate_table_anchor(tbl_clean_num)
        output_blocks.append(f"\n{anchor}\n### Bảng {tbl_clean_num} - {tbl_rest}")
        idx += 1
        continue
        
    # Figure title
    m_fig = re_figure_title.match(text)
    if m_fig:
        output_blocks.append(f"\n**{text}**")
        idx += 1
        continue
        
    # Space-headings in Chapter 4: e.g. "4 1 ...", "4 2 ..."
    m_sp_ch4 = re.match(r"^4\s+([0-9]+)\s*(.*)$", text)
    if m_sp_ch4:
        sec_num = f"4.{m_sp_ch4.group(1)}"
        sec_title = m_sp_ch4.group(2).strip()
        anchor = generate_anchor(sec_num)
        title_part = f"  {sec_title}" if sec_title else ""
        output_blocks.append(f"\n{anchor}\n### {sec_num}{title_part}")
        idx += 1
        continue
        
    # Space-headings in Chapter 7: e.g. "7 1 ...", "7 2 ..."
    m_sp_ch7 = re.match(r"^7\s+([0-9]+)\s*(.*)$", text)
    if m_sp_ch7:
        sec_num = f"7.{m_sp_ch7.group(1)}"
        sec_title = m_sp_ch7.group(2).strip()
        anchor = generate_anchor(sec_num)
        title_part = f"  {sec_title}" if sec_title else ""
        output_blocks.append(f"\n{anchor}\n### {sec_num}{title_part}")
        idx += 1
        continue
        
    # Fix specific DOCX typo: "2.2.13" -> "2.2.1.3"
    if text.startswith("2.2.13 ") or text.startswith("2.2.13\t"):
        fixed_text = "2.2.1.3 " + text[7:].strip()
        anchor = generate_anchor("2-2-1-3")
        output_blocks.append(f"\n{anchor}\n##### {fixed_text}")
        idx += 1
        continue
        
    # Fix specific DOCX typo: "2.5.6.3 3" -> "2.5.6.3.3"
    if text.startswith("2.5.6.3 3"):
        fixed_text = "2.5.6.3.3" + text[9:]
        anchor = generate_anchor("2-5-6-3-3")
        output_blocks.append(f"\n{anchor}\n##### {fixed_text}")
        idx += 1
        continue
        
    # Level 5 subclause: e.g. "2.5.6.2.4"
    m_l5 = re_sec_l5.match(text)
    if m_l5:
        num = m_l5.group(1)
        rest = m_l5.group(2)
        anchor = generate_anchor(num)
        output_blocks.append(f"\n{anchor}\n###### {num}  {rest}")
        idx += 1
        continue
        
    # Level 4 subclause: e.g. "1.1.1.1", "2.1.3.1", "A.1.1.1"
    m_l4 = re_sec_l4.match(text)
    if m_l4:
        num = m_l4.group(1)
        rest = m_l4.group(2)
        anchor = generate_anchor(num)
        output_blocks.append(f"\n{anchor}\n##### {num}  {rest}")
        idx += 1
        continue
        
    # Level 3 clause: e.g. "1.1.1", "A.1.1", "5.2.10"
    m_l3 = re_sec_l3.match(text)
    if m_l3:
        num = m_l3.group(1)
        rest = m_l3.group(2)
        anchor = generate_anchor(num)
        output_blocks.append(f"\n{anchor}\n#### {num}  {rest}")
        idx += 1
        continue
        
    # Level 2 section: e.g. "1.1", "A.1"
    m_l2 = re_sec_l2.match(text)
    if m_l2:
        num = m_l2.group(1)
        rest = m_l2.group(2)
        anchor = generate_anchor(num)
        output_blocks.append(f"\n{anchor}\n### {num}  {rest}")
        idx += 1
        continue
        
    # Notes formatting
    if text.startswith("CHÚ THÍCH"):
        output_blocks.append(f"\n_{text}_\n")
        idx += 1
        continue
        
    # Standard paragraph
    output_blocks.append(f"{text}\n")
    idx += 1

# Join all blocks
final_md = "\n\n".join(output_blocks)

# Normalize consecutive blank lines
final_md = re.sub(r"\n{3,}", "\n\n", final_md).strip() + "\n"

# Write directly to target path
with open(target_md_path, "w", encoding="utf-8") as f:
    f.write(final_md)

print(f"Reconstruction complete.")
print(f"Target: {target_md_path}")
print(f"Total output lines: {len(final_md.splitlines())}")
print(f"Total output size: {len(final_md)} chars")
