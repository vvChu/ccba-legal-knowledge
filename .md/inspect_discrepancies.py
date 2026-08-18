import re
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.docx"
MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.md"

doc = docx.Document(DOCX_PATH)
docx_paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

with open(MD_PATH, 'r', encoding='utf-8') as f:
    md_content = f.read()
    md_lines = md_content.splitlines()

print("=== CHECK UNMATCHED P[250] & P[512] IN DOCX ===")
print(f"DOCX P[250]: '{docx_paras[250]}'")
print(f"DOCX P[512]: '{docx_paras[512]}'")

# Check surrounding DOCX P[248..252]
print("\n--- DOCX Context for P[250] ---")
for i in range(248, min(len(docx_paras), 253)):
    print(f"  P[{i}]: {docx_paras[i]}")

# Check surrounding DOCX P[510..515]
print("\n--- DOCX Context for P[512] ---")
for i in range(510, min(len(docx_paras), 516)):
    print(f"  P[{i}]: {docx_paras[i]}")

# Check Bibliography in MD
print("\n=== BIBLIOGRAPHY IN MD ===")
bib_start = False
for line in md_lines:
    if "THƯ MỤC" in line or "sd1-thu-muc" in line:
        bib_start = True
    if bib_start:
        print(line)

