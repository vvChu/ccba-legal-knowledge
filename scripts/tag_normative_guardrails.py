"""CCBA Legal Enforceability Guardrails Tagger for clauses.json (ADR 0003).

Tags every clause node in clauses.json with:
- normative_status: 'mandatory' | 'informative'
- legal_enforceability: True | False
"""

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BUNDLE_DIR = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
CLAUSES_JSON = BUNDLE_DIR / "clauses.json"


def tag_clauses() -> None:
    if not CLAUSES_JSON.exists():
        print(f"❌ File not found: {CLAUSES_JSON}")
        return

    data = json.loads(CLAUSES_JSON.read_text(encoding="utf-8"))
    mandatory_count = 0
    informative_count = 0

    for item in data:
        cid = str(item.get("id", "")).lower()
        title = str(item.get("title", "")).lower()

        # Informative: Phụ lục I (tham khảo) or tài liệu tham khảo
        if "phu-luc-i" in cid or "tham khảo" in title or "phụ lục i" in title:
            item["normative_status"] = "informative"
            item["legal_enforceability"] = False
            informative_count += 1
        else:
            item["normative_status"] = "mandatory"
            item["legal_enforceability"] = True
            mandatory_count += 1

    CLAUSES_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Đã gắn cờ Legal Guardrails cho {len(data)} điều khoản trong clauses.json:")
    print(f"   - Mandatory (Bắt buộc) : {mandatory_count} điều khoản")
    print(f"   - Informative (Tham khảo): {informative_count} điều khoản")


def main() -> None:
    print("=================================================================")
    print("      TAGGING LEGAL ENFORCEABILITY GUARDRAILS (ADR 0003)        ")
    print("=================================================================")
    tag_clauses()
    print("=================================================================")


if __name__ == "__main__":
    main()
