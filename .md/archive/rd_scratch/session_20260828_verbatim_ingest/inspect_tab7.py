import json
from ccba_legal.cdp import ChromeCDP

cdp = ChromeCDP(port=9222)
pages = cdp.get_pages()
if not pages:
    print("No open Chrome pages found.")
    exit(1)

ws_url = pages[0].get("webSocketDebuggerUrl")
cdp.connect_tab(ws_url)

url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?tab=7"
print(f"Navigating to {url}...")
cdp.navigate(url)
cdp.wait_ready()
cdp.handle_cloudflare()

js_inspect = """
(() => {
    let links = Array.from(document.querySelectorAll('a'));
    let download_links = links.filter(a => {
        let href = a.href || '';
        let txt = (a.innerText || '').toLowerCase();
        let cls = a.className || '';
        return href.includes('download') || href.includes('part=') || href.includes('.doc') || href.includes('.pdf') || txt.includes('tải') || txt.includes('tai');
    }).map(a => ({
        id: a.id,
        text: a.innerText.trim(),
        href: a.href,
        onclick: a.getAttribute('onclick') || ''
    }));
    return download_links;
})()
"""
links = cdp.evaluate_js(js_inspect)
print(f"Found {len(links)} candidate download links:")
for l in links:
    print(l)
