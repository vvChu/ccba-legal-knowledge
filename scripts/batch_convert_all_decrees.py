"""Batch convert all 7 authentic Decree docx files to OKF v0.2 Markdown bundles."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.docx_converter import convert_docx_to_okf_bundle

DECREE_FILES = [
    ("nghi_dinh_217_2026_nd_cp", "217_2026_ND-CP_696494.docx"),
    ("nghi_dinh_207_2026_nd_cp", "207_2026_ND-CP_701883.docx"),
    ("nghi_dinh_212_2026_nd_cp", "212_2026_ND-CP_697287.docx"),
    ("nghi_dinh_206_2026_nd_cp", "206_2026_ND-CP_457659.docx"),
    ("nghi_dinh_210_2026_nd_cp", "210_2026_ND-CP_696691.docx"),
    ("nghi_dinh_209_2026_nd_cp", "209_2026_ND-CP_288496.docx"),
    ("nghi_dinh_193_2026_nd_cp", "193_2026_ND-CP_709388.docx"),
]

def batch_convert():
    root_dir = Path(__file__).resolve().parent.parent
    extracted_base = root_dir / ".md" / "extracted_docs"
    bundle_base = root_dir / "legal_docs" / "01_vbpl"

    results = []
    print("=================================================================")
    print("       BATCH DECREES OKF BUNDLE CONVERSION ENGINE               ")
    print("=================================================================\n")

    for slug, docx_filename in DECREE_FILES:
        docx_path = extracted_base / slug / docx_filename
        target_bundle_dir = bundle_base / slug

        if not docx_path.exists():
            print(f"❌ [MISSING]: {docx_path}")
            continue

        print(f"\n---> Processing {slug} ({docx_filename})...")
        res = convert_docx_to_okf_bundle(
            docx_path=docx_path,
            target_bundle_dir=target_bundle_dir,
            output_filename=f"{slug}.md",
            doc_type="vbpl",
        )
        md_file = target_bundle_dir / f"{slug}.md"
        size_kb = md_file.stat().st_size / 1024 if md_file.exists() else 0
        res["size_kb"] = size_kb
        results.append((slug, res))

    print("\n=================================================================")
    print("CONVERSION SUMMARY REPORT:")
    print("=================================================================")
    for slug, res in results:
        print(f"✅ {slug:<30}: Size={res['size_kb']:.1f} KB | Clauses={res.get('clauses_count', 0)} | QA={res.get('qa_count', 0)}")

if __name__ == "__main__":
    batch_convert()
