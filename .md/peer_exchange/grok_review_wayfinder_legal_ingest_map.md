---
request_id: req-20261105-review-wayfinder-legal-ingest-map-001
verdict: REVISE_PLAN
conditions:
- id: C1
  description: 'T-01 phải ghi đè đúng khóa registry_summary (không tạo khóa summary).
    total_documents = 106 bằng cách đếm laws+decrees+standards (51+19+36). Bốn categories
    phải đếm theo bundle_path: 01_vbpl 53, 02_qcvn 17, 03_tcvn 33, 04_appendices 3.
    Cấm gán 01_vbpl = len(laws)+len(decrees) (=70). Mỗi lần ingest tính lại cả bốn
    phân khu, không chỉ args.category. Tìm bản ghi trên cả ba list rồi sửa đúng list
    đang chứa nó; văn bản mới vẫn append theo quy ước hiện tại cho đến Fog-02.'
  blocking: true
  source_profiles: []
- id: C2
  description: T-01 không được chuyển audit_provenance sang quét registry. Hàm đã
    walk đĩa qua scan_all_bundles_provenance (01_vbpl..04_appendices); dòng 186 là
    bộ đếm KaTeX, tiêu đề cứng '38 Văn Bản' thuộc T-04 tại spoke_cli.py:297. Tiêu
    chí nghiệm thu đổi thành python scripts/spoke_cli.py stats (lệnh status --json
    và khóa total_documents hiện không tồn tại; get_spoke_stats trả doc_count).
  blocking: true
  source_profiles: []
- id: C3
  description: Trước khi đổi vòng Sub-Gate 5.3, chạy một lượt dry-run trên 19 decrees
    và chỉ sửa status khi quan hệ replaces/replaced_by đã có sẵn. Cấm viết status
    để làm gate xanh. Ingest update phải giữ status, relations, issued_date, effective_date,
    pdf_origin, raw_scan_pdf khi handoff chỉ có default. existing_entry.update(new_entry)
    hiện ghi đè status thành active; 10/2021/NĐ-CP đang expired, expiration_date 2026-07-01
    (đã qua ngày 2026-11-05) và nằm trên sàn STATUTORY_BASELINE_REPEALED.
  blocking: true
  source_profiles: []
- id: C4
  description: Gate liên kết index.md so khớp chuỗi POSIX với metadata.yaml:pdf_path
    cho mọi href .pdf/.docx. Cấm Path.exists() trên binary bị .gitignore (legal_docs/**/*.pdf,
    legal_docs/**/*.docx, sources/*). exists() chỉ áp dụng cho .md/.json/.yaml và
    thư mục tables|templates|figures|annexes|sources. Sửa href theo basename của pdf_path,
    không chỉ thêm tiền tố ./sources/ vào slug. Luật Đấu thầu đang trỏ ./luat_22_2023_qh15.pdf
    trong khi metadata là sources/luat_dau_thau_2023_22_2023_qh15.pdf. Giữ 'Chính
    phủ' cho nghị định; 11 file sai là thông tư, luật PCCC và QĐ 1812.
  blocking: true
  source_profiles: []
- id: C5
  description: 'T-03 phụ thuộc T-02 hoặc phải vá metadata.yaml sau convert_docx_to_okf_bundle,
    giống ccba_legal/cli.py:913-944. _write_bundle_metadata_and_index đang ghi đè
    trắng metadata và sẽ làm rơi pdf_origin, raw_scan_pdf, source_assets, issued_by,
    verification_scope. Merge giữ các khóa đó. Thiếu issued_by thì để trống, không
    điền ''Cơ quan có thẩm quyền'' hay ''Chính phủ''. Chỉ ghi pdf_origin: docx_vector_rendered
    sau khi convert_to_pdf thành công; lỗi LibreOffice thì giữ scan và không đóng
    cờ, đúng nhánh fallback cli.py:870-879. Đưa Fog-01 vào acceptance của T-03.'
  blocking: true
  source_profiles: []
- id: C6
  description: Attachments không nằm trong handle_ingest. Nguồn thật là payload crawler
    (tier_downloader trả attachments). Copy vào sources/attachments phải đi cùng .gitignore
    và vault ADR 0035; .xlsx trong legal_docs/sources hiện không bị ignore (chỉ .md/**/*.xlsx).
    Không commit binary mới.
  blocking: true
  source_profiles: []
- id: C7
  description: 'T-04 parse SUMMARY REPORT: Errors: (\d+) | Warnings: (\d+) trên cả
    exit 0 và exit khác 0 (validate_legal_spoke.py:2019; out_ci đã gộp stdout+stderr).
    Giữ Stage 1 golden cohort (mặc định 11 bundles). Con số 106 chỉ là Stage 2 / registry_summary
    sau T-01. Lệnh audit-provenance không được kèm --attest-group-a.'
  blocking: true
  source_profiles: []
- id: C8
  description: 'Sửa Fog-03: 02_qcvn và 03_tcvn đã có nhiều index.md (không phải 2/17
    và 0/33). sync_expansion_roadmap.py:153 đã đọc registry_summary.total_documents;
    sau C1 không cộng thêm một bộ đếm list thứ hai. Bản sao .md/data/legal_registry.yaml
    cần một kiểm tra parity với file gốc nếu vẫn được giữ.'
  blocking: false
  source_profiles: []
risk_score: 4
summary: Wayfinder đủ năm phần và tách việc đúng hướng Reuse-First, nhưng chưa được
  thực thi nguyên văn. Khóa registry, lệnh nghiệm thu, trục đếm category/section,
  thứ tự T-02 trước T-03, và kiểm tra link PDF trên CI đều lệch mã hiện tại; chạy
  theo ticket sẽ làm đỏ Master CI hoặc ghi đè hiệu lực văn bản.
telemetry:
  session_id: bd8d9305-de15-4491-b8ce-5fbf59f16b4d
  primary_model: grok-4.7-build
  input_tokens: 714262
  output_tokens: 29784
  reasoning_tokens: 23792
  cached_read_tokens: 609920
  total_tokens: 744046
  model_calls: 12
  turn_count: 1
  cost_usd: 0.2354
  cost_mode: exact
  duration_seconds: 443.41
  degraded_reasoning: false
---

# Thẩm định Stage 1 — Wayfinder `/ccba-legal-ingest` (106 bundles)

Khung map đạt chuẩn Wayfinder: Destination, Decisions (D-01..D-03), Frontier (T-01..T-04), Not yet specified (Fog-01..03), Out of scope. D-01 cấy vào seam có sẵn (`spoke_cli.py`, `validate_legal_spoke.py`, `vbpl_admin.py`, `ccba_platform_cli.py`) đúng Reuse-First. Phần lệch là dữ kiện thực thi và quan hệ phụ thuộc, không phải hướng đích.

Số liệu gốc đã khớp đĩa và sổ, trên **hai trục khác nhau**:

| Trục | Số đúng | Nguồn |
|---|---|---|
| Khóa YAML | `laws` 51, `decrees` 19, `standards` 36, tổng 106 | 106 mục `- id:` trong `legal_registry.yaml` |
| Thư mục | `01_vbpl` 53, `02_qcvn` 17, `03_tcvn` 33, `04_appendices` 3 | `legal_docs/` |
| `registry_summary` hiện tại | `total_documents: 87`, `01_vbpl: 34` | Dòng 4–10, thiếu 19 nghị định |

`registry_summary` mới là khóa đang được `run_nightly_telemetry.py:38` và `sync_expansion_roadmap.py:152-154` đọc. Khóa `summary:` trong T-01 không có người tiêu thụ.

## Cấu trúc và KISS

T-01, T-02, T-04 mỗi ticket một quyết định. T-03 gộp Dual-PDF, attachments, parser offline và sửa tài liệu; vẫn một điểm vào ingest, với điều kiện C5–C6 tách phần chưa có trong `cli.py`.

D-03 nói bốn ticket thực thi độc lập. Quan hệ đúng là: T-04 chờ T-01 cho con số 106; T-03 chờ T-02 (hoặc tự vá metadata sau convert). `audit_provenance` không thuộc T-01.

Các bug dẫn được xác nhận:

- `get_spoke_stats` chỉ cộng `laws` + `standards` (`spoke_cli.py:91-96`).
- `ingest` gán mọi `01_vbpl` vào `laws` và cộng summary không có `decrees` (`:881-882`, `:1011-1019`).
- Sub-Gate 5.3 lặp `["laws", "standards"]` (`validate_legal_spoke.py:615`). Các vòng ở `:224` và `:848` đã gồm `decrees`.
- `_write_bundle_metadata_and_index` ghi đè metadata, cứng "Chính phủ", href `./{pdf name}`, luôn in `./templates/` (`vbpl_admin.py:226-267`).
- Dual-PDF `pdf_tier == 3` nằm ở `ccba_legal/cli.py:857-944` và chưa có trong `spoke_cli.py:ingest`.
- Offline handoff cứng `title: Document {slug}`, `status: effective` (`ccba_platform_cli.py:533-541`).
- Nightly gán `✅ PASSED (0 Errors, 0 Warnings)` khi exit 0 (`run_nightly_telemetry.py:157`).
- Tiêu đề provenance cứng ở `spoke_cli.py:297`.

Đếm tay khớp ticket: 11 `index.md` ở `01_vbpl` ghi "Chính phủ" cho thông tư, Luật PCCC và QĐ 1812 (nghị định ghi Chính phủ là đúng). 27 href PDF nằm ngoài `sources/` (25 ở `01_vbpl`, 2 ở `02_qcvn`).

## Hồi quy khi mở Sub-Gate 5.3 (T-01)

Mở vòng lặp là an toàn nếu **không sửa status**. Cả 19 mục `decrees:` đang `status: active`. Sàn `STATUTORY_BASELINE_REPEALED` không chứa số hiệu của 19 mục đó. `214/2025/NĐ-CP` thay thế `24/2024/NĐ-CP`, và 24/2024 đã `expired` trong `laws`. Split-brain 5.3 (`:769-783`) gom `active`, `effective`, `current` về cùng một nhãn; lệch `effective`/`active` không tự thành error.

Điểm gãy là bước "chuẩn hóa status" cộng với `existing_entry.update(new_entry)`. Re-ingest thiếu `status` trong handoff sẽ ghi `active`. Với `10/2021/NĐ-CP` (expired, `expiration_date: 2026-07-01`, `replaced_by` nghị định 206), lần chạy 5.3 kế tiếp thành hard error vì sàn luật định và vì ngày hết hạn đã qua 2026-11-05.

`len(laws)+len(decrees)` không phải số bundle `01_vbpl`. Laws đang chứa QCVN và 3 phụ lục. Gán category theo độ dài section sẽ phá `registry_summary` mà nightly và roadmap đang đọc.

## Hồi quy link `index.md` trên CI (T-02)

`.gitignore` bỏ `legal_docs/**/sources/*.pdf`, `legal_docs/**/*.pdf` và mọi `.docx` tương ứng. Gate 1 đã chỉ **warning** khi binary vắng (`validate_legal_spoke.py:185-198`). `verify_cross_links.py:49-55` thì `exists()` và còn chấp nhận href gốc nếu basename tình cờ có trong `sources/`. Trên CI cả hai đường đều vắng, nên mọi href PDF — kể cả `./sources/<file>.pdf` đã đúng — thành link gãy.

Gate mới phải so chuỗi với `metadata.yaml:pdf_path`. `exists()` dành cho markdown, JSON, YAML và thư mục ngăn kéo. Hai alias không hết bằng cách thêm `./sources/` trước slug: Luật PCCC khớp basename `luat_55_2024_qh15.pdf`; Luật Đấu thầu thì href `./luat_22_2023_qh15.pdf` khác `sources/luat_dau_thau_2023_22_2023_qh15.pdf`.

## Hồi quy `convert_to_pdf` (T-03)

`convert_to_pdf` (`ccba_ooxml/converter.py:121-176`) trên Linux đi LibreOffice headless. Gate 11 đối soát DOCX↔Markdown, không đo số trang PDF. `pdf_origin: docx_vector_rendered` vẫn bị Dual-PDF Gate đọc (`validate_legal_spoke.py:546-558`), và trên CI gate đó **bỏ qua** PDF mất file. Đóng cờ khi convert lỗi sẽ xanh giả.

`handle_ingest` đã có fallback: xóa raw scan dở, giữ PDF scan, không ghi `pdf_origin`. Acceptance T-03 ("luôn đóng cờ và qua Gate 11 ngay lần đầu") đang ngược Fog-01 và ngược fallback đó. Fog-01 phải thành điều kiện nghiệm thu của T-03.

Attachments được crawler trả về (`tier_downloader.py`) và không được `cli.py:858-945` ghi vào bundle. `.xlsx` trong `legal_docs/**/sources/` không nằm trong `.gitignore` (chỉ `.md/**/*.xlsx`). Copy attachments vào `sources/attachments/` sẽ commit binary nếu chưa khóa vault.

Parser offline không được điền ngày `utcnow` hay cơ quan ban hành khi không đọc được từ DOCX. `spoke_cli.py:928-930` đang làm đúng việc đó.

## T-04 và sương mù

Regex `SUMMARY REPORT: Errors: (\d+) | Warnings: (\d+)` khớp `validate_legal_spoke.py:2019`. Áp dụng cho cả lần CI fail. Stage 1 mặc định là 5 golden cohorts, không phải 106 bundle. Ép hai tầng cùng số 106 sẽ đổi nghĩa parity.

`audit-provenance` không kèm `--attest-group-a` (flag này ghi tem Gate 15). Tiêu đề 38 là chuỗi cứng; thân bảng đã lấy `len(records)` từ walk đĩa.

Fog-03 sai sự thật: `02_qcvn` và `03_tcvn` đã có hàng chục `index.md`. Gate link phải quét mọi `index.md` hiện có, không chỉ `01_vbpl`.

## Kết luận

Sửa map và bốn ticket theo C1–C7 rồi mới thực thi. Destination 106 bundle, Reuse-First và việc để Fog-02 (hợp nhất `decrees`/`laws`) ngoài phạm vi vẫn đúng.