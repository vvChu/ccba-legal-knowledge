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
- [ ] Chạy `python scripts/validate_legal_spoke.py` đạt 0 ERRORS.
- [ ] Chạy bộ kiểm thử tự động `python -m pytest tests/` đạt 100% PASSED.
</USER_REQUEST>
