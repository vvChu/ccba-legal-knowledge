---
request_id: "req-spoke-legal-hygiene-plan-001"
from_agent: "antigravity"
to_agent: "grok"
request_type: "review"
profile: "audit_plan"
subject: "Thẩm định Kế hoạch Thực thi Mục 1, 2 và 3: Chuẩn hóa Cấu hình Workspace Context, Khắc phục Drift Con số Cố định (Dynamic Scale Invariant) trong test_spoke_cli.py và Khử SyntaxWarning trong verify_formula_visual_matrix.py"
timestamp: "2026-11-05T13:18:00+07:00"
source_documents:
  - ".md/workspace_context.yaml"
  - "tests/integration/test_spoke_cli.py"
  - "scripts/verify_formula_visual_matrix.py"
  - "features/INDEX.md"
output_path: ".md/peer_exchange/grok_review_plan_spoke_hygiene.md"
context: "Thẩm định đối kháng kế hoạch hoàn thiện 3 hạng mục vệ sinh và đồng bộ kiểm thử cho Spoke ccba-legal-knowledge sau khi kiến tạo 3 trụ cột Verification Skills (ccba-verify-legal-knowledge, ccba-verify-legal-intel, ccba-verify-legal-ingest)."
---

# 🎯 Yêu Cầu Thẩm Định Đối Kháng Kế Hoạch Thực Thi (Implementation Plan) — Mục 1, 2 và 3 Tại Spoke `ccba-legal-knowledge`

> ⚠️ **Chỉ Dẫn Cho Grok**: Toàn bộ ngữ cảnh thực tế (`get_spoke_stats`, `get_canonical_manifest`, mã nguồn hiện tại của 3 tệp mục tiêu) đã được trích xuất và đính kèm đầy đủ trong tài liệu này. Grok **KHÔNG CẦN** quét rộng toàn bộ 87 gói văn bản pháp lý. Hãy tập trung thẩm định đối kháng 3 hạng mục thay đổi bên dưới và xuất báo cáo phản biện kèm khối `PeerVerdictBlock` (YAML frontmatter) ở đầu tệp `.md/peer_exchange/grok_review_plan_spoke_hygiene.md`.

---

## I. BỐI CẢNH HIỆN TẠI (GROUND TRUTH CONTEXT)

Sau khi đồng bộ Spoke với Hub (`/ccba-update-spoke`) và hoàn tất kiến tạo 3 trụ cột kỹ năng kiểm định tự động:
1. `ccba-verify-legal-knowledge` (Pillar 1 — 15-Gate Bundle & Multimodal Parity)
2. `ccba-verify-legal-intel` (Pillar 2 — Hybrid RAG, VBHN Engine, ID Parser, CWE-22 Guard)
3. `ccba-verify-legal-ingest` (Pillar 3 — Acquisition, Sanitizer, Visual Parity, Legal Opinion)

Quá trình rà soát toàn diện Spoke `ccba-legal-knowledge` phát hiện 3 điểm tồn đọng cần xử lý dứt điểm:
- **Điểm 1 (`.md/workspace_context.yaml`):** Danh sách `agent_skills` mới chỉ có `ccba-verify-legal-knowledge`, chưa đăng ký 2 verification skills mới (`ccba-verify-legal-intel`, `ccba-verify-legal-ingest`). Đồng thời `verification.test_path` mới chỉ khai báo `tests/unit`, chưa bao gồm `tests/integration`.
- **Điểm 2 (`tests/integration/test_spoke_cli.py`):** Tệp kiểm thử tích hợp được viết từ thời điểm Spoke có 60 văn bản, sử dụng các phép so sánh bằng cứng (`assert stats["doc_count"] == 60`, `assert len(normative_sources) == 60`, `assert stats["total_figures"] == 370`, `assert stats["total_templates"] == 128`). Hiện tại Spoke đã phát triển lên **87 bundles vật lý** và **106 văn bản quy phạm** đăng ký trong `legal_registry.yaml` (`491` figures, `174` templates). Ngoài ra `test_spoke_validator_pass()` kiểm tra `assert len(validator.warnings) == 0`, bị vướng 2 dòng thông báo telemetry hợp lệ `[VBHN Telemetry]` từ các văn bản hợp nhất có khai báo `verification_scope.consolidation_note`.
- **Điểm 3 (`scripts/verify_formula_visual_matrix.py`):** Dòng 552–553 chứa 2 biểu thức chính quy JavaScript nhúng trong chuỗi Python `f"""` không có tiền tố raw (`_C(\d+(?:_\d+)+)_` và `_ANNEX_([A-Z](?:_\d+)+)_`), dẫn đến Python 3.12 phát cảnh báo `SyntaxWarning: invalid escape sequence '\d'` mỗi khi AST parser của `check_spoke_cleanliness.py` hoặc `check_hub_import_depth.py` biên dịch tệp này.

---

## II. NỘI DUNG CHI TIẾT KẾ HOẠCH THỰC THI (`implementation_plan.md`)

### 1. Cấu Hình Workspace Context (`.md/workspace_context.yaml`)

#### [MODIFY] `.md/workspace_context.yaml`
- Bổ sung `ccba-verify-legal-intel` và `ccba-verify-legal-ingest` vào danh sách `agent_skills`.
- Thêm `tests/integration` vào `verification.test_path` để cờ `--verify` hậu đồng bộ kiểm tra trọn vẹn cả Unit Tests (126 bài) và Integration Tests (8 files).

```diff
   - form-template-cleaner
   - table-reconstructor
   - ccba-verify-legal-knowledge
+  - ccba-verify-legal-intel
+  - ccba-verify-legal-ingest
 agents:
...
 verification:
   test_path:
   - tests/unit
+  - tests/integration
```

---

### 2. Kiểm Thử Tích Hợp CLI & NotebookLM Manifest (`tests/integration/test_spoke_cli.py`)

#### [MODIFY] `tests/integration/test_spoke_cli.py`
- Áp dụng **Dynamic Scale Invariant**: Sử dụng ngưỡng sàn tối thiểu (`>=`) khớp với quy mô hiện hành của Kho Tri thức (87 bundles vật lý / 106 văn bản quy phạm đăng ký) và kiểm tra tính toàn vẹn tổng thành phần (`len(state_normative_sources) + len(appendix_sources) == len(normative_sources)`).
- Trong `test_spoke_validator_pass()`, bỏ qua các dòng thông báo telemetry dự kiến có tiền tố `[VBHN Telemetry]` (đã được khai báo hợp lệ qua `verification_scope.consolidation_note`).

```diff
 def test_spoke_stats_computation():
     root_dir = Path(__file__).resolve().parent.parent.parent
     stats = get_spoke_stats(root_dir)
 
-    assert stats["doc_count"] == 60
-    assert stats["categories"].get("Luật", 0) >= 2
-    assert stats["categories"].get("Nghị định", 0) >= 7
-    assert stats["categories"].get("Thông tư", 0) >= 12
-    assert stats["categories"].get("Tiêu chuẩn quốc gia", 0) == 18
-    assert stats["total_size_mb"] > 3.0
-    assert stats["total_clauses"] > 3500
-    assert stats["total_qa"] > 700
-    assert stats["total_figures"] == 370
-    assert stats["total_templates"] == 128
+    assert stats["doc_count"] >= 87
+    assert stats["categories"].get("Luật", 0) >= 7
+    assert stats["categories"].get("Nghị định", 0) >= 11
+    assert stats["categories"].get("Thông tư", 0) >= 14
+    assert stats["categories"].get("Tiêu chuẩn quốc gia", 0) >= 31
+    assert stats["total_size_mb"] > 15.0
+    assert stats["total_clauses"] > 20000
+    assert stats["total_qa"] > 20000
+    assert stats["total_figures"] >= 491
+    assert stats["total_templates"] >= 174
 
 
 def test_spoke_validator_pass():
     root_dir = Path(__file__).resolve().parent.parent.parent
     validator = LegalSpokeValidator(root_dir)
     success = validator.run_all_checks()
 
     assert success is True
     assert len(validator.errors) == 0
-    assert len(validator.warnings) == 0
+    unexpected_warnings = [
+        w for w in validator.warnings if not w.startswith("[VBHN Telemetry]")
+    ]
+    assert len(unexpected_warnings) == 0
 
 
 def test_notebooklm_canonical_manifest_includes_standards():
...
-    # Test normative-only manifest (ADR 0012 whitelist 60 normative bodies)
+    # Test normative-only manifest (ADR 0012 whitelist normative bodies)
     normative_sources = get_canonical_manifest(root_dir, ultra_full=False)
-    assert len(normative_sources) == 60
+    assert len(normative_sources) >= 106
 
-    # Phân định rõ 57 thân quy phạm Nhà nước (01_vbpl, 02_qcvn, 03_tcvn) và 3 phụ lục đối chiếu (04_appendices)
+    # Phân định rõ thân quy phạm Nhà nước (01_vbpl, 02_qcvn, 03_tcvn) và phụ lục đối chiếu (04_appendices)
     state_normative_sources = [
         s for s in normative_sources
         if s.get("category") in {"01_vbpl", "02_qcvn", "03_tcvn"}
     ]
     appendix_sources = [
         s for s in normative_sources
         if s.get("category") == "04_appendices"
     ]
-    assert len(state_normative_sources) == 57
-    assert len(appendix_sources) == 3
+    assert len(state_normative_sources) >= 103
+    assert len(appendix_sources) >= 3
+    assert len(state_normative_sources) + len(appendix_sources) == len(normative_sources)
 
     normative_tcvn = [
         s for s in normative_sources
         if (
             s.get("category") == "03_tcvn"
             or "03_tcvn" in str(s.get("rel_path", ""))
         )
     ]
-    assert len(normative_tcvn) == 18
+    assert len(normative_tcvn) >= 33
```

---

### 3. Khử `SyntaxWarning` trong `scripts/verify_formula_visual_matrix.py`

#### [MODIFY] `scripts/verify_formula_visual_matrix.py`
- Thoát ký tự `\\d` trong 2 biểu thức regex JavaScript nằm trong chuỗi `f"""` để loại bỏ cảnh báo `SyntaxWarning: invalid escape sequence '\d'` của Python 3.12+.

```diff
                     let locLabel = "Biểu thức không số hiệu";
                     let fid = row.formula_id || "";
-                    let mClause = fid.match(/_C(\d+(?:_\d+)+)_/);
-                    let mAnnex = fid.match(/_ANNEX_([A-Z](?:_\d+)+)_/);
+                    let mClause = fid.match(/_C(\\d+(?:_\\d+)+)_/);
+                    let mAnnex = fid.match(/_ANNEX_([A-Z](?:_\\d+)+)_/);
                     if (mClause) {{
```

---

## III. CÂU HỎI THẨM VẤN ĐỐI KHÁNG DÀNH CHO GROK

1. **Về Mục 1 (`workspace_context.yaml` & `sync_spoke.py`):** Khi thêm `ccba-verify-legal-intel` và `ccba-verify-legal-ingest` (vốn là các Spoke-specific verification skills không nằm trong Hub `catalog.yaml`) vào `agent_skills` trong `.md/workspace_context.yaml`, liệu lần chạy `sync_spoke.py --spoke . --apply` tiếp theo có gặp lỗi hay cảnh báo "skill not found in Hub" không? Và việc đưa `tests/integration` vào `verification.test_path` có ảnh hưởng gì đến thời gian thực thi post-sync `--verify` không (hiện tại `pytest tests/unit tests/integration -q` chạy mất bao lâu khi gọi `LegalSpokeValidator.run_all_checks()`)?
2. **Về Mục 2 (`test_spoke_cli.py` — Dynamic Scale Invariant vs Exact Registry Consistency):** Việc dùng ngưỡng sàn `>= 87` / `>= 106` giúp tránh gãy test mỗi khi nạp thêm văn bản mới, nhưng có nên kết hợp kiểm tra tính nhất quán động (ví dụ: đối chiếu `len(normative_sources)` hoặc `stats` với chính dữ liệu đọc động từ `legal_registry.yaml` / cấu trúc thư mục) để vừa đảm bảo Dynamic Scale Invariant vừa không bị "lọt" lỗi nếu một bundle vô tình bị rớt khi nạp tiếp sau khi đã vượt ngưỡng 87?
3. **Về Mục 3 (`verify_formula_visual_matrix.py`):** Còn vị trí nào khác trong `scripts/verify_formula_visual_matrix.py` hoặc toàn bộ `scripts/*.py` có chuỗi escape không hợp lệ khi biên dịch với `python -W error::SyntaxWarning -m py_compile scripts/*.py` không?

Vui lòng xuất phán quyết chính thức với khối `PeerVerdictBlock` (YAML frontmatter) ở đầu phản hồi:

```yaml
---
request_id: "req-spoke-legal-hygiene-plan-001"
verdict: APPROVE_PLAN | APPROVE_WITH_CONDITIONS | REVISE_PLAN | REJECT_PLAN
risk_score: 2
conditions:
  - id: COND-01
    description: "..."
    blocking: true
summary: "..."
---
```
