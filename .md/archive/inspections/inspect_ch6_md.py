"""
Inspect Chapter 6 section 6.2.1 in markdown
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MD_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md")
md_lines = MD_PATH.read_text(encoding="utf-8").splitlines()

for i, line in enumerate(md_lines):
    if "6.2.1" in line or "6.2." in line:
        print(f"Line {i+1}: {line}")
        for j in range(max(0, i-2), min(len(md_lines), i+15)):
            print(f"  {j+1:4d}: {md_lines[j]}")
        print("="*60)
