import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
from pathlib import Path
from collections import defaultdict

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

# Extract all anchors and headings from MD
md_items = []
for idx, line in enumerate(md_lines, 1):
    m = re.findall(r'<a id="([^"]+)"></a>', line)
    if m:
        for a in m:
            # Look at next non-empty line or current line for heading text
            heading = line
            for offset in range(1, 4):
                if idx - 1 + offset < len(md_lines):
                    next_l = md_lines[idx - 1 + offset].strip()
                    if next_l.startswith("#"):
                        heading = next_l
                        break
                    elif next_l and heading == line:
                        heading = next_l
            md_items.append({
                "line": idx,
                "anchor": a,
                "heading": heading
            })

print(f"Total MD items with anchor: {len(md_items)}")

# Classify MD items by Chapter/Appendix
md_by_section = defaultdict(list)
for item in md_items:
    a = item["anchor"]
    if a.startswith("chuong-") or a.startswith("muc-1") or a.startswith("dieu-1"):
        md_by_section["ch1"].append(item)
    elif a.startswith("muc-2") or a.startswith("dieu-2") or a.startswith("chuong-2"):
        md_by_section["ch2"].append(item)
    elif a.startswith("muc-3") or a.startswith("dieu-3") or a.startswith("chuong-3"):
        md_by_section["ch3"].append(item)
    elif a.startswith("muc-4") or a.startswith("dieu-4") or a.startswith("chuong-4"):
        md_by_section["ch4"].append(item)
    elif a.startswith("muc-5") or a.startswith("dieu-5") or a.startswith("chuong-5"):
        md_by_section["ch5"].append(item)
    elif a.startswith("muc-6") or a.startswith("dieu-6") or a.startswith("chuong-6"):
        md_by_section["ch6"].append(item)
    elif a.startswith("muc-7") or a.startswith("dieu-7") or a.startswith("chuong-7"):
        md_by_section["ch7"].append(item)
    elif a.startswith("phu-luc-") or a.startswith("pl-") or a.startswith("bang-"):
        md_by_section["appendices"].append(item)
    else:
        md_by_section["other"].append(item)

print("\n=== MD ANCHOR BREAKDOWN BY SECTION ===")
for sec, items in md_by_section.items():
    print(f"  {sec:<12}: {len(items)} anchors")

# Check which MD anchors are in qa_benchmark
qa_anchors = {qa["anchor"]: qa for qa in qa_data}
clauses_anchors = {c["anchor"]: c for c in clauses_data}

print("\n=== COVERAGE OF MD ANCHORS IN QA BENCHMARK ===")
for sec, items in md_by_section.items():
    present = sum(1 for it in items if it["anchor"] in qa_anchors)
    print(f"  {sec:<12}: {present}/{len(items)} in QA benchmark ({present/len(items)*100:.1f}%)")

