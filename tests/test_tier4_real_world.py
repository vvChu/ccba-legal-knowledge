"""Tier 4: Real-World Application Scenarios E2E Test Suite.

Simulates 8 realistic application workloads (RAG retrieval, table parameter lookups,
amendment overrides, bidirectional cross-reference traversal, and full spoke validation)
against QCVN 06:2022/BXD and Sửa đổi 1:2023.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

from tests.conftest import (
    DocxParsedBundle,
    DocxTableData,
    MarkdownParsedBundle,
)

# =====================================================================
# SCENARIO S1: END-TO-END FIRE COMPARTMENT QUERY (RAG RETRIEVAL)
# =====================================================================

def test_scenario_s1_fire_compartment_rag_query(
    qcvn_md_parsed: MarkdownParsedBundle, json_tables_map: Dict[str, dict]
):
    """S1: RAG retrieval simulation for fire resistance ratings of fire separation walls (Bảng 1, Điều 2.3)."""
    # 1. Locate Bảng 1 in JSON table assets
    matching = [v for k, v in json_tables_map.items() if "bang_01" in k or "bang_1" in k]
    assert len(matching) > 0, "Bảng 1 table asset not found in JSON map"
    t1_data = matching[0]

    # 2. Verify table title and structure
    assert "Giới hạn chịu lửa" in t1_data.get("title", "")

    # 3. Simulate RAG query extraction: Tường ngăn cháy loại 1 -> REI 150
    rows = t1_data.get("rows", [])
    found_rei_150 = False
    for r in rows:
        row_str = str(r)
        if "Tường ngăn cháy" in row_str and "REI 150" in row_str:
            found_rei_150 = True
            break
    assert found_rei_150, "REI 150 not found for fire separation walls in Bảng 1"

    # 4. Verify cross-reference in Markdown body
    assert "2.3" in qcvn_md_parsed.normalized_text, "Điều 2.3 cross-reference missing in Markdown"

# =====================================================================
# SCENARIO S2: SMOKE CONTROL & EXTRACTION FORMULA LOOKUP (APPENDIX D)
# =====================================================================

def test_scenario_s2_smoke_control_formula_lookup(
    qcvn_md_parsed: MarkdownParsedBundle, qcvn_docx_parsed: DocxParsedBundle
):
    """S2: Retrieval of Appendix D formula calculations and technical limits for smoke evacuation fans."""
    # 1. Verify Appendix D exists and is indexed
    app_d_paras = qcvn_docx_parsed.chapter_paragraphs.get("D", [])
    assert len(app_d_paras) >= 50, f"Expected >= 50 paragraphs in Appendix D, got {len(app_d_paras)}"

    # 2. Verify smoke exhaust parameters (G_kh, h, density, airflow)
    norm = qcvn_md_parsed.normalized_text
    assert "phụ lục d" in norm, "Appendix D heading missing in Markdown"
    assert "khói" in norm, "Smoke control keywords missing in Markdown"
    
    # Assert smoke fan and formula calculation parameters
    assert "lưu lượng" in norm, "Smoke airflow / mass flow parameter 'lưu lượng' missing in Markdown"
    assert "quạt" in norm or "hút khói" in norm, "Smoke exhaust fan keywords missing in Markdown"
    assert any(term in norm for term in ["nhiệt độ", "áp suất", "khối lượng riêng"]), (
        "Thermodynamic parameters (temperature, pressure, density) missing for smoke control"
    )
    assert any(sym in qcvn_md_parsed.raw_text for sym in ["G", "h", "kg/s", "kg/h", "m3/h", "m³/h"]), (
        "Smoke formula calculation symbols/units missing in Markdown"
    )

# =====================================================================
# SCENARIO S3: TECHNICAL TABLE PARAMETER EXTRACTION (BẢNG E.4a / E.4b)
# =====================================================================

def test_scenario_s3_fire_separation_distance_lookup(
    json_tables_map: Dict[str, dict], qcvn_md_parsed: MarkdownParsedBundle
):
    """S3: Querying fire separation distances for industrial and residential buildings across varying fire hazard categories."""
    # 1. Retrieve Bảng E.4a and E.4b
    t_e4a = [v for k, v in json_tables_map.items() if "bang_e_4a" in k]
    t_e4b = [v for k, v in json_tables_map.items() if "bang_e_4b" in k]

    assert len(t_e4a) > 0, "Bảng E.4a missing in tables/json/"
    assert len(t_e4b) > 0, "Bảng E.4b missing in tables/json/"

    # 2. Verify table dimensions and non-empty data
    assert len(t_e4a[0].get("rows", [])) > 0, "Bảng E.4a has no data rows"
    assert len(t_e4b[0].get("rows", [])) > 0, "Bảng E.4b has no data rows"

# =====================================================================
# SCENARIO S4: AMENDMENT 1:2023 WATER FLOW OVERRIDE (BẢNG 10)
# =====================================================================

def test_scenario_s4_amendment_water_flow_override(
    sd1_md_parsed: Dict[str, Any], qcvn_docx_parsed: DocxParsedBundle
):
    """S4: Verifying queries on fire water flow rates correctly resolve to the replacement Bảng 10 grid in Sửa đổi 1:2023."""
    # 1. Check replacement Table 10 exists in SD1 Markdown
    t10_lines = sd1_md_parsed.get("table_10_lines", [])
    assert len(t10_lines) >= 10, f"Expected 10 rows in SD1 replacement Table 10, found {len(t10_lines)}"

    # 2. Check anchor 'sd1-bang-10'
    assert "sd1-bang-10" in sd1_md_parsed.get("anchors", set()), "Anchor 'sd1-bang-10' missing in SD1"

# =====================================================================
# SCENARIO S5: BIDIRECTIONAL LEGAL CROSS-REFERENCE NAVIGATION
# =====================================================================

def test_scenario_s5_bidirectional_cross_reference_navigation(
    sd1_md_parsed: Dict[str, Any], qcvn_md_parsed: MarkdownParsedBundle
):
    """S5: Navigating from Sửa đổi 1:2023 modified clauses back to base QCVN 06:2022 anchors and vice versa."""
    cross_links = sd1_md_parsed.get("cross_links", [])
    assert len(cross_links) >= 50, f"Expected >= 50 cross-links in SD1, found {len(cross_links)}"

    # Check that each target anchor resolves to a valid anchor in base QCVN
    for label, target_url in cross_links[:20]:
        if "#" in target_url:
            anchor_name = target_url.split("#")[-1]
            assert anchor_name in qcvn_md_parsed.anchors, f"Broken cross-link target '{anchor_name}' for '{label}'"

# =====================================================================
# SCENARIO S6: AST CLAUSE TREE HIERARCHY TRAVERSAL
# =====================================================================

def test_scenario_s6_ast_clause_tree_hierarchy_traversal(
    clauses_ast_data: List[dict], qcvn_md_parsed: MarkdownParsedBundle
):
    """S6: Validating hierarchical tree traversal from Chapter 1 down to leaf subclauses."""
    assert len(clauses_ast_data) >= 183, f"Expected >= 183 nodes in AST, found {len(clauses_ast_data)}"

    # Traverse Chapter 1 -> Section 1.4 -> Definition
    sec_1_4 = [c for c in clauses_ast_data if c["clause_id"] == "muc-1-4" or "1.4" in c["title"]]
    assert len(sec_1_4) > 0, "Section 1.4 not found in AST"

    # Verify line text slice
    node = sec_1_4[0]
    l_start = node["line_start"]
    l_end = node["line_end"]
    assert 1 <= l_start <= l_end <= len(qcvn_md_parsed.raw_lines)

# =====================================================================
# SCENARIO S7: FOOTNOTE REGULATORY INTERPRETATION
# =====================================================================

def test_scenario_s7_footnote_regulatory_interpretation(
    json_tables_map: Dict[str, dict], qcvn_md_parsed: MarkdownParsedBundle
):
    """S7: Querying special conditions and exceptions specified in technical table footnotes."""
    # Find tables with footnotes
    tables_with_fn = [d for d in json_tables_map.values() if len(d.get("footnotes", [])) > 0]
    assert len(tables_with_fn) >= 10, f"Expected >= 10 tables with footnotes, found {len(tables_with_fn)}"

    # Verify footnotes contain regulatory conditions
    for t_data in tables_with_fn[:5]:
        fn_list = t_data.get("footnotes", [])
        for fn in fn_list:
            assert len(fn) > 10, f"Footnote too short in {t_data.get('title')}: '{fn}'"

# =====================================================================
# SCENARIO S8: FULL OKF SPOKE & REGISTRY VERIFICATION GATE
# =====================================================================

def test_scenario_s8_full_okf_spoke_validation_gate(repo_root: Path):
    """S8: Complete automated gate execution via validate_legal_spoke.py and verify_knowledge_integrity.py."""
    # 1. Execute validate_legal_spoke.py
    v_spoke = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "validate_legal_spoke.py")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(repo_root),
    )
    assert v_spoke.returncode == 0, f"validate_legal_spoke failed:\n{v_spoke.stdout}\n{v_spoke.stderr}"

    # 2. Execute verify_knowledge_integrity.py
    v_integrity = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "verify_knowledge_integrity.py")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(repo_root),
    )
    assert v_integrity.returncode == 0, f"verify_knowledge_integrity failed:\n{v_integrity.stdout}\n{v_integrity.stderr}"
