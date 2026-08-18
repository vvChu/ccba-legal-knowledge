import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
from pathlib import Path

repo_root = Path(r"d:\GitHubProjects\ccba-legal-knowledge")
bundle_dir = repo_root / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
md_path = bundle_dir / "qcvn_06_2022_bxd.md"
qa_path = bundle_dir / "qa_benchmark.json"
clauses_path = bundle_dir / "clauses.json"

md_lines = md_path.read_text(encoding="utf-8").splitlines()
with open(qa_path, "r", encoding="utf-8") as f:
    qa_data = json.load(f)
with open(clauses_path, "r", encoding="utf-8") as f:
    clauses_data = json.load(f)

# Find all anchors in Chapter 4 in qcvn_06_2022_bxd.md
ch4_md_anchors = []
for idx, line in enumerate(md_lines, 1):
    m = re.findall(r'<a id="([^"]+)"></a>', line)
    for a in m:
        if a.startswith("muc-4") or a.startswith("chuong-4"):
            ch4_md_anchors.append((idx, a, line))

print(f"=== CHAPTER 4 ANCHORS IN MD ({len(ch4_md_anchors)}) ===")
for idx, a, line in ch4_md_anchors:
    print(f"Line {idx:4d}: {a:<20} | {line[:80]}")

print("\n=== CHAPTER 4 IN QA BENCHMARK ===")
for qa in qa_data:
    a = qa.get("anchor", "")
    if a.startswith("muc-4") or a.startswith("chuong-4"):
        print(f"QA anchor: {a:<20} | Q: {qa.get('question')} | A: {qa.get('answer')[:60]}")
