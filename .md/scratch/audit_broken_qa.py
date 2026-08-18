import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
from pathlib import Path
from collections import defaultdict

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

md_lines = md_path.read_text(encoding="utf-8").splitlines()
sd1_lines = sd1_path.read_text(encoding="utf-8").splitlines()

# Build MD anchor to line map and heading map
md_anchor_to_line = {}
md_anchor_to_heading = {}
for idx, line in enumerate(md_lines, 1):
    m = re.findall(r'<a id="([^"]+)"></a>', line)
    for a in m:
        md_anchor_to_line[a] = idx
        # Find heading text on this or following lines
        heading = line
        for offset in range(1, 4):
            if idx - 1 + offset < len(md_lines):
                next_l = md_lines[idx - 1 + offset].strip()
                if next_l.startswith("#"):
                    heading = next_l
                    break
                elif next_l and heading == line:
                    heading = next_l
        md_anchor_to_heading[a] = heading

print(f"Total entries in qa_benchmark: {len(qa_data)}")

# Map broken chapter 4 anchors to real anchors
broken_mapping = {
    "muc-4-1-0": "muc-4-10",
    "muc-4-1-1": "muc-4-11",
    "muc-4-1-2": "muc-4-12",
    "muc-4-1-3": "muc-4-13",
    "muc-4-1-4": "muc-4-14",
    "muc-4-1-5": "muc-4-15",
    "muc-4-1-6": "muc-4-16",
    "muc-4-1-7": "muc-4-17",
    "muc-4-1-8": "muc-4-18",
    "muc-4-1-9": "muc-4-19",
    "muc-4-2-0": "muc-4-20",
    "muc-4-2-1": "muc-4-21",
    "muc-4-2-2": "muc-4-22",
    "muc-4-2-3": "muc-4-23",
    "muc-4-2-4": "muc-4-24",
    "muc-4-2-5": "muc-4-25",
    "muc-4-2-6": "muc-4-26",
    "muc-4-2-7": "muc-4-27",
    "muc-4-2-8": "muc-4-28",
    "muc-4-2-9": "muc-4-29",
    "muc-4-3-0": "muc-4-30",
    "muc-4-3-1": "muc-4-31",
    "muc-4-3-2": "muc-4-32",
    "muc-4-3-3": "muc-4-33",
    "muc-4-3-4": "muc-4-34",
    "muc-4-3-5": "muc-4-35",
}

print("\n=== DETAILED ANALYSIS OF THE 26 BROKEN CHAPTER 4 QA ENTRIES ===")
for old_a, new_a in broken_mapping.items():
    qa_item = next((q for q in qa_data if q["anchor"] == old_a), None)
    real_line = md_anchor_to_line.get(new_a)
    real_heading = md_anchor_to_heading.get(new_a)
    if qa_item:
        print(f"OLD: anchor='{old_a}' | Q='{qa_item['question']}'")
        print(f"     A='{qa_item['answer'][:60]}...'")
        print(f"NEW: anchor='{new_a}' | Line={real_line} | Heading='{real_heading}'")
        print("-" * 70)

# Check all 183 QA entries against MD headings
print("\n=== AUDITING ALL 183 QA ENTRIES AGAINST MD ===")
valid_count = 0
broken_count = 0
for idx, qa in enumerate(qa_data):
    a = qa["anchor"]
    if a in md_anchor_to_line:
        valid_count += 1
    else:
        broken_count += 1

print(f"Valid anchors in MD: {valid_count}/183")
print(f"Broken anchors in MD: {broken_count}/183")
