"""Comprehensive Anchor Builder for ALL Sections, Tables, and Appendices in qcvn_06_2022_bxd.md."""

import re
import sys
from pathlib import Path
from typing import List, Set

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
base_file = bundle_dir / "qcvn_06_2022_bxd.md"
sd_file = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"


def make_canonical_anchor(sec_str: str) -> str:
    s = sec_str.strip().lower()
    if s.startswith("bảng"):
        t_id = s.replace("bảng", "").strip().lower()
        t_id = re.sub(r"[\s.]+", "-", t_id)
        return f"bang-{t_id}"
    if s.startswith("phụ lục"):
        pl_id = s.replace("phụ lục", "").strip().lower()
        return f"phu-luc-{pl_id}"
    s = re.sub(r"^[^\da-z]+", "", s)
    s = re.sub(r"[^\da-z]+$", "", s)
    s = re.sub(r"[\s.]+", "-", s)
    return f"muc-{s}"


def tag_all_sections_in_base() -> Set[str]:
    text = base_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    new_lines: List[str] = []
    generated_anchors: Set[str] = set()

    for idx, line in enumerate(lines):
        l_strip = line.strip()

        # Check existing anchor tags in the line
        existing_anchor_m = re.search(r'<a id="([^"]+)"[^>]*></a>', l_strip)
        if existing_anchor_m:
            generated_anchors.add(existing_anchor_m.group(1))

        # Check headings or paragraphs that start with section codes
        # e.g. "#### 6.13 ...", "##### A.1.2.1 ...", "### Bảng H.9 ...", "6.13  Mỗi khoang..."
        h_match = re.match(r"^(#{1,6}\s+)?(?:<a[^>]+></a>\s*)?((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+|Bảng\s+[A-Z0-9.]+|PHỤ LỤC\s+[A-Z])(\s+.*)?$", l_strip, re.IGNORECASE)

        if h_match:
            hashes = h_match.group(1) or "#### "
            sec_code = h_match.group(2).strip()
            rest = h_match.group(3) or ""

            # Exclude lines that are just numbers in tables or footnotes
            if l_strip.startswith("|") or l_strip.startswith("CHÚ THÍCH") or l_strip.startswith("_CHÚ THÍCH"):
                new_lines.append(line)
                continue

            anchor_id = make_canonical_anchor(sec_code)
            generated_anchors.add(anchor_id)

            # Strip old anchor tags from rest
            rest_clean = re.sub(r"<a[^>]+></a>", "", rest).strip()
            new_line = f'{hashes.strip()} <a id="{anchor_id}" name="{anchor_id}"></a>{sec_code}  {rest_clean}'.strip()
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    new_text = "\n".join(new_lines)
    base_file.write_text(new_text, encoding="utf-8")
    return generated_anchors


def update_all_sd1_links(base_anchors: Set[str]) -> None:
    text = sd_file.read_text(encoding="utf-8")

    def replacer(m: re.Match) -> str:
        label = m.group(1)
        target = m.group(2)

        if not target.startswith("qcvn_06_2022_bxd.md#"):
            return m.group(0)

        old_anchor = target.split("#", 1)[1]
        if old_anchor in base_anchors:
            return m.group(0)

        # Try to find corresponding canonical anchor
        sec_m = re.search(r"((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)", label)
        tbl_m = re.search(r"Bảng\s+([A-Z0-9.]+)", label, re.IGNORECASE)
        app_m = re.search(r"Phụ lục\s+([A-Z])", label, re.IGNORECASE)

        cand = None
        if tbl_m:
            c = f"bang-{tbl_m.group(1).lower().replace('.', '-')}"
            if c in base_anchors:
                cand = c
        elif app_m:
            c = f"phu-luc-{app_m.group(1).lower()}"
            if c in base_anchors:
                cand = c
        elif sec_m:
            c = f"muc-{sec_m.group(1).lower().replace('.', '-')}"
            if c in base_anchors:
                cand = c

        if cand:
            return f"[{label}](qcvn_06_2022_bxd.md#{cand})"
        return m.group(0)

    new_text = re.sub(r"\[([^\]]+)\]\((qcvn_06_2022_bxd\.md#[^\)]+)\)", replacer, text)
    sd_file.write_text(new_text, encoding="utf-8")


def main() -> None:
    base_anchors = tag_all_sections_in_base()
    print(f"✅ Đã tạo {len(base_anchors)} thẻ neo canonical trong qcvn_06_2022_bxd.md")
    update_all_sd1_links(base_anchors)
    print("✅ Đã cập nhật liên kết trong sua_doi_1_2023...")


if __name__ == "__main__":
    main()
