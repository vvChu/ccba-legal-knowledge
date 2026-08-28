import base64
import json
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

page_url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx"
print(f"Navigating to {page_url}...", flush=True)
cdp.navigate(page_url)
cdp.wait_ready()
cdp.handle_cloudflare()
time.sleep(3)

def eval_async_js(js_expr: str):
    res = cdp.send_command(
        "Runtime.evaluate",
        {"expression": js_expr, "returnByValue": True, "awaitPromise": True},
    )
    return res.get("result", {}).get("result", {}).get("value")

# 1. DOCX
print("Fetching DOCX with awaitPromise...", flush=True)
js_docx = """
(async () => {
    let resp = await fetch("https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?part=-1&docx=1");
    if (!resp.ok) return { status: resp.status, error: "HTTP " + resp.status };
    let blob = await resp.blob();
    return new Promise((resolve) => {
        let reader = new FileReader();
        reader.onloadend = () => resolve({ status: resp.status, data: reader.result, size: blob.size });
        reader.readAsDataURL(blob);
    });
})()
"""
res_d = eval_async_js(js_docx)
print("DOCX Fetch result:", {k: v for k, v in res_d.items() if k != "data"} if isinstance(res_d, dict) else res_d, flush=True)

if isinstance(res_d, dict) and res_d.get("data"):
    data_url = res_d["data"]
    b64_data = data_url.split(",")[1]
    raw_bytes = base64.b64decode(b64_data)
    ext = ".docx" if raw_bytes.startswith(b"PK") else ".doc"
    out_docx = target_dir / f"qcvn_03_2022_bxd{ext}"
    out_docx.write_bytes(raw_bytes)
    print(f"✅ Successfully saved DOCX: {out_docx} ({len(raw_bytes)} bytes)", flush=True)

# 2. PDF
for p in [-100, 0]:
    print(f"Fetching PDF (part={p}) with awaitPromise...", flush=True)
    js_pdf = f"""
    (async () => {{
        let resp = await fetch("https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?part={p}");
        if (!resp.ok) return {{ status: resp.status, error: "HTTP " + resp.status }};
        let blob = await resp.blob();
        return new Promise((resolve) => {{
            let reader = new FileReader();
            reader.onloadend = () => resolve({{ status: resp.status, data: reader.result, size: blob.size }});
            reader.readAsDataURL(blob);
        }});
    }})()
    """
    res_p = eval_async_js(js_pdf)
    print(f"PDF (part={p}) result:", {k: v for k, v in res_p.items() if k != "data"} if isinstance(res_p, dict) else res_p, flush=True)
    if isinstance(res_p, dict) and res_p.get("data"):
        data_url = res_p["data"]
        b64_data = data_url.split(",")[1]
        raw_bytes = base64.b64decode(b64_data)
        if raw_bytes.startswith(b"%PDF"):
            out_pdf = target_dir / "qcvn_03_2022_bxd.pdf"
            out_pdf.write_bytes(raw_bytes)
            print(f"✅ Successfully saved PDF: {out_pdf} ({len(raw_bytes)} bytes)", flush=True)
            break
