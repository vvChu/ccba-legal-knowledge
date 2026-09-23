# Walkthrough: Phát Hành Tính Năng PR #13 (Tri-Tier Cloud Vault Hydration, Parity Hardening & Catalog Sync — ADR 0035, ADR 0059)

> **Mục tiêu:** Hoàn thiện kiến trúc Tri-Tier Cloud Binary Vault theo ADR 0035 / ADR 0059: Đẩy toàn bộ 142 tệp vật lý nhị phân (PDF/DOCX) lên Google Drive Cloud Vault (`CCBA_Legal_Vault`), trục xuất 100% tệp nhị phân khỏi Git tracking và thiết lập Pre-commit Binary Guardrail, tăng cường động cơ Hydration tự động hóa với cơ chế Tự Lành (Self-Healing) qua mã băm SHA-256, đồng bộ hóa 13 văn bản quy phạm với tài sản nguồn `source_assets.docx` trên cả metadata và registry, bảo lưu DOCX Thông tư 38/2026/TT-BXD chờ bóc tách 2,838 bảng định mức để bảo toàn Gate 11, thanh lọc sạch sẽ 61 tệp `desktop.ini` và các bản nháp duplicate trên Vault.
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **PR #13:** [vvChu/ccba-legal-knowledge#13](https://github.com/vvChu/ccba-legal-knowledge/pull/13) (Squash Commit: `4f15baa`)
> **CI Gate:** 100% Green (Deterministic Parity & Schema Audit PASSED in 19s, 0 Errors, 0 Blocker Comments)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (PR #13)

### A. Tri-Tier Cloud Binary Vault & Tự Động Hóa Hydration (ADR 0035 / ADR 0059)
- **Đẩy kho nhị phân lên Cloud Vault**: Toàn bộ 142 tệp nguồn vật lý từ local `sources/` đã được đồng bộ an toàn lên Google Drive `CCBA_Legal_Vault` (`macvnboy@gmail.com`).
- **Động cơ Hydration Đa Nền Tảng (`scripts/hydrate_sources_from_vault.py`)**:
  - Hỗ trợ đầy đủ các cờ CLI: `--push`, `--dry-run`, `--verify-only`, `--all`.
  - Dò tìm động mount letter qua `CCBA_VAULT_MOUNT_PATH` và danh sách ổ đĩa (`G:`, `H:`, `I:`), khử hoàn toàn hardcode đường dẫn máy trạm.
  - Quét bulk in-memory danh mục Cloud Vault qua `rclone lsf -R --files-only` để tra cứu $O(1)$ thay vì gọi rclone riêng lẻ.
  - Tích hợp cơ chế **Tự Lành (Self-Healing)**: Tự động đối soát SHA-256 sau khi tải về, loại bỏ file biến dạng và hỗ trợ tải đè để khôi phục trạng thái chuẩn.

### B. Git Index Hygiene & Rào Chắn Pre-Commit Binary Shield
- **Trục xuất 4 tệp nhị phân khỏi Git index**: Sử dụng `git rm --cached` cho `qcvn_04_2021_bxd.pdf`, `qcvn_06_2022_bxd.pdf`, `sd1_2023_qcvn_06_2022_bxd.pdf`, `tcvn_5574_2018.doc`. Kết quả `git ls-files` đạt 0 bytes nhị phân được theo dõi trong Git index.
- **Bảo vệ quy tắc `.gitignore`**: Bổ sung `legal_docs/**/sources/*.doc` và `legal_docs/**/*.doc`.
- **Pre-commit Binary Guard**: Bổ sung `check_staged_binary_files()` (`git diff --cached --name-only --diff-filter=ACMR`) vào `scripts/check_spoke_cleanliness.py`, cập nhật hook `.git/hooks/pre-commit` chặn lập tức mọi file `.pdf`, `.docx`, `.doc` bị stage nhầm.

### C. Đồng Bộ Metadata & Catalog Registry (13 Văn Bản Quy Phạm)
- Khai báo trường `source_assets.docx` kèm mã băm SHA-256 xác thực từ tệp vật lý cho 13 văn bản (TT 32, 33, 34, 36, 37, 39, 40, 41, TT 101/BQP, NĐ 193, NĐ 209, QCVN 02:2022, Luật PCCC & CNCH 2024) trên cả `metadata.yaml` và `legal_registry.yaml`.
- **Bảo lưu Thông tư 38/2026/TT-BXD**: Giữ tệp DOCX (4.37 MB) tại `.md/extracted_docs/38_2026_TT-BXD_712406.docx` chờ Ticket A3_Batch bóc tách 2,838 bảng định mức, tránh làm rớt Gate 11 Verbatim Parity (2.4% vs 98.0%).
- **Chuẩn hóa Thông tư 73/2026/TT-BTC**: Đổi tên `vault_path` thành `thong_tu_73_2026_tt_btc.docx` đồng bộ cả metadata và registry.
- **Gỡ bỏ khai báo ảo QCVN 04:2021/BXD**: Loại bỏ mục `docx:` không có thực.
- **Cấu hình NĐ 10 và NĐ 339**: Thiết lập `status: pending_acquisition` bảo toàn schema.

### D. Thanh Lọc Cloud Vault & Dọn Dẹp Cục Bộ
- **Trên Cloud Vault**: Xóa sạch 61 tệp `desktop.ini`, 5 tệp duplicate/nháp (`702686.pdf`, `702686.docx`, `luat_22_2023_qh15.pdf`, `luat_135_2025_qh15.pdf`, `test_vector.pdf`), purge thư mục mồ côi `02_qcvn/01_2021_tt_bxd/` và bảo tồn nguyên vẹn thư mục hợp lệ `01_vbpl/10_2021_nd_cp/`.
- **Trên đĩa cục bộ**: Dọn sạch các tệp trùng trong `sources/` và xóa 2 thư mục crawler rỗng trong `qcvn_09_2017_bxd/sources/`.

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Môi Trường | Lệnh Kiểm Tra | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :---: | :---: |
| **Git Binary Tracking** | Local Spoke | `git ls-files "legal_docs/**/*.pdf" "legal_docs/**/*.docx" "legal_docs/**/*.doc"` | **0 files (0 bytes)** | ✅ **PASSED** |
| **Cleanliness & Guardrail**| Local Spoke | `python scripts/check_spoke_cleanliness.py` | **0 errors, 0 warnings** | ✅ **PASSED** |
| **Vault Integrity Check** | Local + Cloud | `python scripts/hydrate_sources_from_vault.py --verify-only` | **138/138 verified (0 missing, 0 mismatches)** | ✅ **PASSED** |
| **Self-Healing Hydration** | Local Spoke | `python scripts/hydrate_sources_from_vault.py --all` | **3/3 hydrated & verified** | ✅ **PASSED** |
| **Master CI Gates** | Local Spoke | `python scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors, 0 Warnings)** | ✅ **PASSED** |
| **GitHub Actions CI** | Remote PR #13 | `Deterministic Parity & Schema Audit` | **Passed (19s)** | ✅ **PASSED** |
| **Copilot Review Audit**| Remote PR #13 | `gh pr view 13 --json reviewRequests,reviews` | **0 blocker comments, clean** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

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
