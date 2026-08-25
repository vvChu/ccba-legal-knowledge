import sys, docx, re
sys.stdout.reconfigure(encoding="utf-8")
doc = docx.Document(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx")

# Let's inspect Section 1.4: p[84] to p[233]
for i in range(84, 234):
    p = doc.paragraphs[i].text.strip()
    if p:
        print(f"p[{i:3d}]: {p}")
