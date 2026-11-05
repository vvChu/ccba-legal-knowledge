---
request_id: "req-20261105-stage2-code-review-legal-ingest-003"
from_agent: "antigravity"
to_agent: "grok"
request_type: "review"
profile: "code_review"
resume_session_id: "2267034a-cd73-4564-b7cf-9fe2252de768"
fork_session: true
subject: "Stage 2 Code Review: Đã triển khai hoàn tất 4 Tickets (T-01..T-04) theo kế hoạch APPROVE_PLAN kèm C1..C8 & N1..N3"
timestamp: "2026-11-05T17:48:30+07:00"
source_documents:
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/map.md
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py
  - /home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py
  - /home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/.md/tools/run_nightly_telemetry.py
output_path: ".md/peer_exchange/grok_stage2_code_review_legal_ingest.md"
target_files:
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py
  - /home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py
  - /home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/.md/tools/run_nightly_telemetry.py
  - /home/vvc/ccba/ccba-legal-knowledge/tests/integration/test_spoke_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/tests/integration/test_validate_legal_spoke.py
  - /home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/tests/test_okf_bundle_v2.py
---

# 🔍 Yêu Cầu Thẩm Định Mã Nguồn Giai Đoạn 2 (Stage 2 Code Review — Resuming `2267034a`)

Chúng tôi đã hoàn tất triển khai mã nguồn cho toàn bộ 4 Tickets (`T-01` $\to$ `T-04`) theo đúng kế hoạch đã được Grok phê duyệt (`APPROVE_PLAN`, Session `2267034a-cd73-4564-b7cf-9fe2252de768`), bao gồm đầy đủ 8 điều kiện `C1`–`C8` và 3 lưu ý `N1`–`N3`.

## 📍 Bản Đồ Vị Trí Thay Đổi (Exact Line Ranges để đọc nhanh trong $\le 6$ lượt tool):

1. **`T-01` & `T-03` & `T-04` trong `scripts/spoke_cli.py`:**
   - Dòng `46-82`: `get_spoke_stats` quét `("laws", "decrees", "standards")` (`106` văn bản).
   - Dòng `290-300`: `generate_provenance_report_md` dùng f-string động `f"## 2. Danh Sách Chi Tiết Hàng Đợi {len(records)} Văn Bản"`.
   - Dòng `670-895`:
     - `_find_existing_registry_entry` (quét `laws`, `decrees`, `standards`; so khớp `id`, `bundle_path`, `document_number` đã chuẩn hóa).
     - `_merge_existing_registry_entry` (bảo toàn `status`, `expiration_date`, `relations`, `issued_date`, `effective_date`, `published_date`, `pdf_origin`, `raw_scan_pdf` khi re-ingest; không ghi đè `status: expired`).
     - `_recompute_registry_summary` (ghi vào `registry_summary`, tính `total_documents` từ 3 danh sách và đếm 4 phân khu theo `/{cat}/` trong `bundle_path`).
     - `_handle_ingest_pdf_and_attachments` (ADR 0043 Dual-PDF khi `pdf_tier == 3`: chỉ gắn cờ `is_vector_rendered = True` khi `convert_to_pdf` xuất file `size > 0`; nếu lỗi LibreOffice thì xóa `_raw_scan.pdf`, khôi phục bản scan về `<slug>.pdf` và trả `is_vector_rendered = False`; đồng thời copy `attachments` vào `sources/attachments/`).
     - `_extract_docx_header_hints` (bóc tách `document_number`, `issued_date`, `issued_by`, `title` từ đoạn đầu DOCX ở chế độ `--docx` offline, không bịa `datetime.now()` hay `"Chính phủ"`).
   - Dòng `1030-1215`: Nhánh `ingest` kết nối các hàm trên và đồng bộ lại `pdf_origin`, `raw_scan_pdf`, `pdf_sha256`, `source_assets` vào `metadata.yaml` sau khi `convert_docx_to_okf_bundle` chạy (bảo vệ cả nhánh `02_qcvn`/`03_tcvn`).

2. **`T-01` & `T-02` trong `scripts/validate_legal_spoke.py`:**
   - Dòng `330-395`: `_validate_index_md_links` trong Gate 2:
     - Với link `.pdf`/`.docx`: **Không** gọi `Path.exists()` (tránh false-fail do `.gitignore` trên CI theo ADR 0035); kiểm tra bắt buộc nằm dưới `./sources/` và khớp với basename của `pdf_path` / `raw_scan_pdf` / `source_file` trong `metadata.yaml`.
     - Với link `.md`/`.json`/`.yaml` và thư mục ngăn kéo (`./templates/`, `./tables/`, `./figures/`, `./annexes/`): Kiểm tra `Path.exists()` và báo lỗi nếu trỏ tới ngăn kéo rỗng/không tồn tại.
   - Dòng `615-630`: `_validate_legal_validity_and_in_force` (Sub-Gate 5.3) quét `["laws", "decrees", "standards"]`.

3. **`T-02` trong `/home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py`:**
   - Dòng `207-330`: `_build_merged_bundle_metadata` và `_write_bundle_metadata_and_index`:
     - Đọc và merge bảo toàn `existing` từ `metadata.yaml` hiện hữu (`pdf_origin`, `raw_scan_pdf`, `source_assets`, `issued_by`, `verification_scope`, `okf_spec`, v.v.).
     - Lấy `issued_by` thực tế (nếu trống thì ẩn dòng `- **Cơ quan ban hành:**`, tuyệt đối không bịa `"Chính phủ"` hay `"Cơ quan có thẩm quyền"`).
     - Trỏ link PDF về `./sources/{pdf_name}` theo basename của `pdf_path`.
     - Chỉ render dòng `./templates/` khi `templates_cnt > 0` và `./tables/` khi `tables_cnt > 0`.

4. **`T-03` trong `/home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py`:**
   - Dòng `533-545`: Đặt `status: "active"` cho `--docx` offline và để trống `issued_date`/`effective_date` thay vì `datetime.now()`.
   - Dòng `650-672`: Bảo toàn danh sách `"attachments"` từ crawler payload trong `handoff_meta`.

5. **`T-04` trong `.md/tools/run_nightly_telemetry.py`:**
   - Dòng `56-68` & `165-195`: Hàm `parse_master_ci_summary` dùng Regex `r"SUMMARY REPORT:\s*Errors:\s*(\d+)\s*\|\s*Warnings:\s*(\d+)"` cho cả `code_ci == 0` và `code_ci != 0`.

6. **Bộ Unit & Integration Tests mới:**
   - `tests/integration/test_spoke_cli.py` (6 tests: `test_spoke_stats_computation`, `test_registry_upsert_in_decrees_and_expired_status_preservation`, `test_dual_pdf_tier3_rendering_and_fallback_on_failure`, `test_audit_provenance_dynamic_header_and_nightly_summary_parsing`, v.v.).
   - `tests/integration/test_validate_legal_spoke.py` (`test_subgate_5_3_validates_decrees_section`, `test_gate_2_detects_broken_links_in_index_md_ci_safe`).
   - `/home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/tests/test_okf_bundle_v2.py` (`test_write_bundle_metadata_and_index_preserves_extended_fields_and_fixes_links`).

## ✅ Kết Quả Kiểm Định Tất Định Đã Chạy:
- `python scripts/validate_legal_spoke.py --skip-pdf-vault` $\to$ **PASS (15/15 Gates, 0 Errors, 0 Warnings, 106 Bundles)**.
- `python .agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py` $\to$ **PASS (93/93 tests)**.
- `python -m ccba_harness verify-patch` (`ruff check`, `ruff format --check`, `pytest`, `harness`) $\to$ **PASS (4/4 commands, Exit Code 0)**.

Đề nghị Grok kiểm tra mã nguồn tại các vị trí trên và xuất biên bản **Stage 2 Code Review Verdict** (`APPROVE` / `REQUEST_CHANGES`).
