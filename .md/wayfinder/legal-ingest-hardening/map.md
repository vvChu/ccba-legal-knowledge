# 🗺️ Wayfinder Map: Gia Cố Toàn Trình Pipeline `/ccba-legal-ingest` & Đồng Bộ Sổ Bộ 106 Bundles (Legal Ingest Pipeline Hardening & Registry Parity)

> **Trạng thái:** 🟢 **COMPLETED — GROK STAGE 1 (`APPROVE_PLAN`) & STAGE 2 CODE REVIEW (`APPROVE`, Risk: 2, 0 Blocking Conditions)**  
> **Thời điểm khởi tạo:** `2026-11-05T16:45:23+07:00` | **Stage 1 Sign-off:** `2267034a-cd73-4564-b7cf-9fe2252de768` | **Stage 2 Code Sign-off:** `04c35a3e-65ef-482d-893b-d44eabea9d6c`  
> **Phạm vi tác động:** Spoke `ccba-legal-knowledge` & Hub `ccba-agent-platform` (`packages/ccba-legal-intel`, `scripts/ccba_platform_cli.py`)  
> **Tiêu chuẩn kiểm định:** 15/15 Master CI Gates (`validate_legal_spoke.py`) + 5-Section Pstack Harness (`verify_legal_ingest_harness.py`)

---

## 🎯 1. Điểm Đích (Destination)

Đưa chu trình nạp và kiểm định tri thức pháp lý `/ccba-legal-ingest` đạt trạng thái **Nhất Quán Tuyệt Đối (Zero-Divergence & 100% Registry/Index Parity)** trên toàn bộ **106 bundles** hiện hữu và mọi văn bản nạp mới:
1. **Đồng bộ `registry_summary` & Kiểm định Hiệu lực 100% (106/106 Bundles):** Khóa `decrees:` (19 văn bản) trong [legal_registry.yaml](file:///home/vvc/ccba/ccba-legal-knowledge/legal_registry.yaml) được quét, cập nhật tại chỗ (bảo toàn `status`, `expiration_date`, `relations`, `pdf_origin`, `raw_scan_pdf`) và kiểm định hiệu lực pháp lý (Sub-Gate 5.3) đồng nhất với `laws:` (51 văn bản) và `standards:` (36 văn bản). Khóa `registry_summary` phản ánh chính xác `total_documents: 106` và đếm 4 phân khu theo `bundle_path` (`01_vbpl: 53`, `02_qcvn: 17`, `03_tcvn: 33`, `04_appendices: 3`).
2. **Chuẩn hóa Sinh `index.md` / `metadata.yaml` & Khóa Cổng Liên kết An toàn CI (0 Broken Links):** Bộ chuyển đổi [`vbpl_admin.py`](file:///home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py) merge bảo toàn các khóa mở rộng của `metadata.yaml` (`pdf_origin`, `raw_scan_pdf`, `source_assets`, `issued_by`, `verification_scope`), hiển thị đúng `issued_by`, trỏ đúng `./sources/{Path(pdf_path).name}` và ẩn `./templates/` khi `templates_cnt == 0`. Toàn bộ **11** file `index.md` ghi nhầm `"Chính phủ"` (thông tư, Luật PCCC, QĐ 1812) và **27** file `index.md` đứt link PDF/templates trên Spoke được khắc phục và kiểm soát tự động tại Gate 2 trên toàn bộ 105 file `index.md` (so khớp chuỗi POSIX với `metadata.yaml:pdf_path` cho tệp nhị phân bị `.gitignore`, và kiểm tra `Path.exists()` cho `.md`/`.json`/`.yaml` cùng thư mục ngăn kéo).
3. **Hợp nhất Điểm vào Ingest "Một Cửa" (Unified Ingest, ADR 0043 Dual-PDF Fallback & Offline Metadata):** Luồng [`spoke_cli.py:ingest`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L728-L1025) và [`ccba_platform_cli.py:execute_ingest_legal`](file:///home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py#L467-L736) tích hợp cơ chế **ADR 0043 Dual-PDF** có nhánh fallback an toàn (chỉ đóng cờ `pdf_origin: docx_vector_rendered` khi `convert_to_pdf` xuất thành công PDF hợp lệ; nếu LibreOffice/Word lỗi thì giữ nguyên bản scan và không đóng cờ), bảo vệ `.gitignore` cho `sources/attachments/`, và tự động bóc tách `doc_meta` từ DOCX khi chạy `--docx` offline mà không bịa ngày/cơ quan ban hành.
4. **Minh bạch Hóa Telemetry Ban đêm & Hàng đợi Provenance:** Báo cáo đêm [`run_nightly_telemetry.py`](file:///home/vvc/ccba/ccba-legal-knowledge/.md/tools/run_nightly_telemetry.py) bóc tách chính xác số lượng `Errors` và `Warnings` trên cả `exit 0` và `exit != 0` (giữ nguyên Tầng 1 Golden Cohort 11 bundles, Tầng 2 đọc `registry_summary` 106 bundles); bảng [`provenance_migration_queue.md`](file:///home/vvc/ccba/ccba-legal-knowledge/.md/knowledge/provenance_migration_queue.md) và bản sao `.md/data/legal_registry.yaml` được đồng bộ chính xác trên **106 văn bản**.

---

## 📝 2. Ghi Chú & Rào Chắn Bất Biến (Notes & Invariants)

- **Biên lai Tra cứu Reuse-First Gate (ADR-0061 Audit Receipt):**
  - `command`: `python scripts/ccba_platform_cli.py find-seam --in docx --out markdown --json`
  - `status`: `MATCH` | `index_sha256`: `bd53036ef0edb549a0686c36dd00f45439da6d38a17d809463bf50446ef8a642`
  - **Seams tái sử dụng:** `legal_ingest.v1` (`ccba_legal.crawler.TVPLCrawler`, `ccba_legal.vbhn_engine.VBHNEngine`), `ooxml_processor.v1` (`ccba_ooxml.sanitizer.DocxCanonicalSanitizer`, `ccba_ooxml.converter.convert_to_pdf`), `legal_markdown.v1` (`ccba_markdown.pipeline.ConversionPipeline`), `pdf_preprocessor.v1` (`ccba_pdf.preprocessor.PDFPreprocessor`).
- **Biên bản Thẩm định Đồng đẳng (Grok Stage 1 Plan Audit & Sign-off):**
  - Vòng 1 (`REVISE_PLAN` — 7 Blocking Conditions `C1`–`C7`, 1 Advisory `C8`): Session `bd8d9305-de15-4491-b8ce-5fbf59f16b4d` | File: [grok_review_wayfinder_legal_ingest_map.md](file:///home/vvc/ccba/ccba-legal-knowledge/.md/peer_exchange/grok_review_wayfinder_legal_ingest_map.md).
  - Vòng 2 (`APPROVE_PLAN` — 0 Blocking Conditions, 3 Implementation Notes `N1`–`N3`): Session `2267034a-cd73-4564-b7cf-9fe2252de768` | File: [grok_signoff_wayfinder_legal_ingest_map.md](file:///home/vvc/ccba/ccba-legal-knowledge/.md/peer_exchange/grok_signoff_wayfinder_legal_ingest_map.md).
- **Biên bản Thẩm định Mã nguồn (Grok Stage 2 Code Review & Sign-off):**
  - Vòng 1 (`REQUEST_CHANGES` — 3 Blocking Conditions `R1`–`R3`, 1 Advisory `N4`): Session `cd54d0f9-489c-4f06-80c7-235e4231ef41` | File: [grok_stage2_code_review_legal_ingest.md](file:///home/vvc/ccba/ccba-legal-knowledge/.md/peer_exchange/grok_stage2_code_review_legal_ingest.md).
  - Vòng 2 (`APPROVE` — Risk: 2, 0 Blocking Conditions): Session `04c35a3e-65ef-482d-893b-d44eabea9d6c` | File: [grok_stage2_signoff_legal_ingest.md](file:///home/vvc/ccba/ccba-legal-knowledge/.md/peer_exchange/grok_stage2_signoff_legal_ingest.md).
- **Rào chắn Hiến pháp:**
  - `ADR 0035 & ADR 0036`: Cấu trúc 4 ngăn kéo chuyên biệt + `sources/` bắt buộc; tệp nhị phân (`.pdf`, `.docx`, `sources/attachments/*`) được `.gitignore` và lưu trên Cloud Vault; đường dẫn chuẩn POSIX `/`.
  - `ADR 0043`: Lưu trữ song song `_raw_scan.pdf` và Vector PDF (`pdf_origin: docx_vector_rendered` chỉ đóng dấu khi render thành công).
  - `ADR 0058`: Mọi thay đổi code phải vượt qua kiểm định tự động (`validate_legal_spoke.py` và `verify_legal_ingest_harness.py`) với `exit code == 0`.
  - `ADR 0059`: Nghiêm cấm sinh dữ liệu giả lập (mock fallback) hoặc tự điền ngày/cơ quan ban hành giả khi không trích xuất được từ tài liệu gốc.

---

## ⚖️ 3. Quyết Định Đã Chốt (Decisions So Far)

- [x] **[D-01] Tái sử dụng 100% Deep Seams hiện hữu (Reuse-First Compliance):** Cấy trực tiếp vào [`spoke_cli.py`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py), [`validate_legal_spoke.py`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py), [`vbpl_admin.py`](file:///home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py) và [`ccba_platform_cli.py`](file:///home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py).
- [x] **[D-02] Bác bỏ 3 đề xuất trùng lặp qua Phản biện Vòng 2:** Xác nhận (1) Chặn Mock Fallback & Multi-session Login đã hoàn tất tại Hub PR `#573`, (2) Chuẩn hóa Lexicon & Clause Regex đã hoàn tất tại Hub PR `#563-#565`, và (3) Bộ Pstack Verification Harness 5 khối đã hoàn tất tại Spoke PR `#43`.
- [x] **[D-03] Đồ thị Phụ thuộc Thực thi 4 Tickets (`C1`–`C8` Grok Audit):**
  - [T-01: Đồng bộ Sổ bộ Khối decrees & Mở rộng Sub-Gate 5.3](tickets/01_decrees_registry_and_subgate_53_sync.md) và [T-02: Khắc phục Lỗi Sinh index.md / metadata.yaml & Cổng Kiểm định Liên kết Gate 2](tickets/02_index_metadata_codegen_and_gate2_link_check.md) là **2 ticket UNBLOCKED tại Biên giới (Frontier)**.
  - [T-03: Hợp nhất Điểm vào Ingest Một Cửa, ADR 0043 Dual-PDF & Offline Metadata](tickets/03_unified_ingest_dual_pdf_and_offline_meta.md) **phụ thuộc (blocked by)** [T-02: Khắc phục Lỗi Sinh index.md / metadata.yaml & Cổng Kiểm định Liên kết Gate 2](tickets/02_index_metadata_codegen_and_gate2_link_check.md) (để `_write_bundle_metadata_and_index` không ghi đè làm mất `pdf_origin`, `raw_scan_pdf`, `source_assets` sau khi `convert_docx_to_okf_bundle` chạy).
  - [T-04: Chuẩn hóa Báo cáo Nightly Telemetry & Hàng đợi Provenance 106 Bundles](tickets/04_nightly_telemetry_and_provenance_queue_sync.md) **phụ thuộc (blocked by)** [T-01: Đồng bộ Sổ bộ Khối decrees & Mở rộng Sub-Gate 5.3](tickets/01_decrees_registry_and_subgate_53_sync.md) (để Tầng 2 Nightly và bản sao `.md/data/legal_registry.yaml` thừa hưởng `registry_summary.total_documents: 106`).

---

## 🎫 4. Danh Sách Ticket Tại Biên Giới & Hàng Đợi Phụ Thuộc (Wayfinder Tickets)

- [x] **[T-01: Đồng bộ Sổ bộ Khối decrees & Mở rộng Sub-Gate 5.3](tickets/01_decrees_registry_and_subgate_53_sync.md)** `[Task - AFK]` *(CLOSED — P0 Khẩn cấp)*
  - **Câu hỏi / Mục tiêu sắc nét:** Làm thế nào để đưa toàn bộ **19 văn bản** trong khóa `decrees:` của [legal_registry.yaml](file:///home/vvc/ccba/ccba-legal-knowledge/legal_registry.yaml) vào luồng đếm (`get_spoke_stats`), cập nhật tại chỗ bảo toàn hiệu lực (`spoke_cli.py:ingest`) và lưới kiểm định Sub-Gate 5.3 ([`validate_legal_spoke.py`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py#L615)), đồng thời tính lại `registry_summary` (`total_documents: 106`, đếm 4 phân khu theo `bundle_path`)?
- [x] **[T-02: Khắc phục Lỗi Sinh index.md / metadata.yaml & Cổng Kiểm định Liên kết Gate 2](tickets/02_index_metadata_codegen_and_gate2_link_check.md)** `[Task - AFK]` *(CLOSED — P1 Cao)*
  - **Câu hỏi / Mục tiêu sắc nét:** Làm thế nào để sửa hàm [`_write_bundle_metadata_and_index`](file:///home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py#L226-L270) merge bảo toàn `metadata.yaml` (`pdf_origin`, `raw_scan_pdf`, `source_assets`, `issued_by`, `verification_scope`), lấy đúng `issued_by` (để trống nếu thiếu, không gán cứng `"Chính phủ"`), trỏ đúng `./sources/{Path(pdf_path).name}` và ẩn `./templates/` rỗng; đồng thời sửa **11** file `index.md` sai cơ quan ban hành, **27** file `index.md` đứt link và khóa kiểm tra tại Gate 2 trên toàn bộ 105 file `index.md` (an toàn với `.gitignore` trên CI)?
- [x] **[T-03: Hợp nhất Điểm vào Ingest Một Cửa, ADR 0043 Dual-PDF & Offline Metadata](tickets/03_unified_ingest_dual_pdf_and_offline_meta.md)** `[Task - AFK]` *(CLOSED — P1 Cao)*
  - **Câu hỏi / Mục tiêu sắc nét:** Làm thế nào để hợp nhất cơ chế **ADR 0043 Dual-PDF** có fallback an toàn (chỉ đóng cờ `pdf_origin: docx_vector_rendered` khi `convert_to_pdf` thành công; giữ nguyên scan nếu lỗi), sao chép `attachments` từ crawler payload kèm quy tắc `.gitignore` cho `legal_docs/**/sources/attachments/*`, và trích xuất `doc_meta` từ DOCX khi chạy `--docx` offline mà không bịa ngày/cơ quan ban hành?
- [x] **[T-04: Chuẩn hóa Báo cáo Nightly Telemetry & Hàng đợi Provenance 106 Bundles](tickets/04_nightly_telemetry_and_provenance_queue_sync.md)** `[Task - AFK]` *(CLOSED — P2 Trung bình)*
  - **Câu hỏi / Mục tiêu sắc nét:** Làm thế nào để [`run_nightly_telemetry.py`](file:///home/vvc/ccba/ccba-legal-knowledge/.md/tools/run_nightly_telemetry.py#L157) parse đúng `SUMMARY REPORT: Errors: (\d+) \| Warnings: (\d+)` trên cả `exit 0` và `exit != 0` (giữ nguyên Tầng 1 Golden Cohort 11 bundles), sửa tiêu đề cứng `"38 Văn Bản"` tại [`spoke_cli.py:297`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L297), làm mới [`provenance_migration_queue.md`](file:///home/vvc/ccba/ccba-legal-knowledge/.md/knowledge/provenance_migration_queue.md) (không kèm `--attest-group-a`) và đồng bộ `.md/data/legal_registry.yaml`?

---

## 🌫️ 5. Sương Mù Chiến Trận / Chưa Xác Định Rõ (Not Yet Specified)

- **[Fog-01] Quy hoạch Schema Sổ bộ `legal_registry.yaml` Thế hệ Tiếp theo (`decrees:` vs `laws:`):** Hiện tại các văn bản thuộc `01_vbpl` đang nằm ở cả `laws:` (51 mục — chứa cả một số QCVN và 3 phụ lục `04_appendices`) và `decrees:` (19 mục). Sau khi [T-01: Đồng bộ Sổ bộ Khối decrees & Mở rộng Sub-Gate 5.3](tickets/01_decrees_registry_and_subgate_53_sync.md) vá xong điểm mù quét 3 khóa và đếm phân khu theo `bundle_path`, cần đánh giá xem ở phiên bản schema `0.4.0` có nên tái tổ chức khóa theo đúng 4 phân khu vật lý (`01_vbpl`, `02_qcvn`, `03_tcvn`, `04_appendices`) hay giữ nguyên 3 khóa để tương thích ngược với các công cụ đọc registry bên ngoài.
- **[Fog-02] Đồng bộ Tự động Kho Đám mây `CCBA_Legal_Vault` cho Thư mục `sources/attachments/`:** Khi [T-03: Hợp nhất Điểm vào Ingest Một Cửa, ADR 0043 Dual-PDF & Offline Metadata](tickets/03_unified_ingest_dual_pdf_and_offline_meta.md) bổ sung lưu trữ các tệp phụ lục đính kèm rời (`.xlsx`, `.docx`, `.zip` từ crawler payload) vào `sources/attachments/` và chặn commit bằng `.gitignore`, cần xác định quy ước ánh xạ `source_assets.attachments` trên Google Drive Vault và trong `hydrate_sources_from_vault.py` ở các phiên tiếp theo.

---

## 🚫 6. Ngoài Phạm Vi (Out of Scope)

- **Cơ chế Chống Mock Fallback & Xử lý Multi-Session Login trên TVPL:** Đã tồn tại và vận hành ổn định sau Hub PR `#573` (`execute_ingest_legal` & `selectors.py`).
- **Bộ Từ điển Thuật ngữ Pháp lý (Legal Lexicon) & Regex Điều khoản Đa phương ngữ:** Đã tồn tại trong `ccba_legal/lexicon/` sau Hub PR `#563`, `#564`, `#565`.
- **Xây dựng Mới Bộ Kiểm thử Pstack 5 Khối cho `/ccba-legal-ingest`:** Đã tồn tại tại [`verify_legal_ingest_harness.py`](file:///home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py) (Spoke PR `#43`).
- **Viết lại Động cơ Chuyển đổi DOCX/PDF Cốt lõi (`DocxCanonicalSanitizer` / `ConversionPipeline`):** Giữ nguyên kiến trúc Deep Seams hiện hữu theo nguyên tắc KISS và Reuse-First Gate (ADR-0061).
