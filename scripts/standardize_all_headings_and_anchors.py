"""CCBA Master Heading & Anchor Normalization Engine.

1. Fixes sub-dot spaces: '5.3  1' -> '5.3.1', '6.2.2  1' -> '6.2.2.1'
2. Converts bold section tags '__A.1.2.1__' -> '##### <a id="muc-a-1-2-1" name="muc-a-1-2-1"></a>A.1.2.1'
3. Establishes canonical anchors for all Appendices and Tables
4. Re-links all cross-references in sua_doi_1_2023_qcvn_06_2022_bxd.md
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
base_file = bundle_dir / "qcvn_06_2022_bxd.md"
sd_file = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"


def make_anchor_slug(sec_code: str) -> str:
    s = sec_code.strip().lower()
    if s.startswith("bảng"):
        t = s.replace("bảng", "").strip().lower()
        t = re.sub(r"[\s.]+", "-", t)
        return f"bang-{t}"
    if s.startswith("phụ lục"):
        pl = s.replace("phụ lục", "").strip().lower()
        return f"phu-luc-{pl}"
    s = re.sub(r"^[^\da-z]+", "", s)
    s = re.sub(r"[^\da-z]+$", "", s)
    s = re.sub(r"[\s.]+", "-", s)
    return f"muc-{s}"


def clean_and_tag_base_doc() -> Set[str]:
    text = base_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    new_lines: List[str] = []
    anchors: Set[str] = set()

    for line in lines:
        l = line.strip()

        # Check for Appendix headers e.g. '__PHỤ LỤC A__' or '#### PHỤ LỤC A'
        app_m = re.search(r"PHỤ LỤC\s+([A-Z])", l, re.IGNORECASE)
        if ("__PHỤ LỤC" in l or "#### PHỤ LỤC" in l or "### PHỤ LỤC" in l or "## PHỤ LỤC" in l) and app_m:
            pl_letter = app_m.group(1).upper()
            slug = f"phu-luc-{pl_letter.lower()}"
            anchors.add(slug)
            clean_title = re.sub(r"<a[^>]+></a>", "", l).replace("__", "").strip()
            new_lines.append(f'## <a id="{slug}" name="{slug}"></a>{clean_title}')
            continue

        # Check for Tables e.g. '### Bảng 4' or '### Bảng H.9' or '**Bảng 10**'
        tbl_m = re.match(r"^(?:#{1,6}\s+|\*\*)?(?:<a[^>]+></a>\s*)?(Bảng\s+([A-Z0-9.]+))(?:\s*-\s*|\s+)(.*)$", l, re.IGNORECASE)
        if tbl_m and not l.startswith("|"):
            tbl_full = tbl_m.group(1)
            tbl_code = tbl_m.group(2)
            tbl_desc = tbl_m.group(3).replace("**", "").strip()
            slug = make_anchor_slug(tbl_full)
            anchors.add(slug)
            new_lines.append(f'### <a id="{slug}" name="{slug}"></a>{tbl_full} - {tbl_desc}')
            continue

        # Fix sub-dot spaces e.g. '5.3  1' -> '5.3.1', '6.2.2  3' -> '6.2.2.3', '### 2.5.3  1' -> '### 2.5.3.1'
        l_fixed = re.sub(r"^((?:#{1,6}\s+)?(?:<a[^>]+></a>\s*)?)(\d+(?:\.\d+)+)\s+(\d+)\b", r"\1\2.\3", l)
        l_fixed = re.sub(r"^(__)(\d+(?:\.\d+)+)\s+(\d+)(__)", r"\1\2.\3\4", l_fixed)

        # Check for section markers e.g. '##### 1.1.2', '__A.1.2.1__', '### 6.13'
        sec_m = re.match(r"^(?:#{1,6}\s+|__)?(?:<a[^>]+></a>\s*)?((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)(?:__|:)?\s*(.*)$", l_fixed)
        if sec_m and not l_fixed.startswith("|") and not l_fixed.startswith("_CHÚ THÍCH") and not l_fixed.startswith("CHÚ THÍCH"):
            sec_code = sec_m.group(1)
            rest_text = sec_m.group(2).replace("__", "").strip()

            # Determine appropriate heading level based on dot count
            dots = sec_code.count(".")
            h_level = min(5, max(3, dots + 2))
            hashes = "#" * h_level

            slug = make_anchor_slug(sec_code)
            anchors.add(slug)
            new_lines.append(f'{hashes} <a id="{slug}" name="{slug}"></a>{sec_code}  {rest_text}'.strip())
            continue

        new_lines.append(line)

    new_text = "\n".join(new_lines)
    base_file.write_text(new_text, encoding="utf-8")
    return anchors


def harmonize_amendment_links(base_anchors: Set[str]) -> None:
    text = sd_file.read_text(encoding="utf-8")

    def replacer(m: re.Match) -> str:
        label = m.group(1)
        target = m.group(2)

        if not target.startswith("qcvn_06_2022_bxd.md#"):
            return m.group(0)

        # Extract section number / table name
        lbl_sec = re.search(r"((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)", label)
        lbl_tbl = re.search(r"Bảng\s+([A-Z0-9.]+)", label, re.IGNORECASE)
        lbl_app = re.search(r"Phụ lục\s+([A-Z])", label, re.IGNORECASE)

        target_slug = None
        if lbl_tbl:
            c = make_anchor_slug(f"Bảng {lbl_tbl.group(1)}")
            if c in base_anchors:
                target_slug = c
        elif lbl_app:
            c = make_anchor_slug(f"Phụ lục {lbl_app.group(1)}")
            if c in base_anchors:
                target_slug = c
        elif lbl_sec:
            c = make_anchor_slug(lbl_sec.group(1))
            if c in base_anchors:
                target_slug = c

        if not target_slug:
            old_slug = target.split("#", 1)[1]
            if old_slug in base_anchors:
                target_slug = old_slug

        if target_slug:
            return f"[{label}](qcvn_06_2022_bxd.md#{target_slug})"
        return m.group(0)

    new_text = re.sub(r"\[([^\]]+)\]\((qcvn_06_2022_bxd\.md#[^\)]+)\)", replacer, text)
    sd_file.write_text(new_text, encoding="utf-8")


def main() -> None:
    print("=================================================================")
    print("      MASTER HARMONIZATION OF CANONICAL ANCHORS & LINKS         ")
    print("=================================================================")

    base_anchors = clean_and_tag_base_doc()
    print(f"✅ Đã tạo {len(base_anchors)} thẻ neo canonical chuẩn hóa trong qcvn_06_2022_bxd.md")

    harmonize_amendment_links(base_anchors)
    print("✅ Đã chuẩn hóa toàn bộ các liên kết đối soát trong sua_doi_1_2023...")
    print("=================================================================")


if __name__ == "__main__":
    main()
