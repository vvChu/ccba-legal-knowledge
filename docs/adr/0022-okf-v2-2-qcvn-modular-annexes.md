# ADR 0022: OKF v2.2 QCVN Modular Technical Annexes & Active Core Pattern

* **Trạng thái:** Đã phê duyệt (Approved)
* **Ngày quyết định:** 2026-08-20
* **Tác giả:** Antigravity AI Agent & CCBA Legal Knowledge Lead
* **Phạm vi áp dụng:** Toàn bộ Quy chuẩn Kỹ thuật Quốc gia (QCVN) và Tiêu chuẩn Quốc gia (TCVN) trong CCBA Agent Platform.

---

## 1. Bối cảnh & Vấn đề (Context & Problem Statement)

Trong các phiên bản OKF trước đây, các văn bản Quy chuẩn Kỹ thuật đồ sộ (tiêu biểu là **QCVN 06:2022/BXD** với hơn 5.700 dòng Markdown, 64 bảng biểu phức tạp và 9 Phụ lục từ A đến I) được lưu trữ dưới dạng **tệp đơn khối (Monolithic Markdown)**. 

Khi các AI Agent tương tác thực tế với kho tri thức:
1. **Ô Nhiễm Ngữ Cảnh (Context Dilution / Lost in the Middle):** Khi Agent chỉ cần thẩm tra một điều khoản hẹp (ví dụ: *Khoảng cách thoát nạn* ở Phụ lục G hoặc *Hút khói* ở Phụ lục D), việc phải nạp cả tệp 5.700 dòng làm lãng phí $> 80\%$ token và làm giảm độ tập trung của LLM.
2. **Rủi Ro Trích Dẫn Sai Văn Bản:** Việc lưu song song bản gốc 2022 và các bản sửa đổi tại thư mục gốc khiến Agent có nguy cơ đọc nhầm vào các điều khoản cũ đã hết hiệu lực.
3. **Phụ Lục Kỹ Thuật Đồ Sộ Thiếu Tính Module Hóa:** Các phụ lục trong QCVN mang tính chất quy chuẩn chuyên ngành độc lập cao cần được tách thành các module chuyên biệt để phục vụ các Agent thẩm định chuyên môn.

---

## 2. Quyết Định Kiến Trúc (Architectural Decisions)

Hệ thống chính thức ban hành tiêu chuẩn **OKF v2.2 Technical Standards Pattern** với 4 quy tắc bất biến:

### Nguyên tắc 1: Active Consolidated Core là Tệp Cửa Ngõ Gốc (Root Gateway)
* Tệp `qcvn_XX_YYYY_bxd.md` tại thư mục gốc của bundle luôn là **Bản Hợp Nhất Đang Có Hiệu Lực Thi Hành** (chỉ chứa Chương 1 đến Chương cuối cùng, kết thúc bằng Mục Lục điều hướng sang `annexes/` và `tables/`).
* Tuyệt đối không để bản cũ hoặc bản sửa đổi lẻ tẻ ở thư mục gốc.

### Nguyên tắc 2: Phân Rã Phụ Lục Kỹ Thuật Chuyên Đề Nguyên Tử (`annexes/`)
* Toàn bộ các Phụ lục quy chuẩn (Phụ lục A, B, C...) được bóc tách thành từng tệp Markdown độc lập tại thư mục `annexes/`:
  * `annexes/phu_luc_a_quy_dinh_bo_sung_nhom_nha_cu_the.md`
  * `annexes/phu_luc_d_bao_ve_chong_khoi.md`
  * `annexes/phu_luc_g_khoang_cach_va_chieu_rong_thoat_nan.md`
* Mỗi tệp Phụ lục có Frontmatter đầy đủ, giữ nguyên các thẻ neo `<a id="...">` để liên kết chéo hai chiều (Bidirectional Linking).

### Nguyên tắc 3: Gom Gọn Dữ Liệu Lịch Sử & Tài Liệu Nguồn (`sources/`)
* Mọi tệp văn bản cũ trước hợp nhất (`*_goc_*.md`), tệp thông tư sửa đổi (`sua_doi_*.md`), và các tệp `.pdf` gốc được lưu trữ tập trung tại thư mục `sources/`.

### Nguyên tắc 4: Cây AST Hợp Nhất 100% Hiện Hành (`clauses.json`)
* Cây AST `clauses.json` tại Root đại diện cho toàn bộ các điều khoản của **Cả Core và Annexes** sau khi đã áp dụng các sửa đổi, có phân định thẩm quyền (`CQXD` vs `CONG_AN`) và ngày hết hạn ân hạn (`grace_period_end`).

---

## 3. Hệ Quả & Lợi Ích (Consequences & Benefits)

* **Tối Ưu Hóa Context Window:** Agent thẩm tra chuyên ngành chỉ cần nạp tệp phụ lục tương ứng ($100 - 600$ dòng), tiết kiệm $> 80\%$ token cho mỗi lượt gọi LLM.
* **Triệt Tiêu Hoàn Toàn Ảo Giác Trích Dẫn Cũ:** Agent luôn đọc bản có hiệu lực cao nhất tại file gốc.
* **Tra Cứu Bảng Biểu Số Hóa:** 100% bảng biểu kỹ thuật được truy cập qua `tables/csv/` và `tables/json/`.
* **Zero Broken Links:** Cổng CI `verify_cross_links.py` đảm bảo toàn bộ liên kết nội bộ và liên kết chéo giữa Core và Annexes đều chính xác $100\%$.
