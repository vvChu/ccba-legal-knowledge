import time
from pathlib import Path
from ccba_legal.cdp import ChromeCDP

target_dir = Path(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_03_2022_bxd")
target_dir.mkdir(parents=True, exist_ok=True)

cdp = ChromeCDP(port=9222)
pages = cdp.get_pages()
if not pages:
    print("No open Chrome pages found.")
    exit(1)

ws_url = pages[0].get("webSocketDebuggerUrl")
cdp.connect_tab(ws_url)

# Set download behavior
cdp.send_command(
    "Browser.setDownloadBehavior",
    {"behavior": "allow", "downloadPath": str(target_dir.resolve()), "eventsEnabled": True},
)
cdp.send_command(
    "Page.setDownloadBehavior",
    {"behavior": "allow", "downloadPath": str(target_dir.resolve())},
)

base_url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx"

# 1. Direct DOCX URL
docx_url = f"{base_url}?part=-1&docx=1"
print(f"Navigating to direct DOCX download URL: {docx_url}...", flush=True)
cdp.navigate(docx_url)
time.sleep(6)

# 2. Direct PDF URL
pdf_url = f"{base_url}?part=-100"
print(f"Navigating to direct PDF download URL: {pdf_url}...", flush=True)
cdp.navigate(pdf_url)
time.sleep(6)

# Fallback: part=0 if part=-100 not present
files = list(target_dir.glob("*"))
print(f"Files after part=-100 ({len(files)}): {[f.name for f in files]}", flush=True)
if not any(f.suffix == ".pdf" for f in files):
    pdf_url_0 = f"{base_url}?part=0"
    print(f"Trying part=0: {pdf_url_0}...", flush=True)
    cdp.navigate(pdf_url_0)
    time.sleep(6)

files = list(target_dir.glob("*"))
print(f"Final files in target_dir ({len(files)}): {[f.name for f in files]}", flush=True)
for f in files:
    print(f" - {f.name} ({f.stat().st_size} bytes)", flush=True)
