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


def test_subgate_5_3_transitive_dag_detects_superseded_active_document(tmp_path: Path) -> None:
    """Sub-Gate 5.3 DAG BFS must automatically detect when active doc replaces another active doc."""
    registry_path = tmp_path / "legal_registry.yaml"
    registry_content = """version: 0.2.0
standards:
  - id: QCVN-10-2025-BCA
    title: QCVN 10:2025/BCA
    document_number: QCVN 10:2025/BCA
    bundle_path: legal_docs/02_qcvn/qcvn_10_2025_bca
    status: active
    relations:
      replaces: TCVN-3890-2023
  - id: TCVN-3890-2023
    title: TCVN 3890:2023
    document_number: TCVN 3890:2023
    bundle_path: legal_docs/03_tcvn/tcvn_3890_2023
    status: active
"""
    registry_path.write_text(registry_content, encoding="utf-8")
    validator = LegalSpokeValidator(tmp_path)
    validator._validate_legal_validity_and_in_force()
    assert any("TCVN-3890-2023" in err and "strictly banned from status: active" in err for err in validator.errors)


def test_gate_1_detects_windows_backslashes_in_registry_paths(tmp_path: Path) -> None:
    """Gate 1 must raise Registry Format Error if any path field contains Windows backslash."""
    registry_path = tmp_path / "legal_registry.yaml"
    registry_content = r"""version: 0.2.0
laws:
  - id: test_backslash_doc
    title: Test Backslash Doc
    bundle_path: legal_docs\01_vbpl\test_backslash_doc
    pdf_path: legal_docs\01_vbpl\test_backslash_doc\sources\test.pdf
    raw_scan_pdf: legal_docs\01_vbpl\test_backslash_doc\sources\test_raw_scan.pdf
    source_file: legal_docs\01_vbpl\test_backslash_doc\sources\test.docx
    source_assets:
      docx:
        vault_path: CCBA_Legal_Vault\01_vbpl\test_backslash_doc\test.docx
"""
    registry_path.write_text(registry_content, encoding="utf-8")
    validator = LegalSpokeValidator(tmp_path)
    errors, warnings = validator.validate_registry()
    assert errors >= 5
    format_errors = [e for e in validator.errors if "Registry Format Error" in e]
    assert any("bundle_path" in e for e in format_errors)
    assert any("pdf_path" in e for e in format_errors)
    assert any("raw_scan_pdf" in e for e in format_errors)
    assert any("source_file" in e for e in format_errors)
    assert any("vault_path" in e for e in format_errors)


def test_gate_1_warns_on_missing_files_on_disk(tmp_path: Path) -> None:
    """Gate 1 must issue Registry Warning when declared files do not exist on disk."""
    registry_path = tmp_path / "legal_registry.yaml"
    registry_content = """version: 0.2.0
spoke_name: ccba-legal-knowledge
registry_summary:
  total_documents: 1
laws:
  - id: test_missing_files
    title: Test Missing Files
    bundle_path: legal_docs/01_vbpl/test_missing_files
    pdf_path: legal_docs/01_vbpl/test_missing_files/sources/test.pdf
    raw_scan_pdf: legal_docs/01_vbpl/test_missing_files/sources/test_raw_scan.pdf
    source_file: legal_docs/01_vbpl/test_missing_files/sources/test.docx
    pdf_status: verified
"""
    registry_path.write_text(registry_content, encoding="utf-8")
    validator = LegalSpokeValidator(tmp_path)
    errors, warnings = validator.validate_registry()
    assert errors == 0
    assert warnings >= 3
    warn_texts = [w for w in validator.warnings if "Registry Warning [test_missing_files]" in w]
    assert any("pdf_path" in w for w in warn_texts)
    assert any("raw_scan_pdf" in w for w in warn_texts)
    assert any("source_file" in w for w in warn_texts)


def test_gate_1_suppresses_missing_pdf_warning_when_pending_download(tmp_path: Path) -> None:
    """Gate 1 must suppress missing pdf warning when pdf_status is pending_download."""
    registry_path = tmp_path / "legal_registry.yaml"
    registry_content = """version: 0.2.0
spoke_name: ccba-legal-knowledge
registry_summary:
  total_documents: 1
laws:
  - id: test_pending_doc
    title: Test Pending Doc
    bundle_path: legal_docs/04_appendices/test_pending_doc
    pdf_path: legal_docs/04_appendices/test_pending_doc/test.pdf
    pdf_status: pending_download
"""
    registry_path.write_text(registry_content, encoding="utf-8")
    bundle_dir = tmp_path / "legal_docs" / "04_appendices" / "test_pending_doc"
    bundle_dir.mkdir(parents=True)
    validator = LegalSpokeValidator(tmp_path)
    errors, warnings = validator.validate_registry()
    assert errors == 0
    assert not any("pdf_path" in w for w in validator.warnings)


def test_gate_2_detects_windows_backslashes_in_bundle_metadata(tmp_path: Path) -> None:
    """Gate 2 must flag OKF Metadata Format Error if bundle metadata.yaml has backslashes."""
    bundle_dir = tmp_path / "legal_docs" / "01_vbpl" / "test_bundle"
    bundle_dir.mkdir(parents=True)
    (bundle_dir / "index.md").write_text("# Test", encoding="utf-8")
    (bundle_dir / "sources").mkdir()
    metadata_content = r"pdf_path: legal_docs\01_vbpl\test_bundle\sources\test.pdf"
    (bundle_dir / "metadata.yaml").write_text(metadata_content, encoding="utf-8")

    validator = LegalSpokeValidator(tmp_path)
    errors, warnings = validator.validate_okf_bundles()
    assert errors >= 1
    assert any("OKF Metadata Format Error" in e and "pdf_path" in e for e in validator.errors)


