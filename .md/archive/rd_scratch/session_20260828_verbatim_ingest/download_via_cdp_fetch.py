import time
import base64
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

# Navigate to document page
page_url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx"
print(f"Navigating to {page_url}...", flush=True)
cdp.navigate(page_url)
cdp.wait_ready()
cdp.handle_cloudflare()
time.sleep(3)

# 1. In-browser fetch for DOCX
print("Fetching DOCX in browser...", flush=True)
js_fetch_docx = """
(async () => {
    try {
        let resp = await fetch("https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?part=-1&docx=1");
        if (!resp.ok) return { status: resp.status, error: "HTTP " + resp.status };
        let blob = await resp.blob();
        return new Promise((resolve) => {
            let reader = new FileReader();
            reader.onloadend = () => resolve({ status: resp.status, data: reader.result });
            reader.readAsDataURL(blob);
        });
    } catch (e) {
        return { status: 0, error: e.toString() };
    }
})()
"""
res_d = cdp.evaluate_js(js_fetch_docx)
print("DOCX Fetch status:", res_d.get("status") if isinstance(res_d, dict) else res_d, flush=True)

if isinstance(res_d, dict) and res_d.get("data"):
    data_url = res_d["data"]
    b64_data = data_url.split(",")[1]
    raw_bytes = base64.b64decode(b64_data)
    ext = ".docx" if raw_bytes.startswith(b"PK") else ".doc"
    out_docx = target_dir / f"qcvn_03_2022_bxd{ext}"
    out_docx.write_bytes(raw_bytes)
    print(f"✅ Saved DOCX: {out_docx} ({len(raw_bytes)} bytes)", flush=True)

# 2. In-browser fetch for PDF
for p in [-100, 0]:
    print(f"Fetching PDF (part={p}) in browser...", flush=True)
    js_fetch_pdf = f"""
    (async () => {{
        try {{
            let resp = await fetch("https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?part={p}");
            if (!resp.ok) return {{ status: resp.status, error: "HTTP " + resp.status }};
            let blob = await resp.blob();
            return new Promise((resolve) => {{
                let reader = new FileReader();
                reader.onloadend = () => resolve({{ status: resp.status, data: reader.result }});
                reader.readAsDataURL(blob);
            }});
        }} catch (e) {{
            return {{ status: 0, error: e.toString() }};
        }}
    }})()
    """
    res_p = cdp.evaluate_js(js_fetch_pdf)
    print(f"PDF (part={p}) Fetch status:", res_p.get("status") if isinstance(res_p, dict) else res_p, flush=True)
    if isinstance(res_p, dict) and res_p.get("data"):
        data_url = res_p["data"]
        b64_data = data_url.split(",")[1]
        raw_bytes = base64.b64decode(b64_data)
        if raw_bytes.startswith(b"%PDF"):
            out_pdf = target_dir / "qcvn_03_2022_bxd.pdf"
            out_pdf.write_bytes(raw_bytes)
            print(f"✅ Saved PDF: {out_pdf} ({len(raw_bytes)} bytes)", flush=True)
            break
