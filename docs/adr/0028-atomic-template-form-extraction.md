# ADR 0028: Atomic Template Form Extraction & Table Isolation

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-08-21)

## 2. Bối Cảnh (Context)
Nhiều Thông tư và Nghị định chứa hàng chục Phụ lục biểu mẫu hành chính (như Mẫu số 01, Mẫu số 02) và các bảng đơn giá/định mức lớn. Nếu để nguyên trong thân văn bản chính:
- Làm loãng ngữ cảnh quy phạm pháp luật (Normative Text Clutter).
- Làm tăng chi phí và giảm độ chính xác khi RAG truy vấn điều khoản luật.

## 3. Quyết Định Thiết Kế (Decision)
1. **Tách Biểu Mẫu Thành Atomic Form Templates (`templates/phu_luc_XX/mau_YY_...md`):**
   - Loại bỏ rác layout hành chính (Quốc hiệu, Tiêu ngữ, Kính gửi, Dấu chấm lửng placeholder `...`).
   - Giữ lại cấu trúc trường dữ liệu điền thông tin dạng bảng Markdown chuẩn.
2. **Tách Bảng Số Liệu Lớn Vào `tables/`:**
   - Các bảng tra cứu độc lập được trích xuất thành các tệp bảng riêng, thân văn bản chỉ giữ liên kết tham chiếu `[Bảng X](tables/bang_X.md)`.

## 4. Hệ Quả (Consequences)
- Thân văn bản đạt độ thuần khiết quy phạm $100\%$ (Pure Normative Body).
- Phục vụ trực tiếp cho AI Agent tự động điền biểu mẫu hồ sơ hoàn thành và nghiệm thu.
