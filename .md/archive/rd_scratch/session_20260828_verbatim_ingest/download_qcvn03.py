import time
import shutil
from pathlib import Path
from ccba_legal.cdp import ChromeCDP

cdp = ChromeCDP(port=9222)
pages = cdp.get_pages()
if not pages:
    print("No open Chrome pages found.")
    exit(1)

ws_url = pages[0].get("webSocketDebuggerUrl")
cdp.connect_tab(ws_url)

url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?tab=7"
print(f"Navigating to {url}...", flush=True)
cdp.navigate(url)
cdp.wait_ready()
cdp.handle_cloudflare()
time.sleep(3)

downloads_dir = Path(r"C:\Users\chuvu\Downloads")
target_dir = Path(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_03_2022_bxd")
target_dir.mkdir(parents=True, exist_ok=True)

before_files = set(downloads_dir.glob("*"))

# 1. Click DOCX button
print("Clicking DOCX link...", flush=True)
js_docx = """
(() => {
    let btn = document.querySelector('#ctl00_Content_ThongTinVB_vietnameseHyperLink_Docx');
    if (!btn) {
        btn = document.querySelector('#ctl00_Content_ThongTinVB_vietnameseHyperLink');
    }
    if (btn) {
        btn.click();
        return 'Clicked DOCX: ' + btn.id;
    }
    return 'DOCX not found';
})()
"""
res_docx = cdp.evaluate_js(js_docx)
print(f"Result DOCX: {res_docx}", flush=True)
time.sleep(5)

# 2. Click PDF link
print("Clicking PDF link...", flush=True)
js_pdf = """
(() => {
    let btn = document.querySelector('#ctl00_Content_ThongTinVB_pdfHyperLink') ||
              document.querySelector('#ctl00_Content_ThongTinVB_filePDFHyperLink');
    if (!btn) {
        btn = Array.from(document.querySelectorAll('a')).find(a => (a.innerText || '').includes('Tải Văn bản gốc'));
    }
    if (btn) {
        btn.click();
        return 'Clicked PDF: ' + (btn.id || btn.innerText);
    }
    return 'PDF not found';
})()
"""
res_pdf = cdp.evaluate_js(js_pdf)
print(f"Result PDF: {res_pdf}", flush=True)

# Wait for downloads to arrive in Downloads folder
print("Waiting for downloads to complete...", flush=True)
found_docx = None
found_pdf = None

for i in range(20):
    time.sleep(2)
    after_files = [f for f in downloads_dir.glob("*") if f not in before_files or "543956" in f.name]
    for f in after_files:
        if f.suffix in [".docx", ".doc"] and not f.name.endswith(".crdownload") and not f.name.endswith(".tmp"):
            found_docx = f
        elif f.suffix == ".pdf" and not f.name.endswith(".crdownload") and not f.name.endswith(".tmp"):
            found_pdf = f

    if found_docx and found_pdf:
        print(f"Both assets downloaded! DOCX: {found_docx.name}, PDF: {found_pdf.name}", flush=True)
        break

if found_docx:
    dest_docx = target_dir / f"qcvn_03_2022_bxd{found_docx.suffix}"
    shutil.copy2(found_docx, dest_docx)
    print(f"Saved DOCX: {dest_docx} ({dest_docx.stat().st_size} bytes)", flush=True)

if found_pdf:
    dest_pdf = target_dir / "qcvn_03_2022_bxd.pdf"
    shutil.copy2(found_pdf, dest_pdf)
    print(f"Saved PDF: {dest_pdf} ({dest_pdf.stat().st_size} bytes)", flush=True)
