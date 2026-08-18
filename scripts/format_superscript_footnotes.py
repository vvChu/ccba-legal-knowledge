"""CCBA Superscript Footnote Reference & Note Section Formatter (Clean Version).

Processes only table cells and footnote blocks, strictly preserving markdown links.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"


def format_table_cells_superscript(line: str) -> str:
    """Formats attached footnote symbols inside table rows only."""
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return line

    cells = line.split("|")
    new_cells = []
    for c in cells:
        # 1. Word attached to footnote: 'thạch cao1)' -> 'thạch cao <sup>1)</sup>', 'thạch cao2)' -> 'thạch cao <sup>2)</sup>'
        c_mod = re.sub(r"([a-zA-ZÀ-ỹ]+)\s*(\d+)\)", r"\1 <sup>\2)</sup>", c)
        
        # 2. Number attached to footnote inside table cell: '1001)' -> '100 <sup>1)</sup>', '851)' -> '85 <sup>1)</sup>'
        def rep_num_fn(m):
            val = m.group(1).strip()
            fn_idx = m.group(2)
            return f"{val} <sup>{fn_idx})</sup>"

        c_mod = re.sub(r"\b(\d+(?:\s+\d+)*)(\d)\)", rep_num_fn, c_mod)
        new_cells.append(c_mod)

    return "|".join(new_cells)


def format_document(text: str) -> str:
    lines = text.splitlines()
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check if line contains standalone specific item footnotes like '1) Có thể bổ sung... 2) Vermiculite...'
        m_item_fn = re.match(r"^(?:_)?\s*(\d+\)\s+[A-ZÀ-Ỹ].*)$", stripped)
        if m_item_fn and not stripped.startswith("- **CHÚ THÍCH") and not stripped.startswith("_CHÚ THÍCH") and not stripped.startswith("####"):
            raw_fn = m_item_fn.group(1).strip(" _")
            parts = re.split(r"(?=\b\d+\)\s+)", raw_fn)
            
            new_lines.append("")
            new_lines.append("_GHI CHÚ CHỈ SỐ PHỤ:_")
            for p in parts:
                p_clean = p.strip(" _")
                if not p_clean:
                    continue
                p_formatted = re.sub(r"^(\d+\))\s*", r"- **\1** ", p_clean)
                new_lines.append(p_formatted)
            new_lines.append("")
            i += 1
            continue

        line_formatted = format_table_cells_superscript(line)
        new_lines.append(line_formatted)
        i += 1

    res = "\n".join(new_lines)
    res = re.sub(r"\n{3,}", "\n\n", res)
    return res


def main():
    for fn in ["qcvn_06_2022_bxd.md", "qcvn_06_2022_bxd_hop_nhat_2023.md", "sua_doi_1_2023_qcvn_06_2022_bxd.md"]:
        fp = BUNDLE_DIR / fn
        if not fp.exists():
            continue
        text = fp.read_text(encoding="utf-8")
        formatted_text = format_document(text)
        fp.write_text(formatted_text, encoding="utf-8")
        print(f"✅ Đã nâng cấp Superscript Footnotes cho: {fn}")


if __name__ == "__main__":
    main()
