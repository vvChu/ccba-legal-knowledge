"""Inject 132 precise cross-links into sua_doi_1_2023_qcvn_06_2022_bxd.md pointing to qcvn_06_2022_bxd.md."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
base_file = bundle_dir / "qcvn_06_2022_bxd.md"
sd_file = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"

base_text = base_file.read_text(encoding="utf-8")
base_anchors = set(re.findall(r'<a id="([^"]+)"', base_text))
print(f"Base anchors count: {len(base_anchors)}")

sd_text = sd_file.read_text(encoding="utf-8")

# Pattern to link: "điểm 5.1.3.3", "khoản 1.1.2", "Bảng 10", "Bảng H.9", "Phụ lục A"
def inject_link(m: re.Match) -> str:
    full = m.group(0)
    prefix = m.group(1)  # e.g. "điểm ", "Bảng ", "khoản "
    code = m.group(2).strip()

    if "bang" in prefix.lower():
        slug = f"bang-{code.lower().replace('.', '-')}"
    elif "phụ lục" in prefix.lower():
        slug = f"phu-luc-{code.lower()}"
    else:
        slug = f"muc-{code.lower().replace('.', '-')}"

    if slug in base_anchors:
        return f"[{full}](qcvn_06_2022_bxd.md#{slug})"
    return full

# Only link occurrences in headings like "#### Sửa đổi điểm 1.1.2" or "#### Bổ sung Bảng 10"
def process_heading(line: str) -> str:
    if line.startswith("#") and "qcvn_06_2022_bxd.md" not in line:
        # Match "điểm X.Y.Z"
        line = re.sub(r"(điểm\s+|khoản\s+|mục\s+)((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)", inject_link, line)
        # Match "Bảng X"
        line = re.sub(r"(Bảng\s+)([A-Z0-9.]+)", inject_link, line)
        # Match "Phụ lục X"
        line = re.sub(r"(Phụ lục\s+)([A-Z])\b", inject_link, line)
    return line

lines = sd_text.splitlines()
new_lines = [process_heading(l) for l in lines]
new_text = "\n".join(new_lines)
sd_file.write_text(new_text, encoding="utf-8")

print(f"✅ Injected cross-links into sua_doi_1_2023_qcvn_06_2022_bxd.md")
