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
    pdf_status: AVAILABLE
    cong_bao_number: "123/2026"
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

def test_validator_detects_missing_registry(tmp_path: Path) -> None:
    """Test LegalSpokeValidator fails when registry is missing."""
    validator = LegalSpokeValidator(tmp_path)
    errors, warnings = validator.validate_registry()
    assert errors > 0
    assert "missing" in validator.errors[0].lower()


def test_subgate_5_3_detects_banned_expired_document_with_active_status(tmp_path: Path) -> None:
    """Sub-Gate 5.3 must fail if banned expired statute (e.g. 10/2021/NĐ-CP) is active."""
    registry_path = tmp_path / "legal_registry.yaml"
    registry_content = """version: 0.2.0
laws:
  - id: 10_2021_nd_cp
    title: Nghị định 10/2021/NĐ-CP
    document_number: 10/2021/NĐ-CP
    bundle_path: legal_docs/01_vbpl/10_2021_nd_cp
    status: active
    pdf_status: AVAILABLE
    cong_bao_number: "123/2021"
"""
    registry_path.write_text(registry_content, encoding="utf-8")
    validator = LegalSpokeValidator(tmp_path)
    validator._validate_legal_validity_and_in_force()
    assert any("RULE-3.1" in err and "strictly banned" in err for err in validator.errors)


def test_subgate_5_3_detects_expired_date_in_past_with_active_status(tmp_path: Path) -> None:
    """Sub-Gate 5.3 must fail if expiration_date <= today but status is active."""
    registry_path = tmp_path / "legal_registry.yaml"
    registry_content = """version: 0.2.0
laws:
  - id: old_law
    title: Old Law
    document_number: 99/2020/NĐ-CP
    bundle_path: legal_docs/01_vbpl/old_law
    status: active
    expiration_date: "2021-01-01"
    pdf_status: AVAILABLE
    cong_bao_number: "123/2020"
"""
    registry_path.write_text(registry_content, encoding="utf-8")
    validator = LegalSpokeValidator(tmp_path)
    validator._validate_legal_validity_and_in_force()
    assert any("has expiration_date" in err and "Must be 'expired'" in err for err in validator.errors)


def test_subgate_5_3_detects_status_split_brain(tmp_path: Path) -> None:
    """Sub-Gate 5.3 must fail if registry status does not match bundle metadata.yaml."""
    registry_path = tmp_path / "legal_registry.yaml"
    registry_content = """version: 0.2.0
laws:
  - id: doc_split
    title: Split Document
    document_number: 123/2026/NĐ-CP
    bundle_path: legal_docs/01_vbpl/doc_split
    status: active
    pdf_status: AVAILABLE
    cong_bao_number: "123/2026"
"""
    registry_path.write_text(registry_content, encoding="utf-8")
    bundle_dir = tmp_path / "legal_docs" / "01_vbpl" / "doc_split"
    bundle_dir.mkdir(parents=True)
    (bundle_dir / "metadata.yaml").write_text("status: expired\n", encoding="utf-8")

    validator = LegalSpokeValidator(tmp_path)
    validator._validate_legal_validity_and_in_force()
    assert any("Split-Brain Status Error" in err for err in validator.errors)


def test_gate_4_detects_empty_ast_clauses(tmp_path: Path) -> None:
    """Gate 4 must flag Empty AST Error when clauses.json has 0 clauses."""
    bundle_dir = tmp_path / "legal_docs" / "01_vbpl" / "custom_vbpl"
    bundle_dir.mkdir(parents=True)
    (bundle_dir / "custom_vbpl.md").write_text("### Điều 1. Điều khoản đầu tiên\nNội dung", encoding="utf-8")
    (bundle_dir / "clauses.json").write_text("[]", encoding="utf-8")

    validator = LegalSpokeValidator(tmp_path)
    validator._check_vbpl_fake_data(bundle_dir)
    assert any("Empty AST Error" in err for err in validator.errors)


def test_gate_4_detects_missing_ast_clauses(tmp_path: Path) -> None:
    """Gate 4 must flag Missing AST Error when clauses.json is missing on disk."""
    bundle_dir = tmp_path / "legal_docs" / "01_vbpl" / "custom_vbpl_no_ast"
    bundle_dir.mkdir(parents=True)
    (bundle_dir / "custom_vbpl_no_ast.md").write_text("### Điều 1. Điều khoản đầu tiên\nNội dung", encoding="utf-8")

    validator = LegalSpokeValidator(tmp_path)
    validator._check_vbpl_fake_data(bundle_dir)
    assert any("Missing AST Error" in err for err in validator.errors)
