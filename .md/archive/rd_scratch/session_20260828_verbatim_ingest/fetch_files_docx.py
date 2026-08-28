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

# Navigate to files.thuvienphapluat.vn endpoint
files_url = "https://files.thuvienphapluat.vn/doc.aspx?p=09pBeU5pMHdPQzB5T0MweE5TMHlNUTTW&id=I=RRek9UVTTl&part=-100&v=1"
print(f"Navigating to {files_url}...", flush=True)
cdp.navigate(files_url)
cdp.wait_ready()
cdp.handle_cloudflare()
time.sleep(2)

# Try fetching part=-1&docx=1 and part=-1 from this origin
for query_part in ["part=-1&docx=1", "part=-1", "part=0", "part=1"]:
    doc_url = f"https://files.thuvienphapluat.vn/doc.aspx?p=09pBeU5pMHdPQzB5T0MweE5TMHlNUTTW&id=I=RRek9UVTTl&{query_part}"
    print(f"\nFetching {doc_url}...", flush=True)
    js = f"""
    (async () => {{
        try {{
            let resp = await fetch("{doc_url}");
            if (!resp.ok) return {{ status: resp.status, error: "HTTP " + resp.status }};
            let blob = await resp.blob();
            let ctype = resp.headers.get("content-type") || "";
            return new Promise((resolve) => {{
                let reader = new FileReader();
                reader.onloadend = () => resolve({{ status: resp.status, data: reader.result, size: blob.size, ctype: ctype }});
                reader.readAsDataURL(blob);
            }});
        }} catch (e) {{
            return {{ status: 0, error: e.toString() }};
        }}
    }})()
    """
    res = cdp.send_command("Runtime.evaluate", {"expression": js, "returnByValue": True, "awaitPromise": True})
    val = res.get("result", {}).get("result", {}).get("value")
    if isinstance(val, dict):
        print(f"Result for {query_part}: status={val.get('status')}, size={val.get('size')}, ctype={val.get('ctype')}")
        if val.get("data"):
            b64_data = val["data"].split(",")[1]
            raw = base64.b64decode(b64_data)
            header = raw[:16]
            print(f"Header: {header}")
            if raw.startswith(b"PK") or b"word" in header:
                out = target_dir / "qcvn_03_2022_bxd.docx"
                out.write_bytes(raw)
                print(f"✅ Saved DOCX: {out} ({len(raw)} bytes)")
                break
            elif b"\xd0\xcf\x11\xe0" in header:  # OLE Compound Doc (legacy .doc)
                out = target_dir / "qcvn_03_2022_bxd.doc"
                out.write_bytes(raw)
                print(f"✅ Saved OLE DOC: {out} ({len(raw)} bytes)")
                break
