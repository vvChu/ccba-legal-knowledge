"""
CCBA Legal Knowledge Spoke — Automated Batch PDF Downloader & Checksum Engine.
Tự động tải về toàn bộ file PDF Công báo gốc và tính toán mã băm SHA-256 (ADR 0016).
"""

from __future__ import annotations

import hashlib
import os
import sys
import time
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT_DIR / "legal_registry.yaml"

# Nạp biến môi trường
load_dotenv(ROOT_DIR / ".env")
load_dotenv(Path(r"D:\GitHubProjects\ccba-agent-platform\.env"))

TVPL_USER = os.getenv("TVPL_USER", "vuvanchu119")
TVPL_PASS = os.getenv("TVPL_PASS", "Chu@123456")


def compute_sha256(file_path: Path) -> str:
    """Tính mã băm SHA-256 của tệp tin nhị phân."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def batch_download_all_pdfs(headless: bool = True, max_docs: int | None = None) -> None:
    """Tải hàng loạt file PDF Công báo gốc từ Thư Viện Pháp Luật."""
    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {REGISTRY_FILE}")

    reg_data = yaml.safe_load(REGISTRY_FILE.read_text(encoding="utf-8"))
    laws = reg_data.get("laws", [])

    print("=================================================================")
    print("      CCBA AUTOMATED BATCH PDF DOWNLOADER (ADR 0016)             ")
    print("=================================================================")
    print(f"Tổng số văn bản theo dõi trong Registry: {len(laws)}")
    print(f"Tài khoản TVPL: {TVPL_USER}")
    print("-----------------------------------------------------------------")

    download_results: list[dict[str, Any]] = []

    with sync_playwright() as p:
        print("[Browser] Khởi chạy trình duyệt Playwright Chromium...")
        browser = p.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            accept_downloads=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        )
        page = context.new_page()

        # Đăng nhập TVPL 1 lần cho cả phiên
        print("[TVPL] Đang đăng nhập tài khoản Thư Viện Pháp Luật...")
        try:
            page.goto("https://thuvienphapluat.vn/thanh-vien/dang-nhap.aspx", wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            if page.query_selector("input[name='txtDangNhap']"):
                page.fill("input[name='txtDangNhap']", TVPL_USER)
                page.fill("input[name='txtMatKhau']", TVPL_PASS)
                page.click("#btDangNhap, input[type='submit']")
                time.sleep(3)
                print("✅ [TVPL] Đăng nhập thành công!")
        except Exception as e:
            print(f"⚠️ [TVPL] Cảnh báo khi đăng nhập: {e}")

        # Duyệt qua từng văn bản
        count = 0
        for idx, doc in enumerate(laws, 1):
            if max_docs and count >= max_docs:
                break

            doc_id = doc.get("id", "")
            doc_num = doc.get("document_number", "")
            source_url = doc.get("source_url", "")
            pdf_rel_path = doc.get("pdf_path", "")
            status = doc.get("pdf_status", "")

            if not source_url:
                continue

            target_pdf = ROOT_DIR / pdf_rel_path if pdf_rel_path else ROOT_DIR / "legal_docs" / "01_vbpl" / doc_id / f"{doc_id}.pdf"
            target_pdf.parent.mkdir(parents=True, exist_ok=True)

            print(f"\n[{idx:02d}/{len(laws)}] Đang xử lý: {doc_num} ({doc.get('title', '')[:40]}...)")
            print(f"   URL Nguồn: {source_url}")

            download_url = source_url if "?tab=1" in source_url else f"{source_url}?tab=1"
            success = False
            saved_file: Path | None = None

            try:
                page.goto(download_url, wait_until="domcontentloaded", timeout=25000)
                time.sleep(2)

                # Tìm nút tải PDF (ưu tiên PDF Công báo / PDF Tiếng Việt)
                download_btn = None
                buttons = page.query_selector_all("a[href*='.pdf'], a[href*='download'], a[href*='taive'], a.btn-download")

                for b in buttons:
                    txt = b.inner_text().lower()
                    href = b.get_attribute("href") or ""
                    if ".pdf" in href.lower() or "pdf" in txt or "công báo" in txt or "tiếng việt" in txt:
                        download_btn = b
                        break

                if not download_btn and buttons:
                    download_btn = buttons[0]

                if download_btn:
                    with page.expect_download(timeout=15000) as download_info:
                        download_btn.click()
                    download = download_info.value
                    download.save_as(str(target_pdf))

                    sha256_hash = compute_sha256(target_pdf)
                    file_size = target_pdf.stat().st_size
                    print(f"   ✅ ĐÃ TẢI XONG: {target_pdf.name} ({file_size / 1024:.1f} KB)")
                    print(f"   🔑 SHA-256   : {sha256_hash}")

                    # Cập nhật registry metadata
                    doc["pdf_status"] = "downloaded"
                    doc["pdf_sha256"] = sha256_hash
                    success = True
                    saved_file = target_pdf
                    count += 1
                else:
                    print(f"   ⚠️ Không tìm thấy nút tải PDF trên trang tải về.")

            except Exception as e:
                print(f"   ❌ Lỗi khi tải văn bản {doc_num}: {e}")

            download_results.append({
                "document_number": doc_num,
                "title": doc.get("title", ""),
                "target_file": str(target_pdf.relative_to(ROOT_DIR)) if saved_file else None,
                "success": success,
            })

        browser.close()

    # Ghi lại legal_registry.yaml
    REGISTRY_FILE.write_text(
        yaml.dump(reg_data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print("\n=================================================================")
    print("      TỔNG KẾT TẢI PDF CÔNG BÁO GỐC (ADR 0016)                   ")
    print("=================================================================")
    success_count = sum(1 for r in download_results if r["success"])
    print(f"• Tổng số văn bản đã xử lý : {len(download_results)}")
    print(f"• Số tệp PDF tải thành công : {success_count}/{len(download_results)}")
    print(f"• Đã cập nhật SHA-256 vào   : legal_registry.yaml")
    print("=================================================================\n")


def main() -> None:
    headless = "--visible" not in sys.argv
    max_count = None
    for arg in sys.argv:
        if arg.startswith("--limit="):
            max_count = int(arg.split("=")[1])

    batch_download_all_pdfs(headless=headless, max_docs=max_count)


if __name__ == "__main__":
    main()
