"""CCBA Dot-Split and Canonical Heading Restorer.

Restores accurate decimal dot numbering across chapters:
- 1.11 -> 1.1.1, 1.12 -> 1.1.2, ..., 1.19 -> 1.1.9, 1.110 -> 1.1.10
- 2.11 -> 2.1.1, ..., 2.533 -> 2.5.3.3
- 5.133 -> 5.1.3.3, 5.134 -> 5.1.3.4
- Inlines canonical anchors: ### <a id="muc-X" name="muc-X"></a>X
"""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
base_file = bundle_dir / "qcvn_06_2022_bxd.md"

def fix_dots_in_text(text: str) -> str:
    # 1. Fix Chapter 1: 1.11 -> 1.1.1, 1.12 -> 1.1.2 ... 1.19 -> 1.1.9, 1.110 -> 1.1.10
    for u in range(1, 10):
        text = re.sub(rf"(#+|\b)1\.1{u}\b", rf"\g<1>1.1.{u}", text)
        text = re.sub(rf"(#+|\b)1\.2{u}\b", rf"\g<1>1.2.{u}", text)
        text = re.sub(rf"(#+|\b)1\.3{u}\b", rf"\g<1>1.3.{u}", text)
    text = re.sub(r"(#+|\b)1\.110\b", r"\g<1>1.1.10", text)

    # 2. Fix 4-level section numbers across Chapters 2-7
    # E.g. 5.1.33 -> 5.1.3.3, 5.1.34 -> 5.1.3.4, 2.5.31 -> 2.5.3.1, 2.5.32 -> 2.5.3.2, 2.5.33 -> 2.5.3.3
    text = re.sub(r"(#+|\b)(\d+\.\d+\.\d)(\d)\b", r"\1\2.\3", text)

    # E.g. 3-level section numbers where 2nd dot missing: 5.11 -> 5.1.1, 5.12 -> 5.1.2 ... 5.19 -> 5.1.9
    for c in [2, 3, 4, 5, 6, 7]:
        for s in range(1, 10):
            for u in range(1, 10):
                text = re.sub(rf"(#+|\b){c}\.{s}{u}\b", rf"\g<1>{c}.{s}.{u}", text)

    # 3. Ensure heading lines have canonical anchors
    lines = text.splitlines()
    new_lines = []

    for line in lines:
        l = line.strip()

        # Match heading with section number
        m_h = re.match(r"^(#{1,6})\s+(?:<a[^>]+></a>\s*)?((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)\s*(.*)$", l)
        if m_h and not l.startswith("|") and not l.startswith("_CHÚ THÍCH") and not l.startswith("CHÚ THÍCH"):
            hashes = m_h.group(1)
            code = m_h.group(2)
            rest = m_h.group(3).strip()
            rest_clean = re.sub(r"<a[^>]+></a>", "", rest).strip()

            slug = f"muc-{code.lower().replace('.', '-')}"
            new_lines.append(f'{hashes} <a id="{slug}" name="{slug}"></a>{code}  {rest_clean}'.strip())
            continue

        # Match Table heading
        m_tbl = re.match(r"^(#{1,6})\s+(?:<a[^>]+></a>\s*)?(Bảng\s+([A-Z0-9.]+))\s*[-–:]?\s*(.*)$", l, re.IGNORECASE)
        if m_tbl and not l.startswith("|"):
            hashes = m_tbl.group(1)
            full_t = m_tbl.group(2)
            t_num = m_tbl.group(3)
            desc = m_tbl.group(4).strip()
            desc_clean = re.sub(r"<a[^>]+></a>", "", desc).strip()
            slug = f"bang-{t_num.lower().replace('.', '-')}"
            new_lines.append(f'{hashes} <a id="{slug}" name="{slug}"></a>{full_t} - {desc_clean}'.strip())
            continue

        # Match Appendix heading
        m_app = re.match(r"^(#{1,6})\s+(?:<a[^>]+></a>\s*)?(PHỤ LỤC\s+([A-Z]))\s*(.*)$", l, re.IGNORECASE)
        if m_app:
            hashes = m_app.group(1)
            full_app = m_app.group(2)
            app_let = m_app.group(3).lower()
            desc = m_app.group(4).strip()
            slug = f"phu-luc-{app_let}"
            new_lines.append(f'{hashes} <a id="{slug}" name="{slug}"></a>{full_app} {desc}'.strip())
            continue

        new_lines.append(line)

    return "\n".join(new_lines)

def main() -> None:
    text = base_file.read_text(encoding="utf-8")
    fixed_text = fix_dots_in_text(text)
    base_file.write_text(fixed_text, encoding="utf-8")
    print(f"✅ Fixed all dot splits and canonical anchors in qcvn_06_2022_bxd.md")

if __name__ == "__main__":
    main()
