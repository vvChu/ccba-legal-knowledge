with open(r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
for idx in range(3470, len(lines)):
    l = lines[idx]
    if l.strip().startswith('#'):
        out.append(f"Line {idx+1:5d}: {l.strip()}\n")

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\md_after_line_3481.txt', 'w', encoding='utf-8') as f:
    f.writelines(out)

print(f"Total headings after line 3481: {len(out)}")
