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
for line in md_lines[530:545]:
    if line.strip().startswith('|') and not re.match(r'\|\s*[-:]+\s*\|', line):
        cells = [c.strip() for c in line.strip().split('|')[1:-1]]
        md_t10_rows.append(cells)

print(f"DOCX Table 10 Data Rows: {len(t10_docx.rows)} (including footnote row 9)")
print(f"MD Table 10 Pipe Rows   : {len(md_t10_rows)}")

print("\n=== CELL-BY-CELL COMPARISON FOR TABLE 10 ===")
# Row 0 to 8 in DOCX corresponds to row 0 to 8 in MD Table
for r_idx in range(len(md_t10_rows)):
    docx_row = [c.text.replace('\n', ' ').strip() for c in t10_docx.rows[r_idx].cells]
    md_row = md_t10_rows[r_idx]
    
    print(f"\n--- ROW {r_idx} ({len(docx_row)} cols DOCX vs {len(md_row)} cols MD) ---")
    mismatches = []
    for c_idx in range(min(len(docx_row), len(md_row))):
        d_c = re.sub(r'\s+', ' ', docx_row[c_idx]).replace('\xa0', ' ')
        m_c = re.sub(r'\s+', ' ', md_row[c_idx]).replace('\xa0', ' ')
        if d_c != m_c and not (d_c == "" and m_c == "-") and not (d_c == "-" and m_c == "-"):
            mismatches.append((c_idx, d_c, m_c))
            
    if mismatches:
        print(f"  ⚠️ Mismatches found in Row {r_idx}:")
        for c_idx, d_c, m_c in mismatches:
            print(f"     Col {c_idx:2d}: DOCX='{d_c}' vs MD='{m_c}'")
    else:
        print(f"  ✅ Row {r_idx} MATCHED 100% (All {len(docx_row)} cells identical)")

# Check footnote (DOCX Row 9 vs MD line 544)
docx_fn = re.sub(r'\s+', ' ', t10_docx.rows[9].cells[0].text).replace('\xa0', ' ').strip()
md_fn = re.sub(r'[*_]', '', md_lines[543]).strip()
md_fn = re.sub(r'\s+', ' ', md_fn).replace('\xa0', ' ')
print(f"\n--- FOOTNOTE COMPARISON ---")
print(f"DOCX Footnote: '{docx_fn}'")
print(f"MD   Footnote: '{md_fn}'")
if docx_fn == md_fn:
    print(f"✅ Footnote MATCHED 100% PERFECTLY!")
else:
    print(f"⚠️ Footnote Diff: SequenceMatcher = {docx_fn == md_fn}")
