import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx"
doc = docx.Document(DOCX_PATH)

for i in range(1758, 1768):
    print(f"P#{i}: {repr(doc.paragraphs[i].text)}")
