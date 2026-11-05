# Walkthrough: Phát Hành Tính Năng PR #44 & Hub PR #607 (Gia Cố Toàn Trình Pipeline `/ccba-legal-ingest`, Đồng Bộ Sổ Bộ 106 Bundles & Khóa Cổng Liên Kết Gate 2)

> **Mục tiêu:** Gia cố toàn trình chu trình `/ccba-legal-ingest` theo bản đồ [Wayfinder Map `legal-ingest-hardening`](../../wayfinder/legal-ingest-hardening/map.md) (`T-01` $\to$ `T-04`): đồng bộ toàn bộ 19 nghị định trong `decrees:` vào `registry_summary` (`total_documents: 106`), Sub-Gate 5.3 và `spoke_cli.py`; khắc phục lỗi sinh `index.md` / `metadata.yaml` trong `vbpl_admin.py` và sửa 28 tệp `index.md` / `metadata.yaml` kèm khóa kiểm tra liên kết an toàn CI tại Gate 2; hợp nhất cơ chế ADR 0043 Dual-PDF có fallback an toàn, sao chép `attachments` và trích xuất DOCX header hints ở chế độ `--docx` offline; chuẩn hóa báo cáo Nightly Telemetry và làm mới hàng đợi Provenance 106 bundles.
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **Spoke PR #44:** [vvChu/ccba-legal-knowledge#44](https://github.com/vvChu/ccba-legal-knowledge/pull/44) — Merge Commit: `9a06d36` (Squash and merge, 6/6 CI Checks Passed)
> - **Hub PR #607:** [vvChu/ccba-agent-platform#607](https://github.com/vvChu/ccba-agent-platform/pull/607) — Merge Commit: `80ff3c66` (Squash and merge, 8/8 CI Checks Passed)
> - **Biên bản Thẩm định Grok:** Stage 1 Plan Sign-off (`APPROVE_PLAN`, Session `2267034a-cd73-4564-b7cf-9fe2252de768`) & Stage 2 Code Sign-off (`APPROVE`, Risk: 2, 0 Blocking Conditions, Session `04c35a3e-65ef-482d-893b-d44eabea9d6c`).

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (Spoke PR #44 & Hub PR #607)

### A. T-01: Đồng Bộ Khối `decrees:` (19 Văn Bản) & Mở Rộng Sub-Gate 5.3 (106/106 Bundles)
- Cập nhật `get_spoke_stats`, `_find_existing_registry_entry`, `_merge_existing_registry_entry`, `_recompute_registry_summary` trong `scripts/spoke_cli.py`, Sub-Gate 5.3 (`_validate_legal_validity_and_in_force`) trong `scripts/validate_legal_spoke.py`, và `scripts/verify_all_docs_against_pdf.py` để quét hợp nhất cả 3 khóa `("laws", "decrees", "standards")` (**51 + 19 + 36 = 106 văn bản**).
- Bảo toàn hiệu lực pháp lý (`status: expired` của `10/2021/NĐ-CP`, `status: superseded` của `06/2021/TT-BXD`, `expiration_date`, `relations`, `pdf_origin`, `raw_scan_pdf`) khi re-ingest và cập nhật `registry_summary` trong `legal_registry.yaml` (`total_documents: 106`; `01_vbpl: 53, 02_qcvn: 17, 03_tcvn: 33, 04_appendices: 3`).

### B. T-02: Chuẩn Hóa Sinh `index.md` / `metadata.yaml` & Cổng Kiểm Định Liên Kết Gate 2 An Toàn CI
- Tại Hub `vbpl_admin.py`: Tách `_build_merged_bundle_metadata` và `_write_bundle_metadata_and_index`, bảo toàn các khóa mở rộng trong `metadata.yaml`, loại bỏ hoàn toàn các giá trị bịa đặt mặc định (`"Chính phủ"`, `"Thủ tướng Chính phủ"`, `"2021-03-03"`, `datetime.now()`), trỏ link PDF về `./sources/{pdf_name}` và ẩn `./templates/` hoặc `./tables/` khi số lượng bằng `0`.
- Tại Spoke: Sửa **11** tệp `index.md` ghi nhầm `"Chính phủ"`, **27** tệp `index.md` trỏ PDF ra ngoài `./sources/`, **8** dòng liên kết tới ngăn kéo rỗng, và bổ sung `_validate_index_md_links` trong Gate 2 (`scripts/validate_legal_spoke.py`).

### C. T-03: Hợp Nhất Điểm Vào Ingest Một Cửa, ADR 0043 Dual-PDF Fallback & Offline DOCX Hints
- Bổ sung `_handle_ingest_pdf_and_attachments` và `_extract_docx_header_hints` trong `scripts/spoke_cli.py` cùng cập nhật `execute_ingest_legal` trong `scripts/ccba_platform_cli.py`:
  - Hỗ trợ ADR 0043 Dual-PDF khi `pdf_tier == 3` (`_raw_scan.pdf` + `convert_to_pdf`) kèm nhánh fallback an toàn khôi phục bản scan nếu lỗi.
  - Sao chép `attachments` trực tiếp vào `sources/attachments/` của bundle và khóa `.gitignore` (`legal_docs/**/sources/attachments/*`, `.xlsx`, `.xls`, `.zip`, `.rar`).
  - Bóc tách tự động `document_number`, `issued_date`, `issued_by`, `title` từ bảng header và đoạn đầu DOCX khi chạy `--docx` offline.

### D. T-04: Chuẩn Hóa Nightly Telemetry & Hàng Đợi Provenance 106 Bundles
- Bổ sung `parse_master_ci_summary` trong `.md/tools/run_nightly_telemetry.py` cho cả `exit 0` và `exit != 0`; sửa tiêu đề động `len(records)` trong `generate_provenance_report_md` và làm mới `.md/knowledge/provenance_migration_queue.md` lên đúng **106 văn bản** (`103/103` gói chính quy đạt `VERIFIED`).

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Loại Kiểm Tra | Lệnh Thực Thi / Workflow | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :--- | :---: |
| **Maskara Secret Gate** | Bảo mật mã nguồn | `python -m ccba_maskara.cli scan --staged` / CI | **0 secret leaks** | ✅ **PASSED** |
| **Cleanliness & Budget** | Vệ sinh Spoke | `python scripts/_guardrails/check_spoke_cleanliness.py` | **Clean, 0 violations** | ✅ **PASSED** |
| **Skills Governance** | Metadata Governance | Inline Python AST (ADR-0066/ADR-0057) | **100% Valid, GPI $\ge$ 12.0** | ✅ **PASSED** |
| **Pstack Verification** | Harness Full & Smoke | `python .agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py` | **93/93 tests passed** | ✅ **PASSED** |
| **Master Legal CI Gates**| 15 Cổng Tri thức | `python scripts/validate_legal_spoke.py --skip-pdf-vault` | **15/15 Gates Passed (0 Errors)** | ✅ **PASSED** |
| **Hub CI Matrix (Py 3.10-3.12)**| 8 Jobs trên Hub | `gh pr checks 607 --repo vvChu/ccba-agent-platform` | **8/8 Checks Passed** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

<details>
<summary>Nhấn để xem chi tiết PR #40 (Phát hành ngày 2026-10-21)</summary>

### PR #40: Nạp Quyết Định 1812/QĐ-BXD 2026 Từ Điển Dữ Liệu Quốc Gia Về Hoạt Động Xây Dựng v1.0 & Đồng Bộ Spoke Guardrails
- **Tài liệu nguồn xác thực SHA-256 (`sources/`)**:
  - `quyet_dinh_1812_qd_bxd_2026.docx`: `35,186 bytes` (`d6e7c7d3fdd25a187fe66eeddfaf843741dc8054e575b0a0718652ed1f6a2e19`)
  - `quyet_dinh_1812_qd_bxd_2026.pdf`: `921,231 bytes`, 38 trang (`db769ac3c9f7795152aa7f8989b71974e9e2e18ef5afe0a87b8737a77627942e`)
- **Cấu trúc Bundle `legal_docs/01_vbpl/quyet_dinh_1812_qd_bxd_2026/`**:
  - Văn bản quy phạm nguyên văn `quyet_dinh_1812_qd_bxd_2026.md` (2,875 dòng, Verbatim Parity 100%).
  - Bảng từ điển dữ liệu 2D `tables/csv/bang_01.csv` & `tables/json/bang_01.json` (176 hàng dữ liệu x 9 cột, Zero Ragged Rows).
  - Cây điều khoản `clauses.json`, `qa_benchmark.json`, `metadata.yaml` và đăng ký vào `legal_registry.yaml` (liên kết `guided_by`: `nghi_dinh_212_2026_nd_cp`, `thong_tu_39_2026_tt_bxd`).
- **Đồng Bộ Layer-1 Constitution & Hiện Đại Hóa CI Matrix**:
  - Đồng bộ `.agents/AGENTS.md` từ Hub `ccba-agent-platform` và di chuyển bộ kiểm chuẩn về `scripts/_guardrails/`.
  - Cập nhật `scripts/spoke_cli.py` loại bỏ các trường sandbox tạm thời (`docx_path`, `pdf_path`, `attachments`, `links`) khi nạp `metadata_handoff.json`.

</details>

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
