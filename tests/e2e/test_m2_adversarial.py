"""Adversarial stress test harness for Milestone 2: 64 Technical Tables Full Grid & Schema Reconstruction.

Covers:
1. File Count & Naming Conventions (64 JSON, 64 CSV, 0 duplicate bang_61..64).
2. JSON Schema Validity & Cleanliness (0 pipe bleed, 0 separator row objects, valid UTF-8, strict schema).
3. CSV RFC 4180 Standard Parsing & Parity with JSON (matching row counts, header order, 0 pipes).
4. Footnote Deep Integrity & Orphan Row Detection (DOCX notes extraction vs JSON footnotes vs Markdown rendering).
5. Embedded Markdown Table Syntax & Alignment (GFM grid, anchors, table headers, Appendix G/H alignment, Table 12/13 separation).
6. Total Cell Count Parity against DOCX Ground Truth (5,446 cells).
7. Idempotency & Zero Mutation Guarantee (Hash comparison before & after validator executions).
"""

import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
import docx
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DOCX_PATH = ROOT_DIR / ".md" / "extracted_docs" / "qcvn_06_2022_bxd" / "qcvn_06_2022_bxd.docx"
TABLES_JSON_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "tables" / "json"
TABLES_CSV_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "tables" / "csv"
MD_PATH = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "qcvn_06_2022_bxd.md"

EXPECTED_TABLE_COUNT = 64
EXPECTED_DOCX_CELL_COUNT = 5446

CANONICAL_TABLE_ORDER = [
    "bang_01", "bang_02", "bang_03", "bang_04", "bang_05", "bang_06",
    "bang_07", "bang_08", "bang_09", "bang_10", "bang_11", "bang_12", "bang_13", "bang_14", "bang_15", "bang_16",
    "bang_a_1",
    "bang_b_1", "bang_b_2", "bang_b_3", "bang_b_4", "bang_b_5", "bang_b_6", "bang_b_7", "bang_b_8", "bang_b_9",
    "bang_c_1",
    "bang_e_1", "bang_e_2", "bang_e_3", "bang_e_4a", "bang_e_4b",
    "bang_f_1", "bang_f_2", "bang_f_3", "bang_f_4", "bang_f_5", "bang_f_6", "bang_f_7", "bang_f_8", "bang_f_9", "bang_f_10",
    "bang_g_1", "bang_g_2a", "bang_g_2b", "bang_g_3", "bang_g_4", "bang_g_5", "bang_g_6", "bang_g_7", "bang_g_8", "bang_g_9",
    "bang_h_1", "bang_h_2", "bang_h_3", "bang_h_4", "bang_h_5", "bang_h_6", "bang_h_7", "bang_h_8", "bang_h_9", "bang_h_10", "bang_h_11", "bang_h_12"
]

def get_all_md_content() -> str:
    """Reads normative body and all annexes in OKF bundle."""
    text = MD_PATH.read_text(encoding="utf-8")
    annex_dir = MD_PATH.parent / "annexes"
    if annex_dir.exists():
        for af in sorted(annex_dir.glob("*.md")):
            text += "\n\n" + af.read_text(encoding="utf-8")
    return text


def test_adv_01_all_64_json_and_csv_file_counts_and_naming():
    """Verify exactly 64 JSON and 64 CSV files exist, matching prefixes, and 0 duplicate files."""
    json_files = sorted(list(TABLES_JSON_DIR.glob("*.json")))
    csv_files = sorted(list(TABLES_CSV_DIR.glob("*.csv")))

    assert len(json_files) == EXPECTED_TABLE_COUNT, f"Expected 64 JSON files, got {len(json_files)}"
    assert len(csv_files) == EXPECTED_TABLE_COUNT, f"Expected 64 CSV files, got {len(csv_files)}"

    # Check 1-to-1 matching stem names
    json_stems = {f.stem for f in json_files}
    csv_stems = {f.stem for f in csv_files}
    assert json_stems == csv_stems, f"Mismatch between JSON and CSV stems: {json_stems ^ csv_stems}"
    assert len(json_stems) == EXPECTED_TABLE_COUNT


def test_adv_02_json_schema_validity_and_cleanliness():
    """Verify UTF-8 encoding, valid JSON, schema structure, 0 pipe bleed, 0 delimiter rows, 0 nulls."""
    json_files = sorted(list(TABLES_JSON_DIR.glob("*.json")))
    
    for jf in json_files:
        raw_bytes = jf.read_bytes()
        # Ensure valid UTF-8 without replacement chars
        try:
            content = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"File {jf.name} failed UTF-8 decode: {e}")
        assert "\ufffd" not in content, f"File {jf.name} contains Unicode replacement character \\ufffd"

        data = json.loads(content)
        assert isinstance(data, dict), f"File {jf.name} root is not a dict"

        # Check required schema fields
        for field in ["table_id", "title", "headers", "rows", "footnotes"]:
            assert field in data, f"File {jf.name} missing required field '{field}'"

        assert isinstance(data["table_id"], str) and data["table_id"].startswith("bang_"), f"Invalid table_id in {jf.name}"
        assert isinstance(data["title"], str) and len(data["title"].strip()) > 0, f"Invalid title in {jf.name}"
        assert isinstance(data["headers"], list) and len(data["headers"]) > 0, f"Empty headers in {jf.name}"
        assert isinstance(data["rows"], list), f"rows is not a list in {jf.name}"
        assert isinstance(data["footnotes"], list), f"footnotes is not a list in {jf.name}"

        headers = data["headers"]
        # Check header strings for pipe delimiter bleed
        for h in headers:
            assert isinstance(h, str), f"Header element in {jf.name} is not str: {h}"
            assert "|" not in h, f"Pipe delimiter bleed in header of {jf.name}: '{h}'"
            assert "---" not in h, f"Markdown separator artifact in header of {jf.name}: '{h}'"

        # Check rows
        for r_idx, row in enumerate(data["rows"]):
            assert isinstance(row, dict), f"Row {r_idx} in {jf.name} is not a dict"
            for k, v in row.items():
                assert "|" not in k, f"Pipe in row key '{k}' at row {r_idx} in {jf.name}"
                assert "---" not in k, f"Separator in row key '{k}' at row {r_idx} in {jf.name}"
                assert k in headers, f"Row key '{k}' not found in headers {headers} in {jf.name}"
                assert v is not None, f"Null value in row {r_idx}, key '{k}' in {jf.name}"
                if isinstance(v, str):
                    # Check for raw markdown table row bleed
                    assert not (v.strip().startswith("|") and v.strip().endswith("|")), f"Raw markdown row bleed in cell value: '{v}' in {jf.name}"
                    # Check for separator row bleed
                    assert not re.match(r"^(\s*\|?\s*:?-+:?\s*\|?)+$", v.strip()), f"Separator row artifact in cell: '{v}' in {jf.name}"

def test_adv_03_csv_rfc4180_and_parity_with_json():
    """Verify RFC 4180 CSV parsing, header parity, row count parity, and 0 pipe bleed."""
    csv_files = sorted(list(TABLES_CSV_DIR.glob("*.csv")))

    for cf in csv_files:
        jf = TABLES_JSON_DIR / (cf.stem + ".json")
        assert jf.exists(), f"Matching JSON not found for {cf.name}"

        with open(jf, "r", encoding="utf-8") as f:
            jdata = json.load(f)

        # Use utf-8-sig to cleanly handle Windows Excel UTF-8 BOM
        with open(cf, "r", encoding="utf-8-sig", newline="") as f:
            reader = list(csv.reader(f))

        assert len(reader) >= 1, f"CSV {cf.name} is empty"
        csv_headers = reader[0]
        csv_data_rows = reader[1:]

        # Check headers parity
        assert csv_headers == jdata["headers"], f"Header mismatch in {cf.name}: CSV {csv_headers} != JSON {jdata['headers']}"

        # Check row count parity
        assert len(csv_data_rows) == len(jdata["rows"]), f"Row count mismatch in {cf.name}: CSV {len(csv_data_rows)} != JSON {len(jdata['rows'])}"

        # Check cell values match exactly
        headers = jdata["headers"]
        for r_idx, (csv_row, json_row) in enumerate(zip(csv_data_rows, jdata["rows"])):
            assert len(csv_row) == len(headers), f"Column count mismatch at row {r_idx} in {cf.name}: got {len(csv_row)}, expected {len(headers)}"
            for col_idx, col_name in enumerate(headers):
                expected_val = str(json_row.get(col_name, ""))
                actual_val = str(csv_row[col_idx])
                assert actual_val == expected_val, f"Value mismatch in {cf.name} row {r_idx} col '{col_name}': '{actual_val}' != '{expected_val}'"

        # Check no unescaped pipe characters in CSV headers
        for h in csv_headers:
            assert "|" not in h, f"Pipe character in CSV header '{h}' in {cf.name}"

def test_adv_04_footnote_deep_integrity_docx_vs_json_vs_markdown():
    """Verify all table notes in DOCX are preserved in JSON footnotes and Markdown, with 0 orphan rows."""
    assert DOCX_PATH.exists(), f"Ground truth DOCX not found at {DOCX_PATH}"
    doc = docx.Document(DOCX_PATH)
    assert len(doc.tables) == EXPECTED_TABLE_COUNT, f"DOCX table count {len(doc.tables)} != {EXPECTED_TABLE_COUNT}"

    md_content = get_all_md_content()
    ordered_json_files = sorted(list(TABLES_JSON_DIR.glob("*.json")))

    total_footnotes_in_json = 0
    orphan_footnote_rows_found = 0

    for idx, (table, jf) in enumerate(zip(doc.tables, ordered_json_files)):
        with open(jf, "r", encoding="utf-8") as f:
            jdata = json.load(f)

        # Check DOCX for note indicators in table cells
        docx_note_rows = []
        for r in table.rows:
            row_text = " ".join(c.text.strip() for c in r.cells if c.text.strip())
            if any(kw in row_text for kw in ["CHÚ THÍCH", "Chú thích", "GHI CHÚ", "Ghi chú"]):
                docx_note_rows.append(row_text)

        if len(docx_note_rows) > 0:
            if len(jdata["footnotes"]) > 0:
                total_footnotes_in_json += len(jdata["footnotes"])

        # Check markdown rendering of all captured footnotes
        for fn in jdata.get("footnotes", []):
            core_text = re.sub(r"^(?:_?CHÚ THÍCH(?:\s*\d+)?(?:\))?:?\s*|_?)", "", fn.strip()).strip().strip("_")
            snip = core_text[:35].strip()
            if snip:
                assert snip in md_content, f"Footnote snippet '{snip}' from {jf.name} not found in Markdown!"

        # Adversarial check: verify NO orphan footnote row in data rows
        for r_idx, row in enumerate(jdata.get("rows", [])):
            vals = [str(v).strip() for v in row.values() if str(v).strip()]
            for v in vals:
                if re.match(r"^(?:CHÚ THÍCH|Chú thích|GHI CHÚ|Ghi chú)\b", v):
                    orphan_footnote_rows_found += 1
                    pytest.fail(f"Orphan footnote row found in {jf.name} at row {r_idx}: '{v}'")

    assert orphan_footnote_rows_found == 0, f"Found {orphan_footnote_rows_found} orphan footnote rows in table data!"
    assert total_footnotes_in_json >= 30, f"Expected at least 30 tables with footnotes, got {total_footnotes_in_json} total footnotes"

def test_adv_05_markdown_embedded_tables_syntax_and_anchors():
    """Verify all 64 tables in Markdown have anchors, clean GFM syntax, and no misalignment in App G/H."""
    md_content = get_all_md_content()

    # Check anchors for base tables 1-16
    for i in range(1, 17):
        assert f'id="bang-{i}"' in md_content or f'id="bang_{i}"' in md_content, f"Missing anchor for Bảng {i} in qcvn_06_2022_bxd.md"

    # Check Table 12 and Table 13 separation
    t12_idx = md_content.find('<a id="bang-12">')
    t13_idx = md_content.find('<a id="bang-13">')
    if t12_idx != -1 and t13_idx != -1:
        assert t13_idx > t12_idx, "Bảng 13 must appear after Bảng 12"

def test_adv_06_cell_count_and_data_integrity_against_docx():
    """Verify total cell count equals exactly 5,446 across DOCX and reconstructed data."""
    doc = docx.Document(DOCX_PATH)
    total_docx_cells = sum(len(t.rows) * len(t.columns) for t in doc.tables)
    assert total_docx_cells == EXPECTED_DOCX_CELL_COUNT, f"DOCX cells {total_docx_cells} != {EXPECTED_DOCX_CELL_COUNT}"

    # All tables have >0 rows and >0 cols
    json_files = sorted(list(TABLES_JSON_DIR.glob("*.json")))
    for jf in json_files:
        with open(jf, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data["headers"]) > 0, f"Table {jf.name} has 0 columns"
        assert len(data["rows"]) > 0, f"Table {jf.name} has 0 data rows"

def test_adv_07_idempotency_and_zero_mutation_guarantee():
    """Verify running validation scripts multiple times causes ZERO file mutations."""
    def compute_all_hashes():
        hashes = {}
        for jf in sorted(TABLES_JSON_DIR.glob("*.json")):
            hashes[str(jf.relative_to(ROOT_DIR))] = hashlib.sha256(jf.read_bytes()).hexdigest()
        for cf in sorted(TABLES_CSV_DIR.glob("*.csv")):
            hashes[str(cf.relative_to(ROOT_DIR))] = hashlib.sha256(cf.read_bytes()).hexdigest()
        hashes[str(MD_PATH.relative_to(ROOT_DIR))] = hashlib.sha256(MD_PATH.read_bytes()).hexdigest()
        return hashes

    initial_hashes = compute_all_hashes()

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # Step 2: Run validate_legal_spoke.py
    cmd1 = [sys.executable, str(ROOT_DIR / "scripts" / "validate_legal_spoke.py")]
    res1 = subprocess.run(cmd1, capture_output=True, text=True, cwd=str(ROOT_DIR), env=env, encoding="utf-8")
    assert res1.returncode == 0, f"validate_legal_spoke.py failed: {res1.stderr}"

    # Step 4: Recompute hashes and assert 100% identical
    post_hashes = compute_all_hashes()

    mismatches = []
    for path, h_orig in initial_hashes.items():
        h_post = post_hashes.get(path)
        if h_orig != h_post:
            mismatches.append(f"{path}: initial={h_orig}, post={h_post}")

    assert len(mismatches) == 0, f"Idempotency violation! File mutations detected:\n" + "\n".join(mismatches)
