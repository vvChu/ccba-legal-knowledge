"""Direct download script for QCVN 06 docx."""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

def download_now():
    target_dir = Path("d:/GitHubProjects/ccba-legal-knowledge/.md/extracted_docs/qcvn_06_2022_bxd")
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "qcvn_06_2022_bxd.docx"

    url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Nha-o/Thong-tu-06-2022-TT-BXD-Quy-chuan-ky-thuat-quoc-gia-an-toan-chay-cho-nha-va-cong-trinh-545609.aspx"

    with sync_playwright() as p:
        print("[Playwright] Launching Chromium...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("[Playwright] Logging into Thư viện Pháp luật...")
        page.goto("https://thuvienphapluat.vn/thanh-vien/dang-nhap.aspx", wait_until="domcontentloaded")
        time.sleep(2)

        if page.query_selector("input[name='txtDangNhap']"):
            page.fill("input[name='txtDangNhap']", "vuvanchu119")
            page.fill("input[name='txtMatKhau']", "Chu@123456")
            page.click("#btDangNhap, input[type='submit']")
            time.sleep(3)

        print(f"[Playwright] Navigating to document page: {url}")
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(3)

        # Click Tab Tải về (tab=1)
        print("[Playwright] Navigating to Download Tab...")
        page.goto(url + "?tab=1", wait_until="domcontentloaded")
        time.sleep(3)

        # Look for docx link
        docx_btn = page.query_selector("a[href*='.doc'], a[href*='docx'], a[href*='download']")
        if not docx_btn:
            for a in page.query_selector_all("a"):
                t = a.inner_text().strip()
                if "tiếng việt" in t.lower() or "docx" in t.lower() or "tải" in t.lower():
                    docx_btn = a
                    break

        if docx_btn:
            print(f"[Playwright] Found download button: {docx_btn.inner_text()}")
            with page.expect_download() as download_info:
                docx_btn.click()
            download = download_info.value
            download.save_as(str(target_file))
            print(f"[SUCCESS] Downloaded and saved file to: {target_file.resolve()} ({target_file.stat().st_size} bytes)")
            browser.close()
            return True
        else:
            print("[ERROR] Could not find download button on tab=1")
            browser.close()
            return False

if __name__ == "__main__":
    download_now()
