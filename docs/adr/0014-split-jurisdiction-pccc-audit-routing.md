# ADR 0014: Split Jurisdiction PCCC Audit Routing & Metadata Binding (Luật 55/2024 & NĐ 105/2025)

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-19
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0006: Thứ bậc Hiệu lực](0006-legal-precedence-conflict-arbitration.md), [ADR 0008: Temporal Query Engine](0008-temporal-query-engine-point-in-time-auditing.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Theo quy định tại **Luật Phòng cháy, chữa cháy và cứu nạn, cứu hộ 2024 (Luật số 55/2024/QH15)** và **Nghị định 105/2025/NĐ-CP** (có hiệu lực từ ngày 01/07/2025):
- Quy trình thẩm định thiết kế PCCC được cải cách theo mô hình **Phân định Thẩm quyền Chuyên ngành (Split Jurisdiction)** thay cho cơ chế một cửa Cảnh sát PCCC trước đây:
  1. *Cơ quan chuyên môn về Xây dựng (CQXD):* Thẩm định phần Kiến trúc, Bậc chịu lửa, Khoang cháy, Giải pháp thoát nạn, Hệ thống kiểm soát khói và Chỗ để xe điện (theo QCVN 06:2022 và QCVN 04:2021).
  2. *Cơ quan Công an (Cảnh sát PC07):* Thẩm định phần Hệ thống Cơ điện PCCC (MEP), Hệ thống báo cháy tự động, Hệ thống chữa cháy tự động Sprinkler/Drencher/Khí, Hệ thống cấp nước chữa cháy ngoài nhà và Phương tiện cứu nạn (theo QCVN 10, TCVN 3890, TCVN 7336).
  3. *Chủ đầu tư / Tư vấn:* Tự thẩm tra và chịu trách nhiệm đối với các công trình không thuộc diện cơ quan nhà nước thẩm định bắt buộc.

Nếu cây tri thức AST (`clauses.json`) chỉ lưu trữ văn bản kỹ thuật đơn thuần mà không có nhãn thẩm quyền:
- Báo cáo kiểm toán AI QC sẽ bị dồn chung thành một khối hỗn tạp, không thể phân rã thành các bộ hồ sơ nộp riêng biệt cho từng cơ quan nhà nước theo luật định.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định cấu trúc hóa mô hình **Phân Định Thẩm Quyền Thẩm Tra Đa Bộ Môn (Split Jurisdiction Routing Architecture)** vào toàn bộ cây dữ liệu tri thức và AI QC Pipeline:

1. **Cấu Trúc Siêu Dữ Liệu Thẩm Quyền (Jurisdiction Metadata Schema):**
   - Mọi điều khoản trong `clauses.json` thuộc các quy chuẩn/tiêu chuẩn kỹ thuật (QCVN 06, QCVN 04, QCVN 10, TCVN 3890...) bắt buộc phải mang các trường định tuyến thẩm quyền:
     ```json
     {
       "clause_id": "muc-2-10-2-1",
       "jurisdiction": "CQXD",
       "cooperating_agency": "CONG_AN",
       "review_workflow": "workflow_pccc_thamdinh_cqxd",
       "legal_basis": "Luat-55-2024-ND-105-2025"
     }
     ```
   - Các giá trị `jurisdiction` được chuẩn hóa thành Enum:
     - `CQXD`: Cơ quan Chuyên môn về Xây dựng (Sở Xây dựng / Cục QLXD).
     - `CONG_AN`: Cơ quan Cảnh sát PCCC và CNCH (PC07 / Cục C07).
     - `CHU_DAU_TU_TU_THAM_DINH`: Chủ đầu tư / Tư vấn tự thẩm tra.

2. **Cơ Chế Phân Rã Báo Cáo Tự Động (Multi-Dossier Report Generation):**
   - Khi kích hoạt Audit, AI QC Engine tự động phân luồng kết quả thành **3 tập hồ sơ chuyên biệt**:
     - *Hồ sơ Tập 1:* Báo cáo Thẩm tra Kiến trúc & Khói nộp CQXD (theo workflow `/workflow_pccc_thamdinh_cqxd`).
     - *Hồ sơ Tập 2:* Báo cáo Thẩm duyệt Hệ thống Cơ điện PCCC nộp Cơ quan Công an (theo workflow `/workflow_pccc_thamdinh_congan`).
     - *Hồ sơ Tập 3:* Báo cáo Kiểm soát Chất lượng Nội bộ cho Chủ đầu tư (theo workflow `/workflow_pccc_cdt_tuthamdinh`).

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Tương thích $100\%$ với Luật 55/2024 và NĐ 105/2025:** Giúp các đơn vị tư vấn thiết kế và chủ đầu tư phát hành hồ sơ nộp cơ quan chức năng hoàn toàn chuẩn chỉnh theo đúng thẩm quyền.
- **Tự động hóa toàn trình (End-to-End Automation):** Kỹ sư không phải tốn hàng giờ đồng hồ để lọc và tách lỗi thủ công giữa phần Kiến trúc và phần Cơ điện.

### Đánh đổi:
- Cần duy trì ma trận phân định thẩm quyền trong `clauses.json` và cập nhật khi có hướng dẫn liên tịch mới giữa Bộ Xây dựng và Bộ Công an.
