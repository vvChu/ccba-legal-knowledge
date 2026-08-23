"""OKF v2.2 Gold Standard Data Processing Engine for Technical Standards & Decrees.

Thin Spoke wrapper delegating to Hub SDK `ccba_legal.gold_standard` while providing
backward-compatible utility functions for tests and local CLI.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from ccba_legal.gold_standard import (
    DocProfile,
    GoldStandardProcessor,
    clean_html_tables,
    clean_table_footnotes_and_superscripts,
    generate_bundle_ast_and_qa,
    get_doc_profile,
    inject_semantic_anchors,
    normalize_notes_and_lists,
    normalize_tvpl_formatting,
    strip_existing_anchors,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def generate_clauses_ast(
    text: str, profile: DocProfile | None = None
) -> list[dict[str, Any]]:
    """Parse text lines into structured clause AST items."""
    prof = profile or get_doc_profile("vbpl")
    clauses: list[dict[str, Any]] = []
    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        m = prof.dieu_pattern.match(line.strip())
        if m:
            dieu_title = m.group(1).strip()
            dieu_num = m.group(2)
            anc_id = f"dieu-{dieu_num}"
            clauses.append(
                {
                    "title": dieu_title,
                    "anchor": anc_id,
                    "level": 1,
                    "line_start": idx,
                    "line_end": idx,
                }
            )
        else:
            sm = prof.sec_pattern.match(line.strip())
            if sm and not line.strip().lower().startswith("điều"):
                sec_title = sm.group(1).strip()
                sec_code = sm.group(2).strip().lower().replace(".", "-")
                anc_id = f"{prof.section_prefix}-{sec_code}"
                clauses.append(
                    {
                        "title": sec_title,
                        "anchor": anc_id,
                        "level": 1,
                        "line_start": idx,
                        "line_end": idx,
                    }
                )
    return clauses


def extract_tables_and_formulas(text: str) -> list[dict[str, Any]]:
    """Extract table matrices and formulas placeholder for backward compatibility."""
    return []


def process_okf_bundle(bundle_dir: Path | str, doc_type: str | None = None) -> dict[str, Any]:
    """Compatibility function calling Hub GoldStandardProcessor.process_bundle."""
    return GoldStandardProcessor.process_bundle(Path(bundle_dir), doc_type=doc_type)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="OKF v2.2 Gold Standard Processing Pipeline (Hub SDK Engine)"
    )
    parser.add_argument("bundle_dir", help="Path to OKF bundle directory")
    parser.add_argument(
        "--type", "-t", default=None, help="Document type (e.g. 'qcvn', 'vbpl', 'decree')"
    )
    args = parser.parse_args()

    target = Path(args.bundle_dir)
    result = process_okf_bundle(target, doc_type=args.type)
    print(f"Result: {result}")
    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
