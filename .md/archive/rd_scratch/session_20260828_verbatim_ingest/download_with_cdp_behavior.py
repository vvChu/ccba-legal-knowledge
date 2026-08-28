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

# Set download behavior to allow automatic downloads directly into target_dir
print(f"Setting CDP download behavior to {target_dir}...", flush=True)
try:
    res = cdp.send_command(
        "Browser.setDownloadBehavior",
        {"behavior": "allow", "downloadPath": str(target_dir.resolve()), "eventsEnabled": True},
    )
    print("Browser.setDownloadBehavior result:", res, flush=True)
except Exception as e:
    print("Browser.setDownloadBehavior error:", e, flush=True)

try:
    res2 = cdp.send_command(
        "Page.setDownloadBehavior",
        {"behavior": "allow", "downloadPath": str(target_dir.resolve())},
    )
    print("Page.setDownloadBehavior result:", res2, flush=True)
except Exception as e:
    print("Page.setDownloadBehavior error:", e, flush=True)

# Navigate to tab=7
target_url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?tab=7"
print(f"Navigating to {target_url}...", flush=True)
cdp.navigate(target_url)
cdp.wait_ready()
cdp.handle_cloudflare()
time.sleep(3)

# 1. Click DOCX
print("Clicking DOCX link...", flush=True)
js_docx = """
(() => {
    let btn = document.querySelector('#ctl00_Content_ThongTinVB_vietnameseHyperLink_Docx') ||
              document.querySelector('#ctl00_Content_ThongTinVB_vietnameseHyperLink');
    if (btn) {
        btn.click();
        return 'Clicked: ' + btn.id;
    }
    return 'DOCX not found';
})()
"""
res_d = cdp.evaluate_js(js_docx)
print("DOCX click result:", res_d, flush=True)
time.sleep(6)

# 2. Click PDF
print("Clicking PDF link...", flush=True)
js_pdf = """
(() => {
    let btn = document.querySelector('#ctl00_Content_ThongTinVB_pdfHyperLink') ||
              document.querySelector('#ctl00_Content_ThongTinVB_filePDFHyperLink');
    if (btn) {
        btn.click();
        return 'Clicked: ' + btn.id;
    }
    return 'PDF not found';
})()
"""
res_p = cdp.evaluate_js(js_pdf)
print("PDF click result:", res_p, flush=True)

# Wait and check target_dir
for i in range(15):
    time.sleep(2)
    files = list(target_dir.glob("*"))
    print(f"Files in target_dir ({len(files)}): {[f.name for f in files]}", flush=True)
    if any(f.suffix in [".docx", ".doc"] for f in files) and any(f.suffix == ".pdf" for f in files):
        print("Both DOCX and PDF arrived!", flush=True)
        break
