"""CCBA Modernize Annex Engine — Auto-Compositor, Table Matrix Builder & Math Converter (OKF v2.3 / ADR 0034).

Provides CLI and API for:
1. Composite Figures: Merging multi-panel sub-figures into a unified centered white-RGB composite image.
2. Lossless Table Matrices: Building multi-column Markdown tables with dual-value formatting and separated footnotes.
3. Math Equation Conversion: Converting numbered equations to pure KaTeX blocks with \\tag{X.Y}.

Usage:
    python scripts/modernize_annex_engine.py composite-figures --images a.png b.png --output hinh_1.png --labels a) b)
    python scripts/modernize_annex_engine.py build-matrix-tables --input data.csv --output table.md
    python scripts/modernize_annex_engine.py convert-math --input file.md --output file_clean.md
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Any, Sequence

# Enforce UTF-8 output encoding for Windows PowerShell
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class FigureAutoCompositor:
    """Composites multiple sub-panels/diagrams into a unified high-resolution image."""

    @staticmethod
    def composite_panels(
        image_paths: Sequence[Path | str],
        output_path: Path | str,
        layout: str = "vertical",
        panel_labels: Sequence[str] | None = None,
        padding: int = 20,
        bg_color: tuple[int, int, int] = (255, 255, 255),
    ) -> Path:
        """Combines images vertically, horizontally, or as a grid on a white RGB canvas."""
        from PIL import Image, ImageDraw, ImageFont

        resolved_paths = [Path(p) for p in image_paths]
        for p in resolved_paths:
            if not p.exists():
                raise FileNotFoundError(f"Source panel image not found: {p}")

        images = [Image.open(p).convert("RGB") for p in resolved_paths]
        if not images:
            raise ValueError("No images provided for compositing.")

        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)

        if layout == "horizontal":
            total_width = sum(img.width for img in images) + padding * (len(images) + 1)
            max_height = max(img.height for img in images) + padding * 2
            composite = Image.new("RGB", (total_width, max_height), color=bg_color)
            draw = ImageDraw.Draw(composite)

            curr_x = padding
            for idx, img in enumerate(images):
                y_pos = padding + (max_height - padding * 2 - img.height) // 2
                composite.paste(img, (curr_x, y_pos))
                if panel_labels and idx < len(panel_labels):
                    label = panel_labels[idx]
                    draw.text((curr_x + 5, y_pos - 15 if y_pos >= 15 else y_pos + 5), label, fill=(0, 0, 0))
                curr_x += img.width + padding

        elif layout == "grid" and len(images) >= 4:
            # 2x2 Grid
            col1_w = max(images[0].width, images[2].width)
            col2_w = max(images[1].width, images[3].width if len(images) > 3 else 0)
            row1_h = max(images[0].height, images[1].height)
            row2_h = max(images[2].height, images[3].height if len(images) > 3 else 0)

            total_width = col1_w + col2_w + padding * 3
            total_height = row1_h + row2_h + padding * 3
            composite = Image.new("RGB", (total_width, total_height), color=bg_color)
            draw = ImageDraw.Draw(composite)

            coords = [
                (padding, padding),
                (padding * 2 + col1_w, padding),
                (padding, padding * 2 + row1_h),
                (padding * 2 + col1_w, padding * 2 + row1_h),
            ]
            for idx, img in enumerate(images[:4]):
                pos = coords[idx]
                composite.paste(img, pos)
                if panel_labels and idx < len(panel_labels):
                    draw.text((pos[0] + 5, pos[1] + 5), panel_labels[idx], fill=(0, 0, 0))
        else:
            # Vertical layout (default)
            max_width = max(img.width for img in images) + padding * 2
            label_extra = 25 if panel_labels else 0
            total_height = sum(img.height + label_extra for img in images) + padding * (len(images) + 1)
            composite = Image.new("RGB", (max_width, total_height), color=bg_color)
            draw = ImageDraw.Draw(composite)

            curr_y = padding
            for idx, img in enumerate(images):
                x_pos = padding + (max_width - padding * 2 - img.width) // 2
                if panel_labels and idx < len(panel_labels):
                    label = panel_labels[idx]
                    draw.text((x_pos, curr_y), label, fill=(0, 0, 0))
                    curr_y += label_extra
                composite.paste(img, (x_pos, curr_y))
                curr_y += img.height + padding

        composite.save(out_file, format="PNG", quality=95)
        return out_file


class TableMatrixBuilder:
    """Constructs lossless multi-tier Markdown tables with separated footnotes."""

    @staticmethod
    def format_dual_value(cell_text: str) -> str:
        """Formats dual suction/pressure values (e.g. -1.7 / +0.2) with <br> tag."""
        text = cell_text.strip()
        # Pattern: -1.7 / +0.0 or -1,7 ; +0,0 or -1.7 +0.0
        m = re.match(r"^([-\+−]\s*\d+[\.,]?\d*)\s*(?:[/;]|\s+)\s*([-\+−]\s*\d+[\.,]?\d*)$", text)
        if m:
            v1 = m.group(1).replace("−", "-").replace(" ", "")
            v2 = m.group(2).replace("−", "-").replace(" ", "")
            # Ensure proper sign formatting
            return f"{v1}<br>{v2}"
        return text

    @classmethod
    def format_lossless_matrix_table(
        cls,
        raw_rows: list[list[str]],
        caption: str = "",
        table_num: str = "",
        footnotes: list[str] | None = None,
    ) -> str:
        """Generates a clean GFM pipe table with 100% column preservation."""
        if not raw_rows:
            return ""

        extracted_notes: list[str] = list(footnotes or [])
        clean_grid: list[list[str]] = []

        for row in raw_rows:
            clean_row = [cls.format_dual_value(str(cell).strip()) for cell in row]
            if not clean_row or not any(clean_row):
                continue

            first_val = clean_row[0]
            # Check for footnote row embedded in table
            if re.match(r"^(?:\*\*)?(?:CHÚ\s+THÍCH|GHI\s+CHÚ|Chú\s+thích|Ghi\s+chú)", first_val, re.IGNORECASE):
                note_text = " ".join([c for c in clean_row if c.strip()])
                note_clean = re.sub(
                    r"^(?:\*\*)?(?:CHÚ\s+THÍCH|GHI\s+CHÚ|Chú\s+thích|Ghi\s+chú)\s*(?:\d+)?\s*[:–-]\s*(?:\*\*)?",
                    "",
                    note_text,
                    flags=re.IGNORECASE,
                ).strip()
                extracted_notes.append(note_clean)
                continue

            clean_grid.append(clean_row)

        if not clean_grid:
            return ""

        max_cols = max(len(r) for r in clean_grid)
        padded_grid = [r + [""] * (max_cols - len(r)) for r in clean_grid]

        alignments: list[str] = []
        for c_idx in range(max_cols):
            vals = [r[c_idx] for r in padded_grid[1:] if r[c_idx].strip()]
            is_num = all(re.match(r"^[0-9\.,\-\+\s%±<br>]+$", v) for v in vals) if vals else False
            alignments.append(":---:" if is_num else ":---")

        table_lines: list[str] = []
        if caption or table_num:
            tag = f"**{table_num} — {caption}**" if table_num and caption else f"**{table_num or caption}**"
            table_lines.append(tag + "\n")

        table_lines.append("| " + " | ".join(padded_grid[0]) + " |")
        table_lines.append("| " + " | ".join(alignments) + " |")
        for r in padded_grid[1:]:
            table_lines.append("| " + " | ".join(r) + " |")

        result = "\n".join(table_lines) + "\n\n"

        if extracted_notes:
            result += "_CHÚ THÍCH:_\n\n"
            if len(extracted_notes) == 1:
                result += f"{extracted_notes[0]}\n\n"
            else:
                for idx, note in enumerate(extracted_notes, 1):
                    result += f"{idx}) {note}\n"
                result += "\n"

        return result


class MathEquationConverter:
    """Converts raw formula text and equation numbers into standardized KaTeX blocks."""

    @staticmethod
    def convert_numbered_equations(markdown_text: str) -> str:
        """Finds standalone formulas with equation numbers and wraps in $$ ... \tag{...} $$."""
        lines = markdown_text.splitlines()
        converted_lines: list[str] = []

        for line in lines:
            stripped = line.strip()
            # Match pattern: Formula text ... (F.1) or (10.2) or (E.4)
            m = re.match(r"^(.+?)\s+\(([A-H0-9]+\.[0-9]+|[0-9]+)\)$", stripped)
            if m and not stripped.startswith(("#", "|", ">", "$$")) and "=" in stripped:
                eq_body = m.group(1).strip().strip("$")
                eq_tag = m.group(2).strip()
                # Format as clean block KaTeX
                converted_lines.append(f"$$\n{eq_body} \\tag{{{eq_tag}}}\n$$\n")
            else:
                converted_lines.append(line)

        return "\n".join(converted_lines)


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
