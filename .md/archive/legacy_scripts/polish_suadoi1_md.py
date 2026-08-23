"""Polish spacing and anchor formatting for sua_doi_1_2023_qcvn_06_2022_bxd.md."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

p = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "sua_doi_1_2023_qcvn_06_2022_bxd.md"
text = p.read_text(encoding="utf-8")

# Ensure blank line before <a id="sd1-...">
text = re.sub(r"([^\n])\n(<a id=\"sd1-[^\"]+\"></a>)", r"\1\n\n\2", text)
# Ensure clean spacing
text = re.sub(r"\n{3,}", "\n\n", text)

p.write_text(text, encoding="utf-8")
print("✅ Polished sua_doi_1_2023_qcvn_06_2022_bxd.md successfully.")
