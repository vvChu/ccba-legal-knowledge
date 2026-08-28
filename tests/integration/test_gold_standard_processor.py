"""Unit tests for OKF Gold Standard Processor."""

import json
from pathlib import Path

from ccba_legal.gold_standard import (
    clean_html_tables,
    inject_semantic_anchors,
    generate_clauses_ast,
    process_okf_bundle,
    get_doc_profile,
)

SAMPLE_RAW_HTML_TEXT = """---
title: "Luật PCCC 2024"
---

# Điều 1. Phạm vi điều chỉnh
1. Luật này quy định về phòng cháy, chữa cháy và cứu nạn, cứu hộ.
<table border="1">
<tr><td>Chỉ tiêu</td><td>Giá trị</td></tr>
<tr><td>Bán kính phục vụ</td><td>500m</td></tr>
</table>
2. Cơ quan, tổ chức, cá nhân có trách nhiệm tuân thủ.

# Điều 2. Đối tượng áp dụng
1. Cơ quan nhà nước, tổ chức kinh tế.
"""

SAMPLE_QCVN_TEXT = """---
title: "QCVN 04:2021/BXD"
---

# 1.1 Phạm vi áp dụng
Thủ tục quy định về an toàn nhà chung cư.

# 2.1.2 Giới hạn chịu lửa
Chi tiết về giới hạn chịu lửa của linh kiện.
"""

def test_clean_html_tables():
    cleaned = clean_html_tables(SAMPLE_RAW_HTML_TEXT)
    assert "<table" not in cleaned.lower()
    assert "| Chỉ tiêu | Giá trị |" in cleaned
    assert "| Bán kính phục vụ | 500m |" in cleaned

def test_inject_semantic_anchors():
    anchored = inject_semantic_anchors(SAMPLE_RAW_HTML_TEXT)
    assert '<a id="dieu-1"></a>' in anchored
    assert '<a id="dieu-1-khoan-1"></a>' in anchored
    assert '<a id="dieu-2"></a>' in anchored

def test_inject_semantic_anchors_qcvn():
    profile = get_doc_profile("qcvn")
    anchored = inject_semantic_anchors(SAMPLE_QCVN_TEXT, profile)
    assert '<a id="muc-1-1"></a>' in anchored
    assert '<a id="muc-2-1-2"></a>' in anchored

def test_generate_clauses_ast():
    anchored = inject_semantic_anchors(SAMPLE_RAW_HTML_TEXT)
    clauses = generate_clauses_ast(anchored)
    assert len(clauses) >= 2
    assert clauses[0]["anchor"] == "dieu-1"
    assert "Điều 1" in clauses[0]["title"]

def test_process_okf_bundle(tmp_path: Path):
    bundle_dir = tmp_path / "test_bundle"
    bundle_dir.mkdir()
    md_file = bundle_dir / "test_bundle.md"
    md_file.write_text(SAMPLE_RAW_HTML_TEXT, encoding="utf-8")

    res = process_okf_bundle(bundle_dir)
    assert res["status"] == "success"
    assert (bundle_dir / "clauses.json").exists()
    assert (bundle_dir / "qa_benchmark.json").exists()

    clauses_data = json.loads((bundle_dir / "clauses.json").read_text(encoding="utf-8"))
    assert len(clauses_data) > 0

    qa_data = json.loads((bundle_dir / "qa_benchmark.json").read_text(encoding="utf-8"))
    assert len(qa_data) >= 1
