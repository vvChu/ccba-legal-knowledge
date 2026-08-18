"""
Inspect lines 2600 to 2680 in qcvn_06_2022_bxd.md
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MD_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md")
md_lines = MD_PATH.read_text(encoding="utf-8").splitlines()

for i in range(2590, 2680):
    print(f"{i+1:4d}: {md_lines[i]}")
