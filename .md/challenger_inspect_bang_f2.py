import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx"
MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"

doc = docx.Document(DOCX_PATH)
with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

p1763 = doc.paragraphs[1763].text
print("DOCX P#1763:")
print(repr(p1763))

# Search for parts of it in MD
print("\nSearch in MD:")
for line in md_content.splitlines():
    if "Bảng F.2" in line or "F.2" in line and "Tường" in line:
        print("MD:", repr(line))
