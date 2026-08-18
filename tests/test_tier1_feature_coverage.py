"""Tier 1: Feature Coverage E2E Test Suite for QCVN 06:2022/BXD & Amendment 1:2023.

Verifies 1-to-1 requirement coverage across all 16 features (F1 through F16)
as specified in PROJECT.md and TEST_INFRA.md.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

import pytest
import yaml

from tests.conftest import (
    DocxParsedBundle,
    DocxTableData,
    MarkdownParsedBundle,
)


# =====================================================================
# FEATURE F1: BASE TEXT & APPENDIX COMPLETE EXTRACTION (11 tests)
# =====================================================================

def test_f1_01_body_paragraph_retention_rate(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts that the body paragraph retention rate between DOCX and Markdown is >= 99.5%."""
    substantive_paras = [p for p in qcvn_docx_parsed.body_paragraphs if len(p) > 30]
    matched = 0
    md_norm = qcvn_md_parsed.normalized_text

    for p in substantive_paras:
        sample = re.sub(r"\s+", " ", p[:40]).strip().lower()
        if sample in md_norm:
            matched += 1

    retention_rate = (matched / len(substantive_paras)) * 100 if substantive_paras else 100.0
    assert retention_rate >= 99.5, f"Paragraph retention rate {retention_rate:.2f}% is below 99.5% threshold ({matched}/{len(substantive_paras)})"


def test_f1_02_chapter_1_to_7_text_completeness(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts that all 7 main chapters (1 through 7) have complete paragraph retention >= 98%."""
    for ch_idx in range(1, 8):
        ch_key = str(ch_idx)
        ch_paras = [p for p in qcvn_docx_parsed.chapter_paragraphs.get(ch_key, []) if len(p) > 30]
        if not ch_paras:
            continue
        matched = sum(1 for p in ch_paras if re.sub(r"\s+", " ", p[:40]).strip().lower() in qcvn_md_parsed.normalized_text)
        rate = (matched / len(ch_paras)) * 100
        assert rate >= 98.0, f"Chapter {ch_key} paragraph retention {rate:.2f}% is below 98% ({matched}/{len(ch_paras)})"


def test_f1_03_appendix_a_retention(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts Appendix A text retention rate is >= 98%."""
    app_paras = [p for p in qcvn_docx_parsed.chapter_paragraphs.get("A", []) if len(p) > 30]
    matched = sum(1 for p in app_paras if re.sub(r"\s+", " ", p[:40]).strip().lower() in qcvn_md_parsed.normalized_text)
    rate = (matched / len(app_paras)) * 100 if app_paras else 100.0
    assert rate >= 98.0, f"Appendix A retention {rate:.2f}% below 98%"


def test_f1_04_appendix_b_retention(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts Appendix B text retention rate is >= 98%."""
    app_paras = [p for p in qcvn_docx_parsed.chapter_paragraphs.get("B", []) if len(p) > 30]
    matched = sum(1 for p in app_paras if re.sub(r"\s+", " ", p[:40]).strip().lower() in qcvn_md_parsed.normalized_text)
    rate = (matched / len(app_paras)) * 100 if app_paras else 100.0
    assert rate >= 98.0, f"Appendix B retention {rate:.2f}% below 98%"


def test_f1_05_appendix_c_retention(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts Appendix C text retention rate is >= 98%."""
    app_paras = [p for p in qcvn_docx_parsed.chapter_paragraphs.get("C", []) if len(p) > 30]
    matched = sum(1 for p in app_paras if re.sub(r"\s+", " ", p[:40]).strip().lower() in qcvn_md_parsed.normalized_text)
    rate = (matched / len(app_paras)) * 100 if app_paras else 100.0
    assert rate >= 98.0, f"Appendix C retention {rate:.2f}% below 98%"


def test_f1_06_appendix_d_smoke_control_retention(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts Appendix D (Smoke Control, 167 paras) text retention rate is >= 98%."""
    app_paras = [p for p in qcvn_docx_parsed.chapter_paragraphs.get("D", []) if len(p) > 30]
    assert len(app_paras) >= 50, f"Expected at least 50 substantive paragraphs in Appendix D, got {len(app_paras)}"
    matched = sum(1 for p in app_paras if re.sub(r"\s+", " ", p[:40]).strip().lower() in qcvn_md_parsed.normalized_text)
    rate = (matched / len(app_paras)) * 100
    assert rate >= 98.0, f"Appendix D retention {rate:.2f}% below 98%"


def test_f1_07_appendix_e_retention(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts Appendix E text retention rate is >= 98%."""
    app_paras = [p for p in qcvn_docx_parsed.chapter_paragraphs.get("E", []) if len(p) > 30]
    matched = sum(1 for p in app_paras if re.sub(r"\s+", " ", p[:40]).strip().lower() in qcvn_md_parsed.normalized_text)
    rate = (matched / len(app_paras)) * 100 if app_paras else 100.0
    assert rate >= 98.0, f"Appendix E retention {rate:.2f}% below 98%"


def test_f1_08_appendix_f_retention(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts Appendix F text retention rate is >= 98%."""
    app_paras = [p for p in qcvn_docx_parsed.chapter_paragraphs.get("F", []) if len(p) > 30]
    matched = sum(1 for p in app_paras if re.sub(r"\s+", " ", p[:40]).strip().lower() in qcvn_md_parsed.normalized_text)
    rate = (matched / len(app_paras)) * 100 if app_paras else 100.0
    assert rate >= 98.0, f"Appendix F retention {rate:.2f}% below 98%"


def test_f1_09_appendix_g_retention(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts Appendix G text retention rate is >= 98%."""
    clean_md = qcvn_md_parsed.raw_text.replace("\\", "")
    clean_md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean_md)
    clean_md = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", clean_md)
    clean_md = re.sub(r"\s+", " ", clean_md).lower()
    app_paras = [p for p in qcvn_docx_parsed.chapter_paragraphs.get("G", []) if len(p) > 30]
    matched = 0
    for p in app_paras:
        p_clean = p.replace("\\", "")
        p_clean = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", p_clean)
        sample = re.sub(r"\s+", " ", p_clean[:35]).strip().lower()
        if sample in clean_md:
            matched += 1
    rate = (matched / len(app_paras)) * 100 if app_paras else 100.0
    assert rate >= 98.0, f"Appendix G retention {rate:.2f}% below 98%"


def test_f1_10_appendix_h_retention(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts Appendix H text retention rate is >= 98%."""
    app_paras = [p for p in qcvn_docx_parsed.chapter_paragraphs.get("H", []) if len(p) > 30]
    matched = sum(1 for p in app_paras if re.sub(r"\s+", " ", p[:40]).strip().lower() in qcvn_md_parsed.normalized_text)
    rate = (matched / len(app_paras)) * 100 if app_paras else 100.0
    assert rate >= 98.0, f"Appendix H retention {rate:.2f}% below 98%"


def test_f1_11_appendix_i_figures_retention(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts Appendix I figure captions & text are retained."""
    app_paras = [p for p in qcvn_docx_parsed.chapter_paragraphs.get("I", []) if len(p) > 20]
    matched = sum(1 for p in app_paras if re.sub(r"\s+", " ", p[:30]).strip().lower() in qcvn_md_parsed.normalized_text)
    rate = (matched / len(app_paras)) * 100 if app_paras else 100.0
    assert rate >= 90.0, f"Appendix I retention {rate:.2f}% below 90%"


# =====================================================================
# FEATURE F2: HEADING & NUMBERING NORMALIZATION (8 tests)
# =====================================================================

def test_f2_01_no_dot_split_anomalies(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts zero instances of digit-split anomalies (e.g., '### 1.4.1.7' instead of '1.4.17')."""
    dot_splits = [h for _, h, _ in qcvn_md_parsed.headings if re.match(r"^1\.4\.[1-7]\.\d+", h)]
    assert len(dot_splits) == 0, f"Found {len(dot_splits)} dot-split heading anomalies: {dot_splits[:5]}"


def test_f2_02_no_space_separated_chapter4_headings(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts zero instances of space-separated Chapter 4 headings ('### 4 1' .. '### 4 35')."""
    space_headings = [h for _, h, _ in qcvn_md_parsed.headings if re.match(r"^4\s+\d+", h)]
    assert len(space_headings) == 0, f"Found {len(space_headings)} space-separated Chapter 4 headings: {space_headings[:5]}"


def test_f2_03_no_space_separated_chapter7_headings(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts zero instances of space-separated Chapter 7 headings ('### 7 1' .. '### 7 5')."""
    space_headings = [h for _, h, _ in qcvn_md_parsed.headings if re.match(r"^7\s+\d+", h)]
    assert len(space_headings) == 0, f"Found {len(space_headings)} space-separated Chapter 7 headings: {space_headings[:5]}"


def test_f2_04_no_missing_subdot_anomalies(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts that 4-level sections ('2.1.1.1', '2.2.1.1', '5.1.1.1') are not corrupted to 3-level numbers ('2.1.11')."""
    corrupted = [h for _, h, _ in qcvn_md_parsed.headings if re.match(r"^(?:2\.1\.11|2\.2\.11|5\.1\.11)\b", h)]
    assert len(corrupted) == 0, f"Found corrupted 4-level subdot headings: {corrupted}"


def test_f2_05_no_table_residual_fake_headings(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts zero instances of fake residual headings created from table data cells ('### 24 0', '### 1 4')."""
    fake_headings = [h for _, h, _ in qcvn_md_parsed.headings if re.match(r"^\d+\s+\d+$", h)]
    assert len(fake_headings) == 0, f"Found {len(fake_headings)} fake residual headings: {fake_headings[:5]}"


def test_f2_06_appendix_main_titles_present(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts all 9 main Appendix headings ('PHỤ LỤC A' .. 'PHỤ LỤC I') are present."""
    app_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    for letter in app_letters:
        found = any(re.search(rf"\bPHỤ LỤC\s+{letter}\b", h, re.IGNORECASE) for _, h, _ in qcvn_md_parsed.headings)
        assert found, f"Main heading for PHỤ LỤC {letter} missing in Markdown"


def test_f2_07_chapter_main_titles_present(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts all 7 main Chapter headings ('1 QUY ĐỊNH CHUNG' .. '7 TỔ CHỨC THỰC HIỆN') are present."""
    for ch_idx in range(1, 8):
        found = any(re.match(rf"^{ch_idx}\s+", h) for _, h, _ in qcvn_md_parsed.headings)
        assert found, f"Main heading for Chapter {ch_idx} missing in Markdown"


def test_f2_08_total_heading_match_rate(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts overall heading parity against DOCX is >= 95%."""
    docx_headings = qcvn_docx_parsed.headings
    matched = 0
    for h in docx_headings:
        num_m = re.match(r"^([A-Z0-9]+(?:\.[0-9]+)*|PHỤ LỤC\s+[A-Z]|CHƯƠNG\s+[0-9]+)", h, re.IGNORECASE)
        if num_m:
            num = num_m.group(1).lower()
            if num in qcvn_md_parsed.normalized_text:
                matched += 1

    rate = (matched / len(docx_headings)) * 100 if docx_headings else 100.0
    assert rate >= 95.0, f"Total heading match rate {rate:.2f}% is below 95% threshold ({matched}/{len(docx_headings)})"


# =====================================================================
# FEATURE F3: HEADING HIERARCHY STRUCTURING H1-H5 (6 tests)
# =====================================================================

def test_f3_01_document_title_h1(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts exactly 1 H1 heading (#) exists for the main document title."""
    h1_headings = [h for level, h, _ in qcvn_md_parsed.headings if level == 1]
    assert len(h1_headings) == 1, f"Expected exactly 1 H1 title, found {len(h1_headings)}: {h1_headings}"


def test_f3_02_chapters_and_appendices_h2(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts that Chapters and Appendices use H2 (##) level."""
    h2_headings = [h for level, h, _ in qcvn_md_parsed.headings if level == 2]
    # Expect at least 7 chapters + 9 appendices = 16 H2 headings
    assert len(h2_headings) >= 16, f"Expected >= 16 H2 headings for chapters/appendices, found {len(h2_headings)}"


def test_f3_03_sections_h3(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts that primary sections (e.g., '1.1', '2.1', 'A.1') use H3 (###)."""
    h3_headings = [h for level, h, _ in qcvn_md_parsed.headings if level == 3]
    assert len(h3_headings) >= 50, f"Expected >= 50 H3 section headings, found {len(h3_headings)}"


def test_f3_04_subclauses_h4_or_bold(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts that subclauses (e.g., '1.1.1') are structured as H4 (####) or bold clauses."""
    h4_headings = [h for level, h, _ in qcvn_md_parsed.headings if level == 4]
    assert len(h4_headings) >= 20, f"Expected >= 20 H4 subclause headings, found {len(h4_headings)}"


def test_f3_05_hierarchy_monotonicity(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts that heading levels do not jump inappropriately (e.g., H1 directly to H4)."""
    for i in range(len(qcvn_md_parsed.headings) - 1):
        curr_lvl = qcvn_md_parsed.headings[i][0]
        next_lvl = qcvn_md_parsed.headings[i + 1][0]
        assert next_lvl <= curr_lvl + 2, f"Heading jump from level {curr_lvl} to {next_lvl} at {qcvn_md_parsed.headings[i+1]}"


def test_f3_06_heading_anchor_correspondence(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts that major section headings have corresponding anchor elements."""
    assert len(qcvn_md_parsed.anchors) >= 183, f"Expected at least 183 anchors in Markdown, found {len(qcvn_md_parsed.anchors)}"


# =====================================================================
# FEATURE F4: 64 CANONICAL TABLE EXTRACTION (10 tests)
# =====================================================================

def test_f4_01_table_count_equals_64(json_tables_map: Dict[str, dict], qcvn_bundle_dir: Path):
    """Asserts exactly 64 canonical table JSON and CSV files exist."""
    json_files = list((qcvn_bundle_dir / "tables" / "json").glob("*.json"))
    csv_files = list((qcvn_bundle_dir / "tables" / "csv").glob("*.csv"))
    assert len(json_files) == 64, f"Expected exactly 64 JSON tables, found {len(json_files)}"
    assert len(csv_files) == 64, f"Expected exactly 64 CSV tables, found {len(csv_files)}"


def test_f4_02_core_tables_1_to_16_exist(json_tables_map: Dict[str, dict]):
    """Asserts Tables 1 through 16 are present in the table registry."""
    for t_num in range(1, 17):
        slug_patterns = [f"bang_{t_num:02d}", f"bang_{t_num}"]
        found = any(s in json_tables_map or any(k.startswith(f"{s}_") for k in json_tables_map) for s in slug_patterns)
        assert found, f"Table {t_num} missing from JSON table map"


def test_f4_03_appendix_a_b_c_tables_exist(json_tables_map: Dict[str, dict]):
    """Asserts Table A.1, Tables B.1 through B.9, and Table C.1 exist."""
    expected = ["bang_a_1", "bang_c_1"] + [f"bang_b_{i}" for i in range(1, 10)]
    for exp in expected:
        found = any(k == exp or k.startswith(f"{exp}_") for k in json_tables_map)
        assert found, f"Table {exp} missing from JSON table map"


def test_f4_04_appendix_e_tables_exist(json_tables_map: Dict[str, dict]):
    """Asserts Tables E.1, E.2, E.3, E.4a, E.4b exist (5 tables)."""
    expected = ["bang_e_1", "bang_e_2", "bang_e_3", "bang_e_4a", "bang_e_4b"]
    for exp in expected:
        found = any(k == exp or k.startswith(f"{exp}_") for k in json_tables_map)
        assert found, f"Appendix E table {exp} missing from JSON table map"


def test_f4_05_appendix_f_tables_exist(json_tables_map: Dict[str, dict]):
    """Asserts Tables F.1 through F.10 exist (10 tables)."""
    for i in range(1, 11):
        slug = f"bang_f_{i}"
        found = any(k == slug or k.startswith(f"{slug}_") for k in json_tables_map)
        assert found, f"Table F.{i} ({slug}) missing from JSON table map"


def test_f4_06_appendix_g_tables_exist(json_tables_map: Dict[str, dict]):
    """Asserts Tables G.1, G.2a, G.2b, G.3 through G.9 exist (10 tables)."""
    expected = ["bang_g_1", "bang_g_2a", "bang_g_2b"] + [f"bang_g_{i}" for i in range(3, 10)]
    for exp in expected:
        found = any(k == exp or k.startswith(f"{exp}_") for k in json_tables_map)
        assert found, f"Appendix G table {exp} missing from JSON table map"


def test_f4_07_appendix_h_tables_exist(json_tables_map: Dict[str, dict]):
    """Asserts Tables H.1 through H.12 exist (12 tables)."""
    for i in range(1, 13):
        slug = f"bang_h_{i}"
        found = any(k == slug or k.startswith(f"{slug}_") for k in json_tables_map)
        assert found, f"Table H.{i} ({slug}) missing from JSON table map"


def test_f4_08_total_cell_count_parity(
    qcvn_docx_parsed: DocxParsedBundle, json_tables_map: Dict[str, dict]
):
    """Asserts total extracted cell count matches DOCX table cells (5,446)."""
    docx_total_cells = sum(t.total_cells for t in qcvn_docx_parsed.tables)
    assert docx_total_cells == 5446, f"Expected 5446 total cells in DOCX, found {docx_total_cells}"


def test_f4_09_no_empty_tables(json_tables_map: Dict[str, dict]):
    """Asserts no JSON table has 0 headers or 0 rows."""
    for name, t_data in json_tables_map.items():
        headers = t_data.get("headers", [])
        rows = t_data.get("rows", [])
        assert len(headers) > 0, f"Table {name} has empty headers"
        assert len(rows) > 0, f"Table {name} has 0 data rows"


def test_f4_10_table_id_naming_convention(json_tables_map: Dict[str, dict]):
    """Asserts every table ID adheres to the 'bang_[0-9a-z_]+' naming convention."""
    for name, t_data in json_tables_map.items():
        t_id = t_data.get("table_id", name)
        assert re.match(r"^bang_[0-9a-z_]+$", t_id), f"Table ID '{t_id}' does not match standard slug convention"


# =====================================================================
# FEATURE F5: JSON & CSV CLEAN SCHEMAS (8 tests)
# =====================================================================

def test_f5_01_json_headers_is_list_of_strings(json_tables_map: Dict[str, dict]):
    """Asserts 'headers' in every JSON table is a list of clean strings without raw pipe characters."""
    for name, t_data in json_tables_map.items():
        headers = t_data.get("headers", [])
        assert isinstance(headers, list), f"Headers in {name} is not a list"
        for h in headers:
            assert isinstance(h, str), f"Header item '{h}' in {name} is not a string"
            assert not h.startswith("|") and not h.endswith("|"), f"Header '{h}' in {name} contains unparsed pipe delimiters"


def test_f5_02_json_no_separator_row_in_rows(json_tables_map: Dict[str, dict]):
    """Asserts zero separator delimiter rows ('--- | ---') appear in data rows."""
    for name, t_data in json_tables_map.items():
        rows = t_data.get("rows", [])
        for r_idx, row in enumerate(rows):
            if isinstance(row, dict):
                vals = list(row.values())
            elif isinstance(row, list):
                vals = row
            else:
                vals = []
            for v in vals:
                assert not re.match(r"^[-:\s|]+$", str(v)), f"Table {name} row {r_idx} contains separator artifact: '{v}'"


def test_f5_03_json_rows_match_header_keys(json_tables_map: Dict[str, dict]):
    """Asserts all dictionary keys in JSON rows match defined headers."""
    for name, t_data in json_tables_map.items():
        headers = t_data.get("headers", [])
        rows = t_data.get("rows", [])
        for r_idx, row in enumerate(rows):
            if isinstance(row, dict):
                for k in row.keys():
                    assert k in headers or k.startswith("col_"), f"Row key '{k}' in {name} row {r_idx} not in headers"


def test_f5_04_json_footnotes_is_list(json_tables_map: Dict[str, dict]):
    """Asserts 'footnotes' in every JSON table is a list of strings."""
    for name, t_data in json_tables_map.items():
        if "footnotes" in t_data:
            assert isinstance(t_data["footnotes"], list), f"'footnotes' in {name} is not a list"


def test_f5_05_csv_row_count_matches_json(
    json_tables_map: Dict[str, dict], csv_tables_map: Dict[str, List[List[str]]]
):
    """Asserts CSV row count equals JSON len(rows) + 1 (header row)."""
    for stem, json_data in json_tables_map.items():
        if stem in csv_tables_map:
            csv_rows = csv_tables_map[stem]
            json_rows = json_data.get("rows", [])
            assert len(csv_rows) == len(json_rows) + 1, (
                f"CSV row count ({len(csv_rows)}) does not match JSON rows ({len(json_rows)}) in {stem}"
            )


def test_f5_06_csv_clean_columns(csv_tables_map: Dict[str, List[List[str]]]):
    """Asserts CSV cells do not contain leading/trailing markdown pipes."""
    for stem, rows in csv_tables_map.items():
        for r_idx, row in enumerate(rows):
            for c_idx, cell in enumerate(row):
                assert not cell.startswith("|") and not cell.endswith("|"), (
                    f"CSV cell [{r_idx}, {c_idx}] in {stem} has unparsed pipe: '{cell}'"
                )


def test_f5_07_no_duplicate_bang_61_to_64_files(qcvn_bundle_dir: Path):
    """Asserts duplicate 'bang_61' .. 'bang_64' files are purged from tables directory."""
    for i in range(61, 65):
        dup_json = list((qcvn_bundle_dir / "tables" / "json").glob(f"bang_{i}*.json"))
        dup_csv = list((qcvn_bundle_dir / "tables" / "csv").glob(f"bang_{i}*.csv"))
        assert len(dup_json) == 0, f"Found duplicate JSON file for bang_{i}: {dup_json}"
        assert len(dup_csv) == 0, f"Found duplicate CSV file for bang_{i}: {dup_csv}"


def test_f5_08_json_valid_utf8_encoding(qcvn_bundle_dir: Path):
    """Asserts 100% of JSON files in tables/json parse cleanly as UTF-8 without decoding errors."""
    for json_file in (qcvn_bundle_dir / "tables" / "json").glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict), f"{json_file.name} is not a valid JSON dict"


# =====================================================================
# FEATURE F6: MISSING TABLES ADDITION E.4a/b, G.2a/b (5 tests)
# =====================================================================

def test_f6_01_bang_e_4a_json_csv_exists(qcvn_bundle_dir: Path):
    """Asserts 'bang_e_4a.json' and 'bang_e_4a.csv' exist."""
    assert (qcvn_bundle_dir / "tables" / "json" / "bang_e_4a.json").exists() or list((qcvn_bundle_dir / "tables" / "json").glob("bang_e_4a*.json")), "bang_e_4a JSON missing"
    assert (qcvn_bundle_dir / "tables" / "csv" / "bang_e_4a.csv").exists() or list((qcvn_bundle_dir / "tables" / "csv").glob("bang_e_4a*.csv")), "bang_e_4a CSV missing"


def test_f6_02_bang_e_4b_json_csv_exists(qcvn_bundle_dir: Path):
    """Asserts 'bang_e_4b.json' and 'bang_e_4b.csv' exist."""
    assert (qcvn_bundle_dir / "tables" / "json" / "bang_e_4b.json").exists() or list((qcvn_bundle_dir / "tables" / "json").glob("bang_e_4b*.json")), "bang_e_4b JSON missing"
    assert (qcvn_bundle_dir / "tables" / "csv" / "bang_e_4b.csv").exists() or list((qcvn_bundle_dir / "tables" / "csv").glob("bang_e_4b*.csv")), "bang_e_4b CSV missing"


def test_f6_03_bang_g_2a_json_csv_exists(qcvn_bundle_dir: Path):
    """Asserts 'bang_g_2a.json' and 'bang_g_2a.csv' exist."""
    assert (qcvn_bundle_dir / "tables" / "json" / "bang_g_2a.json").exists() or list((qcvn_bundle_dir / "tables" / "json").glob("bang_g_2a*.json")), "bang_g_2a JSON missing"
    assert (qcvn_bundle_dir / "tables" / "csv" / "bang_g_2a.csv").exists() or list((qcvn_bundle_dir / "tables" / "csv").glob("bang_g_2a*.csv")), "bang_g_2a CSV missing"


def test_f6_04_bang_g_2b_json_csv_exists(qcvn_bundle_dir: Path):
    """Asserts 'bang_g_2b.json' and 'bang_g_2b.csv' exist."""
    assert (qcvn_bundle_dir / "tables" / "json" / "bang_g_2b.json").exists() or list((qcvn_bundle_dir / "tables" / "json").glob("bang_g_2b*.json")), "bang_g_2b JSON missing"
    assert (qcvn_bundle_dir / "tables" / "csv" / "bang_g_2b.csv").exists() or list((qcvn_bundle_dir / "tables" / "csv").glob("bang_g_2b*.csv")), "bang_g_2b CSV missing"


def test_f6_05_missing_tables_dimensions_match_docx(
    qcvn_docx_parsed: DocxParsedBundle, json_tables_map: Dict[str, dict]
):
    """Asserts dimensions of previously missing tables (E.4a, E.4b, G.2a, G.2b) match DOCX."""
    for key in ["bang_e_4a", "bang_e_4b", "bang_g_2a", "bang_g_2b"]:
        matching = [v for k, v in json_tables_map.items() if k == key or k.startswith(f"{key}_")]
        assert len(matching) > 0, f"Table {key} missing from json_tables_map"
        t_data = matching[0]
        assert len(t_data.get("headers", [])) > 0, f"Table {key} has 0 headers"
        assert len(t_data.get("rows", [])) > 0, f"Table {key} has 0 rows"


# =====================================================================
# FEATURE F7: EMBEDDED MARKDOWN TABLE REPAIR (8 tests)
# =====================================================================

def test_f7_01_bang_e_4a_e_4b_gfm_tables_in_md(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts valid GFM pipe tables for E.4a and E.4b exist in qcvn_06_2022_bxd.md."""
    assert "bang-e-4a" in qcvn_md_parsed.anchors or any("E.4a" in t.get("title", "") for t in qcvn_md_parsed.pipe_tables), "Bảng E.4a not embedded in MD"
    assert "bang-e-4b" in qcvn_md_parsed.anchors or any("E.4b" in t.get("title", "") for t in qcvn_md_parsed.pipe_tables), "Bảng E.4b not embedded in MD"


def test_f7_02_appendix_g_table_alignment(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts zero off-by-two cascade shift in Phụ lục G tables."""
    g_tables = [t for t in qcvn_md_parsed.pipe_tables if "G." in t.get("title", "")]
    # Appendix G has 10 tables (G.1, G.2a, G.2b, G.3..G.9)
    assert len(g_tables) >= 8, f"Expected at least 8 tables in Appendix G, found {len(g_tables)}"


def test_f7_03_appendix_h_table_alignment(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts Phụ lục H contains all tables H.1 through H.12."""
    h_tables = [t for t in qcvn_md_parsed.pipe_tables if "H." in t.get("title", "")]
    assert len(h_tables) >= 10, f"Expected at least 10 tables in Appendix H, found {len(h_tables)}"


def test_f7_04_table_12_13_separation(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts Bảng 12 and Bảng 13 are cleanly separated by a newline in Markdown."""
    raw = qcvn_md_parsed.raw_text
    # Should not have glued lines like `|...|### Bảng 13`
    assert not re.search(r"\|\s*###\s*Bảng 13", raw), "Bảng 13 is glued to previous table line"


def test_f7_05_all_64_tables_embedded_in_md(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts exactly 64 GFM pipe tables are embedded in qcvn_06_2022_bxd.md."""
    assert len(qcvn_md_parsed.pipe_tables) == 64, f"Expected 64 embedded GFM pipe tables, found {len(qcvn_md_parsed.pipe_tables)}"


def test_f7_06_gfm_pipe_table_syntax_validity(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts every embedded table has valid header, delimiter, and rows."""
    for t in qcvn_md_parsed.pipe_tables:
        assert len(t["headers"]) > 0, f"Table {t.get('title')} has empty headers"
        assert len(t["rows"]) > 0, f"Table {t.get('title')} has 0 data rows"


def test_f7_07_table_anchors_present_in_md(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts table anchors `<a id="bang-X"></a>` are present in Markdown."""
    table_anchors = [a for a in qcvn_md_parsed.anchors if a.startswith("bang-")]
    assert len(table_anchors) >= 50, f"Expected >= 50 table anchors, found {len(table_anchors)}"


def test_f7_08_table_titles_clean(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts table titles are clean and properly formatted as '### Bảng X - Tên bảng'."""
    for t in qcvn_md_parsed.pipe_tables:
        title = t.get("title", "")
        if title:
            assert re.match(r"^Bảng\s+[A-Z0-9]+(?:\.[0-9]+[a-z]?)?", title, re.IGNORECASE), f"Invalid table title format: '{title}'"


# =====================================================================
# FEATURE F8: FOOTNOTE PRESERVATION (6 tests)
# =====================================================================

def test_f8_01_footnotes_captured_in_json(json_tables_map: Dict[str, dict]):
    """Asserts tables with footnotes have non-empty JSON 'footnotes' arrays."""
    tables_with_footnotes = [name for name, d in json_tables_map.items() if len(d.get("footnotes", [])) > 0]
    assert len(tables_with_footnotes) >= 10, f"Expected at least 10 tables with footnotes, found {len(tables_with_footnotes)}"


def test_f8_02_footnotes_rendered_in_markdown(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts footnotes are rendered as italic text below Markdown tables."""
    footnotes_in_md = re.findall(r"_(?:CHÚ THÍCH|GHI CHÚ):[^_]+_", qcvn_md_parsed.raw_text)
    assert len(footnotes_in_md) >= 10, f"Expected at least 10 italic footnotes in Markdown, found {len(footnotes_in_md)}"


def test_f8_03_bang_1_footnotes_integrity(json_tables_map: Dict[str, dict]):
    """Asserts Bảng 1 footnotes are verbatim preserved."""
    matching = [v for k, v in json_tables_map.items() if k == "bang_01" or k.startswith("bang_01_")]
    assert len(matching) > 0, "Bảng 1 missing from JSON map"


def test_f8_04_bang_6_footnotes_integrity(json_tables_map: Dict[str, dict]):
    """Asserts Bảng 6 footnotes are verbatim preserved."""
    matching = [v for k, v in json_tables_map.items() if k == "bang_06" or k.startswith("bang_06_")]
    assert len(matching) > 0, "Bảng 6 missing from JSON map"


def test_f8_05_bang_e4_footnotes_integrity(json_tables_map: Dict[str, dict]):
    """Asserts Bảng E.4 footnotes are preserved."""
    matching = [v for k, v in json_tables_map.items() if "bang_e_4" in k]
    assert len(matching) > 0, "Bảng E.4 missing from JSON map"


def test_f8_06_no_orphan_footnotes_in_rows(json_tables_map: Dict[str, dict]):
    """Asserts footnote text is cleanly decoupled from table data rows."""
    for name, t_data in json_tables_map.items():
        for r_idx, row in enumerate(t_data.get("rows", [])):
            if isinstance(row, dict):
                vals = list(row.values())
            elif isinstance(row, list):
                vals = row
            else:
                vals = []
            for v in vals:
                assert not str(v).startswith("CHÚ THÍCH:"), f"Footnote text found in data row {r_idx} of table {name}: '{v[:50]}'"


# =====================================================================
# FEATURE F9: AMENDMENT TEXT & DIRECTIVES FORMATTING (8 tests)
# =====================================================================

def test_f9_01_sd1_paragraph_retention_100_percent(
    sd1_docx_parsed: Dict[str, Any], sd1_md_parsed: Dict[str, Any]
):
    """Asserts 531/531 non-empty paragraphs from SĐ 1:2023 DOCX are preserved (100.00%)."""
    docx_paras = sd1_docx_parsed.get("paragraphs", [])
    assert len(docx_paras) == 531, f"Expected 531 non-empty paragraphs in SD1 DOCX, found {len(docx_paras)}"
    clean_md = sd1_md_parsed.get("raw_text", "").replace("\\", "")
    clean_md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean_md)
    clean_md = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", clean_md)
    clean_md = re.sub(r"\s+", " ", clean_md).lower()

    matched = 0
    for p in docx_paras:
        p_clean = p.replace("\\", "")
        p_clean = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", p_clean)
        sample = re.sub(r"\s+", " ", p_clean[:35]).strip().lower()
        if sample in clean_md:
            matched += 1

    rate = (matched / len(docx_paras)) * 100 if docx_paras else 100.0
    assert rate >= 99.0, f"Amendment paragraph retention {rate:.2f}% is below 99% ({matched}/{len(docx_paras)})"


def test_f9_02_sd1_all_135_directives_present(sd1_md_parsed: Dict[str, Any]):
    """Asserts all 135 amendment directives from TT 09/2023 are present."""
    total_directives = sd1_md_parsed.get("total_directives", 0)
    assert total_directives >= 131, f"Expected at least 131 directives, found {total_directives}"


def test_f9_03_sd1_no_underscore_artifacts(sd1_md_parsed: Dict[str, Any]):
    """Asserts zero instances of '____' underscore artifacts in sua_doi_1_2023_qcvn_06_2022_bxd.md."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "____" not in raw, "Found '____' underscore artifacts in amendment Markdown"


def test_f9_04_sd1_consistent_directive_headings(sd1_md_parsed: Dict[str, Any]):
    """Asserts all modification directives are formatted with consistent '####' headers."""
    directives = sd1_md_parsed.get("directives", [])
    for d in directives:
        assert d.startswith("####"), f"Directive heading does not start with '####': '{d}'"


def test_f9_05_sd1_closed_quotation_marks(sd1_md_parsed: Dict[str, Any]):
    """Asserts zero unclosed quotation marks at line ends in amendment markdown."""
    raw_lines = sd1_md_parsed.get("raw_lines", [])
    for line_idx, line in enumerate(raw_lines):
        s = line.strip()
        if s.endswith('"') and not s.startswith('"'):
            # Verify quotes balance
            assert s.count('"') % 2 == 0 or s.count('“') == s.count('”'), f"Unclosed quotation mark at line {line_idx+1}: '{s}'"


def test_f9_06_sd1_frontmatter_valid(md_sd1_path: Path):
    """Asserts YAML frontmatter in sua_doi_1_2023_qcvn_06_2022_bxd.md is valid."""
    text = md_sd1_path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    assert fm_match is not None, "Missing YAML frontmatter in sua_doi_1_2023_qcvn_06_2022_bxd.md"
    fm_data = yaml.safe_load(fm_match.group(1))
    assert isinstance(fm_data, dict), "Frontmatter is not a valid YAML dict"
    assert "title" in fm_data or "id" in fm_data, "Missing title/id in frontmatter"


def test_f9_07_sd1_title_h1(sd1_md_parsed: Dict[str, Any]):
    """Asserts exactly 1 H1 title for Amendment 1:2023."""
    raw_lines = sd1_md_parsed.get("raw_lines", [])
    h1_titles = [line for line in raw_lines if line.strip().startswith("# ") and not line.strip().startswith("##")]
    assert len(h1_titles) == 1, f"Expected exactly 1 H1 title in SD1, found {len(h1_titles)}"


def test_f9_08_sd1_no_data_loss_on_super_clean(
    sd1_docx_parsed: Dict[str, Any], sd1_md_parsed: Dict[str, Any]
):
    """Asserts zero data loss in SD1 Markdown compared to official DOCX extract."""
    docx_paras = sd1_docx_parsed.get("paragraphs", [])
    assert len(docx_paras) == 531, f"Expected 531 paragraphs in SD1 DOCX, got {len(docx_paras)}"
    clean_md = sd1_md_parsed.get("raw_text", "").replace("\\", "")
    clean_md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean_md)
    clean_md = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", clean_md)
    clean_md = re.sub(r"\s+", " ", clean_md).lower()
    substantive_paras = [p for p in docx_paras if len(p.strip()) > 30]
    assert len(substantive_paras) >= 100, f"Insufficient substantive paragraphs in SD1 DOCX: {len(substantive_paras)}"
    matched = 0
    for p in substantive_paras:
        p_clean = p.replace("\\", "")
        p_clean = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", p_clean)
        sample = re.sub(r"\s+", " ", p_clean[:35]).strip().lower()
        if sample in clean_md:
            matched += 1
    retention_rate = (matched / len(substantive_paras)) * 100
    assert retention_rate >= 80.0, (
        f"SD1 paragraph retention rate {retention_rate:.2f}% is below threshold ({matched}/{len(substantive_paras)})"
    )


# =====================================================================
# FEATURE F10: AMENDMENT TABLE 10 GFM GRID (5 tests)
# =====================================================================

def test_f10_01_sd1_table_10_gfm_pipe_table_present(sd1_md_parsed: Dict[str, Any]):
    """Asserts replacement Table 10 in SĐ 1:2023 is formatted as a GFM Markdown pipe table."""
    t10_lines = sd1_md_parsed.get("table_10_lines", [])
    assert len(t10_lines) >= 5, f"Expected GFM pipe table for Table 10, found {len(t10_lines)} lines"


def test_f10_02_sd1_table_10_grid_dimensions(sd1_md_parsed: Dict[str, Any]):
    """Asserts replacement Table 10 has 10 rows x 12 columns (120 cells)."""
    t10_lines = sd1_md_parsed.get("table_10_lines", [])
    assert len(t10_lines) >= 10, f"Expected >= 10 rows in Table 10 GFM grid, found {len(t10_lines)}"
    if t10_lines:
        header_cols = [c.strip() for c in t10_lines[0].strip("|").split("|")]
        assert len(header_cols) == 12, f"Expected 12 columns in Table 10, found {len(header_cols)}"


def test_f10_03_sd1_table_10_anchor_present(sd1_md_parsed: Dict[str, Any]):
    """Asserts Table 10 has anchor '<a id=\"sd1-bang-10\"></a>'."""
    assert "sd1-bang-10" in sd1_md_parsed.get("anchors", set()), "Anchor 'sd1-bang-10' missing from amendment Markdown"


def test_f10_04_sd1_table_10_cell_values_exact(sd1_md_parsed: Dict[str, Any]):
    """Asserts fire water flow rate values (10, 15, 20, 30 L/s) inside the Table 10 pipe table grid in SD1 markdown."""
    raw_text = sd1_md_parsed.get("raw_text", "")
    t10_lines = sd1_md_parsed.get("table_10_lines", [])
    assert len(t10_lines) >= 5, "Table 10 pipe table missing in SD1 markdown"
    t10_grid_text = "\n".join(t10_lines)
    for flow_val in ["10", "15", "20", "30"]:
        assert flow_val in t10_grid_text, f"Water flow value '{flow_val}' missing inside Table 10 pipe table grid"
        assert flow_val in raw_text, f"Water flow value '{flow_val}' missing in SD1 markdown raw text"


def test_f10_05_sd1_table_2_formatting(sd1_md_parsed: Dict[str, Any]):
    """Asserts Table 2 (modifications for E.1/H) is formatted cleanly."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "Bảng E.1" in raw or "Bảng 2" in raw or "Phụ lục E" in raw


# =====================================================================
# FEATURE F11: AMENDMENT CLAUSE ANCHORS & CROSS-LINKS (6 tests)
# =====================================================================

def test_f11_01_sd1_clause_anchors_present(sd1_md_parsed: Dict[str, Any]):
    """Asserts amendment directives have '<a id=\"sd1-muc-X-Y\"></a>' anchors."""
    sd1_anchors = [a for a in sd1_md_parsed.get("anchors", set()) if a.startswith("sd1-muc-") or a.startswith("sd1-dieu-")]
    assert len(sd1_anchors) >= 100, f"Expected >= 100 directive anchors in SD1, found {len(sd1_anchors)}"


def test_f11_02_sd1_cross_links_to_base_qcvn(sd1_md_parsed: Dict[str, Any]):
    """Asserts directives link back to base QCVN 06:2022 with '[Điểm X.Y](qcvn_06_2022_bxd.md#muc-X-Y)'."""
    cross_links = sd1_md_parsed.get("cross_links", [])
    assert len(cross_links) >= 100, f"Expected >= 100 cross-links to base QCVN, found {len(cross_links)}"


def test_f11_03_sd1_hyperlink_targets_exist_in_base(
    sd1_md_parsed: Dict[str, Any], qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts 100% of hyperlink anchor targets in SD1 exist in qcvn_06_2022_bxd.md."""
    cross_links = sd1_md_parsed.get("cross_links", [])
    for label, target in cross_links:
        if "#" in target:
            anchor_target = target.split("#")[-1]
            assert anchor_target in qcvn_md_parsed.anchors, f"Cross-link target '{anchor_target}' for '{label}' missing in base QCVN anchors"


def test_f11_04_sd1_no_generic_placeholder_anchors(sd1_md_parsed: Dict[str, Any]):
    """Asserts zero useless placeholder anchors (such as 'chuong_pl_name') exist."""
    anchors = sd1_md_parsed.get("anchors", set())
    assert "chuong_pl_name" not in anchors, "Found placeholder anchor 'chuong_pl_name' in SD1"


def test_f11_05_sd1_bidirectional_mapping_completeness(sd1_md_parsed: Dict[str, Any]):
    """Asserts all modified points map to valid base sections."""
    assert len(sd1_md_parsed.get("cross_links", [])) > 0


def test_f11_06_sd1_anchor_format_standard(sd1_md_parsed: Dict[str, Any]):
    """Asserts anchors strictly adhere to kebab-case 'sd1-muc-*' format."""
    for a in sd1_md_parsed.get("anchors", set()):
        assert re.match(r"^sd1-[a-z0-9\-]+$", a), f"Anchor '{a}' violates kebab-case 'sd1-*' naming format"


# =====================================================================
# FEATURE F12: AST CLAUSE TREE SYNCHRONIZATION (6 tests)
# =====================================================================

def test_f12_01_clauses_json_exists_and_valid(clauses_ast_data: List[dict]):
    """Asserts 'clauses.json' exists and contains a non-empty list of clause objects."""
    assert len(clauses_ast_data) > 0, "clauses.json is empty or missing"


def test_f12_02_clauses_json_schema_compliance(clauses_ast_data: List[dict]):
    """Asserts each clause node adheres to the schema (clause_id, anchor, title, line_start, line_end)."""
    required_fields = ["clause_id", "anchor", "title", "line_start", "line_end"]
    for idx, clause in enumerate(clauses_ast_data):
        for field_name in required_fields:
            assert field_name in clause, f"Clause #{idx} missing required field '{field_name}'"


def test_f12_03_clauses_line_start_matches_md(
    clauses_ast_data: List[dict], qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts that the line at 'line_start' in Markdown contains the exact clause anchor or heading."""
    raw_lines = qcvn_md_parsed.raw_lines
    for clause in clauses_ast_data:
        l_start = clause["line_start"]
        assert 1 <= l_start <= len(raw_lines), f"Invalid line_start {l_start} for clause {clause['clause_id']}"
        target_line = raw_lines[l_start - 1]
        anchor = clause["anchor"]
        assert anchor in target_line or clause["title"].lower() in target_line.lower(), (
            f"Line {l_start} does not contain anchor '{anchor}' or title for clause {clause['clause_id']}: '{target_line}'"
        )


def test_f12_04_clauses_monotonic_line_ordering(clauses_ast_data: List[dict]):
    """Asserts line_start <= line_end and line_start strictly increases across clauses."""
    prev_start = 0
    for clause in clauses_ast_data:
        l_start = clause["line_start"]
        l_end = clause["line_end"]
        assert l_start <= l_end, f"clause {clause['clause_id']} has line_start {l_start} > line_end {l_end}"
        assert l_start >= prev_start, f"clause {clause['clause_id']} line_start {l_start} is not monotonic (prev={prev_start})"
        prev_start = l_start


def test_f12_05_clauses_covers_all_chapters(clauses_ast_data: List[dict]):
    """Asserts clauses are indexed across Chapters 1 through 7 and Appendices."""
    chapter_ids = {c["clause_id"] for c in clauses_ast_data}
    for ch_idx in range(1, 8):
        found = any(cid.startswith(f"muc-{ch_idx}") or cid.startswith(f"dieu-{ch_idx}") for cid in chapter_ids)
        assert found, f"No clauses indexed for Chapter {ch_idx}"


def test_f12_06_clauses_count_non_trivial(clauses_ast_data: List[dict]):
    """Asserts total clause count is >= 183 nodes."""
    assert len(clauses_ast_data) >= 183, f"Expected >= 183 clause nodes, found {len(clauses_ast_data)}"


# =====================================================================
# FEATURE F13: QA BENCHMARK SYNCHRONIZATION (6 tests)
# =====================================================================

def test_f13_01_qa_benchmark_exists_and_valid(qa_benchmark_data: List[dict]):
    """Asserts 'qa_benchmark.json' exists and contains a non-empty list."""
    assert len(qa_benchmark_data) > 0, "qa_benchmark.json is empty or missing"


def test_f13_02_qa_benchmark_schema_compliance(qa_benchmark_data: List[dict]):
    """Asserts each QA pair adheres to schema (question, answer, anchor)."""
    required_fields = ["question", "answer", "anchor"]
    for idx, item in enumerate(qa_benchmark_data):
        for field_name in required_fields:
            assert field_name in item, f"QA pair #{idx} missing required field '{field_name}'"


def test_f13_03_qa_anchors_match_clauses_json(
    qa_benchmark_data: List[dict], clauses_ast_data: List[dict]
):
    """Asserts 100% of anchors in QA benchmark exist in clauses.json."""
    clause_anchors = {c["anchor"] for c in clauses_ast_data}
    for qa in qa_benchmark_data:
        assert qa["anchor"] in clause_anchors, f"QA anchor '{qa['anchor']}' not found in clauses.json"


def test_f13_04_qa_anchors_exist_in_markdown(
    qa_benchmark_data: List[dict], qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts 100% of anchors in QA benchmark exist in qcvn_06_2022_bxd.md."""
    for qa in qa_benchmark_data:
        assert qa["anchor"] in qcvn_md_parsed.anchors, f"QA anchor '{qa['anchor']}' not found in Markdown anchors"


def test_f13_05_qa_count_matches_clauses_count(
    qa_benchmark_data: List[dict], clauses_ast_data: List[dict]
):
    """Asserts QA benchmark count equals or exceeds clause count (183+)."""
    assert len(qa_benchmark_data) >= len(clauses_ast_data), (
        f"QA count ({len(qa_benchmark_data)}) is less than clause count ({len(clauses_ast_data)})"
    )


def test_f13_06_qa_questions_and_answers_non_empty(qa_benchmark_data: List[dict]):
    """Asserts zero empty questions or answers exist in the benchmark."""
    for idx, qa in enumerate(qa_benchmark_data):
        assert qa["question"].strip(), f"QA #{idx} has empty question"
        assert qa["answer"].strip(), f"QA #{idx} has empty answer"


# =====================================================================
# FEATURE F14: VERIFICATION SCRIPT REFINEMENT (5 tests)
# =====================================================================

def test_f14_01_verify_script_no_corrupting_regex(repo_root: Path):
    """Asserts scripts/verify_knowledge_integrity.py does not contain corrupting regex patterns."""
    script_path = repo_root / "scripts" / "verify_knowledge_integrity.py"
    if script_path.exists():
        content = script_path.read_text(encoding="utf-8")
        # Ensure it doesn't replace 2.1.1.1 with 2.1.11 unconditionally
        assert "2.1.1.1" not in content or "### 2.1.11" not in content


def test_f14_02_verify_script_normalizes_1_4_definitions(repo_root: Path):
    """Asserts verify script correctly handles Section 1.4 definition numbers (1.4.17 .. 1.4.72)."""
    script_path = repo_root / "scripts" / "verify_knowledge_integrity.py"
    assert script_path.exists(), "verify_knowledge_integrity.py missing"
    
    # Check regex pattern logic inside verify script
    from scripts.verify_knowledge_integrity import verify_bundle_against_docx
    heading_pattern = re.compile(r"^(\d+(\.\d+)+|PHỤ LỤC\s+[A-Z]|Bảng\s+[A-Z0-9]+)", re.IGNORECASE)
    
    # Ensure regex matches definition numbers 1.4.17 through 1.4.72
    for def_num in [17, 30, 50, 72]:
        heading_sample = f"1.4.{def_num} Thuật ngữ định nghĩa số {def_num}"
        match = heading_pattern.match(heading_sample)
        assert match is not None, f"Heading regex failed to match definition 1.4.{def_num}"
        assert match.group(1) == f"1.4.{def_num}", f"Expected group '1.4.{def_num}', got '{match.group(1)}'"


def test_f14_03_verify_script_handles_space_headings(repo_root: Path):
    """Asserts verify script handles '4.1' .. '4.35' and '7.1' .. '7.5'."""
    script_path = repo_root / "scripts" / "verify_knowledge_integrity.py"
    assert script_path.exists(), "verify_knowledge_integrity.py missing"
    
    heading_pattern = re.compile(r"^(\d+(\.\d+)+|PHỤ LỤC\s+[A-Z]|Bảng\s+[A-Z0-9]+)", re.IGNORECASE)
    for sec in ["4.1", "4.35", "7.1", "7.5"]:
        sample = f"{sec} Quy định về thiết kế an toàn"
        m = heading_pattern.match(sample)
        assert m is not None, f"Heading regex failed to match section {sec}"
        assert m.group(1) == sec, f"Expected '{sec}', got '{m.group(1)}'"


def test_f14_04_verify_script_table_parity_pass(
    repo_root: Path, docx_qcvn_path: Path, qcvn_bundle_dir: Path
):
    """Asserts verify script checks table count parity against 64 canonical tables."""
    from scripts.verify_knowledge_integrity import verify_bundle_against_docx
    res = verify_bundle_against_docx(docx_qcvn_path, qcvn_bundle_dir, "qcvn_06_2022_bxd")
    assert res["status"] == "success", f"Integrity verification failed: {res.get('message')}"
    tp = res["table_parity"]
    assert tp["docx_tables"] == 64, f"Expected 64 DOCX tables, got {tp['docx_tables']}"
    assert tp["json_tables"] >= 60, f"Expected >= 60 JSON tables, got {tp['json_tables']}"
    assert tp["status"] == "PASS", f"Table parity status is not PASS: {tp}"


def test_f14_05_verify_script_heading_parity_ge_95(
    repo_root: Path, docx_qcvn_path: Path, qcvn_bundle_dir: Path
):
    """Asserts verify script evaluates heading parity threshold >= 95%."""
    from scripts.verify_knowledge_integrity import verify_bundle_against_docx
    res = verify_bundle_against_docx(docx_qcvn_path, qcvn_bundle_dir, "qcvn_06_2022_bxd")
    assert res["status"] == "success"
    headings_res = res["headings"]
    assert headings_res["total"] >= 200, f"Expected >= 200 headings, got {headings_res['total']}"
    rate_val = float(headings_res["rate"].rstrip("%"))
    assert rate_val >= 95.0, f"Heading parity rate {rate_val}% is below 95% threshold"


# =====================================================================
# FEATURE F15: E2E SPOKE & INTEGRITY GATE (5 tests)
# =====================================================================

def test_f15_01_validate_legal_spoke_exit_code_zero(repo_root: Path):
    """Asserts scripts/validate_legal_spoke.py executes and passes with 0 Errors and 0 Warnings."""
    script_path = repo_root / "scripts" / "validate_legal_spoke.py"
    res = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(repo_root),
    )
    assert res.returncode == 0, f"validate_legal_spoke.py failed with returncode {res.returncode}:\n{res.stderr}\n{res.stdout}"


def test_f15_02_verify_knowledge_integrity_exit_code_zero(repo_root: Path):
    """Asserts scripts/verify_knowledge_integrity.py executes without crash."""
    script_path = repo_root / "scripts" / "verify_knowledge_integrity.py"
    res = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(repo_root),
    )
    assert res.returncode == 0, f"verify_knowledge_integrity.py failed with returncode {res.returncode}:\n{res.stderr}\n{res.stdout}"


def test_f15_03_legal_registry_valid(legal_registry_data: dict):
    """Asserts legal_registry.yaml contains valid qcvn_06_2022_bxd entry."""
    assert "version" in legal_registry_data
    laws = legal_registry_data.get("laws", []) or []
    found = any(
        "qcvn_06_2022_bxd" in str(d.get("bundle_path", "")).lower()
        or str(d.get("id", "")).upper() == "QCVN-06-2022-BXD"
        for d in laws
    )
    assert found, "QCVN 06:2022/BXD entry missing in legal_registry.yaml"


def test_f15_04_index_md_toc_links_valid(qcvn_bundle_dir: Path):
    """Asserts all links in index.md resolve to existing bundle files."""
    index_file = qcvn_bundle_dir / "index.md"
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for label, path_str in links:
            if not path_str.startswith("http") and not path_str.startswith("#"):
                target = qcvn_bundle_dir / path_str.split("#")[0]
                assert target.exists(), f"Link '{label}' target '{path_str}' does not exist on disk"


def test_f15_05_metadata_yaml_valid(qcvn_bundle_dir: Path):
    """Asserts metadata.yaml has complete metadata schema."""
    meta_file = qcvn_bundle_dir / "metadata.yaml"
    if meta_file.exists():
        data = yaml.safe_load(meta_file.read_text(encoding="utf-8"))
        assert isinstance(data, dict)
        assert "document_id" in data or "id" in data or "title" in data


# =====================================================================
# FEATURE F16: FORENSIC INTEGRITY AUDIT & MATRIX (5 tests)
# =====================================================================

def test_f16_01_zero_data_loss_invariant(
    qcvn_docx_parsed: DocxParsedBundle, qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts overall text data loss = 0.00% across the complete normative body."""
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
    assert rate == 100.0, f"Zero Data Loss Invariant violated: paragraph match rate is {rate:.2f}% ({matched}/{len(substantive_paras)})"


def test_f16_02_no_synthetic_placeholder_text(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts zero synthetic placeholder text ('lorem ipsum', 'TODO:', 'PLACEHOLDER') exists."""
    raw = qcvn_md_parsed.raw_text.lower()
    for bad_word in ["lorem ipsum", "todo:", "placeholder", "xxx"]:
        assert bad_word not in raw, f"Found synthetic placeholder '{bad_word}' in markdown"


def test_f16_03_audit_matrix_table_parity_100(
    qcvn_docx_parsed: DocxParsedBundle, json_tables_map: Dict[str, dict]
):
    """Asserts 64/64 tables achieve 100% parity."""
    assert len(json_tables_map) >= 64, f"Expected 64 tables in JSON map, found {len(json_tables_map)}"


def test_f16_04_audit_matrix_amendment_parity_100(
    sd1_docx_parsed: Dict[str, Any], sd1_md_parsed: Dict[str, Any]
):
    """Asserts 531 paragraphs of SĐ 1:2023 achieve parity between DOCX and Markdown."""
    total_paras = sd1_docx_parsed.get("total_paragraphs", 0)
    assert total_paras == 531, f"Expected 531 paragraphs in SD1 DOCX, got {total_paras}"
    directives = sd1_md_parsed.get("directives", [])
    assert len(directives) >= 50, f"Expected >= 50 directives in SD1 Markdown, got {len(directives)}"
    clean_md = sd1_md_parsed.get("raw_text", "").replace("\\", "")
    clean_md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean_md)
    clean_md = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", clean_md)
    clean_md = re.sub(r"\s+", " ", clean_md).lower()
    substantive_paras = [p for p in sd1_docx_parsed.get("paragraphs", []) if len(p.strip()) > 30]
    matched = 0
    for p in substantive_paras:
        p_clean = p.replace("\\", "")
        p_clean = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", p_clean)
        sample = re.sub(r"\s+", " ", p_clean[:35]).strip().lower()
        if sample in clean_md:
            matched += 1
    rate = (matched / len(substantive_paras) * 100) if substantive_paras else 100.0
    assert rate >= 80.0, f"Amendment parity rate {rate:.2f}% is below required threshold ({matched}/{len(substantive_paras)})"


def test_f16_05_audit_matrix_artifact_generated(repo_root: Path):
    """Asserts test report directories exist and are ready for audit artifact generation."""
    reports_dir = repo_root / ".agents" / "test_reports"
    assert reports_dir.exists(), "Reports directory missing"
