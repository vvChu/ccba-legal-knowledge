import json
import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
sys.stderr.reconfigure(line_buffering=True, encoding="utf-8")

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

from ccba_legal.crawler import ChromeCDP, get_tvpl_credentials

username, password = get_tvpl_credentials()
log(f"[VIP Harvester] Target Account: {username}")

cdp = ChromeCDP(9222)
pages = cdp.get_pages()
log(f"[VIP Harvester] Connected to Chrome, open tabs: {len(pages)}")

cdp.connect_tab(pages[0]["webSocketDebuggerUrl"])
target_dir = Path("legal_docs/02_qcvn/qcvn_02_2022_bxd").resolve()
cdp.set_download_behavior(target_dir)

doc_url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-02-2022-TT-BXD-QCVN-02-2022-BXD-So-lieu-dieu-kien-tu-nhien-dung-trong-xay-dung-530884.aspx"
log(f"Navigating to document URL: {doc_url}")
cdp.navigate(doc_url)
cdp.wait_ready(15)
cdp.handle_cloudflare()
time.sleep(3)

# Check login on document page safely
check_login_js = """
(() => {
    let body = document.body;
    let txt = body ? body.innerText : '';
    if (txt.includes('vuvanchu119') || txt.includes('Tài khoản :') || document.querySelector('.info-user') || document.querySelector('#ctl00_Header_divUser')) {
        return 'LOGGED_IN';
    }
    return 'GUEST';
})()
"""
status = cdp.evaluate_js(check_login_js)
log(f"Login status on document page: {status}")

if status != "LOGGED_IN":
    log("Opening login modal...")
    cdp.evaluate_js("""
    (() => {
        let login_link = document.querySelector('#aDangNhap') ||
                         document.querySelector('#ctl00_Header_aDangNhap') ||
                         Array.from(document.querySelectorAll('a')).find(a => (a.innerText || '').trim() === 'Đăng nhập');
        if (login_link) login_link.click();
    })()
    """)
    time.sleep(2)

    fill_payload = json.dumps({"u": username, "p": password})
    fill_js = f"""
    (() => {{
        let creds = {fill_payload};
        let tb = document.querySelector('#TB_window') || document.body;
        let user = tb.querySelector('input[name*="User"], input[id*="User"], input[type="text"]');
        let pass = tb.querySelector('input[name*="Pass"], input[id*="Pass"], input[type="password"]');
        let btn = tb.querySelector('input[type="submit"], input[id*="Login"], input[id*="DangNhap"], button[id*="Login"]') ||
                  Array.from(tb.querySelectorAll('input, button')).find(b => (b.value || b.innerText || '').includes('Đăng nhập'));

        if (user && pass && btn) {{
            user.value = creds.u;
            user.dispatchEvent(new Event('input', {{ bubbles: true }}));
            user.dispatchEvent(new Event('change', {{ bubbles: true }}));

            pass.value = creds.p;
            pass.dispatchEvent(new Event('input', {{ bubbles: true }}));
            pass.dispatchEvent(new Event('change', {{ bubbles: true }}));

            btn.click();
            return 'SUBMITTED';
        }}
        return 'INPUTS_NOT_FOUND';
    }})()
    """
    sub_res = cdp.evaluate_js(fill_js)
    log(f"Login submit result: {sub_res}")
    time.sleep(5)

    try:
        pages = cdp.get_pages()
        cdp.connect_tab(pages[0]["webSocketDebuggerUrl"])
        cdp.set_download_behavior(target_dir)
        log("Reconnected WebSocket after login.")
    except Exception as e:
        log(f"Reconnect note: {e}")

    warn_res = cdp.evaluate_js("""
    (() => {
        let agree = Array.from(document.querySelectorAll('input, button, a')).find(el => {
            let t = (el.value || el.innerText || '').trim().toLowerCase();
            return t === 'đồng ý';
        });
        if (agree) {
            agree.click();
            return 'CLICKED_DONG_Y';
        }
        return 'NO_WARNING';
    })()
    """)
    log(f"Warning confirmation: {warn_res}")
    time.sleep(3)

    cdp.navigate(doc_url)
    cdp.wait_ready(15)
    time.sleep(3)

log("Switching to Tab 'Tải về'...")
cdp.evaluate_js("""
(() => {
    let tab = document.querySelector('#aTabTaiVe') || Array.from(document.querySelectorAll('a')).find(a => (a.innerText || '').includes('Tải về'));
    if (tab) tab.click();
})()
""")
time.sleep(3)

links = cdp.evaluate_js("""
(() => {
    return Array.from(document.querySelectorAll('a')).map(a => ({
        id: a.id,
        text: (a.innerText || '').trim(),
        href: a.href
    })).filter(x => x.text.length > 0 && (x.text.includes('Tải') || x.text.includes('PDF') || x.text.includes('Quy chuan')));
})()
""")
log("Links in Tab 'Tải về':")
if isinstance(links, list):
    for l in links:
        log(f"  * {l}")
else:
    log(f"  Raw links: {links}")

log("Clicking 'Tải bản PDF' (VIP)...")
click_res = cdp.evaluate_js("""
(() => {
    let pdf_a = Array.from(document.querySelectorAll('a')).find(a => (a.innerText || '').trim() === 'Tải bản PDF') ||
                Array.from(document.querySelectorAll('a')).find(a => (a.innerText || '').includes('Tải bản PDF'));
    if (pdf_a) {
        pdf_a.click();
        return 'SUCCESS_CLICKED: ' + pdf_a.innerText + ' (' + pdf_a.href + ')';
    }
    return 'NOT_FOUND';
})()
""")
log(f"PDF Click action: {click_res}")

downloads_folder = Path.home() / "Downloads"
downloaded = False
for s in range(15):
    for f in list(target_dir.glob("*.pdf")) + list(downloads_folder.glob("*.pdf")):
        if time.time() - f.stat().st_mtime < 20 and f.stat().st_size > 0:
            log(f"SUCCESS: Download detected: {f.name} ({f.stat().st_size / 1024 / 1024:.2f} MB)")
            downloaded = True
            break
    if downloaded:
        break
    time.sleep(1)

cdp.close()
log("Execution Finished.")
