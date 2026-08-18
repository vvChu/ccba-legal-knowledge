# ADR 0004: Structured Array Pointer Binding Cho Chỉ Số Phụ Đa Tầng Trong Bảng Kỹ Thuật

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-18
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0002: Structured Table Footnote Binding Matrix](0002-structured-table-footnote-binding.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)
Trong các bảng kỹ thuật của QCVN 06:2022/BXD và Sửa đổi 1:2023 (đặc biệt tại Phụ lục H, Phụ lục F, Phụ lục E), xuất hiện nhiều trường hợp một ô dữ liệu hoặc một hàng mang **đồng thời nhiều chỉ số phụ** hoặc **chỉ số phụ lồng điều kiện**, ví dụ:
- Ô dữ liệu: `1 400 <sup>2), 3)</sup>` (Vừa yêu cầu hệ thống chữa cháy tự động Sprinkler, vừa giới hạn chiều cao trần).
- Ô dữ liệu: `150 <sup>a), 1)</sup>` (Vừa viện dẫn bảng phụ lục con, vừa viện dẫn ghi chú chỉ số chân bảng).

Nếu biểu diễn thô dạng chuỗi hoặc nhúng trực tiếp toàn văn (*inline text dereferencing*), hệ thống sẽ gặp các vấn đề nghiêm trọng:
1. **Dữ liệu phình to và trùng lặp:** Sao chép nội dung chú thích vào hàng nghìn ô dữ liệu.
2. **Sai lệch logic thẩm tra:** AI QC Agent không thể thực thi logic Boolean (`AND`/`OR`) giữa các điều kiện ràng buộc độc lập.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định áp dụng mô hình **Structured Array Pointer Binding** (Ràng buộc Mảng Con trỏ Điều kiện) trong schema JSON của toàn bộ các bảng kỹ thuật (`tables/json/*.json`):

1. **Phân rã mảng nguyên tử (`Atomic Array`):** Mỗi ô dữ liệu kỹ thuật được chuẩn hóa thành cấu trúc chứa:
   - `raw`: Chuỗi ký tự hiển thị ban đầu.
   - `numeric_value`: Giá trị số học thuần túy (dành cho bộ so sánh toán học).
   - `unit`: Đơn vị đo lường danh định (`mm`, `m2`, `m`, `m3/h`, v.v.).
   - `superscript_refs`: Mảng các mã số/ký tự chỉ số phụ `[2, 3]`.
   - `evaluation_logic`: Toán tử logic bắt buộc giữa các điều kiện (Mặc định là `"AND"`, hoặc `"OR"` khi có quy định thay thế).
   - `condition_bindings`: Mảng các con trỏ ràng buộc ánh xạ trực tiếp đến định danh chú thích (`target_footnote_id`).

2. **Schema mẫu chuẩn:**
   ```json
   {
     "raw": "1 400 2), 3)",
     "numeric_value": 1400,
     "unit": "m2",
     "superscript_refs": [2, 3],
     "evaluation_logic": "AND",
     "condition_bindings": [
       {
         "ref": 2,
         "type": "normative_mandatory",
         "target_footnote_id": "fn_2",
         "condition_summary": "Phải trang bị hệ thống chữa cháy tự động sprinkler"
       },
       {
         "ref": 3,
         "type": "normative_mandatory",
         "target_footnote_id": "fn_3",
         "condition_summary": "Chiều cao từ sàn đến trần không vượt quá 6,1 m"
       }
     ]
   }
   ```

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Độ tin cậy toán học $100\%$:** AI QC Agent lấy được giá trị số $1.400$ mà không bị nhiễu bởi các ký tự chú thích.
- **Thực thi logic tuần tự:** Pipeline thẩm tra PCCC có thể kiểm tra từng điều kiện tiên quyết theo toán tử `AND`: Nếu công trình chưa có Sprinkler $\rightarrow$ Từ chối áp dụng giá trị $1.400\text{ m}^2$ và hạ bậc diện tích khoang cháy theo đúng luật.
- **Tiết kiệm dung lượng:** Không trùng lặp văn bản, duy trì cấu trúc quan hệ chuẩn mực.

### Đánh đổi:
- Bộ Parser cần tích hợp mô-đun bóc tách đa chỉ số (`Multi-index regex parser`) và validate schema JSON trong CI Gate.
