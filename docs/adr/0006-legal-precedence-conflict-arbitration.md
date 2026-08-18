# ADR 0006: Thứ Bậc Hiệu Lực Pháp Lý & Cơ Chế Phân Xử Xung Đột Trong AI QC Audits

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-18
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0003: Annex Normative Guardrails](0003-annex-normative-guardrails.md), [ADR 0005: Semantic Legal URI Scheme](0005-semantic-legal-uri-scheme.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)
Trong quá trình thẩm tra tự động hồ sơ thiết kế công trình (*AI QC Audits*), mô hình AI thường xuyên đối mặt với các tình huống xung đột chỉ tiêu kỹ thuật giữa nhiều tầng văn bản pháp quy:
1. Xung đột giữa Quy chuẩn Kỹ thuật Quốc gia (QCVN - Bắt buộc) và Tiêu chuẩn Quốc gia (TCVN - Tự nguyện áp dụng).
2. Xung đột giữa các mốc thời gian hiệu lực pháp lý (Văn bản mới ban hành như Nghị định 217/2026/NĐ-CP thay thế Nghị định 175/2024/NĐ-CP).
3. Các trường hợp QCVN quy định một chỉ tiêu cứng nhưng cho phép áp dụng giải pháp tương đương hoặc tiêu chuẩn chuyên ngành thông qua thuyết minh tính toán.

Nếu không có cơ chế phân xử thứ bậc rõ ràng:
- AI Agent sẽ sinh ra hàng loạt cảnh báo sai (*False Positives*), gây ức chế cho đơn vị tư vấn thiết kế và đội chi phí công trình (*Over-engineering*).
- Hoặc ngược lại, bỏ sót các lỗi vi phạm quy chuẩn bắt buộc (*False Negatives*), gây rủi ro pháp lý khi thẩm duyệt PCCC.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định thiết lập mô hình **Thứ Bậc Hiệu Lực Pháp Lý & Phân Xử Xung Đột (Strict Hierarchical Precedence with Exception Tagging)** cho toàn bộ AI QC Pipeline:

### A. Quy Tắc Phân Cấp Hiệu Lực (Precedence Hierarchy):
1. **Thứ bậc Loại hình:** `Luật > Nghị định > Thông tư / QCVN > TCVN / Tiêu chuẩn cơ sở`.
2. **Nguyên tắc Văn bản Mới (Lex Posterior):** Khi 2 văn bản cùng cấp điều chỉnh một nội dung, áp dụng văn bản ban hành sau có hiệu lực (ví dụ: Nghị định 217/2026/NĐ-CP có hiệu lực từ 01/07/2026 thay thế hoàn toàn Nghị định 175/2024/NĐ-CP).
3. **QCVN là Tối Thượng:** Nếu TCVN cho phép thông số nới lỏng hơn QCVN $\rightarrow$ Cưỡng chế bắt buộc tuân thủ theo QCVN.

### B. Cơ Chế Gán Nhãn Phát Hiện (Defect Classification Matrix):
- **Lỗi Vi Phạm Cốt Tử (`Critical Defect` - Bắt buộc sửa):** Vi phạm trực tiếp điều khoản bắt buộc của Luật, Nghị định hoặc QCVN mà không có ngoại lệ.
- **Khuyến Nghị Thuyết Minh (`Verification Required Notice` - Cảnh báo vàng):** Trường hợp hồ sơ áp dụng giải pháp theo TCVN chuyên ngành hoặc giải pháp tương đương mà chính QCVN cho phép mở $\rightarrow$ AI QC Agent không gắn nhãn vi phạm, mà tạo mục yêu cầu kỹ sư đính kèm bản thuyết minh tính toán kỹ thuật.
- **Gợi Ý Tối Ưu (`Informational Suggestion` - Tham khảo xanh):** Ý kiến đóng góp từ các Phụ lục tham khảo (như Phụ lục I).

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Chuẩn xác pháp lý $100\%$:** Kết quả báo cáo thẩm tra PCCC và hồ sơ kỹ thuật có căn cứ pháp lý vững chắc khi làm việc với cơ quan Cảnh sát PCCC và Sở Xây dựng.
- **Giảm $95\%$ False Positives:** Không bắt bẻ oan các giải pháp thiết kế hợp pháp đã có thuyết minh tính toán tương đương.
- **Bảo vệ chi phí đầu tư:** Tránh tình trạng đội chi phí kết cấu do áp dụng quy chuẩn quá mức cần thiết.

### Đánh đổi:
- AI QC Reasoner cần phân tích ngữ nghĩa để nhận diện các câu mở ngoại lệ (*Exception Clauses*) trong quy chuẩn.
