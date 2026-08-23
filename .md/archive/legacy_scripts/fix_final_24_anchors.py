"""Fix exact 24 remaining anchors in qcvn_06_2022_bxd.md and link targets."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
base_file = bundle_dir / "qcvn_06_2022_bxd.md"
sd_file = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"

base_text = base_file.read_text(encoding="utf-8")

# 1. Specific Chapter fixes in base text:
replacements = {
    # 6.13
    '6.1.3  Mỗi khoang cháy': '6.13  Mỗi khoang cháy',
    'muc-6-1-3': 'muc-6-13',
    # 6.14
    '6.1.4  Phải có đường': '6.14  Phải có đường',
    'muc-6-1-4': 'muc-6-14',
    # 6.17.2
    '6.1.7.2  ': '6.17.2  ',
    'muc-6-1-7-2': 'muc-6-17-2',
    # 4.35
    '4.3.5  ': '4.35  ',
    'muc-4-3-5': 'muc-4-35',
    # 5.2.11
    '5.2.1.1  ': '5.2.11  ',
    'muc-5-2-1-1': 'muc-5-2-11',
    # 3.4.11
    '3.4.1.1  ': '3.4.11  ',
    'muc-3-4-1-1': 'muc-3-4-11',
}

for k, v in replacements.items():
    base_text = base_text.replace(k, v)

# Ensure Appendix anchors exist for D.1.1, D.1.3, D.1.5, D.1.8, D.8, D.9, E.3, E.3.3, H.2.1, H.2.12.4, H.6.2, A.2.3, A.2.4, A.3.2.1, C.3.2, C.3.2.2
app_clauses = ['A.2.3', 'A.2.4', 'A.3.2.1', 'C.3.2', 'C.3.2.2', 'D.1.1', 'D.1.3', 'D.1.5', 'D.1.8', 'D.8', 'D.9', 'E.3', 'E.3.3', 'H.2.1', 'H.2.12.4', 'H.6.2']
for ac in app_clauses:
    slug = f"muc-{ac.lower().replace('.', '-')}"
    # If code exists without anchor, add anchor
    pattern = rf'(#{1,6}\s+)?(\b{re.escape(ac)}\b\s+)'
    def add_anchor(m: re.Match) -> str:
        h = m.group(1) or "#### "
        return f'{h}<a id="{slug}" name="{slug}"></a>{m.group(2)}'
    if f'id="{slug}"' not in base_text:
        base_text = re.sub(pattern, add_anchor, base_text, count=1)

base_file.write_text(base_text, encoding="utf-8")

# 2. Fix link targets in Sửa đổi 1
sd_text = sd_file.read_text(encoding="utf-8")
sd_text = sd_text.replace("#muc-e-1", "#bang-e-1").replace("#muc-h-6", "#bang-h-6")
sd_file.write_text(sd_text, encoding="utf-8")

print("✅ Applied exact 24 anchor fixes.")
