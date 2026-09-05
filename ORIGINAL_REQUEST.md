# Original User Request

## 2026-08-04T10:13:00Z

<USER_REQUEST>
Nghiên cứu, phân tích toàn diện và làm rõ kiến trúc tổng thể của dự án `ccba-legal-knowledge` (Tri thức Pháp luật & Quy chuẩn Kỹ thuật Xây dựng).

Working directory: d:/GitHubProjects/ccba-legal-knowledge
Integrity mode: development

## Requirements

### R1. Phân tích Cấu trúc Thư mục & Mô hình Dữ liệu Tri thức (OKF v2.0)
Khảo sát và lập sơ đồ tổ chức thư mục `legal_docs/`, cơ chế quản lý metadata trong `legal_registry.yaml`, các gói tri thức (OKF Markdown Bundles) và luồng đồng bộ với Google NotebookLM/Cloud Storage.

### R2. Phân tích Mã nguồn Helper Scripts & Test Suite
Phân tích chi tiết các utility scripts trong `scripts/` và bộ kiểm thử tự động trong `tests/` (bao gồm `safe_pytest.py`, `validate_docs.py`, `update_legal_registry.py`...) để xác định luồng dữ liệu end-to-end.

### R3. Phân tích Rào chắn Quản trị (Governance & Platform Integration)
Khảo sát quy định vận hành Spoke tại `AGENTS.md`, `workspace_context.yaml`, các quy trình Workflows (`.agents/workflows/`), Skills (`.agents/skills/`), rào cản Reuse-First Gate với Hub (`ccba-agent-platform`) và kết nối AI Gateway (`ccba-ai`).

## Acceptance Criteria

### Báo cáo Kế hoạch & Sơ đồ Kiến trúc
- [ ] Tạo báo cáo tổng quan kiến trúc chi tiết (xuất ra file markdown tại `.md/codebase_architecture_analysis.md`) có sơ đồ Mermaid visualize luồng dữ liệu tri thức và quản trị.
- [ ] Liệt kê đầy đủ danh mục thành phần: Modules, Scripts, Workflows, Skills, RAG Metadata Registries.
- [ ] Phân tích đánh giá sự tuân thủ các quy chuẩn Governance: OKF v2.0 Native-First, Reuse-First Gate với Hub, và 8 rào chắn trong Global Memory & Layer 1 Constitution.
</USER_REQUEST>

## Follow-up — 2026-08-10T02:48:04Z

<USER_REQUEST>
Nghiên cứu, thu thập toàn văn Luật Xây dựng số 135/2025/QH15 (thay thế Luật Xây dựng 2014) từ nguồn chính thống, bóc tách thành Markdown, đóng gói OKF v0.2 Bundle tiêu chuẩn, khởi tạo Bảng so sánh điểm mới, và cập nhật sổ bạ legal_registry.yaml — tất cả tuân thủ kiến trúc OKF Native-First của Spoke `ccba-legal-knowledge`.

Working directory: d:/GitHubProjects/ccba-legal-knowledge
Integrity mode: development

## Reference Material & Existing Tools

Dự án Spoke này đã có sẵn các công cụ và mẫu tham khảo sau. Agent Team phải ưu tiên sử dụng thay vì viết mới (Reuse-First Gate):

- **Download scripts**: `scripts/download_tvpl_docx.py`, `scripts/direct_download.py` — cào file `.docx` từ Thư viện Pháp luật.
- **Conversion**: `scripts/docx_converter.py` — chuyển `.docx` thành Markdown.
- **OKF Processing Engine**: `scripts/gold_standard_processor.py` — đóng gói OKF Bundle v0.2 (CLI: `python scripts/gold_standard_processor.py <bundle_dir> --type vbpl`).
- **Validation**: `scripts/validate_legal_spoke.py` — kiểm định toàn bộ Spoke.
- **OKF Bundle mẫu**: `legal_docs/01_vbpl/luat_phong_chay_chua_chay_va_cuu_nan_cuu_ho_2024_55_2024_qh1/` — Tham khảo cấu trúc: `<slug>.md` (nội dung chính), `index.md` (MOC), `clauses.json`, `qa_benchmark.json`, `tables/`.
- **Appendix mẫu**: `legal_docs/04_appendices/bang_so_sanh_sua_doi_2026/` — Bảng so sánh cần có 4 cột: `Hạng Mục Quy Định`, `Quy định cũ`, `Quy định mới`, `Tác Động Kỹ Thuật`.
- **Raw evidence store**: Lưu file gốc trước xử lý vào `.md/extracted_docs/luat_xay_dung_2025_135_2025_qh15/`.
- **URL nguồn chính thống**: `https://thuvienphapluat.vn` hoặc `https://chinhphu.vn`.

## Requirements

### R1. Thu thập & Bóc tách Văn bản Luật Xây dựng 135/2025/QH15
Thu thập toàn văn Luật Xây dựng số 135/2025/QH15 (Quốc hội thông qua 10/12/2025, hiệu lực từ 01/07/2026) từ nguồn chính thống. Lưu giữ tệp gốc tại `.md/extracted_docs/luat_xay_dung_2025_135_2025_qh15/`, sau đó bóc tách thành Markdown sạch phục vụ bước đóng gói OKF.

### R2. Đóng gói OKF Bundle v0.2 Native-First
Đóng gói thành gói tri thức hoàn chỉnh tại `legal_docs/01_vbpl/luat_xay_dung_2025_135_2025_qh15/` tuân thủ cấu trúc OKF v0.2: tệp nội dung Markdown chính (`<slug>.md`), bản đồ nội dung (`index.md`), mỏ neo ngữ nghĩa (`<a id="dieu-X"></a>`), cây chỉ mục AST (`clauses.json`), bộ benchmark QA (`qa_benchmark.json`), và thư mục bảng dữ liệu (`tables/`) nếu có.

### R3. Khởi tạo Bảng So sánh Điểm mới (Comparative Appendix)
Tạo gói Phụ lục tại `legal_docs/04_appendices/bang_so_sanh_luat_xay_dung_2025_vs_2014/` so sánh các thay đổi đột phá giữa Luật 135/2025 và Luật Xây dựng 2014 (chuyển từ tiền kiểm sang hậu kiểm, tích hợp PCCC, miễn GPXD...). Bảng phải có tối thiểu 4 cột (`Hạng Mục`, `Luật XD 2014`, `Luật XD 2025`, `Tác Động`) và tối thiểu 8 hàng nội dung thực chất.

### R4. Cập nhật Metadata Graph (`legal_registry.yaml`) & Validation
Đăng ký entry mới cho Luật 135/2025/QH15 vào mảng `laws:` của `legal_registry.yaml` với đầy đủ các trường metadata (id, document_number, type, issued_by, issued_date, effective_date, status, title, bundle_path, source_url). Đồng thời cập nhật `registry_summary.total_documents` và `categories.01_vbpl` cho nhất quán.

## Acceptance Criteria

### Tính toàn vẹn Tri thức
- [ ] Tệp Markdown nội dung chính `luat_xay_dung_2025_135_2025_qh15.md` tồn tại trong bundle và có dung lượng > 10KB.
- [ ] `clauses.json` chứa ít nhất 30 clause entries (Luật Xây dựng có > 100 Điều).
- [ ] `qa_benchmark.json` chứa ít nhất 10 Q&A pairs.
- [ ] `index.md` tồn tại và liên kết đúng tới file nội dung chính.

### Bảng So sánh
- [ ] File bảng so sánh trong `04_appendices/bang_so_sanh_luat_xay_dung_2025_vs_2014/` chứa bảng Markdown pipe table có ít nhất 4 cột và 8 hàng nội dung.

### Registry & Validation
- [ ] `legal_registry.yaml` chứa entry mới với `document_number: "135/2025/QH15"` và `status: active`.
- [ ] `registry_summary.total_documents` và `categories.01_vbpl` đã được tăng đúng.

## 2026-09-02T08:06:20Z

Kiểm toán ngữ nghĩa sâu (Semantic Quality Audit) dữ liệu tri thức pháp lý trong 37 OKF bundles tại `ccba-legal-knowledge`. Mục tiêu: phát hiện các lỗi ngữ nghĩa, thiếu sót metadata, và bất nhất cấu trúc mà hệ thống CI tự động 11-Gate hiện tại **không bao phủ**. Đây là kiểm toán read-only — KHÔNG được sửa bất kỳ file nào trong repo.

Working directory: d:\GitHubProjects\ccba-legal-knowledge
Integrity mode: development

## Context

Kho tri thức gồm 37 legal document bundles (24 VBPL, 5 QCVN, 5 TCVN, 3 Phụ lục so sánh) đóng gói theo tiêu chuẩn OKF v2.4. Hệ thống CI tự động (`scripts/validate_legal_spoke.py`, 11 gates) đã pass 0 Errors / 0 Warnings — nhưng CI chỉ kiểm tra cấu trúc, không kiểm tra tính chính xác ngữ nghĩa của dữ liệu bên trong.

Key files:
- `legal_registry.yaml` — Registry tổng của 37 tài liệu
- `legal_docs/{01_vbpl,02_qcvn,03_tcvn,04_appendices}/*/clauses.json` — Cây điều khoản AST
- `legal_docs/*/tables/{csv/,json/,tables_catalog.json}` — Bảng số liệu tra cứu 2D
- `legal_docs/*/templates/*.md` — Biểu mẫu hành chính
- `legal_docs/*/figures/{cards/,images/,figures_catalog.yaml}` — Thẻ hình vẽ kỹ thuật
- `legal_docs/*/metadata.yaml` — Siêu dữ liệu từng bundle

## Requirements

### R1. Clauses.json Schema Consistency Audit
Hiện tại tồn tại **4 biến thể schema khác nhau** trong `clauses.json` trên 34 bundles. Kiểm toán phải xác định chính xác:
- Bundles nào thiếu trường `jurisdiction` (đã biết: `luat_xay_dung_2025`, `nghi_dinh_105_2025`)
- Bundles nào thiếu trường `cong_bao_number` (đã biết: 9 bundles gồm toàn bộ TCVN và 2 VBPL)
- Bundles nào thiếu trường `line_start`/`line_end` (đã biết: `qcvn_03_2022_bxd`)
- Chỉ 1 bundle (`qcvn_03_2022_bxd`) có trường `compliance_severity` — đánh giá liệu trường này nên có ở tất cả QCVN hay thiết kế hiện tại là có chủ đích
- Lập bảng ma trận schema cho toàn bộ 34 bundles (3 bundles `04_appendices` không có `clauses.json`)

### R2. Anchor-to-Heading Resolution Verification
Mỗi entry trong `clauses.json` có trường `anchor` dùng để deep-link đến heading tương ứng trong file Markdown. Kiểm tra end-to-end:
- Đọc từng `clauses.json`, với mỗi entry lấy `anchor` + `source_file`
- Mở file Markdown tương ứng, tìm heading có slug khớp với anchor
- Báo cáo tỷ lệ resolved/unresolved cho từng bundle
- Liệt kê cụ thể 10 anchor đầu tiên bị unresolved (nếu có) kèm heading gần nhất

### R3. CSV Table Data Fidelity Spot-Check
Trong 10 bundles có bảng 2D (tổng cộng ~245 CSV files), chọn ngẫu nhiên **ít nhất 3 bảng CSV/JSON từ mỗi bundle có tables/** và đối chiếu:
- Số hàng và số cột trong CSV có khớp với bảng Markdown tương ứng trong thân văn bản
- Giá trị số liệu ở 3 ô bất kỳ trong CSV có khớp giá trị trong bảng Markdown
- `tables_catalog.json` có liệt kê đúng và đủ tất cả CSV files không

### R4. Metadata Cross-Validation
Đối chiếu chéo giữa `metadata.yaml` từng bundle với `legal_registry.yaml` (root):
- `document_number`, `issued_date`, `effective_date`, `status` phải khớp
- `pdf_sha256` trong `metadata.yaml` phải khớp `pdf_sha256` trong `legal_registry.yaml`
- `bundle_path` phải trỏ đến thư mục bundle thực tế tồn tại
- Liệt kê mọi bất nhất phát hiện được

### R5. Consolidated Semantic Audit Report
Tổng hợp toàn bộ kết quả R1–R4 thành **một báo cáo kiểm toán duy nhất**, lưu tại `.md/reports/semantic_quality_audit.md`, bao gồm:
- Bảng Ma trận Schema cho 34 bundles (có/không từng trường)
- Bảng Tỷ lệ Anchor Resolution cho từng bundle
- Kết quả spot-check CSV Data Fidelity (pass/fail + chi tiết sai lệch)
- Kết quả cross-validation Metadata (pass/fail + chi tiết bất nhất)
- Executive Summary: tổng số phát hiện, phân loại theo mức nghiêm trọng (Critical / Warning / Info)

## Acceptance Criteria

### Audit Coverage
- [ ] Báo cáo bao phủ đủ 34 bundles có `clauses.json` (R1, R2) và 10 bundles có `tables/` (R3)
- [ ] Mỗi phát hiện (finding) phải kèm bundle name, file path, và dẫn chứng cụ thể (trích dẫn giá trị thực tế vs giá trị kỳ vọng)

### Anchor Resolution
- [ ] Kiểm tra anchor resolution cho tối thiểu 100 entries `clauses.json` phân bổ trên ít nhất 10 bundles khác nhau
- [ ] Báo cáo tỷ lệ resolution dạng `X/Y resolved (Z%)` cho từng bundle được kiểm tra

### CSV Spot-Check
- [ ] Ít nhất 30 bảng CSV được đối chiếu (3 bảng × 10 bundles có tables/)
- [ ] Mỗi bảng spot-check phải ghi nhận: tên file CSV, số hàng/cột, 3 giá trị đối chiếu, kết quả pass/fail

### Deliverable
- [ ] File `.md/reports/semantic_quality_audit.md` tồn tại, có cấu trúc rõ ràng với các section tương ứng R1–R4, và Executive Summary ở đầu
