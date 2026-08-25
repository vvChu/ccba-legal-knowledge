import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx"
MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"

doc = docx.Document(DOCX_PATH)
with open(MD_PATH, "r", encoding="utf-8") as f:
    md_lines = f.readlines()

# Extract all potential numbered clauses from DOCX (excluding tables)
docx_clauses = []
for p_idx, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if not txt:
        continue
    # Check if starts with clause number e.g. 1.1, 1.1.1, 1.1.1.1, A.1, A.1.1, etc.
    m = re.match(r"^((?:[A-I]|\d+)(?:\.\d+)+)\b\s*(.*)", txt)
    if m:
        num = m.group(1)
        rest = m.group(2).strip()
        docx_clauses.append((p_idx, num, rest))

print(f"Total numbered clauses found in DOCX: {len(docx_clauses)}")

# Extract all numbered headings from MD
md_clauses = []
for l_idx, line in enumerate(md_lines):
    if line.startswith("#"):
        m = re.match(r"^#{1,6}\s+((?:[A-I]|\d+)(?:\.\d+)+)\b\s*(.*)", line)
        if m:
            num = m.group(1)
            rest = m.group(2).strip()
            md_clauses.append((l_idx + 1, num, rest, line.strip()))

print(f"Total numbered headings found in MD: {len(md_clauses)}")

# Compare clause numbers
docx_nums = [c[1] for c in docx_clauses]
md_nums = [c[1] for c in md_clauses]

print("\n--- CHECKING NUMBER DIFFERENCES ---")
print(f"Unique clause numbers in DOCX: {len(set(docx_nums))}")
print(f"Unique clause numbers in MD  : {len(set(md_nums))}")

# Check which numbers are in DOCX but not in MD
in_docx_not_md = set(docx_nums) - set(md_nums)
print(f"In DOCX but not in MD: {len(in_docx_not_md)}")
for n in sorted(in_docx_not_md):
    # Find in docx_clauses
    examples = [c for c in docx_clauses if c[1] == n]
    print(f"  DOCX: {n} -> P#{examples[0][0]}: {examples[0][2][:60]}")

# Check which numbers are in MD but not in DOCX
in_md_not_docx = set(md_nums) - set(docx_nums)
print(f"\nIn MD but not in DOCX: {len(in_md_not_docx)}")
for n in sorted(in_md_not_docx):
    examples = [c for c in md_clauses if c[1] == n]
    print(f"  MD  : {n} -> L#{examples[0][0]}: {examples[0][2][:60]}")
