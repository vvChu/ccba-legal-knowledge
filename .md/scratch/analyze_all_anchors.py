import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
from pathlib import Path
from collections import Counter

repo_root = Path(r"d:\GitHubProjects\ccba-legal-knowledge")
bundle_dir = repo_root / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
md_path = bundle_dir / "qcvn_06_2022_bxd.md"

md_lines = md_path.read_text(encoding="utf-8").splitlines()

anchors = []
for idx, line in enumerate(md_lines, 1):
    m = re.findall(r'<a id="([^"]+)"></a>', line)
    for a in m:
        anchors.append((idx, a, line))

print(f"Total anchors found: {len(anchors)}")

prefix_counts = Counter()
for _, a, _ in anchors:
    parts = a.split("-")
    prefix = parts[0]
    if len(parts) > 1:
        prefix = f"{parts[0]}-{parts[1]}"
    prefix_counts[prefix] += 1

print("\n=== ANCHOR PREFIX COUNTS ===")
for p, c in sorted(prefix_counts.items(), key=lambda x: -x[1]):
    print(f"  {p:<25}: {c}")

print("\n=== SAMPLE OF 'OTHER' / APPENDIX ANCHORS ===")
for idx, a, line in anchors:
    if not a.startswith("muc-") and not a.startswith("chuong-"):
        print(f"Line {idx:4d}: {a:<30} | {line[:70]}")
