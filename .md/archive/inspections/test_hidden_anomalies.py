"""
Test anomaly regex with #+ instead of ###
"""
import re
import sys
import docx
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MD_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md")
DOCX_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx")

md_lines = MD_PATH.read_text(encoding="utf-8").splitlines()
doc = docx.Document(str(DOCX_PATH))

docx_paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

re_4digit_fixed = re.compile(r'(#+|__|\*\*)\s*([0-9]+\.[0-9]+\.[0-9]{2,})\b')

anomalies = []
for idx, l in enumerate(md_lines):
    m = re_4digit_fixed.search(l)
    if m:
        num = m.group(2)
        parts = num.split('.')
        if len(parts) == 3 and len(parts[2]) == 2:
            candidate = f"{parts[0]}.{parts[1]}.{parts[2][0]}.{parts[2][1]}"
            if any(candidate in p for p in docx_paras):
                anomalies.append({
                    'line': idx + 1,
                    'found': num,
                    'expected': candidate,
                    'raw': l[:120]
                })

print(f"Total hidden subdot anomalies found with proper #+ regex: {len(anomalies)}")
for a in anomalies:
    print(f"  Line {a['line']:4d}: Found '{a['found']}', Expected '{a['expected']}' -> {a['raw']}")
