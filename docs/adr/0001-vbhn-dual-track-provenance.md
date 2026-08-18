# ADR 0001: Chiến lược Quản lý Văn bản Hợp nhất (VBHN) Dual-Track Provenance cho RAG & Thẩm tra Thiết kế

- **Trạng thái:** `Accepted`
- **Ngày quyết định:** 2026-08-18
- **Tác giả:** CCBA Core Engineering Team
- **Phạm vi:** Toàn bộ Spoke `ccba-legal-knowledge`

---

## 1. Ngữ cảnh & Vấn đề (Context & Problem Statement)

Khi văn bản quy chuẩn hoặc luật được sửa đổi bổ sung (như Thông tư 09/2023/TT-BXD sửa đổi QCVN 06:2022/BXD, hay Thông tư 31/2026 sửa đổi QCVN 04:2021/BXD), hệ thống cơ sở tri thức đứng trước 2 nhu cầu kỹ thuật mâu thuẫn:
1. **Yêu cầu Fast-RAG & Automation QC:** AI Agent cần tra cứu một văn bản thống nhất, duy nhất, cập nhật mới nhất để đối soát hồ sơ thiết kế công trình với độ trễ thấp nhất và không bị hallucination do phải tự chắp vá các văn bản sửa đổi rời rạc tại runtime.
2. **Yêu cầu Truy nguyên Pháp lý (Legal Provenance):** Chuyên gia pháp lý và kiểm toán viên cần đối chiếu chính xác nguyên văn từng văn bản ban hành độc lập theo đúng thời điểm hiệu lực pháp lý (Point-in-Time).

---

## 2. Các Phương án Đã Xem xét (Considered Options)

- **Option A (Được chọn): Mô hình Dual-Track (Provenance + Pre-Consolidated VBHN).**  
  Tạo sẵn tệp Văn bản Hợp nhất (`*_hop_nhat_*.md`) nhúng trực tiếp các điểm sửa đổi vào thân văn bản kèm callout cảnh báo `> [!NOTE] Sửa đổi`, đồng thời duy trì song song 2 tệp văn bản gốc và văn bản sửa đổi độc lập. `index.md` ưu tiên trỏ VBHN cho RAG.
- **Option B: Pure Map-Reduce Runtime.**  
  Chỉ lưu tệp gốc và tệp sửa đổi, bắt buộc AI Agent tự đọc `clauses_sd1.json` và ghép nối văn bản khi truy vấn. *(Bị loại vì tăng token cost, tăng latency và dễ phát sinh lỗi logic khi ghép nhiều sửa đổi)*.
- **Option C: In-Place Overwrite.**  
  Ghi đè trực tiếp sửa đổi vào văn bản gốc và xóa bỏ tệp sửa đổi. *(Bị loại vì làm mất tính toàn vẹn lịch sử ban hành của văn bản pháp quy)*.

---

## 3. Quyết định (Decision)

Áp dụng **Option A (Dual-Track Provenance)** cho toàn bộ các gói OKF Bundle trong Spoke:
1. Mỗi gói tài liệu có sửa đổi bổ sung sẽ có 3 tệp cốt lõi:
   - `[doc_slug].md`: Văn bản gốc ban đầu.
   - `sua_doi_[N]_[year]_[doc_slug].md`: Văn bản sửa đổi độc lập kèm cây AST `clauses_sd[N].json`.
   - `[doc_slug]_hop_nhat_[year].md`: Văn bản Hợp nhất cập nhật mới nhất.
2. Tệp `index.md` (Map of Content) đóng vai trò Router chỉ dẫn rõ ràng cho người dùng và Agent.

---

## 4. Hệ quả & Đánh đổi (Consequences & Trade-offs)

### Tích cực:
- **Tốc độ RAG tối đa:** AI Agent truy vấn thẳng vào 1 tệp Markdown hợp nhất hoàn chỉnh.
- **Bảo toàn 100% Provenance:** Không làm mất mát hay sai lệch bất kỳ chữ nào trong các văn bản gốc ban hành.
- **Tính minh bạch cao:** Các đoạn sửa đổi trong VBHN đều có nhãn dẫn xuất nguồn gốc rõ ràng.

### Đánh đổi (Negative/Effort):
- Spoke cần duy trì script tạo và kiểm toán VBHN tự động để đảm bảo tính đồng bộ tuyệt đối khi có sửa đổi mới.
