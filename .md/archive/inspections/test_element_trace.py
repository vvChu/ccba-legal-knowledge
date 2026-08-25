import sys, re, docx
from docx.oxml.text.paragraph import CT_P

sys.stdout.reconfigure(encoding="utf-8")
doc = docx.Document(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx")

re_sec_l4 = re.compile(r"^((?:[1-7]|[A-I])\.\d+\.\d+\.\d+)\s+(.*)$")

for idx, elem in enumerate(doc._body._element):
    if isinstance(elem, CT_P):
        p = docx.text.paragraph.Paragraph(elem, doc)
        t = p.text.strip()
        if t.startswith("2.1.1.") or t.startswith("2.2.1.") or t.startswith("5.1.1.") or t.startswith("6.2.1."):
            m4 = re_sec_l4.match(t)
            print(f"elem[{idx:4d}]: text={repr(t[:40])} m4_group1={m4.group(1) if m4 else None}")
