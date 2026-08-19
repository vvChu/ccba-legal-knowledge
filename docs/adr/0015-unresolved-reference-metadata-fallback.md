# ADR 0015: Unresolved Normative Reference Fallback & Metadata Card Resolution

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-19
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0005: Semantic Legal URI](0005-semantic-legal-uri-scheme.md), [ADR 0006: Thứ bậc Hiệu lực](0006-legal-precedence-conflict-arbitration.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Trong hệ thống quy chuẩn kỹ thuật xây dựng và PCCC (như QCVN 04:2021, QCVN 06:2022), tồn tại mạng lưới viện dẫn chéo đến hàng trăm Tiêu chuẩn quốc gia chuyên ngành (TCVN).
- Trong khi Spoke `ccba-legal-knowledge` đã hoàn tất số hóa toàn văn các đại quy chuẩn và văn bản quy phạm chính (29 tài liệu), một số tiêu chuẩn chuyên ngành (như *QCVN 10:2025/BCA, TCVN 6396 về thang máy, TCVN 3890 về trang bị phương tiện PCCC...*) đang ở trạng thái tệp gốc thô tại `.md/extracted_docs/` hoặc đang chờ bóc tách sang Markdown (`status: pending`).

Nếu liên kết bị gãy vỡ (Broken Links / 404):
- Kỹ sư khi bấm tra cứu sẽ nhận lỗi không tìm thấy tài liệu.
- Các mô hình AI RAG khi thực hiện suy luận đồ thị đa tài liệu (*Cross-Document Graph Traversal*) sẽ bị đứt mạch thông tin.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định chuẩn hóa cơ chế **Phân Giải Trì Hoãn & Thẻ Siêu Dữ Liệu Thông Minh (Unresolved Reference Fallback & Metadata Card Resolution)**:

1. **Chuẩn Hóa Giao Thức Viện Dẫn 100% qua Semantic URI (`legal://`):**
   - Mọi viện dẫn tiêu chuẩn kỹ thuật trong Markdown được định danh theo cú pháp:
     ```markdown
     [QCVN 10:2025/BCA](legal://qcvn_10_2025_bca)
     ```

2. **Cơ Chế Phân Giải 2 Nhánh Thông Minh (Two-Branch Resolver):**
   - **Nhánh 1 (Tài liệu đã có Markdown toàn văn - `status: active`):**
     - Router chuyển hướng tức thì đến đúng vị trí điều khoản/mục trong tệp `.md`.
   - **Nhánh 2 (Tài liệu chưa bóc tách Markdown - `status: pending/raw`):**
     - Router tự động hiển thị **Thẻ Siêu Dữ Liệu Tra Cứu (Metadata Stub Card)** trích xuất từ `legal_registry.yaml`:
       * Số hiệu tiêu chuẩn, Tên đầy đủ, Cơ quan ban hành, Ngày hiệu lực.
       * Tóm tắt phạm vi áp dụng.
       * Nút bấm **"Mở file PDF gốc có dấu đỏ"** (trỏ trực tiếp vào file PDF tại `.md/extracted_docs/`).
     - **Triệt tiêu hoàn toàn $100\%$ lỗi 404 Broken Links.**

3. **Bảo Toàn Đồ Thị Suy Luận RAG (Graph Reasoning Preservation):**
   - Khi Agent truy vấn một điều khoản có chứa liên kết `legal://`, engine RAG vẫn ghi nhận được mối quan hệ viện dẫn (Relation Graph Node) dựa trên dữ liệu tóm tắt của Metadata Card, không bị ngắt quãng chuỗi lập luận pháp lý.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Trải nghiệm tra cứu liền mạch 100% ngoại tuyến (Offline-First):** Kỹ sư luôn nhận được thông tin hữu ích và mở được file PDF gốc ngay cả khi văn bản chưa được số hóa sang Markdown.
- **Bảo vệ tính toàn vẹn của đồ thị tri thức pháp lý:** Không có liên kết "cụt" (Dead-end links).

### Đánh đổi:
- Cần khai báo đầy đủ số hiệu, tên và đường dẫn file PDF gốc trong `legal_registry.yaml` cho các tài liệu ở trạng thái `pending`.
