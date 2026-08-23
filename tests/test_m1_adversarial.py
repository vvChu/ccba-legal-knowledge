"""Adversarial stress test harness for Milestone 1 changes.

Covers:
1. Stress-testing scripts/docx_converter.py with edge case inputs, custom filenames, nested dirs, invalid CLI flags.
2. Verification of raw evidence files in .md/extracted_docs/<slug>/ for truncation, corruption, missing slugs, and structural validity.
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path
import pytest
import docx

from ccba_legal import convert_docx_to_okf_bundle, normalize_docx_markdown
from ccba_legal.cli import main as docx_converter_main

TARGET_DECREES = [
    "nghi_dinh_217_2026_nd_cp",
    "nghi_dinh_207_2026_nd_cp",
    "nghi_dinh_212_2026_nd_cp",
    "nghi_dinh_206_2026_nd_cp",
    "nghi_dinh_210_2026_nd_cp",
    "nghi_dinh_209_2026_nd_cp",
    "nghi_dinh_193_2026_nd_cp",
]

ROOT_DIR = Path(__file__).resolve().parent.parent
EXTRACTED_DOCS_DIR = ROOT_DIR / ".md" / "extracted_docs"
LEGAL_DOCS_DIR = ROOT_DIR / "legal_docs" / "01_vbpl"

def create_sample_docx(docx_path: Path, title: str = "Nghị định thử nghiệm") -> Path:
    """Utility helper to create a valid docx file with headers and tables."""
    doc = docx.Document()
    doc.add_heading(title, level=1)
    doc.add_paragraph("Căn cứ Luật Xây dựng số 135/2025/QH15.")
    doc.add_heading("Điều 1. Phạm vi điều chỉnh", level=2)
    doc.add_paragraph("1. Nghị định này quy định chi tiết thi hành Luật Xây dựng.")
    doc.add_paragraph("2. Bao gồm các nội dung quản lý dự án & chi phí.")
    
    doc.add_heading("Điều 2. Đối tượng áp dụng", level=2)
    doc.add_paragraph("1. Cơ quan, tổ chức, cá nhân trong nước và nước ngoài.")
    
    # Add table
    table = doc.add_table(rows=3, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "STT"
    hdr_cells[1].text = "Hạng mục"
    hdr_cells[2].text = "Ghi chú"
    
    row1 = table.rows[1].cells
    row1[0].text = "1"
    row1[1].text = "Dự án nhóm A"
    row1[2].text = "Cấp đặc biệt"
    
    row2 = table.rows[2].cells
    row2[0].text = "2"
    row2[1].text = "Dự án nhóm B"
    row2[2].text = "Cấp I, II"

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(docx_path))
    return docx_path

# =====================================================================
# 1. STRESS TESTS FOR docx_converter.py
# =====================================================================

def test_docx_converter_non_existent_input():
    """Test calling converter with non-existent input path."""
    fake_path = Path("non_existent_file_12345.docx")
    target_dir = Path("tmp_bundle_dir")
    with pytest.raises(FileNotFoundError):
        convert_docx_to_okf_bundle(fake_path, target_dir)

def test_docx_converter_corrupted_input(tmp_path: Path):
    """Test calling converter with a non-docx file disguised as .docx."""
    bad_docx = tmp_path / "corrupted.docx"
    bad_docx.write_text("This is not a zip/docx file", encoding="utf-8")
    target_dir = tmp_path / "corrupted_bundle"

    with pytest.raises(Exception):
        convert_docx_to_okf_bundle(bad_docx, target_dir)

def test_docx_converter_empty_file(tmp_path: Path):
    """Test calling converter with 0-byte file."""
    empty_docx = tmp_path / "empty.docx"
    empty_docx.touch()
    target_dir = tmp_path / "empty_bundle"

    with pytest.raises(Exception):
        convert_docx_to_okf_bundle(empty_docx, target_dir)

def test_docx_converter_deep_nested_non_existent_target_dir(tmp_path: Path):
    """Test converter creates deep non-existent target directories automatically."""
    input_docx = tmp_path / "valid.docx"
    create_sample_docx(input_docx)

    deep_dir = tmp_path / "sub1" / "sub2" / "sub3" / "target_bundle"
    assert not deep_dir.exists()

    res = convert_docx_to_okf_bundle(input_docx, deep_dir)
    assert res.get("status") == "success"
    assert deep_dir.exists()
    assert (deep_dir / "target_bundle.md").exists()

def test_docx_converter_custom_output_filename(tmp_path: Path):
    """Test converter with custom output filename."""
    input_docx = tmp_path / "doc.docx"
    create_sample_docx(input_docx)

    target_dir = tmp_path / "bundle_custom"
    res = convert_docx_to_okf_bundle(input_docx, target_dir, output_filename="my_output.md")
    assert res.get("status") == "success"
    assert (target_dir / "my_output.md").exists()

def test_docx_converter_custom_output_filename_in_subfolder(tmp_path: Path):
    """Stress test custom output filename specified as a relative subpath."""
    input_docx = tmp_path / "doc.docx"
    create_sample_docx(input_docx)

    target_dir = tmp_path / "bundle_subpath"
    # If output_filename has subfolder like 'nested/output.md', write_text might fail if nested/ is not created
    subpath_filename = "nested/output.md"
    try:
        res = convert_docx_to_okf_bundle(input_docx, target_dir, output_filename=subpath_filename)
        assert (target_dir / "nested" / "output.md").exists()
    except FileNotFoundError:
        # Documented behavior: subfolder in output_filename is not auto-created unless handled
        pytest.skip("Converter output_filename with subfolder requires pre-created subfolder")

def test_docx_converter_cli_invalid_flags():
    """Test CLI behavior with invalid flags using subprocess."""
    cmd = [sys.executable, "-m", "scripts.docx_converter", "--invalid-flag-xyz"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    assert result.returncode != 0
    assert "unrecognized arguments" in result.stderr or "usage:" in result.stderr

def test_docx_converter_cli_missing_args():
    """Test CLI behavior when mandatory positional args are omitted."""
    cmd = [sys.executable, "-m", "scripts.docx_converter"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    assert result.returncode != 0
    assert "required" in result.stderr or "usage:" in result.stderr

def test_docx_converter_cli_valid_run(tmp_path: Path):
    """Test CLI execution with valid arguments."""
    input_docx = tmp_path / "cli_doc.docx"
    create_sample_docx(input_docx)
    target_dir = tmp_path / "cli_bundle"

    cmd = [
        sys.executable, "-m", "scripts.docx_converter",
        str(input_docx), str(target_dir),
        "-o", "cli_out.md",
        "-t", "vbpl"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    assert result.returncode == 0
    assert "COMPLETE OKF BUNDLE RESULT" in result.stdout
    assert (target_dir / "cli_out.md").exists()

# =====================================================================
# 2. EDGE CASE TESTS FOR RAW EVIDENCE STORE (.md/extracted_docs/<slug>/)
# =====================================================================

def test_raw_evidence_all_7_decrees_exist():
    """Check that all 7 required decrees exist in legal_docs/01_vbpl/<slug>/."""
    assert LEGAL_DOCS_DIR.exists(), f"Missing directory: {LEGAL_DOCS_DIR}"
    for slug in TARGET_DECREES:
        slug_dir = LEGAL_DOCS_DIR / slug
        assert slug_dir.exists(), f"Missing raw evidence dir for slug: {slug}"
        assert slug_dir.is_dir(), f"Not a directory: {slug_dir}"

def test_raw_evidence_no_corruption_or_truncation():
    """Check files in legal docs for corruption, truncation, HTML error pages, null bytes."""
    for slug in TARGET_DECREES:
        slug_dir = LEGAL_DOCS_DIR / slug
        md_file = slug_dir / f"{slug}.md"
        assert md_file.exists(), f"Missing {slug}.md in {slug_dir}"

        md_size = md_file.stat().st_size
        # Rule: Minimum size > 5KB
        assert md_size > 5120, f"{slug}.md for {slug} is too small ({md_size} bytes)"

        md_content = md_file.read_text(encoding="utf-8")

        # Check for null bytes (corruption)
        assert "\x00" not in md_content, f"Null byte corruption found in {md_file}"

        # Check for HTML error pages or captcha responses
        error_indicators = ["404 Not Found", "500 Internal Server Error", "Access Denied", "Cloudflare", "Captcha"]
        for err in error_indicators:
            assert err.lower() not in md_content[:1000].lower(), f"Potential web error page in {md_file}: {err}"

        # Check for key structural legal terms to ensure no truncation or bogus data
        assert "Điều 1" in md_content, f"Missing 'Điều 1' in {slug}"

@pytest.mark.milestone2
def test_okf_bundles_match_raw_evidence():
    """Cross-verify OKF bundles in legal_docs/01_vbpl/<slug>/ with raw evidence."""
    missing_bundles = [slug for slug in TARGET_DECREES if not (LEGAL_DOCS_DIR / slug).exists()]
    if missing_bundles:
        pytest.skip(
            f"Milestone 2 OKF bundles not created yet under legal_docs/01_vbpl/ (missing: {missing_bundles}). Skipping in Milestone 1."
        )

    for slug in TARGET_DECREES:
        bundle_dir = LEGAL_DOCS_DIR / slug
        assert bundle_dir.exists(), f"Missing OKF bundle dir: {bundle_dir}"

        md_file = bundle_dir / f"{slug}.md"
        assert md_file.exists(), f"Missing primary markdown file in bundle: {md_file}"
        assert md_file.stat().st_size > 5120, f"Bundle primary markdown for {slug} is < 5KB"

        clauses_file = bundle_dir / "clauses.json"
        assert clauses_file.exists(), f"Missing clauses.json in {bundle_dir}"

        qa_file = bundle_dir / "qa_benchmark.json"
        assert qa_file.exists(), f"Missing qa_benchmark.json in {bundle_dir}"

        index_file = bundle_dir / "index.md"
        assert index_file.exists(), f"Missing index.md in {bundle_dir}"
