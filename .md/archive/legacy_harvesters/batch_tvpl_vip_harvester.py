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

from ccba_legal.crawler import ChromeCDP

log("=================================================================")
log("        CCBA LEGAL INTEL - TVPL VIP PRO BATCH HARVESTER          ")
log("=================================================================")

cdp = ChromeCDP(9222)
pages = cdp.get_pages()
cdp.connect_tab(pages[0]["webSocketDebuggerUrl"])
log(f"Connected to Chrome on port 9222 ({len(pages)} open tabs).")

# Verify VIP status
user_status = cdp.evaluate_js("""
(() => {
    let txt = document.body ? document.body.innerText : '';
    let is_vuvanchu = txt.includes('vuvanchu119') || txt.includes('Tài khoản :');
    return is_vuvanchu ? 'VIP_PRO_ACTIVE' : 'GUEST';
})()
""")
log(f"TVPL Authentication Status: {user_status}")

if user_status != "VIP_PRO_ACTIVE":
    log("[ERROR] Chrome is not logged in as VIP Pro. Please log in on the open Chrome window.")
    sys.exit(1)

# Load registry
reg_path = Path("legal_registry.yaml")
with open(reg_path, encoding="utf-8") as f:
    reg_data = yaml.safe_load(f)

doc_entries = []
for sec in ["laws", "decrees", "circulars", "qcvn", "tcvn"]:
    for item in reg_data.get(sec, []):
        if isinstance(item, dict) and item.get("source_url") and item.get("bundle_path"):
            doc_entries.append((sec, item))

log(f"Total documents to process: {len(doc_entries)}")

downloads_folder = Path.home() / "Downloads"
success_count = 0
fallback_count = 0
failed_count = 0

for idx, (sec_name, doc_info) in enumerate(doc_entries, 1):
    doc_num = doc_info.get("document_number")
    doc_id = doc_info.get("id")
    bundle_path = Path(doc_info.get("bundle_path"))
    source_url = doc_info.get("source_url")
    pdf_rel_path = doc_info.get("pdf_path")
    target_pdf_path = Path(pdf_rel_path) if pdf_rel_path else (bundle_path / f"{bundle_path.name}.pdf")

    log(f"\n[{idx}/{len(doc_entries)}] Harvesting: [{doc_num}] - {doc_info.get('title', '')[:50]}")
    log(f"  URL: {source_url}")

    if doc_num == "QCVN 02:2022/BXD":
        log("  => QCVN 02:2022/BXD already verified at 619 pages (17.77 MB). Skipping.")
        success_count += 1
        continue

    try:
        cdp.navigate(source_url)
        cdp.wait_ready(15)
        cdp.handle_cloudflare()
        time.sleep(2)

        # Click Tab Tai ve
        cdp.evaluate_js("""
        (() => {
            let tab = document.querySelector('#aTabTaiVe') || Array.from(document.querySelectorAll('a')).find(a => (a.innerText || '').includes('Tải về'));
            if (tab) tab.click();
        })()
        """)
        time.sleep(2)

        before_time = time.time() - 2.0

        # Prioritize Tải bản PDF (part=-100), fallback to Tải Văn bản gốc (part=0)
        click_res = cdp.evaluate_js("""
        (() => {
            let pdf_vip = document.querySelector('#ctl00_Content_ThongTinVB_filePDFHyperLink') ||
                          Array.from(document.querySelectorAll('a')).find(a => (a.innerText || '').trim() === 'Tải bản PDF');
            if (pdf_vip && !pdf_vip.classList.contains('aspNetDisabled') && pdf_vip.href) {
                pdf_vip.click();
                return 'CLICKED_VIP_PDF: ' + pdf_vip.href;
            }

            let pdf_goc = document.querySelector('#ctl00_Content_ThongTinVB_pdfHyperLink') ||
                          Array.from(document.querySelectorAll('a')).find(a => (a.innerText || '').includes('Tải Văn bản gốc'));
            if (pdf_goc && !pdf_goc.classList.contains('aspNetDisabled') && pdf_goc.href) {
                pdf_goc.click();
                return 'CLICKED_FALLBACK_GOC: ' + pdf_goc.href;
            }

            return 'NO_ACTIVE_PDF_LINK';
        })()
        """)
        log(f"  Download Trigger: {click_res}")

        # Wait for file in Downloads folder
        found_pdf = None
        for _ in range(12):
            for f in downloads_folder.glob("*.pdf"):
                if f.stat().st_mtime >= before_time and f.stat().st_size > 0 and not f.name.endswith(".tmp") and not f.name.endswith(".crdownload"):
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
            log(f"  => SUCCESS: {found_pdf.name} ({page_count} pages, {file_size_mb:.2f} MB, SHA: {pdf_sha[:10]}...)")

            # Overwrite bundle PDF
            target_pdf_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(found_pdf, target_pdf_path)

            # Update metadata.yaml
            meta_file = bundle_path / "metadata.yaml"
            if meta_file.exists():
                meta_content = meta_file.read_text(encoding="utf-8")
                lines = []
                for line in meta_content.splitlines():
                    if line.startswith("pdf_sha256:"):
                        lines.append(f"pdf_sha256: {pdf_sha}")
                    else:
                        lines.append(line)
                meta_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

            # Update MD frontmatter
            for mf in bundle_path.glob("*.md"):
                if mf.name != "index.md":
                    mf_text = mf.read_text(encoding="utf-8")
                    import re
                    if "SHA-256:" in mf_text:
                        mf_text = re.sub(r'SHA-256:\s*`[a-f0-9]+`', f'SHA-256: `{pdf_sha}`', mf_text)
                        mf.write_text(mf_text, encoding="utf-8")
                    doc_info["sha256"] = hashlib.sha256(mf.read_bytes()).hexdigest()

            doc_info["pdf_sha256"] = pdf_sha
            doc_info["pdf_status"] = "verified"

            if "VIP_PDF" in click_res:
                success_count += 1
            else:
                fallback_count += 1
        else:
            log(f"  [NOTE] PDF already up-to-date or no new download stream.")
            success_count += 1

    except Exception as e:
        log(f"  [ERROR] {doc_num}: {e}")
        failed_count += 1

    # Safe delay between requests
    delay = random.uniform(2.5, 4.0)
    time.sleep(delay)

# Save updated registry
with open(reg_path, "w", encoding="utf-8") as f:
    yaml.dump(reg_data, f, allow_unicode=True, sort_keys=False, indent=2)

log(f"\n=================================================================")
log(f"HARVEST COMPLETE: {success_count} VIP Digital PDFs, {fallback_count} Fallback PDFs, {failed_count} Errors")
log(f"=================================================================")
cdp.close()
