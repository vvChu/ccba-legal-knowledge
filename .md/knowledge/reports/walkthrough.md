# Walkthrough: Phát Hành Tính Năng PR #32 (Triển Khai Pstack Verification Harness, Features Map & Hiện Đại Hóa Ma Trận 6 CI Gates)

> **Mục tiêu:** Thiết lập bộ công cụ kiểm định Pstack 5 khối (`ccba-verify-legal-knowledge`) tuân thủ chuẩn mực ADR-0009/ADR-0044/ADR-0066; lập bản đồ 9 tính năng quy phạm trong `features/INDEX.md` kèm quy tắc COND-01; tham vấn phản biện song phương với Grok-4.7; và tái cấu trúc CI GitHub Actions từ 1 job nguyên khối thành ma trận 5 cổng song song kèm Master Aggregator Gate ("Deterministic Parity & Schema Audit") giải quyết triệt để GitHub Ruleset #23696513.
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **PR #32:** [vvChu/ccba-legal-knowledge#32](https://github.com/vvChu/ccba-legal-knowledge/pull/32)
> - **Merge Commit:** `7920331` (Squash and merge)
> **CI Gate:** 100% Green (6/6 Checks Passed, 0 Errors, 0 Warnings, 100% Parity)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (PR #32)

### A. Triển Khai Pstack 5-Block Verification Harness (`ccba-verify-legal-knowledge`)
- **Kiến trúc Pstack 5 khối độc lập**:
  1. **Block 1 — Clean-Slate Pre-flight**: Dọn dẹp triệt để tiến trình mồ côi, kiểm tra tính sẵn sàng của port, tệp tin và môi trường cô lập trước khi chạy.
  2. **Block 2 — Dual-Mode Process Lifecycle**: Tương thích đa nền tảng hoàn toàn giữa POSIX (`os.setsid`) và Windows (`CREATE_NEW_PROCESS_GROUP`), quản lý vòng đời tiến trình kiểm định chặt chẽ.
  3. **Block 3 — Deterministic Health Barrier**: Cơ chế rào chắn xác định với độ trễ tối thiểu ($0.087\text{ s}$), đảm bảo dịch vụ sẵn sàng trước khi nạp bài test.
  4. **Block 4 — Evidence-Capture Suite**: Hỗ trợ 4 chế độ thu thập bằng chứng kiểm định (`snapshot`, `coverage`, `performance`, `full`) phục vụ truy vết lỗi và nghiệm thu.
  5. **Block 5 — Guaranteed Cleanup**: Khối dọn dẹp tất định cưỡng chế kết thúc tiến trình sau khi kiểm định, hỗ trợ per-step timeout $300.0\text{ s}$ chống treo vĩnh viễn.
- **Chuẩn hóa Metadata kỹ năng theo ADR-0066 / ADR-0057**:
  - `bundle: _core`, `scope: spoke`.
  - Chỉ số giá trị kỹ năng: $\mathbf{GPI} = 2.5S + 2.0K + 2.0A - 1.5P = 24.0 \ge 12.0$ (Đạt chuẩn Tier 2B Standalone Skill).

### B. Lập Bản Đồ Tính Năng Quy Phạm (`features/INDEX.md`)
- **Bản đồ 9 tính năng cốt lõi**:
  - `FEAT-001`: Tra cứu & kiểm định tính toàn vẹn Sổ bộ Quy chuẩn / Tiêu chuẩn (`legal_registry.yaml`).
  - `FEAT-002`: AST Clause Extraction & Zero-LLM Paraphrase Invariant.
  - `FEAT-003`: 2D Table Knowledge Extraction & Grid Regularity.
  - `FEAT-004`: Atomic Form Templates (`templates/`).
  - `FEAT-005`: High-Resolution Multimodal Vector Diagrams & SVG/Cards Integrity.
  - `FEAT-006`: KaTeX Math Syntax Integrity.
  - `FEAT-007`: In-Bundle Comparative Matrix & VBHN Consolidation.
  - `FEAT-008`: Tri-Tier Cloud Binary Vault & Provenance Tracking.
  - `FEAT-009`: Shift-Left Verification & 15-Gate Master CI Gate.
- **Rào chắn chống gian lận COND-01**: Cấm mọi hành vi mock dữ liệu, bỏ qua bước kiểm tra hoặc hạ ngưỡng chấp nhận.

### C. Tham Vấn Đối Soát Peer Review Song Phương Với Grok-4.7
- **Đánh giá Harness Pstack**: `.md/peer_exchange/grok_review_legal_spoke_verification_harness.md` (Kết luận: `APPROVE_WITH_CONDITIONS`, điểm rủi ro: 2/10).
- **Đánh giá Kiến trúc Ma trận CI**: `.md/peer_exchange/grok_review_ci_granularity_matrix.md` (Kết luận: `APPROVE_WITH_CONDITIONS`, điểm rủi ro: 2/10).
- **Ghi nhận & tiếp thu**: Bổ sung per-step timeout $300.0\text{ s}$, thiết lập umbrella aggregation gate chống rò rỉ trạng thái kiểm định.

### D. Tái Cấu Trúc & Hiện Đại Hóa Ma Trận 6 Cổng CI GitHub Actions
- **Chuyển đổi từ 1 Job nguyên khối sang Ma trận 5 cổng song song**:
  1. `security-secrets-gate`: Quét bảo mật toàn diện với `ccba-maskara` (cài đặt trực tiếp từ Hub Git repository).
  2. `spoke-cleanliness-gate`: Giám sát vệ sinh Spoke và ngân sách nghiêm ngặt $15/15$ scripts tại `scripts/`.
  3. `skills-governance-gate`: Kiểm tra tính hợp lệ của metadata kỹ năng theo ADR-0066 / ADR-0057 thông qua inline Python AST checker.
  4. `pstack-verification-gate`: Chạy bộ kiểm tra tự động của harness `ccba-verify-legal-knowledge`.
  5. `legal-knowledge-gates`: Chạy toàn bộ 15 Cổng kiểm định văn bản pháp lý Master CI (`validate_legal_spoke.py`).
- **Master Aggregator Gate (`Deterministic Parity & Schema Audit`)**:
  - Thu thập kết quả từ cả 5 cổng song song với `needs: [...]` và `if: always()`.
  - Khớp $1:1$ với Required Status Check của GitHub Ruleset `#23696513`, loại bỏ triệt để tình trạng check bị pending/treo vĩnh viễn mà không cần can thiệp quyền Admin repo.

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Loại Kiểm Tra | Lệnh Thực Thi / Workflow | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :---: | :---: |
| **Maskara Secret Gate** | Bảo mật mã nguồn | `python -m ccba_maskara.cli scan --staged` / CI | **0 secret leaks** | ✅ **PASSED** |
| **Cleanliness & Budget** | Vệ sinh Spoke | `python scripts/check_spoke_cleanliness.py` | **15/15 scripts budget, Clean** | ✅ **PASSED** |
| **Skills Governance** | Metadata Governance | Inline Python AST (ADR-0066/ADR-0057) | **100% Valid, GPI = 24.0** | ✅ **PASSED** |
| **Pstack Verification** | Harness Unit Test | `python -m unittest discover` | **All tests passed** | ✅ **PASSED** |
| **Master Legal CI Gates**| Pháp lý OKF v2.4 | `python scripts/validate_legal_spoke.py` | **15/15 Gates Passed** | ✅ **PASSED** |
| **Master Aggregator Gate**| GitHub Ruleset #23696513 | `Deterministic Parity & Schema Audit` | **Aggregated 5/5 sub-gates (3s)** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

<details>
<summary>Nhấn để xem chi tiết PR #30 (Phát hành ngày 2026-10-05)</summary>

### PR #30: Số Hóa 6 Tiêu Chuẩn PCCC & Đường Đất Yếu, Cài Đặt Maskara Guardrail, Spoke Đạt 96 Bundles
- **Số hóa toàn diện 6 tiêu chuẩn**: `QCVN 02:2020/BCA`, `TCVN 13456:2022`, `TCVN 6379:2024`, `TCVN 7568-14:2025`, `TCCS 41:2022/TCĐBVN`, `TCCS 39:2022/TCĐBVN`.
- **Cài đặt Client-Side Guardrail**: Cài đặt `.githooks/pre-commit` kích hoạt `ccba-maskara` trước mỗi commit.
- **Đồng bộ Tri-Tier Cloud Vault**: 18 tệp nhị phân nguồn lên Google Drive Vault `gdrive:CCBA_Legal_Vault`.
- **Giải quyết triệt để 6/6 góp ý từ Copilot Code Review**.

</details>

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
