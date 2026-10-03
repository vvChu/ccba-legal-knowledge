# Walkthrough: Phát Hành Tính Năng PR #19 (Nạp 2 Văn Bản Luật Tier 1: Luật Nhà Ở 2023 & Luật Đất Đai 2024 Chuẩn OKF v2.4 Universal)

> **Mục tiêu:** Mở rộng cơ sở dữ liệu tri thức pháp lý Spoke theo lộ trình mở rộng Tier 1, nạp toàn văn nguyên văn 100% Luật Nhà ở 2023 (`27/2023/QH15`) và Luật Đất đai 2024 (`31/2024/QH15`) theo chuẩn OKF v2.4 Universal, cấu trúc 4 ngăn kéo chuyên biệt, đồng bộ Sổ bộ Pháp lý, cập nhật Living Roadmap và đối soát chỉ mục Cloud RAG NotebookLM.
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **PR #19:** [vvChu/ccba-legal-knowledge#19](https://github.com/vvChu/ccba-legal-knowledge/pull/19)
> **CI Gate:** 100% Green (Deterministic Parity & Schema Audit PASSED in 19s, 0 Errors, 0 Blocker Comments)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (PR #19)

### A. Nạp Toàn Văn Luật Nhà Ở 2023 (`27/2023/QH15`)
- **Vị trí lưu trữ**: `legal_docs/01_vbpl/luat_nha_o_2023_27_2023_qh15/`.
- **Nguồn gốc công báo**: DOCX (109,658 B, SHA-256: `20e094b919ac9b2acef4ded15040ee3b2c9043776cdbff57d12eba01ad906305`) & PDF (37,158,011 B, SHA-256: `845027819231cccc087ba21c6a959b9a670ced96fc9da9e34185e30eef182d45`) được bảo vệ trong `sources/` và `.gitignore`.
- **Cấu trúc OKF v2.4**:
  - `clauses.json`: 978 điều khoản AST phân cấp chi tiết.
  - `luat_nha_o_2023_27_2023_qh15.md`: Thân văn bản quy phạm nguyên văn 1:1, không tóm tắt diễn giải (ADR 0037).
  - `tables/`: 1 bảng số liệu 2D (`bang_01.csv` & `bang_01.json`) kèm `tables_catalog.json` chuẩn ADR 0041.
  - `qa_benchmark.json`: 978 cặp câu hỏi - đáp đối soát ngữ nghĩa phục vụ RAG Benchmark.
  - `index.md` & `metadata.yaml`: Hoàn thiện cây mục lục và định danh pháp lý đầy đủ.

### B. Nạp Toàn Văn Luật Đất Đai 2024 (`31/2024/QH15`)
- **Vị trí lưu trữ**: `legal_docs/01_vbpl/luat_dat_dai_2024_31_2024_qh15/`.
- **Nguồn gốc công báo**: DOCX (170,384 B, SHA-256: `65500a3ff2553d7bd85ea5175f7cff526cb80e75d863c9b913bb9fef09f7a6d9`) & PDF (30,696,261 B, SHA-256: `a626dcf54621f31a567c22957d65546f8f35a95bdc250b8cd77fc7fff8966398`) được bảo vệ trong `sources/` và `.gitignore`.
- **Cấu trúc OKF v2.4**:
  - `clauses.json`: 1,500 điều khoản AST phân cấp chi tiết.
  - `luat_dat_dai_2024_31_2024_qh15.md`: Thân văn bản quy phạm nguyên văn 1:1.
  - `tables/`: 2 bảng số liệu 2D (`bang_01.csv`, `bang_02.csv`) kèm JSON và `tables_catalog.json`.
  - `qa_benchmark.json`: 1,500 cặp câu hỏi - đáp ngữ nghĩa RAG Benchmark.
  - `index.md` & `metadata.yaml`: Hoàn thiện cây mục lục và định danh pháp lý đầy đủ.

### C. Đăng Ký Sổ Bộ & Đồng Bộ Roadmap Mở Rộng
- **Sổ bộ Pháp lý (`legal_registry.yaml`)**:
  - Nâng tổng số văn bản từ **70** lên **72** tài liệu pháp quy.
  - Nâng nhóm danh mục `01_vbpl` từ **35** lên **37** văn bản.
- **Living Expansion Roadmap (`.md/knowledge/expansion_roadmap.md`)**:
  - Tự động cập nhật qua Validator: **72 Active Bundles**, **19 Pending Documents** (Tier 1 hoàn thành 2/8 văn bản).
- **Đối soát Cloud RAG NotebookLM Manifest**:
  - Xác nhận 65 bundles Ultra Tier (13.0% dung lượng NotebookLM), 1,528,662 từ sẵn sàng cho đồng bộ NotebookLM RAG.

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Môi Trường | Lệnh Kiểm Tra | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :---: | :---: |
| **Shift-Left Local Gate** | Local Spoke | `python scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors, 1 Telemetry Warning)** | ✅ **PASSED** |
| **Spoke Cleanliness** | Local Spoke | `python scripts/check_spoke_cleanliness.py` | **15/15 Scripts Budget, 0 Machine Leaks** | ✅ **PASSED** |
| **Visual Parity** | Local Spoke | `python scripts/lint_visual_parity.py` | **849 files scanned, 0 errors** | ✅ **PASSED** |
| **Hub Import Depth** | Local Spoke | `python scripts/check_hub_import_depth.py` | **44 files scanned, 0 violations (ADR 0044)** | ✅ **PASSED** |
| **GitHub Actions CI** | Remote PR #19 | `Deterministic Parity & Schema Audit` | **Passed (19s)** | ✅ **PASSED** |
| **Copilot Review Audit** | Remote PR #19 | `gh pr view 19 --json reviews,reviewRequests` | **0 blocker comments, clean** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

<details>
<summary>Nhấn để xem chi tiết PR #17 (Phát hành ngày 2026-10-02)</summary>

### PR #17: Kiến Trúc & Hoàn Thiện Dữ Liệu Tri Thức Pháp Lý OKF v2.4 Universal
- **Khắc phục môi trường CI & Gate 11**: Bổ sung `python-docx` trên Linux, cấu hình `requirements-dev.txt`, nâng cấp nhận diện phạm vi `verification_scope` VBHN.
- **Audit toàn diện 70/70 bundles**: Chuẩn hóa `registry_summary`, bổ sung `index.md` cho `qcvn_10_2024_bxd`.
- **Vệ sinh Spoke**: Lưu trữ `analyze_gate_audit.py` vào `.md/archive/legacy_scripts/`, bảo đảm 15/15 scripts budget.

</details>

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
