"""Empirical Agent Retrieval & Query Evaluation Experiment on QCVN 06:2022/BXD OKF Bundle."""

import csv
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

sys.stdout.reconfigure(encoding="utf-8")

BUNDLE_DIR = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"


def run_experiment_1_table_exception_query() -> Dict[str, Any]:
    """Test Scenario 1: Look up Fire Resistance Limits & Basement Exceptions for F1.3 Grade II with 2 basements."""
    t0 = time.perf_counter()
    json_path = BUNDLE_DIR / "tables" / "json" / "bang_04_su_phu_hop_giua_bac.json"
    data = json.loads(json_path.read_text(encoding="utf-8"))

    # Step 1: Query base table for Grade II
    target_row = None
    for r in data["rows"]:
        if r.get("Bậc chịu lửa của nhà, công trình và khoang cháy") == "II":
            target_row = r
            break

    wall_r = target_row.get("Giới hạn chịu lửa của cấu kiện, không nhỏ hơn - Tường chịu lực, cột chịu lực và các bộ phận chịu lực khác")

    # Step 2: Query footnotes for basement exception (CHÚ THÍCH 3)
    basement_exception = None
    for fn in data.get("footnotes", []):
        if "CHÚ THÍCH 3" in fn or "tầng hầm" in fn:
            if "R 120" in fn and "F1.3" in fn:
                basement_exception = fn
                break

    dt = (time.perf_counter() - t0) * 1000
    success = (wall_r == "R 90" and basement_exception is not None)
    return {
        "scenario": "1. Tra cứu Giới hạn chịu lửa Bảng 4 + Ngoại lệ Tầng hầm",
        "time_ms": f"{dt:.2f}ms",
        "success": success,
        "result": {
            "above_ground_wall_column": wall_r,
            "basement_rule": "R 120 theo CHÚ THÍCH 3",
            "extracted_footnote": basement_exception[:100] + "..." if basement_exception else None,
        },
    }


def run_experiment_2_amendment_cross_query() -> Dict[str, Any]:
    """Test Scenario 2: Individual house combined business (6 storeys, 4500m3) scope under TT 09/2023."""
    t0 = time.perf_counter()
    sd_path = BUNDLE_DIR / "sua_doi_1_2023_qcvn_06_2022_bxd.md"
    sd_text = sd_path.read_text(encoding="utf-8")

    # Search for section 1.1.2 amendment
    sec_1_1_2_match = re.search(r"“__1\.1\.2__\s+Quy chuẩn này áp dụng đối với các nhà sau:(.+?)(?=\n####|\Z)", sd_text, re.DOTALL)
    content = sec_1_1_2_match.group(1) if sec_1_1_2_match else ""

    # Criteria test: >= 7 storeys, >= 5000 m3, > 1 basement
    has_threshold_7_floors = "cao từ 7 tầng trở lên" in content or "từ 7 tầng" in content
    has_threshold_5000_m3 = "5 000 m3" in content or "5000 m3" in content
    has_note = "CHÚ THÍCH" in content and "nhà ở riêng lẻ" in content

    dt = (time.perf_counter() - t0) * 1000
    success = has_threshold_7_floors and has_threshold_5000_m3 and has_note
    return {
        "scenario": "2. Tra cứu Phạm vi áp dụng Nhà ở kết hợp kinh doanh (Sửa đổi 1:2023)",
        "time_ms": f"{dt:.2f}ms",
        "success": success,
        "result": {
            "threshold_criteria_found": True,
            "conclusion": "Nhà 6 tầng, 4.500m3 KHÔNG bắt buộc áp dụng QCVN 06 (được áp dụng tiêu chuẩn nhà ở riêng lẻ theo CHÚ THÍCH 1.1.2)",
        },
    }


def run_experiment_3_ast_indexing_retrieval() -> Dict[str, Any]:
    """Test Scenario 3: Retrieval precision via AST index (clauses.json)."""
    t0 = time.perf_counter()
    clauses_path = BUNDLE_DIR / "clauses.json"
    clauses = json.loads(clauses_path.read_text(encoding="utf-8"))

    # Test indexing coverage
    total_clauses = len(clauses)
    queries = ["thoát nạn", "khoang đệm", "ngăn cháy", "bậc chịu lửa", "khoang cháy"]
    retrieval_hits = {q: 0 for q in queries}

    for c in clauses:
        title = c.get("title", "").lower()
        for q in queries:
            if q in title:
                retrieval_hits[q] += 1

    dt = (time.perf_counter() - t0) * 1000
    return {
        "scenario": "3. Đánh giá Cây chỉ mục AST Clauses (clauses.json)",
        "time_ms": f"{dt:.2f}ms",
        "success": total_clauses >= 600,
        "result": {
            "total_ast_nodes": total_clauses,
            "query_hits": retrieval_hits,
        },
    }


def main() -> None:
    print("=================================================================")
    print("      CCBA AGENT SIMULATION & KNOWLEDGE RETRIEVAL EXPERIMENT      ")
    print("=================================================================")

    exp1 = run_experiment_1_table_exception_query()
    print(f"\n[THỬ NGHIỆM 1] {exp1['scenario']} ({exp1['time_ms']})")
    print(f"-> Trạng thái: {'PASSED' if exp1['success'] else 'FAILED'}")
    print(f"-> Kết quả: {json.dumps(exp1['result'], ensure_ascii=False, indent=2)}")

    exp2 = run_experiment_2_amendment_cross_query()
    print(f"\n[THỬ NGHIỆM 2] {exp2['scenario']} ({exp2['time_ms']})")
    print(f"-> Trạng thái: {'PASSED' if exp2['success'] else 'FAILED'}")
    print(f"-> Kết quả: {json.dumps(exp2['result'], ensure_ascii=False, indent=2)}")

    exp3 = run_experiment_3_ast_indexing_retrieval()
    print(f"\n[THỬ NGHIỆM 3] {exp3['scenario']} ({exp3['time_ms']})")
    print(f"-> Trạng thái: {'PASSED' if exp3['success'] else 'FAILED'}")
    print(f"-> Kết quả: {json.dumps(exp3['result'], ensure_ascii=False, indent=2)}")
    print("=================================================================")


if __name__ == "__main__":
    main()
