"""
CCBA Legal Knowledge Spoke — Automated Batch Document & PDF Fetcher.
Tự động tải về toàn bộ tệp gốc (DOCX & PDF Công báo) cho toàn bộ 24 VBPL qua Chrome CDP (ADR 0016).
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT_DIR / "legal_registry.yaml"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Load environment
load_dotenv(ROOT_DIR / ".env")
load_dotenv(Path(r"D:\GitHubProjects\ccba-agent-platform\.env"))

from scripts.fetch_tvpl_doc import (
    find_doc_in_registry,
    fetch_tvpl_document,
    is_cdp_listening,
    launch_chrome_cdp,
)


def run_batch_fetch(port: int = 9222, limit: int | None = None) -> None:
    """Chạy vòng lặp tải hàng loạt toàn bộ văn bản trong legal_registry.yaml."""
    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Không tìm thấy registry tại {REGISTRY_FILE}")

    reg = yaml.safe_load(REGISTRY_FILE.read_text(encoding="utf-8"))
    laws = reg.get("laws", [])

    print("=================================================================")
    print("   CCBA BATCH DOCUMENT & PDF FETCHER ENGINE (ADR 0016)           ")
    print("=================================================================")
    print(f"Tổng số văn bản cần xử lý: {len(laws)}")
    print(f"Chrome CDP Port: {port}")
    print("-----------------------------------------------------------------")

    # Khởi chạy Chrome một lần nếu chưa chạy
    if not is_cdp_listening(port):
        first_url = laws[0].get("source_url", "https://thuvienphapluat.vn")
        launch_chrome_cdp(first_url, port=port)
        time.sleep(3)

    results: list[dict[str, Any]] = []
    processed = 0

    for idx, doc in enumerate(laws, 1):
        if limit and processed >= limit:
            break

        doc_num = doc.get("document_number", "")
        doc_id = doc.get("id", "")
        source_url = doc.get("source_url", "")

        if not source_url:
            continue

        print(f"\n[{idx:02d}/{len(laws)}] Tiến hành tải: {doc_num} ({doc.get('title', '')[:45]}...)")
        
        try:
            success = fetch_tvpl_document(
                identifier=doc_num or doc_id,
                port=port,
                skip_verify=True,
            )
            results.append({"doc_num": doc_num, "success": success})
            if success:
                processed += 1
            time.sleep(2)  # Nghỉ giữa các lượt tải để chống rate-limit
        except Exception as e:
            print(f"❌ [LỖI] Tải thất bại cho {doc_num}: {e}")
            results.append({"doc_num": doc_num, "success": False, "error": str(e)})

    print("\n=================================================================")
    print("                TỔNG KẾT BATCH DOWNLOAD                          ")
    print("=================================================================")
    success_count = sum(1 for r in results if r.get("success"))
    print(f"• Tổng số văn bản đã xử lý : {len(results)}")
    print(f"• Số văn bản tải thành công: {success_count}/{len(results)}")
    print("=================================================================\n")


def main() -> None:
    limit = None
    for arg in sys.argv:
        if arg.startswith("--limit="):
            limit = int(arg.split("=")[1])
    run_batch_fetch(limit=limit)


if __name__ == "__main__":
    main()
