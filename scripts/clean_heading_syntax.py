"""CCBA Heading Syntax & Anchor Normalizer.

Cleans up:
1. Multi-hash blocks like '### ### <a id' -> '### <a id'.
2. Orphan standalone anchors directly preceding a heading.
3. In-line text issues.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"


def clean_file(fpath: Path) -> None:
    text = fpath.read_text(encoding="utf-8")

    # 1. Clean multi-hash blocks: '### ### <a id...' -> '### <a id...'
    text = re.sub(r"^#+(?:\s+#+)+\s*", "### ", text, flags=re.MULTILINE)

    # 2. Remove orphan standalone anchor lines directly preceding a heading
    text = re.sub(r'<a id="[^"]+"></a>\s*\n+(#+\s+<a id=)', r"\1", text)

    # 3. Ensure consistent blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    fpath.write_text(text, encoding="utf-8")
    print(f"✅ Cleaned heading syntax in: {fpath.name}")


def main() -> None:
    for fn in ["qcvn_06_2022_bxd.md", "qcvn_06_2022_bxd_hop_nhat_2023.md", "sua_doi_1_2023_qcvn_06_2022_bxd.md"]:
        fp = BUNDLE_DIR / fn
        if fp.exists():
            clean_file(fp)


if __name__ == "__main__":
    main()
