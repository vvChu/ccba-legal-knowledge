# Walkthrough: Phát Hành Tính Năng PR #12 (Modular Dual-Dispatch Converter, Multipart Tables & QCVN 07 Parity)

> **Mục tiêu:** Tái cấu trúc pipeline chuyển đổi DOCX sang OKF v2.4 Universal Agent-Centric, phân rã `strategy.py` thành Dual-Dispatch Orchestrator tinh gọn (<200 dòng), trích xuất `preprocessor.py` và `exporter.py`, giải quyết triệt để lỗi ghi đè bảng đa phần theo ADR 0044 tại `qcvn_07_2023_bxd` (bóc tách đầy đủ 25 bảng phân phần), phân tách footnote bảng biểu theo ADR 0041, và bảo toàn 100% Zero-Regression trên toàn bộ 60 bundles.
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **PR #12:** [vvChu/ccba-legal-knowledge#12](https://github.com/vvChu/ccba-legal-knowledge/pull/12) (Squash Commit: `f5532f3`)
> **CI Gate:** 100% Green (Deterministic Parity & Schema Audit PASSED in 22s, 0 Errors, 0 Blocker Comments)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (PR #12)

### A. Tái cấu trúc Kiến trúc Hub Converter (`packages/ccba-legal-intel`)
- **`strategy.py`**: Rút gọn từ 622 dòng (>26KB) xuống **184 dòng** (<8KB), đóng vai trò **Dual-Dispatch Orchestrator** thuần túy điều phối giữa các handlers và functional helpers.
- **`preprocessor.py` [NEW]**: Bóc tách toàn bộ logic duyệt DOM blocks order-preserving, bộ phát hiện ranh giới mở đầu/quy phạm (`find_standard_header_start_index`, `find_normative_start_index`), và bộ chuyển đổi số La Mã sang mã phần (`parse_part_number`).
- **`exporter.py` [NEW]**: Xây dựng module Functional Helpers thuần túy (`export_standard_bundle`, `build_frontmatter_yaml`), bảo đảm nguyên tắc KISS (User Rule 5) và không phát sinh class thừa thãi.
- **`formula_handler.py`**: Dọn sạch 38 dòng dead code, tiếp nhận an toàn logic trích xuất công thức OLE `r:id` từ paragraph rỗng qua `handle_empty_paragraph_formula`.
- **`heading_handler.py`**: Bổ sung bộ nhận diện tiêu đề `PHẦN X` / La Mã (`PHẦN I`..`XX`) và tiêm `current_part` (`p01`..`p20`) vào context xử lý.

### B. Khử Trùng Lặp Bảng Đa Phần (ADR 0044) & Bóc Tách Footnote (ADR 0041)
- **`table_handler.py`**:
  - Hỗ trợ tiền tố phân phần cho mã bảng: sinh tên tệp chuẩn tắc `bang_pXX_YY.csv/json` khi tài liệu có chia phần.
  - Tiêm trường `part_id` vào `tables_catalog.json` theo đúng quy chuẩn ADR 0044.
  - Bóc tách dòng chú thích `CHÚ THÍCH` và `<sup>X)</sup>` ra khỏi lưới dữ liệu CSV `raw_grid`, lưu trữ có cấu trúc vào mảng `footnotes` của file JSON metadata.
  - **Sửa lỗi va chạm dữ liệu số (Numeric Collision)**: Bổ sung guardrail `not is_numeric` ngăn thuật toán gộp subheader nuốt chửng hàng số liệu có giá trị trùng nhau (`['50', '50']`).
  - **Khử lặp footnote trên ô merge ngang (`gridSpan`)**: Khắc phục hiện tượng python-docx nhân bản chuỗi cell text trong các cột merge.

### C. Nâng Cấp Kho Tri Thức Spoke (`ccba-legal-knowledge`)
- **Re-convert QCVN 07:2023/BXD**: Thay thế 12 bảng cũ (trong đó 5 bảng bị đè mất nội dung) bằng **25 bảng phân phần độc lập** (`bang_p02_01.csv` $\dots$ `bang_p09_02.csv`), `Duplicate table_ids: {}`. Khôi phục đầy đủ số liệu 50/50 tại Bảng 4 Phần 7.
- **Traceability Matrix**: Tự động đồng bộ [docs/adr/TRACEABILITY_MATRIX.md](file:///d:/GitHubProjects/ccba-legal-knowledge/docs/adr/TRACEABILITY_MATRIX.md) với 44 ADRs và các kỹ năng vừa tiến hóa.
- **Golden Snapshot**: Cập nhật [`.md/cache/golden_snapshots.json`](file:///d:/GitHubProjects/ccba-legal-knowledge/.md/cache/golden_snapshots.json), xác thực 60/60 bundles khớp 100%.

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Môi Trường | Lệnh Kiểm Tra | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :---: | :---: |
| **Hub Unit Tests** | Hub Package | `pytest packages/ccba-legal-intel/tests/test_technical_standard_strategy.py` | 4/4 passed (13.2s) | ✅ **PASSED** |
| **Hub Code Quality** | Hub Package | `ruff check` + `mypy --strict` (15 files) | 0 errors | ✅ **PASSED** |
| **Golden Snapshot** | Spoke | `python scripts/test_converter_regression.py --verify` | **60/60 Match (100%)** | ✅ **PASSED** |
| **Master CI Gates** | Spoke | `python scripts/validate_legal_spoke.py --skip-pdf-vault` | **15/15 Gates Passed** | ✅ **PASSED** |
| **Hermetic Teardown** | Spoke | `check_release_cleanliness.py --phase post` | Working tree clean | ✅ **PASSED** |
| **GitHub Actions CI** | Remote PR #12 | `Deterministic Parity & Schema Audit` | Passed (22s) | ✅ **PASSED** |
| **Copilot Review Audit**| Remote PR #12 | `python scripts/validation/audit_pr_comments.py --pr 12` | 0 blockers, clean | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

<details>
<summary>Nhấn để xem chi tiết PR #10 & PR #11 (Phát hành ngày 2026-09-22)</summary>

### PR #10: Ingestion NĐ 339, NĐ 10, Sub-Gate 5.3 DAG & 24 VBPL Multi-line Spans
- **Nghị định 339/2026/NĐ-CP**: Nạp toàn diện vào `legal_docs/01_vbpl/nghi_dinh_339_2026_nd_cp/` với 135 điều khoản AST multi-line (`line_start < line_end`), bộ câu hỏi chuẩn hóa QA benchmark, mỏ neo nguồn (.docx, .pdf) và thiết lập quan hệ `relations: { replaces: '16/2022/NĐ-CP' }`.
- **Nghị định 10/2021/NĐ-CP**: Đóng gói bundle lịch sử và đánh dấu trạng thái `expired`, thiết lập quan hệ `relations: { replaced_by: '206/2026/NĐ-CP' }`.
- **Sub-Gate 5.3 Transitive DAG BFS Engine**: Nâng cấp `scripts/validate_legal_spoke.py` với bộ giải đồ thị có hướng hai tầng.
- **Batch Span Migration 24 VBPL Bundles**: Chuyển dịch toàn bộ 24 bundles VBPL di sản từ single-line span sang multi-line AST spans chuẩn xác.

### PR #11: Tinh Chỉnh CI Ergonomics, Triệt Tiêu Warnings & Idempotent RPC Sync
- **Khử 2 False-Positive Warnings**: Tinh chỉnh heuristic kiểm tra số lượng điều khoản AST tại `_validate_vbpl_ast_clauses`.
- **Hỗ trợ Local Developer Ergonomics**: Bổ sung cờ CLI `--skip-pdf-vault` và nhận diện biến môi trường `CCBA_SKIP_PDF_VAULT=1`.
- **Đồng bộ Idempotent Cloud RAG (NotebookLM)**: Kết nối phiên Google thật (`macvnboy@gmail.com`) và nạp hoàn tất **47 nguồn tri thức hoạt động** vào `CCBA_Legal_Knowledge_Base_2026`.

</details>
