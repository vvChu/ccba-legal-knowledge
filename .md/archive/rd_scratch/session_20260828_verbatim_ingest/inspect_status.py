import time
from ccba_legal.cdp import ChromeCDP

cdp = ChromeCDP(port=9222)
pages = cdp.get_pages()
if not pages:
    print("No open Chrome pages found.")
    exit(1)

ws_url = pages[0].get("webSocketDebuggerUrl")
cdp.connect_tab(ws_url)

# Check current URL and page title
js_status = """
(() => {
    return {
        url: window.location.href,
        title: document.title,
        bodyTextSnippet: document.body.innerText.substring(0, 300),
        dialogs: Array.from(document.querySelectorAll('.ui-dialog, .modal, .popup, [class*="dialog"], [class*="modal"], [class*="alert"]')).map(d => d.innerText.trim()).filter(Boolean)
    };
})()
"""
status = cdp.evaluate_js(js_status)
print("Page Status:", status)
