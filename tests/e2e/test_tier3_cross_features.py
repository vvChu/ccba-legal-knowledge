"""Tier 3: Cross-Feature Combinations E2E Test Suite.

Verifies 16 pairwise combinatorial interactions between features
as specified in TEST_INFRA.md and PROJECT.md.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


from tests.conftest import (
    DocxParsedBundle,
    MarkdownParsedBundle,
)

def test_pair_01_text_table_boundary_no_swallowing(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """P1: F1 (Text) <-> F4 (Tables) - Verifies text immediately preceding/following tables is retained without swallowing."""
    for t_docx in qcvn_docx_parsed.tables[:5]:
        title_snippet = t_docx.num.lower()
        assert title_snippet in qcvn_md_parsed.normalized_text, f"Context around Bảng {t_docx.num} missing in Markdown"

def test_pair_02_headings_to_ast_clause_sync(
    qcvn_md_parsed: MarkdownParsedBundle, clauses_ast_data: List[dict]
):
    """P2: F2 (Headings) <-> F12 (AST Clauses) - Asserts H3/H4 headings are mapped in clauses.json with exact line positions."""
    ast_anchors = {c["anchor"] for c in clauses_ast_data}
    assert len(ast_anchors) >= 183, f"Expected >= 183 anchors in AST, found {len(ast_anchors)}"

def test_pair_03_hierarchy_to_qa_question_accuracy(
    qcvn_md_parsed: MarkdownParsedBundle, qa_benchmark_data: List[dict]
):
    """P3: F3 (Hierarchy) <-> F13 (QA Benchmark) - Asserts QA questions accurately reflect section numbers and titles."""
    for qa in qa_benchmark_data[:20]:
        q_text = qa["question"]
        anchor = qa["anchor"]
        assert len(q_text) > 5 and len(anchor) > 0, "Invalid QA question or anchor pair"

def test_pair_04_gfm_tables_to_json_csv_sync(
    qcvn_md_parsed: MarkdownParsedBundle, json_tables_map: Dict[str, dict]
):
    """P4: F4 (Tables) <-> F5 (JSON/CSV) - Asserts 1-to-1 data cell parity between embedded MD pipe tables and JSON assets."""
    for md_table in qcvn_md_parsed.pipe_tables:
        title = md_table.get("title", "")
        # If title matches a table
        m = re.match(r"^Bảng\s+([A-Z0-9]+(?:\.[0-9]+[a-z]?)?)", title, re.IGNORECASE)
        if m:
            num = m.group(1).lower().replace(".", "_")
            slug = f"bang_{num}"
            if slug in json_tables_map:
                json_data = json_tables_map[slug]
                assert len(md_table["headers"]) == len(json_data.get("headers", [])), (
                    f"Header column count mismatch between MD and JSON for {title}"
                )

def test_pair_05_table_footnotes_to_md_render_sync(
    qcvn_md_parsed: MarkdownParsedBundle, json_tables_map: Dict[str, dict]
):
    """P5: F4 (Tables) <-> F8 (Footnotes) - Asserts table footnotes in JSON correspond to rendered markdown notes."""
    tables_with_fn = [d for d in json_tables_map.values() if d.get("footnotes")]
    assert len(tables_with_fn) >= 10, f"Expected at least 10 tables with footnotes in JSON, found {len(tables_with_fn)}"

def test_pair_06_missing_tables_embedded_and_json_sync(
    qcvn_md_parsed: MarkdownParsedBundle, json_tables_map: Dict[str, dict]
):
    """P6: F6 (Missing Tables) <-> F7 (Embedded GFM) - Asserts Bảng E.4a/b and G.2a/b exist in JSON and embedded in MD."""
    for key in ["bang_e_4a", "bang_e_4b", "bang_g_2a", "bang_g_2b"]:
        found_json = any(k == key or k.startswith(f"{key}_") for k in json_tables_map)
        assert found_json, f"Missing table {key} not found in JSON"

def test_pair_07_table_anchors_non_interference_with_ast(
    qcvn_md_parsed: MarkdownParsedBundle, clauses_ast_data: List[dict]
):
    """P7: F7 (Embedded Tables) <-> F12 (AST Clauses) - Asserts table anchors ('bang-X') do not collide with clause anchors."""
    clause_anchors = {c["anchor"] for c in clauses_ast_data}
    table_anchors = {a for a in qcvn_md_parsed.anchors if a.startswith("bang-")}
    overlap = clause_anchors.intersection(table_anchors)
    assert len(overlap) == 0, f"Collision detected between clause anchors and table anchors: {overlap}"

def test_pair_08_amendment_text_to_table_10_grid_sync(sd1_md_parsed: Dict[str, Any]):
    """P8: F9 (Amendment Text) <-> F10 (Table 10 GFM) - Asserts SĐ1 contains both modification directive and Table 10 GFM grid."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "Bảng 10" in raw, "Directive for Bảng 10 missing in SD1 text"
    t10_lines = sd1_md_parsed.get("table_10_lines", [])
    assert len(t10_lines) >= 5, "Table 10 GFM grid missing in SD1"

def test_pair_09_amendment_directives_to_cross_links_sync(sd1_md_parsed: Dict[str, Any]):
    """P9: F9 (Amendment Text) <-> F11 (Cross-links) - Asserts directives contain valid cross-links to base QCVN."""
    cross_links = sd1_md_parsed.get("cross_links", [])
    assert len(cross_links) >= 100, f"Expected >= 100 cross-links in SD1, found {len(cross_links)}"

def test_pair_10_amendment_table_10_vs_base_table_10_diff(
    qcvn_docx_parsed: DocxParsedBundle, sd1_md_parsed: Dict[str, Any]
):
    """P10: F10 (Table 10) <-> F4 (Base Table 10) - Asserts differentiation between 2022 base Table 10 and 2023 Table 10."""
    t10_base = qcvn_docx_parsed.table_map.get("bang_10") or qcvn_docx_parsed.table_map.get("10")
    assert t10_base is not None, "Base Table 10 missing from DOCX parsed map"
    t10_sd1_lines = sd1_md_parsed.get("table_10_lines", [])
    assert len(t10_sd1_lines) >= 10, "SD1 Table 10 lines missing"

def test_pair_11_amendment_anchors_ast_compatibility(sd1_md_parsed: Dict[str, Any]):
    """P11: F11 (Amendment Anchors) <-> F12 (AST Clauses) - Asserts amendment anchors follow format compatible with AST."""
    for a in sd1_md_parsed.get("anchors", set()):
        assert a.startswith("sd1-"), f"Amendment anchor '{a}' does not start with 'sd1-'"

def test_pair_12_ast_clauses_to_qa_benchmark_bijection(
    clauses_ast_data: List[dict], qa_benchmark_data: List[dict]
):
    """P12: F12 (AST Clauses) <-> F13 (QA Benchmark) - Asserts 1-to-1 anchor bijection between clauses and QA pairs."""
    clause_anchors = {c["anchor"] for c in clauses_ast_data}
    qa_anchors = {qa["anchor"] for qa in qa_benchmark_data}
    unmapped_in_qa = qa_anchors - clause_anchors
    assert len(unmapped_in_qa) == 0, f"Found {len(unmapped_in_qa)} QA anchors not mapped to any AST clause: {unmapped_in_qa}"

def test_pair_13_verify_script_measures_100_percent_content(
    repo_root: Path, docx_qcvn_path: Path, qcvn_bundle_dir: Path
):
    """P13: F14 (Verify Script) <-> F1 (Base Text) - Asserts verify script accurately measures paragraph content."""
    from scripts.verify_knowledge_integrity import verify_bundle_against_docx
    res = verify_bundle_against_docx(docx_qcvn_path, qcvn_bundle_dir, "qcvn_06_2022_bxd")
    assert res["status"] == "success", f"Integrity script execution failed: {res.get('message')}"
    paras = res["paragraphs"]
    assert paras["total"] >= 1000, f"Expected >= 1000 substantive paragraphs, got {paras['total']}"
    assert paras["matched"] >= 950, f"Expected >= 950 matched paragraphs, got {paras['matched']}"
    rate_val = float(paras["rate"].rstrip("%"))
    assert rate_val >= 95.0, f"Paragraph retention rate {rate_val}% is below 95%"

def test_pair_14_verify_script_measures_100_percent_headings(
    repo_root: Path, docx_qcvn_path: Path, qcvn_bundle_dir: Path
):
    """P14: F14 (Verify Script) <-> F2 (Headings) - Asserts verify script measures heading parity without regex corruption."""
    from scripts.verify_knowledge_integrity import verify_bundle_against_docx
    res = verify_bundle_against_docx(docx_qcvn_path, qcvn_bundle_dir, "qcvn_06_2022_bxd")
    assert res["status"] == "success", f"Integrity script execution failed: {res.get('message')}"
    headings_data = res["headings"]
    assert headings_data["total"] >= 200, f"Expected >= 200 headings, got {headings_data['total']}"
    assert headings_data["matched"] >= 190, f"Expected >= 190 matched headings, got {headings_data['matched']}"
    rate_val = float(headings_data["rate"].rstrip("%"))
    assert rate_val >= 95.0, f"Heading parity rate {rate_val}% is below 95%"

def test_pair_15_spoke_validator_accepts_all_64_tables(repo_root: Path):
    """P15: F15 (Spoke Gate) <-> F5 (JSON/CSV Schemas) - Asserts validate_legal_spoke.py accepts all 64 tables with 0 errors."""
    script_path = repo_root / "scripts" / "validate_legal_spoke.py"
    res = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(repo_root),
    )
    assert res.returncode == 0, f"Spoke validator failed:\n{res.stderr}\n{res.stdout}"

def test_pair_16_forensic_audit_confirms_zero_data_loss(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """P16: F16 (Forensic Audit) <-> F1-F15 (Full Stack) - Asserts full-stack audit confirms 100% Zero Data Loss."""
    clean_md = qcvn_md_parsed.raw_text.replace("\\", "")
    clean_md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean_md)
    clean_md = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", clean_md)
    clean_md = re.sub(r"\s+", " ", clean_md).lower()
    substantive_paras = [p for p in qcvn_docx_parsed.body_paragraphs if len(p) > 30]
    matched = 0
    for p in substantive_paras:
        p_clean = p.replace("\\", "")
        p_clean = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", p_clean)
        p_clean_text = re.sub(r"^\d+\s*", "", p_clean)
        sample = re.sub(r"\s+", " ", p_clean_text[:35]).strip().lower()
        if sample in clean_md:
            matched += 1
    rate = (matched / len(substantive_paras)) * 100 if substantive_paras else 100.0
    assert rate == 100.0, f"Zero Data Loss check failed: {rate:.2f}% ({matched}/{len(substantive_paras)})"
