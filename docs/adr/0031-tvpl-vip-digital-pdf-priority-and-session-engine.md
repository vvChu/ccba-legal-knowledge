# ADR 0031: TVPL VIP Digital Vector PDF Priority & Persistent Session Engine

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-08-24)

## 2. Bối Cảnh (Context)
Các tài liệu quy chuẩn kỹ thuật và thông tư quy mô lớn khi tải từ TVPL qua các luồng thông thường chỉ nhận được bản Scan Công báo rút gọn (thiếu phụ lục và bảng biểu). Ngoài ra, cơ chế bảo vệ của TVPL dễ khiến tài khoản bot bị rớt phiên VIP.

## 3. Quyết Định Thiết Kế (Decision)
1. **Thứ Tự Ưu Tiên 3 Tầng Tải Tệp:**
   - **Tier 1 — VIP Digital Vector Searchable PDF (`part=-100` / `#ctl00_Content_ThongTinVB_filePDFHyperLink`):** Mỏ neo pháp lý tối thượng đầy đủ 100% nội dung và phụ lục.
   - **Tier 2 — VIP OpenXML Word Document (`part=-1&docx=1` / `#ctl00_Content_ThongTinVB_vietnameseHyperLink_Docx`):** Nguồn nạp để chuyển đổi sang OKF v2.2 Markdown.
   - **Tier 3 — Gazette Scan PDF (`part=0` / `#ctl00_Content_ThongTinVB_pdfHyperLink`):** Fallback dự phòng.
2. **Persistent Chromium VIP Profile Session Engine:**
   - Profile độc lập tại `~/.gemini/antigravity/chrome_vip` và lệnh `python -m ccba_legal login`.
3. **Guard Lọc Thời Gian Tải (`start_time`):**
   - Chỉ nhận tệp có thời gian sửa đổi sau thời điểm bấm nút tải, chống nhận nhầm file cũ trong `~/Downloads`.

## 4. Hệ Quả (Consequences)
- Đạt $100\%$ đối soát SHA-256 trên toàn bộ 29/29 văn bản kho tri thức.
