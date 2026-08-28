import requests
from pathlib import Path
from ccba_legal.session import CookieVault, get_tvpl_credentials

vault = CookieVault()
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
})

target_dir = Path(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_03_2022_bxd")
target_dir.mkdir(parents=True, exist_ok=True)

loaded = vault.load_cookies_into_session(session)
print(f"Cookies loaded from vault: {loaded}")

base_url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx"

# 1. Download DOCX
docx_url = f"{base_url}?part=-1&docx=1"
print(f"Fetching DOCX from {docx_url}...")
r_docx = session.get(docx_url, allow_redirects=True, timeout=30)
print(f"DOCX status: {r_docx.status_code}, content-type: {r_docx.headers.get('Content-Type')}, length: {len(r_docx.content)}")

if r_docx.status_code == 200 and len(r_docx.content) > 5000 and not r_docx.content.startswith(b"<!DOCTYPE"):
    ext = ".docx" if r_docx.content.startswith(b"PK") else ".doc"
    out_docx = target_dir / f"qcvn_03_2022_bxd{ext}"
    out_docx.write_bytes(r_docx.content)
    print(f"✅ Saved DOCX: {out_docx} ({out_docx.stat().st_size} bytes)")
else:
    print(f"⚠️ DOCX response preview: {r_docx.text[:300]}")

# 2. Download PDF (part=-100 or part=0)
for p in [-100, 0]:
    pdf_url = f"{base_url}?part={p}"
    print(f"Fetching PDF from {pdf_url}...")
    r_pdf = session.get(pdf_url, allow_redirects=True, timeout=30)
    print(f"PDF (part={p}) status: {r_pdf.status_code}, content-type: {r_pdf.headers.get('Content-Type')}, length: {len(r_pdf.content)}")
    if r_pdf.status_code == 200 and r_pdf.content.startswith(b"%PDF"):
        out_pdf = target_dir / "qcvn_03_2022_bxd.pdf"
        out_pdf.write_bytes(r_pdf.content)
        print(f"✅ Saved PDF: {out_pdf} ({out_pdf.stat().st_size} bytes)")
        break
    else:
        print(f"⚠️ PDF response preview: {r_pdf.text[:200]}")
