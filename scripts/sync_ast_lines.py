"""Sync AST Clause trees line numbers after anchor inlining."""

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"


def sync_clauses_json(md_path: Path, json_path: Path) -> int:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    clauses = json.loads(json_path.read_text(encoding="utf-8"))
    anchor_to_line = {}

    for idx, l in enumerate(lines):
        m = re.search(r'<a id="([^"]+)"', l)
        if m:
            anchor_to_line[m.group(1)] = idx + 1

    updated = 0
    for c in clauses:
        anchor = c.get("anchor")
        if anchor and anchor in anchor_to_line:
            c["line_number"] = anchor_to_line[anchor]
            updated += 1

    json_path.write_text(json.dumps(clauses, ensure_ascii=False, indent=2), encoding="utf-8")
    return updated


def main() -> None:
    u1 = sync_clauses_json(bundle_dir / "qcvn_06_2022_bxd.md", bundle_dir / "clauses.json")
    print(f"✅ Đã đồng bộ {u1} AST clauses cho qcvn_06_2022_bxd.md")

    u2 = sync_clauses_json(bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md", bundle_dir / "clauses_sd1.json")
    print(f"✅ Đã đồng bộ {u2} AST clauses cho sua_doi_1_2023_qcvn_06_2022_bxd.md")


if __name__ == "__main__":
    main()
