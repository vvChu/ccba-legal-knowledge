import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

md_path = "legal_docs/01_vbpl/luat_xay_dung_2025_135_2025_qh15/luat_xay_dung_2025_135_2025_qh15.md"
clauses_path = "legal_docs/01_vbpl/luat_xay_dung_2025_135_2025_qh15/clauses.json"
qa_path = "legal_docs/01_vbpl/luat_xay_dung_2025_135_2025_qh15/qa_benchmark.json"

content = open(md_path, encoding="utf-8").read()
anchors = set(re.findall(r'<a id="([^"]+)"></a>', content))
print(f"Total HTML anchors found in Markdown: {len(anchors)}")

clauses = json.load(open(clauses_path, encoding="utf-8"))
missing_c = [c["anchor"] for c in clauses if c.get("anchor") not in anchors]
print(f"Missing clause anchors: {len(missing_c)}")

qa = json.load(open(qa_path, encoding="utf-8"))
missing_q = [q["anchor"] for q in qa if q.get("anchor") not in anchors]
print(f"Missing QA anchors: {len(missing_q)}")
