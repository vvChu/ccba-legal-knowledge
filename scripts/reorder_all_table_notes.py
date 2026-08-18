"""CCBA Table Footnotes & Multi-tier Header Polisher.

Formats all table footnotes into clean, readable bulleted blocks:
- Splits concatenated 'CHÚ THÍCH 1..N' into individual bullet lines.
- Cleans up trailing underscores and artifacts.
- Ensures clean paragraph spacing before and after footnotes.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"


def format_table_notes_in_text(text: str) -> str:
    lines = text.splitlines()
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check if line is a footnote line
        if stripped.startswith("_CHÚ THÍCH") or stripped.startswith("CHÚ THÍCH") or stripped.startswith("_Chú thích"):
            # Clean raw text
            raw = stripped.strip(" _\t")
            # Split multiple footnotes: CHÚ THÍCH 1:, CHÚ THÍCH 2: or 1), 2)
            # Match pattern like: CHÚ THÍCH 1:, CHÚ THÍCH 2:, or CHÚ THÍCH:
            parts = re.split(r"(?=(?:CHÚ THÍCH\s*\d*\s*:|(?<=[.;])\s*(?:CHÚ THÍCH|\d+\))))", raw, flags=re.IGNORECASE)
            
            cleaned_parts = []
            for p in parts:
                p_str = p.strip(" _\t\r\n")
                if not p_str:
                    continue
                # Normalize prefix
                p_str = re.sub(r"^(?:_)?(CHÚ THÍCH\s*\d*)\s*:\s*", r"**\1:** ", p_str, flags=re.IGNORECASE)
                cleaned_parts.append(p_str)

            if len(cleaned_parts) > 1 or any(p.startswith("**CHÚ THÍCH") for p in cleaned_parts):
                new_lines.append("")
                new_lines.append("_CHÚ THÍCH:_")
                for cp in cleaned_parts:
                    # Remove redundant CHÚ THÍCH: header if already at root
                    if cp.strip() == "_CHÚ THÍCH:_" or cp.strip() == "**CHÚ THÍCH:**":
                        continue
                    if not cp.startswith("- "):
                        cp = "- " + cp
                    new_lines.append(cp)
                new_lines.append("")
            else:
                new_lines.append("")
                new_lines.append(f"_{raw}_")
                new_lines.append("")
            i += 1
            continue

        new_lines.append(line)
        i += 1

    res = "\n".join(new_lines)
    res = re.sub(r"\n{3,}", "\n\n", res)
    return res


def polish_all_files():
    for fname in ["qcvn_06_2022_bxd.md", "qcvn_06_2022_bxd_hop_nhat_2023.md", "sua_doi_1_2023_qcvn_06_2022_bxd.md"]:
        fpath = BUNDLE_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        polished = format_table_notes_in_text(text)
        fpath.write_text(polished, encoding="utf-8")
        print(f"✅ Đã chuẩn hóa Chú thích chân bảng cho: {fname}")


if __name__ == "__main__":
    polish_all_files()
