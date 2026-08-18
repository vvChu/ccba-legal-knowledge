with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md', 'r', encoding='utf-8') as f:
    ext_lines = f.readlines()

print(f"Extracted docs MD lines: {len(ext_lines)}")

# Search for Phụ lục headings in extracted_docs
pl_found = []
for idx, l in enumerate(ext_lines):
    if 'phụ lục' in l.lower() or 'phu luc' in l.lower():
        if l.strip().startswith('#') or l.strip().startswith('**') or l.strip().startswith('PHỤ'):
            pl_found.append((idx + 1, l.strip()))

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_md_phuluc.txt', 'w', encoding='utf-8') as out:
    for line_no, txt in pl_found:
        out.write(f"Line {line_no:5d}: {txt}\n")

print(f"Found {len(pl_found)} Phụ lục lines in extracted_docs MD")
