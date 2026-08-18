"""Inline anchor tags into Markdown headings for seamless IDE/Browser jump navigation.

Converts:
<a id="foo"></a>
### Bar
To:
### <a id="foo" name="foo"></a>Bar
"""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"


def process_file(md_path: Path) -> int:
    text = md_path.read_text(encoding="utf-8")

    # Match: <a id="foo"></a>\n(#+ .+)
    # Replace with: #+ <a id="foo" name="foo"></a>.+
    pattern = r'<a id="([^"]+)"></a>\n(#{1,6})\s*(.+)'

    def replacer(match: re.Match) -> str:
        anchor_id = match.group(1)
        hashes = match.group(2)
        title = match.group(3)
        return f'{hashes} <a id="{anchor_id}" name="{anchor_id}"></a>{title}'

    new_text, count = re.subn(pattern, replacer, text)
    md_path.write_text(new_text, encoding="utf-8")
    return count


def main() -> None:
    print("=================================================================")
    print("      INLINE ANCHORS TO HEADINGS FOR PRECISE SCROLLING          ")
    print("=================================================================")

    c1 = process_file(bundle_dir / "qcvn_06_2022_bxd.md")
    print(f"✅ Đã inline {c1} thẻ neo vào đề mục của qcvn_06_2022_bxd.md")

    c2 = process_file(bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md")
    print(f"✅ Đã inline {c2} thẻ neo vào đề mục của sua_doi_1_2023_qcvn_06_2022_bxd.md")

    print("=================================================================")


if __name__ == "__main__":
    main()
