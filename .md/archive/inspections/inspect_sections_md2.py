"""
Inspect the exact text around sections 2.1.1, 2.2.1, 5.1.1, 6.2.1
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MD_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md")
md_lines = MD_PATH.read_text(encoding="utf-8").splitlines()

def show_range(start_kw, num_lines=25):
    for i, line in enumerate(md_lines):
        if start_kw in line:
            print(f"=== Found '{start_kw}' at line {i+1} ===")
            for j in range(max(0, i-2), min(len(md_lines), i+num_lines)):
                print(f"{j+1:4d}: {md_lines[j]}")
            print("="*60)
            break

show_range("2.1.1", 25)
show_range("2.2.1", 25)
show_range("5.1.1", 25)
show_range("6.2.1", 25)
