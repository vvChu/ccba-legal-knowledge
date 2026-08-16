"""Login script specifically targeting https://notebooklm.google.com for notebooklm-py."""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

STORAGE_PATH = Path.home() / ".notebooklm" / "profiles" / "default" / "storage_state.json"

async def run_login():
    STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print("Navigating to https://notebooklm.google.com...")
        await page.goto("https://notebooklm.google.com")
        print("\n=================================================================")
        print("Vui lòng đăng nhập Google tại cửa sổ Chromium vừa mở.")
        print("Khi màn hình hiển thị danh sách Sổ tay NotebookLM (https://notebooklm.google.com),")
        print("bấm phím ENTER tại cửa sổ Terminal này để lưu xác thực.")
        print("=================================================================\n")
        
        input("Bấm ENTER tại đây sau khi đã đăng nhập thành công vào NotebookLM...")
        
        await context.storage_state(path=str(STORAGE_PATH))
        print(f"\n✅ Successfully saved authentication cookies to: {STORAGE_PATH}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_login())
