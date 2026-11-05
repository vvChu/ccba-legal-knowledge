"""Integration tests for the Deep Module CLI Facade (spoke_cli.py) and NotebookLM Manifest."""

from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from scripts.spoke_cli import get_spoke_stats
from scripts.validate_legal_spoke import LegalSpokeValidator


def _load_registry_entries(
    root_dir: Path, include_decrees: bool = False
) -> list[dict[str, Any]]:
    """Load registry document entries matching target key union."""
    registry_file = root_dir / "legal_registry.yaml"
    reg_data = yaml.safe_load(registry_file.read_text(encoding="utf-8")) or {}
    entries: list[dict[str, Any]] = []
    keys = ["laws", "decrees", "standards"] if include_decrees else ["laws", "standards"]
    for key in keys:
        val = reg_data.get(key, [])
        if isinstance(val, list):
            entries.extend(d for d in val if isinstance(d, dict))
    documents = reg_data.get("documents", {})
    if isinstance(documents, dict):
        entries.extend(d for d in documents.values() if isinstance(d, dict))
    elif isinstance(documents, list):
        entries.extend(d for d in documents if isinstance(d, dict))
    return entries


def test_spoke_stats_computation() -> None:
    root_dir = Path(__file__).resolve().parent.parent.parent
    legal_docs_dir = root_dir / "legal_docs"
    stats = get_spoke_stats(root_dir)

    # 1. Mọi bundle_path trong registry phải tồn tại thư mục và {slug}.md trên đĩa (COND-01)
    all_reg_entries = _load_registry_entries(root_dir, include_decrees=True)
    for item in all_reg_entries:
        bp = item.get("bundle_path", "")
        if not bp:
            continue
        bundle_dir = root_dir / bp.strip("/")
        assert bundle_dir.is_dir(), f"Missing bundle directory: {bundle_dir}"
        normative_md = bundle_dir / f"{bundle_dir.name}.md"
        assert normative_md.is_file(), f"Missing normative markdown: {normative_md}"

    # 2. Đối soát động doc_count và categories khớp chính xác hợp khóa của get_spoke_stats
    stats_entries = _load_registry_entries(root_dir, include_decrees=False)
    expected_categories = Counter(doc.get("type", "Khác") for doc in stats_entries)
    assert stats["doc_count"] == len(stats_entries)
    assert stats["doc_count"] >= 87
    assert stats["categories"] == dict(expected_categories)
    assert stats["categories"].get("Luật", 0) >= 7
    assert stats["categories"].get("Nghị định", 0) >= 11
    assert stats["categories"].get("Thông tư", 0) >= 14
    assert stats["categories"].get("Tiêu chuẩn quốc gia", 0) >= 31

    # 3. Đối soát động figures/cards và templates kèm ngưỡng sàn chống suy giảm
    expected_figures = len(list(legal_docs_dir.glob("**/figures/cards/*.md"))) + len(
        list(legal_docs_dir.glob("**/figures/cards/*.json"))
    )
    expected_templates = len(list(legal_docs_dir.glob("**/templates/**/*.md")))
    assert stats["total_figures"] == expected_figures
    assert stats["total_figures"] >= 491
    assert stats["total_templates"] == expected_templates
    assert stats["total_templates"] >= 174
    assert stats["total_size_mb"] > 15.0
    assert stats["total_clauses"] > 20000
    assert stats["total_qa"] > 20000


def test_spoke_validator_pass() -> None:
    root_dir = Path(__file__).resolve().parent.parent.parent
    validator = LegalSpokeValidator(root_dir)
    success = validator.run_all_checks()

    assert success is True
    assert len(validator.errors) == 0

    # COND-05: Chỉ cho phép warning [VBHN Telemetry] từ các bundle có verification_scope.type == vbhn_consolidation
    vbhn_slugs: set[str] = set()
    for meta_path in (root_dir / "legal_docs").glob("*/*/metadata.yaml"):
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        v_scope = meta.get("verification_scope") or {}
        if isinstance(v_scope, dict) and v_scope.get("type") == "vbhn_consolidation":
            vbhn_slugs.add(meta_path.parent.name)

    telemetry_warnings = [
        w for w in validator.warnings if w.startswith("[VBHN Telemetry]")
    ]
    unexpected_warnings = [
        w for w in validator.warnings if not w.startswith("[VBHN Telemetry]")
    ]
    assert len(unexpected_warnings) == 0
    for w in telemetry_warnings:
        assert any(slug in w for slug in vbhn_slugs), (
            f"Telemetry warning does not match any vbhn_consolidation bundle: {w}"
        )


def test_notebooklm_canonical_manifest_includes_standards() -> None:
    from scripts.sync_notebooklm_knowledge import get_canonical_manifest

    root_dir = Path(__file__).resolve().parent.parent.parent

    # Test full comprehensive Ultra Tier manifest
    sources = get_canonical_manifest(root_dir, ultra_full=True)
    tcvn_sources = [
        s
        for s in sources
        if (
            s.get("category") == "03_tcvn"
            or "03_tcvn" in str(s.get("rel_path", ""))
        )
    ]
    assert len(tcvn_sources) >= 500
    assert len(sources) > 1100

    # Test normative-only manifest (COND-01: đối soát động với registry + category markdowns)
    normative_sources = get_canonical_manifest(root_dir, ultra_full=False)

    expected_normative_files: set[Path] = set()
    for item in _load_registry_entries(root_dir, include_decrees=True):
        bp = item.get("bundle_path", "")
        if not bp:
            continue
        bundle_dir = root_dir / bp.strip("/")
        normative_md = bundle_dir / f"{bundle_dir.name}.md"
        if normative_md.is_file():
            expected_normative_files.add(normative_md)

    for cat_dir in sorted((root_dir / "legal_docs").iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("."):
            continue
        for mf in sorted(cat_dir.glob("*.md")):
            if mf.name not in ("index.md", "dead_ends.md", "log.md"):
                expected_normative_files.add(mf)

    assert len(normative_sources) == len(expected_normative_files)
    assert len(normative_sources) >= 106

    # Phân hoạch 4 category (01_vbpl, 02_qcvn, 03_tcvn) + (04_appendices) bằng toàn bộ manifest
    state_normative_sources = [
        s
        for s in normative_sources
        if s.get("category") in {"01_vbpl", "02_qcvn", "03_tcvn"}
    ]
    appendix_sources = [
        s for s in normative_sources if s.get("category") == "04_appendices"
    ]
    assert len(state_normative_sources) >= 103
    assert len(appendix_sources) >= 3
    assert len(state_normative_sources) + len(appendix_sources) == len(normative_sources)

    expected_tcvn_files = {
        p for p in expected_normative_files if "03_tcvn" in str(p.relative_to(root_dir))
    }
    normative_tcvn = [
        s
        for s in normative_sources
        if (
            s.get("category") == "03_tcvn"
            or "03_tcvn" in str(s.get("rel_path", ""))
        )
    ]
    assert len(normative_tcvn) == len(expected_tcvn_files)
    assert len(normative_tcvn) >= 33
