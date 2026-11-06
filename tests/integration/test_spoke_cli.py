"""Integration tests for the Deep Module CLI Facade (spoke_cli.py) and NotebookLM Manifest."""

from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from scripts.spoke_cli import (
    _extract_docx_header_hints,
    _find_existing_registry_entry,
    _handle_ingest_pdf_and_attachments,
    _merge_existing_registry_entry,
    _recompute_registry_summary,
    generate_provenance_report_md,
    get_spoke_stats,
)
from scripts.validate_legal_spoke import LegalSpokeValidator


def _load_registry_entries(
    root_dir: Path, include_decrees: bool = False
) -> list[dict[str, Any]]:
    """Load registry document entries matching target key union."""
    registry_file = root_dir / "legal_registry.yaml"
    reg_data = yaml.safe_load(registry_file.read_text(encoding="utf-8")) or {}
    entries: list[dict[str, Any]] = []
    keys = (
        ["laws", "decrees", "standards"] if include_decrees else ["laws", "standards"]
    )
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

    # 2. Đối soát động doc_count và categories khớp chính xác hợp khóa của get_spoke_stats (bao gồm cả decrees)
    stats_entries = _load_registry_entries(root_dir, include_decrees=True)
    expected_categories = Counter(doc.get("type", "Khác") for doc in stats_entries)
    assert stats["doc_count"] == len(stats_entries)
    assert stats["doc_count"] >= 106
    assert stats["categories"] == dict(expected_categories)

    reg_data = (
        yaml.safe_load((root_dir / "legal_registry.yaml").read_text(encoding="utf-8"))
        or {}
    )
    reg_summary = reg_data.get("registry_summary", {})
    assert reg_summary.get("total_documents") == len(stats_entries)
    reg_cats = reg_summary.get("categories", {})
    assert sum(reg_cats.values()) == len(stats_entries)
    assert reg_cats.get("01_vbpl", 0) >= 53
    assert reg_cats.get("02_qcvn", 0) >= 17
    assert reg_cats.get("03_tcvn", 0) >= 33
    assert reg_cats.get("04_appendices", 0) >= 3
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
        if (s.get("category") == "03_tcvn" or "03_tcvn" in str(s.get("rel_path", "")))
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
    assert len(state_normative_sources) + len(appendix_sources) == len(
        normative_sources
    )

    expected_tcvn_files = {
        p for p in expected_normative_files if "03_tcvn" in str(p.relative_to(root_dir))
    }
    normative_tcvn = [
        s
        for s in normative_sources
        if (s.get("category") == "03_tcvn" or "03_tcvn" in str(s.get("rel_path", "")))
    ]
    assert len(normative_tcvn) == len(expected_tcvn_files)
    assert len(normative_tcvn) >= 33


def test_registry_upsert_in_decrees_and_expired_status_preservation() -> None:
    """Verify C1 & C3: lookup across laws/decrees/standards, preserve expired status, and count 4 categories by bundle_path."""
    reg_data: dict[str, Any] = {
        "laws": [
            {
                "id": "nghi_dinh_10_2021_nd_cp",
                "document_number": "10/2021/NĐ-CP",
                "bundle_path": "legal_docs/01_vbpl/nghi_dinh_10_2021_nd_cp/",
                "status": "expired",
                "expiration_date": "2026-07-01",
                "relations": {"replaced_by": "206/2025/NĐ-CP"},
                "issued_date": "2021-02-09",
                "effective_date": "2021-02-09",
                "pdf_origin": "docx_vector_rendered",
                "raw_scan_pdf": "legal_docs/01_vbpl/nghi_dinh_10_2021_nd_cp/sources/nghi_dinh_10_2021_nd_cp_raw_scan.pdf",
            },
            {
                "id": "phu_luc_01",
                "bundle_path": "legal_docs/04_appendices/phu_luc_01/",
                "status": "active",
            },
        ],
        "decrees": [
            {
                "id": "nghi_dinh_214_2025_nd_cp",
                "document_number": "214/2025/NĐ-CP",
                "bundle_path": "legal_docs/01_vbpl/nghi_dinh_214_2025_nd_cp/",
                "status": "active",
            }
        ],
        "standards": [
            {
                "id": "qcvn_06_2022_bxd",
                "bundle_path": "legal_docs/02_qcvn/qcvn_06_2022_bxd/",
                "status": "active",
            },
            {
                "id": "tcvn_5574_2018",
                "bundle_path": "legal_docs/03_tcvn/tcvn_5574_2018/",
                "status": "active",
            },
        ],
    }

    # 1. Lookup finds entry in decrees (does not duplicate into laws)
    sec, idx = _find_existing_registry_entry(reg_data, "nghi_dinh_214_2025_nd_cp", {})
    assert sec == "decrees"
    assert idx == 0

    # 2. Re-ingest on expired law with default fallback raw_meta preserves status, expiration_date, pdf_origin, raw_scan_pdf
    sec_exp, idx_exp = _find_existing_registry_entry(
        reg_data, "nghi_dinh_10_2021_nd_cp", {}
    )
    assert sec_exp == "laws" and idx_exp == 0
    existing = reg_data["laws"][idx_exp]
    new_entry = {
        "id": "nghi_dinh_10_2021_nd_cp",
        "title": "Document nghi_dinh_10_2021_nd_cp",
        "status": "active",
        "relations": {},
        "issued_date": "2026-11-05",
        "effective_date": "2026-11-05",
        "bundle_path": "legal_docs\\01_vbpl\\nghi_dinh_10_2021_nd_cp\\",
        "source_assets": {},
    }
    merged = _merge_existing_registry_entry(
        existing,
        new_entry,
        raw_meta={"status": "active"},
        doc_title="Document nghi_dinh_10_2021_nd_cp",
    )
    assert merged["status"] == "expired"
    assert merged["expiration_date"] == "2026-07-01"
    assert merged["relations"] == {"replaced_by": "206/2025/NĐ-CP"}
    assert merged["issued_date"] == "2021-02-09"
    assert merged["pdf_origin"] == "docx_vector_rendered"
    assert "\\" not in merged["bundle_path"]

    # 2b. Re-ingest on superseded document (e.g., thong_tu_06_2021_tt_bxd) with raw_meta status='active' must preserve 'superseded'
    superseded_existing = {
        "id": "thong_tu_06_2021_tt_bxd",
        "document_number": "06/2021/TT-BXD",
        "title": "Thông tư 06/2021/TT-BXD quy định phân cấp công trình",
        "status": "superseded",
        "bundle_path": "legal_docs/01_vbpl/thong_tu_06_2021_tt_bxd/",
    }
    superseded_merged = _merge_existing_registry_entry(
        superseded_existing,
        {"id": "thong_tu_06_2021_tt_bxd", "status": "active"},
        raw_meta={"status": "active"},
        doc_title="Document thong_tu_06_2021_tt_bxd",
    )
    assert superseded_merged["status"] == "superseded"

    # 3. Summary counts total_documents = 5 and categories by bundle_path
    _recompute_registry_summary(reg_data)
    assert reg_data["registry_summary"]["total_documents"] == 5
    assert reg_data["registry_summary"]["categories"] == {
        "01_vbpl": 2,
        "02_qcvn": 1,
        "03_tcvn": 1,
        "04_appendices": 1,
    }


def test_dual_pdf_tier3_rendering_and_fallback_on_failure(
    tmp_path: Path, monkeypatch: Any
) -> None:
    """Verify C5 & C6: Dual-PDF Tier 3 stamps vector PDF on success, falls back cleanly on error, and copies attachments."""
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir(parents=True)
    input_docx = sources_dir / "doc_t3.docx"
    input_docx.write_bytes(b"PK\x03\x04dummy-docx")
    scan_pdf = tmp_path / "incoming_scan.pdf"
    scan_pdf.write_bytes(b"%PDF-1.4-scan-bytes")
    att_file = tmp_path / "phu_luc_01.xlsx"
    att_file.write_bytes(b"PK\x03\x04dummy-xlsx")

    # Case 1: convert_to_pdf succeeds (writes non-empty vector PDF)
    def _mock_convert_ok(docx_p: Path, pdf_p: Path) -> Path:
        pdf_p.write_bytes(b"%PDF-1.4-vector-rendered-bytes")
        return pdf_p

    target_pdf, raw_scan_pdf, is_vec = _handle_ingest_pdf_and_attachments(
        sources_dir=sources_dir,
        slug="doc_t3",
        input_docx=input_docx,
        pdf_arg=scan_pdf,
        raw_meta={"pdf_tier": 3, "attachments": [str(att_file)]},
        convert_fn=_mock_convert_ok,
    )
    assert is_vec is True
    assert (
        target_pdf is not None
        and target_pdf.read_bytes() == b"%PDF-1.4-vector-rendered-bytes"
    )
    assert raw_scan_pdf is not None and raw_scan_pdf.exists()
    assert raw_scan_pdf.read_bytes() == b"%PDF-1.4-scan-bytes"
    assert (sources_dir / "attachments" / "phu_luc_01.xlsx").is_file()

    # Case 2: convert_to_pdf fails (LibreOffice error) -> must unlink _raw_scan.pdf, restore scan to <slug>.pdf, is_vec=False
    sources_dir_fail = tmp_path / "sources_fail"
    sources_dir_fail.mkdir(parents=True)
    input_docx_fail = sources_dir_fail / "doc_fail.docx"
    input_docx_fail.write_bytes(b"PK\x03\x04dummy-docx")

    def _mock_convert_fail(docx_p: Path, pdf_p: Path) -> Path:
        raise RuntimeError("LibreOffice headless conversion failed")

    target_pdf_f, raw_scan_f, is_vec_f = _handle_ingest_pdf_and_attachments(
        sources_dir=sources_dir_fail,
        slug="doc_fail",
        input_docx=input_docx_fail,
        pdf_arg=scan_pdf,
        raw_meta={"pdf_tier": 3},
        convert_fn=_mock_convert_fail,
    )
    assert is_vec_f is False
    assert raw_scan_f is None
    assert not (sources_dir_fail / "doc_fail_raw_scan.pdf").exists()
    assert (
        target_pdf_f is not None and target_pdf_f.read_bytes() == b"%PDF-1.4-scan-bytes"
    )

    # Case 3: _extract_docx_header_hints extracts document_number, issued_date, issued_by, and title
    from docx import Document

    sample_docx = tmp_path / "sample_header.docx"
    doc = Document()
    doc.add_paragraph("BỘ XÂY DỰNG")
    doc.add_paragraph("Số: 1812/QĐ-BXD")
    doc.add_paragraph("Hà Nội, ngày 19 tháng 8 năm 2026")
    doc.add_paragraph("QUYẾT ĐỊNH")
    doc.add_paragraph("Về việc công bố định mức dự toán xây dựng công trình")
    doc.save(str(sample_docx))

    hints = _extract_docx_header_hints(sample_docx)
    assert hints["document_number"] == "1812/QĐ-BXD"
    assert hints["issued_date"] == "2026-08-19"
    assert hints["issued_by"] == "BỘ XÂY DỰNG"
    assert "Về việc công bố định mức" in hints["title"]


def test_audit_provenance_dynamic_header_and_nightly_summary_parsing() -> None:
    """Verify T-04 (C2, C7, C8): dynamic provenance header count and nightly summary regex parsing."""
    import importlib.util

    sample_records = [
        {
            "doc_id": "doc_1",
            "doc_number": "01/2026/NĐ-CP",
            "type": "NĐ",
            "group": "GROUP_A",
            "group_label": "🟢 Nhóm A",
            "prov_status": "VERIFIED",
            "status_label": "✅ VERIFIED",
            "math_blocks": 0,
            "csv_count": 0,
            "json_count": 0,
            "cards_count": 0,
            "action": "OK",
        },
        {
            "doc_id": "doc_2",
            "doc_number": "02/2026/NĐ-CP",
            "type": "NĐ",
            "group": "GROUP_A",
            "group_label": "🟢 Nhóm A",
            "prov_status": "MISSING_TELEMETRY",
            "status_label": "⏳ CHƯA CẤP DẤU",
            "math_blocks": 0,
            "csv_count": 0,
            "json_count": 0,
            "cards_count": 0,
            "action": "OK",
        },
    ]
    md_text = generate_provenance_report_md(sample_records)
    assert "## 2. Danh Sách Chi Tiết Hàng Đợi 2 Văn Bản" in md_text
    assert "38 Văn Bản" not in md_text

    root_dir = Path(__file__).resolve().parent.parent.parent
    telemetry_path = root_dir / ".md" / "tools" / "run_nightly_telemetry.py"
    spec = importlib.util.spec_from_file_location(
        "run_nightly_telemetry", telemetry_path
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert hasattr(mod, "parse_master_ci_summary")
    errs_0, warns_0, status_0 = mod.parse_master_ci_summary(
        0, "Gate 15: PASS\nSUMMARY REPORT: Errors: 0 | Warnings: 4\n"
    )
    assert (errs_0, warns_0) == (0, 4)
    assert status_0 == "✅ PASSED (0 Errors, 4 Warnings)"

    errs_1, warns_1, status_1 = mod.parse_master_ci_summary(
        1, "Gate 2: FAIL\nSUMMARY REPORT: Errors: 2 | Warnings: 5\n"
    )
    assert (errs_1, warns_1) == (2, 5)
    assert status_1 == "❌ FAILED (Exit 1: 2 Errors, 5 Warnings)"

    md_reg = root_dir / ".md" / "data" / "legal_registry.yaml"
    if md_reg.exists():
        root_reg_data = yaml.safe_load(
            (root_dir / "legal_registry.yaml").read_text(encoding="utf-8")
        )
        md_reg_data = yaml.safe_load(md_reg.read_text(encoding="utf-8"))
        assert md_reg_data.get("registry_summary") == root_reg_data.get(
            "registry_summary"
        )
