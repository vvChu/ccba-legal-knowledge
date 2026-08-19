"""Download official QCVN 06:2022/BXD .docx file from Thư viện Pháp luật."""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def download_qcvn_docx() -> bool:
    target_dir = Path(".md/extracted_docs/qcvn_06_2022_bxd")
    target_dir.mkdir(parents=True, exist_ok=True)
    dest_file = target_dir / "qcvn_06_2022_bxd.docx"

    url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Nha-o/Thong-tu-06-2022-TT-BXD-Quy-chuan-ky-thuat-quoc-gia-an-toan-chay-cho-nha-va-cong-trinh-545609.aspx"

    with sync_playwright() as p:
        print("[Crawler] Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("[Crawler] Logging in as VIP account 'vuvanchu119'...")
        try:
            page.goto("https://thuvienphapluat.vn/thanh-vien/dang-nhap.aspx", wait_until="domcontentloaded")
            time.sleep(2)
            page.fill("input[name='txtDangNhap']", "vuvanchu119")
            page.fill("input[name='txtMatKhau']", "Chu@123456")
            page.click("input[type='submit'], button[type='submit'], #btDangNhap")
            time.sleep(3)
        except Exception as e:
            print(f"[Warning] Login exception: {e}")

        # Navigate to document download page tab
        print(f"[Crawler] Navigating to {url}")
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(3)

        # Look for doc/docx download link specifically
        download_link = None
        for a in page.query_selector_all("a"):
            text = a.inner_text().strip()
            href = a.get_attribute("href") or ""
            if ("docx" in text.lower() or "doc" in text.lower() or "tiếng việt" in text.lower()) and "pdf" not in text.lower():
                download_link = a
                print(f"[Found Link] Text: {text} | Href: {href}")
                break

        if not download_link:
            # Fallback to any download link
            download_link = page.query_selector("a[href*='download'], a[href*='Tai-ve']")

        if download_link:
            print("[Action] Clicking download link...")
            with page.expect_download() as download_info:
                download_link.click()
            download = download_info.value
            
            # Save specifically with extension .docx
            ext = ".docx" if "doc" in download.suggested_filename.lower() else Path(download.suggested_filename).suffix
            final_path = target_dir / f"qcvn_06_2022_bxd{ext}"
            download.save_as(str(final_path))
            print(f"[Success] Downloaded official document file: {final_path} ({final_path.stat().st_size} bytes)")
            browser.close()
            return True
        else:
            print("[Error] Download link not found on page.")
            browser.close()
            return False

if __name__ == "__main__":
    download_qcvn_docx()
