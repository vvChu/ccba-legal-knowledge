import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
from pathlib import Path
from collections import Counter

repo_root = Path(r"d:\GitHubProjects\ccba-legal-knowledge")
bundle_dir = repo_root / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
qa_path = bundle_dir / "qa_benchmark.json"
clauses_path = bundle_dir / "clauses.json"
md_path = bundle_dir / "qcvn_06_2022_bxd.md"
sd1_path = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"

with open(qa_path, "r", encoding="utf-8") as f:
    qa_data = json.load(f)

with open(clauses_path, "r", encoding="utf-8") as f:
    clauses_data = json.load(f)

md_text = md_path.read_text(encoding="utf-8")
md_lines = md_text.splitlines()

sd1_text = sd1_path.read_text(encoding="utf-8")
sd1_lines = sd1_text.splitlines()

print(f"=== BASIC STATS ===")
print(f"Total QA items: {len(qa_data)}")
print(f"Total clauses in clauses.json: {len(clauses_data)}")
print(f"qcvn_06_2022_bxd.md total lines: {len(md_lines)}")
print(f"sua_doi_1_2023_qcvn_06_2022_bxd.md total lines: {len(sd1_lines)}")

# 1. Schema audit
keys_per_item = [tuple(sorted(item.keys())) for item in qa_data]
key_counter = Counter(keys_per_item)
print(f"\n=== SCHEMA AUDIT ===")
for schema, count in key_counter.items():
    print(f"Schema {schema}: {count} items")

sample_item = qa_data[0]
print(f"Sample QA item: {json.dumps(sample_item, ensure_ascii=False, indent=2)}")

# 2. Extract anchors from MD and SD1
md_anchor_map = {} # anchor -> line_no (1-based)
md_anchor_lines_map = {}
for idx, line in enumerate(md_lines, 1):
    m = re.findall(r'<a id="([^"]+)"></a>', line)
    for a in m:
        md_anchor_map[a] = idx
        md_anchor_lines_map.setdefault(a, []).append(idx)

sd1_anchor_map = {} # anchor -> line_no (1-based)
for idx, line in enumerate(sd1_lines, 1):
    m = re.findall(r'<a id="([^"]+)"></a>', line)
    for a in m:
        sd1_anchor_map[a] = idx

print(f"\n=== ANCHORS COUNT ===")
print(f"Unique anchors in qcvn_06_2022_bxd.md: {len(md_anchor_map)}")
print(f"Total anchor occurrences in qcvn_06_2022_bxd.md: {sum(len(v) for v in md_anchor_lines_map.values())}")
print(f"Unique anchors in sua_doi_1_2023_qcvn_06_2022_bxd.md: {len(sd1_anchor_map)}")

# 3. Check clause anchors and line mappings
clause_anchor_map = {c.get("anchor"): c for c in clauses_data}
print(f"Unique anchors in clauses.json: {len(clause_anchor_map)}")

# 4. Check QA anchor mapping against MD and Clauses
qa_anchors = [qa.get("anchor") for qa in qa_data]
qa_anchor_counts = Counter(qa_anchors)
duplicate_qa_anchors = {k: v for k, v in qa_anchor_counts.items() if v > 1}
print(f"\n=== QA ANCHOR INTEGRITY ===")
print(f"Duplicate anchors in qa_benchmark.json: {len(duplicate_qa_anchors)}")
if duplicate_qa_anchors:
    print(f"Duplicates: {duplicate_qa_anchors}")

# Broken anchors in QA
qa_not_in_md = [qa for qa in qa_data if qa.get("anchor") not in md_anchor_map]
print(f"QA items with anchor NOT in qcvn_06_2022_bxd.md: {len(qa_not_in_md)}")
for item in qa_not_in_md:
    print(f"  Missing in MD: anchor='{item.get('anchor')}', question='{item.get('question')}'")

qa_not_in_clauses = [qa for qa in qa_data if qa.get("anchor") not in clause_anchor_map]
print(f"QA items with anchor NOT in clauses.json: {len(qa_not_in_clauses)}")
for item in qa_not_in_clauses:
    print(f"  Missing in clauses: anchor='{item.get('anchor')}', question='{item.get('question')}'")

clauses_not_in_qa = [c for c in clauses_data if c.get("anchor") not in qa_anchor_counts]
print(f"Clauses NOT mapped to any QA item: {len(clauses_not_in_qa)}")
for c in clauses_not_in_qa[:10]:
    print(f"  Clause missing in QA: anchor='{c.get('anchor')}', title='{c.get('title')}'")

md_anchors_not_in_qa = [a for a in md_anchor_map if a not in qa_anchor_counts]
print(f"MD anchors NOT in QA benchmark: {len(md_anchors_not_in_qa)}")

# 5. Check line ranges in clauses.json vs qcvn_06_2022_bxd.md
print(f"\n=== CLAUSES.JSON LINE ACCURACY AUDIT ===")
line_mismatches = []
for c in clauses_data:
    anchor = c.get("anchor")
    actual_line = md_anchor_map.get(anchor)
    c_start = c.get("line_start")
    c_end = c.get("line_end")
    if actual_line is None:
        line_mismatches.append((c, "Anchor missing in MD", None))
    elif c_start != actual_line:
        line_mismatches.append((c, f"line_start={c_start} != actual_line={actual_line}", actual_line))

print(f"Clauses with line_start mismatched with actual anchor line in MD: {len(line_mismatches)}")
for c, err, act in line_mismatches[:15]:
    print(f"  Clause '{c.get('anchor')}': {err}")

# 6. Question and Answer Quality checks
print(f"\n=== QA QUALITY CHECKS ===")
empty_questions = [i for i, qa in enumerate(qa_data) if not str(qa.get("question", "")).strip()]
empty_answers = [i for i, qa in enumerate(qa_data) if not str(qa.get("answer", "")).strip()]
short_questions = [i for i, qa in enumerate(qa_data) if len(str(qa.get("question", "")).strip()) <= 10]
short_answers = [i for i, qa in enumerate(qa_data) if len(str(qa.get("answer", "")).strip()) <= 15]

print(f"Empty questions: {len(empty_questions)}")
print(f"Empty answers: {len(empty_answers)}")
print(f"Short questions (<=10 chars): {len(short_questions)}")
print(f"Short answers (<=15 chars): {len(short_answers)}")

questions = [qa.get("question", "") for qa in qa_data]
q_counter = Counter(questions)
dup_questions = {k: v for k, v in q_counter.items() if v > 1}
print(f"Duplicate questions count: {len(dup_questions)}")
for q, count in list(dup_questions.items())[:10]:
    print(f"  Dup ({count}x): '{q}'")

print(f"\n=== QA BENCHMARK FULL LIST INSPECTION ===")
# Let's inspect what types of anchors exist in QA benchmark:
ch_counts = Counter()
for qa in qa_data:
    a = qa.get("anchor", "")
    if a.startswith("muc-"):
        parts = a.split("-")
        ch_counts[parts[1]] += 1
    elif a.startswith("chuong-"):
        parts = a.split("-")
        ch_counts[f"chuong_{parts[1]}"] += 1
    elif a.startswith("phu-luc-"):
        parts = a.split("-")
        ch_counts[f"phu_luc_{parts[2]}"] += 1
    else:
        ch_counts["other"] += 1

print(f"Anchor distribution across sections in QA: {dict(ch_counts)}")
