import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx"
doc = docx.Document(DOCX_PATH)

for idx in [341, 342, 393, 394, 395, 901, 902, 903, 904, 1086, 1087, 1089, 1095]:
    p = doc.paragraphs[idx]
    print(f"P#{idx} text: {repr(p.text[:60])}")
    print(f"P#{idx} runs: {[r.text for r in p.runs[:5]]}")
