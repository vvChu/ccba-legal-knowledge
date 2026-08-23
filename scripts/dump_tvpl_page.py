import os
from dotenv import load_dotenv
"""Dump TVPL page DOM for Thông tư 03/2021/TT-BXD."""

import re
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

load_dotenv()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def dump_page():
    target_dir = Path("d:/GitHubProjects/ccba-legal-knowledge/.md/extracted_docs/qcvn_04_2021_bxd")
    target_dir.mkdir(parents=True, exist_ok=True)

    url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Nha-o/Thong-tu-03-2021-TT-BXD-Quy-chuan-ky-thuat-quoc-gia-ve-Nha-chung-cu-475266.aspx"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("[Playwright] Logging in...")
        page.goto("https://thuvienphapluat.vn/thanh-vien/dang-nhap.aspx", wait_until="domcontentloaded")
        time.sleep(2)

        if page.query_selector("input[name='txtDangNhap']"):
            page.fill("input[name='txtDangNhap']", os.getenv("TVPL_USERNAME", ""))
            page.fill("input[name='txtMatKhau']", os.getenv("TVPL_PASSWORD", ""))
            page.click("#btDangNhap, input[type='submit']")
            time.sleep(3)

        print(f"[Playwright] Visiting {url}...")
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(4)

        html = page.content()
        (target_dir / "page_full.html").write_text(html, encoding="utf-8")
        print(f"Dumped full HTML: {len(html)} bytes to page_full.html")

        # Let's find main text elements
        # Print all div IDs
        div_ids = [d.get_attribute("id") for d in page.query_selector_all("div") if d.get_attribute("id")]
        print("Div IDs on page (first 30):", div_ids[:30])

        # Find all a tags
        a_list = []
        for a in page.query_selector_all("a"):
            t = a.inner_text().strip()
            h = a.get_attribute("href") or ""
            if t or h:
                a_list.append(f"Text: {t[:40]} | Href: {h}")
        print(f"Total links: {len(a_list)}")
        (target_dir / "links.txt").write_text("\n".join(a_list), encoding="utf-8")

        browser.close()

if __name__ == "__main__":
    dump_page()
