# ADR 0002: Chuẩn hóa Ma trận Ràng buộc Footnote Bảng biểu (Structured Footnote Binding Matrix) cho AI QC Audit

- **Trạng thái:** `Accepted`
- **Ngày quyết định:** 2026-08-18
- **Tác giả:** CCBA Core Engineering Team
- **Phạm vi:** Toàn bộ dữ liệu bảng biểu kỹ thuật (`tables/json/*.json`, `tables/csv/*.csv`) trong Spoke `ccba-legal-knowledge`

---

## 1. Ngữ cảnh & Vấn đề (Context & Problem Statement)

Trong các quy chuẩn xây dựng Việt Nam (như QCVN 06:2022/BXD, QCVN 04:2021/BXD), các bảng kỹ thuật thường chứa các ô giá trị gắn liền với số hiệu chú thích điều kiện (ví dụ: `"1 400 5)"` nghĩa là diện tích 1.400 $\text{m}^2$ đi kèm điều kiện ràng buộc tại Chú thích 5).
Nếu hệ thống chỉ lưu trữ bảng ở dạng chuỗi văn bản phẳng (*Flat String*):
1. **Lỗi thẩm tra số học:** AI QC Agent chỉ so sánh giá trị số $1.400\text{ m}^2$ mà không thể tự động phát hiện và kiểm tra các điều kiện tiên quyết bắt buộc (ví dụ: công trình phải trang bị chữa cháy tự động).
2. **Rủi ro phân tích cú pháp:** Mô hình LLM dễ nhầm lẫn ký hiệu số chú thích `5)` với số mũ toán học, chỉ số phụ hoặc kích thước hình học.

---

## 2. Các Phương án Đã Xem xét (Considered Options)

- **Option A (Được chọn): Structured Footnote Binding Matrix.**  
  Chuẩn hóa cấu trúc JSON của bảng với 3 thành phần: Lưới ô dữ liệu bóc tách `numeric_value`, `unit`, `condition_refs` liên kết trực tiếp với danh mục `footnotes` có `id` và `type: normative_condition`.
- **Option B: Flat String Footnotes.**  
  Giữ nguyên chuỗi thô `"1 400 5)"` trong ô và để footnotes là mảng chuỗi đơn thuần. *(Bị loại vì làm giảm độ chính xác và tăng chi phí token khi chạy AI QC Pipeline)*.

---

## 3. Quyết định (Decision)

Áp dụng **Option A (Structured Footnote Binding Matrix)** cho toàn bộ hệ thống bảng biểu kỹ thuật trong Spoke:
1. `tables/json/bang_*.json` sẽ hỗ trợ schema mở rộng chứa cả `raw`, `numeric_value`, `unit`, và `condition_refs`.
2. Mọi `CHÚ THÍCH` đều được đánh chỉ mục và phân loại pháp lý (`normative_condition`, `exception`, `definition`).
3. Xuất file `tables/tables_catalog.json` cung cấp bản đồ tổng thể cho Agent truy vấn bảng và điều kiện trong $\le 0.1\text{ ms}$.

---

## 4. Hệ quả & Đánh đổi (Consequences & Trade-offs)

### Tích cực:
- **Nâng cao 100% độ chính xác cho AI QC:** Agent tự động tạo checklist 2 bước (kiểm tra thông số kỹ thuật + kiểm tra điều kiện kèm theo).
- **Hạn chế tối đa Hallucination:** Dữ liệu số học và điều kiện biên được tách rời minh bạch, máy đọc trực tiếp không cần parse lại text thô.

### Đánh đổi (Negative/Effort):
- Script trích xuất bảng biểu (`docx_table_extractor.py`) cần bổ sung module phân tích cú pháp số + footnote regex để tự động sinh schema mở rộng.
