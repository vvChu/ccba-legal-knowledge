import re
import json

with open(r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md', 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

# Search for all major sections, appendices, chapters in MD
print("Scanning MD for structural landmarks...")
results = []
for idx, line in enumerate(md_lines):
    l = line.strip()
    if not l.startswith('#'):
        continue
    
    # Check if chapter or appendix or high-level section
    if re.search(r'###\s+([0-9]\b|PHỤ LỤC|Phụ lục|QUY ĐỊNH)', l, re.IGNORECASE):
        results.append((idx + 1, l))

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\md_structural_landmarks.txt', 'w', encoding='utf-8') as out:
    for line_no, text in results:
        out.write(f"Line {line_no:5d}: {text}\n")

print(f"Found {len(results)} landmarks in MD.")
