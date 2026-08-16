import os, sys, difflib
sys.path.insert(0, '.')
from pathlib import Path
from scripts.gold_standard_processor import process_okf_bundle

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path('legal_docs/01_vbpl/luat_xay_dung_2025_135_2025_qh15')
md_file = bundle_dir / 'luat_xay_dung_2025_135_2025_qh15.md'

text_before = md_file.read_text(encoding='utf-8')

# Run process_okf_bundle
res = process_okf_bundle(bundle_dir, doc_type='vbpl')

text_after = md_file.read_text(encoding='utf-8')

lines_before = text_before.splitlines()
lines_after = text_after.splitlines()

print(f'Lines before: {len(lines_before)}')
print(f'Lines after : {len(lines_after)}')

diff = list(difflib.unified_diff(lines_before, lines_after, fromfile='before.md', tofile='after.md', lineterm=''))

print(f'Total diff lines: {len(diff)}')
for line in diff[:40]:
    print(line)
