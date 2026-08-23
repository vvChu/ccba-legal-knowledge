"""Download official .docx document from Thư viện Pháp luật."""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

_TVPL_USERNAME = os.getenv("TVPL_USERNAME")
_TVPL_PASSWORD = os.getenv("TVPL_PASSWORD")

def download_qcvn_docx(url: str, output_path: Path) -> bool:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print(f"[Crawler] Navigating to URL: {url}")
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(3)

        # Check for TVPL login button or download links
        download_btn = page.query_selector("a[href*='download'], a[href*='Tai-ve'], a[href*='.doc']")
        if not download_btn:
            print("[Crawler] Looking for login button...")
            login_btn = page.query_selector("a[href*='dang-nhap'], .btn-login")
            if login_btn:
                login_btn.click()
                time.sleep(2)
                if not _TVPL_USERNAME or not _TVPL_PASSWORD:
                    print("[Error] TVPL_USERNAME or TVPL_PASSWORD not set in .env")
                    browser.close()
                    return False
                page.fill("input[name='txtDangNhap'], input[type='text']", _TVPL_USERNAME)
                page.fill("input[name='txtMatKhau'], input[type='password']", _TVPL_PASSWORD)
                page.click("button[type='submit'], input[type='submit']")
                time.sleep(3)
                page.goto(url)

        # Trigger download
        download_elem = page.query_selector("a[href*='download'], a[href*='Tai-ve'], a[href*='.doc']")
        if download_elem:
            with page.expect_download() as download_info:
                download_elem.click()
            download = download_info.value
            download.save_as(str(output_path))
            print(f"[Success] Saved .docx to: {output_path} ({output_path.stat().st_size} bytes)")
            browser.close()
            return True
        else:
            print("[Error] Could not find download button on page.")
            browser.close()
            return False

if __name__ == "__main__":
    url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Nha-o/Thong-tu-06-2022-TT-BXD-Quy-chuan-ky-thuat-quoc-gia-an-toan-chay-cho-nha-va-cong-trinh-545609.aspx"
    target = Path(".md/extracted_docs/qcvn_06_2022_bxd/qcvn_06_2022_bxd.docx")
    download_qcvn_docx(url, target)
