import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(".")
LEGAL_DOCS = ROOT / "legal_docs"

# Compare QCVN 06:2022 clause 3.4.12 or similar
q06_base = (LEGAL_DOCS / "02_qcvn" / "qcvn_06_2022_bxd" / "qcvn_06_2022_bxd.md").read_text(encoding="utf-8")
q06_hn = (LEGAL_DOCS / "02_qcvn" / "qcvn_06_2022_bxd" / "qcvn_06_2022_bxd_hop_nhat_2023.md").read_text(encoding="utf-8")

import re

def get_clause(text, anchor):
    pattern = rf'(<a id="{anchor}".*?)(?=(?:<a id="muc-|\Z))'
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1).strip() if m else "NOT FOUND"

print("=== VÍ DỤ XUNG ĐỘT THỰC TẾ 1: QCVN 06 - Điều 2.2.1.2 ===")
print("--- [BẢN GỐC 2022 (qcvn_06_2022_bxd.md)] ---")
print(get_clause(q06_base, "muc-2-2-1-2")[:300])
print("\n--- [BẢN HỢP NHẤT 2023 (qcvn_06_2022_bxd_hop_nhat_2023.md)] ---")
print(get_clause(q06_hn, "muc-2-2-1-2")[:300])

print("\n=== VÍ DỤ XUNG ĐỘT THỰC TẾ 2: QCVN 04 - Mục 2.10 (Bổ sung mới toàn bộ) ===")
print("--- [BẢN GỐC 2021 (qcvn_04_2021_bxd.md)] ---")
print(get_clause(q06_base, "muc-2-10")) # Not present in QCVN 04 base
print("\n--- [BẢN HỢP NHẤT 2026 (qcvn_04_2021_bxd_hop_nhat_2026.md)] ---")
q04_hn = (LEGAL_DOCS / "02_qcvn" / "qcvn_04_2021_bxd" / "qcvn_04_2021_bxd_hop_nhat_2026.md").read_text(encoding="utf-8")
print(get_clause(q04_hn, "muc-2-10")[:300])
