with open(r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

occurrences = []
for idx, l in enumerate(lines):
    if 'phụ lục' in l.lower():
        occurrences.append((idx + 1, l.strip()))

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\phu_luc_in_md.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total lines mentioning Phụ lục: {len(occurrences)}\n\n")
    for line_no, text in occurrences:
        out.write(f"Line {line_no:5d}: {text[:150]}\n")

print(f"Saved {len(occurrences)} occurrences of Phụ lục to phu_luc_in_md.txt")
