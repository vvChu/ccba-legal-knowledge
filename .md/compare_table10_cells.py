import re
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.docx"
MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.md"

doc = docx.Document(DOCX_PATH)
t10_docx = doc.tables[0]

with open(MD_PATH, 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

# Extract Table 10 from MD
md_t10_rows = []
in_t10 = False
for line in md_lines:
    if "Bảng 10 - Lưu lượng nước chữa cháy ngoài nhà" in line or (in_t10 and line.strip().startswith('|')):
        in_t10 = True
        if line.strip().startswith('|') and not re.match(r'\|\s*[-:]+\s*\|', line):
            # Parse cells
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            md_t10_rows.append(cells)
    elif in_t10 and not line.strip().startswith('|') and line.strip() != "":
        if not "CHÚ THÍCH" in line:
            in_t10 = False

print(f"DOCX Table 10: {len(t10_docx.rows)} rows x {len(t10_docx.columns)} cols")
print(f"MD Table 10  : {len(md_t10_rows)} rows x {[len(r) for r in md_t10_rows]}")

print("\n=== DOCX vs MD CELL-BY-CELL COMPARISON ===")
for r_idx in range(len(t10_docx.rows)):
    docx_row = [c.text.replace('\n', ' ').strip() for c in t10_docx.rows[r_idx].cells]
    print(f"\n--- ROW {r_idx} ---")
    print(f"  DOCX ({len(docx_row)} cells): {docx_row[:6]}")
    if r_idx < len(md_t10_rows):
        md_row = md_t10_rows[r_idx]
        print(f"  MD   ({len(md_row)} cells): {md_row[:6]}")
        # Compare cell by cell
        mismatches = []
        for c_idx in range(min(len(docx_row), len(md_row))):
            d_c = re.sub(r'\s+', ' ', docx_row[c_idx]).replace('\xa0', ' ')
            m_c = re.sub(r'\s+', ' ', md_row[c_idx]).replace('\xa0', ' ')
            if d_c != m_c and not (d_c == "" and m_c == "-") and not (d_c == "-" and m_c == "-"):
                mismatches.append((c_idx, d_c, m_c))
        if mismatches:
            print(f"  ⚠️ Mismatches in row {r_idx}:")
            for c_idx, d_c, m_c in mismatches:
                print(f"     Col {c_idx}: DOCX='{d_c}' vs MD='{m_c}'")
        else:
            print(f"  ✅ Row {r_idx} MATCHED PERFECTLY")
    else:
        print(f"  ❌ Missing row {r_idx} in MD!")

