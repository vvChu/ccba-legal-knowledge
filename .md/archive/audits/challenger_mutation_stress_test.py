"""Challenger 1 Empirical Mutation Testing & Stress Performance Harness.

Evaluates:
1. Sensitivity & discriminative power across all 4 tiers (M1: Table cell, M2: Text/Headings, M3: Anchors/Links, M4: AST/QA).
2. Detection rate (Killed mutants / Total mutants).
3. Stress testing under load and execution profiling.
"""

import copy
import gc
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

# Enforce UTF-8 for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tests.conftest import (
    DocxParsedBundle,
    DocxTableData,
    MarkdownParsedBundle,
    parse_docx_amendment,
    parse_docx_qcvn,
    parse_markdown_amendment,
    parse_markdown_qcvn,
)

# Import test functions from all tiers
import tests.test_tier1_feature_coverage as t1
import tests.test_tier2_boundaries as t2
import tests.test_tier3_cross_features as t3
import tests.test_tier4_real_world as t4

def load_fixtures():
    """Loads and caches all standard test fixtures."""
    extracted_dir = REPO_ROOT / ".md" / "extracted_docs" / "qcvn_06_2022_bxd"
    bundle_dir = REPO_ROOT / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"

    docx_qcvn_path = extracted_dir / "qcvn_06_2022_bxd.docx"
    docx_sd1_path = extracted_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.docx"
    md_qcvn_path = bundle_dir / "qcvn_06_2022_bxd.md"
    md_sd1_path = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"

    qcvn_docx_parsed = parse_docx_qcvn(docx_qcvn_path)
    sd1_docx_parsed = parse_docx_amendment(docx_sd1_path)
    qcvn_md_parsed = parse_markdown_qcvn(md_qcvn_path)
    sd1_md_parsed = parse_markdown_amendment(md_sd1_path)

    # JSON tables map
    json_tables_map = {}
    for jf in (bundle_dir / "tables" / "json").glob("*.json"):
        with open(jf, "r", encoding="utf-8") as f:
            data = json.load(f)
            json_tables_map[jf.stem] = data
            if "table_id" in data:
                json_tables_map[data["table_id"]] = data

    # CSV tables map
    import csv
    csv_tables_map = {}
    for cf in (bundle_dir / "tables" / "csv").glob("*.csv"):
        with open(cf, "r", encoding="utf-8") as f:
            csv_tables_map[cf.stem] = list(csv.reader(f))

    # Clauses AST
    clauses_ast_data = []
    if (bundle_dir / "clauses.json").exists():
        with open(bundle_dir / "clauses.json", "r", encoding="utf-8") as f:
            clauses_ast_data = json.load(f)

    # QA Benchmark
    qa_benchmark_data = []
    if (bundle_dir / "qa_benchmark.json").exists():
        with open(bundle_dir / "qa_benchmark.json", "r", encoding="utf-8") as f:
            qa_benchmark_data = json.load(f)

    # Legal Registry
    import yaml
    legal_registry_data = {}
    if (REPO_ROOT / "legal_registry.yaml").exists():
        with open(REPO_ROOT / "legal_registry.yaml", "r", encoding="utf-8") as f:
            legal_registry_data = yaml.safe_load(f)

    return {
        "repo_root": REPO_ROOT,
        "qcvn_bundle_dir": bundle_dir,
        "qcvn_docx_parsed": qcvn_docx_parsed,
        "sd1_docx_parsed": sd1_docx_parsed,
        "qcvn_md_parsed": qcvn_md_parsed,
        "sd1_md_parsed": sd1_md_parsed,
        "json_tables_map": json_tables_map,
        "csv_tables_map": csv_tables_map,
        "clauses_ast_data": clauses_ast_data,
        "qa_benchmark_data": qa_benchmark_data,
        "legal_registry_data": legal_registry_data,
        "md_sd1_path": md_sd1_path,
    }

def run_mutation_trial(name: str, category: str, test_fn: Callable, args: tuple, expect_fail: bool = True) -> Dict[str, Any]:
    """Runs a single test assertion against mutated fixture data."""
    try:
        test_fn(*args)
        passed = True
        err = None
    except AssertionError as e:
        passed = False
        err = str(e)
    except Exception as e:
        passed = False
        err = f"Unexpected {type(e).__name__}: {e}"

    killed = not passed if expect_fail else passed

    return {
        "name": name,
        "category": category,
        "expect_fail": expect_fail,
        "actual_passed": passed,
        "killed": killed,
        "error_message": err[:200] if err else "",
    }

def run_all_mutation_tests(fixtures: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generates and executes adversarial mutations across 4 tiers."""
    trials: List[Dict[str, Any]] = []

    # =========================================================================
    # CATEGORY 1: TABLE CELL & VALUE MUTATIONS (M1)
    # =========================================================================

    # M1.1: Mutate Bảng 1 fire rating REI 150 -> REI 999
    mutated_tables = copy.deepcopy(fixtures["json_tables_map"])
    for k, v in mutated_tables.items():
        if "bang_01" in k or "bang_1" in k:
            v["rows"] = [{"col1": "Tường ngăn cháy loại 1", "col2": "REI 999"}]
    trials.append(run_mutation_trial(
        "M1.1: Mutate Bảng 1 cell rating to REI 999",
        "Table Cell Mutations",
        t2.test_b2_10_table_1_boundary,
        (mutated_tables,),
    ))

    # M1.2: Mutate Bảng 1 in Scenario S1 RAG Query
    trials.append(run_mutation_trial(
        "M1.2: Mutate Bảng 1 REI 150 -> S1 Scenario RAG Failure",
        "Table Cell Mutations",
        t4.test_scenario_s1_fire_compartment_rag_query,
        (fixtures["qcvn_md_parsed"], mutated_tables),
    ))

    # M1.3: Inject Markdown pipe artifact into JSON table headers
    mutated_tables_pipe = copy.deepcopy(fixtures["json_tables_map"])
    for k, v in mutated_tables_pipe.items():
        v["headers"] = ["| Cột 1 |", "| Cột 2 |"]
        break
    trials.append(run_mutation_trial(
        "M1.3: Inject pipe artifact '| Col |' into JSON headers",
        "Table Cell Mutations",
        t1.test_f5_01_json_headers_is_list_of_strings,
        (mutated_tables_pipe,),
    ))

    # M1.4: Inject delimiter separator row into JSON rows
    mutated_tables_sep = copy.deepcopy(fixtures["json_tables_map"])
    for k, v in mutated_tables_sep.items():
        v["rows"].append({"col1": "--- | ---", "col2": "---"})
        break
    trials.append(run_mutation_trial(
        "M1.4: Inject delimiter row '--- | ---' into JSON data rows",
        "Table Cell Mutations",
        t1.test_f5_02_json_no_separator_row_in_rows,
        (mutated_tables_sep,),
    ))

    # M1.5: Delete all rows from smallest table C.1
    mutated_tables_c1 = copy.deepcopy(fixtures["json_tables_map"])
    for k, v in mutated_tables_c1.items():
        if "bang_c_1" in k:
            v["rows"] = []
    trials.append(run_mutation_trial(
        "M1.5: Truncate smallest table C.1 to 0 rows",
        "Table Cell Mutations",
        t2.test_b2_01_smallest_table_c1,
        (mutated_tables_c1,),
    ))

    # M1.6: Truncate Bảng 9 headers to 3 columns
    mutated_tables_b9 = copy.deepcopy(fixtures["json_tables_map"])
    for k, v in mutated_tables_b9.items():
        if "bang_09" in k or "bang_9" in k:
            v["headers"] = ["Col1", "Col2", "Col3"]
    trials.append(run_mutation_trial(
        "M1.6: Truncate widest table 9 headers to 3 cols",
        "Table Cell Mutations",
        t2.test_b2_04_widest_table_9,
        (mutated_tables_b9,),
    ))

    # M1.7: Mutate Table ID slug to invalid format (e.g., 'table_invalid_01')
    mutated_tables_slug = copy.deepcopy(fixtures["json_tables_map"])
    for k, v in mutated_tables_slug.items():
        v["table_id"] = "TABLE-INVALID-SLUG"
        break
    trials.append(run_mutation_trial(
        "M1.7: Violate table ID slug format",
        "Table Cell Mutations",
        t1.test_f4_10_table_id_naming_convention,
        (mutated_tables_slug,),
    ))

    # M1.8: Inject unescaped CRLF into table cell values
    mutated_tables_crlf = copy.deepcopy(fixtures["json_tables_map"])
    for k, v in mutated_tables_crlf.items():
        v["rows"] = [{"col1": "line1\r\nline2"}]
        break
    trials.append(run_mutation_trial(
        "M1.8: Inject raw CRLF into table cell values",
        "Table Cell Mutations",
        t2.test_b2_23_table_rows_no_raw_newlines,
        (mutated_tables_crlf,),
    ))

    # =========================================================================
    # CATEGORY 2: TEXT & PARAGRAPH MUTATIONS (M2)
    # =========================================================================

    # M2.1: Delete Section 1.1 from Markdown parsed normalized text
    mutated_md_1_1 = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_1_1.headings = [(lvl, text, line) for lvl, text, line in mutated_md_1_1.headings if "1.1" not in text]
    trials.append(run_mutation_trial(
        "M2.1: Delete first section 1.1 from Markdown headings",
        "Text & Paragraph Mutations",
        t2.test_b1_01_first_heading_boundary,
        (mutated_md_1_1,),
    ))

    # M2.2: Inject synthetic dot-split heading '### 1.4.1.7 Khái niệm'
    mutated_md_dot = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_dot.headings.append((3, "1.4.1.7 Khái niệm gian phòng", 100))
    trials.append(run_mutation_trial(
        "M2.2: Inject dot-split heading 1.4.1.7 into MD",
        "Text & Paragraph Mutations",
        t1.test_f2_01_no_dot_split_anomalies,
        (mutated_md_dot,),
    ))

    # M2.3: Inject space-separated heading '### 4 15 Khoảng cách'
    mutated_md_space = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_space.headings.append((3, "4 15 Khoảng cách", 200))
    trials.append(run_mutation_trial(
        "M2.3: Inject space-separated heading '4 15' into MD",
        "Text & Paragraph Mutations",
        t1.test_f2_02_no_space_separated_chapter4_headings,
        (mutated_md_space,),
    ))

    # M2.4: Inject corrupted subdot heading '2.1.11'
    mutated_md_subdot = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_subdot.headings.append((3, "2.1.11 Quy định bậc chịu lửa", 300))
    trials.append(run_mutation_trial(
        "M2.4: Inject corrupted subdot heading '2.1.11' into MD",
        "Text & Paragraph Mutations",
        t1.test_f2_04_no_missing_subdot_anomalies,
        (mutated_md_subdot,),
    ))

    # M2.5: Inject synthetic fake residual heading '### 24 0'
    mutated_md_fake = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_fake.headings.append((3, "24 0", 400))
    trials.append(run_mutation_trial(
        "M2.5: Inject fake residual heading '24 0' into MD",
        "Text & Paragraph Mutations",
        t1.test_f2_05_no_table_residual_fake_headings,
        (mutated_md_fake,),
    ))

    # M2.6: Inject 'LOREM IPSUM' placeholder text into Markdown
    mutated_md_placeholder = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_placeholder.raw_text += "\n\nLOREM IPSUM DOLOR SIT AMET\n"
    trials.append(run_mutation_trial(
        "M2.6: Inject synthetic 'LOREM IPSUM' placeholder into MD",
        "Text & Paragraph Mutations",
        t1.test_f16_02_no_synthetic_placeholder_text,
        (mutated_md_placeholder,),
    ))

    # M2.7: Inject zero-width space into heading
    mutated_md_zwsp = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_zwsp.headings = [(3, "1.1\u200b Phạm vi điều chỉnh", 50)]
    trials.append(run_mutation_trial(
        "M2.7: Inject zero-width space '\\u200b' into heading",
        "Text & Paragraph Mutations",
        t2.test_b3_11_no_zero_width_space_corruption,
        (mutated_md_zwsp,),
    ))

    # M2.8: Remove H1 document title (leaving 0 H1 headings)
    mutated_md_noh1 = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_noh1.headings = [(lvl, t, l) for lvl, t, l in mutated_md_noh1.headings if lvl != 1]
    trials.append(run_mutation_trial(
        "M2.8: Remove H1 document title",
        "Text & Paragraph Mutations",
        t1.test_f3_01_document_title_h1,
        (mutated_md_noh1,),
    ))

    # =========================================================================
    # CATEGORY 3: ANCHOR TAG & CROSS-LINK MUTATIONS (M3)
    # =========================================================================

    # M3.1: Clear all anchors in Markdown parsed bundle (< 183 anchors)
    mutated_md_anchors = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_anchors.anchors = set()
    trials.append(run_mutation_trial(
        "M3.1: Purge all anchors from Markdown (0 anchors)",
        "Anchor & Cross-link Mutations",
        t1.test_f3_06_heading_anchor_correspondence,
        (mutated_md_anchors,),
    ))

    # M3.2: Mutate SD1 cross-link target to broken non-existent anchor
    mutated_sd1_links = copy.deepcopy(fixtures["sd1_md_parsed"])
    mutated_sd1_links["cross_links"] = [("Điểm 1.1.2", "qcvn_06_2022_bxd.md#muc-non-existent-anchor-999")]
    trials.append(run_mutation_trial(
        "M3.2: Mutate SD1 cross-link to non-existent target anchor",
        "Anchor & Cross-link Mutations",
        t1.test_f11_03_sd1_hyperlink_targets_exist_in_base,
        (mutated_sd1_links, fixtures["qcvn_md_parsed"]),
    ))

    # M3.3: Mutate SD1 cross-link in Scenario S5 Navigation
    trials.append(run_mutation_trial(
        "M3.3: Mutate SD1 cross-link -> S5 Scenario Navigation Failure",
        "Anchor & Cross-link Mutations",
        t4.test_scenario_s5_bidirectional_cross_reference_navigation,
        (mutated_sd1_links, fixtures["qcvn_md_parsed"]),
    ))

    # M3.4: Inject placeholder anchor 'chuong_pl_name' into SD1
    mutated_sd1_ph = copy.deepcopy(fixtures["sd1_md_parsed"])
    mutated_sd1_ph["anchors"].add("chuong_pl_name")
    trials.append(run_mutation_trial(
        "M3.4: Inject placeholder anchor 'chuong_pl_name' into SD1",
        "Anchor & Cross-link Mutations",
        t1.test_f11_04_sd1_no_generic_placeholder_anchors,
        (mutated_sd1_ph,),
    ))

    # M3.5: Mutate SD1 anchor format to non-kebab uppercase ('SD1_MUC_1_1')
    mutated_sd1_upper = copy.deepcopy(fixtures["sd1_md_parsed"])
    mutated_sd1_upper["anchors"] = {"SD1_MUC_1_1_UPPER"}
    trials.append(run_mutation_trial(
        "M3.5: Violate SD1 anchor lowercase kebab format",
        "Anchor & Cross-link Mutations",
        t1.test_f11_06_sd1_anchor_format_standard,
        (mutated_sd1_upper,),
    ))

    # M3.6: Delete anchor 'sd1-bang-10' from SD1 in Scenario S4
    mutated_sd1_no_t10 = copy.deepcopy(fixtures["sd1_md_parsed"])
    mutated_sd1_no_t10["anchors"] = {a for a in mutated_sd1_no_t10.get("anchors", set()) if a != "sd1-bang-10"}
    trials.append(run_mutation_trial(
        "M3.6: Remove 'sd1-bang-10' anchor -> S4 Water Flow Override Failure",
        "Anchor & Cross-link Mutations",
        t4.test_scenario_s4_amendment_water_flow_override,
        (mutated_sd1_no_t10, fixtures["qcvn_docx_parsed"]),
    ))

    # M3.7: Cause anchor collision between AST clause and table anchor ('bang-01')
    mutated_clauses_collision = copy.deepcopy(fixtures["clauses_ast_data"])
    if mutated_clauses_collision:
        mutated_clauses_collision[0]["anchor"] = "bang-01"
    mutated_md_table_anchor = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_table_anchor.anchors.add("bang-01")
    trials.append(run_mutation_trial(
        "M3.7: Inject anchor collision between AST and Table",
        "Anchor & Cross-link Mutations",
        t3.test_pair_07_table_anchors_non_interference_with_ast,
        (mutated_md_table_anchor, mutated_clauses_collision),
    ))

    # =========================================================================
    # CATEGORY 4: AST CLAUSE TREE & QA BENCHMARK MUTATIONS (M4)
    # =========================================================================

    # M4.1: Invert line range in first AST clause (line_start=5000, line_end=100)
    mutated_clauses_inv = copy.deepcopy(fixtures["clauses_ast_data"])
    if mutated_clauses_inv:
        mutated_clauses_inv[0]["line_start"] = 5000
        mutated_clauses_inv[0]["line_end"] = 100
    trials.append(run_mutation_trial(
        "M4.1: Invert line range (line_start > line_end) in clauses.json",
        "AST & QA Benchmark Mutations",
        t2.test_b5_04_ast_no_inverted_ranges,
        (mutated_clauses_inv,),
    ))

    # M4.2: Break monotonic ordering in clauses.json
    mutated_clauses_order = copy.deepcopy(fixtures["clauses_ast_data"])
    if len(mutated_clauses_order) > 1:
        mutated_clauses_order[0]["line_start"] = 9999
        mutated_clauses_order[0]["line_end"] = 10000
    trials.append(run_mutation_trial(
        "M4.2: Violate monotonic line_start ordering in clauses.json",
        "AST & QA Benchmark Mutations",
        t1.test_f12_04_clauses_monotonic_line_ordering,
        (mutated_clauses_order,),
    ))

    # M4.3: Inject duplicate clause ID into clauses.json
    mutated_clauses_dup = copy.deepcopy(fixtures["clauses_ast_data"])
    if mutated_clauses_dup:
        mutated_clauses_dup.append(copy.deepcopy(mutated_clauses_dup[0]))
    trials.append(run_mutation_trial(
        "M4.3: Inject duplicate clause_id into clauses.json",
        "AST & QA Benchmark Mutations",
        t2.test_b5_05_ast_unique_clause_ids,
        (mutated_clauses_dup,),
    ))

    # M4.4: Mutate QA benchmark anchor to an unmapped anchor not in clauses.json
    mutated_qa_unmapped = copy.deepcopy(fixtures["qa_benchmark_data"])
    if mutated_qa_unmapped:
        mutated_qa_unmapped[0]["anchor"] = "unmapped_foreign_anchor_xyz"
    trials.append(run_mutation_trial(
        "M4.4: Mutate QA anchor to unmapped value -> QA sync failure",
        "AST & QA Benchmark Mutations",
        t1.test_f13_03_qa_anchors_match_clauses_json,
        (mutated_qa_unmapped, fixtures["clauses_ast_data"]),
    ))

    # M4.5: Mutate QA benchmark anchor -> Tier 3 Pair 12 Bijection Failure
    trials.append(run_mutation_trial(
        "M4.5: Mutate QA anchor -> Pair 12 Bijection Failure",
        "AST & QA Benchmark Mutations",
        t3.test_pair_12_ast_clauses_to_qa_benchmark_bijection,
        (fixtures["clauses_ast_data"], mutated_qa_unmapped),
    ))

    # M4.6: Inject duplicate question into QA benchmark
    mutated_qa_dup = copy.deepcopy(fixtures["qa_benchmark_data"])
    if len(mutated_qa_dup) > 1:
        mutated_qa_dup[1]["question"] = mutated_qa_dup[0]["question"]
    trials.append(run_mutation_trial(
        "M4.6: Inject duplicate question into qa_benchmark.json",
        "AST & QA Benchmark Mutations",
        t2.test_b5_22_qa_question_uniqueness,
        (mutated_qa_dup,),
    ))

    # M4.7: Empty question in QA benchmark
    mutated_qa_empty = copy.deepcopy(fixtures["qa_benchmark_data"])
    if mutated_qa_empty:
        mutated_qa_empty[0]["question"] = "   "
    trials.append(run_mutation_trial(
        "M4.7: Empty question in QA benchmark",
        "AST & QA Benchmark Mutations",
        t1.test_f13_06_qa_questions_and_answers_non_empty,
        (mutated_qa_empty,),
    ))

    # M4.8: Short answer (< 15 chars) in QA benchmark
    mutated_qa_short = copy.deepcopy(fixtures["qa_benchmark_data"])
    if mutated_qa_short:
        mutated_qa_short[0]["answer"] = "Short."
    trials.append(run_mutation_trial(
        "M4.8: Short answer (< 15 chars) in QA benchmark",
        "AST & QA Benchmark Mutations",
        t2.test_b5_19_qa_answer_length_bounds,
        (mutated_qa_short,),
    ))

    # =========================================================================
    # CATEGORY 5: VACUOUS / WEAK ASSERTION PROBING (M5)
    # =========================================================================

    # M5.1: Inject unbalanced quotation mark into test_b3_13_quotation_marks_consistency
    mutated_md_quotes = copy.deepcopy(fixtures["qcvn_md_parsed"])
    mutated_md_quotes.raw_text = 'This is an "unbalanced quote'
    trials.append(run_mutation_trial(
        "M5.1: Weak Assertion Probe - Unbalanced quotes in test_b3_13",
        "Vacuous & Weak Assertion Detection",
        t2.test_b3_13_quotation_marks_consistency,
        (mutated_md_quotes,),
        expect_fail=True,
    ))

    # M5.2: Remove definition 1.4.72 in test_b5_17_ast_definition_1_4_72_bounds
    mutated_clauses_no_72 = [c for c in fixtures["clauses_ast_data"] if "1-4-72" not in c["clause_id"] and "1-4-7-2" not in c["clause_id"]]
    trials.append(run_mutation_trial(
        "M5.2: Weak Assertion Probe - Missing definition 1.4.72 in test_b5_17",
        "Vacuous & Weak Assertion Detection",
        t2.test_b5_17_ast_definition_1_4_72_bounds,
        (mutated_clauses_no_72,),
        expect_fail=True,
    ))

    # M5.3: Set last QA anchor to invalid string in test_b5_21_qa_last_node_mapping
    mutated_qa_last_bad = copy.deepcopy(fixtures["qa_benchmark_data"])
    if mutated_qa_last_bad:
        mutated_qa_last_bad[-1]["anchor"] = "invalid_middle_anchor_no_chapter7"
    trials.append(run_mutation_trial(
        "M5.3: Weak Assertion Probe - Bad last QA anchor in test_b5_21",
        "Vacuous & Weak Assertion Detection",
        t2.test_b5_21_qa_last_node_mapping,
        (mutated_qa_last_bad,),
        expect_fail=True,
    ))

    # M5.4: Delete 1 table from json_tables_map (reducing count to 63)
    mutated_tables_63 = copy.deepcopy(fixtures["json_tables_map"])
    # Remove one table key
    for k in list(mutated_tables_63.keys()):
        if "bang_01" in k:
            del mutated_tables_63[k]
    trials.append(run_mutation_trial(
        "M5.4: Delete table 1 from JSON table map",
        "Table Cell Mutations",
        t1.test_f4_02_core_tables_1_to_16_exist,
        (mutated_tables_63,),
    ))

    # M5.5: Mutate SD1 replacement Table 10 numeric values (change "10", "15", "20", "30" to "999")
    mutated_sd1_t10_vals = copy.deepcopy(fixtures["sd1_md_parsed"])
    mutated_sd1_t10_vals["raw_text"] = "No numbers here"
    trials.append(run_mutation_trial(
        "M5.5: Mutate SD1 Table 10 numeric flow rates",
        "Table Cell Mutations",
        t1.test_f10_04_sd1_table_10_cell_values_exact,
        (mutated_sd1_t10_vals,),
    ))

    return trials

def run_performance_stress_test(fixtures: Dict[str, Any], iterations: int = 5) -> Dict[str, Any]:
    start_total = time.time()

    # 1. Benchmark DOCX & Markdown parsing speeds
    extracted_dir = REPO_ROOT / ".md" / "extracted_docs" / "qcvn_06_2022_bxd"
    bundle_dir = REPO_ROOT / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
    docx_qcvn_path = extracted_dir / "qcvn_06_2022_bxd.docx"
    md_qcvn_path = bundle_dir / "qcvn_06_2022_bxd.md"

    parse_docx_times = []
    parse_md_times = []

    for _ in range(iterations):
        t0 = time.time()
        _ = parse_docx_qcvn(docx_qcvn_path)
        parse_docx_times.append(time.time() - t0)

        t0 = time.time()
        _ = parse_markdown_qcvn(md_qcvn_path)
        parse_md_times.append(time.time() - t0)

    # 2. Benchmark memory assertion loops (in-memory fixture evaluations)
    in_memory_assertion_times = []
    passing_test_functions = [
        (t1.test_f4_01_table_count_equals_64, (fixtures["json_tables_map"], fixtures["qcvn_bundle_dir"])),
        (t1.test_f5_01_json_headers_is_list_of_strings, (fixtures["json_tables_map"],)),
        (t1.test_f12_01_clauses_json_exists_and_valid, (fixtures["clauses_ast_data"],)),
        (t1.test_f13_01_qa_benchmark_exists_and_valid, (fixtures["qa_benchmark_data"],)),
        (t2.test_b1_01_first_heading_boundary, (fixtures["qcvn_md_parsed"],)),
        (t2.test_b2_09_table_numeric_sorting, (fixtures["json_tables_map"],)),
        (t2.test_b3_10_vietnamese_diacritics_normalization, (fixtures["qcvn_md_parsed"],)),
        (t2.test_b5_05_ast_unique_clause_ids, (fixtures["clauses_ast_data"],)),
        (t2.test_b5_22_qa_question_uniqueness, (fixtures["qa_benchmark_data"],)),
        (t3.test_pair_07_table_anchors_non_interference_with_ast, (fixtures["qcvn_md_parsed"], fixtures["clauses_ast_data"])),
        (t3.test_pair_12_ast_clauses_to_qa_benchmark_bijection, (fixtures["clauses_ast_data"], fixtures["qa_benchmark_data"])),
    ]

    for _ in range(iterations):
        t0 = time.time()
        for fn, args in passing_test_functions:
            try:
                fn(*args)
            except Exception:
                pass
        in_memory_assertion_times.append(time.time() - t0)

    total_time = time.time() - start_total

    return {
        "iterations": iterations,
        "avg_docx_parse_sec": round(sum(parse_docx_times) / len(parse_docx_times), 4),
        "min_docx_parse_sec": round(min(parse_docx_times), 4),
        "max_docx_parse_sec": round(max(parse_docx_times), 4),
        "avg_md_parse_sec": round(sum(parse_md_times) / len(parse_md_times), 4),
        "min_md_parse_sec": round(min(parse_md_times), 4),
        "max_md_parse_sec": round(max(parse_md_times), 4),
        "avg_in_memory_assertion_batch_sec": round(sum(in_memory_assertion_times) / len(in_memory_assertion_times), 6),
        "total_benchmark_time_sec": round(total_time, 3),
    }

def main():
    print("=" * 72)
    print("      CHALLENGER 1: EMPIRICAL MUTATION & STRESS TEST HARNESS")
    print("=" * 72)

    print("\n[STEP 1] Loading and caching official fixtures...")
    t0 = time.time()
    fixtures = load_fixtures()
    print(f"-> Loaded in {time.time() - t0:.3f}s")
    print(f"-> DOCX paras: {len(fixtures['qcvn_docx_parsed'].raw_paragraphs)}, Tables: {len(fixtures['qcvn_docx_parsed'].tables)}")
    print(f"-> MD lines: {len(fixtures['qcvn_md_parsed'].raw_lines)}, Anchors: {len(fixtures['qcvn_md_parsed'].anchors)}")

    print("\n[STEP 2] Executing 29 Adversarial Mutation Trials across 4 Categories...")
    trials = run_all_mutation_tests(fixtures)

    killed_count = sum(1 for t in trials if t["killed"])
    total_mutants = len(trials)
    mutation_score = (killed_count / total_mutants) * 100

    print("\n" + "-" * 72)
    print(f"MUTATION TRIAL SUMMARY: {killed_count}/{total_mutants} KILLED ({mutation_score:.1f}%)")
    print("-" * 72)

    categories = sorted(list({t["category"] for t in trials}))
    for cat in categories:
        cat_trials = [t for t in trials if t["category"] == cat]
        cat_killed = sum(1 for t in cat_trials if t["killed"])
        print(f"\n### {cat} ({cat_killed}/{len(cat_trials)} killed)")
        for t in cat_trials:
            status_str = "[KILLED]" if t["killed"] else "[SURVIVED - CRITICAL BUG]"
            print(f"  {status_str} {t['name']}")
            if not t["killed"]:
                print(f"    WARNING: Mutation survived! Test did not fail as expected.")
            elif t["error_message"]:
                safe_err = t['error_message'][:90].encode("ascii", errors="replace").decode("ascii")
                print(f"    Expected Failure Triggered: {safe_err}...")

    print("\n[STEP 3] Running Performance Stress Benchmarking (5 iterations)...")
    perf_metrics = run_performance_stress_test(fixtures, iterations=5)
    print(f"-> Avg DOCX Parse Time : {perf_metrics['avg_docx_parse_sec']}s (range: {perf_metrics['min_docx_parse_sec']}s - {perf_metrics['max_docx_parse_sec']}s)")
    print(f"-> Avg MD Parse Time   : {perf_metrics['avg_md_parse_sec']}s (range: {perf_metrics['min_md_parse_sec']}s - {perf_metrics['max_md_parse_sec']}s)")
    print(f"-> Avg Assertion Batch : {perf_metrics['avg_in_memory_assertion_batch_sec']*1000:.3f}ms per 12 assertions")
    print(f"-> Total Benchmark Time: {perf_metrics['total_benchmark_time_sec']}s")

    # Export Mutation Results Artifact
    output_file = REPO_ROOT / ".md" / "challenger_mutation_report.json"
    report_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_mutants": total_mutants,
        "killed_mutants": killed_count,
        "survived_mutants": total_mutants - killed_count,
        "mutation_score_pct": mutation_score,
        "performance_metrics": perf_metrics,
        "trials": trials,
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    print(f"\n[ARTIFACT] Saved mutation test report to {output_file}")

    print("\n" + "=" * 72)
    if mutation_score == 100.0:
        print("      VERDICT: 100% DISCRIMINATIVE SENSITIVITY CONFIRMED (APPROVE)")
    else:
        print("      VERDICT: DEFECTS DETECTED IN TEST SUITE (REQUEST_CHANGES)")
    print("=" * 72)

    return 0 if mutation_score == 100.0 else 1

if __name__ == "__main__":
    sys.exit(main())
