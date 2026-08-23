import os
from dotenv import load_dotenv
"""Inspect TVPL logged in page for 03/2021/TT-BXD."""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

load_dotenv()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect():
    url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Nha-o/Thong-tu-03-2021-TT-BXD-Quy-chuan-ky-thuat-quoc-gia-ve-Nha-chung-cu-475266.aspx"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("Navigating to login...")
        page.goto("https://thuvienphapluat.vn/thanh-vien/dang-nhap.aspx", wait_until="domcontentloaded")
        time.sleep(2)

        if page.query_selector("input[name='txtDangNhap']"):
            page.fill("input[name='txtDangNhap']", os.getenv("TVPL_USERNAME", ""))
            page.fill("input[name='txtMatKhau']", os.getenv("TVPL_PASSWORD", ""))
            page.click("#btDangNhap, input[type='submit']")
            time.sleep(3)

        print(f"Navigating to {url}...")
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(3)

        print(f"Current page title: {page.title()}")
        print(f"Current page URL: {page.url}")

        # List all anchors on page
        anchors = page.query_selector_all("a")
        print(f"Total anchors found: {len(anchors)}")
        for idx, a in enumerate(anchors):
            t = a.inner_text().strip()
            h = a.get_attribute("href") or ""
            c = a.get_attribute("class") or ""
            if any(k in t.lower() or k in h.lower() for k in ["tải", "tai", "doc", "bản", "view", "nội dung", "toàn văn", "in"]):
                print(f"[{idx}] Text='{t}' | Href='{h}' | Class='{c}'")

        browser.close()

if __name__ == "__main__":
    inspect()
