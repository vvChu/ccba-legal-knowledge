# ADR 0008: Temporal Legal Query Engine & Point-in-Time Auditing Protocol

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-18
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0001: Dual-Track VBHN](0001-vbhn-dual-track-provenance.md), [ADR 0006: Thứ bậc Hiệu lực](0006-legal-precedence-conflict-arbitration.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)
Các dự án đầu tư xây dựng thực tế thường trải qua chu kỳ thiết kế, thẩm duyệt, thi công và nghiệm thu kéo dài từ 2 đến 5 năm. Theo quy định tại Điều 156 Luật Ban hành VBPL và các điều khoản chuyển tiếp:
- Một công trình được cấp Giấy phép quy hoạch / Thẩm duyệt PCCC tại mốc thời gian $T_1$ phải được thẩm tra và nghiệm thu dựa trên đúng quy chuẩn pháp lý có hiệu lực tại thời điểm $T_1$, không bị hồi tố bởi các quy chuẩn ban hành sau tại $T_2$ (trừ trường hợp tự nguyện áp dụng hoặc quy chuẩn mới có quy định hồi tố bắt buộc).

Nếu hệ thống AI QC chỉ duy trì phiên bản mới nhất (*Latest Version*):
- AI Agent sẽ bắt lỗi sai lệch (*False Violations*) đối với các công trình thiết kế hợp pháp theo mốc thời gian cũ.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định thiết lập mô hình **Động cơ Tra cứu Theo Thời gian (Temporal Legal Query Engine / Time-Travel RAG)** cho toàn bộ Spoke Tri thức Pháp lý:

1. **Khoảng Thời Gian Hiệu Lực (Effective Temporal Interval):**
   - Trong `legal_registry.yaml` và `clauses.json`, mỗi phiên bản văn bản và mỗi điều khoản đều được gắn cặp thuộc tính thời gian:
     ```yaml
     qcvn_06_2022_bxd:
       effective_from: "2023-01-16"
       effective_to: "2023-11-30"  # Hết hiệu lực bản gốc khi Sửa đổi 1 có hiệu lực
     qcvn_06_2022_bxd_hop_nhat_2023:
       effective_from: "2023-12-01"
       effective_to: null          # Hiện hành
     ```

2. **Cơ Chế Phân Giải Tự Động Theo Mốc Thiết Kế (Design Base Date Filter):**
   - Khi Agent hoặc kỹ sư kích hoạt tác vụ thẩm tra với tham số `design_date` (ví dụ: `design_date: "2023-05-20"`):
   - Query Engine tự động lọc và cấp phát chính xác tệp tri thức tương ứng:
     - Nếu `design_date < 2023-12-01` $\rightarrow$ Nạp toàn văn `qcvn_06_2022_bxd.md` (Bản gốc).
     - Nếu `design_date >= 2023-12-01` $\rightarrow$ Nạp toàn văn `qcvn_06_2022_bxd_hop_nhat_2023.md` (Bản Hợp nhất).

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Khả năng thẩm tra lịch sử chính xác $100\%$:** Giải quyết hoàn toàn bài toán nghiệm thu công trình chuyển tiếp và thẩm tra hồ sơ cải tạo nâng cấp.
- **Tương thích RAG đa phiên bản:** Không cần nhân bản nhiều codebase riêng biệt, cùng một engine có thể phục vụ mọi mốc lịch sử dự án.

### Đánh đổi:
- Cần ghi nhận chính xác mốc `effective_from` và `effective_to` trong `legal_registry.yaml` cho tất cả các văn bản quy phạm.
