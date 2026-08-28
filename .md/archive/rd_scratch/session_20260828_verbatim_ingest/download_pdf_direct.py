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

# 1. Fetch PDF from direct files endpoint
pdf_endpoint = "https://files.thuvienphapluat.vn/doc.aspx?p=09pBeU5pMHdPQzB5T0MweE5TMHlNUTTW&id=I=RRek9UVTTl&part=-100&v=1"
print(f"Fetching PDF from {pdf_endpoint}...", flush=True)

js_fetch_pdf = f"""
(async () => {{
    try {{
        let resp = await fetch("{pdf_endpoint}");
        if (!resp.ok) return {{ status: resp.status, error: "HTTP " + resp.status }};
        let blob = await resp.blob();
        return new Promise((resolve) => {{
            let reader = new FileReader();
            reader.onloadend = () => resolve({{ status: resp.status, data: reader.result, size: blob.size }});
            reader.readAsDataURL(blob);
        }});
    }} catch (e) {{
        return {{ status: 0, error: e.toString() }};
    }}
}})()
"""
res = cdp.send_command("Runtime.evaluate", {"expression": js_fetch_pdf, "returnByValue": True, "awaitPromise": True})
val = res.get("result", {}).get("result", {}).get("value")
print("PDF fetch result:", {k: v for k, v in val.items() if k != "data"} if isinstance(val, dict) else val, flush=True)

if isinstance(val, dict) and val.get("data"):
    b64_data = val["data"].split(",")[1]
    raw_pdf = base64.b64decode(b64_data)
    out_pdf = target_dir / "qcvn_03_2022_bxd.pdf"
    out_pdf.write_bytes(raw_pdf)
    print(f"✅ Successfully saved VIP PDF: {out_pdf} ({len(raw_pdf)} bytes)", flush=True)
