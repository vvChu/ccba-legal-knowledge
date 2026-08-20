"""OKF v0.2 Gold Standard Data Processing Engine.

Performs:
1. TVPL HTML & Line Normalization (Joining split lines like Điều\\n1).
2. HTML-to-Pure-Markdown Table Conversion.
3. Config-driven Inline Semantic Anchor Injection (<a id="dieu-XX-khoan-YY"></a> & <a id="muc-1-1"></a>).
4. Structural AST Parsing (clauses.json).
5. Technical Table CSV & Formula Extraction (tables/*.csv).
6. Ground Truth QA Benchmark Generation (qa_benchmark.json).
"""

import argparse
import json
import re
import sys
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
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
    return re.sub(r'<a id="[^"]+"></a>\s*', '', text)

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

def generate_clauses_ast(text: str) -> list[dict[str, Any]]:
    """Parse text into structural AST clause indexing."""
    lines = text.splitlines()
    clauses: list[dict[str, Any]] = []

    anchor_pattern = re.compile(r'<a id="([^"]+)"></a>')

    for idx, line in enumerate(lines, 1):
        anchor_match = anchor_pattern.search(line)
        if anchor_match:
            anchor_id = anchor_match.group(1)
            title = line
            if idx < len(lines):
                title = lines[idx]

            clauses.append({
                "clause_id": anchor_id,
                "anchor": anchor_id,
                "title": title.strip("# *").strip(),
                "line_start": idx,
                "line_end": idx,
            })

    return clauses

def extract_tables_and_formulas(bundle_dir: Path, text: str) -> list[Path]:
    """Extract tables into CSV files inside bundle_dir/tables."""
    tables_dir = bundle_dir / "tables"
    tables_dir.mkdir(exist_ok=True)
    extracted_files: list[Path] = []

    table_pattern = re.compile(r"(\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n?)+)")
    matches = table_pattern.findall(text)

    for idx, table_str in enumerate(matches, 1):
        csv_file = tables_dir / f"table_{idx}.csv"
        rows = [r.strip() for r in table_str.strip().splitlines() if r.strip()]
        clean_rows = []
        for r in rows:
            if re.match(r"^\|[\s:-|]+\|$", r):
                continue
            cells = [cell.strip() for cell in r.strip("|").split("|")]
            clean_rows.append(",".join(f'"{c}"' for c in cells))

        csv_file.write_text("\n".join(clean_rows), encoding="utf-8")
        extracted_files.append(csv_file)

    return extracted_files

def generate_qa_benchmark(text: str, metadata: dict[str, Any], profile: Optional[DocProfile] = None) -> list[dict[str, Any]]:
    """Generate ground truth Q&A pairs for RAG evaluation."""
    if profile is None:
        profile = get_doc_profile("vbpl")

    qa_list: list[dict[str, Any]] = []
    lines = text.splitlines()

    for line in lines:
        stripped = line.strip()
        match_dieu = profile.dieu_pattern.match(stripped)
        if match_dieu:
            dieu_num = match_dieu.group(2)
            # Extracted title line if present
            dieu_title = match_dieu.group(1)
            qa_list.append(
                {
                    "question": f"Điều {dieu_num} quy định về nội dung gì?",
                    "answer": f"Chi tiết tại {dieu_title}.",
                    "anchor": f"dieu-{dieu_num}",
                }
            )
            continue

        match_sec = profile.sec_pattern.match(stripped)
        if match_sec:
            sec_num = match_sec.group(2)
            sec_title = match_sec.group(1)
            qa_list.append(
                {
                    "question": f"Mục {sec_num} quy định về nội dung gì?",
                    "answer": f"Chi tiết tại {sec_title}.",
                    "anchor": f"{profile.section_prefix}-{sec_num.replace('.', '-')}",
                }
            )

    return qa_list

try:
    from scripts.table_extractor import parse_and_extract_all_tables
except ImportError:
    from table_extractor import parse_and_extract_all_tables

def detect_doc_type_from_bundle(bundle_dir: Path) -> str:
    """Infer doc_type from metadata.yaml or directory path."""
    meta_path = bundle_dir / "metadata.yaml"
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = yaml.safe_load(f)
                if isinstance(meta, dict) and meta.get("doc_type"):
                    return str(meta["doc_type"])
        except Exception:
            pass

    parent_dir_name = bundle_dir.parent.name.lower()
    if "qcvn" in parent_dir_name or "02_qcvn" in parent_dir_name:
        return "qcvn"
    if "tcvn" in parent_dir_name or "03_tcvn" in parent_dir_name:
        return "tcvn"
    return "vbpl"

def process_okf_bundle(bundle_dir: Path, doc_type: Optional[str] = None) -> dict[str, Any]:
    """Process an OKF bundle directory to meet Gold Standard OKF v0.2."""
    if not bundle_dir.exists() or not bundle_dir.is_dir():
        return {"status": "error", "message": f"Bundle dir {bundle_dir} does not exist."}

    md_files = [f for f in bundle_dir.glob("*.md") if f.name not in ("index.md", "dead_ends.md", "log.md")]
    if not md_files:
        return {"status": "error", "message": "No primary markdown file found in bundle."}

    if doc_type is None:
        doc_type = detect_doc_type_from_bundle(bundle_dir)

    profile = get_doc_profile(doc_type)
    primary_md = md_files[0]
    raw_content = primary_md.read_text(encoding="utf-8")

    # Step 1: Normalize TVPL line wrapping
    norm_content = normalize_tvpl_formatting(raw_content)

    # Step 2: Extract HTML, Markdown Pipe, and Text tables to structured JSON & CSV
    table_md, tables = parse_and_extract_all_tables(bundle_dir, norm_content)

    # Step 3: Inject Semantic Anchors (idempotent)
    anchored_content = inject_semantic_anchors(table_md, profile)

    # Write back clean anchored content
    primary_md.write_text(anchored_content, encoding="utf-8")

    # Step 4: AST Clauses
    clauses = generate_clauses_ast(anchored_content)
    (bundle_dir / "clauses.json").write_text(
        json.dumps(clauses, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Step 5: QA Benchmark
    qa_benchmark = generate_qa_benchmark(anchored_content, {}, profile)
    (bundle_dir / "qa_benchmark.json").write_text(
        json.dumps(qa_benchmark, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return {
        "status": "success",
        "bundle_dir": str(bundle_dir),
        "doc_type": profile.name,
        "clauses_count": len(clauses),
        "tables_count": len(tables),
        "qa_count": len(qa_benchmark),
    }

def main() -> None:
    """CLI entrypoint for Gold Standard Processor Engine."""
    parser = argparse.ArgumentParser(description="CCBA OKF Gold Standard Data Processing Engine.")
    parser.add_argument("bundle_dir", type=str, help="Path to OKF bundle directory")
    parser.add_argument("--type", type=str, default=None, choices=["vbpl", "qcvn", "tcvn"], help="Document type profile")

    args = parser.parse_args()
    target_dir = Path(args.bundle_dir).resolve()
    result = process_okf_bundle(target_dir, args.type)

    if result.get("status") == "success":
        print(f"✅ SUCCESS: Processed bundle '{result['bundle_dir']}' (Profile: {result['doc_type']})")
        print(f"   -> Clauses AST : {result['clauses_count']}")
        print(f"   -> Tables      : {result['tables_count']}")
        print(f"   -> QA Bench    : {result['qa_count']}")
        sys.exit(0)
    else:
        print(f"❌ ERROR: {result.get('message')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
