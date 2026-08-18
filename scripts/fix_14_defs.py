"""Fix Section 1.4 definitions in qcvn_06_2022_bxd.md: 1.4.X.Y -> 1.4.XY."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
base_file = bundle_dir / "qcvn_06_2022_bxd.md"

text = base_file.read_text(encoding="utf-8")

# Convert 1.4.tens.units -> 1.4.num
for tens in range(1, 8):
    for units in range(0, 10):
        num = tens * 10 + units
        if 10 <= num <= 72:
            # Replace anchor
            text = text.replace(f'muc-1-4-{tens}-{units}', f'muc-1-4-{num}')
            # Replace heading
            text = re.sub(rf'(#+|\b)1\.4\.{tens}\.{units}\b', rf'\g<1>1.4.{num}', text)

base_file.write_text(text, encoding="utf-8")
print("✅ Fixed Section 1.4 definitions 1.4.10 to 1.4.72.")
