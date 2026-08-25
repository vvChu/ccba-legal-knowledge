import re
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.docx"
MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.md"

doc = docx.Document(DOCX_PATH)
t_h9 = doc.tables[1]

print(f"DOCX Table 2 (H.9): {len(t_h9.rows)} rows x {len(t_h9.columns)} cols")
for r_idx, row in enumerate(t_h9.rows):
    print(f"  Row {r_idx}: {[c.text.strip() for c in row.cells]}")

# Find H.9 section in MD
with open(MD_PATH, 'r', encoding='utf-8') as f:
    md_content = f.read()

h9_match = re.search(r'Sửa đổi, bổ sung Bảng H\.9.*?(?=\n####|\Z)', md_content, re.DOTALL)
if h9_match:
    print(f"\n--- MD Bảng H.9 Section ---")
    print(h9_match.group(0))

