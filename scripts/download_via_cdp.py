"""Download QCVN 06 .docx via ChromeCDP."""

import os
import subprocess
import sys
import time
from pathlib import Path
from ccba_legal import ChromeCDP, trigger_download

sys.stdout.reconfigure(encoding="utf-8")


def run_cdp_download():
    target_dir = Path("d:/GitHubProjects/ccba-legal-knowledge/.md/extracted_docs/qcvn_06_2022_bxd")
    target_dir.mkdir(parents=True, exist_ok=True)

    # Launch Chrome on debugging port 9222
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data = r"C:\Users\chuvu\AppData\Local\Google\Chrome\User Data"

    chrome_cmd = [
        chrome_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data}",
        "https://thuvienphapluat.vn/van-ban/Xay-dung-Nha-o/Thong-tu-06-2022-TT-BXD-Quy-chuan-ky-thuat-quoc-gia-an-toan-chay-cho-nha-va-cong-trinh-545609.aspx",
    ]

    print("[CDP] Launching Chrome on port 9222...")
    proc = subprocess.Popen(chrome_cmd)
    time.sleep(5)

    try:
        cdp = ChromeCDP(port=9222)
        print("[CDP] Connected to Chrome instance!")
        time.sleep(2)
        cdp.handle_cloudflare()

        print("[CDP] Triggering download...")
        success = trigger_download(cdp, target_dir, "qcvn_06_2022_bxd")
        print(f"[CDP] Download result: {success}")
        cdp.close()
    except Exception as e:
        print(f"[CDP Error] {e}")
    finally:
        proc.terminate()


if __name__ == "__main__":
    run_cdp_download()
