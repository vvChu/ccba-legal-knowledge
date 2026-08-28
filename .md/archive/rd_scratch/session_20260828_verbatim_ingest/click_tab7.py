import time
from pathlib import Path
from ccba_legal.cdp import ChromeCDP

downloads_dir = Path(r"C:\Users\chuvu\Downloads")
target_dir = Path(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_03_2022_bxd")
target_dir.mkdir(parents=True, exist_ok=True)

cdp = ChromeCDP(port=9222)
pages = cdp.get_pages()
if not pages:
    print("No open Chrome pages found.")
    exit(1)

ws_url = pages[0].get("webSocketDebuggerUrl")
cdp.connect_tab(ws_url)

# Navigate to tab=7
url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?tab=7"
print(f"Navigating to {url}...", flush=True)
cdp.navigate(url)
cdp.wait_ready()
cdp.handle_cloudflare()
time.sleep(3)

# Enable downloads via CDP
cdp.send_command("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": str(downloads_dir.resolve())})
cdp.send_command("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": str(downloads_dir.resolve()), "eventsEnabled": True})

# 1. Dispatch click on DOCX button
print("Dispatching click on DOCX button...", flush=True)
click_docx = """
(() => {
    let btn = document.querySelector('#ctl00_Content_ThongTinVB_vietnameseHyperLink_Docx');
    if (btn) {
        btn.click();
        return 'Clicked DOCX';
    }
    return 'Button not found';
})()
"""
res = cdp.evaluate_js(click_docx)
print("Click DOCX result:", res, flush=True)

# Wait 8s for download
time.sleep(8)

# 2. Dispatch click on PDF button
print("Dispatching click on PDF button...", flush=True)
click_pdf = """
(() => {
    let btn = document.querySelector('#ctl00_Content_ThongTinVB_pdfHyperLink') ||
              document.querySelector('#ctl00_Content_ThongTinVB_filePDFHyperLink');
    if (btn) {
        btn.click();
        return 'Clicked PDF';
    }
    return 'Button not found';
})()
"""
res2 = cdp.evaluate_js(click_pdf)
print("Click PDF result:", res2, flush=True)

# Wait 8s for download
time.sleep(8)

# Check recent files in Downloads
for f in sorted(downloads_dir.glob("*"), key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
    print(f" - {f.name} ({f.stat().st_size} bytes)")
