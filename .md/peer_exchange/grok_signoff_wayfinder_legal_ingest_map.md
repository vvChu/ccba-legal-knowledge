---
request_id: req-20261105-signoff-wayfinder-legal-ingest-map-002
verdict: APPROVE_PLAN
conditions:
- id: N1
  description: Khi code Gate 2, href ./sources/{basename} khớp metadata.yaml:pdf_path
    nếu Path(pdf_path).name trùng basename và href nằm dưới ./sources/ (cùng quy tắc
    cho raw_scan_pdf và source_file). Chuỗi href không cần bằng nguyên văn legal_docs/.../sources/....
    Cấm Path.exists() trên .pdf/.docx.
  blocking: false
  source_profiles: []
- id: N2
  description: Lệnh nghiệm thu T-01 là python scripts/spoke_cli.py stats với doc_count
    == 106. Banner hiện có trong spoke_cli.py:131 là 'Total Legal Documents', không
    phải 'Total Registered Docs'.
  blocking: false
  source_profiles: []
- id: N3
  description: Quét mọi index.md đang có trên đĩa; số 105 làcensus kỳ vọng (53+17+33+2),
    không phải cận cứng của vòng lặp. Đóng cờ pdf_origin sau convert_to_pdf thành
    công (size > 0) vẫn chưa đo lệch trang LibreOffice; Gate 11 tiếp tục đối soát
    DOCX với Markdown.
  blocking: false
  source_profiles: []
risk_score: 2
summary: Map và T-01..T-04 đã khóa đủ C1–C8. Đồ thị phụ thuộc T-02 trước T-03 và T-01
  trước T-04 đúng. Kế hoạch được thực thi; ba ghi chú N1–N3 chỉ chốt cách so đường
  dẫn và chuỗi lệnh, không chặn.
telemetry:
  session_id: 2267034a-cd73-4564-b7cf-9fe2252de768
  primary_model: grok-4.7-build
  input_tokens: 363636
  output_tokens: 7330
  reasoning_tokens: 5633
  cached_read_tokens: 236544
  total_tokens: 370966
  model_calls: 3
  turn_count: 2
  cost_usd: 0.1416
  cost_mode: exact
  duration_seconds: 112.09
  degraded_reasoning: false
---

# Sign-off Stage 1 — Wayfinder `/ccba-legal-ingest`

Năm tệp đã được sửa đúng các điều kiện của phiên `bd8d9305`. Phán quyết là **APPROVE_PLAN**.

## Đối chiếu C1–C8

| Điều kiện | Chỗ đã khóa | Kết quả |
|---|---|---|
| C1 | `T-01` mục 1: khóa `registry_summary`, `51+19+36=106`, bốn phân khu theo `bundle_path` trên mọi lần `ingest`, cấm `01_vbpl = 70`, cập nhật đúng list đang chứa bản ghi | Đạt |
| C2 | `T-01` mục 2: không đụng `audit_provenance`; nghiệm thu bằng `spoke_cli.py stats` và `doc_count == 106` | Đạt |
| C3 | `T-01` mục 2–3: giữ `status`, `expiration_date`, `relations`, ngày ban hành/hiệu lực, `pdf_origin`, `raw_scan_pdf`; cấm sửa status 19 nghị định cho xanh cổng; bảo vệ `10/2021/NĐ-CP` | Đạt |
| C4 | `T-02`: merge metadata, `issued_by` để trống nếu thiếu, 11 file thông tư/Luật PCCC/QĐ 1812, 27 href theo basename kể cả Luật Đấu thầu, Gate 2 không `exists()` trên PDF/DOCX | Đạt |
| C5 | Map `D-03` và header `T-03`: blocked by `T-02`. Vá metadata sau convert như `cli.py:913-944`. Chỉ đóng `pdf_origin` khi `convert_to_pdf` ra file `size > 0`. Lỗi LibreOffice thì trả scan về `sources/<slug>.pdf` và không đóng cờ. Offline cấm `datetime.now()` và cơ quan bịa | Đạt |
| C6 | `T-03` mục 2: `attachments` từ payload `tier_downloader`. `.gitignore` thêm `legal_docs/**/sources/attachments/*` cùng `.xlsx`, `.xls`, `.zip`, `.rar` | Đạt |
| C7 | `T-04`: regex trên cả exit 0 và exit khác 0; Tầng 1 giữ Golden Cohort 11; Tầng 2 đọc `registry_summary` 106; `audit-provenance` không có `--attest-group-a`; tiêu đề dùng `len(records)` | Đạt |
| C8 | `T-01` ghi `sync_expansion_roadmap.py` đã đọc `registry_summary`. Fog cũ "0/33 index" đã bỏ. `T-02` quét cả 4 phân khu. `T-04` có parity cho `.md/data/legal_registry.yaml` | Đạt |

Đồ thị thực thi trong map là T-01 và T-02 ở frontier, T-03 chờ T-02, T-04 chờ T-01. Reuse-First giữ nguyên bốn seam cũ. Fog-02 để vault của `sources/attachments/` sang phiên sau là đúng phạm vi C6.

Cờ `--skip-pdf-vault` có thật tại `validate_legal_spoke.py:2044`, nên các acceptance dùng cờ này chạy được.

## Ghim khi code (không chặn)

- **N1.** `metadata.yaml:pdf_path` là đường dẫn repo (`legal_docs/.../sources/<file>.pdf`). Href sau sửa là `./sources/<file>.pdf`. So basename trong `sources/`, không so nguyên văn hai chuỗi.
- **N2.** Banner `stats` hiện là `Total Legal Documents` (`spoke_cli.py:131`). Mệnh đề cần xanh là `doc_count == 106`.
- **N3.** Vòng Gate 2 đi theo từng `index.md` có trên đĩa. Mốc 105 là census kỳ vọng. Nhánh thành công của `convert_to_pdf` chưa đo lệch trang LibreOffice; Gate 11 vẫn là đối soát DOCX với Markdown.