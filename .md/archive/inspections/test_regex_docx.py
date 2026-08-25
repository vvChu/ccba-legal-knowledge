"""
Test how reconstruct_qcvn06 logic processes paragraph 341, 342, 393, 394, 901..904, 1086..1095
"""
import sys
import re
import docx
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DOCX_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx")
doc = docx.Document(str(DOCX_PATH))

re_sec_l2 = re.compile(r"^((?:[1-7]|[A-I])\.\d+)\s+(.*)$")
re_sec_l3 = re.compile(r"^((?:[1-7]|[A-I])\.\d+\.\d+)\s+(.*)$")
re_sec_l4 = re.compile(r"^((?:[1-7]|[A-I])\.\d+\.\d+\.\d+)\s+(.*)$")
re_sec_l5 = re.compile(r"^((?:[1-7]|[A-I])\.\d+\.\d+\.\d+\.\d+)\s+(.*)$")

check_indices = [341, 342, 393, 394, 395, 397, 901, 902, 903, 904, 1086, 1087, 1089, 1095]

for idx in check_indices:
    text = doc.paragraphs[idx].text.strip()
    m_l4 = re_sec_l4.match(text)
    m_l3 = re_sec_l3.match(text)
    m_l2 = re_sec_l2.match(text)
    print(f"P#{idx}: text prefix = {repr(text[:30])}")
    if m_l4:
        print(f"  Matched L4: num = {repr(m_l4.group(1))}")
    elif m_l3:
        print(f"  Matched L3: num = {repr(m_l3.group(1))}")
    elif m_l2:
        print(f"  Matched L2: num = {repr(m_l2.group(1))}")
    else:
        print("  No section regex matched!")
