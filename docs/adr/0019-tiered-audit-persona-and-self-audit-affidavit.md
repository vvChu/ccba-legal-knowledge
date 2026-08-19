# ADR 0019: Tiered Audit Persona & Client Self-Audit Affidavit Engine

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-19
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0014: Split Jurisdiction PCCC Audit Routing](0014-split-jurisdiction-pccc-audit-routing.md), [ADR 0016: Dual-Track Hybrid PDF Anchor](0016-dual-track-hybrid-pdf-anchor-of-trust.md), [ADR 0018: Git-Ratchet Multi-Platform Knowledge Sync](0018-git-ratchet-multi-platform-knowledge-sync.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Theo khung pháp lý mới của **Luật Phòng cháy, chữa cháy và Cứu nạn, cứu hộ số 55/2024/QH15** và **Nghị định số 105/2025/NĐ-CP**:
- Trách nhiệm thẩm định thiết kế PCCC được phân luồng rõ rệt theo 3 nhóm đối tượng:
  1. **Cơ quan Chuyên môn về Xây dựng (Sở Xây dựng / Bộ Xây dựng):** Thẩm tra phần Kiến trúc, Bậc chịu lửa, Ngăn cháy lan, Khoảng cách thoát nạn, Hệ thống kiểm soát khói và Khu vực sạc xe điện.
  2. **Cơ quan Cảnh sát PCCC & CNCH (PC07):** Thẩm duyệt phần Hệ thống thiết bị PCCC, Báo cháy tự động, Chữa cháy tự động (Sprinkler, Drencher, Khí), Cấp nước chữa cháy ngoài nhà và trong nhà.
  3. **Chủ Đầu Tư (Chế độ Tự Thẩm Định - Self-Audit):** Áp dụng đối với các công trình không thuộc danh mục bắt buộc cơ quan nhà nước thẩm duyệt, hoặc các công trình thuộc diện tự cải tạo, sửa chữa, hoặc nhu cầu tự kiểm tra trước (Pre-Audit) của các Chủ đầu tư lớn trước khi nộp hồ sơ chính thức.

Nếu hệ thống kiểm toán AI QC xuất ra một báo cáo gộp đơn khối (*Monolithic Report*):
- Sẽ gây lúng túng cho các cơ quan thẩm duyệt chuyên ngành vì phải đọc lẫn các điều khoản ngoài thẩm quyền quản lý.
- Thiếu một chứng từ pháp lý chuẩn hóa (*Self-Audit Affidavit*) cho Chủ đầu tư để ký số lưu trữ vào Hồ sơ Hoàn thành công trình phục vụ công tác hậu kiểm của Thanh tra Xây dựng và Công an PCCC.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định thiết lập **Động Cơ Kiểm Toán Phân Hạng Đối Tượng & Tự Động Xuất Biên Bản Tự Thẩm Định (Tiered Audit Persona & Self-Audit Affidavit Generator)**:

1. **Ba Chế Độ Kiểm Toán Độc Lập (3 Independent Audit Personas):**
   - `MODE_CQXD` (Hồ sơ Thẩm tra Xây dựng):
     - Lọc các điều khoản có nhãn `jurisdiction: 'CQXD'`.
     - Xuất báo cáo kỹ thuật theo mẫu thẩm tra phục vụ nộp Sở Xây dựng theo Nghị định 175/2024/NĐ-CP & Luật Xây dựng 2025.
   - `MODE_PC07` (Hồ sơ Thẩm duyệt PCCC):
     - Lọc các điều khoản có nhãn `jurisdiction: 'CONG_AN'`.
     - Xuất báo cáo kỹ thuật theo thể thức nộp Phòng Cảnh sát PC07 theo Nghị định 105/2025/NĐ-CP.
   - `MODE_CDT_SELF_AUDIT` (Biên bản Tự Thẩm định của Chủ Đầu Tư):
     - Quét toàn diện các bộ môn (Arch, KC, MEP, PCCC), đối chiếu đồng thời cả QCVN 04, QCVN 06, TCVN 3890 và TCVN 7568.
     - Tự động sinh **Biên Bản Tự Thẩm Định Thiết Kế PCCC** có bố cục pháp lý hoàn chỉnh theo Nghị định 105/2025.

2. **Cấu Trúc Biên Bản Tự Thẩm Định Pháp Lý (Self-Audit Affidavit Schema):**
   Biên bản được kết xuất tự động gồm 5 thành phần bắt buộc:
   - *Phần 1:* Thông tin dự án, quy mô phân cấp công trình, căn cứ pháp lý áp dụng (Luật 55/2024, NĐ 105/2025).
   - *Phần 2:* Bảng ma trận đối soát $100\%$ các điều khoản quy chuẩn kỹ thuật bắt buộc kèm tọa độ bản vẽ đối chiếu.
   - *Phần 3:* Bảng danh mục sai phạm (`Critical Defect` / `Warning Notice`) kèm khuyến nghị khắc phục.
   - *Phần 4:* Khóa toàn vẹn mật mã học: Mã băm **SHA-256** của bộ bản vẽ thiết kế được kiểm toán và mã băm của bản quy chuẩn hợp nhất tương ứng.
   - *Phần 5:* Khối ký số điện tử (*Digital Signature Block*) dành cho Chủ đầu tư và Đơn vị tư vấn thẩm tra.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Tối ưu hóa thủ tục hành chính:** Tạo ra các bộ hồ sơ độc lập, sạch sẽ, trúng thẩm quyền của từng cơ quan quản lý nhà nước.
- **Giá trị pháp lý hoàn chỉnh cho Chủ đầu tư:** Cung cấp tài liệu tự thẩm định có giá trị giải trình pháp lý cao, có thể lưu trữ vĩnh viễn trong Hồ sơ Hoàn công.

### Đánh đổi:
- Cần duy trì bộ template biểu mẫu Markdown/Word/PDF động tương thích với các biểu mẫu mới ban hành của Nghị định 105/2025/NĐ-CP.
