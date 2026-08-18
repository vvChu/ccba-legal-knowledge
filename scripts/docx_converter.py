"""CCBA Master Skill: Markdown Document Processing Engine (Docx Converter).

Converts official .docx documents (QCVN 06:2022/BXD) to GFM Markdown with
clean 2D Pipe Tables, standardized section headings (### 1.1),
and full Gold Standard OKF v0.2 integration.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import mammoth
from scripts.gold_standard_processor import process_okf_bundle
from scripts.qcvn_md_table_formatter import format_all_qcvn_md_tables

sys.stdout.reconfigure(encoding="utf-8")


def normalize_docx_markdown(md_text: str) -> str:
    """Normalize mammoth converted markdown headings and clean up escape chars."""
    # Remove escaped dots, hyphens, and brackets
    md_text = md_text.replace(r"\.", ".").replace(r"\-", "-").replace(r"\(", "(").replace(r"\)", ")")

    # Replace bold Chapter and Article headings
    md_text = re.sub(r"__(Chương\s+[IVXLCDM0-9]+(?::\s*[^_]+)?)__", r"## \1", md_text)
    md_text = re.sub(r"__(Điều\s+\d+\.\s*[^_]+)__", r"### \1", md_text)
    
    # Replace bold Appendix headings (Appendices A through I and Roman numerals)
    md_text = re.sub(r"__(Phụ lục\s+[A-Za-z0-9]+(?:\s*\([^)]+\))?(?:\.\s*[^_]+)?)__", r"## \1", md_text, flags=re.IGNORECASE)
    md_text = re.sub(r"^#*\s*(PHỤ LỤC\s+[A-I]\b[^\n]*)", r"## \1", md_text, flags=re.MULTILINE | re.IGNORECASE)

    # Replace bold table headings __Bảng X - Title__ with ### Bảng X - Title
    md_text = re.sub(r"__Bảng\s+([A-Z0-9]+(?:\.[0-9]+)?)\s*[-–:]\s*([^_]+)__", r"### Bảng \1 - \2", md_text)

    # Replace bold section headings with hierarchical Markdown headings
    # 4-level: __1.1.1.1 Title__ -> ##### 1.1.1.1 Title
    md_text = re.sub(r"__((?:[1-7]|[A-I])\.\d+\.\d+\.\d+)\.?\s*([^_]+)__", r"##### \1 \2", md_text)
    # 3-level: __1.1.1 Title__ -> #### 1.1.1 Title
    md_text = re.sub(r"__((?:[1-7]|[A-I])\.\d+\.\d+)\.?\s*([^_]+)__", r"#### \1 \2", md_text)
    # 2-level: __1.1 Title__ -> ### 1.1 Title
    md_text = re.sub(r"__((?:[1-7]|[A-I])\.\d+)\.?\s*([^_]+)__", r"### \1 \2", md_text)

    # Clean double ### headers if any exist
    md_text = re.sub(r"(###\s*)+", "### ", md_text)
    md_text = re.sub(r"###\s*###\s*", "### ", md_text)

    return md_text


def convert_docx_to_okf_bundle(
    docx_path: Path,
    target_bundle_dir: Path,
    output_filename: Optional[str] = None,
    doc_type: Optional[str] = None,
) -> dict:
    """Convert .docx file to Gold Standard OKF Markdown bundle."""
    if not docx_path.exists():
        raise FileNotFoundError(f"Input file not found: {docx_path}")

    target_bundle_dir.mkdir(parents=True, exist_ok=True)
    if not output_filename:
        output_filename = f"{target_bundle_dir.name}.md"

    target_md_path = target_bundle_dir / output_filename

    print(f"[1/4] Converting {docx_path.name} to Markdown via Mammoth Engine...")
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
        raw_md = result.value

    print("[2/4] Normalizing section headings & typography (Sub-skill: vn-legal-normalizer)...")
    normalized_md = normalize_docx_markdown(raw_md)

    # Backup converted md to Layer 1 store
    raw_md_store = docx_path.parent / f"{docx_path.stem}_from_docx.md"
    raw_md_store.write_text(normalized_md, encoding="utf-8")
    print(f"  [Saved] Layer 1 Raw Docx Markdown: {raw_md_store} ({len(normalized_md)} bytes)")

    # Write normalized markdown to target bundle
    target_md_path.write_text(normalized_md, encoding="utf-8")

    print("[3/4] Reconstructing 2D GFM Pipe Tables (Sub-skill: table-reconstructor)...")
    formatted_tables = format_all_qcvn_md_tables(target_md_path)
    print(f"  [Table Reconstructor] Formatted {formatted_tables} 2D GFM Pipe Tables")

    print("[4/4] Packing Gold Standard OKF v0.2 Bundle...")
    bundle_result = process_okf_bundle(target_bundle_dir, doc_type=doc_type)
    return bundle_result


def main() -> None:
    """CLI entrypoint for Docx Converter Engine."""
    parser = argparse.ArgumentParser(description="Convert official .docx document to OKF v0.2 Markdown bundle.")
    parser.add_argument("docx_path", type=Path, help="Path to input .docx file")
    parser.add_argument("target_bundle_dir", type=Path, help="Path to target OKF bundle directory")
    parser.add_argument("-o", "--output-filename", type=str, default=None, help="Custom output markdown filename")
    parser.add_argument("-t", "--doc-type", type=str, default=None, help="Document type profile (e.g. vbpl, qcvn, tcvn)")

    args = parser.parse_args()
    res = convert_docx_to_okf_bundle(
        docx_path=args.docx_path,
        target_bundle_dir=args.target_bundle_dir,
        output_filename=args.output_filename,
        doc_type=args.doc_type,
    )
    print("\n[COMPLETE OKF BUNDLE RESULT]:", res)


if __name__ == "__main__":
    main()

