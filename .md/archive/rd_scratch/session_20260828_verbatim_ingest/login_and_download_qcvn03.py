import time
import shutil
from pathlib import Path
from ccba_legal.cdp import ChromeCDP
from ccba_legal.session import get_tvpl_credentials, sleep_with_jitter

username, password = get_tvpl_credentials()

cdp = ChromeCDP(port=9222)
pages = cdp.get_pages()
if not pages:
    print("No open Chrome pages found.")
    exit(1)

ws_url = pages[0].get("webSocketDebuggerUrl")
cdp.connect_tab(ws_url)

# 1. Check login status
print("Checking login status...", flush=True)
cdp.navigate("https://thuvienphapluat.vn/page/dang-nhap.aspx")
cdp.wait_ready()
cdp.handle_cloudflare()
time.sleep(2)

login_js = f"""
(() => {{
    let u = document.querySelector('#usernameTextBox') ||
            document.querySelector('#txtUsername') ||
            document.querySelector('input[placeholder*="Tên đăng nhập"]') ||
            document.querySelector('input[placeholder*="Email"]');
    let p = document.querySelector('#passwordTextBox') ||
            document.querySelector('#txtPassword') ||
            document.querySelector('input[placeholder*="Mật khẩu"]');
    let btn = document.querySelector('#loginButton') ||
               document.querySelector('#btLogin') ||
               document.querySelector('input[value="Đăng nhập"]');
    if (u && p && btn) {{
        u.value = "{username}";
        p.value = "{password}";
        u.dispatchEvent(new Event('input', {{ bubbles: true }}));
        p.dispatchEvent(new Event('input', {{ bubbles: true }}));
        btn.click();
        return "Submitted login form";
    }}
    return "Login form not found (possibly already logged in)";
}})()
"""
res_login = cdp.evaluate_js(login_js)
print("Login result:", res_login, flush=True)
time.sleep(3)
cdp.wait_ready()
cdp.handle_cloudflare()

# Handle multi-session dialog
confirm_js = """
(() => {
    let btns = Array.from(document.querySelectorAll('.ui-dialog-buttonpane button, .ui-dialog-buttonset button, input[type="button"], button'));
    let dong_y = btns.find(b => {
        let txt = (b.innerText || b.value || '').trim().toLowerCase();
        return txt.includes('đồng ý') || txt.includes('tiếp tục') || txt.includes('dong y');
    });
    if (dong_y) {
        dong_y.click();
        return 'Clicked: ' + (dong_y.innerText || dong_y.value);
    }
    if (typeof ContinueLogin === 'function') {
        ContinueLogin();
        return 'Called ContinueLogin()';
    }
    return 'No multi-session warning';
})()
"""
res_conf = cdp.evaluate_js(confirm_js)
print("Confirmation result:", res_conf, flush=True)
time.sleep(2)

# 2. Navigate directly to tab=7
target_url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx?tab=7"
print(f"Navigating to {target_url}...", flush=True)
cdp.navigate(target_url)
cdp.wait_ready()
cdp.handle_cloudflare()
time.sleep(3)

downloads_dir = Path(r"C:\Users\chuvu\Downloads")
target_dir = Path(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_03_2022_bxd")
target_dir.mkdir(parents=True, exist_ok=True)

before_files = set(downloads_dir.glob("*"))

# 3. Click DOCX
print("Clicking DOCX link on tab=7...", flush=True)
click_docx_js = """
(() => {
    let btn = document.querySelector('#ctl00_Content_ThongTinVB_vietnameseHyperLink_Docx') ||
              document.querySelector('#ctl00_Content_ThongTinVB_vietnameseHyperLink');
    if (btn) {
        btn.click();
        return 'Clicked: ' + btn.id;
    }
    return 'DOCX link not found';
})()
"""
r_d = cdp.evaluate_js(click_docx_js)
print("DOCX click result:", r_d, flush=True)
time.sleep(4)

# 4. Click PDF
print("Clicking PDF link on tab=7...", flush=True)
click_pdf_js = """
(() => {
    let btn = document.querySelector('#ctl00_Content_ThongTinVB_pdfHyperLink') ||
              document.querySelector('#ctl00_Content_ThongTinVB_filePDFHyperLink') ||
              Array.from(document.querySelectorAll('a')).find(a => (a.innerText || '').includes('Tải Văn bản gốc'));
    if (btn) {
        btn.click();
        return 'Clicked: ' + (btn.id || btn.innerText);
    }
    return 'PDF link not found';
})()
"""
r_p = cdp.evaluate_js(click_pdf_js)
print("PDF click result:", r_p, flush=True)

# 5. Wait for files in Downloads folder
print("Waiting for downloaded files...", flush=True)
found_docx = None
found_pdf = None

for i in range(15):
    time.sleep(2)
    new_files = [f for f in downloads_dir.glob("*") if f not in before_files or "543956" in f.name]
    for f in new_files:
        if f.suffix in [".docx", ".doc"] and not f.name.endswith(".crdownload") and not f.name.endswith(".tmp"):
            found_docx = f
        elif f.suffix == ".pdf" and not f.name.endswith(".crdownload") and not f.name.endswith(".tmp"):
            found_pdf = f

    if found_docx and found_pdf:
        print(f"Both files found! DOCX: {found_docx.name}, PDF: {found_pdf.name}", flush=True)
        break

if found_docx:
    dest_docx = target_dir / f"qcvn_03_2022_bxd{found_docx.suffix}"
    shutil.copy2(found_docx, dest_docx)
    print(f"✅ Saved DOCX: {dest_docx} ({dest_docx.stat().st_size} bytes)", flush=True)

if found_pdf:
    dest_pdf = target_dir / "qcvn_03_2022_bxd.pdf"
    shutil.copy2(found_pdf, dest_pdf)
    print(f"✅ Saved PDF: {dest_pdf} ({dest_pdf.stat().st_size} bytes)", flush=True)
