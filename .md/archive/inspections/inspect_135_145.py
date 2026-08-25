"""
Inspect P#135 to P#145 in DOCX and Markdown
"""
import sys
import docx
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DOCX_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx")
MD_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md")

doc = docx.Document(str(DOCX_PATH))
md_lines = MD_PATH.read_text(encoding="utf-8").splitlines()

print("--- DOCX P#135 to P#145 ---")
for i in range(135, 145):
    print(f"P#{i:3d}: {repr(doc.paragraphs[i].text)}")

print("\n--- MD lines around Section 1.4.16 / 1.4.17 ---")
for idx, line in enumerate(md_lines):
    if "1.4.16" in line or "1.4.17" in line or "1.4.18" in line:
        for j in range(max(0, idx-2), min(len(md_lines), idx+8)):
            print(f"{j+1:4d}: {md_lines[j]}")
        print("="*50)
