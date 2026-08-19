# ADR 0016: Dual-Track Hybrid Extraction & PDF Anchor of Trust Protocol

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-19
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0001: Dual-Track VBHN](0001-vbhn-dual-track-provenance.md), [ADR 0010: TVPL VIP Crawler](0010-four-layer-tvpl-vip-crawler-three-tier-fallback.md), [ADR 0011: Atomic Clause Chunking](0011-atomic-clause-rag-chunking-strategy.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Trong hoạt động tư vấn xây dựng và thẩm định pháp lý tại Việt Nam:
- Các cơ quan quản lý nhà nước (Cục Cảnh sát PCCC & CNCH, Sở Xây dựng, Hội đồng nghiệm thu Nhà nước) **chỉ công nhận giá trị pháp lý tối thượng của bản in Công báo có mộc đỏ và chữ ký số chính thức**.
- Tuy nhiên, việc bóc tách tri thức trực tiếp từ file PDF thuần túy gặp nhiều rào cản kỹ thuật:
  * Tiêu đề đầu trang (*Header*), chân trang (*Footer*), số trang chèn ngang làm đứt đoạn câu văn và bảng biểu.
  * Mất các thuộc tính cấu trúc quan trọng (như định dạng phân cấp tiêu đề, ô gộp bảng, chỉ số trên/dưới $m^2, m^3$).

Nếu chỉ dựa hoàn toàn vào file DOCX bóc tách mà không có cơ chế đối soát và truy vết gắn kết với file PDF Công báo:
- Kỹ sư khi sử dụng kết quả thẩm tra của AI QC sẽ gặp khó khăn khi giải trình với cán bộ thẩm duyệt nhà nước nếu không có số trang và bằng chứng đối chiếu trên bản in Công báo chính thức.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định thiết lập quy chuẩn **Mô hình Trích Xuất & Đối Soát Lai Ghép (Dual-Track Hybrid Model)** lấy **File PDF Công Báo làm Mỏ Neo Pháp Lý Tối Thượng (Legal Anchor of Trust)**:

1. **Phân Công Vai Trò Kỹ Thuật (Role Separation):**
   - **Tệp DOCX (Structure & AST Extraction Engine):** Đóng vai trò là nguồn bóc tách cấu trúc dữ liệu nguyên tử (DOM parsing, trích xuất bảng biểu 2D không bị ngắt trang, chuyển đổi Markdown OKF và cây cú pháp AST `clauses.json`).
   - **Tệp PDF Công Báo (Legal Anchor of Trust & Visual Ground Truth):** Đóng vai trò là mỏ neo pháp lý bất biến, căn cứ đối soát thị giác đa tầng và cơ sở giải trình có dấu mộc nhà nước.

2. **Quy Trình 4 Lớp Phòng Thủ Đối Soát PDF Gốc (4-Layer PDF Defense):**
   - **Lớp 1 (Mã Băm Bất Biến):** Tính toán và lưu cứng mã băm SHA-256 của file PDF gốc trong `legal_registry.yaml`.
   - **Lớp 2 (Đối Soát Phân Cấp Thị Giác):** Sử dụng ảnh quét trang PDF Công báo để phát hiện và chuẩn hóa các danh mục lồng đa tầng (như quy định trạm sạc xe điện 3 cấp tại trang 96 Công báo 373/2026).
   - **Lớp 3 (AI Vision Table Verification):** Sử dụng AI Vision chụp ảnh từng trang bảng số liệu trong PDF gốc để đối soát $100\%$ độ chính xác giá trị số, đơn vị đo và số mũ.
   - **Lớp 4 (Truy Vết Tọa Độ Trang 1-Click):** Mỗi điều khoản trong `clauses.json` bắt buộc lưu trữ tọa độ trang PDF (`source_pdf_page`, `cong_bao_number`). Kỹ sư bấm vào trích dẫn sẽ mở trực tiếp trang PDF Công báo có dấu đỏ tương ứng.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Bảo đảm giá trị pháp lý $100\%$:** Mọi kết luận kiểm toán của AI QC đều có thể chứng minh tức thì trên giấy trắng mực đen có mộc đỏ của cơ quan nhà nước.
- **Tối ưu hóa hiệu suất:** Kết hợp được tốc độ xử lý siêu tốc của Markdown/JSON với độ tin cậy tuyệt đối của PDF Công báo.

### Đánh đổi:
- Cần lưu trữ song song cả file PDF gốc và DOCX trong kho `.md/extracted_docs/` và duy trì chỉ mục số trang `source_pdf_page` trong AST.
