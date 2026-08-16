import os, glob, json, re

bundle_dir = 'legal_docs/01_vbpl/luat_xay_dung_2025_135_2025_qh15'
files = glob.glob(os.path.join(bundle_dir, '*'))

print('=== 1. ENCODING AND LINE ENDINGS CHECK ===')
for fpath in sorted(files):
    fname = os.path.basename(fpath)
    with open(fpath, 'rb') as f:
        raw = f.read()
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    try:
        text = raw.decode('utf-8')
        valid_utf8 = True
    except Exception as e:
        valid_utf8 = False
        text = ''
    
    crlf_count = raw.count(b'\r\n')
    lf_count = raw.count(b'\n') - crlf_count
    cr_count = raw.count(b'\r') - crlf_count
    
    if crlf_count == 0 and cr_count == 0:
        line_ending_style = 'LF'
    elif lf_count == 0 and cr_count == 0:
        line_ending_style = 'CRLF'
    else:
        line_ending_style = f'MIXED (CRLF:{crlf_count}, LF:{lf_count}, CR:{cr_count})'
    
    print(f'File: {fname:40s} | Size: {len(raw):7d} B | BOM: {str(has_bom):5s} | UTF-8: {str(valid_utf8):5s} | EOL: {line_ending_style}')

print('\n=== 2. ANCHOR UNIQUENESS CHECK ===')
md_path = os.path.join(bundle_dir, 'luat_xay_dung_2025_135_2025_qh15.md')
with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

anchors = re.findall(r'<a\s+id=["\']([^"\']+)["\']\s*></a>', md_content)
print(f'Total HTML anchors found in MD: {len(anchors)}')

anchor_counts = {}
for a in anchors:
    anchor_counts[a] = anchor_counts.get(a, 0) + 1

duplicates = {a: c for a, c in anchor_counts.items() if c > 1}
if duplicates:
    print(f'DUPLICATE ANCHORS FOUND ({len(duplicates)}): {duplicates}')
else:
    print('ZERO DUPLICATE ANCHORS. All HTML anchors in MD are unique!')

print('\n=== 3. CLAUSES.JSON STRUCTURAL CHECK ===')
clauses_path = os.path.join(bundle_dir, 'clauses.json')
with open(clauses_path, 'r', encoding='utf-8') as f:
    clauses = json.load(f)

print(f'Total clause entries in clauses.json: {len(clauses)}')
missing_anchor = []
clause_ids = set()
dup_clause_ids = set()
for c in clauses:
    cid = c.get('clause_id')
    if not cid:
        print(f'WARNING: Entry missing clause_id: {c}')
        continue
    if cid in clause_ids:
        dup_clause_ids.add(cid)
    clause_ids.add(cid)
    # verify if anchor exists in markdown
    if f'<a id="{cid}"></a>' not in md_content:
        missing_anchor.append(cid)

print(f'Duplicate clause_id in clauses.json: {len(dup_clause_ids)}')
if dup_clause_ids:
    print(f'  Duplicates: {dup_clause_ids}')
print(f'Clause IDs missing in markdown anchors: {len(missing_anchor)}')
if missing_anchor:
    print(f'  Missing: {missing_anchor}')

print('\n=== 4. QA_BENCHMARK.JSON STRUCTURAL CHECK ===')
qa_path = os.path.join(bundle_dir, 'qa_benchmark.json')
with open(qa_path, 'r', encoding='utf-8') as f:
    qa_data = json.load(f)

if isinstance(qa_data, list):
    print(f'qa_benchmark.json is a list with {len(qa_data)} items')
    missing_qa_anchors = [item for item in qa_data if item.get('anchor') and f'<a id="{item["anchor"]}"></a>' not in md_content]
    print(f'QA anchors missing in markdown: {len(missing_qa_anchors)}')
