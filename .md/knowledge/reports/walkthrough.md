# Walkthrough: Phát Hành Tính Năng PR #40 (Nạp Quyết Định 1812/QĐ-BXD 2026 Từ Điển Dữ Liệu Quốc Gia Về Hoạt Động Xây Dựng v1.0 & Đồng Bộ Spoke Guardrails)

> **Mục tiêu:** Thu thập chính quy và chuyển đổi chuẩn OKF v2.4 Universal cho **Quyết định số 1812/QĐ-BXD ngày 21/10/2026** của Bộ Xây dựng (*Ban hành Từ điển dữ liệu Cơ sở dữ liệu quốc gia về hoạt động xây dựng và năng lực hành nghề hoạt động xây dựng - Phiên bản 1.0*); đồng bộ Layer-1 Constitution và chuyển dịch các script kiểm chuẩn sang `scripts/_guardrails/`; gia cố `spoke_cli.py` và GitHub Actions CI (`legal-knowledge-ci.yml`).
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **PR #40:** [vvChu/ccba-legal-knowledge#40](https://github.com/vvChu/ccba-legal-knowledge/pull/40)
> - **Merge Commit:** `ebccbe5` (Squash and merge)
> - **CI Gate:** 100% Green (6/6 Checks Passed, 15/15 Legal Gates Passed, 0 Errors)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (PR #40)

### A. Nạp Chuẩn OKF v2.4 Universal cho Quyết Định 1812/QĐ-BXD (2026)
- **Tài liệu nguồn xác thực SHA-256 (`sources/`)**:
  - `quyet_dinh_1812_qd_bxd_2026.docx`: `35,186 bytes` (`d6e7c7d3fdd25a187fe66eeddfaf843741dc8054e575b0a0718652ed1f6a2e19`)
  - `quyet_dinh_1812_qd_bxd_2026.pdf`: `921,231 bytes`, 38 trang (`db769ac3c9f7795152aa7f8989b71974e9e2e18ef5afe0a87b8737a77627942e`)
- **Cấu trúc Bundle `legal_docs/01_vbpl/quyet_dinh_1812_qd_bxd_2026/`**:
  - Văn bản quy phạm nguyên văn `quyet_dinh_1812_qd_bxd_2026.md` (2,875 dòng, Verbatim Parity 100%).
  - Bảng từ điển dữ liệu 2D `tables/csv/bang_01.csv` & `tables/json/bang_01.json` (176 hàng dữ liệu x 9 cột, Zero Ragged Rows).
  - Cây điều khoản `clauses.json`, `qa_benchmark.json`, `metadata.yaml` và đăng ký vào `legal_registry.yaml` (liên kết `guided_by`: `nghi_dinh_212_2026_nd_cp`, `thong_tu_39_2026_tt_bxd`).

### B. Đồng Bộ Layer-1 Constitution & Hiện Đại Hóa CI Matrix
- Đồng bộ `.agents/AGENTS.md` từ Hub `ccba-agent-platform` và di chuyển bộ kiểm chuẩn về `scripts/_guardrails/`.
- Cập nhật `scripts/spoke_cli.py` loại bỏ các trường sandbox tạm thời (`docx_path`, `pdf_path`, `attachments`, `links`) khi nạp `metadata_handoff.json`.
- Cập nhật `.github/workflows/legal-knowledge-ci.yml` và `verify_legal_harness.py` trỏ tới `scripts/_guardrails/` kèm cơ chế fallback quét secrets cho Maskara trên GitHub Actions runner.

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Loại Kiểm Tra | Lệnh Thực Thi / Workflow | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :--- | :---: |
| **Maskara Secret Gate** | Bảo mật mã nguồn | `python -m ccba_maskara.cli scan --staged` / CI | **0 secret leaks** | ✅ **PASSED** |
| **Cleanliness & Budget** | Vệ sinh Spoke | `python scripts/_guardrails/check_spoke_cleanliness.py` | **15/15 scripts budget, Clean** | ✅ **PASSED** |
| **Skills Governance** | Metadata Governance | Inline Python AST (ADR-0066/ADR-0057) | **100% Valid, GPI $\ge$ 12.0** | ✅ **PASSED** |
| **Pstack Verification** | Harness Smoke Test | `verify_legal_harness.py --mode smoke --skip-pdf-vault` | **All tests passed** | ✅ **PASSED** |
| **Master Legal CI Gates**| 15 Cổng Tri thức | `python scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors)** | ✅ **PASSED** |
| **Master Aggregator Gate**| Ruleset #23696513 | `Deterministic Parity & Schema Audit` | **Aggregated 5/5 sub-gates** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

<details>
<summary>Nhấn để xem chi tiết PR #37 (Phát hành ngày 2026-10-12)</summary>

### PR #37: Mạng Tri Thức Pháp Lý 5 Vành Đai Luật Xây Dựng 2025 & Suy Diễn Ngược Hai Chiều Trên RAM
- **Ontology 5 vành đai** kết nối Luật Xây dựng 2025 (`135/2025/QH15`) với 7 Nghị định thi hành, Nghị định xử phạt `339/2026/NĐ-CP`, 6 QCVN cốt lõi và phân cấp địa phương.
- **Động cơ suy diễn ngược 2 chiều trên RAM** (`build_bidirectional_legal_graph`) và Sub-Gate 5.4 / Sub-Gate 2.1.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #32 (Phát hành ngày 2026-10-06)</summary>

### PR #32: Triển Khai Pstack Verification Harness, Features Map & Hiện Đại Hóa Ma Trận 6 CI Gates
- **Kiến trúc Pstack 5 khối độc lập**: Clean-Slate Pre-flight, Dual-Mode Lifecycle, Deterministic Health Barrier, Evidence-Capture Suite, Guaranteed Cleanup ($300.0\text{ s}$ timeout).
- **Lập Bản Đồ 9 Tính Năng Quy Phạm**: Trong `features/INDEX.md` kèm quy tắc COND-01 chống gian lận dữ liệu.
- **Tái cấu trúc Ma trận CI 6 cổng song song**: Phân rã 1 job nguyên khối thành 5 cổng song song kèm Master Aggregator Gate khớp $1:1$ GitHub Ruleset `#23696513`.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #30 (Phát hành ngày 2026-10-05)</summary>

### PR #30: Số Hóa 6 Tiêu Chuẩn PCCC & Đường Đất Yếu, Cài Đặt Maskara Guardrail, Spoke Đạt 96 Bundles
- **Số hóa toàn diện 6 tiêu chuẩn**: `QCVN 02:2020/BCA`, `TCVN 13456:2022`, `TCVN 6379:2024`, `TCVN 7568-14:2025`, `TCCS 41:2022/TCĐBVN`, `TCCS 39:2022/TCĐBVN`.
- **Cài đặt Client-Side Guardrail**: Cài đặt `.githooks/pre-commit` kích hoạt `ccba-maskara` trước mỗi commit.
- **Đồng bộ Tri-Tier Cloud Vault**: 18 tệp nhị phân nguồn lên Google Drive Vault `gdrive:CCBA_Legal_Vault`.

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
