# ADR 0025: Strict Zero-Tolerance Provenance Enactment Gate for Legal Ingestion

- **Trạng thái:** ACCEPTED
- **Ngày quyết định:** 2026-08-22
- **Người đề xuất:** CCBA Legal Intelligence Team
- **Phạm vi:** CI Verification Pipeline (`validate_legal_spoke.py`), Acquisition Gate (`AGENTS.md`)

---

## 1. Bối cảnh & Vấn đề (Context & Problem Statement)

Trong các chu kỳ phát triển trước, hệ thống từng ghi nhận các sai phạm nghiêm trọng do Agent bỏ qua bước thu thập tệp nhị phân gốc, tự ý cào HTML trên web hoặc tạo tệp Markdown giả lập không thể truy nguyên nguồn gốc (Synthetic/Unverified Markdown). Hậu quả dẫn đến:
- Lọt hàng ngàn dòng mã JavaScript, quảng cáo website và form thu thập dữ liệu vào thân văn bản quy phạm.
- Làm đứt gãy câu từ, mất bảng biểu kỹ thuật và không thể đối soát mã băm với Công báo Quốc gia.

Để bảo đảm vị thế của Spoke `ccba-legal-knowledge` là **Cơ sở Tri thức Pháp lý Chuẩn mực Tối cao của Nền tảng CCBA**, cần có một cơ chế kỹ thuật cưỡng chế không khoan nhượng (Zero-Tolerance Enforcement) tại cổng nạp dữ liệu.

---

## 2. Quyết định Thiết kế (Decision)

1. **Cưỡng Chế 100% Sự Hiện Diện Của Tệp Nhị Phân Nguồn (Mandatory Binary Asset Gate):**
   * Mọi gói tri thức pháp lý (`legal_docs/01_vbpl/<slug>/`) khi được đăng ký vào hệ thống bắt buộc phải thỏa mãn đồng thời:
     - Tồn tại tệp nhị phân nguồn thật trong `.md/extracted_docs/<slug>/<file>.docx` (được tải từ TVPL VIP hoặc Cổng Dữ liệu Quốc gia).
     - Hoặc có tệp PDF Công báo gốc trong bundle với mã băm SHA-256 đã qua kiểm toán đối soát thị giác.
2. **Cổng Chặn Tuyệt Đối Tại `validate_legal_spoke.py`:**
   * Tích hợp kiểm tra bắt buộc trong `validate_legal_spoke.py`. Nếu phát hiện bất kỳ bundle nào thiếu tệp nguồn nhị phân hoặc có kích thước bất thường (< 10 KB đối với văn bản quy phạm lớn):
     - Đánh lỗi đỏ `CRITICAL ERROR`.
     - Ngăn chặn hoàn toàn quá trình Git Commit hoặc Merge Request.
3. **Cấm Tiếp Nhận Nguồn Markdown Trôi Nổi:**
   * Tuyệt đối cấm tạo mới văn bản quy phạm chỉ từ việc sao chép/dán mã HTML web thô bằng các công cụ `read_url_content` hay `requests`.

---

## 3. Hệ quả & Đánh đổi (Consequences)

### Tích cực:
* ✅ Bảo vệ 100% tính toàn vẹn và uy tín pháp lý của dữ liệu Spoke.
* ✅ Triệt tiêu hoàn toàn hiện tượng "chữa cháy" bằng tệp giả tạo từ các AI Agent.
* ✅ Tự động hóa quy trình kiểm định chất lượng dữ liệu trước khi tích hợp vào các dịch vụ AI QC downstream.

---

## 4. Tham chiếu (References)
- [ADR 0010: Four-Layer TVPL VIP Crawler](./0010-four-layer-tvpl-vip-crawler-three-tier-fallback.md)
- [ADR 0016: Dual-Track Hybrid PDF Anchor of Trust](./0016-dual-track-hybrid-pdf-anchor-of-trust.md)
- [ADR 0021: OKF v2.2 Pure Normative Body & Legal Graph](./0021-okf-v2-2-pure-normative-body-legal-graph.md)
- [AGENTS.md: Spoke Workspace Constitution](../../AGENTS.md)
