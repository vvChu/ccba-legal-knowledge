"""Tests for raw evidence store (Requirement R1)."""

from pathlib import Path
import pytest

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


def test_raw_evidence_directories_exist():
    assert EXTRACTED_DOCS_DIR.exists(), f"{EXTRACTED_DOCS_DIR} does not exist"
    for slug in TARGET_DECREES:
        decree_dir = EXTRACTED_DOCS_DIR / slug
        assert decree_dir.exists(), f"Directory missing for {slug}: {decree_dir}"
        assert decree_dir.is_dir()


def test_raw_evidence_file_sizes():
    for slug in TARGET_DECREES:
        decree_dir = EXTRACTED_DOCS_DIR / slug
        raw_files = list(decree_dir.glob("raw_text.txt")) + list(decree_dir.glob(f"{slug}.md")) + list(decree_dir.glob("*.docx"))
        assert len(raw_files) > 0, f"No raw evidence files found in {decree_dir}"
        max_size = max(f.stat().st_size for f in raw_files)
        assert max_size > 5120, f"Raw evidence for {slug} is only {max_size} bytes (must be > 5KB)"
