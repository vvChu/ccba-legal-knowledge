import json
import urllib.parse
from ccba_legal.cdp import ChromeCDP

cdp = ChromeCDP(port=9222)
pages = cdp.get_pages()
if not pages:
    print("No open Chrome pages found on port 9222.")
    exit(1)

ws_url = pages[0].get("webSocketDebuggerUrl")
cdp.connect_tab(ws_url)

query = "05/2022/TT-BXD"
search_url = f"https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword={urllib.parse.quote(query)}"
print(f"Navigating to {search_url}...")
cdp.navigate(search_url)
cdp.wait_ready()
cdp.handle_cloudflare()

js_get_links = """
(() => {
    let links = Array.from(document.querySelectorAll('a[href*="/van-ban/"]'));
    return links.map(a => ({ title: a.innerText.trim(), href: a.href })).filter(x => x.title.length > 5);
})()
"""
results = cdp.evaluate_js(js_get_links)
print("Search results:")
for r in results[:10]:
    print(r)
