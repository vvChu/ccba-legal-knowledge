# ADR 0013: Dynamic Grace Period Compliance Gate for Retroactive Transition Auditing

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-19
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0006: Thứ bậc Hiệu lực](0006-legal-precedence-conflict-arbitration.md), [ADR 0008: Temporal Query Engine](0008-temporal-query-engine-point-in-time-auditing.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Một số văn bản quy phạm kỹ thuật mới ban hành đưa ra các nghĩa vụ bắt buộc áp dụng hồi tố đối với các công trình hiện hữu nhưng cho phép một **Khoảng thời gian Ân hạn (Grace Period)** để chủ đầu tư, ban quản trị hoàn thiện phương án cải tạo, thích ứng.
- Cụ thể: Theo Khoản 2 Điều 2 Thông tư 31/2026/TT-BXD ban hành Sửa đổi 01:2026 QCVN 04:2021/BXD:
  * Quy định bắt buộc rà soát an toàn PCCC, phân vùng chỗ để xe điện trong các chung cư hiện hữu có hiệu lực từ ngày `2026-12-15`.
  * Các chung cư hiện hữu được nhà nước cho phép thời hạn **06 tháng** kể từ ngày có hiệu lực (tức đến hết ngày `2027-06-15`) để hoàn thành rà soát và thực hiện các biện pháp an toàn.

Nếu hệ thống kiểm toán tự động AI QC áp dụng cứng quy tắc nhị phân (*Binary Pass/Fail*) ngay khi Thông tư vừa có hiệu lực:
- AI sẽ gán nhãn `Critical Defect` (Lỗi Đỏ Vi phạm Pháp luật) cho tất cả các chung cư hiện hữu đang trong quá trình rà soát, dẫn đến sai lệch bản chất pháp lý (*Legal Fallacy*) và gây hoang mang không cần thiết cho khách hàng.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định thiết lập mô hình **Cổng Kiểm Toán Ân Hạn Động (Dynamic Grace Period Compliance Gate)** trong AI QC Engine:

1. **Cấu Trúc Siêu Dữ Liệu Ân Hạn (Grace Period Schema):**
   - Trong `clauses.json` và `legal_registry.yaml`, các điều khoản có quy định ân hạn chuyển tiếp được gắn thêm các trường:
     ```json
     {
       "clause_id": "muc-2-10-2-1",
       "effective_date": "2026-12-15",
       "has_grace_period": true,
       "grace_period_days": 180,
       "grace_period_end": "2027-06-15",
       "grace_target": "existing_buildings"
     }
     ```

2. **Quy Tắc Đổi Nhãn Kiểm Toán Theo Mốc Thời Gian (Dynamic Label Escalation):**
   - **Giai đoạn 1 (`audit_date < 2026-12-15`):** Chưa có hiệu lực $\rightarrow$ Thông báo khuyến nghị chuẩn bị (*Advisory Note*).
   - **Giai đoạn 2 (`2026-12-15 <= audit_date <= 2027-06-15`):** Giai đoạn Ân hạn 6 tháng $\rightarrow$ Gán nhãn **🟡 Warning Notice (Cảnh Báo Ân Hạn Rà Soát)** kèm số ngày còn lại đến hạn chót `2027-06-15` và bản danh mục công việc cần hoàn thành.
   - **Giai đoạn 3 (`audit_date > 2027-06-15`):** Hết thời hạn ân hạn $\rightarrow$ Tự động nâng mức thành **🔴 Critical Defect (Lỗi Đỏ Vi Phạm Quy Chuẩn Bắt Buộc)**.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Độ chính xác pháp lý tuyệt đối:** Báo cáo thẩm tra của CCBA phản ánh trung thực quyền và nghĩa vụ hợp pháp của chủ đầu tư trong từng giai đoạn chuyển tiếp.
- **Tăng giá trị tư vấn thực tiễn:** Cung cấp lộ trình hành động (Actionable Roadmap) kèm đồng hồ đếm ngược thời hạn tuân thủ giúp khách hàng chủ động ngân sách cải tạo.

### Đánh đổi:
- Cần bổ sung logic kiểm tra `audit_date` so với `grace_period_end` trong bộ quy tắc kiểm toán QC của nền tảng.
