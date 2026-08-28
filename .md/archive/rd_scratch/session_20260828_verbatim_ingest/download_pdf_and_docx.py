import base64
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

# 1. Navigate directly to PDF endpoint on files.thuvienphapluat.vn
pdf_url = "https://files.thuvienphapluat.vn/doc.aspx?p=09pBeU5pMHdPQzB5T0MweE5TMHlNUTTW&id=I=RRek9UVTTl&part=-100&v=1"
print(f"Navigating to PDF endpoint: {pdf_url}...", flush=True)
cdp.navigate(pdf_url)
cdp.wait_ready()
cdp.handle_cloudflare()
time.sleep(3)

js_fetch_self = """
(async () => {
    try {
        let resp = await fetch(window.location.href);
        if (!resp.ok) return { status: resp.status, error: "HTTP " + resp.status };
        let blob = await resp.blob();
        return new Promise((resolve) => {
            let reader = new FileReader();
            reader.onloadend = () => resolve({ status: resp.status, data: reader.result, size: blob.size });
            reader.readAsDataURL(blob);
        });
    } catch (e) {
        return { status: 0, error: e.toString() };
    }
})()
"""
res = cdp.send_command("Runtime.evaluate", {"expression": js_fetch_self, "returnByValue": True, "awaitPromise": True})
val = res.get("result", {}).get("result", {}).get("value")
print("PDF fetch result:", {k: v for k, v in val.items() if k != "data"} if isinstance(val, dict) else val, flush=True)

if isinstance(val, dict) and val.get("data"):
    b64_data = val["data"].split(",")[1]
    raw_pdf = base64.b64decode(b64_data)
    out_pdf = target_dir / "qcvn_03_2022_bxd.pdf"
    out_pdf.write_bytes(raw_pdf)
    print(f"✅ Successfully saved VIP PDF: {out_pdf} ({len(raw_pdf)} bytes)", flush=True)

# 2. Now for DOCX: on thuvienphapluat.vn, let's navigate to tab=7 and fetch DOCX
tab7_url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?tab=7"
print(f"Navigating to {tab7_url}...", flush=True)
cdp.navigate(tab7_url)
cdp.wait_ready()
cdp.handle_cloudflare()
time.sleep(3)

# In tab=7, let's submit the form for vietnameseHyperLink_Docx
js_postback = """
(() => {
    if (typeof __doPostBack === 'function') {
        __doPostBack('ctl00$Content$ThongTinVB$vietnameseHyperLink_Docx','');
        return 'Triggered __doPostBack for DOCX';
    }
    return '__doPostBack not found';
})()
"""
res_post = cdp.evaluate_js(js_postback)
print("PostBack result:", res_post, flush=True)
time.sleep(5)
