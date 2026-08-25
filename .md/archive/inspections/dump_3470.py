with open(r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Let's see what is on lines 3470 to 3750
out_lines = []
for i in range(3470, min(3800, len(lines))):
    out_lines.append(f"L{i+1}: {lines[i]}")

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\inspect_3470_3800.txt', 'w', encoding='utf-8') as out:
    out.writelines(out_lines)

print("Dumped lines 3470 to 3800")
