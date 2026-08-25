import hashlib
import json
import os
import random
import shutil
import sys
import time
from pathlib import Path
import yaml
import fitz

sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
sys.stderr.reconfigure(line_buffering=True, encoding="utf-8")

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

from ccba_legal.crawler import ChromeCDP, get_tvpl_credentials

username, password = get_tvpl_credentials()
log(f"=== BATCH TVPL PDF HARVESTER (VIP PRO) ===")
log(f"Target Account: {username}")

# 1. Load all documents from registry
reg_path = Path("legal_registry.yaml")
with open(reg_path, encoding="utf-8") as f:
    reg_data = yaml.safe_load(f)

doc_entries = []
for section_name in ["laws", "decrees", "circulars", "qcvn", "tcvn"]:
    items = reg_data.get(section_name, [])
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and item.get("source_url") and item.get("bundle_path"):
                doc_entries.append((section_name, item))

log(f"Total official documents queued: {len(doc_entries)}")

# 2. Connect to Chrome CDP
cdp = ChromeCDP(9222)
pages = cdp.get_pages()
cdp.connect_tab(pages[0]["webSocketDebuggerUrl"])
log("Connected to Chrome.")

downloads_folder = Path.home() / "Downloads"

success_count = 0
failed_count = 0

for idx, (sec_name, doc_info) in enumerate(doc_entries, 1):
    doc_num = doc_info.get("document_number")
    doc_id = doc_info.get("id")
    bundle_path = Path(doc_info.get("bundle_path"))
    source_url = doc_info.get("source_url")
    pdf_rel_path = doc_info.get("pdf_path")
    target_pdf_path = Path(pdf_rel_path) if pdf_rel_path else (bundle_path / f"{bundle_path.name}.pdf")

    log(f"\n[{idx}/{len(doc_entries)}] Processing [{doc_num}] ({doc_id})...")
    log(f"  URL: {source_url}")

    if doc_num == "QCVN 02:2022/BXD":
        log("  => QCVN 02:2022/BXD is already verified at 619 pages. Skipping download.")
        success_count += 1
        continue

    # Navigate
    try:
        cdp.navigate(source_url)
        cdp.wait_ready(15)
        cdp.handle_cloudflare()
        time.sleep(2)

        # Switch to Tab Tai ve
        cdp.evaluate_js("""
        (() => {
            let tab = document.querySelector('#aTabTaiVe') || Array.from(document.querySelectorAll('a')).find(a => (a.innerText || '').includes('Tải về'));
            if (tab) tab.click();
        })()
        """)
        time.sleep(2)

        # Record download timestamp before click
        before_time = time.time() - 2.0

        # Click Tải bản PDF (or fallback)
        click_res = cdp.evaluate_js("""
        (() => {
            let links = Array.from(document.querySelectorAll('a'));
            let pdf_a = links.find(a => (a.innerText || '').trim() === 'Tải bản PDF') ||
                        links.find(a => (a.innerText || '').includes('Tải bản PDF')) ||
                        document.querySelector('#ctl00_Content_ThongTinVB_pdfHyperLink') ||
                        links.find(a => (a.innerText || '').includes('Tải Văn bản gốc') || (a.innerText || '').includes('Bản PDF'));
            if (pdf_a) {
                pdf_a.click();
                return 'CLICKED: ' + (pdf_a.innerText || pdf_a.id || 'PDF_LINK');
            }
            return 'NO_PDF_LINK';
        })()
        """)
        log(f"  Action: {click_res}")

        # Wait for download in Downloads folder
        found_pdf = None
        for _ in range(12):
            for f in downloads_folder.glob("*.pdf"):
                if f.stat().st_mtime >= before_time and f.stat().st_size > 0 and not f.name.endswith(".tmp"):
                    found_pdf = f
                    break
            if found_pdf:
                break
            time.sleep(1.0)

        if found_pdf:
            doc_fitz = fitz.open(found_pdf)
            page_count = len(doc_fitz)
            file_size_mb = found_pdf.stat().st_size / 1024 / 1024
            pdf_sha = hashlib.sha256(found_pdf.read_bytes()).hexdigest()
            log(f"  => Downloaded: {found_pdf.name} ({page_count} pages, {file_size_mb:.2f} MB, SHA-256: {pdf_sha[:12]}...)")

            # Copy to target bundle
            target_pdf_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(found_pdf, target_pdf_path)

            # Update metadata.yaml
            meta_file = bundle_path / "metadata.yaml"
            if meta_file.exists():
                meta_content = meta_file.read_text(encoding="utf-8")
                # update pdf_sha256
                lines = []
                for line in meta_content.splitlines():
                    if line.startswith("pdf_sha256:"):
                        lines.append(f'pdf_sha256: {pdf_sha}')
                    else:
                        lines.append(line)
                meta_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

            # Update MD frontmatter
            md_files = list(bundle_path.glob("*.md"))
            for mf in md_files:
                if mf.name != "index.md":
                    mf_text = mf.read_text(encoding="utf-8")
                    if "pdf_anchor:" in mf_text or "SHA-256:" in mf_text:
                        import re
                        mf_text = re.sub(r'SHA-256:\s*`[a-f0-9]+`', f'SHA-256: `{pdf_sha}`', mf_text)
                        mf.write_text(mf_text, encoding="utf-8")

            # Update registry data in memory
            doc_info["pdf_sha256"] = pdf_sha
            doc_info["pdf_status"] = "verified"
            # Update MD sha256
            for mf in md_files:
                if mf.name != "index.md":
                    doc_info["sha256"] = hashlib.sha256(mf.read_bytes()).hexdigest()

            success_count += 1
        else:
            log(f"  [WARN] Download timeout for {doc_num}")
            failed_count += 1

    except Exception as e:
        log(f"  [ERROR] Processing {doc_num}: {e}")
        failed_count += 1

    # Jitter delay
    sleep_delay = random.uniform(2.0, 3.5)
    time.sleep(sleep_delay)

# Save updated registry
with open(reg_path, "w", encoding="utf-8") as f:
    yaml.dump(reg_data, f, allow_unicode=True, sort_keys=False, indent=2)

log(f"\n==========================================")
log(f"BATCH FINISHED: {success_count} succeeded, {failed_count} failed")
log(f"==========================================")
cdp.close()
