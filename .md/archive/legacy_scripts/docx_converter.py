"""CCBA Master Legal Converter Engine (OKF v2.2 Universal Gateway).

Converts official .docx documents (QCVN / TCVN / VBPL / Nghị định / Luật / Thông tư)
into Gold Standard OKF v2.2 Markdown bundles with:
- Pure Normative Body (.md)
- Structured Legal Knowledge Graph (legal_basis in metadata.yaml)
- Atomic Form Templates (templates/phu_luc_XX/mau_YY_...md)
- 3-Tier Semantic Table Classifier (tables/csv and tables/json)
- Universal Clause Numbering Normalization (**1.**, **2.**)
- Atomic AST (clauses.json) & QA Benchmark (qa_benchmark.json)
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Ensure repository root is on sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

sys.stdout.reconfigure(encoding="utf-8")

import yaml
import mammoth
from scripts.okf_v22_converter import process_vbpl_bundle_okf_v22
from scripts.gold_standard_processor import process_okf_bundle


def format_all_qcvn_md_tables(md_path: Path) -> int:
    """Scan and convert all multiline/broken table blocks in md_path to 2D GFM Pipe Tables."""
    if not md_path.exists():
        return 0

    content = md_path.read_text(encoding="utf-8")
    table_block_regex = re.compile(
        r"(<a id=\"[^\"]+\"></a>\n)?([#*]+)?\s*(Bảng\s+([A-Z0-9]+(?:\.[0-9]+)?)\s*[-–:]\s*([^\n\*\#]+))([#*]*|\n)?"
        r"(.*?)(?=\n<a id=\"|\n#{1,6}\s+|\n(?:\#|\*)*\s*Bảng|\Z)",
        re.DOTALL | re.IGNORECASE,
    )

    formatted_count = 0

    def replace_table_block(match: re.Match) -> str:
        nonlocal formatted_count
        full_match_text = match.group(0)
        table_num = match.group(4)
        table_title_text = match.group(5).strip("*\n# ")
        table_title = f"Bảng {table_num} - {table_title_text}"
        table_anchor = f"bang-{table_num.lower().replace('.', '-')}"
        body_text = match.group(7)

        raw_lines = body_text.splitlines()
        clean_tokens: list[str] = []
        footnotes: list[str] = []

        for line in raw_lines:
            line_str = line.strip()
            clean_str = re.sub(r"<a id=\"[^\"]+\"></a>", "", line_str)
            clean_str = re.sub(r"^[#*\s|]+", "", clean_str).strip(" |")

            if not clean_str or clean_str == "---":
                continue

            if re.match(r"^\d+\)\s+", clean_str) or clean_str.startswith("CHÚ THÍCH"):
                footnotes.append(clean_str)
                continue

            if "\t" in clean_str:
                parts = [p.strip(" |") for p in clean_str.split("\t") if p.strip()]
                clean_tokens.extend(parts)
            else:
                clean_tokens.append(clean_str)

        if len(clean_tokens) < 2:
            return full_match_text

        header_end = 1
        for tok_idx, tok in enumerate(clean_tokens[1:], 1):
            if re.match(r"^\d+[\.\)]?\s*", tok) or re.search(r"\b(REI|EI|R|E|P|F\d)\s*\d*", tok):
                header_end = tok_idx
                break

        cols_count = max(1, header_end)
        header_row = clean_tokens[:cols_count]
        data_tokens = clean_tokens[cols_count:]

        data_rows: list[list[str]] = []
        for chunk_idx in range(0, len(data_tokens), cols_count):
            chunk = data_tokens[chunk_idx : chunk_idx + cols_count]
            if any(chunk):
                if len(chunk) < cols_count:
                    chunk.extend([""] * (cols_count - len(chunk)))
                data_rows.append(chunk)

        if not data_rows:
            return full_match_text

        md_lines = [
            f'<a id="{table_anchor}"></a>',
            f"### {table_title}\n",
            "| " + " | ".join(header_row) + " |",
            "| " + " | ".join(["---"] * cols_count) + " |",
        ]
        for row in data_rows:
            md_lines.append("| " + " | ".join(row) + " |")

        if footnotes:
            md_lines.append("\n" + "\n".join(f"_{fn}_" for fn in footnotes))

        md_lines.append("\n")
        formatted_count += 1
        return "\n".join(md_lines)

    new_content = table_block_regex.sub(replace_table_block, content)
    md_path.write_text(new_content, encoding="utf-8")
    return formatted_count


def normalize_docx_markdown(md_text: str) -> str:
    """Normalize mammoth converted markdown headings and clean up escape chars."""
    md_text = md_text.replace(r"\.", ".").replace(r"\-", "-").replace(r"\(", "(").replace(r"\)", ")")

    md_text = re.sub(r"__(Chương\s+[IVXLCDM0-9]+(?::\s*[^_]+)?)__", r"## \1", md_text)
    md_text = re.sub(r"__(Điều\s+\d+\.\s*[^_]+)__", r"### \1", md_text)
    
    md_text = re.sub(r"__(Phụ lục\s+[A-Za-z0-9]+(?:\s*\([^)]+\))?(?:\.\s*[^_]+)?)__", r"## \1", md_text, flags=re.IGNORECASE)
    md_text = re.sub(r"^#*\s*(PHỤ LỤC\s+[A-I]\b[^\n]*)", r"## \1", md_text, flags=re.MULTILINE | re.IGNORECASE)

    md_text = re.sub(r"__Bảng\s+([A-Z0-9]+(?:\.[0-9]+)?)\s*[-–:]\s*([^_]+)__", r"### Bảng \1 - \2", md_text)

    md_text = re.sub(r"__((?:[1-7]|[A-I])\.\d+\.\d+\.\d+)\.?\s*([^_]+)__", r"##### \1 \2", md_text)
    md_text = re.sub(r"__((?:[1-7]|[A-I])\.\d+\.\d+)\.?\s*([^_]+)__", r"#### \1 \2", md_text)
    md_text = re.sub(r"__((?:[1-7]|[A-I])\.\d+)\.?\s*([^_]+)__", r"### \1 \2", md_text)

    md_text = re.sub(r"(###\s*)+", "### ", md_text)
    md_text = re.sub(r"###\s*###\s*", "### ", md_text)

    return md_text


def detect_document_pipeline(
    target_bundle_dir: Path,
    doc_type: Optional[str] = None,
    registry_file: Optional[Path] = None
) -> str:
    """Determine whether to use VBPL (OKF v2.2) or QCVN pipeline."""
    if doc_type:
        dt = doc_type.lower()
        if "qcvn" in dt or "tcvn" in dt or "standard" in dt:
            return "qcvn"
        return "vbpl"

    # Check path heuristic
    path_str = str(target_bundle_dir).lower()
    if "01_vbpl" in path_str:
        return "vbpl"
    if "02_qcvn" in path_str or "03_tcvn" in path_str:
        return "qcvn"

    # Check registry metadata
    reg_path = registry_file or (Path(__file__).resolve().parent.parent / "legal_registry.yaml")
    if reg_path.exists():
        with open(reg_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            all_items = []
            for k, v in data.items():
                if isinstance(v, list):
                    all_items.extend(v)
            for item in all_items:
                if item.get("id") == target_bundle_dir.name or item.get("bundle_path", "").rstrip("/\\").endswith(target_bundle_dir.name):
                    t = item.get("type", "").lower()
                    if "quy chuẩn" in t or "tiêu chuẩn" in t:
                        return "qcvn"
                    return "vbpl"

    return "vbpl"


def convert_docx_to_okf_bundle(
    docx_path: Path,
    target_bundle_dir: Path,
    output_filename: Optional[str] = None,
    doc_type: Optional[str] = None,
    registry_file: Optional[Path] = None
) -> Dict[str, Any]:
    """Convert .docx file to Gold Standard OKF v2.2 Markdown bundle."""
    if not docx_path.exists():
        raise FileNotFoundError(f"Input file not found: {docx_path}")

    target_bundle_dir.mkdir(parents=True, exist_ok=True)
    reg_file = registry_file or (Path(__file__).resolve().parent.parent / "legal_registry.yaml")

    pipeline_type = detect_document_pipeline(target_bundle_dir, doc_type, reg_file)
    print(f"-> Selected Pipeline: [{pipeline_type.upper()}] for target: {target_bundle_dir.name}")

    if pipeline_type == "vbpl":
        # Pure Normative Body & Atomic Templates OKF v2.2
        return process_vbpl_bundle_okf_v22(
            docx_path=docx_path,
            bundle_dir=target_bundle_dir,
            registry_file=reg_file,
            output_filename=output_filename
        )
    else:
        # QCVN / TCVN 2D Table Pipeline
        if not output_filename:
            output_filename = f"{target_bundle_dir.name}.md"

        target_md_path = target_bundle_dir / output_filename

        print(f"[1/4] Converting {docx_path.name} via Mammoth Engine...")
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_markdown(docx_file)
            raw_md = result.value

        print("[2/4] Normalizing section headings & typography...")
        normalized_md = normalize_docx_markdown(raw_md)

        raw_md_store = docx_path.parent / f"{docx_path.stem}_from_docx.md"
        raw_md_store.write_text(normalized_md, encoding="utf-8")

        target_md_path.write_text(normalized_md, encoding="utf-8")

        print("[3/4] Reconstructing 2D GFM Pipe Tables...")
        formatted_tables = format_all_qcvn_md_tables(target_md_path)
        print(f"  [Table Reconstructor] Formatted {formatted_tables} 2D GFM Pipe Tables")

        print("[4/4] Packing Gold Standard OKF Bundle...")
        return process_okf_bundle(target_bundle_dir, doc_type=doc_type)


def main() -> None:
    """CLI entrypoint for Universal Legal Docx Converter Engine."""
    parser = argparse.ArgumentParser(description="Universal Legal Docx Converter Engine (OKF v2.2)")
    parser.add_argument("docx_path", type=Path, help="Path to input .docx file")
    parser.add_argument("target_bundle_dir", type=Path, help="Path to target OKF bundle directory")
    parser.add_argument("-o", "--output-filename", type=str, default=None, help="Custom output markdown filename")
    parser.add_argument("-t", "--doc-type", type=str, default=None, help="Document type profile (vbpl, qcvn, tcvn)")
    parser.add_argument("-r", "--registry", type=Path, default=None, help="Path to legal_registry.yaml")

    args = parser.parse_args()
    res = convert_docx_to_okf_bundle(
        docx_path=args.docx_path,
        target_bundle_dir=args.target_bundle_dir,
        output_filename=args.output_filename,
        doc_type=args.doc_type,
        registry_file=args.registry
    )
    print("\n[OKF v2.2 TRANSFORMATION RESULT]:", res)


if __name__ == "__main__":
    main()
