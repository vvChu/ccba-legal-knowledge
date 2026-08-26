"""Unit tests for the Deep Module CLI Facade (spoke_cli.py)."""

import sys
from pathlib import Path

from scripts.spoke_cli import get_spoke_stats
from scripts.validate_legal_spoke import LegalSpokeValidator

def test_spoke_stats_computation():
    root_dir = Path(__file__).resolve().parent.parent.parent
    stats = get_spoke_stats(root_dir)

    assert stats["doc_count"] >= 21
    assert stats["categories"].get("Luật", 0) >= 2
    assert stats["categories"].get("Nghị định", 0) >= 7
    assert stats["categories"].get("Thông tư", 0) >= 12
    assert stats["total_size_mb"] > 3.0
    assert stats["total_clauses"] > 3500
    assert stats["total_qa"] > 700

def test_spoke_validator_pass():
    root_dir = Path(__file__).resolve().parent.parent.parent
    validator = LegalSpokeValidator(root_dir)
    success = validator.run_all_checks()

    assert success is True
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 0
