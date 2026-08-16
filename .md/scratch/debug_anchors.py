import os, json, re

bundle_dir = 'legal_docs/01_vbpl/luat_xay_dung_2025_135_2025_qh15'
md_path = os.path.join(bundle_dir, 'luat_xay_dung_2025_135_2025_qh15.md')
clauses_path = os.path.join(bundle_dir, 'clauses.json')

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

with open(clauses_path, 'r', encoding='utf-8') as f:
    clauses = json.load(f)

anchors = re.findall(r'<a\s+id=["\']([^"\']+)["\']\s*></a>', md_content)
print(f'First 10 anchors in markdown: {anchors[:10]}')

clause_ids = [c.get('id') for c in clauses]
print(f'First 10 IDs in clauses.json: {clause_ids[:10]}')

# Check duplicates in clauses.json
id_counts = {}
for cid in clause_ids:
    id_counts[cid] = id_counts.get(cid, 0) + 1

dup_ids = {k: v for k, v in id_counts.items() if v > 1}
print(f'Duplicate IDs in clauses.json: {dup_ids}')

# Check match between clauses.json IDs and anchors
anchor_set = set(anchors)
matched = sum(1 for cid in clause_ids if cid in anchor_set)
print(f'Matched clause IDs with markdown anchors: {matched} / {len(clause_ids)}')
