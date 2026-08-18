import docx

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)
with open(md_path, 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

out = []
out.append("DOCX 1.4 samples:\n")
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if any(f"1.4.{n}" in t or f"1.4 {n}" in t for n in range(15, 25)):
        out.append(f"p{i:4d}: {t}\n")

out.append("\nMD lines 320 to 360:\n")
for i in range(320, 360):
    out.append(f"L{i+1:4d}: {md_lines[i].strip()}\n")

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\inspect_14_out.txt', 'w', encoding='utf-8') as f:
    f.writelines(out)

print("Saved inspect_14_out.txt")
