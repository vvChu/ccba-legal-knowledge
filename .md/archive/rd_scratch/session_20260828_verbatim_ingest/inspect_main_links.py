import json
from ccba_legal.cdp import ChromeCDP

cdp = ChromeCDP(port=9222)
pages = cdp.get_pages()
if not pages:
    print("No open Chrome pages found.")
    exit(1)

ws_url = pages[0].get("webSocketDebuggerUrl")
cdp.connect_tab(ws_url)

url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx"
print(f"Navigating to {url}...", flush=True)
cdp.navigate(url)
cdp.wait_ready()
cdp.handle_cloudflare()

js_all_links = """
(() => {
    let links = Array.from(document.querySelectorAll('a'));
    let matches = links.filter(a => {
        let h = a.href || '';
        let t = (a.innerText || '').trim();
        return h.includes('part=') || h.includes('.doc') || h.includes('.pdf') || h.includes('download') || h.includes('File') || t.includes('Tải') || t.includes('Doc') || t.includes('PDF');
    }).map(a => ({
        id: a.id,
        text: a.innerText.trim(),
        href: a.href,
        onclick: a.getAttribute('onclick') || ''
    }));
    return matches;
})()
"""
res = cdp.evaluate_js(js_all_links)
print(f"Found {len(res)} candidate download links on main tab:")
for r in res:
    print(" -", r)
