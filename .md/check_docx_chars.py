"""
Check exact characters in doc.paragraphs[341], [342], [393], [394], [395], [898..904], [1086..1095]
"""
import sys
import docx
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DOCX_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx")
doc = docx.Document(str(DOCX_PATH))

check_indices = [341, 342, 393, 394, 395, 397, 901, 902, 903, 904, 1086, 1087, 1089, 1095]
for idx in check_indices:
    p = doc.paragraphs[idx]
    first_word = p.text.split()[0] if p.text.split() else ""
    print(f"P#{idx:4d}: first_word = {repr(first_word)}, full_prefix = {repr(p.text[:30])}")
    print(f"  raw bytes of first_word: {[ord(c) for c in first_word]}")

