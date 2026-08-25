with open(r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Search for B.1, C.1, D.1, E.1, F.1, G.1, H.1, I.1
targets = ['B.1', 'C.1', 'D.1', 'E.1', 'F.1', 'G.1', 'H.1', 'I.1']
found_targets = []

for idx, line in enumerate(lines):
    l_strip = line.strip()
    for t in targets:
        if t in l_strip and (l_strip.startswith('#') or l_strip.startswith('__') or l_strip.startswith('**') or l_strip.startswith(t)):
            found_targets.append((idx + 1, t, l_strip[:120]))

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\appendix_sections_found.txt', 'w', encoding='utf-8') as out:
    for line_no, tag, txt in found_targets:
        out.write(f"Line {line_no:5d} [{tag}]: {txt}\n")

print(f"Found {len(found_targets)} appendix section occurrences.")
