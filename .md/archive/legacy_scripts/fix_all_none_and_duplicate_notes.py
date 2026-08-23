"""CCBA None Heading & Duplicate Note Header Cleaner.

Fixes:
1. Malformed '### #### <a id="muc-x-y-z"></a>NoneText' into '#### <a id="muc-x-y-z" name="muc-x-y-z"></a>X.Y.Z  Text'.
2. In-line text '#### <a id="muc-e-3"></a>Nonetrong' into 'E.3 trong'.
3. Deduplicates consecutive '_CHÚ THÍCH:_' headers into a unified bullet list.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"

def slug_to_code(slug: str) -> str:
    # e.g. muc-d-8 -> D.8, muc-a-3-2-1 -> A.3.2.1, muc-1-4-8 -> 1.4.8
    s = slug.replace("muc-", "").replace("sd1-", "").replace("bang-", "")
    parts = s.split("-")
    if len(parts) > 0 and parts[0].isalpha():
        return parts[0].upper() + "." + ".".join(parts[1:]) if len(parts) > 1 else parts[0].upper()
    return ".".join(parts)

def fix_document(text: str) -> str:
    # 1. Fix in-line sentence artifact: 'quy định tại #### <a id="muc-e-3"...></a>Nonetrong Phụ lục E'
    text = re.sub(
        r'quy định tại\s+#+\s*<a\s+id="muc-e-3"[^>]*></a>None\s*trong\s+Phụ lục E',
        'quy định tại E.3 trong Phụ lục E',
        text
    )

    # 2. Fix '### #### <a id="muc-(...)"></a>None(...)'
    def replace_none_heading(m: re.Match) -> str:
        slug = m.group(1)
        body = m.group(2).strip()
        code = slug_to_code(slug)
        dots = code.count(".")
        h_level = min(5, max(3, dots + 2))
        h_hashes = "#" * h_level
        return f'{h_hashes} <a id="{slug}" name="{slug}"></a>{code}  {body}'

    text = re.sub(
        r'#+\s*<a\s+id="([^"]+)"[^>]*></a>None\s*([^\n]+)',
        replace_none_heading,
        text
    )

    # 3. Clean up multiple consecutive '_CHÚ THÍCH:_' lines
    lines = text.splitlines()
    new_lines = []
    i = 0
    in_note_group = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped == "_CHÚ THÍCH:_":
            if not in_note_group:
                new_lines.append("")
                new_lines.append("_CHÚ THÍCH:_")
                in_note_group = True
            i += 1
            continue

        if stripped.startswith("- **CHÚ THÍCH") or (in_note_group and stripped.startswith("- ")):
            new_lines.append(line)
            i += 1
            continue

        if stripped:
            in_note_group = False

        new_lines.append(line)
        i += 1

    res = "\n".join(new_lines)
    res = re.sub(r"\n{3,}", "\n\n", res)
    return res

def main() -> None:
    for fn in ["qcvn_06_2022_bxd.md", "qcvn_06_2022_bxd_hop_nhat_2023.md", "sua_doi_1_2023_qcvn_06_2022_bxd.md"]:
        fp = BUNDLE_DIR / fn
        if not fp.exists():
            continue
        text = fp.read_text(encoding="utf-8")
        fixed = fix_document(text)
        fp.write_text(fixed, encoding="utf-8")
        print(f"✅ Đã khắc phục lỗi None Heading & Duplicate Note Headers cho: {fn}")

if __name__ == "__main__":
    main()
