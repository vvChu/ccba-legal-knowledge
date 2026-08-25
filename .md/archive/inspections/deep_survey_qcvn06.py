import docx
import re
import json

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)

# Extract all DOCX elements in order (paragraphs and tables)
# In python-docx, doc.paragraphs gives body paragraphs (not inside tables).
# doc.tables gives tables.

docx_elements = []
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t:
        docx_elements.append({
            'type': 'paragraph',
            'docx_p_idx': i,
            'text': t,
            'style': p.style.name if p.style else '',
            'runs': [r.text for r in p.runs if r.text.strip()]
        })

print(f"Total non-empty DOCX paragraphs: {len(docx_elements)}")

# Read Markdown lines
with open(md_path, 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

print(f"Total MD lines: {len(md_lines)}")

# Parse MD into structured sections and headings
md_headings = []
for idx, line in enumerate(md_lines):
    l_strip = line.strip()
    if l_strip.startswith('#'):
        # Match heading level
        match = re.match(r'^(#+)\s*(.*)', l_strip)
        if match:
            level = len(match.group(1))
            heading_text = match.group(2).strip()
            md_headings.append({
                'line_num': idx + 1,
                'level': level,
                'raw': l_strip,
                'text': heading_text
            })

# Identify major divisions (Chapters and Appendices) in DOCX
# Standard QCVN 06 structure:
# 1. QUY ĐỊNH CHUNG (or CHƯƠNG 1)
# 2. PHÂN LOẠI KỸ THUẬT VỀ CHÁY (CHƯƠNG 2)
# 3. BẢO ĐẢM AN TOÀN CHO NGƯỜI (CHƯƠNG 3)
# 4. NGĂN CHẶN CHÁY LAN (CHƯƠNG 4)
# 5. CẤP NƯỚC CHỮA CHÁY (CHƯƠNG 5)
# 6. CHỮA CHÁY VÀ CỨU NẠN (CHƯƠNG 6)
# 7. QUY ĐỊNH VỀ QUẢN LÝ (CHƯƠNG 7)
# PHỤ LỤC A -> PHỤ LỤC I

# Let's inspect how DOCX represents headings and chapters
chapters_docx = []
appendices_docx = []

re_chuong = re.compile(r'^(1|2|3|4|5|6|7)\s*\.?\s+([A-ZĐÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ\s\-,:]{3,})', re.UNICODE)
re_phuluc = re.compile(r'^(PHỤ LỤC|Phụ lục)\s+([A-I])(\b.*)?', re.IGNORECASE)

for elem in docx_elements:
    t = elem['text']
    m_pl = re_phuluc.match(t)
    if m_pl:
        appendices_docx.append(elem)
    elif elem['style'].startswith('Heading 1') or elem['style'] == 'Heading' or re_chuong.match(t):
        if any(f"{c}." in t[:4] or t.startswith(f"{c} ") for c in range(1, 8)):
            chapters_docx.append(elem)

# Let's also check MD chapters and appendices
md_chapters = [h for h in md_headings if any(h['text'].startswith(f"Chương {c}") or h['text'].startswith(f"{c}. ") or h['text'].startswith(f"{c} ") for c in range(1, 8)) and h['level'] <= 2]
md_appendices = [h for h in md_headings if 'Phụ lục' in h['text'] or 'PHỤ LỤC' in h['text']]

print(f"DOCX Chapter candidates: {len(chapters_docx)}")
print(f"DOCX Appendix candidates: {len(appendices_docx)}")
print(f"MD Chapter candidates: {len(md_chapters)}")
print(f"MD Appendix candidates: {len(md_appendices)}")

# Let's write out all headings in both for side-by-side comparison
with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\docx_all_paragraphs.json', 'w', encoding='utf-8') as f:
    json.dump(docx_elements, f, ensure_ascii=False, indent=2)

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\md_all_headings.json', 'w', encoding='utf-8') as f:
    json.dump(md_headings, f, ensure_ascii=False, indent=2)

print("Saved intermediate parsed files.")
