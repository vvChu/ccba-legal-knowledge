# Walkthrough: Phát Hành Tính Năng PR #21 (Đồng Bộ Cloud RAG NotebookLM & Ưu Tiên 6 Văn Bản Đấu Thầu 2024–2026 Vào Living Roadmap)

> **Mục tiêu:** Hoàn thiện 100% đồng bộ toàn văn 65 nguồn quy phạm lên Google NotebookLM Cloud RAG (`CCBA_Legal_Knowledge_Base_2026`), vá lỗi thư viện Playwright polling capture, và cập nhật nghiên cứu hệ thống văn bản đấu thầu mới nhất (2024–2026) bổ sung 6 văn bản trọng yếu vào Living Expansion Roadmap.
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **PR #21:** [vvChu/ccba-legal-knowledge#21](https://github.com/vvChu/ccba-legal-knowledge/pull/21)
> **CI Gate:** 100% Green (Deterministic Parity & Schema Audit PASSED in 27s, 0 Errors, 0 Blocker Comments)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (PR #21)

### A. Đồng Bộ 100% Kho Tri Thức Lên Google NotebookLM Cloud RAG
- **Khắc phục lỗi xác thực Playwright (`notebooklm-py`)**: 
  - Truy vết và hotfix lỗi race condition / premature commit tại `browser_capture.py` và `wait_for_login_landing()`.
  - Thay thế cơ chế commit sớm bằng vòng lặp **Active Polling** kiểm tra cookie `SID` thực tế, cho phép mở và giữ cửa sổ trình duyệt đăng nhập trong 5 phút.
- **Thực thi đồng bộ 65 nguồn văn bản quy phạm**:
  - Tải mới **37 nguồn tri thức** (gồm toàn văn Luật Nhà ở 2023, Luật Đất đai 2024, Thông tư 79/2025/TT-BTC, và toàn bộ 14 QCVN, 18 TCVN).
  - Bỏ qua an toàn **28 nguồn** đã tồn tại sẵn trên Cloud.
  - Sổ tay `CCBA_Legal_Knowledge_Base_2026` (`6dca7e4e-c407-4d1f-882a-e0d9459d1120`) đã được nạp đầy đủ 100% nguồn tri thức chính quy.

### B. Nghiên Cứu Thể Chế & Bổ Sung 6 Văn Bản Đấu Thầu Mới Vào Roadmap
- **Nghị định 349/2026/NĐ-CP** *(09/09/2026)*: Sửa đổi, bổ sung Nghị định 214/2025/NĐ-CP về lựa chọn nhà thầu ➔ **TOP Tier 1 (Điểm: 10.3)**.
- **Luật số 57/2024/QH15** *(15/01/2025)*: Sửa đổi 21 điều then chốt của Luật Đấu thầu 2023 ➔ **TOP Tier 1 (Điểm: 10.1)**.
- **Nghị định 225/2025/NĐ-CP** *(15/08/2025)*: Sửa đổi Nghị định 23/2024/NĐ-CP và Nghị định 115/2024/NĐ-CP về lựa chọn nhà đầu tư ➔ **TOP Tier 2 (Điểm: 9.6)**.
- **Thông tư 05/2024/TT-BKHĐT**: Chi phí trong lựa chọn nhà thầu, nhà đầu tư trên Hệ thống mạng đấu thầu quốc gia ➔ **Tier 3 (Điểm: 8.9)**.
- **Thông tư 105/2025/TT-BTC**: Sửa đổi Thông tư 02/2024/TT-BKHĐT về đào tạo, chứng chỉ đấu thầu ➔ **Tier 3 (Điểm: 8.9)**.
- **Thông tư 03/2024/TT-BKHĐT**: Mẫu hồ sơ đấu thầu lựa chọn nhà đầu tư dự án đầu tư kinh doanh ➔ **Tier 3 (Điểm: 8.6)**.

### C. Đồng Bộ Living Expansion Roadmap (`expansion_roadmap.md`)
- Tổng số văn bản đang hoạt động trong Spoke: **72 bundles** (74.2%).
- Tổng số ứng viên đang chờ nạp: **25 văn bản** (25.8%).
- Tổng quy mô mục tiêu: **97 văn bản**.

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Môi Trường | Lệnh Kiểm Tra | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :---: | :---: |
| **Shift-Left Local Gate** | Local Spoke | `python scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors, 1 Telemetry Warning)** | ✅ **PASSED** |
| **Spoke Cleanliness** | Local Spoke | `python scripts/check_spoke_cleanliness.py` | **15/15 Scripts Budget, 0 Machine Leaks** | ✅ **PASSED** |
| **Visual Parity** | Local Spoke | `python scripts/lint_visual_parity.py` | **849 files scanned, 0 errors** | ✅ **PASSED** |
| **Hub Import Depth** | Local Spoke | `python scripts/check_hub_import_depth.py` | **44 files scanned, 0 violations (ADR 0044)** | ✅ **PASSED** |
| **GitHub Actions CI** | Remote PR #21 | `Deterministic Parity & Schema Audit` | **Passed (27s)** | ✅ **PASSED** |
| **Copilot Review Audit** | Remote PR #21 | `gh pr view 21 --json reviews,reviewRequests` | **0 blocker comments, clean** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

<details>
<summary>Nhấn để xem chi tiết PR #19 (Phát hành ngày 2026-10-03)</summary>

### PR #19: Nạp 2 Văn Bản Luật Tier 1 (Luật Nhà Ở 2023 & Luật Đất Đai 2024)
- **Luật Nhà ở 2023 (`27/2023/QH15`)**: 978 AST clauses, 1 bảng dữ liệu, 978 QA pairs.
- **Luật Đất đai 2024 (`31/2024/QH15`)**: 1,500 AST clauses, 2 bảng dữ liệu, 1,500 QA pairs.
- **Sổ bộ Pháp lý (`legal_registry.yaml`)**: Nâng từ 70 lên 72 văn bản pháp quy.
- **Google Drive Vault (`CCBA_Legal_Vault`)**: Tải lên và xác thực 100% SHA-256 cho 4 tệp DOCX/PDF gốc.

</details>

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
