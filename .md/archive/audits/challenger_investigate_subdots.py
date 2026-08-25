import re
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"
DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx"

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_lines = f.readlines()

print("--- CHECKING SUBDOTS IN MD ---")
for idx, line in enumerate(md_lines):
    if re.search(r"^\s*#{1,6}\s+(?:2\.1\.11|2\.1\.12|2\.2\.11|2\.2\.12|2\.2\.13|5\.1\.11|5\.1\.12|5\.1\.13|5\.1\.14|6\.2\.11|6\.2\.12|6\.2\.13|6\.2\.14)\b", line):
        print(f"Line {idx+1}: {line.strip()}")
        # Show next 2 lines
        for j in range(1, 3):
            if idx + j < len(md_lines):
                print(f"  + {md_lines[idx+j].strip()}")

print("\n--- CHECKING DOCX FOR THESE SUBDOTS ---")
doc = docx.Document(DOCX_PATH)
for idx, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if re.search(r"^(?:2\.1\.11|2\.1\.12|2\.2\.11|2\.2\.12|2\.2\.13|5\.1\.11|5\.1\.12|5\.1\.13|5\.1\.14|6\.2\.11|6\.2\.12|6\.2\.13|6\.2\.14)\b", txt):
        print(f"DOCX P#{idx}: {txt[:80]}")
    elif re.search(r"^(?:2\.1\.1\.1|2\.1\.1\.2|2\.2\.1\.1|2\.2\.1\.2|2\.2\.1\.3|5\.1\.1\.1|5\.1\.1\.2|5\.1\.1\.3|5\.1\.1\.4|6\.2\.1\.1|6\.2\.1\.2|6\.2\.1\.3|6\.2\.1\.4)\b", txt):
        print(f"DOCX P#{idx} (WITH SUBDOT): {txt[:80]}")
