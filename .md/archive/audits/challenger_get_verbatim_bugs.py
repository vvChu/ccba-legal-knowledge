import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"

with open(MD_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

targets = [
    "##### 2.1.11", "##### 2.1.12", "##### 2.2.11", "##### 2.2.12", "##### 2.2.13",
    "##### 5.1.11", "##### 5.1.12", "##### 5.1.13", "##### 5.1.14",
    "##### 6.2.11", "##### 6.2.12", "##### 6.2.13", "##### 6.2.14"
]

print("=== EXACT VERBATIM LOCATIONS IN qcvn_06_2022_bxd.md ===")
for idx, line in enumerate(lines):
    for t in targets:
        if line.strip().startswith(t):
            # Print previous line (anchor), current line, next line
            prev_line = lines[idx-1].strip() if idx > 0 else ""
            prev2_line = lines[idx-2].strip() if idx > 1 else ""
            print(f"Line {idx+1}:")
            print(f"  Anchor : {prev_line or prev2_line}")
            print(f"  Heading: {line.strip()[:80]}")
