# Walkthrough: Phát Hành Tính Năng PR #10 & PR #11 (Legal Spoke Hardening & Cloud Sync)

> **Mục tiêu:** Phát hành trọn vẹn NĐ 339/2026/NĐ-CP, NĐ 10/2021/NĐ-CP, nâng cấp Sub-Gate 5.3 Transitive DAG Engine, chuẩn hóa multi-line spans cho 27 VBPL, tối ưu hóa CI Validator đạt 0 Errors / 0 Warnings, và hoàn tất đồng bộ Cloud RAG lên Google NotebookLM (`CCBA_Legal_Knowledge_Base_2026`).
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **PR #10:** [vvChu/ccba-legal-knowledge#10](https://github.com/vvChu/ccba-legal-knowledge/pull/10) (Squash Commit: `ab7205c`)
> - **PR #11:** [vvChu/ccba-legal-knowledge#11](https://github.com/vvChu/ccba-legal-knowledge/pull/11) (Squash Commit: `d6f7c77`)
> **CI Gate:** 100% Green (15/15 Master Gates PASSED, 0 Errors, 0 Warnings)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành

### PR #10: Ingestion NĐ 339, NĐ 10, Sub-Gate 5.3 DAG & 24 VBPL Multi-line Spans
- **Nghị định 339/2026/NĐ-CP**: Nạp toàn diện vào `legal_docs/01_vbpl/nghi_dinh_339_2026_nd_cp/` với 135 điều khoản AST multi-line (`line_start < line_end`), bộ câu hỏi chuẩn hóa QA benchmark, mỏ neo nguồn (.docx, .pdf) và thiết lập quan hệ `relations: { replaces: '16/2022/NĐ-CP' }`.
- **Nghị định 10/2021/NĐ-CP**: Đóng gói bundle lịch sử và đánh dấu trạng thái `expired`, thiết lập quan hệ `relations: { replaced_by: '206/2026/NĐ-CP' }`.
- **Sub-Gate 5.3 Transitive DAG BFS Engine**: Nâng cấp `scripts/validate_legal_spoke.py` với bộ giải đồ thị có hướng hai tầng (Two-Tier In-Memory Transitive DAG BFS Engine) và cơ chế token hóa khóa định danh chuẩn tắc (`canonical lookup tokens`), phát hiện tức thì các văn bản hết hiệu lực hoặc bị thay thế chéo.
- **Batch Span Migration 24 VBPL Bundles**: Chuyển dịch toàn bộ 24 bundles VBPL di sản từ single-line span sang multi-line AST spans chuẩn xác, tái tạo 100% QA benchmarks tương ứng.

### PR #11: Tinh Chỉnh CI Ergonomics, Triệt Tiêu Warnings & Idempotent RPC Sync
- **Khử 2 False-Positive Warnings**: Tinh chỉnh heuristic kiểm tra số lượng điều khoản AST tại `_validate_vbpl_ast_clauses`. Với các thông tư ban hành có `max_dieu < 10` (như TT 37/2026 và TT 38/2026 có 4 Điều mở đầu và toàn bộ quy phạm nằm ở Phụ lục/Templates), hệ thống miễn trừ cảnh báo `Expected >= 30 clauses`.
- **Hỗ trợ Local Developer Ergonomics**: Bổ sung cờ CLI `--skip-pdf-vault` và nhận diện biến môi trường `CCBA_SKIP_PDF_VAULT=1` cho Sub-Gate 5.2 (Dual-PDF Archive Invariant). Cho phép chạy nghiệm thu trên máy trạm chưa mount Google Drive Vault mà không phát sinh 28 lỗi PDF ảo.
- **Hoàn thiện Dependency Package**: Bổ sung `"Pillow"` vào dependencies của `ccba-legal-intel` trên Hub, giải quyết dứt điểm lỗi import khi chạy test suite.
- **Đồng bộ Idempotent Cloud RAG (NotebookLM)**:
  - Tự động phát hiện danh sách nguồn đã có trên Cloud để bỏ qua, chống ghi đè trùng lặp.
  - Chuyển sang giao thức direct RPC text ingestion (`sources.add_text`) thay cho HTTP resumable upload endpoint, loại trừ hoàn toàn lỗi `500 Internal Server Error`.
  - Kết nối phiên Google thật (`macvnboy@gmail.com`) và nạp hoàn tất **47 nguồn tri thức hoạt động (Active Sources)** vào `CCBA_Legal_Knowledge_Base_2026` (`6dca7e4e-c407-4d1f-882a-e0d9459d1120`).

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Lệnh Kiểm Tra | Kết Quả | Trạng Thái |
| :--- | :--- | :---: | :---: |
| **Master CI Gate (15 Cổng)** | `CI=1 uv run python scripts/validate_legal_spoke.py` | **0 Errors, 0 Warnings** | ✅ **PASSED** |
| **Local Offline Validator** | `uv run python scripts/validate_legal_spoke.py --skip-pdf-vault` | **0 Errors, 0 Warnings** | ✅ **PASSED** |
| **Spoke Cleanliness Budget** | `CI=1 uv run python scripts/check_spoke_cleanliness.py` | 15/15 valid scripts, 0 machine leaks | ✅ **PASSED** |
| **Visual Parity Linter** | `CI=1 uv run python scripts/lint_visual_parity.py` | 783 files scanned, 0 errors | ✅ **PASSED** |
| **Unit & Integration Suite** | `uv run pytest tests/integration/test_validate_legal_spoke.py tests/integration/test_modernize_annex_engine.py` | 12/12 tests PASS (100%) | ✅ **PASSED** |
| **Cloud RAG Inventory** | `CCBA_Legal_Knowledge_Base_2026` (`6dca7e4e-...`) | **47 Sources READY** | ✅ **VERIFIED** |
