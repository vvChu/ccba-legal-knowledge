# Yêu cầu Peer Review Kỹ thuật Độc lập (Grok 4.7)

Xin chào Grok! Bạn đang tham gia phiên Peer Review kiến trúc chuyên sâu với tư cách Senior Principal Infrastructure & Crawling Architect cho hệ sinh thái **CCBA Agent Services Platform**.

Hãy xem xét và phản biện kế hoạch kỹ thuật **P1: Nâng Cấp Độ Ổn Định Cho TVPL VIP Crawler & Pipeline Legal Ingest** dưới đây:

---

## 📄 Nội dung Kế hoạch Đề xuất (Implementation Plan P1):

### 1. Mục tiêu & Bối cảnh
- **Mục tiêu:** Nâng cấp độ tin cậy của crawler TVPL VIP từ bán tự động (phụ thuộc mở trước trình duyệt) lên tự trị 100% (Zero-Touch Autonomy) trên cả Linux server và Windows.
- **Thực tế đã chứng minh:** Khi phiên Chrome CDP cổng 9222 có cookie sống (`cf_clearance`, VIP cookies), crawler tải thành công 100% file DOCX (547KB) và Vector PDF (68MB) của Nghị định 15/2021/NĐ-CP, convert sang OKF v2.4 Bundle với 541 điều khoản, 23 biểu mẫu nguyên tử, 39 bảng số liệu, pass 15 Cổng Master CI Gate.
- **Điểm nghẽn:** Khi khởi động lạnh (Cold Start) hoặc cookie hết hạn, crawler tự động điền form login web. Trên Linux headless/Xvfb, Cloudflare Turnstile phát hiện bot môi trường -> kẹt captcha -> ngắt pipeline. Giải pháp đã thực hiện thủ công là giải mã cookie từ Google Chrome Desktop SQLite DB qua D-Bus/GNOME Keyring rồi tiêm vào CDP. Nay cần đóng gói chính thức vào Hub package `ccba-legal-intel`.

### 2. Các thành phần giải pháp kỹ thuật đề xuất:
1. **Auto-Cookie Sync Bridge (`CookieVault.sync_from_system_chrome`)**:
   - Tự động phát hiện OS (Linux/Windows).
   - Trên Linux: Dùng D-Bus kết nối `org.freedesktop.Secret.Service` để lấy khóa mã hóa `Chrome Safe Storage` (fallback về `b"peanuts"`).
   - Trên Windows: Dùng DPAPI `CryptUnprotectData` hoặc giải mã AES-GCM với `os_crypt.encrypted_key` từ `Local State`.
   - Sao chép an toàn tệp `Cookies` SQLite sang `/tmp` để tránh file lock (`database is locked`).
   - Truy vấn `WHERE host_key LIKE '%thuvienphapluat%'`.
   - Giải mã `encrypted_value`: PBKDF2 HMAC SHA1 (salt `saltysalt`, 1 iteration, 16 bytes key), AES-128-CBC, unpad PKCS7, bỏ 32-byte header v11.
   - Lưu cookie sạch vào `cookies.json` của `CookieVault`.
2. **CDP Stealth & Anti-Bot Evasion**:
   - Thêm cờ Chromium: `--disable-blink-features=AutomationControlled`, `--no-first-run`, `--no-default-browser-check`.
   - Tiêm script qua `Page.addScriptToEvaluateOnNewDocument`: Xóa `navigator.webdriver`, giả lập `window.chrome.runtime`.
   - Tiêm cookies từ CookieVault vào CDP session qua `Network.setCookie`.
3. **Chuỗi Dự phòng 3 Nấc (Graceful Fallback Chain)**:
   - Nấc 1: TVPL VIP qua Chrome CDP với Cookie Vault đã đồng bộ (DOCX Gold + Vector PDF).
   - Nấc 2: TVPL VIP Login qua Web Form nếu không tìm thấy Chrome Desktop profile (áp dụng CDP Stealth Evasion).
   - Nấc 3: Tự động chuyển hướng tải từ Cổng Công Báo Chính Phủ (`congbao.chinhphu.vn`) nếu Nấc 1 và 2 bị Cloudflare chặn cứng.
4. **Kiểm định & An toàn**:
   - Thao tác read-only trên bản copy `/tmp`, không ghi đè profile người dùng.
   - Viết unit tests kiểm thử mock SQLite giải mã, timeout fallback.

---

## 🎯 Yêu cầu Phản biện Chuyên gia (Peer Review Prompts):
Dưới góc độ chuyên gia hệ thống cào dữ liệu và bảo mật trình duyệt, hãy đánh giá:
1. **Tính khả thi & Độ bền vững (Feasibility & Robustness):** Giải pháp Auto-Cookie Sync Bridge trích xuất từ Chrome Desktop SQLite DB + OS Keystore có những ưu điểm gì? Liệu có rủi ro gì khi Chrome nâng cấp phiên bản (ví dụ v120+ hoặc App-Bound Encryption trên Windows/Linux)?
2. **Bảo mật & Tránh xung đột (Security & Concurrency):** Việc copy file DB sang `/tmp` và dùng D-Bus Secret Service đã đủ an toàn và tránh SQLite lock chưa? Cần thêm biện pháp phòng ngừa nào (ví dụ permissions `0600`, dọn dẹp file tạm trong `try...finally`)?
3. **Hiệu quả Bypass Cloudflare:** Việc tiêm `cf_clearance` + cookies VIP vào CDP session kết hợp stealth scripts có thực sự giải quyết triệt để vấn đề Turnstile ở Cold Start trên Linux headless không?
4. **Kiến trúc Fallback T3:** Đánh giá phương án dự phòng sang Cổng Công Báo (`congbao.chinhphu.vn`).
5. **Góp ý cải tiến bổ sung (Actionable Recommendations):** Những điều chỉnh cụ thể nào nên được bổ sung ngay vào Implementation Plan trước khi tiến hành code?

Vui lòng trả lời bằng tiếng Việt, phân tích kỹ thuật sâu sắc, sắc bén, khách quan và mang tính xây dựng cao.
