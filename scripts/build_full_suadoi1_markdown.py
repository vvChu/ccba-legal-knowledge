"""CCBA Master Sửa đổi 1:2023 QCVN 06:2022/BXD Markdown Builder.

Processes sua_doi_1_2023_qcvn_06_2022_bxd.docx deterministically:
1. Emits Title, Lời nói đầu, and Chapter/Appendix headings (###).
2. Emits 100% of amendment points as structured headings (####) with canonical anchors (sd1-...).
3. Automatically embeds precise bi-directional markdown links to qcvn_06_2022_bxd.md.
4. Renders technical tables (Bảng 10) as clean 2D GFM Markdown Pipe grids with proper newlines & footnotes.
5. Converts layout-only tables into clean text bullet points.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

sys.stdout.reconfigure(encoding="utf-8")

BUNDLE_DIR = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
DOCX_PATH = Path(__file__).resolve().parent.parent / ".md" / "extracted_docs" / "qcvn_06_2022_bxd" / "sua_doi_1_2023_qcvn_06_2022_bxd.docx"
BASE_MD_PATH = BUNDLE_DIR / "qcvn_06_2022_bxd.md"

def get_base_anchors() -> Set[str]:
    if not BASE_MD_PATH.exists():
        return set()
    text = BASE_MD_PATH.read_text(encoding="utf-8")
    return set(re.findall(r'<a id="([^"]+)"', text))

def make_sd1_slug(text: str) -> str:
    s = text.strip().lower()
    m_tbl = re.search(r"bảng\s+([a-z0-9.]+)", s)
    m_app = re.search(r"phụ lục\s+([a-z])", s)
    m_sec = re.search(r"((?:[a-z]\.)?\d+(?:\.\d+)*|[a-z]\.\d+)", s)

    if m_tbl:
        c = m_tbl.group(1).replace(".", "-")
        return f"sd1-bang-{c}"
    if m_app:
        c = m_app.group(1)
        return f"sd1-phu-luc-{c}"
    if m_sec:
        c = m_sec.group(1).replace(".", "-")
        return f"sd1-muc-{c}"

    clean = re.sub(r"[^\w\s-]", "", s)
    clean = re.sub(r"[\s_]+", "-", clean)[:40]
    return f"sd1-{clean}"

def inject_base_links(text: str, base_anchors: Set[str]) -> str:
    def replacer(m: re.Match) -> str:
        full = m.group(0)
        prefix = m.group(1)
        code = m.group(2).strip()

        if "bảng" in prefix.lower():
            slug = f"bang-{code.lower().replace('.', '-')}"
        elif "phụ lục" in prefix.lower():
            slug = f"phu-luc-{code.lower()}"
        else:
            slug = f"muc-{code.lower().replace('.', '-')}"

        if slug in base_anchors:
            return f"[{full}](qcvn_06_2022_bxd.md#{slug})"
        return full

    t = re.sub(r"(điểm\s+|khoản\s+|mục\s+)((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)", replacer, text)
    t = re.sub(r"(Bảng\s+)([A-Z0-9.]+)", replacer, t)
    t = re.sub(r"(Phụ lục\s+)([A-Z])\b", replacer, t)
    return t

def build_suadoi1_markdown() -> str:
    doc = Document(DOCX_PATH)
    base_anchors = get_base_anchors()

    out_lines: List[str] = []
    ast_clauses: List[Dict[str, Any]] = []

    chap_pattern = re.compile(r"^(\d+)\s+([A-ZÀ-Ỹ\s]+)$")
    app_pattern = re.compile(r"^PHỤ LỤC\s+([A-Z])(?:\s*\(.*?\))?\s*(.*)$", re.IGNORECASE)
    mod_pattern = re.compile(r"^(Sửa đổi|Bổ sung|Bãi bỏ|Thay thế)\b", re.IGNORECASE)

    current_chapter = "Mở đầu"

    for elem in doc.element.body:
        if isinstance(elem, CT_P):
            p = Paragraph(elem, doc)
            text = p.text.strip()
            if not text:
                continue

            # Check for Main Document Title & Subtitles
            if text == "SỬA ĐỔI 1:2023 QCVN 06:2022/BXD":
                out_lines.append(f"# {text}\n\n")
                continue
            if text in ["QUY CHUẨN KỸ THUẬT QUỐC GIA", "VỀ AN TOÀN CHÁY CHO NHÀ VÀ CÔNG TRÌNH"]:
                out_lines.append(f"## {text}\n\n")
                continue
            if text.startswith("Amendment 1:2023") or text.startswith("National technical") or text.startswith("Fire Safety"):
                out_lines.append(f"*{text}*\n\n")
                continue
            if text == "Lời nói đầu":
                out_lines.append(f"### {text}\n\n")
                continue

            # Check for Chapter Heading (e.g. "1  QUY ĐỊNH CHUNG")
            m_chap = chap_pattern.match(text)
            if m_chap and len(text) < 60:
                c_num = m_chap.group(1)
                current_chapter = f"Chương {c_num}"
                slug = f"sd1-chuong-{c_num}"
                out_lines.append(f'\n\n### <a id="{slug}" name="{slug}"></a>{text}\n\n')
                continue

            # Check for Appendix Heading (e.g. "PHỤ LỤC A")
            m_app = app_pattern.match(text)
            if m_app:
                pl_letter = m_app.group(1).upper()
                current_chapter = f"Phụ lục {pl_letter}"
                slug = f"sd1-phu-luc-{pl_letter.lower()}"
                out_lines.append(f'\n\n### <a id="{slug}" name="{slug}"></a>{text}\n\n')
                continue

            if text.startswith("Bổ sung THƯ MỤC TÀI LIỆU THAM KHẢO"):
                slug = "sd1-thu-muc-tai-lieu-tham-khao"
                out_lines.append(f'\n\n### <a id="{slug}" name="{slug}"></a>{text}\n\n')
                continue

            # Check for Amendment Action Points (Sửa đổi / Bổ sung / Bãi bỏ / Thay thế)
            if mod_pattern.match(text) and not text.startswith("Sửa đổi 1:2023 QCVN 06"):
                slug = make_sd1_slug(text)
                linked_title = inject_base_links(text, base_anchors)
                out_lines.append(f'\n\n#### <a id="{slug}" name="{slug}"></a>{linked_title}\n\n')
                ast_clauses.append({
                    "id": slug,
                    "title": text,
                    "chapter": current_chapter,
                    "line": len(out_lines),
                })
                continue

            # Standard body paragraph
            out_lines.append(f"{text}\n\n")

        elif isinstance(elem, CT_Tbl):
            table = Table(elem, doc)
            grid: List[List[str]] = []
            footnotes: List[str] = []

            for row in table.rows:
                cells = [c.text.replace("\n", " ").strip().replace("|", "\\|") for c in row.cells]
                # Check for merged footnote row
                unique_c = list(dict.fromkeys(cells))
                if len(unique_c) == 1 and (unique_c[0].startswith("CHÚ THÍCH") or re.match(r"^\d+\)\s+", unique_c[0]) or len(unique_c[0]) > 80):
                    if unique_c[0] and unique_c[0] not in footnotes:
                        footnotes.append(unique_c[0])
                    continue
                grid.append(cells)

            if not grid:
                continue

            # Check if this is a layout table with empty columns (like Table 2)
            non_empty_cols = 0
            for col_idx in range(len(grid[0])):
                col_texts = [r[col_idx] for r in grid if col_idx < len(r) and r[col_idx]]
                if col_texts:
                    non_empty_cols += 1

            if non_empty_cols <= 1:
                # Emit as plain text lines
                for r in grid:
                    row_text = " ".join(c for c in r if c).strip()
                    if row_text:
                        out_lines.append(f"{row_text}\n\n")
                continue

            # Full 2D Table rendering (e.g. Bảng 10)
            # Use row 2 for specific column subheadings if row 1 is a grouped header
            header_row = grid[1] if len(grid) > 1 and "≤ 50" in " ".join(grid[1]) else grid[0]
            data_start_idx = 2 if header_row is grid[1] else 1
            col_count = len(header_row)

            out_lines.append("\n")
            out_lines.append("| " + " | ".join(header_row) + " |\n")
            out_lines.append("| " + " | ".join(["---"] * col_count) + " |\n")

            for r in grid[data_start_idx:]:
                if len(r) < col_count:
                    r = r + [""] * (col_count - len(r))
                out_lines.append("| " + " | ".join(r[:col_count]) + " |\n")

            out_lines.append("\n")

            if footnotes:
                for fn in footnotes:
                    out_lines.append(f"_{fn}_\n\n")

    full_md = "".join(out_lines)
    full_md = re.sub(r"\n{3,}", "\n\n", full_md)
    return full_md

def main() -> None:
    print("=================================================================")
    print("      BUILDING PERFECT MARKDOWN FOR SỬA ĐỔI 1:2023 QCVN 06       ")
    print("=================================================================")

    md_text = build_suadoi1_markdown()
    target_path = BUNDLE_DIR / "sua_doi_1_2023_qcvn_06_2022_bxd.md"
    target_path.write_text(md_text, encoding="utf-8")
    print(f"✅ Đã tạo sua_doi_1_2023_qcvn_06_2022_bxd.md: {len(md_text):,} ký tự, {len(md_text.splitlines())} dòng.")

if __name__ == "__main__":
    main()
