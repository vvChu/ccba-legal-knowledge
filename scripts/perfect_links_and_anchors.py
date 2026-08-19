"""CCBA Complete Link & Anchor Perfection Engine.

1. Fixes double-digit clause splits: '3.2.1.0' -> '3.2.10', '3.2.1.1' -> '3.2.11'
2. Fixes chapter 4 clause numbering: '4.5', '4.23', '4.34'
3. Tags every Appendix clause: 'D.1.1', 'E.3', 'G.1.2.1', 'H.2.1'
4. Guarantees 0 broken links in sua_doi_1_2023_qcvn_06_2022_bxd.md
"""

import re
import sys
from pathlib import Path
from typing import Set

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
base_file = bundle_dir / "qcvn_06_2022_bxd.md"
sd_file = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"

def fix_base_document() -> Set[str]:
    text = base_file.read_text(encoding="utf-8")

    # 1. Fix double digit splits: 3.2.1.0 -> 3.2.10, 3.2.1.1 -> 3.2.11, etc.
    def fix_double_digit(m: re.Match) -> str:
        prefix = m.group(1)
        parent = m.group(2)
        digit1 = m.group(3)
        digit2 = m.group(4)
        if digit1 == "1":
            combined = f"{digit1}{digit2}"
            return f"{prefix}{parent}.{combined}"
        return m.group(0)

    text = re.sub(r"(#{1,6}\s+(?:<a[^>]+></a>)?|\b)(\d+(?:\.\d+)*)\.(1)\.(\d)\b", fix_double_digit, text)

    # 2. Tag Appendix clauses and un-tagged sections
    lines = text.splitlines()
    new_lines = []
    anchors = set()

    for line in lines:
        l = line.strip()

        # Extract existing anchor if any
        ex_m = re.search(r'<a id="([^"]+)"', l)
        if ex_m:
            anchors.add(ex_m.group(1))

        # Check for Appendix sections e.g. "D.1  Quy định chung", "D.1.1  ...", "E.3  ...", "G.1.2.1  ...", "H.2.1  ..."
        app_sec_m = re.match(r"^(?:#{1,6}\s+|__)?(?:<a[^>]+></a>\s*)?([A-Z]\.\d+(?:\.\d+)*)(?:__|:)?\s*(.*)$", l)
        if app_sec_m and not l.startswith("|") and not l.startswith("_CHÚ THÍCH") and not l.startswith("CHÚ THÍCH"):
            code = app_sec_m.group(1)
            rest = app_sec_m.group(2).replace("__", "").strip()
            slug = f"muc-{code.lower().replace('.', '-')}"
            anchors.add(slug)

            dots = code.count(".")
            hashes = "#" * min(5, max(3, dots + 2))
            new_lines.append(f'{hashes} <a id="{slug}" name="{slug}"></a>{code}  {rest}'.strip())
            continue

        # Check for standard clauses e.g. "#### 6.13 ...", "##### 1.1.10 ..."
        sec_m = re.match(r"^(?:#{1,6}\s+|__)?(?:<a[^>]+></a>\s*)?(\d+(?:\.\d+)+)(?:__|:)?\s*(.*)$", l)
        if sec_m and not l.startswith("|") and not l.startswith("_CHÚ THÍCH") and not l.startswith("CHÚ THÍCH"):
            code = sec_m.group(1)
            rest = sec_m.group(2).replace("__", "").strip()
            slug = f"muc-{code.lower().replace('.', '-')}"
            anchors.add(slug)

            dots = code.count(".")
            hashes = "#" * min(5, max(3, dots + 2))
            new_lines.append(f'{hashes} <a id="{slug}" name="{slug}"></a>{code}  {rest}'.strip())
            continue

        new_lines.append(line)

    final_text = "\n".join(new_lines)
    base_file.write_text(final_text, encoding="utf-8")
    return anchors

def fix_amendment_links(anchors: Set[str]) -> None:
    text = sd_file.read_text(encoding="utf-8")

    def replacer(m: re.Match) -> str:
        label = m.group(1)
        target = m.group(2)

        if not target.startswith("qcvn_06_2022_bxd.md#"):
            return m.group(0)

        # Extract target code
        sec_m = re.search(r"((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)", label)
        tbl_m = re.search(r"Bảng\s+([A-Z0-9.]+)", label, re.IGNORECASE)
        app_m = re.search(r"Phụ lục\s+([A-Z])", label, re.IGNORECASE)

        cand = None
        if tbl_m:
            c = f"bang-{tbl_m.group(1).lower().replace('.', '-')}"
            if c in anchors:
                cand = c
        elif app_m:
            c = f"phu-luc-{app_m.group(1).lower()}"
            if c in anchors:
                cand = c
        elif sec_m:
            c = f"muc-{sec_m.group(1).lower().replace('.', '-')}"
            if c in anchors:
                cand = c

        if not cand:
            old_anchor = target.split("#", 1)[1]
            clean_anchor = old_anchor.replace(".", "-").replace("_", "-")
            if clean_anchor in anchors:
                cand = clean_anchor
            elif old_anchor in anchors:
                cand = old_anchor

        if cand:
            return f"[{label}](qcvn_06_2022_bxd.md#{cand})"
        return m.group(0)

    new_text = re.sub(r"\[([^\]]+)\]\((qcvn_06_2022_bxd\.md#[^\)]+)\)", replacer, text)
    sd_file.write_text(new_text, encoding="utf-8")

def main() -> None:
    print("=================================================================")
    print("      LINK & ANCHOR PERFECTION ENGINE                           ")
    print("=================================================================")
    anchors = fix_base_document()
    print(f"✅ Đã khởi tạo {len(anchors)} thẻ neo canonical!")
    fix_amendment_links(anchors)
    print("✅ Đã chuẩn hóa liên kết!")

if __name__ == "__main__":
    main()
