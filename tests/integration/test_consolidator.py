"""Unit & Integration Tests for Legislative Consolidator Engine (OKF v2.0 & ADR 0017)."""

import json
from pathlib import Path
import pytest

from ccba_legal.consolidator import (
    DefectSeverity,
    DocMode,
    DualModeASTParser,
    LegislativeConsolidator,
    PatchAction,
    PatchItem,
    PatchManifest,
    load_manifest,
)


@pytest.fixture
def sample_qcvn_md() -> str:
    return """# QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ THIẾT KẾ MẪU

## MỤC LỤC
- [1  QUY ĐỊNH CHUNG](#muc-1)
- [2  QUY ĐỊNH KỸ THUẬT](#muc-2)

---

### <a id="muc-1" name="muc-1"></a>1  QUY ĐỊNH CHUNG

#### <a id="muc-1-1" name="muc-1-1"></a>1.1  Phạm vi điều chỉnh
Quy chuẩn này quy định các yêu cầu kỹ thuật đối với nhà và công trình.

#### <a id="muc-1-1-2" name="muc-1-1-2"></a>1.1.2  Đối tượng áp dụng
Áp dụng cho các tòa nhà hỗn hợp và chung cư.

#### <a id="muc-1-3" name="muc-1-3"></a>1.3  Tài liệu viện dẫn
TCVN 3890:2023, Phương tiện PCCC.

### <a id="muc-2" name="muc-2"></a>2  QUY ĐỊNH KỸ THUẬT

#### <a id="muc-2-1" name="muc-2-1"></a>2.1  Bậc chịu lửa
Công trình phải đảm bảo bậc chịu lửa tối thiểu bậc II.
"""


@pytest.fixture
def sample_luat_md() -> str:
    return """# LUẬT XÂY DỰNG MẪU

## CHƯƠNG I. QUY ĐỊNH CHUNG

### Điều 1. Phạm vi điều chỉnh
Luật này quy định quyền và nghĩa vụ của cơ quan, tổ chức, cá nhân.

### Điều 2. Đối tượng áp dụng
Áp dụng đối với cơ quan, tổ chức, cá nhân trong nước.
"""


def test_manifest_schema_validation(tmp_path: Path):
    """Test 1: Validate PatchManifest parsing and integrity checks."""
    manifest_yaml = """
target_doc_id: qcvn_test
amending_doc_id: sua_doi_test
doc_mode: qcvn
title: Test Quy Chuẩn
official_citation: TT 99/2026/TT-BXD
effective_date: "2026-12-31"
patches:
  - action: REPLACE
    target_anchor: muc-1-1-2
    citation: Sửa đổi bởi TT 99/2026
    defect_severity: CRITICAL_DEFECT
    new_content_inline: Nội dung sửa đổi mới
"""
    mfile = tmp_path / "test_manifest.yaml"
    mfile.write_text(manifest_yaml, encoding="utf-8")

    manifest = load_manifest(mfile)
    assert manifest.target_doc_id == "qcvn_test"
    assert manifest.doc_mode == DocMode.QCVN
    assert len(manifest.patches) == 1
    assert manifest.patches[0].action == PatchAction.REPLACE
    assert manifest.patches[0].defect_severity == DefectSeverity.CRITICAL_DEFECT


def test_dual_mode_parser_qcvn(sample_qcvn_md: str):
    """Test 2: DualModeASTParser in QCVN mode extracts dotted heading anchors."""
    parser = DualModeASTParser()
    nodes = parser.parse(sample_qcvn_md, mode=DocMode.QCVN)

    flat = parser.flatten_ast(nodes)
    assert "muc-1" in flat
    assert "muc-1-1" in flat
    assert "muc-1-1-2" in flat
    assert "muc-2-1" in flat

    node_112 = flat["muc-1-1-2"]
    assert node_112.clause_number == "1.1.2"
    assert "Đối tượng áp dụng" in node_112.title
    assert "tòa nhà hỗn hợp" in node_112.content


def test_dual_mode_parser_luat(sample_luat_md: str):
    """Test 3: DualModeASTParser in LUAT mode extracts articles (Điều X)."""
    parser = DualModeASTParser()
    nodes = parser.parse(sample_luat_md, mode=DocMode.LUAT)

    flat = parser.flatten_ast(nodes)
    assert "D1" in flat
    assert "D2" in flat

    d1 = flat["D1"]
    assert d1.clause_number == "1"
    assert "Phạm vi điều chỉnh" in d1.title


def test_insert_after_patch(sample_qcvn_md: str, tmp_path: Path):
    """Test 4: INSERT_AFTER action adds new node right after target."""
    manifest = PatchManifest(
        target_doc_id="qcvn_test",
        amending_doc_id="tt_31_2026",
        doc_mode=DocMode.QCVN,
        patches=[
            PatchItem(
                action=PatchAction.INSERT_AFTER,
                target_anchor="muc-1-1-2",
                new_anchor="muc-1-1-3",
                citation="Bổ sung bởi Sửa đổi 01:2026",
                defect_severity=DefectSeverity.CRITICAL_DEFECT,
                new_content_inline="Quy định chỗ để xe điện áp dụng cho chung cư mới và hiện hữu.",
            )
        ]
    )

    base_file = tmp_path / "base.md"
    base_file.write_text(sample_qcvn_md, encoding="utf-8")

    consolidator = LegislativeConsolidator(manifest)
    res = consolidator.consolidate(base_file, output_dir=tmp_path / "out")

    assert res.success
    assert res.added_clauses == 1

    out_md = res.consolidated_md_path.read_text(encoding="utf-8")
    assert "muc-1-1-3" in out_md
    assert "xe điện" in out_md

    # Check clauses.json has the new clause
    clauses = json.loads(res.clauses_json_path.read_text(encoding="utf-8"))
    c_ids = [c["id"] for c in clauses]
    assert "muc-1-1-3" in c_ids


def test_replace_patch(sample_qcvn_md: str, tmp_path: Path):
    """Test 5: REPLACE action overwrites content with Callout block."""
    manifest = PatchManifest(
        target_doc_id="qcvn_test",
        amending_doc_id="tt_31_2026",
        doc_mode=DocMode.QCVN,
        patches=[
            PatchItem(
                action=PatchAction.REPLACE,
                target_anchor="muc-2-1",
                citation="Sửa đổi bởi TT 31/2026",
                defect_severity=DefectSeverity.CRITICAL_DEFECT,
                new_content_inline="Công trình phải đảm bảo bậc chịu lửa tối thiểu bậc I.",
            )
        ]
    )

    base_file = tmp_path / "base.md"
    base_file.write_text(sample_qcvn_md, encoding="utf-8")

    consolidator = LegislativeConsolidator(manifest)
    res = consolidator.consolidate(base_file, output_dir=tmp_path / "out")

    assert res.success
    assert res.modified_clauses == 1

    out_md = res.consolidated_md_path.read_text(encoding="utf-8")
    assert "> [!NOTE]" in out_md
    assert "bậc chịu lửa tối thiểu bậc I" in out_md


def test_repeal_patch(sample_qcvn_md: str, tmp_path: Path):
    """Test 6: REPEAL action marks node as repealed with WARNING callout."""
    manifest = PatchManifest(
        target_doc_id="qcvn_test",
        amending_doc_id="tt_31_2026",
        doc_mode=DocMode.QCVN,
        patches=[
            PatchItem(
                action=PatchAction.REPEAL,
                target_anchor="muc-1-3",
                citation="Bãi bỏ bởi TT 31/2026",
            )
        ]
    )

    base_file = tmp_path / "base.md"
    base_file.write_text(sample_qcvn_md, encoding="utf-8")

    consolidator = LegislativeConsolidator(manifest)
    res = consolidator.consolidate(base_file, output_dir=tmp_path / "out")

    assert res.success
    assert res.repealed_clauses == 1

    out_md = res.consolidated_md_path.read_text(encoding="utf-8")
    assert "> [!WARNING]" in out_md
    assert "Đã bãi bỏ theo" in out_md


def test_substitute_phrase_patch(sample_qcvn_md: str, tmp_path: Path):
    """Test 7: SUBSTITUTE_PHRASE replaces exact keyword inside clause content."""
    manifest = PatchManifest(
        target_doc_id="qcvn_test",
        amending_doc_id="tt_31_2026",
        doc_mode=DocMode.QCVN,
        patches=[
            PatchItem(
                action=PatchAction.SUBSTITUTE_PHRASE,
                target_anchor="muc-1-1-2",
                old_phrase="chung cư",
                new_phrase="chung cư và nhà ở nhiều tầng",
                citation="Thay thế cụm từ",
            )
        ]
    )

    base_file = tmp_path / "base.md"
    base_file.write_text(sample_qcvn_md, encoding="utf-8")

    consolidator = LegislativeConsolidator(manifest)
    res = consolidator.consolidate(base_file, output_dir=tmp_path / "out")

    assert res.success
    out_md = res.consolidated_md_path.read_text(encoding="utf-8")
    assert "chung cư và nhà ở nhiều tầng" in out_md


def test_triple_output_generation(sample_qcvn_md: str, tmp_path: Path):
    """Test 8: Ensure all 3 OKF v2.0 artifacts are created and structurally sound."""
    manifest = PatchManifest(
        target_doc_id="qcvn_test",
        amending_doc_id="tt_31_2026",
        doc_mode=DocMode.QCVN,
        title="Quy Chuẩn Thử Nghiệm",
        official_citation="Thông tư 31/2026/TT-BXD",
        effective_date="2026-12-15",
        patches=[
            PatchItem(
                action=PatchAction.REPLACE,
                target_anchor="muc-2-1",
                citation="Sửa đổi bậc chịu lửa",
                defect_severity=DefectSeverity.CRITICAL_DEFECT,
                new_content_inline="Nội dung mới cho 2.1",
            )
        ]
    )

    base_file = tmp_path / "base.md"
    base_file.write_text(sample_qcvn_md, encoding="utf-8")

    consolidator = LegislativeConsolidator(manifest)
    res = consolidator.consolidate(base_file, output_dir=tmp_path / "out")

    # 1. Consolidated Markdown
    assert res.consolidated_md_path.exists()
    assert res.consolidated_md_path.stat().st_size > 0

    # 2. Rich AST JSON
    assert res.clauses_json_path.exists()
    clauses = json.loads(res.clauses_json_path.read_text(encoding="utf-8"))
    assert len(clauses) > 0
    assert "jurisdiction" in clauses[0]

    # 3. Diff Matrix Table
    assert res.diff_matrix_path.exists()
    diff_content = res.diff_matrix_path.read_text(encoding="utf-8")
    assert "BẢNG MA TRẬN ĐỐI CHIẾU SỬA ĐỔI" in diff_content
    assert "🔴 Critical Defect" in diff_content


def test_real_qcvn04_patch_manifest():
    """Test 9: Integration test validating real QCVN 04 PatchManifest file."""
    m_path = Path("legal_docs/02_qcvn/qcvn_04_2021_bxd/patch_manifest.yaml")
    assert m_path.exists()
    manifest = load_manifest(m_path)
    assert manifest.target_doc_id == "qcvn_04_2021_bxd"
    assert manifest.doc_mode == DocMode.QCVN
    assert len(manifest.patches) >= 6

    # Test running consolidation with real base
    base_path = Path("legal_docs/02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md")
    consolidator = LegislativeConsolidator(manifest)
    
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        res = consolidator.consolidate(base_path, output_dir=tmpdir)
        assert res.success
        assert res.total_clauses >= 100
        
        # Verify EV vehicle provisions exist
        md_text = res.consolidated_md_path.read_text(encoding="utf-8")
        assert "muc-1-1-3" in md_text
        assert "xe điện" in md_text
        assert "muc-1-4-32" in md_text
        assert "Khu vực sạc xe điện" in md_text


def test_manifest_generator_mock(tmp_path: Path):
    """Test 10: LLM-Assisted Manifest Generator produces valid PatchManifest."""
    from ccba_legal.consolidator import ManifestGenerator

    mock_llm_json = """{
      "target_doc_id": "qcvn_mock",
      "amending_doc_id": "tt_mock",
      "doc_mode": "qcvn",
      "title": "Mock Quy Chuẩn",
      "official_citation": "Thông tư Mock",
      "effective_date": "2026-12-15",
      "default_cong_bao_number": "999/2026",
      "default_jurisdiction": "CQXD",
      "patches": [
        {
          "action": "INSERT_AFTER",
          "target_anchor": "muc-1-1-2",
          "new_anchor": "muc-1-1-3",
          "citation": "Bổ sung bởi TT Mock",
          "defect_severity": "CRITICAL_DEFECT",
          "new_content_inline": "Nội dung quy chuẩn mới."
        }
      ]
    }"""

    base_f = tmp_path / "base.md"
    base_f.write_text("# Mock base", encoding="utf-8")
    amend_f = tmp_path / "amend.md"
    amend_f.write_text("# Mock amend", encoding="utf-8")
    out_yaml = tmp_path / "out_manifest.yaml"

    gen = ManifestGenerator()
    manifest = gen.generate_manifest_from_files(
        base_md_path=base_f,
        amending_md_path=amend_f,
        output_yaml_path=out_yaml,
        mock_response=mock_llm_json,
    )

    assert manifest.target_doc_id == "qcvn_mock"
    assert len(manifest.patches) == 1
    assert manifest.patches[0].action == PatchAction.INSERT_AFTER
    assert out_yaml.exists()

