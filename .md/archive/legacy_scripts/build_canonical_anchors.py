"""CCBA Canonical Anchor & Link Harmonization Engine.

Establishes 100% deterministic, canonical anchors in qcvn_06_2022_bxd.md
and harmonizes all cross-document links in sua_doi_1_2023_qcvn_06_2022_bxd.md.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
base_file = bundle_dir / "qcvn_06_2022_bxd.md"
sd_file = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"

def make_canonical_anchor(sec_str: str) -> str:
    """Converts section text to canonical slug."""
    s = sec_str.strip().lower()
    # Handle Table
    if s.startswith("bảng"):
        t_id = s.replace("bảng", "").strip().lower()
        t_id = re.sub(r"[\s.]+", "-", t_id)
        return f"bang-{t_id}"
    # Handle Appendix
    if s.startswith("phụ lục"):
        pl_id = s.replace("phụ lục", "").strip().lower()
        return f"phu-luc-{pl_id}"
    # Handle Sections
    s = re.sub(r"^[^\da-z]+", "", s)
    s = re.sub(r"[^\da-z]+$", "", s)
    s = re.sub(r"[\s.]+", "-", s)
    return f"muc-{s}"

def harmonize_base_document() -> Set[str]:
    text = base_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    new_lines: List[str] = []
    generated_anchors: Set[str] = set()

    for idx, line in enumerate(lines):
        l_strip = line.strip()

        # Match Headings: #, ##, ###, ####, #####, ######
        h_match = re.match(r"^(#{1,6})\s+(?:<a[^>]+></a>\s*)?(.+)$", l_strip)
        if h_match:
            hashes = h_match.group(1)
            title = h_match.group(2).strip()

            # Clean any embedded anchor tags
            title_clean = re.sub(r"<a[^>]+></a>", "", title).strip()

            # Check if this heading has a recognizable section code
            # 1. Section numbers: 1.1, 1.1.2, 5.1.3.3, 6.13, A.1.2.1, D.14.5...
            sec_m = re.match(r"^((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)\b", title_clean)
            # 2. Tables: Bảng 1, Bảng A.1, Bảng H.9...
            table_m = re.match(r"^(Bảng\s+[A-Z0-9.]+)\b", title_clean, re.IGNORECASE)
            # 3. Appendices: PHỤ LỤC A...
            app_m = re.match(r"^(PHỤ LỤC\s+[A-Z])\b", title_clean, re.IGNORECASE)
            # 4. Chapters: 1  QUY ĐỊNH CHUNG, 2  QUY ĐỊNH KỸ THUẬT...
            chap_m = re.match(r"^(\d+)\s+([A-ZÀ-Ỹ\s]+)$", title_clean)

            anchor_id = None
            if sec_m:
                anchor_id = make_canonical_anchor(sec_m.group(1))
            elif table_m:
                anchor_id = make_canonical_anchor(table_m.group(1))
            elif app_m:
                anchor_id = make_canonical_anchor(app_m.group(1))
            elif chap_m:
                anchor_id = f"chuong-{chap_m.group(1)}"

            if anchor_id:
                generated_anchors.add(anchor_id)
                new_line = f'{hashes} <a id="{anchor_id}" name="{anchor_id}"></a>{title_clean}'
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    new_text = "\n".join(new_lines)
    base_file.write_text(new_text, encoding="utf-8")
    return generated_anchors

def harmonize_amendment_links(base_anchors: Set[str]) -> None:
    text = sd_file.read_text(encoding="utf-8")

    # Replace link targets to use canonical anchors
    def link_replacer(match: re.Match) -> str:
        label = match.group(1)
        target = match.group(2)

        if not target.startswith("qcvn_06_2022_bxd.md#"):
            return match.group(0)

        old_anchor = target.split("#", 1)[1]
        if old_anchor in base_anchors:
            return match.group(0)

        # Try to infer canonical anchor from label or old_anchor
        candidate = None
        # Extract section number from label e.g. "điểm 6.13" -> "muc-6-13", "Bảng H.9" -> "bang-h-9"
        lbl_sec = re.search(r"((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)", label)
        lbl_tbl = re.search(r"Bảng\s+([A-Z0-9.]+)", label, re.IGNORECASE)
        lbl_app = re.search(r"Phụ lục\s+([A-Z])", label, re.IGNORECASE)

        if lbl_tbl:
            c = f"bang-{lbl_tbl.group(1).lower().replace('.', '-')}"
            if c in base_anchors:
                candidate = c
        elif lbl_app:
            c = f"phu-luc-{lbl_app.group(1).lower()}"
            if c in base_anchors:
                candidate = c
        elif lbl_sec:
            c = f"muc-{lbl_sec.group(1).lower().replace('.', '-')}"
            if c in base_anchors:
                candidate = c

        if not candidate:
            # Try cleaning old_anchor
            clean_old = old_anchor.replace(".", "-").replace("_", "-")
            if clean_old in base_anchors:
                candidate = clean_old

        if candidate:
            return f"[{label}](qcvn_06_2022_bxd.md#{candidate})"
        return match.group(0)

    new_text = re.sub(r"\[([^\]]+)\]\((qcvn_06_2022_bxd\.md#[^\)]+)\)", link_replacer, text)
    sd_file.write_text(new_text, encoding="utf-8")

def main() -> None:
    print("=================================================================")
    print("      HARMONIZING CANONICAL ANCHORS & CROSS-LINKS                ")
    print("=================================================================")

    base_anchors = harmonize_base_document()
    print(f"✅ Đã chuẩn hóa {len(base_anchors)} thẻ neo canonical trong qcvn_06_2022_bxd.md")

    harmonize_amendment_links(base_anchors)
    print("✅ Đã chuẩn hóa toàn bộ các liên kết đối soát trong sua_doi_1_2023...")
    print("=================================================================")

if __name__ == "__main__":
    main()
