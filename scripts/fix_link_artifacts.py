"""CCBA Link & Anchor Artifact Cleaner.

Fixes:
1. Replaces accidental 'bang-1 <sup>0' -> 'bang-10', 'bang-1 <sup>1' -> 'bang-11', 'bang-h-1 <sup>0' -> 'bang-h-10', 'bang-h-1 <sup>1' -> 'bang-h-11'.
2. Restores '### <a id="muc-e-3" name="muc-e-3"></a>E.3' heading.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"


def fix_file(fpath: Path) -> None:
    text = fpath.read_text(encoding="utf-8")

    # Fix markdown links that got corrupted by footnote regex
    text = re.sub(r"bang-1\s*<sup>0\)", "bang-10", text)
    text = re.sub(r"bang-1\s*<sup>1\)", "bang-11", text)
    text = re.sub(r"bang-h-1\s*<sup>0\)", "bang-h-10", text)
    text = re.sub(r"bang-h-1\s*<sup>1\)", "bang-h-11", text)
    text = re.sub(r"bang-h-1\s*<sup>2\)", "bang-h-12", text)

    # In anchor IDs: <a id="bang-1 <sup>0"...
    text = re.sub(r'id="bang-1\s*<sup>0[^"]*"', 'id="bang-10"', text)
    text = re.sub(r'name="bang-1\s*<sup>0[^"]*"', 'name="bang-10"', text)
    text = re.sub(r'id="bang-1\s*<sup>1[^"]*"', 'id="bang-11"', text)
    text = re.sub(r'name="bang-1\s*<sup>1[^"]*"', 'name="bang-11"', text)
    text = re.sub(r'id="bang-h-1\s*<sup>0[^"]*"', 'id="bang-h-10"', text)
    text = re.sub(r'name="bang-h-1\s*<sup>0[^"]*"', 'name="bang-h-10"', text)
    text = re.sub(r'id="bang-h-1\s*<sup>1[^"]*"', 'id="bang-h-11"', text)
    text = re.sub(r'name="bang-h-1\s*<sup>1[^"]*"', 'name="bang-h-11"', text)
    text = re.sub(r'id="bang-h-1\s*<sup>2[^"]*"', 'id="bang-h-12"', text)
    text = re.sub(r'name="bang-h-1\s*<sup>2[^"]*"', 'name="bang-h-12"', text)

    # Check E.3 heading in base doc
    if fpath.name == "qcvn_06_2022_bxd.md" or fpath.name == "qcvn_06_2022_bxd_hop_nhat_2023.md":
        if '<a id="muc-e-3"' not in text:
            # Inject E.3 heading before E.3.1
            text = text.replace("### <a id=\"muc-e-3-1\"", "### <a id=\"muc-e-3\" name=\"muc-e-3\"></a>E.3  Khoảng cách phòng cháy chống cháy theo đường ranh giới\n\n### <a id=\"muc-e-3-1\"")

    fpath.write_text(text, encoding="utf-8")
    print(f"✅ Cleaned link artifacts in: {fpath.name}")


def main() -> None:
    for fn in ["qcvn_06_2022_bxd.md", "qcvn_06_2022_bxd_hop_nhat_2023.md", "sua_doi_1_2023_qcvn_06_2022_bxd.md"]:
        fp = BUNDLE_DIR / fn
        if fp.exists():
            fix_file(fp)


if __name__ == "__main__":
    main()
