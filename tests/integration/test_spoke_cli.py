"""Unit tests for the Deep Module CLI Facade (spoke_cli.py)."""

from pathlib import Path

from scripts.spoke_cli import get_spoke_stats
from scripts.validate_legal_spoke import LegalSpokeValidator


def test_spoke_stats_computation():
    root_dir = Path(__file__).resolve().parent.parent.parent
    stats = get_spoke_stats(root_dir)

    assert stats["doc_count"] == 60
    assert stats["categories"].get("Luật", 0) >= 2
    assert stats["categories"].get("Nghị định", 0) >= 7
    assert stats["categories"].get("Thông tư", 0) >= 12
    assert stats["categories"].get("Tiêu chuẩn quốc gia", 0) == 18
    assert stats["total_size_mb"] > 3.0
    assert stats["total_clauses"] > 3500
    assert stats["total_qa"] > 700
    assert stats["total_figures"] == 370
    assert stats["total_templates"] == 128


def test_spoke_validator_pass():
    root_dir = Path(__file__).resolve().parent.parent.parent
    validator = LegalSpokeValidator(root_dir)
    success = validator.run_all_checks()

    assert success is True
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 0


def test_notebooklm_canonical_manifest_includes_standards():
    from scripts.sync_notebooklm_knowledge import get_canonical_manifest

    root_dir = Path(__file__).resolve().parent.parent.parent

    # Test full comprehensive Ultra Tier manifest
    sources = get_canonical_manifest(root_dir, ultra_full=True)
    tcvn_sources = [
        s for s in sources
        if (
            s.get("category") == "03_tcvn"
            or "03_tcvn" in str(s.get("rel_path", ""))
        )
    ]
    assert len(tcvn_sources) >= 500
    assert len(sources) > 1100

    # Test normative-only manifest (ADR 0012 whitelist 60 normative bodies)
    normative_sources = get_canonical_manifest(root_dir, ultra_full=False)
    assert len(normative_sources) == 60

    # Phân định rõ 57 thân quy phạm Nhà nước (01_vbpl, 02_qcvn, 03_tcvn) và 3 phụ lục đối chiếu (04_appendices)
    state_normative_sources = [
        s for s in normative_sources
        if s.get("category") in {"01_vbpl", "02_qcvn", "03_tcvn"}
    ]
    appendix_sources = [
        s for s in normative_sources
        if s.get("category") == "04_appendices"
    ]
    assert len(state_normative_sources) == 57
    assert len(appendix_sources) == 3

    normative_tcvn = [
        s for s in normative_sources
        if (
            s.get("category") == "03_tcvn"
            or "03_tcvn" in str(s.get("rel_path", ""))
        )
    ]
    assert len(normative_tcvn) == 18
