"""CCBA Modernize Annex Engine — Thin CLI Wrapper delegating to ccba_legal.modernize (OKF v2.3 / ADR 0034).

Usage:
    python scripts/modernize_annex_engine.py composite-figures --images a.png b.png --output hinh_1.png --labels a) b)
    python scripts/modernize_annex_engine.py build-matrix-tables --input data.csv --output table.md
    python scripts/modernize_annex_engine.py convert-math --input file.md --output file_clean.md
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from ccba_legal.modernize import (
    FigureAutoCompositor,
    MathEquationConverter,
    TableMatrixBuilder,
)

# Enforce UTF-8 output encoding for Windows PowerShell
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    """CLI Dispatcher for Modernize Annex Engine."""
    parser = argparse.ArgumentParser(description="CCBA Modernize Annex Engine (OKF v2.3)")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Command 1: composite-figures
    p_comp = subparsers.add_parser("composite-figures", help="Composite multiple panel images into one")
    p_comp.add_argument("--images", nargs="+", required=True, help="List of panel image file paths")
    p_comp.add_argument("--output", "-o", required=True, help="Output composite PNG path")
    p_comp.add_argument("--layout", choices=["vertical", "horizontal", "grid"], default="vertical")
    p_comp.add_argument("--labels", nargs="*", default=None, help="Panel labels like a) b) c)")

    # Command 2: build-matrix-tables
    p_tab = subparsers.add_parser("build-matrix-tables", help="Build GFM table from CSV")
    p_tab.add_argument("--input", "-i", required=True, help="Input CSV path")
    p_tab.add_argument("--output", "-o", default=None, help="Output MD path (prints to stdout if omitted)")
    p_tab.add_argument("--caption", default="", help="Table caption title")
    p_tab.add_argument("--number", default="", help="Table number (e.g. Bảng F.1)")

    # Command 3: convert-math
    p_math = subparsers.add_parser("convert-math", help="Convert numbered equations to KaTeX")
    p_math.add_argument("--input", "-i", required=True, help="Input MD file path")
    p_math.add_argument("--output", "-o", default=None, help="Output MD file path")

    args = parser.parse_args()

    if args.command == "composite-figures":
        out = FigureAutoCompositor.composite_panels(
            image_paths=args.images,
            output_path=args.output,
            layout=args.layout,
            panel_labels=args.labels,
        )
        print(f"✅ Composite image created at: {out}")
        return 0

    elif args.command == "build-matrix-tables":
        in_p = Path(args.input)
        if not in_p.exists():
            print(f"❌ Input CSV not found: {in_p}")
            return 1
        with open(in_p, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        md_tab = TableMatrixBuilder.format_lossless_matrix_table(
            raw_rows=rows,
            caption=args.caption,
            table_num=args.number,
        )
        if args.output:
            Path(args.output).write_text(md_tab, encoding="utf-8")
            print(f"✅ Table markdown saved to: {args.output}")
        else:
            print(md_tab)
        return 0

    elif args.command == "convert-math":
        in_p = Path(args.input)
        if not in_p.exists():
            print(f"❌ Input markdown not found: {in_p}")
            return 1
        content = in_p.read_text(encoding="utf-8")
        clean_md = MathEquationConverter.convert_numbered_equations(content)
        out_p = Path(args.output) if args.output else in_p
        out_p.write_text(clean_md, encoding="utf-8")
        print(f"✅ Converted equations in: {out_p}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
