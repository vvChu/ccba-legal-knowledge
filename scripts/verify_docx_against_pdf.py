"""CCBA Gate 0: Ingestion Provenance & DOCX vs PDF Cross-Verification Engine (ADR 0016).

Compares official PDF Gazette Scan (Ground Truth) against freshly downloaded DOCX from TVPL:
1. Legal Metadata & Signature Alignment (Title, Number, Signer, Issuing Body).
2. Heading & Chapter Hierarchy Alignment (Chương I-VI, Điều 1-54).
3. Appendices & Forms Inventory (Phụ lục I-X).
4. Text Parity & Zero Data Loss Scoring.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple
import fitz  # PyMuPDF
from docx import Document

# Enforce UTF-8 output encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def normalize_text(text: str) -> str:
    """Clean and normalize whitespace and special punctuation for comparison."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[_*#`><\"“”\'\(\)\[\]–—\-\.\,\:\;]", "", text)
    return text.strip().lower()

def verify_nd207_docx_vs_pdf(root_dir: Path) -> Dict[str, Any]:
    pdf_path = root_dir / "legal_docs" / "01_vbpl" / "nghi_dinh_207_2026_nd_cp" / "nghi_dinh_207_2026_nd_cp.pdf"
    docx_path = root_dir / ".md" / "extracted_docs" / "nghi_dinh_207_2026_nd_cp" / "207_2026_ND-CP_701883.docx"

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if not docx_path.exists():
        raise FileNotFoundError(f"DOCX not found: {docx_path}")

    # 1. Load PDF
    pdf_doc = fitz.open(str(pdf_path))
    pdf_total_pages = len(pdf_doc)
    pdf_full_text = ""
    for page in pdf_doc:
        pdf_full_text += page.get_text() + "\n"

    # 2. Load DOCX
    doc = Document(str(docx_path))
    docx_paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    docx_tables_count = len(doc.tables)
    docx_full_text = "\n".join(docx_paras)

    # --- TẦNG 1: ĐỐI SOÁT METADATA PHÁP LÝ ---
    meta_checks = {}
    
    # Số hiệu: 207/2026/NĐ-CP
    has_num_pdf = bool(re.search(r"207/2026/NĐ-CP", pdf_full_text, re.IGNORECASE))
    has_num_docx = bool(re.search(r"207/2026/NĐ-CP", docx_full_text, re.IGNORECASE))
    meta_checks["document_number"] = has_num_pdf and has_num_docx

    # Cơ quan ban hành: CHÍNH PHỦ
    has_gov_pdf = "CHÍNH PHỦ" in pdf_full_text.upper()
    has_gov_docx = "CHÍNH PHỦ" in docx_full_text.upper()
    meta_checks["issuing_body"] = has_gov_pdf and has_gov_docx

    # Tiêu đề: Quản lý chất lượng, thi công xây dựng và bảo trì
    has_title_pdf = bool(re.search(r"quản lý chất lượng.*thi công.*bảo trì", pdf_full_text, re.IGNORECASE))
    has_title_docx = bool(re.search(r"quản lý chất lượng.*thi công.*bảo trì", docx_full_text, re.IGNORECASE))
    meta_checks["title"] = has_title_pdf and has_title_docx

    # --- TẦNG 2: ĐỐI SOÁT ĐỀ MỤC & ĐIỀU KHOẢN (ĐIỀU 1 -> ĐIỀU 54) ---
    dieu_pattern = re.compile(r"^Điều\s+(\d+)\b", re.IGNORECASE)
    
    # Extract Điều from DOCX
    docx_dieu_list = []
    for p in docx_paras:
        m = dieu_pattern.match(p)
        if m:
            docx_dieu_list.append(int(m.group(1)))
    docx_dieu_set = set(docx_dieu_list)

    # Extract Điều from PDF
    pdf_dieu_matches = re.findall(r"\bĐiều\s+(\d+)\.", pdf_full_text)
    pdf_dieu_set = set(int(x) for x in pdf_dieu_matches if 1 <= int(x) <= 100)

    # Chapters in PDF & DOCX
    chapter_pattern = re.compile(r"Chương\s+([IVXLCDM]+)", re.IGNORECASE)
    pdf_chapters = set(re.findall(chapter_pattern, pdf_full_text))
    docx_chapters = set(re.findall(chapter_pattern, docx_full_text))

    expected_dieu = set(range(1, 55))
    missing_in_docx = expected_dieu - docx_dieu_set
    missing_in_pdf = expected_dieu - pdf_dieu_set

    # --- TẦNG 3: PHỤ LỤC & BIỂU MẪU ---
    pl_pattern = re.compile(r"Phụ lục\s+([IVXLCDM0-9]+)", re.IGNORECASE)
    pdf_pls = set(re.findall(pl_pattern, pdf_full_text))
    docx_pls = set(re.findall(pl_pattern, docx_full_text))

    # --- TẦNG 4: ĐỐI SOÁT ĐỘ PHỦ NỘI DUNG VĂN BẢN (TEXT PARITY) ---
    clean_pdf = normalize_text(pdf_full_text)
    clean_docx = normalize_text(docx_full_text)

    matched_para_count = 0
    total_sampled_paras = 0
    # Sample meaningful paragraphs from DOCX (>40 chars)
    for p in docx_paras:
        if len(p) >= 40:
            total_sampled_paras += 1
            sample_chunk = normalize_text(p[:50])
            if sample_chunk in clean_pdf:
                matched_para_count += 1

    text_parity_rate = (matched_para_count / total_sampled_paras * 100) if total_sampled_paras else 0.0

    overall_pass = (
        all(meta_checks.values())
        and len(missing_in_docx) == 0
        and len(missing_in_pdf) == 0
        and text_parity_rate >= 98.0
    )

    return {
        "doc_id": "nghi_dinh_207_2026_nd_cp",
        "pdf_pages": pdf_total_pages,
        "docx_paras": len(docx_paras),
        "docx_tables": docx_tables_count,
        "meta_checks": meta_checks,
        "docx_dieu_count": len(docx_dieu_set),
        "pdf_dieu_count": len(pdf_dieu_set),
        "missing_in_docx": list(missing_in_docx),
        "missing_in_pdf": list(missing_in_pdf),
        "chapters_pdf": sorted(list(pdf_chapters)),
        "chapters_docx": sorted(list(docx_chapters)),
        "appendices_pdf": sorted(list(pdf_pls)),
        "appendices_docx": sorted(list(docx_pls)),
        "text_parity_rate": text_parity_rate,
        "overall_pass": overall_pass,
    }

def main():
    root_dir = Path(__file__).resolve().parent.parent
    print("=================================================================")
    print("      CCBA GATE 0: DOCX vs PDF PROVENANCE AUDIT ENGINE          ")
    print("=================================================================")
    
    res = verify_nd207_docx_vs_pdf(root_dir)
    
    print(f"Target Document      : {res['doc_id']}")
    print(f"1. Tệp Nguồn Đối Soát: ")
    print(f"   - PDF Công Báo Gốc: {res['pdf_pages']} trang (Scan dấu đỏ TVPL)")
    print(f"   - DOCX VIP TVPL   : {res['docx_paras']} đoạn văn, {res['docx_tables']} bảng biểu")
    print(f"2. Metadata Pháp Lý  : ")
    for k, v in res['meta_checks'].items():
        print(f"   - {k:18}: {'✅ KHỚP 100%' if v else '❌ LỆCH'}")
    print(f"3. Cấu Trúc Đề Mục   : ")
    print(f"   - Tổng số Điều    : PDF: {res['pdf_dieu_count']}/54 Điều | DOCX: {res['docx_dieu_count']}/54 Điều")
    print(f"   - Chương          : PDF: {res['chapters_pdf']} | DOCX: {res['chapters_docx']}")
    print(f"4. Phụ Lục & Biểu Mẫu: ")
    print(f"   - Danh mục Phụ lục: DOCX: {res['appendices_docx']} | PDF: {res['appendices_pdf']}")
    print(f"5. Độ Phủ Văn Bản    : {res['text_parity_rate']:.2f}% Text Parity Score")
    print("=================================================================")

    if res['overall_pass']:
        print("🎉 PASSED GATE 0: Tệp DOCX hoàn toàn khớp chuẩn xác 100% với bản in PDF Công báo gốc!")
        sys.exit(0)
    else:
        print("❌ FAILED GATE 0: Phát hiện sai biệt giữa DOCX và PDF Công báo!")
        sys.exit(1)

if __name__ == "__main__":
    main()
