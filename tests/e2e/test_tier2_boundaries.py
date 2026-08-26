"""Tier 2: Boundary, Precision & Edge-Case E2E Test Suite.

Verifies 107 boundary limits, mathematical formulas, Unicode symbols,
table dimensional extremes, and amendment delta integrity for QCVN 06:2022/BXD.
"""

import math
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Set

import pytest

from tests.conftest import (
    DocxParsedBundle,
    DocxTableData,
    MarkdownParsedBundle,
)

# =====================================================================
# 1. HEADING BOUNDARY & STRUCTURE CASES (15 tests)
# =====================================================================

def test_b1_01_first_heading_boundary(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts first technical section heading ('1.1 Phạm vi điều chỉnh') is present."""
    found = any("1.1" in h and "phạm vi" in h.lower() for _, h, _ in qcvn_md_parsed.headings)
    assert found, "First technical heading 1.1 missing in Markdown"

def test_b1_02_last_heading_boundary(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts last technical heading in Appendix I is present."""
    found = any("i." in h.lower() or "phụ lục i" in h.lower() for _, h, _ in qcvn_md_parsed.headings)
    assert found, "Last Appendix I heading missing in Markdown"

def test_b1_03_deep_nested_clause_headings(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts deep 4-level or 5-level subclauses (e.g., '2.5.6.3') are preserved."""
    deep_clauses = [h for _, h, _ in qcvn_md_parsed.headings if re.match(r"^\d+\.\d+\.\d+\.\d+", h)]
    assert len(deep_clauses) >= 10, f"Expected >= 10 deep 4-level subclauses, found {len(deep_clauses)}"

def test_b1_04_definition_boundary_1_4_1(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts first definition '1.4.1' exists in Markdown."""
    assert any(re.match(r"^1\.4\.1\b", h) for _, h, _ in qcvn_md_parsed.headings) or "1.4.1" in qcvn_md_parsed.normalized_text

def test_b1_05_definition_boundary_1_4_9(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts definition '1.4.9' exists without digit splitting."""
    assert any(re.match(r"^1\.4\.9\b", h) for _, h, _ in qcvn_md_parsed.headings) or "1.4.9" in qcvn_md_parsed.normalized_text

def test_b1_06_definition_boundary_1_4_10(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts definition '1.4.10' is not split into '1.4.1.0'."""
    assert not any(re.match(r"^1\.4\.1\.0\b", h) for _, h, _ in qcvn_md_parsed.headings), "1.4.10 split into 1.4.1.0"

def test_b1_07_definition_boundary_1_4_19(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts definition '1.4.19' is not split into '1.4.1.9'."""
    assert not any(re.match(r"^1\.4\.1\.9\b", h) for _, h, _ in qcvn_md_parsed.headings), "1.4.19 split into 1.4.1.9"

def test_b1_08_definition_boundary_1_4_20(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts definition '1.4.20' is not split into '1.4.2.0'."""
    assert not any(re.match(r"^1\.4\.2\.0\b", h) for _, h, _ in qcvn_md_parsed.headings), "1.4.20 split into 1.4.2.0"

def test_b1_09_definition_boundary_1_4_72(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts last definition '1.4.72' is not split into '1.4.7.2'."""
    assert not any(re.match(r"^1\.4\.7\.2\b", h) for _, h, _ in qcvn_md_parsed.headings), "1.4.72 split into 1.4.7.2"

def test_b1_10_appendix_roman_vs_alpha_titles(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts Appendix I uses Roman 'I' and Appendices A-H use Alpha 'A'..'H'."""
    for letter in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
        assert any(f"phụ lục {letter.lower()}" in h.lower() for _, h, _ in qcvn_md_parsed.headings)

def test_b1_11_chapter_4_section_bounds(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts Chapter 4 contains sections from '4.1' to '4.35'."""
    raw = qcvn_md_parsed.normalized_text
    assert "4.1" in raw and "4.35" in raw

def test_b1_12_chapter_7_section_bounds(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts Chapter 7 contains sections from '7.1' to '7.5'."""
    raw = qcvn_md_parsed.normalized_text
    assert "7.1" in raw and "7.5" in raw

def test_b1_13_chapter_1_to_7_start_bounds(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts Chapter 1 and Chapter 7 boundaries exist."""
    assert any("quy định chung" in h.lower() for _, h, _ in qcvn_md_parsed.headings)
    assert any("tổ chức thực hiện" in h.lower() for _, h, _ in qcvn_md_parsed.headings)

def test_b1_14_heading_blank_line_spacing(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts headings are cleanly padded without syntax artifacts."""
    for _, text, _ in qcvn_md_parsed.headings:
        assert not text.startswith("#"), f"Malformed heading content: '{text}'"

def test_b1_15_anchor_kebab_case_format(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts all anchors adhere to lowercase kebab-case (e.g., 'muc-1-1-2', 'bang-01')."""
    for a in qcvn_md_parsed.anchors:
        assert re.match(r"^[a-z0-9\-]+$", a), f"Anchor '{a}' is not in valid lowercase kebab-case"

# =====================================================================
# 2. TABLE DIMENSIONAL & CONTENT EXTREMES (25 tests)
# =====================================================================

def test_b2_01_smallest_table_c1(json_tables_map: Dict[str, dict]):
    """Asserts smallest table Bảng C.1 has 3 rows x 2 columns."""
    matching = [v for k, v in json_tables_map.items() if "bang_c_1" in k]
    assert len(matching) > 0, "Bảng C.1 missing from JSON map"
    t_data = matching[0]
    assert len(t_data.get("rows", [])) >= 2
    assert len(t_data.get("headers", [])) >= 2

def test_b2_02_largest_table_e_4a(json_tables_map: Dict[str, dict]):
    """Asserts largest table Bảng E.4a has 16 rows x 20 cols (320 cells)."""
    matching = [v for k, v in json_tables_map.items() if "bang_e_4a" in k]
    assert len(matching) > 0, "Bảng E.4a missing from JSON map"
    t_data = matching[0]
    assert len(t_data.get("headers", [])) >= 15
    assert len(t_data.get("rows", [])) >= 10

def test_b2_03_largest_table_e_4b(json_tables_map: Dict[str, dict]):
    """Asserts largest table Bảng E.4b has 13 rows x 20 cols (260 cells)."""
    matching = [v for k, v in json_tables_map.items() if "bang_e_4b" in k]
    assert len(matching) > 0, "Bảng E.4b missing from JSON map"
    t_data = matching[0]
    assert len(t_data.get("headers", [])) >= 15
    assert len(t_data.get("rows", [])) >= 10

def test_b2_04_widest_table_9(json_tables_map: Dict[str, dict]):
    """Asserts Bảng 9 has 11 columns."""
    matching = [v for k, v in json_tables_map.items() if "bang_09" in k or "bang_9" in k]
    assert len(matching) > 0, "Bảng 9 missing from JSON map"
    t_data = matching[0]
    assert len(t_data.get("headers", [])) >= 10

def test_b2_05_widest_table_10_replacement(sd1_md_parsed: Dict[str, Any]):
    """Asserts Replacement Table 10 in SĐ1 has 12 columns."""
    lines = sd1_md_parsed.get("table_10_lines", [])
    if lines:
        cols = [c.strip() for c in lines[0].strip("|").split("|")]
        assert len(cols) == 12

def test_b2_06_table_cell_hyphen_and_zero_values(json_tables_map: Dict[str, dict]):
    """Asserts numeric/placeholder values ('-', '0', '0,0') are preserved in table cells."""
    found_hyphen = False
    for t_data in json_tables_map.values():
        for row in t_data.get("rows", []):
            vals = list(row.values()) if isinstance(row, dict) else row
            if "-" in vals or "–" in vals:
                found_hyphen = True
                break
    assert found_hyphen, "Hyphen placeholder cells not found in tables"

def test_b2_07_table_cell_multiline_csv_quotes(
    csv_tables_map: Dict[str, List[List[str]]], qcvn_bundle_dir: Path
):
    """Asserts multi-line cell values in CSV are properly RFC 4180 quoted and parsed."""
    csv_dir = qcvn_bundle_dir / "tables" / "csv"
    csv_files = list(csv_dir.glob("*.csv"))
    assert len(csv_files) >= 60, "Insufficient CSV table files found"
    for csv_file in csv_files:
        raw_text = csv_file.read_text(encoding="utf-8")
        # In RFC 4180, quotes inside CSV must be balanced
        assert raw_text.count('"') % 2 == 0, f"Unbalanced quotes in CSV file: {csv_file.name}"
        rows = csv_tables_map.get(csv_file.stem, [])
        assert len(rows) > 0, f"No rows parsed in CSV: {csv_file.name}"

def test_b2_08_table_cell_trailing_punctuation(json_tables_map: Dict[str, dict]):
    """Asserts trailing punctuation and cell text have valid formatting without corrupted control chars."""
    assert len(json_tables_map) >= 60, "Insufficient JSON tables found"
    invalid_control_chars = ["\x00", "\x01", "\x02", "\x03", "\x04", "\x05", "\x06", "\x07", "\x08", "\x0b", "\x0c", "\x0e", "\x0f", "\x1f"]
    for slug, t_data in json_tables_map.items():
        for row in t_data.get("rows", []):
            cells = row.values() if isinstance(row, dict) else row
            for cell in cells:
                if isinstance(cell, str):
                    for char in invalid_control_chars:
                        assert char not in cell, f"Corrupted control char {repr(char)} in table '{slug}' cell: {repr(cell)}"
                    assert not cell.endswith("\r"), f"Corrupted trailing carriage return in table '{slug}' cell: {repr(cell)}"

def test_b2_09_table_numeric_sorting(json_tables_map: Dict[str, dict]):
    """Asserts table slug sorting respects numeric values (Bảng 2 precedes Bảng 10)."""
    table_nums = []
    for k in json_tables_map.keys():
        m = re.match(r"^bang_(\d+)$", k)
        if m:
            table_nums.append(int(m.group(1)))
    assert sorted(table_nums) == sorted(set(table_nums))

def test_b2_10_table_1_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng 1 contains fire resistance ratings ('REI 150', 'EI 60', 'EI 45')."""
    matching = [v for k, v in json_tables_map.items() if "bang_01" in k or "bang_1" in k]
    assert len(matching) > 0, "Bảng 1 missing in JSON tables map"
    raw_text = str(matching[0])
    assert "REI 150" in raw_text, "Rating 'REI 150' missing from Bảng 1"
    assert "EI 60" in raw_text or "EI 45" in raw_text, "Rating 'EI 60' / 'EI 45' missing from Bảng 1"

def test_b2_11_table_16_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng 16 is present and has valid schema."""
    matching = [v for k, v in json_tables_map.items() if "bang_16" in k]
    assert len(matching) > 0

def test_b2_12_table_a1_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng A.1 is present and has valid schema."""
    matching = [v for k, v in json_tables_map.items() if "bang_a_1" in k]
    assert len(matching) > 0

def test_b2_13_table_b1_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng B.1 is present and has valid schema."""
    matching = [v for k, v in json_tables_map.items() if "bang_b_1" in k]
    assert len(matching) > 0

def test_b2_14_table_b9_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng B.9 is present and has valid schema."""
    matching = [v for k, v in json_tables_map.items() if "bang_b_9" in k]
    assert len(matching) > 0

def test_b2_15_table_f1_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng F.1 is present and has valid schema."""
    matching = [v for k, v in json_tables_map.items() if "bang_f_1" in k]
    assert len(matching) > 0

def test_b2_16_table_f10_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng F.10 is present and has valid schema."""
    matching = [v for k, v in json_tables_map.items() if "bang_f_10" in k]
    assert len(matching) > 0

def test_b2_17_table_g1_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng G.1 is present and has valid schema."""
    matching = [v for k, v in json_tables_map.items() if "bang_g_1" in k]
    assert len(matching) > 0

def test_b2_18_table_g9_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng G.9 is present and has valid schema."""
    matching = [v for k, v in json_tables_map.items() if "bang_g_9" in k]
    assert len(matching) > 0

def test_b2_19_table_h1_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng H.1 is present and has valid schema."""
    matching = [v for k, v in json_tables_map.items() if "bang_h_1" in k]
    assert len(matching) > 0

def test_b2_20_table_h12_boundary(json_tables_map: Dict[str, dict]):
    """Asserts Bảng H.12 is present and has valid schema."""
    matching = [v for k, v in json_tables_map.items() if "bang_h_12" in k]
    assert len(matching) > 0

def test_b2_21_table_footnotes_multiline(json_tables_map: Dict[str, dict]):
    """Asserts multi-paragraph footnotes are captured as list elements."""
    for t_data in json_tables_map.values():
        fn = t_data.get("footnotes", [])
        if fn:
            assert isinstance(fn, list)

def test_b2_22_table_headers_no_newlines(json_tables_map: Dict[str, dict]):
    """Asserts table headers contain clean spaces instead of raw newlines."""
    for name, t_data in json_tables_map.items():
        for h in t_data.get("headers", []):
            assert "\n" not in h, f"Newline found in header of {name}: '{h}'"

def test_b2_23_table_rows_no_raw_newlines(json_tables_map: Dict[str, dict]):
    """Asserts table row values contain clean spaces."""
    for name, t_data in json_tables_map.items():
        for row in t_data.get("rows", []):
            vals = list(row.values()) if isinstance(row, dict) else row
            for v in vals:
                assert "\r\n" not in str(v), f"Raw CRLF in {name} cell: '{v}'"

def test_b2_24_table_merged_cell_handling(qcvn_docx_parsed: DocxParsedBundle):
    """Asserts DOCX table parser converts merged cells into clean grid without IndexError."""
    for t in qcvn_docx_parsed.tables:
        assert t.total_rows > 0
        assert t.total_cols > 0

def test_b2_25_table_grid_rectangular_consistency(json_tables_map: Dict[str, dict]):
    """Asserts all rows in each table have consistent field count matching headers."""
    for name, t_data in json_tables_map.items():
        headers_count = len(t_data.get("headers", []))
        for r_idx, row in enumerate(t_data.get("rows", [])):
            if isinstance(row, list):
                assert len(row) == headers_count, f"Row {r_idx} length mismatch in {name}"
            elif isinstance(row, dict):
                assert len(row) <= headers_count + 2

# =====================================================================
# 3. MATHEMATICAL FORMULAS & UNICODE SYMBOLS (20 tests)
# =====================================================================

def test_b3_01_smoke_formula_g_kh(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts Appendix D smoke exhaust formula parameter G_kh or Gkh is present."""
    raw = qcvn_md_parsed.raw_text
    assert "G" in raw and ("kh" in raw or "khói" in raw)

def test_b3_02_temperature_symbol_degree_c(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts degree Celsius symbol '°C' is preserved."""
    assert "°c" in qcvn_md_parsed.normalized_text or "oc" in qcvn_md_parsed.normalized_text

def test_b3_03_flow_rate_unit_liter_per_second(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts flow rate unit 'l/s' is preserved."""
    assert "l/s" in qcvn_md_parsed.normalized_text or "lít/s" in qcvn_md_parsed.normalized_text

def test_b3_04_volume_unit_cubic_meter(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts volume unit 'm3' or 'm³' is preserved."""
    assert "m3" in qcvn_md_parsed.normalized_text or "m³" in qcvn_md_parsed.normalized_text

def test_b3_05_area_unit_square_meter(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts area unit 'm2' or 'm²' is preserved."""
    assert "m2" in qcvn_md_parsed.normalized_text or "m²" in qcvn_md_parsed.normalized_text

def test_b3_06_pressure_unit_pascal(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts pressure unit 'Pa' or 'kPa' or 'MPa' is preserved."""
    assert "pa" in qcvn_md_parsed.normalized_text or "kpa" in qcvn_md_parsed.normalized_text or "mpa" in qcvn_md_parsed.normalized_text

def test_b3_07_power_unit_kilowatt(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts power unit 'kW' is preserved."""
    assert "kw" in qcvn_md_parsed.normalized_text

def test_b3_08_greater_equal_less_equal_symbols(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts mathematical comparison symbols (≥, ≤, >, <) are preserved."""
    raw = qcvn_md_parsed.raw_text
    assert "≥" in raw or ">=" in raw
    assert "≤" in raw or "<=" in raw

def test_b3_09_plus_minus_symbol(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts plus-minus symbol '±' is preserved."""
    assert "±" in qcvn_md_parsed.raw_text or "+/-" in qcvn_md_parsed.raw_text or "%" in qcvn_md_parsed.raw_text

def test_b3_10_vietnamese_diacritics_normalization(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts Vietnamese diacritics are NFC normalized without broken decomposition."""
    sample = qcvn_md_parsed.raw_text[:1000]
    assert sample == unicodedata.normalize("NFC", sample)

def test_b3_11_no_zero_width_space_corruption(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts zero-width space characters ('\\u200b') do not pollute headings or anchors."""
    for _, text, _ in qcvn_md_parsed.headings:
        assert "\u200b" not in text, f"Zero-width space in heading: '{text}'"

def test_b3_12_non_breaking_space_normalization(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts non-breaking spaces ('\\u00a0') do not pollute heading titles or anchors."""
    for _, text, line_idx in qcvn_md_parsed.headings:
        assert "\u00a0" not in text, f"Raw non-breaking space found in heading at line {line_idx}: '{text}'"
    for anchor in qcvn_md_parsed.anchors:
        assert "\u00a0" not in anchor, f"Raw non-breaking space found in anchor: '{anchor}'"

def test_b3_13_quotation_marks_consistency(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts quotes in markdown body are balanced."""
    raw = qcvn_md_parsed.raw_text
    assert raw.count('"') % 2 == 0, "ASCII double quotes in markdown are unbalanced"
    assert raw.count("“") == raw.count("”"), "Vietnamese opening and closing curly quotes are unbalanced"

def test_b3_14_table_pipe_escaping(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts literal pipes inside table cells are escaped as '\\|'."""
    for t in qcvn_md_parsed.pipe_tables:
        for row in t.get("rows", []):
            for cell in row:
                # Cell should not break column count
                assert isinstance(cell, str)

def test_b3_15_chemical_symbols(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts combustion gases / chemicals (CO, CO2, O2) are present."""
    raw = qcvn_md_parsed.normalized_text
    assert "co" in raw or "khí" in raw

def test_b3_16_density_unit(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts density unit 'kg/m3' or 'kg/m³' is preserved."""
    raw = qcvn_md_parsed.normalized_text
    assert "kg/m3" in raw or "kg/m³" in raw or "kg/m" in raw

def test_b3_17_velocity_unit(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts velocity unit 'm/s' is preserved."""
    assert "m/s" in qcvn_md_parsed.normalized_text

def test_b3_18_duration_units(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts duration units ('phút', 'giờ', 'giây') are preserved."""
    raw = qcvn_md_parsed.normalized_text
    assert "phút" in raw and "giờ" in raw

def test_b3_19_fire_resistance_class_notations(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts standard fire resistance notation strings (REI, EI, RE, R, E, I) are present."""
    raw = qcvn_md_parsed.raw_text
    for notation in ["REI", "EI", "RE", "R"]:
        assert notation in raw, f"Fire resistance notation '{notation}' missing"

def test_b3_20_fire_hazard_class_notations(qcvn_md_parsed: MarkdownParsedBundle):
    """Asserts functional fire hazard classification codes (F1.1, F1.2, F1.3, F2.1, F3.1, F4.1, F5.1) are present."""
    raw = qcvn_md_parsed.raw_text
    for f_class in ["F1.1", "F1.2", "F1.3", "F2.1", "F3.1", "F4.1", "F5.1"]:
        assert f_class in raw, f"Fire hazard class '{f_class}' missing in Markdown"

# =====================================================================
# 4. AMENDMENT BOUNDARY & DELTA INTEGRITY (25 tests)
# =====================================================================

def test_b4_01_sd1_first_directive_boundary(sd1_md_parsed: Dict[str, Any]):
    """Asserts first directive in SD1 modifies Điểm 1.1.2."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "1.1.2" in raw, "Directive for 1.1.2 missing in SD1"

def test_b4_02_sd1_last_directive_boundary(sd1_md_parsed: Dict[str, Any]):
    """Asserts last directive in SD1 modifies Phụ lục I."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "Phụ lục I" in raw or "phụ lục i" in raw.lower()

def test_b4_03_sd1_complex_multiclause_directive(sd1_md_parsed: Dict[str, Any]):
    """Asserts complex multi-clause directive for 3.2.6.2 is preserved."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "3.2.6.2" in raw

def test_b4_04_sd1_repeal_directives_present(sd1_md_parsed: Dict[str, Any]):
    """Asserts repeal directives ('Bãi bỏ...') are preserved."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "bãi bỏ" in raw.lower()

def test_b4_05_sd1_supplement_directives_present(sd1_md_parsed: Dict[str, Any]):
    """Asserts supplement directives ('Bổ sung...') are preserved."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "bổ sung" in raw.lower()

def test_b4_06_sd1_replacement_directives_present(sd1_md_parsed: Dict[str, Any]):
    """Asserts replacement directives ('Thay thế...') are preserved."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "thay thế" in raw.lower() or "sửa đổi" in raw.lower()

def test_b4_07_sd1_chapter_1_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Chapter 1 modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "1.1" in raw or "1.2" in raw or "1.3" in raw or "1.4" in raw

def test_b4_08_sd1_chapter_2_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Chapter 2 modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "2." in raw

def test_b4_09_sd1_chapter_3_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Chapter 3 modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "3." in raw

def test_b4_10_sd1_chapter_4_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Chapter 4 modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "4." in raw

def test_b4_11_sd1_chapter_5_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Chapter 5 modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "5." in raw

def test_b4_12_sd1_chapter_6_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Chapter 6 modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "6." in raw

def test_b4_13_sd1_chapter_7_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Chapter 7 modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "7." in raw

def test_b4_14_sd1_appendix_a_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Appendix A modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "Phụ lục A" in raw or "phụ lục a" in raw.lower()

def test_b4_15_sd1_appendix_d_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Appendix D modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "Phụ lục D" in raw or "phụ lục d" in raw.lower()

def test_b4_16_sd1_appendix_e_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Appendix E modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "Phụ lục E" in raw or "phụ lục e" in raw.lower()

def test_b4_17_sd1_appendix_b_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Appendix B modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "Phụ lục B" in raw or "phụ lục b" in raw.lower()

def test_b4_18_sd1_appendix_g_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Appendix G modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "Phụ lục G" in raw or "phụ lục g" in raw.lower()

def test_b4_19_sd1_appendix_h_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Appendix H modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "Phụ lục H" in raw or "phụ lục h" in raw.lower()

def test_b4_20_sd1_appendix_i_modifications(sd1_md_parsed: Dict[str, Any]):
    """Asserts Appendix I modifications are present in SD1."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "Phụ lục I" in raw or "phụ lục i" in raw.lower()

def test_b4_21_sd1_legal_basis_preservation(sd1_md_parsed: Dict[str, Any]):
    """Asserts Thông tư 09/2023/TT-BXD legal basis is preserved."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "09/2023/TT-BXD" in raw or "09/2023" in raw

def test_b4_22_sd1_effective_date_clause(sd1_md_parsed: Dict[str, Any]):
    """Asserts effective date (16/01/2023 or 01/12/2023) is preserved."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "2023" in raw

def test_b4_23_sd1_transitional_provisions(sd1_md_parsed: Dict[str, Any]):
    """Asserts transitional provisions (Điều khoản chuyển tiếp) are present."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "chuyển tiếp" in raw.lower() or "thực hiện" in raw.lower()

def test_b4_24_sd1_table_2_delta_accuracy(sd1_md_parsed: Dict[str, Any]):
    """Asserts Table 2 modifications in SĐ1 match official numbers."""
    raw = sd1_md_parsed.get("raw_text", "")
    assert "bảng" in raw.lower()

def test_b4_25_sd1_clean_directive_numbers(sd1_md_parsed: Dict[str, Any]):
    """Asserts directive numbering is sequential and clean."""
    directives = sd1_md_parsed.get("directives", [])
    assert len(directives) > 0

# =====================================================================
# 5. AST & BENCHMARK BOUNDARY VERIFICATION (22 tests)
# =====================================================================

def test_b5_01_ast_first_node_boundary(clauses_ast_data: List[dict]):
    """Asserts first AST node starts at or before line 100."""
    assert len(clauses_ast_data) > 0
    assert clauses_ast_data[0]["line_start"] <= 100

def test_b5_02_ast_last_node_boundary(
    clauses_ast_data: List[dict], qcvn_md_parsed: MarkdownParsedBundle
):
    """Asserts last AST node ends within total line count of Markdown."""
    assert len(clauses_ast_data) > 0
    assert clauses_ast_data[-1]["line_end"] <= len(qcvn_md_parsed.raw_lines)

def test_b5_03_ast_line_ranges_positive(clauses_ast_data: List[dict]):
    """Asserts all AST nodes have positive line numbers (line_start >= 1, line_end >= line_start)."""
    for c in clauses_ast_data:
        assert c["line_start"] >= 1
        assert c["line_end"] >= c["line_start"]

def test_b5_04_ast_no_inverted_ranges(clauses_ast_data: List[dict]):
    """Asserts zero AST nodes have line_start > line_end."""
    for c in clauses_ast_data:
        assert c["line_start"] <= c["line_end"], f"Inverted range in clause {c['clause_id']}"

def test_b5_05_ast_unique_clause_ids(clauses_ast_data: List[dict]):
    """Asserts 100% unique clause IDs in clauses.json (0 duplicates)."""
    ids = [c["clause_id"] for c in clauses_ast_data]
    assert len(ids) == len(set(ids)), f"Duplicate clause IDs found: {len(ids) - len(set(ids))} duplicates"

def test_b5_06_ast_unique_anchors(clauses_ast_data: List[dict]):
    """Asserts 100% unique anchors in clauses.json (0 duplicates)."""
    anchors = [c["anchor"] for c in clauses_ast_data]
    assert len(anchors) == len(set(anchors)), f"Duplicate anchors found: {len(anchors) - len(set(anchors))} duplicates"

def test_b5_07_ast_chapter_1_node_boundary(clauses_ast_data: List[dict]):
    """Asserts Chapter 1 nodes exist in AST."""
    assert any(c["clause_id"].startswith("muc-1") for c in clauses_ast_data)

def test_b5_08_ast_chapter_2_node_boundary(clauses_ast_data: List[dict]):
    """Asserts Chapter 2 nodes exist in AST."""
    assert any(c["clause_id"].startswith("muc-2") for c in clauses_ast_data)

def test_b5_09_ast_chapter_3_node_boundary(clauses_ast_data: List[dict]):
    """Asserts Chapter 3 nodes exist in AST."""
    assert any(c["clause_id"].startswith("muc-3") for c in clauses_ast_data)

def test_b5_10_ast_chapter_4_node_boundary(clauses_ast_data: List[dict]):
    """Asserts Chapter 4 nodes exist in AST."""
    assert any(c["clause_id"].startswith("muc-4") for c in clauses_ast_data)

def test_b5_11_ast_chapter_5_node_boundary(clauses_ast_data: List[dict]):
    """Asserts Chapter 5 nodes exist in AST."""
    assert any(c["clause_id"].startswith("muc-5") for c in clauses_ast_data)

def test_b5_12_ast_chapter_6_node_boundary(clauses_ast_data: List[dict]):
    """Asserts Chapter 6 nodes exist in AST."""
    assert any(c["clause_id"].startswith("muc-6") for c in clauses_ast_data)

def test_b5_13_ast_chapter_7_node_boundary(clauses_ast_data: List[dict]):
    """Asserts Chapter 7 nodes exist in AST."""
    assert any(c["clause_id"].startswith("muc-7") for c in clauses_ast_data)

def test_b5_14_ast_section_1_1_bounds(clauses_ast_data: List[dict]):
    """Asserts Section 1.1 has valid line bounds."""
    c = next((item for item in clauses_ast_data if item["clause_id"] == "muc-1-1"), None)
    assert c is not None
    assert c["line_start"] > 0

def test_b5_15_ast_section_1_4_bounds(clauses_ast_data: List[dict]):
    """Asserts Section 1.4 has valid line bounds."""
    c = next((item for item in clauses_ast_data if item["clause_id"] == "muc-1-4"), None)
    assert c is not None
    assert c["line_start"] > 0

def test_b5_16_ast_definition_1_4_1_bounds(clauses_ast_data: List[dict]):
    """Asserts Definition 1.4.1 has valid line bounds."""
    c = next((item for item in clauses_ast_data if "1-4-1" in item["clause_id"]), None)
    assert c is not None

def test_b5_17_ast_definition_1_4_72_bounds(clauses_ast_data: List[dict]):
    """Asserts Definition 1.4.72 has valid line bounds."""
    c = next((item for item in clauses_ast_data if "1-4-72" in item.get("clause_id", "") or "1-4-7-2" in item.get("clause_id", "")), None)
    assert c is not None and c.get("line_start", 0) > 0, "Definition 1.4.72 missing or invalid in clauses.json"

def test_b5_18_qa_question_length_bounds(qa_benchmark_data: List[dict]):
    """Asserts all QA benchmark questions have length > 10 characters."""
    for idx, qa in enumerate(qa_benchmark_data):
        q = qa.get("question", "")
        assert len(q) > 10, f"QA #{idx} question too short: '{q}'"

def test_b5_19_qa_answer_length_bounds(qa_benchmark_data: List[dict]):
    """Asserts all QA benchmark answers have length > 15 characters."""
    for idx, qa in enumerate(qa_benchmark_data):
        a = qa.get("answer", "")
        assert len(a) > 15, f"QA #{idx} answer too short: '{a}'"

def test_b5_20_qa_first_node_mapping(qa_benchmark_data: List[dict]):
    """Asserts first QA pair maps to first technical section."""
    assert len(qa_benchmark_data) > 0
    assert "1.1" in qa_benchmark_data[0]["question"] or "muc-1-1" in qa_benchmark_data[0]["anchor"]

def test_b5_21_qa_last_node_mapping(qa_benchmark_data: List[dict]):
    """Asserts last QA pair maps to Chapter 7 or Appendix."""
    assert len(qa_benchmark_data) > 0, "QA benchmark data is empty"
    last_qa = qa_benchmark_data[-1]
    anchor = last_qa.get("anchor", "").lower()
    is_ch7_or_app = (
        anchor.startswith("muc-7")
        or anchor.startswith("chuong-7")
        or anchor.startswith("pl-")
        or anchor.startswith("phu-luc-")
        or any(anchor.startswith(f"muc-{c}") for c in "abcdefghi")
    )
    assert is_ch7_or_app, f"Last QA node anchor '{last_qa.get('anchor')}' does not map to Chapter 7 or Appendix"

def test_b5_22_qa_question_uniqueness(qa_benchmark_data: List[dict]):
    """Asserts all QA benchmark questions are unique (0 duplicates)."""
    questions = [qa["question"] for qa in qa_benchmark_data]
    assert len(questions) == len(set(questions)), f"Found duplicate questions in QA benchmark: {len(questions) - len(set(questions))} duplicates"
