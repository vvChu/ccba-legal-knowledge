# Ticket 02: Khắc phục Lỗi Sinh `index.md` / `metadata.yaml` & Cổng Kiểm định Liên kết Gate 2

- **Type:** Task (AFK / Code Implementation)
- **Priority:** P1 (Cao)
- **Status:** closed (completed — 11 issuers, 27 PDF links, 8 empty dir links fixed & Gate 2 active)
- **Assignee:** Antigravity AI
- **Target Seams & Files:**
  - [vbpl_admin.py](file:///home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py#L226-L270) (`_write_bundle_metadata_and_index`)
  - [validate_legal_spoke.py](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py#L312-L320) (Gate 2 — OKF Bundle Integrity)
  - 105 tệp `index.md` hiện hữu trên toàn bộ 4 phân khu (`01_vbpl` 53, `02_qcvn` 17, `03_tcvn` 33, `04_appendices` 2)
- **Reference:** [Wayfinder Map: Gia Cố Toàn Trình Pipeline `/ccba-legal-ingest`](../map.md), ADR 0035, ADR 0036, Grok Audit `C4`, `C5`, `C8`

---

## ❓ Câu Hỏi / Vấn Đề Cốt Lõi Cần Giải Quyết
Làm thế nào để sửa hàm [`_write_bundle_metadata_and_index`](file:///home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py#L226-L270) merge bảo toàn các khóa mở rộng của `metadata.yaml` (`pdf_origin`, `raw_scan_pdf`, `source_assets`, `issued_by`, `verification_scope`), lấy đúng `issued_by` (để trống nếu thiếu, không gán cứng `"Chính phủ"` hay `"Cơ quan có thẩm quyền"`), trỏ đúng `./sources/{Path(pdf_path).name}` và ẩn `./templates/` khi `templates_cnt == 0`; đồng thời sửa **11** file `index.md` sai cơ quan ban hành, **27** file `index.md` đứt link và khóa kiểm tra tại Gate 2 trên mọi file `index.md` một cách an toàn với `.gitignore` trên CI?

---

## 🎯 Mục Tiêu Thực Thi (KISS Implementation Scope — Tuân thủ Grok `C4`, `C5`, `C8`)
1. **Merge bảo toàn `metadata.yaml` và sửa sinh `index.md` trong [`vbpl_admin.py`](file:///home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py#L226-L270) (`C4`, `C5`):**
   - Khi ghi `metadata.yaml`, đọc tệp `metadata.yaml` hiện có (nếu tồn tại) và merge bảo toàn tuyệt đối các khóa `pdf_origin`, `raw_scan_pdf`, `source_assets`, `issued_by`, `issued_date`, `effective_date`, `status`, `relations`, `verification_scope`, `okf_version`.
   - Tại dòng `#L253` của `index.md`: Lấy `issued_by` từ `doc_meta.get("issued_by") or existing_meta.get("issued_by") or ""`. Nếu thiếu `issued_by`, để trống (chỉ hiển thị người ký hoặc ẩn cụm cơ quan ban hành), **tuyệt đối không** tự điền `"Chính phủ"` hay `"Cơ quan có thẩm quyền"`.
   - Tại dòng `#L255` của `index.md`: Trỏ liên kết PDF theo đúng basename của `pdf_path` trong `metadata.yaml`: `[{pdf_name}](./sources/{pdf_name})`.
   - Tại dòng `#L265` của `index.md`: Chỉ xuất dòng `- [Kho Biểu Mẫu Chuẩn Hóa (Templates Directory)](./templates/)` khi `templates_cnt > 0`.
2. **Chuẩn hóa dữ liệu `index.md` hiện hữu trên Spoke (`C4`):**
   - Giữ nguyên `"Chính phủ"` cho các Nghị định; sửa đúng **11** tệp `index.md` bị ghi nhầm `"Chính phủ"` (gồm các Thông tư, Luật PCCC 55/2024/QH15, và Quyết định 1812/QĐ-BXD) theo đúng trường `issued_by` trong `metadata.yaml` của từng bundle.
   - Sửa **27** tệp `index.md` (25 ở `01_vbpl`, 2 ở `02_qcvn`) có href `.pdf` nằm ngoài `./sources/` bằng cách lấy chính xác basename từ `metadata.yaml:pdf_path` (`./sources/{Path(meta["pdf_path"]).name}` — xử lý đúng cả trường hợp Luật Đấu thầu đang trỏ `./luat_22_2023_qh15.pdf` trong khi `metadata.yaml:pdf_path` là `sources/luat_dau_thau_2023_22_2023_qh15.pdf`).
   - Xóa dòng liên kết `./templates/` trong các tệp `index.md` của những bundle không có thư mục `templates/` (0 biểu mẫu).
3. **Bổ sung Cổng kiểm định liên kết `index.md` an toàn CI vào Gate 2 ([`validate_legal_spoke.py`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py#L312-L320)) (`C4`, `C8`, `N1`, `N3`):**
   - Quét động mọi tệp `index.md` hiện có trên đĩa qua cả 4 phân khu (`01_vbpl`, `02_qcvn`, `03_tcvn`, `04_appendices` — kỳ vọng 105 tệp theo `N3`, không hardcode cận cứng).
   - **Quy tắc kiểm tra an toàn CI (`.gitignore` — `N1`):**
     - Với mọi liên kết `.pdf` / `.docx` trong `index.md`: **Cấm gọi `Path.exists()`** (do tệp nhị phân bị `.gitignore` trên CI theo ADR 0035). Thay vào đó, kiểm tra href bắt đầu bằng `./sources/` (hoặc `sources/`) và `Path(href).name == Path(meta_field).name` với `meta_field` thuộc `pdf_path`, `raw_scan_pdf`, hoặc `source_file` trong `metadata.yaml` (không so nguyên văn chuỗi `legal_docs/.../sources/...` với `./sources/...`).
     - Với các liên kết tài nguyên văn bản và ngăn kéo (`.md`, `.json`, `.yaml` và các thư mục `tables`, `templates`, `figures`, `annexes`, `sources`): Kiểm tra `Path.exists()` bắt buộc tồn tại trên đĩa.

---

## 🧪 Tiêu Chí Hoàn Thành (Acceptance Criteria)
- [x] `0/105` tệp `index.md` trên toàn Spoke còn chứa liên kết `.pdf` lệch với `metadata.yaml:pdf_path` hoặc trỏ tới `./templates/` không tồn tại.
- [x] `0/53` tệp `index.md` trong `01_vbpl` bị ghi sai cơ quan ban hành so với `metadata.yaml:issued_by`.
- [x] Gate 2 trong `python scripts/validate_legal_spoke.py --skip-pdf-vault` kiểm tra toàn bộ 105 tệp `index.md`, vượt qua 100% trên môi trường CI không có tệp `.pdf` vật lý, và bắt lỗi ngay lập tức nếu href `.pdf` lệch `metadata.yaml:pdf_path` hoặc href `.md`/thư mục ngăn kéo không tồn tại.
- [x] Unit test cho `_write_bundle_metadata_and_index` (kiểm chứng bảo toàn `pdf_origin`, `raw_scan_pdf`, `source_assets`, `verification_scope` và không điền bừa `"Chính phủ"`) đạt 100% PASS.
