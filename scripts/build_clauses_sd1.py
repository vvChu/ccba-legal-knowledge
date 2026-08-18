"""Generate clauses_sd1.json AST for Sửa đổi 1:2023 QCVN 06:2022/BXD."""

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
sd_path = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"
target_json = bundle_dir / "clauses_sd1.json"

text = sd_path.read_text(encoding="utf-8")
lines = text.splitlines()

nodes = []
current_chapter = "Mở đầu"

for idx, line in enumerate(lines):
    l = line.strip()

    # Match Chapter / Appendix
    m_ch = re.match(r"^###\s+<a id=\"([^\"]+)\"[^>]*></a>(.+)$", l)
    if m_ch:
        current_chapter = m_ch.group(2).strip()
        continue

    # Match Action Point
    m_pt = re.match(r"^####\s+<a id=\"([^\"]+)\"[^>]*></a>(.+)$", l)
    if m_pt:
        slug = m_pt.group(1).strip()
        raw_title = m_pt.group(2).strip()
        clean_title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw_title)

        # Detect action type
        action_type = "modify"
        if "bổ sung" in clean_title.lower() and "sửa đổi" not in clean_title.lower():
            action_type = "add"
        elif "bãi bỏ" in clean_title.lower():
            action_type = "repeal"
        elif "thay thế" in clean_title.lower():
            action_type = "replace"

        # Detect target clause
        m_sec = re.search(r"((?:[A-Z]\.)?\d+(?:\.\d+)*|[A-Z]\.\d+)", clean_title)
        m_tbl = re.search(r"Bảng\s+([A-Z0-9.]+)", clean_title, re.IGNORECASE)
        m_app = re.search(r"Phụ lục\s+([A-Z])", clean_title, re.IGNORECASE)

        target_clause = None
        if m_tbl:
            target_clause = f"Bảng {m_tbl.group(1)}"
        elif m_app:
            target_clause = f"Phụ lục {m_app.group(1)}"
        elif m_sec:
            target_clause = f"điểm {m_sec.group(1)}"

        nodes.append({
            "id": slug,
            "title": clean_title,
            "action_type": action_type,
            "target_clause": target_clause,
            "chapter": current_chapter,
            "line": idx + 1,
        })

target_json.write_text(json.dumps(nodes, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ Đã tạo clauses_sd1.json: {len(nodes)} điểm sửa đổi.")
