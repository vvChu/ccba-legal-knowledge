"""Fix H.2.11, H.2.12 and H.6.2 in base and amendment markdown files."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
base_file = bundle_dir / "qcvn_06_2022_bxd.md"
sd_file = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"

base_text = base_file.read_text(encoding="utf-8")

# Replace H.2.1.1.X with H.2.11.X
base_text = re.sub(r'H\.2\.1\.1\.(\d+)', r'H.2.11.\1', base_text)
base_text = re.sub(r'H\.2\.1\.1\b', r'H.2.11', base_text)

# Replace H.2.1.2.X with H.2.12.X
base_text = re.sub(r'H\.2\.1\.2\.(\d+)', r'H.2.12.\1', base_text)
base_text = re.sub(r'H\.2\.1\.2\b', r'H.2.12', base_text)

# Add anchor for H.2.12.4
base_text = re.sub(
    r'(#{1,6}\s+)?H\.2\.12\.4\s+',
    r'#### <a id="muc-h-2-12-4" name="muc-h-2-12-4"></a>H.2.12.4  ',
    base_text
)

# Add anchor for H.6.2
base_text = re.sub(
    r'(#{1,6}\s+)?H\.6\.2\s+',
    r'#### <a id="muc-h-6-2" name="muc-h-6-2"></a>H.6.2  ',
    base_text
)

base_file.write_text(base_text, encoding="utf-8")

# Fix in Sửa đổi 1
sd_text = sd_file.read_text(encoding="utf-8")
sd_text = sd_text.replace('#bang-h-6-2', '#muc-h-6-2')
sd_file.write_text(sd_text, encoding="utf-8")

print("✅ Fixed H.2.11, H.2.12 and H.6.2 anchors.")
