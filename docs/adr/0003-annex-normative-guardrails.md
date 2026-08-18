# ADR 0003: Phân loại Siêu dữ liệu Phụ lục Bắt buộc vs. Tham khảo & Rào chắn Cưỡng chế Pháp lý

- **Trạng thái:** `Accepted`
- **Ngày quyết định:** 2026-08-18
- **Tác giả:** CCBA Core Engineering Team
- **Phạm vi:** Cây AST (`clauses.json`), RAG Pipeline và AI QC Engine trong Spoke `ccba-legal-knowledge`

---

## 1. Ngữ cảnh & Vấn đề (Context & Problem Statement)

Theo Điều 7 TCVN 1-2:2008, các phụ lục trong tiêu chuẩn/quy chuẩn được phân thành hai nhóm với bản chất pháp lý hoàn toàn khác biệt:
1. **Phụ lục quy định (Normative Annex):** Mang tính bắt buộc pháp lý như thân văn bản chính (ví dụ: Phụ lục A đến H trong QCVN 06:2022/BXD).
2. **Phụ lục tham khảo (Informative Annex):** Chỉ là hình minh họa, ví dụ hoặc hướng dẫn nghiệp vụ (ví dụ: Phụ lục I - Hình minh họa trong QCVN 06:2022/BXD, các bảng so sánh luật trong `04_appendices`).

Nếu không có trường cờ siêu dữ liệu (*Metadata Flag*) phân biệt rõ ràng:
- AI QC Pipeline có nguy cơ ngộ nhận hình ảnh minh họa tham khảo là tiêu chuẩn bắt buộc cứng, dẫn đến **bắt lỗi oan (*False Positives*)** các giải pháp thiết kế hợp chuẩn khác của kỹ sư.

---

## 2. Các Phương án Đã Xem xét (Considered Options)

- **Option A (Được chọn): Explicit Normative Metadata Flagging & Legal Enforceability Guardrails.**  
  Gắn tường minh hai trường `normative_status: "mandatory" | "informative"` và `legal_enforceability: true | false` vào cây AST `clauses.json`. Đồng thời thiết lập rào chắn trong AI QC: Nếu `legal_enforceability == false`, Agent chỉ được phép xuất khuyến nghị (*Advisory Recommendation*), cấm gán nhãn vi phạm pháp lý (*Defect/Violation*).
- **Option B: Textual Context Only.**  
  Chỉ để chữ `(quy định)` hay `(tham khảo)` trong tiêu đề Markdown và dựa vào khả năng đọc hiểu tự nhiên của LLM. *(Bị loại vì tiềm ẩn rủi ro sinh lỗi thẩm tra sai lệch)*.

---

## 3. Quyết định (Decision)

Áp dụng **Option A** cho toàn bộ Spoke:
1. Mọi phụ lục và bảng biểu thuộc phụ lục trong `clauses.json` và `tables/tables_catalog.json` bắt buộc có metadata phân loại hiệu lực pháp lý.
2. AI QC Pipeline tích hợp bộ lọc Guardrail: Tự động hạ cấp các phát hiện liên quan đến Phụ lục tham khảo thành *Best-Practice Advice*, không tính vào chỉ số lỗi nghiêm trọng của hồ sơ thiết kế.

---

## 4. Hệ quả & Đánh đổi (Consequences & Trade-offs)

### Tích cực:
- **Loại bỏ False Positives:** Đảm bảo 100% các lỗi báo cáo từ AI QC là vi phạm quy chuẩn thực sự có chế tài bắt buộc.
- **Tuân thủ đúng bản chất TCVN 1-2:2008:** Phản ánh chính xác khoa học biên soạn tiêu chuẩn quốc gia.

### Đánh đổi (Negative/Effort):
- Schema AST của `clauses.json` cần được cập nhật và kiểm toán tính toàn vẹn qua bộ script `verify_knowledge_integrity.py`.
