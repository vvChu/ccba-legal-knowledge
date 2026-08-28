import json
from ccba_legal.cdp import ChromeCDP

cdp = ChromeCDP(port=9222)
pages = cdp.get_pages()
if not pages:
    print("No open Chrome pages found.")
    exit(1)

ws_url = pages[0].get("webSocketDebuggerUrl")
cdp.connect_tab(ws_url)

url = "https://thuvienphapluat.vn/TCVN/Xay-dung/QCVN-03-2022-BXD-Phan-cap-cong-trinh-phuc-vu-thiet-ke-xay-dung-919646.aspx?tab=7"
print(f"Navigating to {url}...", flush=True)
cdp.navigate(url)
cdp.wait_ready()
cdp.handle_cloudflare()

js_links = """
(() => {
    let links = Array.from(document.querySelectorAll('a'));
    return links.filter(a => {
        let h = a.href || '';
        let t = (a.innerText || '').trim();
        return h.includes('part=') || h.includes('.doc') || h.includes('.pdf') || h.includes('download') || t.includes('Tải') || t.includes('Doc') || t.includes('PDF');
    }).map(a => ({
        id: a.id,
        text: a.innerText.trim(),
        href: a.href,
        onclick: a.getAttribute('onclick') || ''
    }));
})()
"""
res = cdp.evaluate_js(js_links)
print(f"Found {len(res)} links on TCVN tab=7:")
for r in res:
    print(" -", r)
