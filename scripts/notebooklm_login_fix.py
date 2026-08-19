"""
CCBA Platform — Script Đăng Nhập Google NotebookLM Vượt Rào Chắn Bot Detection.
Sử dụng Google Chrome thật với cờ loại bỏ Automation Flags để Google không chặn 'Browser not secure'.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STORAGE_PATH = Path.home() / ".notebooklm" / "profiles" / "default" / "storage_state.json"
PROFILE_DIR = Path.home() / ".notebooklm" / "profiles" / "default" / "chrome_profile"


def save_manual_cookies(cookie_string: str) -> None:
    """Lưu cookie thủ công từ chuỗi header Copy từ Chrome DevTools."""
    STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    cookies = []
    for part in cookie_string.split(";"):
        if "=" in part:
            name, value = part.strip().split("=", 1)
            cookies.append(
                {
                    "name": name,
                    "value": value,
                    "domain": ".google.com",
                    "path": "/",
                    "expires": -1,
                    "httpOnly": True,
                    "secure": True,
                    "sameSite": "Lax",
                }
            )

    storage_data = {"cookies": cookies, "origins": []}
    STORAGE_PATH.write_text(json.dumps(storage_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ Đã lưu thành công {len(cookies)} cookies vào: {STORAGE_PATH}")


async def run_chrome_login() -> None:
    """Mở Google Chrome thật với cờ anti-detection để đăng nhập an toàn."""
    STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    print("=================================================================")
    print("   CCBA NOTEBOOKLM AUTHENTICATION — SECURE CHROME LAUNCHER       ")
    print("=================================================================")
    print("Đang khởi động trình duyệt Google Chrome chính thức...")
    print("Đã tắt các cờ tự động hóa (Automation Controlled) để tránh bị Google chặn.")
    print("-----------------------------------------------------------------")

    async with async_playwright() as p:
        try:
            # Thử mở Google Chrome chính thức cài trên máy
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(PROFILE_DIR),
                channel="chrome",
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars",
                    "--disable-dev-shm-usage",
                    "--start-maximized",
                ],
                ignore_default_args=["--enable-automation"],
            )
        except Exception:
            # Fallback nếu máy không có Chrome chuẩn, dùng MS Edge hoặc Chromium
            try:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(PROFILE_DIR),
                    channel="msedge",
                    headless=False,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-infobars",
                    ],
                    ignore_default_args=["--enable-automation"],
                )
            except Exception:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(PROFILE_DIR),
                    headless=False,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-infobars",
                    ],
                    ignore_default_args=["--enable-automation"],
                )

        page = context.pages[0] if context.pages else await context.new_page()

        # Xóa thuộc tính navigator.webdriver
        await page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        print("Đang điều hướng đến https://notebooklm.google.com ...")
        await page.goto("https://notebooklm.google.com")

        print("\n👉 HÃY ĐĂNG NHẬP GOOGLE TRÊN CỬA SỔ TRÌNH DUYỆT VỪA MỞ.")
        print("Khi màn hình hiển thị danh sách Sổ tay NotebookLM của bạn:")
        print("Bấm phím ENTER tại cửa sổ Terminal này để lưu xác thực.\n")

        input(">>> Bấm phím ENTER tại đây sau khi đã đăng nhập thành công vào NotebookLM...")

        await context.storage_state(path=str(STORAGE_PATH))
        print(f"\n🎉 XÁC THỰC THÀNH CÔNG! Đã lưu token vào: {STORAGE_PATH}")
        await context.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Google NotebookLM Authentication Helper.")
    parser.add_argument(
        "--paste-cookie",
        type=str,
        help="Dán chuỗi cookie trực tiếp từ Chrome DevTools (F12)",
    )
    args = parser.parse_args()

    if args.paste_cookie:
        save_manual_cookies(args.paste_cookie)
    else:
        asyncio.run(run_chrome_login())


if __name__ == "__main__":
    main()
