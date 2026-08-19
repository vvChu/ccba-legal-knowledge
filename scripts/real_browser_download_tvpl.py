"""Download authentic QCVN 04 .doc/.docx from TVPL using real visible Chrome browser."""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
TARGET_DIR = ROOT_DIR / ".md" / "extracted_docs" / "qcvn_04_2021_bxd"
TARGET_DIR.mkdir(parents=True, exist_ok=True)

URL_DOC = "https://thuvienphapluat.vn/van-ban/Xay-dung-Nha-o/Thong-tu-03-2021-TT-BXD-Quy-chuan-ky-thuat-quoc-gia-ve-Nha-chung-cu-475266.aspx"

def run():
    print("=================================================================")
    print("   KHỞI ĐỘNG TRÌNH DUYỆT THẬT (NON-HEADLESS) TẢI FILE TỪ TVPL   ")
    print("=================================================================")

    with sync_playwright() as p:
        # Check for installed Chrome
        chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        launch_kwargs = {
            "headless": False,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ],
        }
        if Path(chrome_exe).exists():
            launch_kwargs["executable_path"] = chrome_exe
            print(f"[Browser] Sử dụng Google Chrome thật: {chrome_exe}")
        else:
            print("[Browser] Sử dụng Chromium bundled...")

        browser = p.chromium.launch(**launch_kwargs)
        context = browser.new_context(
            accept_downloads=True,
            no_viewport=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        )
        page = context.new_page()

        print("[1/4] Đang mở trang đăng nhập Thư Viện Pháp Luật...")
        page.goto("https://thuvienphapluat.vn/thanh-vien/dang-nhap.aspx", wait_until="domcontentloaded")
        time.sleep(3)

        # Handle Cloudflare if present on login
        if "Just a moment" in page.title():
            print("[Cloudflare] Phát hiện màn hình xác thực Cloudflare trên trang đăng nhập...")
            print("[Cloudflare] Đang chờ xác thực tự động hoặc người dùng tương tác (tối đa 25s)...")
            for _ in range(25):
                if "Just a moment" not in page.title():
                    print("[Cloudflare] ✅ Đã vượt qua Cloudflare!")
                    break
                time.sleep(1)

        # Login VIP
        if page.query_selector("input[name='txtDangNhap']"):
            print("[2/4] Điền thông tin tài khoản VIP...")
            page.fill("input[name='txtDangNhap']", "vuvanchu119")
            page.fill("input[name='txtMatKhau']", "Chu@123456")
            page.click("#btDangNhap, input[type='submit']")
            time.sleep(4)

        print(f"[3/4] Điều hướng tới trang văn bản: {URL_DOC}")
        page.goto(URL_DOC, wait_until="domcontentloaded")
        time.sleep(4)

        # Handle Cloudflare on doc page
        if "Just a moment" in page.title():
            print("[Cloudflare] Phát hiện Cloudflare trên trang văn bản...")
            print("[Cloudflare] Đang chờ vượt qua Cloudflare (tối đa 30s)...")
            for _ in range(30):
                if "Just a moment" not in page.title():
                    print("[Cloudflare] ✅ Đã vào được trang văn bản!")
                    break
                time.sleep(1)

        print(f"[Page Status] Tiêu đề trang hiện tại: '{page.title()}'")

        # Click Tab Tải về (tab=1)
        print("[4/4] Đang tìm kiếm nút tải về...")
        tab_download = page.query_selector("a#aTaiVe, a[href*='tab=1'], #tabTaiVe, a:has-text('Tải về')")
        if tab_download:
            print(f"[Action] Bấm vào Tab Tải về: '{tab_download.inner_text().strip()}'")
            tab_download.click()
            time.sleep(3)
        else:
            print("[Action] Điều hướng trực tiếp sang tab=1...")
            page.goto(URL_DOC + "?tab=1", wait_until="domcontentloaded")
            time.sleep(3)

        # Scan for download links
        download_targets = []
        for a in page.query_selector_all("a"):
            t = a.inner_text().strip().lower()
            h = (a.get_attribute("href") or "").lower()
            onclick = (a.get_attribute("onclick") or "").lower()
            if any(k in t or k in h or k in onclick for k in ["tải", "doc", "docx", "tiếng việt", "download"]):
                download_targets.append(a)
                print(f"  -> Link tải tìm thấy: text='{a.inner_text().strip()}' | href='{a.get_attribute('href')}'")

        # Trigger download on best candidate
        saved = False
        for btn in download_targets:
            btn_text = btn.inner_text().strip()
            if "pdf" in btn_text.lower():
                continue
            print(f"[Download] Đang kích hoạt tải về trên nút: '{btn_text}'...")
            try:
                with page.expect_download(timeout=15000) as d_info:
                    btn.click()
                download = d_info.value
                orig_filename = download.suggested_filename
                ext = Path(orig_filename).suffix or ".doc"
                dest_path = TARGET_DIR / f"qcvn_04_2021_bxd_official{ext}"
                download.save_as(str(dest_path))
                print(f"\n🎉 [THÀNH CÔNG RỰC RỠ] Đã tải tệp gốc chính thức từ TVPL:")
                print(f"   -> Đường dẫn: {dest_path}")
                print(f"   -> Dung lượng: {dest_path.stat().st_size:,} bytes")
                print(f"   -> Tên file gốc: {orig_filename}")
                saved = True
                break
            except Exception as e:
                print(f"   ❌ Thử nút này chưa kích hoạt được: {e}")

        if not saved:
            print("[Warning] Chưa bắt được sự kiện tải tự động. Giữ trình duyệt thêm 15s để xem xét...")
            time.sleep(15)

        browser.close()
        return saved

if __name__ == "__main__":
    run()
