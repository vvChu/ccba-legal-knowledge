import docx
import re
import json

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)

# Let's inspect headings in DOCX
docx_headings = []
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    
    # Check if heading
    # Regex patterns for chapters, sections, clauses, appendices
    # 1. Chapters: "1 QUY ĐỊNH CHUNG", "1. QUY ĐỊNH CHUNG", "CHƯƠNG 1..."
    # 2. Appendices: "PHỤ LỤC A", "PHỤ LỤC B"...
    # 3. Numbered clauses: "1.1", "1.1.1", "A.1", "A.1.1", "A.2.1.1", etc.
    
    is_heading = False
    htype = 'text'
    
    # Regex for numbered patterns
    m_chap = re.match(r'^([1-7])\s*\.?\s+([A-ZĐÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ\s\-,:]{3,})$', t)
    m_app = re.match(r'^(PHỤ LỤC|Phụ lục)\s+([A-I])(\b.*)?$', t, re.IGNORECASE)
    m_sec = re.match(r'^(([1-7]|[A-I])\.[0-9]+(\.[0-9]+)*)\b(.*)$', t)
    
    if m_chap:
        is_heading = True
        htype = 'chapter'
    elif m_app:
        is_heading = True
        htype = 'appendix'
    elif m_sec:
        is_heading = True
        htype = 'section_or_clause'
    elif p.style and p.style.name.startswith('Heading'):
        is_heading = True
        htype = p.style.name
        
    if is_heading:
        docx_headings.append({
            'p_idx': i,
            'text': t,
            'htype': htype,
            'style': p.style.name if p.style else ''
        })

print(f"Total DOCX headings identified: {len(docx_headings)}")

# Check heading levels distribution in MD
with open(md_path, 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

md_headings = []
for i, l in enumerate(md_lines):
    l_strip = l.strip()
    if l_strip.startswith('#'):
        m = re.match(r'^(#+)\s*(.*)', l_strip)
        if m:
            md_headings.append({
                'line': i + 1,
                'level': len(m.group(1)),
                'text': m.group(2).strip()
            })

level_counts = {}
for h in md_headings:
    level_counts[h['level']] = level_counts.get(h['level'], 0) + 1

print(f"MD Heading Level Counts: {level_counts}")

# Save report
with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\survey_headings_docx.json', 'w', encoding='utf-8') as f:
    json.dump(docx_headings, f, ensure_ascii=False, indent=2)

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\survey_headings_md.json', 'w', encoding='utf-8') as f:
    json.dump(md_headings, f, ensure_ascii=False, indent=2)

print("Heading survey dumped successfully.")
