"""Unit tests for CCBA Legal Spoke Automated Validator."""

from pathlib import Path
from scripts.validate_legal_spoke import LegalSpokeValidator


def test_validator_on_workspace(tmp_path: Path) -> None:
    """Test LegalSpokeValidator on a mock workspace structure."""
    # 1. Setup mock workspace
    registry_path = tmp_path / "legal_registry.yaml"
    registry_content = """version: 0.2.0
spoke_name: ccba-legal-knowledge
registry_summary:
  total_documents: 1
laws:
  - id: test_law_1
    title: Test Law
    bundle_path: legal_docs/01_vbpl/test_law_1
"""
    registry_path.write_text(registry_content, encoding="utf-8")

    bundle_dir = tmp_path / "legal_docs" / "01_vbpl" / "test_law_1"
    bundle_dir.mkdir(parents=True)
    index_md = bundle_dir / "index.md"
    index_md.write_text("---\ntitle: Test Law\n---\n# Test Law\nContent", encoding="utf-8")

    # 2. Run validator
    validator = LegalSpokeValidator(tmp_path)
    errors, warnings = validator.validate_registry()
    assert errors == 0

    errors, warnings = validator.validate_okf_bundles()
    assert errors == 0

    assert validator.run_all_checks() is True


def test_validator_detects_missing_registry(tmp_path: Path) -> None:
    """Test LegalSpokeValidator fails when registry is missing."""
    validator = LegalSpokeValidator(tmp_path)
    errors, warnings = validator.validate_registry()
    assert errors > 0
    assert "missing" in validator.errors[0].lower()
