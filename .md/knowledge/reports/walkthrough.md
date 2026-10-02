# Walkthrough: Phát Hành Tính Năng PR #17 (Kiến Trúc & Hoàn Thiện Dữ Liệu Tri Thức Pháp Lý OKF v2.4 Universal)

> **Mục tiêu:** Nghiên cứu và hoàn thiện toàn diện kiến trúc kho tri thức Spoke pháp lý, giải quyết dứt điểm các lỗi kiểm định CI tại môi trường Linux, chuẩn hóa cấu trúc OKF v2.4 Universal cho 70/70 bundles, xác thực và đồng bộ dữ liệu VBHN và tối ưu ngân sách tệp kịch bản theo chuẩn Cleanliness.
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **PR #17:** [vvChu/ccba-legal-knowledge#17](https://github.com/vvChu/ccba-legal-knowledge/pull/17)
> **CI Gate:** 100% Green (Deterministic Parity & Schema Audit PASSED in 18s, 0 Errors, 0 Blocker Comments)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (PR #17)

### A. Khắc Phục Môi Trường CI & Rào Chắn Verbatim Parity (Gate 11)
- **Cài đặt `python-docx` trên Linux**: Khắc phục nguyên nhân gốc rễ gây 61 lỗi CI liên quan đến Gate 11. Bổ sung `requirements-dev.txt` khai báo đầy đủ các gói phụ thuộc môi trường Linux.
- **Nâng cấp Gate 11 Nhận Diện Phạm Vi VBHN (ADR 0037)**: Nâng cấp `scripts/validate_legal_spoke.py` tự động đọc `verification_scope` từ `metadata.yaml`. Đối với văn bản hợp nhất (`vbhn_consolidation`), chuyển đổi delta 54 đoạn bãi bỏ/thay thế của Sửa đổi 1:2023 sang telemetry warning thay vì fail CI.
- **Chuẩn hóa Metadata `qcvn_06_2022_bxd`**: Khai báo khối `verification_scope` xác định rõ phạm vi hợp nhất với Thông tư 09/2023/TT-BXD (SĐ1:2023).

### B. Audit Toàn Diện & Chuẩn Hóa Cấu Trúc OKF v2.4 (ADR 0036)
- **Audit Đối Chiếu Registry vs File System**: Xác nhận độ phủ tuyệt đối 70/70 bundles (35 VBPL, 14 QCVN, 18 TCVN, 3 Phụ lục so sánh).
- **Cập Nhật `registry_summary`**: Hiệu chỉnh số liệu tổng tài liệu từ 63 lên 70 và chuẩn hóa phân bổ danh mục theo đúng thực tế lưu trữ.
- **Bổ sung `index.md` cho `qcvn_10_2024_bxd`**: Hoàn thiện mục lục điều hướng AST cho Quy chuẩn kỹ thuật quốc gia về tiếp cận sử dụng (Gate 2).
- **Khảo sát Compartments QCVN**: Xác nhận 9 QCVN thiếu `templates/` hoặc `annexes/` hoàn toàn tuân thủ ADR 0036 do không phát sinh biểu mẫu hành chính nguyên tử hay phụ lục kỹ thuật độc lập.

### C. Vệ Sinh Spoke & Tối Ưu Ngân Sách Script (ADR 0044)
- **Thu hồi script một lần**: Lưu trữ `scripts/analyze_gate_audit.py` vào `.md/archive/legacy_scripts/` để đưa số lượng tệp trong `scripts/` về đúng ngưỡng chuẩn 15/15 files.
- **Cleanliness Gate**: Đạt 100% PASS, 0 rò rỉ đường dẫn máy tuyệt đối.

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Môi Trường | Lệnh Kiểm Tra | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :---: | :---: |
| **Shift-Left Local Gate** | Local Spoke | `python scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors, 1 Telemetry Warning)** | ✅ **PASSED** |
| **Spoke Cleanliness** | Local Spoke | `python scripts/check_spoke_cleanliness.py` | **15/15 Scripts Budget, 0 Machine Leaks** | ✅ **PASSED** |
| **Visual Parity** | Local Spoke | `python scripts/lint_visual_parity.py` | **845 files scanned, 0 errors** | ✅ **PASSED** |
| **Hub Import Depth** | Local Spoke | `python scripts/check_hub_import_depth.py` | **44 files scanned, 0 violations (ADR 0044)** | ✅ **PASSED** |
| **GitHub Actions CI** | Remote PR #17 | `Deterministic Parity & Schema Audit` | **Passed (18s)** | ✅ **PASSED** |
| **Copilot Review Audit** | Remote PR #17 | `gh pr view 17 --json reviews,reviewRequests` | **0 blocker comments, clean** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

<details>
<summary>Nhấn để xem chi tiết PR #13 (Phát hành ngày 2026-09-23)</summary>

### PR #13: Tri-Tier Cloud Vault Hydration, Parity Hardening & Catalog Sync (ADR 0035, ADR 0059)
- **Đẩy kho nhị phân lên Cloud Vault**: Toàn bộ 142 tệp nguồn vật lý từ local `sources/` đã được đồng bộ an toàn lên Google Drive `CCBA_Legal_Vault` (`macvnboy@gmail.com`).
- **Động cơ Hydration Đa Nền Tảng (`scripts/hydrate_sources_from_vault.py`)**: Hỗ trợ đầy đủ cờ CLI, mount letter động, Self-Healing SHA-256.
- **Git Index Hygiene & Rào Chắn Pre-Commit Binary Shield**: Trục xuất 4 tệp nhị phân khỏi Git index, bảo vệ quy tắc `.gitignore`, bổ sung pre-commit hook.
- **Đồng Bộ Metadata & Catalog Registry (13 Văn Bản Quy Phạm)**: Khai báo `source_assets.docx` kèm mã băm SHA-256, bảo lưu TT 38/2026/TT-BXD chờ bóc tách 2,838 bảng định mức.
- **Thanh Lọc Cloud Vault & Dọn Dẹp Cục Bộ**: Xóa sạch 61 tệp `desktop.ini`, 5 tệp nháp duplicate trên Vault.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #12 (Phát hành ngày 2026-09-23)</summary>

### PR #12: Modular Dual-Dispatch Converter, Multipart Tables & QCVN 07 Parity
- **`strategy.py`**: Rút gọn từ 622 dòng xuống **184 dòng**, đóng vai trò **Dual-Dispatch Orchestrator** thuần túy.
- **`preprocessor.py` & `exporter.py`**: Bóc tách duyệt DOM blocks, ranh giới tiêu đề/quy phạm và xuất bundle markdown.
- **Khử trùng lặp bảng đa phần (ADR 0044) & Bóc tách footnote (ADR 0041)**: Tiền tố phân phần `bang_pXX_YY.csv/json`, trường `part_id` và bóc tách footnote khỏi ma trận CSV.
- **Re-convert QCVN 07:2023/BXD**: 25 bảng phân phần độc lập, khôi phục đầy đủ số liệu 50/50.
- **Golden Snapshot**: 60/60 bundles khớp 100%.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #10 & PR #11 (Phát hành ngày 2026-09-22)</summary>

### PR #10: Ingestion NĐ 339, NĐ 10, Sub-Gate 5.3 DAG & 24 VBPL Multi-line Spans
- **Nghị định 339/2026/NĐ-CP**: Nạp toàn diện vào `legal_docs/01_vbpl/nghi_dinh_339_2026_nd_cp/` với 135 điều khoản AST multi-line.
- **Nghị định 10/2021/NĐ-CP**: Đóng gói bundle lịch sử và đánh dấu trạng thái `expired`.
- **Sub-Gate 5.3 Transitive DAG BFS Engine**: Nâng cấp `scripts/validate_legal_spoke.py` với bộ giải đồ thị có hướng hai tầng.
- **Batch Span Migration 24 VBPL Bundles**: Chuyển dịch toàn bộ 24 bundles VBPL di sản từ single-line span sang multi-line AST spans chuẩn xác.

### PR #11: Tinh Chỉnh CI Ergonomics, Triệt Tiêu Warnings & Idempotent RPC Sync
- **Khử 2 False-Positive Warnings**: Tinh chỉnh heuristic kiểm tra số lượng điều khoản AST tại `_validate_vbpl_ast_clauses`.
- **Hỗ trợ Local Developer Ergonomics**: Bổ sung cờ CLI `--skip-pdf-vault` và nhận diện biến môi trường `CCBA_SKIP_PDF_VAULT=1`.
- **Đồng bộ Idempotent Cloud RAG (NotebookLM)**: Kết nối phiên Google thật (`macvnboy@gmail.com`) và nạp hoàn tất **47 nguồn tri thức hoạt động** vào `CCBA_Legal_Knowledge_Base_2026`.

</details>
