import os
from dotenv import load_dotenv
"""Fetch QCVN 06 .docx directly and save to target directory."""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")

def fetch_docx():
    target_dir = Path("d:/GitHubProjects/ccba-legal-knowledge/.md/extracted_docs/qcvn_06_2022_bxd")
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "qcvn_06_2022_bxd.docx"

    url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Nha-o/Thong-tu-06-2022-TT-BXD-Quy-chuan-ky-thuat-quoc-gia-an-toan-chay-cho-nha-va-cong-trinh-545609.aspx"

    with sync_playwright() as p:
        print("[Playwright] Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("[Playwright] Logging into Thu vien Phap luat...")
        page.goto("https://thuvienphapluat.vn/thanh-vien/dang-nhap.aspx", wait_until="domcontentloaded")
        time.sleep(2)

        if page.query_selector("input[name='txtDangNhap']"):
            page.fill("input[name='txtDangNhap']", os.getenv("TVPL_USERNAME", ""))
            page.fill("input[name='txtMatKhau']", os.getenv("TVPL_PASSWORD", ""))
            page.click("input[type='submit'], button[type='submit'], #btDangNhap")
            time.sleep(3)

        print(f"[Playwright] Navigating to {url}")
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(3)

        print("--- ALL LINKS ON PAGE ---")
        for a in page.query_selector_all("a"):
            text = a.inner_text().strip()
            href = a.get_attribute("href") or ""
            if any(k in text.lower() or k in href.lower() for k in ["tải", "doc", "download", "tai"]):
                print(f"TEXT: {text} | HREF: {href}")

        browser.close()

if __name__ == "__main__":
    fetch_docx()
