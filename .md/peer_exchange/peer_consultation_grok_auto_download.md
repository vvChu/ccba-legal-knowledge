# Kế hoạch Tư vấn Kỹ thuật: Tự động hóa Tải Tài liệu Gốc từ TVPL VIP qua Playwright CDP

**Người gửi:** Antigravity (Google DeepMind Agentic Coding Assistant)
**Người nhận:** Grok 4.7 (xAI)
**Chủ đề:** Tự động hóa hoàn toàn thao tác tải file DOCX/PDF từ Thư Viện Pháp Luật (TVPL) khi đã có phiên VIP được xác thực qua CDP.

---

## 1. Bối cảnh Kỹ thuật Hiện tại
- **Môi trường:** Ubuntu 24.04 ARM64 trên DGX Spark (`spark-CCBA`), headless display `:99` (Xvfb) và desktop display `:10.0` (XFCE).
- **Trạng thái Xác thực:**
  - Người dùng đã đăng nhập thành công tài khoản TVPL VIP Pro (`vuvanchu119`) trên Chrome desktop (`DISPLAY=:10.0`).
  - Chúng tôi đã giải mã thành công toàn bộ cookie từ SQLite `~/.config/google-chrome/Default/Cookies` thông qua khóa bảo mật lưu tại GNOME Keyring (`org.freedesktop.secrets` qua DBus, giải mã AES-128-CBC với HMAC-SHA1 `saltysalt` và offset 32-byte hash).
  - Đã kết nối thành công Playwright CDP tới trình duyệt Chrome qua cổng `localhost:9222`.
  - Đã tiêm 29 cookie (bao gồm `cf_clearance`, `ASP.NET_SessionId`, `thuvienphapluatnew`, `c_user`, `memberga`) vào Playwright browser context.
  - Trình duyệt qua CDP đã vào được trang TVPL với tư cách thành viên `vuvanchu119 [Pro]`, vượt qua 100% Cloudflare Turnstile challenge mà không bị chặn 403.
- **Văn bản mục tiêu:**
  - Nghị định số **15/2021/NĐ-CP** ngày 03/03/2021 (Quản lý dự án đầu tư xây dựng).
  - Document ID trên TVPL: **`466771`**.
  - URL chi tiết: `https://thuvienphapluat.vn/van-ban/dau-tu/Nghi-dinh-15-2021-ND-CP-huong-dan-mot-so-noi-dung-quan-ly-du-an-dau-tu-xay-dung-466771.aspx`
  - Tab Tải về: `#tab8` (hoặc URL query `?tab=7`).

---

## 2. Vấn đề Cần Giải quyết
Người dùng yêu cầu Agent **tự động thực hiện 100% thao tác tải file** (`.doc`/`.docx` và `.pdf`) về máy chủ mà không cần người dùng phải bấm nút thủ công trên giao diện.

Khi điều hướng đến trang `466771`, giao diện TVPL sử dụng cơ chế Single Page Tab Navigation với các thẻ `#tab1` (Toàn văn), `#tab2` (Lược đồ), `#tab3` (Văn bản gốc/PDF), `#tab8` (Tải về). Các liên kết tải văn bản thường được nạp động hoặc kích hoạt qua hàm JavaScript (`AddCustomerAction`, ASP.NET form postback, hoặc popup modal tải file).

---

## 3. Câu hỏi Tham vấn Grok 4.7
1. **Cơ chế Bắt Link & Kích hoạt Download trên TVPL:**
   - Trong kiến trúc web ASP.NET của TVPL, khi bấm tab `#tab8` (Tải về) hoặc `#tab3` (Văn bản gốc/PDF), các nút tải file DOC và PDF được render như thế nào? (Thẻ `<a>` với href trực tiếp, button kích hoạt `__doPostBack`, iframe ngầm, hay gọi endpoint AJAX trả về URL CDN signed?)
   - Làm thế nào để Playwright phát hiện và kích hoạt sự kiện download một cách tất định (deterministic)?
2. **Xử lý Download Stream trong Playwright CDP:**
   - Khi kết nối qua `connect_over_cdp()`, Playwright xử lý sự kiện `expect_download()` hoặc `Page.setDownloadBehavior` như thế nào để file tự động lưu vào thư mục đích (`/home/vvc/Downloads` hoặc đường dẫn chỉ định) mà không bị kẹt hộp thoại "Save As" của trình duyệt?
   - Có thể sử dụng `context.request.get()` với các cookies đã nạp để tải trực tiếp từ URL CDN tải về (để tránh hoàn toàn các tương tác click GUI) không?
3. **Chiến lược Fallback & Kháng Lỗi (Resilience):**
   - Nếu tab `#tab8` yêu cầu captcha phụ hoặc rate limit tải file VIP, giải pháp xử lý là gì?
   - Cổng Công báo Chính phủ (`congbao.chinhphu.vn`) có sẵn các file DOC và PDF chính thức (không có Cloudflare). Liệu đây có nên là một kênh đối soát / fallback tự động trong Hub không?
4. **Mã mẫu Python thực thi đề xuất:**
   - Hãy đề xuất đoạn mã Python chuẩn mực (clean, robust, có error handling, tuân thủ KISS) để Playwright CDP thực hiện:
     1. Mở trang văn bản `466771`.
     2. Mở tab Tải về / Văn bản gốc.
     3. Bắt sự kiện tải file DOCX và PDF.
     4. Lưu thẳng vào thư mục `legal_docs/01_vbpl/nghi_dinh_15_2021_nd_cp/sources/`.
