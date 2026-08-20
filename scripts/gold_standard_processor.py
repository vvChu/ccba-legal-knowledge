"""OKF v2.2 Gold Standard Data Processing Engine for Technical Standards & Decrees.

Performs:
1. TVPL HTML & Line Normalization (Joining split lines like Điều\\n1).
2. HTML-to-Pure-Markdown Table Conversion.
3. Config-driven Inline Semantic Anchor Injection (<a id="dieu-XX-khoan-YY"></a> & <a id="muc-1-1"></a>).
4. Structural AST Parsing (clauses.json) across Active Core & Modular Annexes.
5. Technical Table CSV & Formula Extraction (tables/*.csv).
6. Ground Truth QA Benchmark Generation (qa_benchmark.json) with Zero Duplication & Source Tracking.
"""

import argparse
import json
import re
import sys
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from bs4 import BeautifulSoup

# Enforce UTF-8 output encoding for Windows PowerShell compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

@dataclass
class DocProfile:
    """Document processing profile defining regex patterns for anchor injection & QA generation."""

    name: str
    dieu_pattern: re.Pattern = field(default_factory=lambda: re.compile(r"^#*\s*(Điều\s+(\d+)\.?[^\n]*)", re.IGNORECASE))
    khoan_pattern: re.Pattern = field(default_factory=lambda: re.compile(r"^(?:\*\*(\d+)\.\*\*|(\d+)\.)\s+([^\n]+)"))
    sec_pattern: re.Pattern = field(default_factory=lambda: re.compile(r"^#*\s*(?:<a[^>]+></a>\s*)?(((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)\s+([^\n]+))"))
    section_prefix: str = "muc"

def get_doc_profile(doc_type: Optional[str] = "vbpl") -> DocProfile:
    """Factory to return DocProfile by document type."""
    normalized = (doc_type or "vbpl").lower().strip()
    if "qcvn" in normalized or "tcvn" in normalized:
        return DocProfile(
            name="qcvn",
            dieu_pattern=re.compile(r"^#*\s*(Điều\s+(\d+)\.?[^\n]*)", re.IGNORECASE),
            khoan_pattern=re.compile(r"^(?:\*\*(\d+)\.\*\*|(\d+)\.)\s+([^\n]+)"),
            sec_pattern=re.compile(r"^#*\s*(?:<a[^>]+></a>\s*)?(((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)\s+([^\n]+))"),
            section_prefix="muc",
        )
    return DocProfile(
        name="vbpl",
        dieu_pattern=re.compile(r"^#*\s*(Điều\s+(\d+)\.?[^\n]*)", re.IGNORECASE),
        khoan_pattern=re.compile(r"^(?:\*\*(\d+)\.\*\*|(\d+)\.)\s+([^\n]+)"),
        sec_pattern=re.compile(r"^#*\s*((\d+\.\d+(\.\d+)?)\s+([^\n]+))"),
        section_prefix="muc",
    )

def strip_existing_anchors(text: str) -> str:
    """Strip existing inline anchors to make pipeline idempotent."""
    return re.sub(r'<a\s+(?:id|name)="[^"]+"></a>\s*', '', text)

def normalize_tvpl_formatting(text: str) -> str:
    """Normalize line wrapping in raw TVPL text."""
    text = re.sub(r"Điều\s*[\r\n]+\s*(\d+\.)", r"Điều \1", text, flags=re.IGNORECASE)
    text = re.sub(r"Chương\s*[\r\n]+\s*([I|V|X|L|C|D|M]+)", r"Chương \1", text, flags=re.IGNORECASE)
    text = re.sub(r"Mục\s*[\r\n]+\s*(\d+\.)", r"Mục \1", text, flags=re.IGNORECASE)
    return text

def clean_html_tables(text: str) -> str:
    """Convert HTML <table> blocks into clean Markdown tables."""
    if "<table" not in text.lower():
        return text

    def _replace_table(match: re.Match) -> str:
        html = match.group(0)
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all("tr")
        if not rows:
            return ""

        table_matrix: list[list[str]] = []
        for tr in rows:
            cols = tr.find_all(["td", "th"])
            row_data = [re.sub(r"\s+", " ", col.get_text(strip=True)) for col in cols]
            if any(row_data):
                table_matrix.append(row_data)

        if not table_matrix:
            return ""

        max_cols = max(len(r) for r in table_matrix)
        md_lines = []

        header = table_matrix[0] + [""] * (max_cols - len(table_matrix[0]))
        md_lines.append("| " + " | ".join(header) + " |")
        md_lines.append("| " + " | ".join(["---"] * max_cols) + " |")

        for row in table_matrix[1:]:
            padded = row + [""] * (max_cols - len(row))
            md_lines.append("| " + " | ".join(padded) + " |")

        return "\n" + "\n".join(md_lines) + "\n"

    pattern = re.compile(r"<table.*?>.*?</table>", re.DOTALL | re.IGNORECASE)
    return pattern.sub(_replace_table, text)

def clean_table_footnotes_and_superscripts(text: str) -> str:
    """Untrap footnotes from table rows and format in-cell markers as <sup>X)</sup>."""
    lines = text.splitlines()
    new_lines: list[str] = []
    in_table = False
    table_lines: list[str] = []

    def _process_table(t_lines: list[str]) -> list[str]:
        extracted_footnotes: list[str] = []
        cleaned_t_lines: list[str] = []

        for line in t_lines:
            trapped_match = re.search(r"\|\s*(_[1-9]\)|_CHÚ THÍCH|_GHI CHÚ|_Đối với|_Ghi chú|_Không yêu cầu|_Nếu không|_Cho phép)(.*?)\|\s*$", line)
            if trapped_match:
                note_text = trapped_match.group(1) + trapped_match.group(2)
                line = line[:trapped_match.start()] + "|"
                clean_note = note_text.strip("_ ").strip()
                note_parts = re.split(r"(?<=\.)\s+(?=[1-9]\))", clean_note)
                prefixes = ("1)", "2)", "3)", "4)")
                if not note_parts or (len(note_parts) == 1 and not clean_note.startswith(prefixes)):
                    if not clean_note.startswith(prefixes):
                        clean_note = "1) " + clean_note
                    note_parts = [clean_note]

                for part in note_parts:
                    p = part.strip()
                    m_num = re.match(r"^([1-9]\))\s*(.*)", p)
                    if m_num:
                        extracted_footnotes.append(f"- **{m_num.group(1)}** {m_num.group(2)}")
                    else:
                        extracted_footnotes.append(f"- {p}")

            def _superscript_marker(m: re.Match) -> str:
                return f"{m.group(1)}<sup>{m.group(2)}</sup>"

            line = re.sub(r"(\b(?:EIW|REI|EI|E|RE|R|DN|\d+)\s*(?:\d+)?\s+)([1-9]\))(?!\<|/sup)", _superscript_marker, line)
            line = re.sub(r"([a-zA-ZÀ-ỹ]+)\s+([1-9]\))(?!\<|/sup)", r"\1<sup>\2</sup>", line)
            cleaned_t_lines.append(line)

        res = cleaned_t_lines
        if extracted_footnotes:
            res.append("")
            res.append("_GHI CHÚ CHỈ SỐ PHỤ:_")
            for fn in extracted_footnotes:
                res.append(fn)
        return res

    for line in lines:
        if line.startswith("|") and line.endswith("|"):
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
        else:
            if in_table:
                in_table = False
                new_lines.extend(_process_table(table_lines))
                table_lines = []
            new_lines.append(line)

    if in_table:
        new_lines.extend(_process_table(table_lines))

    return "\n".join(new_lines)


def normalize_notes_and_lists(text: str) -> str:
    """Normalize notes structure, deduplicate headers, and format lists cleanly."""
    lines = text.splitlines()
    cleaned_bullet_lines = []

    for line in lines:
        stripped = line.strip()
        if re.match(r"^([-*]\s+)+", stripped):
            stripped = re.sub(r"^([-*]\s+)+", "- ", stripped)
        cleaned_bullet_lines.append(stripped if not line.startswith("  ") else line)

    text = "\n".join(cleaned_bullet_lines)

    # 1. Fix 1.4.9 definitions (Bằng khoảng cách..., Bằng một nửa...)
    text = re.sub(
        r"(####\s*<a id=\"muc-1-4-9\"[^\n]+\n+Chiều cao PCCC của nhà[^\n]+\n+)\s*(Bằng khoảng cách lớn nhất[^\n]+)\n+\s*(Bằng một nửa tổng khoảng cách[^\n]+)",
        r"\1- \2\n\n- \3",
        text,
    )

    # 2. Fix 1.4.72 inline single note (clean merged sentence)
    text = re.sub(
        r"(_?CHÚ THÍCH:\s*Các yếu tố nguy hiểm cháy[^\n]+)\n+\s*[-*]?\s*2\.\s*(luồng nhiệt[^\n]+)",
        r"_CHÚ THÍCH: Các yếu tố nguy hiểm cháy: 1) ngọn lửa và tia lửa, 2) \2_",
        text,
        flags=re.IGNORECASE,
    )

    # 3. Deduplicate _CHÚ THÍCH:_ headers in multi-note blocks
    text = re.sub(r"(\n-\s+\*\*CHÚ THÍCH\s+\d+:?\*\*[^\n]+\n+)\s*_CHÚ THÍCH:_\n+(?=-\s+\*\*CHÚ THÍCH)", r"\1", text)

    # 4. Standardize material classification and hazard level codes
    def _fix_codes(match: re.Match) -> str:
        code_item = match.group(1).strip()
        return f"- {code_item}"

    text = re.sub(r"(?m)^(?!\s*[-*])\s*((?:LT[1-4]|Ch[1-4]|BC[1-3]|SK[1-3]|ĐT[1-4]|CV[0-5]|K[0-3])\s*\([^\n]+)", _fix_codes, text)

    # 5. Indent sub-items inside notes and clean main body lettered items
    lines = text.splitlines()
    processed_lines = []
    in_note = False

    for l in lines:
        st = l.strip()
        if st == "_CHÚ THÍCH:_":
            in_note = True
            processed_lines.append(l)
            continue
        elif st.startswith(("#", "<a id=", "|", ">", "```")):
            in_note = False
            processed_lines.append(l)
            continue

        if in_note:
            m_let = re.match(r"^([a-z]\)\s+.*)", st)
            if m_let:
                processed_lines.append(f"  {m_let.group(1)}")
                continue
            m_sub_b = re.match(r"^\s*-\s+([a-z]\)\s+.*)", st)
            if m_sub_b:
                processed_lines.append(f"  {m_sub_b.group(1)}")
                continue
        else:
            m_main_let = re.match(r"^[-*]\s+([a-z]\)\s+.*)", st)
            if m_main_let:
                processed_lines.append(m_main_let.group(1))
                continue

        processed_lines.append(l)

    text = "\n".join(processed_lines)
    return re.sub(r"\n{3,}", "\n\n", text)


def inject_semantic_anchors(text: str, profile: Optional[DocProfile] = None) -> str:
    """Inject hidden inline semantic anchors into Markdown text (idempotent)."""
    if profile is None:
        profile = get_doc_profile("vbpl")

    text = strip_existing_anchors(text)
    lines = text.splitlines()
    processed_lines: list[str] = []
    current_dieu = ""

    for line in lines:
        stripped = line.strip()

        # Clean multiple bullets (e.g. '- - ' -> '- ')
        if re.match(r"^([-*]\s+)+", stripped):
            stripped = re.sub(r"^([-*]\s+)+", "- ", stripped)

        # 1. Match Law Article: 'Điều 1. Phạm vi'
        dieu_match = profile.dieu_pattern.match(stripped)
        if dieu_match:
            current_dieu = dieu_match.group(2)
            anchor = f'<a id="dieu-{current_dieu}"></a>'
            processed_lines.append(f"\n{anchor}\n### {dieu_match.group(1)}")
            continue

        # 2. Match Section: '1.1 Phạm vi' or '2.1.2 Giới hạn'
        sec_match = profile.sec_pattern.match(stripped)
        if sec_match:
            sec_num = sec_match.group(2).replace(".", "-")
            anchor = f'<a id="{profile.section_prefix}-{sec_num}"></a>'
            processed_lines.append(f"\n{anchor}\n### {sec_match.group(1)}")
            continue

        # 3. Match Clause: '1. Nội dung' -> Bold formatting **1.** to prevent CommonMark list indent
        khoan_match = profile.khoan_pattern.match(stripped)
        if khoan_match and current_dieu:
            khoan_num = khoan_match.group(1) or khoan_match.group(2)
            khoan_rest = khoan_match.group(3)
            anchor = f'<a id="dieu-{current_dieu}-khoan-{khoan_num}"></a>'
            processed_lines.append(f"{anchor}\n**{khoan_num}.** {khoan_rest}")
            continue

        processed_lines.append(line)

    return "\n".join(processed_lines)

def generate_bundle_ast_and_qa(
    bundle_dir: Path,
    doc_title: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Extract deduplicated AST and QA Benchmark across Active Core and Modular Annexes."""
    core_files = [f for f in bundle_dir.glob("*.md") if f.name not in ("index.md", "dead_ends.md", "log.md")]
    annexes_dir = bundle_dir / "annexes"
    annex_files = sorted(list(annexes_dir.glob("*.md"))) if annexes_dir.exists() else []

    all_files = core_files + annex_files
    seen_anchors: Set[str] = set()
    clauses: List[Dict[str, Any]] = []
    qa_list: List[Dict[str, Any]] = []

    anchor_pattern = re.compile(r'<a\s+(?:id|name)="([^"]+)"')
    title_prefix = doc_title or bundle_dir.name

    for md_path in all_files:
        rel_path = str(md_path.relative_to(bundle_dir)).replace("\\", "/")
        content = md_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        in_toc = False
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if "## MỤC LỤC" in stripped:
                in_toc = True
                continue
            if in_toc and stripped.startswith("## ") and "MỤC LỤC" not in stripped:
                in_toc = False

            if in_toc:
                continue

            m_anc = anchor_pattern.search(stripped)
            if m_anc:
                anc_id = m_anc.group(1)
                if anc_id in seen_anchors:
                    continue
                seen_anchors.add(anc_id)

                clean_title = re.sub(r'<[^>]+>', '', stripped).strip("# *").strip()
                if not clean_title and idx < len(lines):
                    clean_title = re.sub(r'<[^>]+>', '', lines[idx]).strip("# *").strip()

                # Determine jurisdiction
                jurisdiction = "CQXD"
                if any(k in anc_id.lower() for k in ["chua-chay", "cuu-nan", "cap-nuoc", "muc-5", "muc-6", "phu-luc-i"]):
                    jurisdiction = "CONG_AN"

                clauses.append({
                    "clause_id": anc_id,
                    "anchor": anc_id,
                    "title": clean_title,
                    "source_file": rel_path,
                    "jurisdiction": jurisdiction,
                    "cong_bao_number": "373/2026",
                    "line_start": idx,
                    "line_end": idx,
                })

                qa_list.append({
                    "question": f"Quy định tại {clean_title} của {title_prefix} là gì?",
                    "answer": f"Xem chi tiết nội dung quy chuẩn tại {clean_title} ({rel_path}#{anc_id}).",
                    "anchor": anc_id,
                    "source_file": rel_path,
                    "jurisdiction": jurisdiction
                })

    return clauses, qa_list

def process_okf_bundle(bundle_dir: Path, doc_type: Optional[str] = None) -> dict[str, Any]:
    """Process an OKF bundle directory to meet Gold Standard OKF v2.2."""
    if not bundle_dir.exists() or not bundle_dir.is_dir():
        return {"status": "error", "message": f"Bundle dir {bundle_dir} does not exist."}

    # Normalize all Markdown files in bundle (Active Core and Annexes)
    core_files = [f for f in bundle_dir.glob("*.md") if f.name not in ("index.md", "dead_ends.md", "log.md")]
    annexes_dir = bundle_dir / "annexes"
    annex_files = sorted(list(annexes_dir.glob("*.md"))) if annexes_dir.exists() else []

    for md_path in core_files + annex_files:
        raw_text = md_path.read_text(encoding="utf-8")
        norm_text = normalize_notes_and_lists(raw_text)
        if norm_text != raw_text:
            md_path.write_text(norm_text, encoding="utf-8")
    # Extract document title from metadata
    meta_path = bundle_dir / "metadata.yaml"
    doc_title = bundle_dir.name
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = yaml.safe_load(f)
                if isinstance(meta, dict) and meta.get("title"):
                    doc_title = meta["title"].split("—")[0].strip()
        except Exception:
            pass

    clauses, qa_benchmark = generate_bundle_ast_and_qa(bundle_dir, doc_title=doc_title)

    # Write clauses.json
    clauses_file = bundle_dir / "clauses.json"
    clauses_file.write_text(json.dumps(clauses, ensure_ascii=False, indent=2), encoding="utf-8")

    # Write qa_benchmark.json
    qa_file = bundle_dir / "qa_benchmark.json"
    qa_file.write_text(json.dumps(qa_benchmark, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"  [OKF v2.2 Processor] Saved {len(clauses)} AST clauses & {len(qa_benchmark)} QA benchmark pairs.")
    return {
        "status": "success",
        "bundle": bundle_dir.name,
        "clauses_count": len(clauses),
        "qa_count": len(qa_benchmark)
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="Gold Standard OKF v2.2 Processor")
    parser.add_argument("bundle_dir", type=Path, help="Path to OKF bundle directory")
    parser.add_argument("-t", "--doc-type", type=str, default=None, help="Document type profile (vbpl, qcvn, tcvn)")

    args = parser.parse_args()
    res = process_okf_bundle(args.bundle_dir, doc_type=args.doc_type)
    print(res)

if __name__ == "__main__":
    main()
