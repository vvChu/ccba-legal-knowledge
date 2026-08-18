import sys, docx, re
sys.stdout.reconfigure(encoding="utf-8")
doc = docx.Document(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx")

def norm_clean(t):
    return re.sub(r'[^\w\d]+', '', t.lower())

short_paras = []
for idx in range(22, len(doc.paragraphs)):
    t = doc.paragraphs[idx].text.strip()
    if not t:
        continue
    nt = norm_clean(t)
    if len(nt) < 5:
        short_paras.append((idx, t, nt))

print(f"Total short paragraphs (len < 5) in body: {len(short_paras)}")
for p in short_paras:
    print(f"p[{p[0]:4d}]: repr={repr(p[1])} norm={repr(p[2])}")
