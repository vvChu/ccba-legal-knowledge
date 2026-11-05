---
request_id: "req-20261105-stage2-code-review-legal-ingest-003"
verdict: REQUEST_CHANGES
risk_score: 3
conditions:
  - id: R1
    description: "Trong _build_merged_bundle_metadata (vbpl_admin.py khoảng 250-254), effective_date rỗng đang rơi xuống '2021-03-03' và signer rỗng xuống 'Thủ tướng Chính phủ' vì chuỗi `or` coi \"\" là thiếu. Để trống cả hai. Dòng index 'Người ký' chỉ in khi signer thật sự có giá trị. Test no-issuer hiện truyền signer nên không bắt được default này."
    blocking: true
  - id: R2
    description: "Handoff --docx offline (ccba_platform_cli.py:533-542) vẫn ghi title 'Document {slug}' và document_number từ slug. spoke_cli.py:1143 chỉ điền hint khi key chưa có, nên số hiệu và tiêu đề thật trong DOCX bị chặn. Bỏ hai placeholder đó, hoặc cho hint ghi đè đúng các placeholder. _extract_docx_header_hints hiện chỉ lấy document_number và issued_date, chưa lấy issued_by hay title."
    blocking: true
  - id: R3
    description: "_merge_existing_registry_entry chỉ giữ status cũ khi raw_meta không có status, hoặc khi existing là expired và raw là active/effective/current. Re-ingest với handoff status 'active' sẽ đổi thong_tu_06_2021_tt_bxd từ superseded thành active. Giữ mọi status hiện hữu khi status đầu vào là default active/effective. Test hiện gọi raw_meta={} nên không đi qua nhánh này."
    blocking: true
  - id: N4
    description: "Chưa có kiểm tra parity giữa legal_registry.yaml gốc và .md/data/legal_registry.yaml khi bản sao tồn tại. File bản sao đang nằm trong .gitignore."
    blocking: false
summary: "Luồng đếm 106, Gate 2 theo basename, Dual-PDF fallback, Sub-Gate 5.3 và nightly regex đã đúng và sổ hiện tại đang PASS. Ba lỗ trên đường ghi tiếp theo vẫn bịa ngày/người ký, chặn metadata trích từ DOCX, và có thể bật lại status superseded."
---

# Stage 2 Code Review — `/ccba-legal-ingest`

Phán quyết là **REQUEST_CHANGES**. Sổ đang chạy và 15 cổng PASS không bị lệch. Ba lỗ dưới đây nằm trên đường `ingest` / `convert` của văn bản kế tiếp.

## Đã khớp kế hoạch

- `registry_summary` là `total_documents: 106`, `01_vbpl: 53`, `02_qcvn: 17`, `03_tcvn: 33`, `04_appendices: 3`. `_recompute_registry_summary` đếm bằng `/{cat}/` trong `bundle_path`, không cộng `len(laws)+len(decrees)`.
- `get_spoke_stats` cộng `laws`, `decrees`, `standards`. `_find_existing_registry_entry` sửa đúng list đang chứa bản ghi.
- Sub-Gate 5.3 quét cả ba list. `verify_all_docs_against_pdf.py` cũng vậy.
- Gate 2 không gọi `Path.exists()` với `.pdf`/`.docx`. Href phải nằm dưới `sources/` và basename phải trùng `pdf_path`, `raw_scan_pdf` hoặc `source_file`. Luật Đấu thầu đã trỏ `./sources/luat_dau_thau_2023_22_2023_qh15.pdf`.
- `_write_bundle_metadata_and_index` merge `pdf_origin`, `raw_scan_pdf`, `source_assets`, `verification_scope`. Thiếu `issued_by` thì không in "Chính phủ". `./templates/` chỉ xuất khi `templates_cnt > 0`.
- Tier 3 chỉ đặt `is_vector_rendered` khi PDF render có `size > 0`. Lỗi LibreOffice thì xóa `_raw_scan.pdf`, trả scan về `<slug>.pdf`, không đóng cờ. Attachments copy vào `sources/attachments/`. `.gitignore` đã có attachments, `.xlsx`, `.xls`, `.zip`, `.rar`.
- `parse_master_ci_summary` đọc `Errors`/`Warnings` cả khi exit khác 0. Tầng 1 vẫn là Golden Cohort 11. Tiêu đề provenance dùng `len(records)`.
- `10/2021/NĐ-CP` được giữ `expired` khi `raw_meta` không có status, hoặc khi status tới là `active`/`effective`/`current`.

## R1 — Ngày và người ký bị bịa khi chuỗi rỗng

`_build_merged_bundle_metadata` dùng `doc_meta.get("effective_date") or existing... or "2021-03-03"` và `signer ... or "Thủ tướng Chính phủ"`. `spoke_cli.py` đưa `""` khi DOCX không có ngày. Chuỗi rỗng là falsy, nên metadata và dòng "Người ký" nhận ngày 03/03/2021 và Thủ tướng. Đó là dữ liệu quy phạm giả. Test no-issuer truyền sẵn `signer`, nên assertion "không có chữ Chính phủ" không chạm default này.

## R2 — Offline chặn số hiệu và tiêu đề thật

`execute_ingest_legal` với `--docx` vẫn ghi `title: Document {slug}` và `document_number` suy từ slug, đồng thời không gửi `issued_date`. Hint trong `spoke_cli.py` chỉ ghi khi key chưa có, nên `Số:` trong DOCX không thắng placeholder. Hàm hint cũng chưa đọc `issued_by` hay `title`.

## R3 — `superseded` bị đổi thành `active`

Nhánh giữ status chỉ đặc cách `expired`. `thong_tu_06_2021_tt_bxd` đang `status: superseded`. Handoff offline luôn gửi `status: active`, nên lần ingest lại sẽ ghi `active` vào registry. Test merge đang gọi `raw_meta={}`, nên nhánh default `active` không được thực thi.

## Ngoài phạm vi chặn

Chưa thấy bước so khớp `.md/data/legal_registry.yaml` với sổ gốc. Bản sao này đã bị `.gitignore`. Có thể làm sau; không chặn bản vá R1–R3.