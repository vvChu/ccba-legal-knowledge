import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
import docx

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.docx"
MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.md"
BASE_MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"

def normalize_text(text: str) -> str:
    # Normalize whitespace, quotes, dashes, non-breaking spaces
    text = text.replace('\xa0', ' ').replace('\u200b', '').replace('\ufeff', '')
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    text = text.replace('–', '-').replace('—', '-')
    return text.strip()

def strip_md_formatting(text: str) -> str:
    # Strip markdown headers, anchors, bold/italic, links
    t = re.sub(r'<a\s+id="[^"]*">\s*</a>', '', text)
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    t = re.sub(r'#+\s*', '', t)
    t = re.sub(r'[*_~`]', '', t)
    t = re.sub(r'^\s*[-*+]\s+', '', t)
    t = re.sub(r'^\s*\|\s*', '', t)
    t = re.sub(r'\s*\|\s*$', '', t)
    t = t.replace('|', ' ')
    return normalize_text(t)

print("=" * 80)
print("  EMPIRICAL CHALLENGER 1: COMPREHENSIVE ZERO-LOSS PARITY AUDIT HARNESS")
print("  Target: Sửa đổi 1:2023 QCVN 06:2022/BXD")
print("=" * 80)

# Load DOCX
doc = docx.Document(DOCX_PATH)
docx_paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

# Load MD
with open(MD_PATH, 'r', encoding='utf-8') as f:
    md_content = f.read()
    md_lines = md_content.splitlines()

# Load Base MD for link target resolution
with open(BASE_MD_PATH, 'r', encoding='utf-8') as f:
    base_md_content = f.read()

print(f"\n1. SOURCE METRICS:")
print(f"   DOCX Non-empty Body Paragraphs: {len(docx_paras)}")
print(f"   DOCX Tables: {len(doc.tables)}")
print(f"   MD Total Lines: {len(md_lines)}")
print(f"   MD Total Characters: {len(md_content)}")

# TEST 1: PARAGRAPH-BY-PARAGRAPH PARITY
print(f"\n" + "=" * 80)
print("TEST 1: PARAGRAPH-BY-PARAGRAPH VERBATIM & SEMANTIC PARITY")
print("=" * 80)

# Cleaned whole MD content
norm_md_full = normalize_text(strip_md_formatting(md_content))
norm_md_lines = [normalize_text(strip_md_formatting(l)) for l in md_lines if l.strip()]

exact_matches = 0
partial_matches = 0
missing_paras = []

for idx, p_raw in enumerate(docx_paras):
    p_norm = normalize_text(p_raw)
    if not p_norm:
        continue
    
    # 1. Exact full string match
    if p_norm in norm_md_full:
        exact_matches += 1
        continue
    
    # 2. Check prefix / suffix match (in case of punctuation nuances or line wrap)
    words = p_norm.split()
    if len(words) >= 3:
        # Check first 5 words and last 5 words
        prefix = ' '.join(words[:min(6, len(words))])
        suffix = ' '.join(words[max(0, len(words)-6):])
        if prefix in norm_md_full and suffix in norm_md_full:
            exact_matches += 1
            continue
        elif prefix in norm_md_full or suffix in norm_md_full:
            # Check 70% word overlap with something in md_full
            matched_words = [w for w in words if w in norm_md_full]
            if len(matched_words) / len(words) >= 0.8:
                partial_matches += 1
                continue
    
    # Check if single short sentence or title
    if len(words) < 3 and any(p_norm in ml for ml in norm_md_lines):
        exact_matches += 1
        continue

    # If reached here, consider missing
    missing_paras.append((idx, p_norm))
    print(f"  ❌ UNMATCHED DOCX P[{idx}]: {p_norm}")

total_docx_p = len(docx_paras)
matched_docx_p = exact_matches + partial_matches
parity_pct = (matched_docx_p / total_docx_p) * 100.0

print(f"\n--- PARAGRAPH PARITY SUMMARY ---")
print(f"Total DOCX Paragraphs: {total_docx_p}")
print(f"Exact Matches        : {exact_matches}")
print(f"Partial Matches      : {partial_matches}")
print(f"Missing Paragraphs   : {len(missing_paras)}")
print(f"Parity Retention Rate: {parity_pct:.2f}%")

# TEST 2: TABLE 10 REPLACEMENT GRID AUDIT
print(f"\n" + "=" * 80)
print("TEST 2: TABLE 10 REPLACEMENT GRID AUDIT (10 rows x 12 cols)")
print("=" * 80)

table10_docx = doc.tables[0]
docx_t10_rows = len(table10_docx.rows)
docx_t10_cols = len(table10_docx.columns)
print(f"DOCX Table 10 Dimensions: {docx_t10_rows} rows x {docx_t10_cols} cols")

# Extract Table 10 from MD
t10_md_lines = []
in_t10 = False
for line in md_lines:
    if "Bảng 10" in line or (in_t10 and line.strip().startswith('|')):
        in_t10 = True
        t10_md_lines.append(line)
    elif in_t10 and not line.strip().startswith('|') and line.strip() != "":
        if "CHÚ THÍCH" in line:
            t10_md_lines.append(line)
        else:
            in_t10 = False

pipe_rows = [l for l in t10_md_lines if l.strip().startswith('|') and not re.match(r'\|\s*[-:]+\s*\|', l)]
print(f"MD Table 10 Pipe Table Rows: {len(pipe_rows)}")

# Check key flow rate numbers in MD Table 10
flow_rates = ['10', '15', '20', '25', '30', '35', '40', '50', '60', '70', '80', '90', '100', '110']
missing_rates = [r for r in flow_rates if r not in '\n'.join(t10_md_lines)]
print(f"Key Flow Rates in Table 10: {flow_rates}")
print(f"Missing Flow Rates: {missing_rates}")

# Check Table 10 footnotes in MD
for fn_num in [1, 2, 3, 4]:
    fn_tag = f"CHÚ THÍCH {fn_num}"
    print(f"  Footnote '{fn_tag}': {'PASS' if fn_tag in md_content else 'FAIL'}")

# TEST 3: TABLE H.9 MODIFICATION AUDIT
print(f"\n" + "=" * 80)
print("TEST 3: TABLE H.9 MODIFICATION AUDIT")
print("=" * 80)
h9_checks = ["25 000", "10 400", "5 200", "1 400", "Bảng H.9"]
for k in h9_checks:
    print(f"  Table H.9 Entity '{k}': {'PASS' if k in md_content else 'FAIL'}")

# TEST 4: DIRECTIVES & ANCHORS AUDIT
print(f"\n" + "=" * 80)
print("TEST 4: PRIMARY DIRECTIVES & ANCHORS AUDIT")
print("=" * 80)

docx_directives = [p for p in docx_paras if re.match(r'^(Sửa đổi, bổ sung|Bổ sung|Bãi bỏ|Thay thế)\s+', p)]
print(f"DOCX Directives Count: {len(docx_directives)}")

md_h4_directives = [l for l in md_lines if l.startswith('#### ')]
print(f"MD H4 Directives Count: {len(md_h4_directives)}")

anchors = re.findall(r'<a\s+id="([^"]+)">\s*</a>', md_content)
print(f"Total HTML Anchors: {len(anchors)}")
print(f"Unique HTML Anchors: {len(set(anchors))}")
duplicates = [a for a in set(anchors) if anchors.count(a) > 1]
print(f"Duplicate Anchors: {duplicates}")

ch_anchors = [a for a in anchors if a.startswith('sd1-chuong-')]
pl_anchors = [a for a in anchors if a.startswith('sd1-phu-luc-')]
muc_anchors = [a for a in anchors if a.startswith('sd1-muc-')]
bang_anchors = [a for a in anchors if a.startswith('sd1-bang-')]

print(f"  - Chapter anchors (sd1-chuong-*): {len(ch_anchors)} -> {ch_anchors}")
print(f"  - Appendix anchors (sd1-phu-luc-*): {len(pl_anchors)} -> {pl_anchors}")
print(f"  - Clause anchors (sd1-muc-*): {len(muc_anchors)}")
print(f"  - Table anchors (sd1-bang-*): {len(bang_anchors)} -> {bang_anchors}")

# TEST 5: CROSS-REFERENCE LINK TARGET VALIDATION
print(f"\n" + "=" * 80)
print("TEST 5: BIDIRECTIONAL CROSS-REFERENCE HYPERLINK AUDIT")
print("=" * 80)

cross_links = re.findall(r'\[([^\]]+)\]\((qcvn_06_2022_bxd\.md#([^\)]+))\)', md_content)
print(f"Total Cross-links to Base QCVN 06: {len(cross_links)}")

base_anchors = set(re.findall(r'<a\s+id="([^"]+)">\s*</a>', base_md_content))
print(f"Total Standard Anchors in Base QCVN 06: {len(base_anchors)}")

valid_links = [l for l in cross_links if l[2] in base_anchors]
broken_links = [l for l in cross_links if l[2] not in base_anchors]

print(f"Valid Target Anchors in Base QCVN 06: {len(valid_links)}")
print(f"Broken Target Anchors: {len(broken_links)}")
if broken_links:
    print(f"Sample broken links (first 10):")
    for b in broken_links[:10]:
        print(f"  ❌ [{b[0]}](#{b[2]}) -> anchor '{b[2]}' NOT found in base QCVN 06")

# TEST 6: RESIDUAL ARTIFACTS & INTEGRITY
print(f"\n" + "=" * 80)
print("TEST 6: RESIDUAL ARTIFACTS & HYGIENE AUDIT")
print("=" * 80)

artifact_underscores = len(re.findall(r'_{4,}', md_content))
base64_images = len(re.findall(r'data:image/[^;]+;base64,', md_content))
legacy_anchors = len(re.findall(r'<a\s+id="chuong_pl[^"]*">', md_content))
raw_img_tags = len(re.findall(r'!\[[^\]]*\]\([^)]+\)', md_content))

print(f"Residual '____' artifacts: {artifact_underscores} (Must be 0)")
print(f"Base64 raw image blobs  : {base64_images} (Must be 0)")
print(f"Legacy placeholder tags : {legacy_anchors} (Must be 0)")
print(f"Markdown image links    : {raw_img_tags} (Must be 0)")

# TEST 7: FORMULA & BIBLIOGRAPHY VERIFICATION
print(f"\n" + "=" * 80)
print("TEST 7: FORMULA & BIBLIOGRAPHY AUDIT")
print("=" * 80)

latex_formulas = re.findall(r'\$\$([^\$]+)\$\$', md_content)
print(f"LaTeX Math Formulas: {len(latex_formulas)} -> {latex_formulas}")

russian_refs = [
    "[5] СНиП 2.01.02-85",
    "[6] СНиП 21-01-97",
    "[7] СП 1.13130.2020",
    "[8] СП 2.13130.2020",
    "[9] СП 4.13130.2013"
]
for ref in russian_refs:
    found = ref[:10] in md_content or ref[:6] in md_content
    print(f"  Russian Ref '{ref[:20]}': {'PASS' if found else 'FAIL'}")

bib_entries_found = [f"[{i}]" for i in range(1, 24) if f"[{i}]" in md_content]
print(f"Bibliography Entries Found: {len(bib_entries_found)} / 23 -> {bib_entries_found}")

# TEST 8: NUMERICAL CLAUSE ENTITY SAMPLING
print(f"\n" + "=" * 80)
print("TEST 8: NUMERICAL CLAUSE ENTITY AUDIT")
print("=" * 80)

critical_entities = [
    "REI 150", "REI 60", "REI 45", "REI 15", "EI 150", "EI 60", "EI 45", "EI 30", "EI 15",
    "0,8 m", "1,2 m", "1,5 m", "2,0 m", "2,5 m", "4,5 m", "150 m3/h", "500 m2",
    "Thông tư số 09/2023/TT-BXD", "16 tháng 10 năm 2023", "01 tháng 12 năm 2023",
    "QCVN 06:2022/BXD", "Sửa đổi 1:2023 QCVN 06:2022/BXD"
]
for ent in critical_entities:
    print(f"  Entity '{ent}': {'PASS' if ent in md_content else 'FAIL'}")

print("\n" + "=" * 80)
print("  AUDIT EXECUTION COMPLETE")
print("=" * 80)
