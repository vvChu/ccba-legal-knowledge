"""CCBA Comprehensive Table & Footnote Refinement.

1. Restores column numbering: '(1 <sup>0)</sup>' -> '(10)', '(1 <sup>1)</sup>' -> '(11)', etc.
2. Converts group names with note indices: 'Nhóm 1 1)' -> 'Nhóm 1 <sup>1)</sup>', 'Nhóm 2 2)' -> 'Nhóm 2 <sup>2)</sup>', 'Nhóm 2 3)' -> 'Nhóm 2 <sup>3)</sup>'.
3. Formats all item footnotes ('1) “Cốt liệu Nhóm 1”...', '2) “Cốt liệu Nhóm 2”...') into '_GHI CHÚ CHỈ SỐ PHỤ:_'.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"


def refine_markdown(text: str) -> str:
    # 1. Fix column numbering artifacts '(1 <sup>0)</sup>' -> '(10)', '(1 <sup>1)</sup>' -> '(11)'
    for n in range(10, 25):
        d1 = n // 10
        d2 = n % 10
        text = text.replace(f"({d1} <sup>{d2})</sup>)", f"({n})")
        text = text.replace(f"({d1}<sup>{d2})</sup>)", f"({n})")

    # 2. Fix group references inside tables: 'Nhóm 1 1)' -> 'Nhóm 1 <sup>1)</sup>', 'Nhóm 2 2)' -> 'Nhóm 2 <sup>2)</sup>', 'Nhóm 2 3)' -> 'Nhóm 2 <sup>3)</sup>'
    lines = text.splitlines()
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # In table rows:
        if stripped.startswith("|") and stripped.endswith("|"):
            # Replace 'Nhóm 1 1)' -> 'Nhóm 1 <sup>1)</sup>'
            line = re.sub(r"\b(Nhóm\s+\d+)\s*(\d)\)", r"\1 <sup>\2)</sup>", line)
            # Replace 'vôi1)' -> 'vôi <sup>1)</sup>'
            line = re.sub(r"\b([a-zA-ZÀ-ỹ]+)(\d)\)", r"\1 <sup>\2)</sup>", line)
            new_lines.append(line)
            i += 1
            continue

        # In footnote lines under tables:
        # Check for patterns like '_1) “Cốt liệu...' or '1) “Cốt liệu...' or '_1) Vermiculite...'
        m_item_fn = re.match(r"^(?:_)?\s*(\d+\)\s+(?:[“\"']|[A-ZÀ-Ỹ]).*)$", stripped)
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

        new_lines.append(line)
        i += 1

    res = "\n".join(new_lines)
    res = re.sub(r"\n{3,}", "\n\n", res)
    return res


def main():
    print("Refining tables and footnotes across all bundle files...")
    for fn in ["qcvn_06_2022_bxd.md", "qcvn_06_2022_bxd_hop_nhat_2023.md", "sua_doi_1_2023_qcvn_06_2022_bxd.md"]:
        fp = BUNDLE_DIR / fn
        if not fp.exists():
            continue
        text = fp.read_text(encoding="utf-8")
        refined = refine_markdown(text)
        fp.write_text(refined, encoding="utf-8")
        print(f"✅ Đã hoàn thiện Bảng & Ghi chú chỉ số phụ cho: {fn}")


if __name__ == "__main__":
    main()
