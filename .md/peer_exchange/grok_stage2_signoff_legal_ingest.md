---
request_id: req-20261105-stage2-signoff-legal-ingest-004
verdict: APPROVE
conditions:
- id: N5
  description: Khi hint không đọc được gì, ingest vẫn gán document_number từ slug
    viết hoa và title dạng 'Văn bản quy phạm pháp luật {số}'. Re-ingest đã giữ title
    cũ nếu title mới thuộc nhóm placeholder. Văn bản mới chưa có hint vẫn nhận hai
    giá trị suy từ slug.
  blocking: false
  source_profiles: []
- id: N6
  description: Gate 1 so registry_summary của .md/data/legal_registry.yaml với sổ
    gốc. Phần thân laws/decrees/standards không nằm trong phép so. ingest chỉ copy
    đè khi bản sao đã tồn tại.
  blocking: false
  source_profiles: []
risk_score: 2
summary: R1, R2, R3 và N4 đã có trong mã và trong test. effective_date/signer rỗng
  không còn bịa ngày hay Thủ tướng; hint ghi đè placeholder và đọc đủ 4 trường; status
  active mặc định giữ expired và superseded; Gate 1 khóa registry_summary của bản
  sao. Được đóng Stage 2.
telemetry:
  session_id: 04c35a3e-65ef-482d-893b-d44eabea9d6c
  primary_model: grok-4.7-build-fast
  input_tokens: 536889
  output_tokens: 3923
  reasoning_tokens: 2718
  cached_read_tokens: 354176
  total_tokens: 540812
  model_calls: 3
  turn_count: 1
  cost_usd: 0.3849
  cost_mode: exact
  duration_seconds: 51.05
  degraded_reasoning: false
---

# Stage 2 Sign-off — `/ccba-legal-ingest`

Phán quyết là **APPROVE**. Bốn điểm của phiên `cd54d0f9` đã nằm đúng chỗ.

## R1

`_build_merged_bundle_metadata` để `effective_date` và `signer` thành `""` khi cả `doc_meta` và metadata cũ đều trống. `_generate_vbpl_frontmatter` dùng cùng fallback rỗng, không còn `datetime.now()` hay `"Thủ tướng Chính phủ"`. `index.md` chỉ in dòng cơ quan, người ký và hiệu lực khi chuỗi khác rỗng. Test `unknown_issuer_bundle` truyền `effective_date: ""`, `signer: ""` và chặn `"Thủ tướng"`, `"Người ký"`, `"2021-03-03"`.

## R2

Handoff `--docx` ghi `document_number: ""` và `title: ""`. Trong `ingest`, hint ghi đè khi giá trị hiện tại rỗng hoặc thuộc `Document {slug}` / slug viết hoa. `_extract_docx_header_hints` đọc bảng đầu và 20 đoạn đầu, lấy `document_number`, `issued_date`, `issued_by`, `title`. Test DOCX mẫu `1812/QĐ-BXD` khẳng định cả bốn trường.

## R3

Khi `raw_meta.status` rỗng hoặc là `active` / `effective` / `current`, merge giữ `status` đang có. Test gọi `raw_meta={"status": "active"}` cho `10/2021/NĐ-CP` (`expired`) và `thong_tu_06_2021_tt_bxd` (`superseded`). Status khác default, ví dụ `expired` gửi tường minh, vẫn ghi đè được.

## N4

Sau khi ghi `legal_registry.yaml`, `ingest` copy sang `.md/data/legal_registry.yaml` nếu bản sao đã có. Gate 1 báo lỗi khi `registry_summary` của hai file khác nhau.

## Ghi chú không chặn

Khi hint thất bại, bản ghi mới vẫn nhận số hiệu suy từ slug và tiêu đề khung. Phép parity của bản sao chỉ khóa `registry_summary`, chưa khóa từng mục trong `laws` / `decrees` / `standards`.