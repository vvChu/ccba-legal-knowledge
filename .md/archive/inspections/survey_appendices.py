import docx
import re
import json

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)
with open(md_path, 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

# Let's search for Phụ lục A to I in DOCX
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
pl_docx_hits = {l: [] for l in letters}

for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    for l in letters:
        if re.search(rf'^(PHỤ LỤC|Phụ lục)\s+{l}\b', t, re.IGNORECASE):
            pl_docx_hits[l].append((i, t, p.style.name if p.style else ''))

# Let's search in MD
pl_md_hits = {l: [] for l in letters}
for idx, line in enumerate(md_lines):
    t = line.strip()
    for l in letters:
        # check headings or bold or plain text
        if re.search(rf'(#+\s+|__|\*\*)?(PHỤ LỤC|Phụ lục)\s+{l}\b', t, re.IGNORECASE):
            pl_md_hits[l].append((idx + 1, t))

out_report = {
    'docx_appendices': pl_docx_hits,
    'md_appendices': pl_md_hits
}

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\appendices_survey.json', 'w', encoding='utf-8') as out:
    json.dump(out_report, out, ensure_ascii=False, indent=2)

print("Appendices survey completed.")
