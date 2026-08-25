import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_lines = f.readlines()

for idx, line in enumerate(md_lines):
    if line.startswith("#"):
        m = re.match(r"^#{1,6}\s+([A-Za-z0-9.]+)\b", line)
        if m:
            num_str = m.group(1)
            parts = num_str.split(".")
            if len(parts) >= 3 and not (len(parts) == 3 and parts[0] == "1" and parts[1] == "4"):
                for p in parts[2:]:
                    if p.isdigit() and int(p) >= 10:
                        # Check if this section really has >= 10 items or if it was a missing dot
                        # E.g. A.2.28.2 (section A.2.28 item 2 - valid!) vs 2.1.11 (section 2.1.1 item 1 - BUG!)
                        print(f"L{idx+1}: '{num_str}' (level {len(parts)}) -> {line.strip()[:60]}")
