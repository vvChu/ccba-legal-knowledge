import json
from ccba_legal.cdp import ChromeCDP

cdp = ChromeCDP(port=9222)
pages = cdp.get_pages()
if not pages:
    print("No open Chrome pages found.")
    exit(1)

ws_url = pages[0].get("webSocketDebuggerUrl")
cdp.connect_tab(ws_url)

for t in [2, 3]:
    url = f"https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?tab={t}"
    print(f"\n--- Checking Tab {t}: {url} ---", flush=True)
    cdp.navigate(url)
    cdp.wait_ready()
    cdp.handle_cloudflare()

    js_pdf_check = """
    (() => {
        let iframes = Array.from(document.querySelectorAll('iframe, embed, object')).map(e => e.src || e.data);
        let pdf_links = Array.from(document.querySelectorAll('a')).filter(a => {
            let h = (a.href || '').toLowerCase();
            let t = (a.innerText || '').toLowerCase();
            return h.includes('.pdf') || h.includes('part=') || t.includes('pdf') || t.includes('tải');
        }).map(a => ({ id: a.id, text: a.innerText.trim(), href: a.href }));
        return { iframes, pdf_links };
    })()
    """
    res = cdp.evaluate_js(js_pdf_check)
    print("Result:", res, flush=True)
