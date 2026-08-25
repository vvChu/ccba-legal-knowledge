import re
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"
DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx"

targets = ["1.1.11", "1.5.5", "1.5.6", "A.2.25.5", "A.3.2.2", "H.2.12.10", "H.7", "TÀI LIỆU THAM KHẢO", "THƯ MỤC"]

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

doc = docx.Document(DOCX_PATH)

print("--- SEARCH IN DOCX ---")
for idx, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    for t in targets:
        if re.search(rf"\b{re.escape(t)}\b", txt, re.IGNORECASE):
            print(f"DOCX P#{idx} (Target '{t}'): {txt[:100]}")

print("\n--- SEARCH IN MD ---")
for idx, line in enumerate(md_content.splitlines()):
    for t in targets:
        if re.search(rf"\b{re.escape(t)}\b", line, re.IGNORECASE):
            print(f"MD L#{idx+1} (Target '{t}'): {line[:100]}")
