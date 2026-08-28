import re
import sys
from pathlib import Path
import docx
from pypdf import PdfReader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path("legal_docs/02_qcvn/qcvn_03_2022_bxd")
docx_path = bundle_dir / "sources" / "qcvn_03_2022_bxd.docx"
pdf_path = bundle_dir / "sources" / "qcvn_03_2022_bxd.pdf"
md_path = bundle_dir / "qcvn_03_2022_bxd.md"
annex_path = bundle_dir / "annexes" / "phu_luc_a_cap_hau_qua_cong_trinh.md"

doc = docx.Document(docx_path)
docx_paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

reader = PdfReader(pdf_path)
pdf_text_pages = [page.extract_text() or "" for page in reader.pages]
pdf_full_text = "\n".join(pdf_text_pages)

md_main = md_path.read_text(encoding="utf-8")
md_annex = annex_path.read_text(encoding="utf-8") if annex_path.exists() else ""
combined_md = md_main + "\n" + md_annex

print("=================================================================")
print("  DETAILED LINE-BY-LINE AUDIT: QCVN 03:2022/BXD (MD vs DOCX/PDF) ")
print("=================================================================")
print(f"📄 DOCX paragraphs : {len(docx_paras)}")
print(f"📄 PDF total pages  : {len(reader.pages)} ({len(pdf_full_text)} characters)")
print(f"📄 Markdown main    : {len(md_main)} characters")
print(f"📄 Markdown annex   : {len(md_annex)} characters")
print("-----------------------------------------------------------------")

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s\d]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()

norm_md = normalize(combined_md)
norm_pdf = normalize(pdf_full_text)

# Check all DOCX paragraphs
unmatched_docx = []
for idx, p in enumerate(docx_paras, 1):
    np = normalize(p)
    if not np:
        continue
    # Check if in Markdown
    # We take key 6-word window to match
    words = np.split()
    matched = False
    if len(words) >= 4:
        for w_start in range(max(1, len(words) - 5)):
            chunk = " ".join(words[w_start : w_start + 6])
            if chunk in norm_md:
                matched = True
                break
    else:
        if np in norm_md:
            matched = True

    if not matched:
        unmatched_docx.append((idx, p))

print(f"📊 DOCX Paragraphs Match Status:")
print(f"   - Matched: {len(docx_paras) - len(unmatched_docx)} / {len(docx_paras)}")
print(f"   - Unmatched in MD: {len(unmatched_docx)}")

if unmatched_docx:
    print("\n🔍 Unmatched DOCX paragraphs (investigating context):")
    for idx, p in unmatched_docx:
        print(f"   [{idx}] {p}")

print("\n-----------------------------------------------------------------")
print("🔍 Examining Document Structure & Section Breakdown:")
# Check each section of QCVN 03:2022/BXD
expected_sections = [
    "Lời nói đầu",
    "1. QUY ĐỊNH CHUNG",
    "1.1. Phạm vi điều chỉnh",
    "1.2. Đối tượng áp dụng",
    "1.3. Giải thích từ ngữ",
    "1.3.1", "1.3.2", "1.3.3", "1.3.4", "1.3.5", "1.3.6", "1.3.7",
    "2. QUY ĐỊNH KỸ THUẬT",
    "2.1. Cấp hậu quả của công trình",
    "2.1.1", "2.1.2", "2.1.3",
    "2.2. Thời hạn sử dụng theo thiết kế của công trình",
    "2.2.1", "2.2.2", "2.2.3", "2.2.4",
    "Bảng 1",
    "2.3. Phân loại công trình theo mục đích an toàn cháy",
    "2.3.1", "2.3.2", "2.3.3", "2.3.4", "2.3.5", "2.3.6",
    "3. TỔ CHỨC THỰC HIỆN",
    "3.1. Quy định chuyển tiếp",
    "3.1.1", "3.1.2", "3.1.3",
    "3.2", "3.3",
    "PHỤ LỤC A",
    "A.1", "A.1.1", "A.1.1.1", "A.1.1.2", "A.1.1.3", "A.1.1.4", "A.1.1.5", "A.1.1.6",
    "A.1.2", "A.1.2.1", "A.1.2.2", "A.1.2.3", "A.1.2.4",
    "A.1.3", "A.1.3.1", "A.1.3.2",
    "A.1.4", "A.1.4.1", "A.1.4.2", "A.1.4.3", "A.1.4.4", "A.1.4.5",
    "A.1.5",
    "A.2", "A.2.1", "A.2.2", "A.2.3", "A.2.4", "A.2.5",
    "A.3"
]

missing_sections = []
for s in expected_sections:
    if s.lower() not in combined_md.lower():
        missing_sections.append(s)

print(f"   - Expected structural landmarks: {len(expected_sections)}")
print(f"   - Missing structural landmarks  : {len(missing_sections)}")
if missing_sections:
    print(f"   ⚠️ Missing: {missing_sections}")
else:
    print("   ✅ ALL structural landmarks and clauses are present 100%!")
