# ADR 0030: Visual Parity & 2D Annex Navigation Matrix for Large Standards

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-08-23)

## 2. Bối Cảnh (Context)
Các quy chuẩn lớn như QCVN 02:2022/BXD (Số liệu điều kiện tự nhiên dùng trong xây dựng) chứa hàng trăm bảng số liệu khí hậu theo 63 tỉnh thành. Việc tra cứu qua lại giữa mục lục chính và các bảng số liệu rất khó khăn nếu không có cấu trúc điều hướng 2 chiều.

## 3. Quyết Định Thiết Kế (Decision)
1. **Bảng Điều Hướng Phụ Lục 2D (2D Navigation Matrix):**
   - Xây dựng ma trận liên kết đa chiều tại `index.md` và đầu mỗi phụ lục, liên kết trực tiếp giữa Tỉnh/Thành $\leftrightarrow$ Trạm Khí Tượng $\leftrightarrow$ Bảng Số Liệu.
2. **Tách Chú Thích Ra Khỏi Ô Bảng (Table Footnote Isolation):**
   - Chú thích chân bảng được đưa ra ngoài khung bảng Markdown (dưới dạng Blockquote hoặc danh sách chú thích) để tránh làm vỡ layout bảng.
3. **Cổng Kiểm Định Thị Giác (Visual Parity Gate):**
   - Khóa bắt buộc trong CI Spoke đảm bảo $0$ lỗi layout và $100\%$ liên kết nội bộ hợp lệ.

## 4. Hệ Quả (Consequences)
- Người dùng và AI Agent có thể định vị và tra cứu bảng số liệu bất kỳ chỉ trong 1 bước nhảy (1-hop retrieval).
