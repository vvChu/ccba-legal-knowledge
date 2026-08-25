import docx
import re
import json
import os

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)
print(f"Total paragraphs in DOCX: {len(doc.paragraphs)}")
print(f"Total tables in DOCX: {len(doc.tables)}")

# Inspect DOCX paragraphs
docx_paras = []
for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if text:
        docx_paras.append({
            'index': i,
            'text': text,
            'style': p.style.name if p.style else ''
        })

print(f"Non-empty paragraphs in DOCX: {len(docx_paras)}")

# Read Markdown
with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()
    md_lines = md_content.splitlines()

print(f"Total lines in MD: {len(md_lines)}")

# Find headings in DOCX vs MD
# Look for Chuong, Muc, Dieu, Phu luc
chuong_pattern = re.compile(r'^(CHƯƠNG|Chương|PHỤ LỤC|Phụ lục)\s+([0-9IVXABCDĐEGHIKLM]+|[\w]+)', re.IGNORECASE)
heading_num_pattern = re.compile(r'^([A-I0-9]+(\.[0-9]+)+)\b')

docx_headings = []
for p in docx_paras:
    t = p['text']
    if chuong_pattern.match(t) or heading_num_pattern.match(t) or p['style'].startswith('Heading'):
        docx_headings.append(p)

print(f"Potential headings in DOCX: {len(docx_headings)}")

# Find headings in MD
md_headings = []
for i, l in enumerate(md_lines):
    l_strip = l.strip()
    if l_strip.startswith('#'):
        md_headings.append({
            'line': i + 1,
            'text': l_strip
        })

print(f"Headings in MD: {len(md_headings)}")

# Save preliminary report
out_data = {
    'docx_para_count': len(doc.paragraphs),
    'docx_non_empty_para_count': len(docx_paras),
    'docx_table_count': len(doc.tables),
    'md_line_count': len(md_lines),
    'md_heading_count': len(md_headings),
    'docx_sample_headings': docx_headings[:30],
    'md_sample_headings': md_headings[:30]
}

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\survey_summary_stage1.json', 'w', encoding='utf-8') as f:
    json.dump(out_data, f, ensure_ascii=False, indent=2)

print("Stage 1 completed successfully.")
