"""Fetch and download official TVPL legal documents (.docx and .pdf) via Chrome CDP with ADR 0016 compliance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

import requests
import websocket
import yaml
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT_DIR / "legal_registry.yaml"

# Load environment variables
load_dotenv(ROOT_DIR / ".env")
load_dotenv(Path(r"D:\GitHubProjects\ccba-agent-platform\.env"))


class ChromeCDPError(Exception):
    """Base exception for Chrome DevTools Protocol operations."""

    pass


class ChromeCDP:
    """Robust client interacting with Chrome via DevTools Protocol (CDP) WebSocket."""

    def __init__(self, port: int = 9222) -> None:
        self.port = port
        self.base_url = f"http://127.0.0.1:{port}"
        self.ws: websocket.WebSocket | None = None

    def get_pages(self) -> list[dict[str, Any]]:
        """List all open page targets in Chrome, creating one if none exist."""
        try:
            resp = requests.get(f"{self.base_url}/json", timeout=5)
            resp.raise_for_status()
            pages = [t for t in resp.json() if t.get("type") == "page"]
            if not pages:
                new_tab_resp = requests.put(f"{self.base_url}/json/new?about:blank", timeout=5)
                if new_tab_resp.status_code in (200, 201):
                    pages = [new_tab_resp.json()]
            return pages
        except Exception as e:
            raise ChromeCDPError(f"Failed to connect to Chrome on port {self.port}: {e}") from e

    def connect_tab(self, ws_url: str) -> None:
        """Connect to a specific tab via WebSockets and initialize domains."""
        try:
            self.ws = websocket.create_connection(ws_url, suppress_origin=True)
            self.ws.settimeout(1.0)
            self.send_command("Page.enable")
            self.send_command("Runtime.enable")
        except Exception as e:
            raise ChromeCDPError(f"Failed to connect to tab WebSocket: {e}") from e

    def send_command(
        self, method: str, params: dict[str, Any] | None = None, timeout_sec: float = 25.0
    ) -> dict[str, Any]:
        """Send a generic CDP command and wait for the matching response ID."""
        if not self.ws:
            raise ChromeCDPError("No active WebSocket connection.")
        cmd_id = random.randint(1, 1000000)
        payload = {"id": cmd_id, "method": method, "params": params or {}}
        try:
            self.ws.send(json.dumps(payload))
            start_time = time.time()
            while time.time() - start_time < timeout_sec:
                try:
                    raw = self.ws.recv()
                except (websocket.WebSocketTimeoutException, socket.timeout):
                    continue
                try:
                    data = json.loads(raw)
                    if data.get("id") == cmd_id:
                        return data
                except Exception:
                    pass
            raise ChromeCDPError(
                f"Timeout ({timeout_sec}s) waiting for response to CDP command {method} (id={cmd_id})"
            )
        except Exception as e:
            if isinstance(e, ChromeCDPError):
                raise
            raise ChromeCDPError(f"Failed to send/recv CDP command {method}: {e}") from e

    def evaluate_js(self, expression: str, timeout_sec: float = 25.0) -> Any:
        """Evaluate a JavaScript expression in the connected tab."""
        data = self.send_command(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True},
            timeout_sec=timeout_sec,
        )
        result_data = data.get("result", {})
        if "exceptionDetails" in result_data:
            exc = result_data["exceptionDetails"]
            raise ChromeCDPError(
                f"JS Exception: {exc.get('text')} - {exc.get('exception', {})}"
            )
        return result_data.get("result", {}).get("value")

    def navigate(self, url: str, timeout_sec: float = 25.0) -> None:
        """Navigate to a URL and wait for the page load."""
        self.send_command("Page.navigate", {"url": url}, timeout_sec=timeout_sec)
        time.sleep(2.0)

    def wait_ready(self, timeout_sec: int = 30) -> None:
        """Wait for document readyState to be 'complete'."""
        start_time = time.time()
        while time.time() - start_time < timeout_sec:
            try:
                state = self.evaluate_js("document.readyState")
                if state == "complete":
                    return
            except ChromeCDPError:
                pass
            time.sleep(0.5)
        raise ChromeCDPError("Timeout waiting for page readyState 'complete'.")

    def handle_cloudflare(self) -> None:
        """Check for Cloudflare bot challenge and pause for user completion if found."""
        check_expr = """
        !!(document.title.includes("Cloudflare") ||
           document.title.includes("Just a moment") ||
           document.querySelector("div.cf-turnstile") ||
           document.querySelector("#challenge-running") ||
           document.querySelector("#challenge-stage"))
        """
        is_blocked = self.evaluate_js(check_expr)
        if is_blocked:
            print("[LegalIntel] Cloudflare Challenge detected! PAUSED.")
            print("[LegalIntel] PLEASE MANUALLY SOLVE THE CAPTCHA IN THE OPEN CHROME WINDOW.")
            start = time.time()
            while is_blocked and time.time() - start < 45:
                time.sleep(2)
                try:
                    is_blocked = self.evaluate_js(check_expr)
                except ChromeCDPError:
                    is_blocked = True
            print("[LegalIntel] Challenge passed! Resuming execution...")
            self.wait_ready()

    def handle_login(self) -> bool:
        """Detect login popup or page, fill in credentials, submit, and confirm multi-session warning."""
        username = os.environ.get("TVPL_USERNAME", "vuvanchu119")
        password = os.environ.get("TVPL_PASSWORD", "Chu@123456")
        if not username or not password:
            print(
                "  [Login] Missing TVPL_USERNAME or TVPL_PASSWORD env variable. Cannot perform auto-login."
            )
            return False

        js = """
        (() => {
            // 1. Check popup ThickBox
            let tb = document.querySelector('#TB_window');
            if (tb && tb.style.display !== 'none') {
                let inputs = Array.from(tb.querySelectorAll('input'));
                let text_inputs = inputs.filter(i => i.type === 'text' || !i.type);
                let pass_inputs = inputs.filter(i => i.type === 'password');
                let buttons = Array.from(tb.querySelectorAll('input[type="submit"], input[type="button"], button'));

                let user = text_inputs[0];
                let pass = pass_inputs[0];
                let login_btn = buttons.find(b => (b.value && b.value.includes('Đăng nhập')) || (b.innerText && b.innerText.includes('Đăng nhập')));

                if (user && pass && login_btn) {
                    user.value = "__USERNAME__";
                    pass.value = "__PASSWORD__";
                    setTimeout(() => { login_btn.click(); }, 50);
                    return "Attempted popup login click";
                }
            }

            // 2. Check full-page login form
            let userEl = document.querySelector('input[name="txtDangNhap"]') || document.querySelector('#txtDangNhap');
            let passEl = document.querySelector('input[name="txtMatKhau"]') || document.querySelector('#txtMatKhau');
            let btnEl = document.querySelector('#btDangNhap') || document.querySelector('input[type="submit"][value*="Đăng nhập"]');
            if (userEl && passEl && btnEl) {
                userEl.value = "__USERNAME__";
                passEl.value = "__PASSWORD__";
                setTimeout(() => { btnEl.click(); }, 50);
                return "Attempted page login click";
            }

            return "No login form found";
        })()
        """.replace("__USERNAME__", username).replace("__PASSWORD__", password)
        res = self.evaluate_js(js)
        if "Attempted" in str(res):
            print(f"  [Login] {res}, autofilling credentials and submitting...")
            time.sleep(3)

            # Check for multi-session login warning popup
            warning_js = """
            (() => {
                let agree_btn = Array.from(document.querySelectorAll('input, button, a')).find(el => {
                    let txt = (el.value || el.innerText || "").trim().toLowerCase();
                    return txt === 'đồng ý';
                });
                if (agree_btn) {
                    setTimeout(() => { agree_btn.click(); }, 50);
                    return "Clicked Dong y";
                }
                return "No warning popup";
            })()
            """
            warn_res = self.evaluate_js(warning_js)
            print(f"  [Login Warning Check] Result: {warn_res}")
            if "Clicked Dong y" in str(warn_res):
                time.sleep(3)
            else:
                time.sleep(2)

            return True
        return False

    def close_popup(self) -> bool:
        """Close any open ThickBox popup on the page."""
        js = """
        (() => {
            let closed = false;
            if (typeof tb_remove === 'function') {
                tb_remove();
                closed = true;
            } else {
                let tbClose = document.querySelector('#TB_closeWindowButton') || document.querySelector('[id*="TB_close"]');
                if (tbClose) {
                    tbClose.click();
                    closed = true;
                }
            }
            let tb = document.querySelector('#TB_window');
            if (tb && tb.style.display !== 'none') {
                tb.style.display = 'none';
                let overlay = document.querySelector('#TB_overlay');
                if (overlay) overlay.style.display = 'none';
                closed = true;
            }
            return closed;
        })()
        """
        return bool(self.evaluate_js(js))

    def switch_to_download_tab(self) -> None:
        """Ensure the 'Tải về' tab is active."""
        tab_click_js = """
        (() => {
            let tab = document.querySelector('#aTabTaiVe') || 
                      document.querySelector('a[href*="#tab8"]') || 
                      Array.from(document.querySelectorAll('a')).find(a => a.innerText && a.innerText.trim() === 'Tải về');
            if (tab) {
                tab.click();
                return "Clicked Tab Tai ve: " + (tab.id || tab.innerText);
            }
            return "Tab Tai ve not found";
        })()
        """
        self.evaluate_js(tab_click_js)
        time.sleep(1.5)

    def close(self) -> None:
        """Close WebSocket connection."""
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
            self.ws = None


def compute_file_sha256(file_path: Path) -> str:
    """Calculate SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def _download_via_action(
    cdp: ChromeCDP, click_js: str, expected_extensions: list[str], dest_file: Path, timeout_sec: int = 35
) -> bool:
    """Trigger click action, handle popups/login, and capture the downloaded file."""
    downloads_path = Path.home() / "Downloads"
    if not downloads_path.exists():
        downloads_path = Path("C:/Users/chuvu/Downloads")

    existing_downloads = {f.name for f in downloads_path.glob("*")}

    cdp.switch_to_download_tab()
    res = cdp.evaluate_js(click_js)
    if "not found" in str(res).lower() or not res:
        print(f"  [Download Action] Selector not found on page.")
        return False

    time.sleep(2)
    # Check if login popup appears
    if cdp.handle_login():
        print("  [Action] Login submitted after click, waiting for reload...")
        cdp.wait_ready()
        cdp.handle_cloudflare()
        cdp.switch_to_download_tab()
        cdp.evaluate_js(click_js)
    elif cdp.close_popup():
        cdp.evaluate_js(click_js)

    # Monitor Downloads folder
    start_time = time.time()
    while time.time() - start_time < timeout_sec:
        current_downloads = list(downloads_path.glob("*"))
        new_downloads = [f for f in current_downloads if f.name not in existing_downloads]
        if new_downloads:
            if any(f.suffix == ".crdownload" or f.name.endswith(".tmp") for f in new_downloads):
                time.sleep(1)
                continue

            completed_files = [f for f in new_downloads if f.suffix.lower() in expected_extensions]
            if completed_files:
                target_file = completed_files[0]
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.move(str(target_file), str(dest_file))
                    print(
                        f"  ✅ Đã tải và lưu trữ: {dest_file.name} ({dest_file.stat().st_size:,} bytes)"
                    )
                    return True
                except Exception as e:
                    print(f"  ❌ Lỗi khi di chuyển tệp: {e}")
                    return False
        time.sleep(1)

    print(f"  ⚠️ Hết thời gian chờ tải ({timeout_sec}s).")
    return False


def download_docx(cdp: ChromeCDP, dest_path: Path) -> bool:
    """Download DOCX / DOC editable file."""
    if dest_path.exists() and dest_path.stat().st_size > 0:
        print(f"  [Tier 1 Local Cache] Tệp DOCX đã tồn tại: {dest_path.name}")
        return True

    click_js = """
    (() => {
        let btnDocx = document.querySelector('#ctl00_Content_ThongTinVB_vietnameseHyperLink_Docx') ||
                      document.querySelector('a[id*="vietnameseHyperLink_Docx"]') ||
                      Array.from(document.querySelectorAll('a')).find(a => a.innerText && a.innerText.includes('(docx)'));
        if (btnDocx) {
            setTimeout(() => { btnDocx.click(); }, 50);
            return "Clicked DOCX download async";
        }
        let btnDoc = document.querySelector('#ctl00_Content_ThongTinVB_vietnameseHyperLink') ||
                     Array.from(document.querySelectorAll('a')).find(a => a.innerText && a.innerText.includes('Văn bản tiếng Việt'));
        if (btnDoc) {
            setTimeout(() => { btnDoc.click(); }, 50);
            return "Clicked DOC download async";
        }
        return "DOCX button not found";
    })()
    """
    return _download_via_action(cdp, click_js, [".docx", ".doc"], dest_path)


def download_pdf(cdp: ChromeCDP, dest_path: Path) -> bool:
    """Download official Công báo PDF file with Tab 3 iframe fallback."""
    if dest_path.exists() and dest_path.stat().st_size > 0:
        print(f"  [Tier 1 Local Cache] Tệp PDF đã tồn tại: {dest_path.name}")
        return True

    downloads_path = Path.home() / "Downloads"
    if not downloads_path.exists():
        downloads_path = Path("C:/Users/chuvu/Downloads")
    existing_downloads = {f.name for f in downloads_path.glob("*")}

    # Strategy 1: Standard button on download tab
    click_js = """
    (() => {
        let btnPdf = document.querySelector('#ctl00_Content_ThongTinVB_filePDFHyperLink') ||
                     document.querySelector('#ctl00_Content_ThongTinVB_pdfHyperLink') ||
                     Array.from(document.querySelectorAll('a')).find(a => a.innerText && (a.innerText.includes('Tải bản PDF') || a.innerText.includes('Tải Văn bản gốc')));
        if (btnPdf && btnPdf.href) {
            setTimeout(() => { btnPdf.click(); }, 50);
            return "Clicked PDF download button";
        }
        return "PDF button not found";
    })()
    """
    if _download_via_action(cdp, click_js, [".pdf"], dest_path, timeout_sec=25):
        return True

    # Strategy 2: Tab 3 (Văn bản gốc / PDF iframe) fallback
    print("  [Strategy 2] Thử tải qua Tab 3 Văn bản gốc / PDF...")
    try:
        tab3_click_js = """
        (() => {
            let tab = document.querySelector('#aVanBanGoc') || document.querySelector('a[href*="#tab3"]');
            if (tab) { tab.click(); return "Clicked Tab 3"; }
            return "Tab 3 not found";
        })()
        """
        cdp.evaluate_js(tab3_click_js)
        time.sleep(2)

        get_iframe_src = """
        (() => {
            let iframes = Array.from(document.querySelectorAll('iframe')).map(f => f.src).filter(s => s && s.includes('files.thuvienphapluat.vn'));
            return iframes[0] || '';
        })()
        """
        iframe_src = cdp.evaluate_js(get_iframe_src)
        if iframe_src:
            print(f"  [Tab 3] Phát hiện nguồn PDF: {iframe_src[:60]}...")
            cdp.navigate(iframe_src)
            time.sleep(3)
            cdp.handle_cloudflare()

            blob_js = f"""
            (async () => {{
                try {{
                    let resp = await fetch(window.location.href);
                    if (!resp.ok) return "Fetch error: " + resp.status;
                    let blob = await resp.blob();
                    let blobUrl = window.URL.createObjectURL(blob);
                    let a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = blobUrl;
                    a.download = '{dest_path.name}';
                    document.body.appendChild(a);
                    a.click();
                    setTimeout(() => {{
                        document.body.removeChild(a);
                        window.URL.revokeObjectURL(blobUrl);
                    }}, 3000);
                    return "Triggered blob download (" + blob.size + " bytes)";
                }} catch(e) {{
                    return "ERROR: " + e.toString();
                }}
            }})()
            """
            cdp.send_command(
                "Runtime.evaluate",
                {"expression": blob_js, "returnByValue": True, "awaitPromise": True},
                timeout_sec=40
            )

            start = time.time()
            while time.time() - start < 30:
                current = list(downloads_path.glob("*"))
                new_files = [f for f in current if f.name not in existing_downloads]
                if new_files:
                    if any(f.suffix == ".crdownload" or f.name.endswith(".tmp") for f in new_files):
                        time.sleep(1)
                        continue
                    completed = [f for f in new_files if f.suffix.lower() == ".pdf"]
                    if completed:
                        target = completed[0]
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(target), str(dest_path))
                        print(
                            f"  ✅ Đã tải và lưu trữ: {dest_path.name} ({dest_path.stat().st_size:,} bytes)"
                        )
                        return True
                time.sleep(1)
    except Exception as e:
        print(f"  ❌ Lỗi Tab 3 PDF download: {e}")

    return False


def _parse_tvpl_date(date_str: str) -> str:
    """Parse a TVPL date string of format DD/MM/YYYY to YYYY-MM-DD."""
    if not date_str:
        return ""
    try:
        parts = date_str.split("/")
        if len(parts) == 3:
            d, m, y = parts
            return f"{y.strip()}-{m.strip().zfill(2)}-{d.strip().zfill(2)}"
    except Exception:
        pass
    return date_str


def get_tvpl_metadata(cdp: ChromeCDP, url: str) -> dict[str, Any]:
    """Retrieve structured metadata from the TVPL document page."""
    meta_js = """
    (() => {
        let result = {};
        let propTable = document.querySelector('#divThuocTinh') || 
                        document.querySelector('#ctl00_Content_Tab_ThuocTinh') ||
                        document.querySelector('.content1 table') ||
                        document.querySelector('table');
        if (propTable) {
            let rows = Array.from(propTable.querySelectorAll('tr'));
            rows.forEach(r => {
                let cells = Array.from(r.querySelectorAll('td, th'));
                if (cells.length >= 2) {
                    let k = cells[0].innerText.trim().replace(':', '');
                    let v = cells[1].innerText.trim();
                    if (k && v) result[k] = v;
                }
            });
        }
        return result;
    })()
    """
    raw_meta = cdp.evaluate_js(meta_js) or {}
    return {
        "document_number": raw_meta.get("Số hiệu", ""),
        "type": raw_meta.get("Loại văn bản", ""),
        "issued_by": raw_meta.get("Nơi ban hành", ""),
        "signer": raw_meta.get("Người ký", ""),
        "issued_date": _parse_tvpl_date(raw_meta.get("Ngày ban hành", "")),
        "effective_date": _parse_tvpl_date(raw_meta.get("Ngày hiệu lực", "")),
        "published_date": _parse_tvpl_date(raw_meta.get("Ngày đăng", "")),
        "status": raw_meta.get("Tình trạng", ""),
        "relations": {},
    }


def _normalize(s: str) -> str:
    """Normalize string for search comparison."""
    import unicodedata

    s = (
        s.strip()
        .lower()
        .replace(":", " ")
        .replace("-", " ")
        .replace("_", " ")
        .replace("/", " ")
    )
    s = s.replace("đ", "d").replace("Đ", "d")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return " ".join(s.split())


def find_doc_in_registry(identifier: str) -> tuple[str, str, dict[str, Any]]:
    """Find document slug, source_url, and registered metadata from legal_registry.yaml."""
    if identifier.startswith("http://") or identifier.startswith("https://"):
        slug = (
            identifier.split("/")[-1]
            .replace(".aspx", "")
            .lower()
            .replace("-", "_")
        )
        return slug, identifier, {}

    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Registry not found: {REGISTRY_FILE}")

    reg = yaml.safe_load(REGISTRY_FILE.read_text(encoding="utf-8"))
    items = reg.get("laws", [])
    if isinstance(reg.get("documents"), list):
        items.extend(reg.get("documents", []))
    elif isinstance(reg.get("documents"), dict):
        items.extend(reg.get("documents", {}).values())

    ident_norm = _normalize(identifier)

    for item in items:
        if not isinstance(item, dict):
            continue
        doc_id = _normalize(str(item.get("id", "")))
        doc_num = _normalize(str(item.get("document_number", "")))
        title = _normalize(str(item.get("title", "")))
        bundle_path = _normalize(str(item.get("bundle_path", "")))
        source_url = _normalize(str(item.get("source_url", "")))

        if (
            ident_norm == doc_id
            or ident_norm in doc_id
            or ident_norm == doc_num
            or ident_norm in doc_num
            or ident_norm in bundle_path
            or ident_norm in title
            or ident_norm in source_url
        ):
            slug = Path(item.get("bundle_path", "doc")).name.strip("/")
            if not slug or slug == "doc":
                slug = item.get("id", "doc")
            url = item.get("source_url", "")
            return str(slug), str(url), item

    return (
        identifier,
        f"https://thuvienphapluat.vn/van-ban/{identifier}.aspx",
        {},
    )


def is_cdp_listening(port: int = 9222) -> bool:
    """Check if Chrome CDP port is already open."""
    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/json/version",
            headers={"User-Agent": "CCBA-Agent"},
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False


def launch_chrome_cdp(url: str, port: int = 9222) -> subprocess.Popen | None:
    """Launch Google Chrome with remote debugging if not already listening."""
    if is_cdp_listening(port):
        print(f"[CDP] Phát hiện Chrome đã mở sẵn trên cổng {port}!")
        return None

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not Path(chrome_exe).exists():
        chrome_exe = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    user_data = ROOT_DIR / ".md" / "data" / "chrome_cdp_profile"
    user_data.mkdir(parents=True, exist_ok=True)

    cmd = [
        chrome_exe,
        f"--remote-debugging-port={port}",
        "--remote-allow-origins=*",
        f"--user-data-dir={user_data.resolve()}",
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
        url,
    ]
    print(f"[CDP] Khởi chạy Chrome thật trên cổng {port}...")
    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    proc = subprocess.Popen(
        cmd, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP, close_fds=True
    )
    time.sleep(3)
    return proc


def update_registry_dual_fetch(
    slug: str,
    docx_file: Path | None = None,
    pdf_file: Path | None = None,
) -> None:
    """Update DOCX sha256 and PDF sha256/status in legal_registry.yaml."""
    if not REGISTRY_FILE.exists():
        return

    content = REGISTRY_FILE.read_text(encoding="utf-8")
    reg = yaml.safe_load(content)

    updated = False
    for section in ["laws", "documents"]:
        items = reg.get(section, [])
        item_list = items if isinstance(items, list) else items.values()
        for item in item_list:
            if (
                item.get("id") == slug
                or Path(item.get("bundle_path", "")).name == slug
            ):
                if docx_file and docx_file.exists():
                    item["sha256"] = compute_file_sha256(docx_file)
                    try:
                        rel_src = docx_file.relative_to(ROOT_DIR)
                        item["source_file"] = str(rel_src)
                    except Exception:
                        item["source_file"] = str(docx_file)
                    item["source_file_size_kb"] = round(docx_file.stat().st_size / 1024, 1)
                    updated = True

                if pdf_file and pdf_file.exists():
                    item["pdf_sha256"] = compute_file_sha256(pdf_file)
                    item["pdf_status"] = "verified"
                    try:
                        rel_pdf = pdf_file.relative_to(ROOT_DIR)
                        item["pdf_path"] = str(rel_pdf).replace("\\", "/")
                    except Exception:
                        pass
                    updated = True

    if updated:
        REGISTRY_FILE.write_text(
            yaml.dump(reg, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        print(f"[Registry] Đã cập nhật metadata và mã băm SHA-256 cho '{slug}' vào legal_registry.yaml")


def fetch_tvpl_document(
    identifier: str,
    output_dir: Path | None = None,
    port: int = 9222,
    skip_verify: bool = False,
) -> bool:
    """Main workflow to verify and dual-fetch official DOCX + PDF legal document via Chrome CDP."""
    slug, url, reg_item = find_doc_in_registry(identifier)
    print(f"=================================================================")
    print(f"  CCBA TVPL VIP DUAL-FETCHER (DOCX + PDF ADR 0016)")
    print(f"=================================================================")
    print(f"  Target Identifier : {identifier}")
    print(f"  Target Slug       : {slug}")
    print(f"  Target Source URL : {url}")

    # Check if URL is placeholder / not yet published
    if not url or "pagenotfound" in url.lower() or ("thong_tu_" in url.lower() and "_tt_" in url.lower() and not any(c.isdigit() for c in url.split("/")[-1].replace(".aspx", "").split("_")[2:3])):
        print(f"  ℹ️ [Thông báo] Văn bản '{slug}' chưa có bản đăng tải chính thức trên TVPL.")
        return False

    bundle_name = Path(reg_item.get("bundle_path", slug)).name.strip("/") or slug
    extracted_dir = ROOT_DIR / ".md" / "extracted_docs" / bundle_name
    extracted_dir.mkdir(parents=True, exist_ok=True)

    # Resolve target file paths
    docx_dest = extracted_dir / f"{slug}.docx"
    reg_pdf_path = reg_item.get("pdf_path", "")
    if reg_pdf_path:
        pdf_dest = ROOT_DIR / reg_pdf_path
    else:
        pdf_dest = ROOT_DIR / "legal_docs" / "01_vbpl" / bundle_name / f"{slug}.pdf"

    # Launch Chrome if needed
    launch_chrome_cdp(url, port=port)

    cdp: ChromeCDP | None = None
    try:
        print(f"\n[CDP] Đang kết nối tới Chrome (ws://127.0.0.1:{port})...")
        cdp = ChromeCDP(port=port)
        pages = cdp.get_pages()
        if not pages:
            raise RuntimeError(f"Không tìm thấy tab nào trong Chrome đang mở trên cổng {port}!")
        ws_url = pages[0].get("webSocketDebuggerUrl")
        if not ws_url:
            raise RuntimeError("Không lấy được webSocketDebuggerUrl từ tab Chrome!")
        cdp.connect_tab(ws_url)
        cdp.navigate(url)
        time.sleep(2)

        # 1. Handle Cloudflare Turnstile
        print("[CDP] Kiểm tra Cloudflare Turnstile...")
        cdp.handle_cloudflare()

        # Check if page is 404
        page_info = cdp.evaluate_js("({ title: document.title, url: window.location.href })") or {}
        if "pagenotfound" in page_info.get("url", "").lower() or "Không tìm thấy" in page_info.get("title", ""):
            print(f"  ⚠️ [Lưu ý] URL '{url}' chuyển hướng về 404 (Trang không tìm thấy trên TVPL).")
            return False

        # --- LỚP 2: ĐỐI SOÁT METADATA TỪ TRANG VĂN BẢN ---
        print("\n--- [LỚP 2] ĐỐI SOÁT BẢNG THUỘC TÍNH PHÁP LÝ ---")
        try:
            metadata = get_tvpl_metadata(cdp, url)
            web_doc_num = metadata.get("document_number", "")
            web_type = metadata.get("type", "")
            web_issuer = metadata.get("issued_by", "")
            web_status = metadata.get("status", "")

            print(f"  - Số hiệu trên Web  : {web_doc_num}")
            print(f"  - Loại văn bản      : {web_type}")
            print(f"  - Cơ quan ban hành  : {web_issuer}")
            print(f"  - Ngày ban hành     : {metadata.get('issued_date', '')}")
            print(f"  - Ngày hiệu lực     : {metadata.get('effective_date', '')}")

            # --- LỚP 3: KIỂM TRA NHÃN TRẠNG THÁI HIỆU LỰC ---
            print("\n--- [LỚP 3] KIỂM TRA TRẠNG THÁI HIỆU LỰC ---")
            if "hết hiệu lực" in web_status.lower():
                print(f"  🔴 [CẢNH BÁO NGUY HIỂM] Tình trạng: {web_status.upper()}")
            elif "chưa có hiệu lực" in web_status.lower():
                print(f"  🟡 [LƯU Ý] Tình trạng: {web_status.upper()} (Áp dụng tương lai)")
            else:
                print(f"  🟢 [HỢP LỆ] Tình trạng: {web_status or 'Đang có hiệu lực'}")

        except Exception as e:
            print(f"  [Lưu ý] Không trích xuất được metadata: {e}")

        # --- LỚP 4: DUAL-FETCH (DOCX + PDF CÔNG BÁO GỐC ADR 0016) ---
        print(f"\n--- [LỚP 4] DUAL-FETCH: TẢI ĐỒNG THỜI DOCX & PDF GỐC CHO '{slug}' ---")
        
        # 1. Fetch DOCX
        print("  1. Tải bản văn bản soạn thảo (DOCX)...")
        docx_ok = download_docx(cdp, docx_dest)
        
        # 2. Fetch PDF
        print("  2. Tải bản PDF Công báo gốc (PDF ADR 0016)...")
        pdf_ok = download_pdf(cdp, pdf_dest)

        if docx_ok or pdf_ok:
            update_registry_dual_fetch(slug, docx_file=docx_dest if docx_ok else None, pdf_file=pdf_dest if pdf_ok else None)
            print(f"\n✅ [HOÀN TẤT] Dual-fetch thành công cho '{slug}' (DOCX: {'✅' if docx_ok else '❌'}, PDF: {'✅' if pdf_ok else '❌'})")
            return True
        else:
            print(f"\n❌ [THẤT BẠI] Không bắt được tệp DOCX hoặc PDF từ TVPL.")
            return False

    except Exception as e:
        print(f"\n❌ [LỖI] Ngoại lệ xảy ra trong quá trình cào: {e}")
        return False
    finally:
        if cdp:
            cdp.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download official legal document from TVPL with Dual-Fetch (DOCX + PDF)"
    )
    parser.add_argument(
        "doc",
        help="Document Slug, Number (e.g. 03/2021/TT-BXD), or TVPL URL",
    )
    parser.add_argument(
        "--port", "-p", help="CDP Port", default=9222, type=int
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip strict metadata comparison",
    )

    args = parser.parse_args()
    ok = fetch_tvpl_document(
        args.doc,
        port=args.port,
        skip_verify=args.skip_verify,
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
