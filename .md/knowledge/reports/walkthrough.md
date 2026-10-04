# Walkthrough: Phát Hành Tính Năng PR #30 (Số Hóa 6 Tiêu Chuẩn PCCC & Đường Đất Yếu, Cài Đặt Maskara Guardrail, Spoke Đạt 96 Bundles)

> **Mục tiêu:** Số hóa, bóc tách và đóng gói hoàn thiện 6 tiêu chuẩn quy phạm trọng yếu về PCCC và thiết kế đường ô tô trên nền đất yếu/mặt đường BTXM; tích hợp client-side security guardrail `ccba-maskara` (pre-commit hook); đồng bộ 100% tài sản nhị phân lên `CCBA_Legal_Vault`; và giải quyết triệt để 6/6 phát hiện từ Copilot Review.
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **PR #30:** [vvChu/ccba-legal-knowledge#30](https://github.com/vvChu/ccba-legal-knowledge/pull/30)
> **CI Gate:** 100% Green (Master CI Gates PASSED, 0 Errors, 1 Telemetry Warning, 1038 Markdown Files 100% Visual Parity)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (PR #30)

### A. Số Hóa Toàn Diện 6 Tiêu Chuẩn & Quy Chuẩn Trọng Yếu
1. **`QCVN 02:2020/BCA`** (`legal_docs/02_qcvn/qcvn_02_2020_bca/`):
   - Quy chuẩn kỹ thuật quốc gia về Trạm bơm nước chữa cháy.
   - 235 điều khoản AST, 6 bảng dữ liệu 2D tra cứu trong `tables/`, 235 QA benchmark pairs, đầy đủ provenance metadata.
2. **`TCVN 13456:2022`** (`legal_docs/03_tcvn/tcvn_13456_2022/`):
   - Phương tiện chiếu sáng sự cố và chỉ dẫn thoát nạn — Yêu cầu thiết kế, lắp đặt.
   - 46 điều khoản AST, 1 bảng tra cứu 2D, 8 thẻ thị giác tham số hóa (`figures/cards/hinh_{1..a_8}.md`), 46 QA pairs.
3. **`TCVN 6379:2024`** (`legal_docs/03_tcvn/tcvn_6379_2024/`):
   - Thiết bị chữa cháy — Trụ nước chữa cháy — Yêu cầu kỹ thuật.
   - 57 điều khoản AST, 2 bảng 2D, 5 thẻ thị giác cấu tạo trụ nổi/ngầm/hố van (`figures/cards/hinh_{a_1..d_1}.md`), 57 QA pairs.
4. **`TCVN 7568-14:2025`** (`legal_docs/03_tcvn/tcvn_7568_14_2025/`):
   - Hệ thống báo cháy — Phần 14: Thiết kế, lắp đặt hệ thống báo cháy cho nhà và công trình (thay thế TCVN 7568-14:2015 & TCVN 5738:2021).
   - 179 điều khoản AST, 2 bảng 2D, 10 thẻ thị giác sơ đồ bố trí (`figures/cards/hinh_{1..10}.md`), 3 phụ lục kỹ thuật quy phạm (`annexes/`), 179 QA pairs.
5. **`TCCS 41:2022/TCĐBVN`** (`legal_docs/03_tcvn/tccs_41_2022_tcdbvn/`):
   - Khảo sát, thiết kế nền đường ô tô trên nền đất yếu.
   - 81 điều khoản AST, 22 thẻ thị giác sơ đồ & toán đồ Osterberg/PVD (`figures/cards/hinh_{1..e_9}.md`), 81 QA pairs.
6. **`TCCS 39:2022/TCĐBVN`** (`legal_docs/03_tcvn/tccs_39_2022_tcdbvn/`):
   - Thiết kế mặt đường bê tông xi măng thông thường có khe nối trong xây dựng công trình giao thông.
   - 14 điều khoản AST, 13 thẻ thị giác cấu tạo khe nối và bố trí thép (`figures/cards/hinh_{1..13}.md`), 14 QA pairs.

### B. Cài Đặt Client-Side Guardrail: CCBA Maskara Pre-Commit Hook
- **Cấu hình Hook**: Cài đặt `.githooks/pre-commit` kích hoạt `python -m ccba_maskara.cli scan --staged` trước mỗi commit.
- **Git Attributes**: Thiết lập `.gitattributes` (`.githooks/* text eol=lf`) để đảm bảo tính tất định trên cả Linux và Windows.
- **Bảo mật tuyệt đối**: Tự động phát hiện và chặn các rò rỉ API key, credentials, private key trên các tệp staged.

### C. Đồng Bộ Tri-Tier Cloud Vault (ADR 0035)
- Đồng bộ thành công 18 tệp nhị phân nguồn (`.pdf`, `.docx`, `_raw_scan.pdf`) của cả 6 tiêu chuẩn lên Google Drive Vault `gdrive:CCBA_Legal_Vault`.

### D. Giải Quyết Triệt Để 6/6 Góp Ý Từ Copilot Code Review
- **Review ID**: `PRR_kwDOT56haM8AAAABQicr9Q` (Copilot Pull Request Reviewer).
- **Trạng thái**: ✅ **100% RESOLVED**
  1. *Roadmap KPI regression (Comment #4172969397)*: Cập nhật `registry_summary.total_documents: 96` trong `legal_registry.yaml` và đồng bộ lại `expansion_roadmap.md` đạt chính xác 96 bundles.
  2. *QCVN 02 missing metadata (Comment #4172969407)*: Bổ sung đầy đủ `bundle_path`, `source_file`, `sha256`, `cong_bao_number`, `source_assets` vào `qcvn_02_2020_bca/metadata.yaml`.
  3. *TCCS 39 incorrect jurisdiction (Comment #4172969414)*: Sửa nhãn jurisdiction từ `CONG_AN` thành `CQXD` cho các điều khoản tính toán tải trọng xe/kiểm toán.
  4. *TCCS 41 duplicate FIG_B_1 (Comment #4172969426)*: Khử trùng lặp entry `FIG_B_1` trong `figures_catalog.yaml` và cập nhật `total_figures: 22`.
  5. *TCVN 7568-14 duplicate figures (Comment #4172969437)*: Khử trùng lặp các thẻ `FIG_1`, `FIG_6`, `FIG_9` trong `figures_catalog.yaml` và cập nhật `total_figures: 10`.
  6. *TCVN 7568-14 missing formula C.2 (Comment #4176557868)*: Khử bỏ toàn bộ chuỗi ký tự rác OCR và cập nhật công thức KaTeX chuẩn mực $I_C = \frac{1{,}25[(I_Q \times 5) + (I_A \times 0{,}5)]}{24} \qquad (C.2)$ vào phụ lục C.

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Môi Trường | Lệnh Kiểm Tra | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :---: | :---: |
| **Shift-Left Local Gate** | Local Spoke | `python scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors, 1 Telemetry Warning)** | ✅ **PASSED** |
| **Visual Parity Gate** | Local Spoke | `python scripts/lint_visual_parity.py` | **1,038 files scanned, 0 errors (100% Parity)** | ✅ **PASSED** |
| **Security Maskara Gate** | Local Spoke | `python -m ccba_maskara.cli scan --staged` | **Zero secret leaks** | ✅ **PASSED** |
| **GitHub Actions CI** | Remote PR #30 | `CCBA Legal Knowledge Spoke CI Gates` | **Passed (22s)** | ✅ **PASSED** |
| **Copilot Review Audit** | Remote PR #30 | `gh api repos/vvChu/ccba-legal-knowledge/pulls/30/comments` | **6/6 findings resolved** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

<details>
<summary>Nhấn để xem chi tiết PR #21 (Phát hành ngày 2026-10-03)</summary>

### PR #21: Đồng Bộ Cloud RAG NotebookLM & Ưu Tiên 6 Văn Bản Đấu Thầu 2024–2026 Vào Living Roadmap
- **Khắc phục lỗi xác thực Playwright (`notebooklm-py`)**: Truy vết và hotfix lỗi race condition / premature commit tại `browser_capture.py`.
- **Thực thi đồng bộ 65 nguồn văn bản quy phạm**: Tải mới 37 nguồn tri thức vào sổ tay `CCBA_Legal_Knowledge_Base_2026`.
- **Nghiên cứu thể chế & bổ sung 6 văn bản đấu thầu**: NĐ 349/2026, Luật 57/2024, NĐ 225/2025, TT 05/2024, TT 105/2025, TT 03/2024.

</details>

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
