import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_lines = f.readlines()

print("--- SCANNING FOR ANY HEADING WITH 2-DIGIT SEGMENTS (EXCEPT 1.4 DEFINITIONS) ---")
for idx, line in enumerate(md_lines):
    if line.startswith("#"):
        # Match heading numbers like 2.1.11, 2.5.6.33, etc.
        m = re.match(r"^#{1,6}\s+([A-Za-z0-9.]+)\b", line)
        if m:
            num_str = m.group(1)
            parts = num_str.split(".")
            # If any part after the second is >= 10, check if it's outside 1.4
            if len(parts) >= 3 and not (len(parts) == 3 and parts[0] == "1" and parts[1] == "4"):
                for p in parts[2:]:
                    if p.isdigit() and int(p) >= 10:
                        print(f"Line {idx+1}: Heading '{num_str}' -> {line.strip()[:80]}")
