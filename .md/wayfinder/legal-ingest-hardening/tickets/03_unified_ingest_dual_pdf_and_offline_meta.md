# Ticket 03: Hợp nhất Điểm vào Ingest Một Cửa, ADR 0043 Dual-PDF & Offline Metadata

- **Type:** Task (AFK / Code Implementation)
- **Priority:** P1 (Cao)
- **Status:** closed
- **Assignee:** Antigravity AI
- **Target Seams & Files:**
  - [spoke_cli.py](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L728-L1050) (`ingest`)
  - [ccba_platform_cli.py](file:///home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py#L467-L736) (`execute_ingest_legal`)
  - [cli.py](file:///home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/cli.py#L858-L945) (`handle_ingest`)
  - [.gitignore](file:///home/vvc/ccba/ccba-legal-knowledge/.gitignore#L60-L66) (bổ sung `legal_docs/**/sources/attachments/*`)
  - [AGENTS.md](file:///home/vvc/ccba/ccba-legal-knowledge/AGENTS.md#L56) & [sync_expansion_roadmap.py](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/sync_expansion_roadmap.py#L238)
- **Reference:** [Wayfinder Map: Gia Cố Toàn Trình Pipeline `/ccba-legal-ingest`](../map.md), ADR 0035, ADR 0043, ADR 0059, Grok Audit `C5`, `C6`

---

## ❓ Câu Hỏi / Vấn Đề Cốt Lõi Cần Giải Quyết
Làm thế nào để hợp nhất cơ chế **ADR 0043 Dual-PDF** có nhánh fallback an toàn (`pdf_tier == 3` $\to$ chỉ đóng cờ `pdf_origin: docx_vector_rendered` khi `convert_to_pdf` thành công; giữ nguyên bản scan nếu lỗi), sao chép `attachments` từ crawler payload kèm khóa `.gitignore` chống rò rỉ tệp nhị phân, và trích xuất `doc_meta` từ DOCX khi chạy `--docx` offline mà không tự bịa ngày/cơ quan ban hành?

---

## 🎯 Mục Tiêu Thực Thi (KISS Implementation Scope — Tuân thủ Grok `C5`, `C6`)
1. **Tích hợp ADR 0043 Dual-PDF có Fallback an toàn vào [`spoke_cli.py:ingest`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L770-L875) (`C5`):**
   - Thực thi sau khi [T-02: Khắc phục Lỗi Sinh index.md / metadata.yaml & Cổng Kiểm định Liên kết Gate 2](02_index_metadata_codegen_and_gate2_link_check.md) đã đảm bảo `convert_docx_to_okf_bundle` không ghi đè mất các khóa của `metadata.yaml` (đồng thời vá/cập nhật lại `metadata.yaml` sau bước convert giống [`ccba_legal/cli.py:913-944`](file:///home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/cli.py#L913-L944)).
   - Khi phát hiện PDF gốc là bản scan/ảnh (`pdf_tier == 3` từ crawler payload hoặc `PDFPreprocessor`) và có tệp `.docx`:
     - Di chuyển tạm PDF scan sang `sources/<slug>_raw_scan.pdf` và gọi Seam `ccba_ooxml.converter.convert_to_pdf(input_docx, target_pdf)`.
     - **Chỉ khi `convert_to_pdf` thành công và tạo ra tệp `target_pdf` hợp lệ (`size > 0`)**: mới tính lại `pdf_sha256`, ghi `pdf_origin: docx_vector_rendered` và `raw_scan_pdf: legal_docs/<cat>/<slug>/sources/<slug>_raw_scan.pdf` vào `metadata.yaml` và `legal_registry.yaml`.
     - **Nhánh Fallback an toàn (khi LibreOffice/Word lỗi hoặc không tạo được PDF — `ccba_legal/cli.py:870-879`)**: Khôi phục `_raw_scan.pdf` về lại `sources/<slug>.pdf`, xóa file tạm dở dang, giữ nguyên `pdf_sha256` của bản scan và **tuyệt đối không** đóng cờ `pdf_origin: docx_vector_rendered` (chống xanh giả trên CI).
2. **Chuyển tiếp `attachments` từ Crawler Payload & Khóa `.gitignore` (`C6`):**
   - Trong [`execute_ingest_legal`](file:///home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py#L600-L660) và [`spoke_cli.py:ingest`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L770-L815): Chuyển danh sách `attachments` do crawler (`tier_downloader.py`) tải về vào `sources/attachments/` của bundle.
   - Bổ sung `legal_docs/**/sources/attachments/*` (và `legal_docs/**/*.xlsx`, `legal_docs/**/*.xls`, `legal_docs/**/*.zip`, `legal_docs/**/*.rar`) vào [.gitignore](file:///home/vvc/ccba/ccba-legal-knowledge/.gitignore#L60-L66) theo đúng chuẩn ADR 0035 Tri-Tier Cloud Binary Vault để tuyệt đối không commit tệp nhị phân mới vào Git.
3. **Trích xuất Metadata trung thực khi chạy Offline (`--docx`) (`C5`):**
   - Trong [`execute_ingest_legal`](file:///home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py#L533-L542) và [`spoke_cli.py:ingest`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L905-L933): Đọc đoạn đầu của tệp `.docx` để bóc tách `document_number`, `issued_date`, `issued_by`, `title` nếu có; nếu không đọc được trường nào từ DOCX và không có trong `existing_entry` thì để trống (`""`), **cấm điền `datetime.now()` hay bịa cơ quan ban hành**.
4. **Đồng bộ câu lệnh mẫu Một Cửa:**
   - Cập nhật câu lệnh ingest trong [AGENTS.md](file:///home/vvc/ccba/ccba-legal-knowledge/AGENTS.md#L56) và [`sync_expansion_roadmap.py`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/sync_expansion_roadmap.py#L238).

---

## 🧪 Tiêu Chí Hoàn Thành (Acceptance Criteria)
- [x] Khi `convert_to_pdf` thành công trên văn bản `pdf_tier == 3`, `spoke_cli.py ingest` lưu `<slug>_raw_scan.pdf`, xuất Vector PDF, đóng cờ `pdf_origin: docx_vector_rendered` và bảo toàn đầy đủ các khóa này trong `metadata.yaml` sau khi `convert_docx_to_okf_bundle` kết thúc.
- [x] Khi `convert_to_pdf` thất bại (mock lỗi LibreOffice/Word), `spoke_cli.py ingest` tự động khôi phục bản PDF scan gốc, xóa file `_raw_scan.pdf` dở dang và **không** gắn cờ `pdf_origin: docx_vector_rendered` (đáp ứng yêu cầu kiểm chứng Fog-01 / `C5`).
- [x] `.gitignore` chặn hoàn toàn các tệp nhị phân trong `legal_docs/**/sources/attachments/*` và `.xlsx`/`.zip` trong `legal_docs/`.
- [x] Chế độ `--docx` offline không tự điền ngày `datetime.now()` hay cơ quan ban hành giả khi không trích xuất được từ DOCX.
- [x] `python scripts/validate_legal_spoke.py --skip-pdf-vault` và `verify_legal_ingest_harness.py` đạt 100% PASS.
