"""CCBA Gate 0: Universal Ingestion Provenance & DOCX vs PDF Cross-Verification Engine (ADR 0016).

Compares official PDF Gazette Scan (Ground Truth) against freshly downloaded DOCX from TVPL:
1. Legal Metadata & Signature Alignment (Title, Number, Signer, Issuing Body).
2. Heading & Chapter Hierarchy Alignment (Chương I-n, Điều 1-n / Section 1.1-n).
3. Appendices & Forms Inventory (Phụ lục I-n).
4. Text Parity & Zero Data Loss Scoring across any registered bundle.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

from ccba_legal.provenance import (
    find_bundle_assets,
    verify_bundle_docx_vs_pdf,
)

# Enforce UTF-8 output encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    """CLI runner for Universal Gate 0 Ingestion Provenance."""
    parser = argparse.ArgumentParser(description="CCBA Universal Gate 0: DOCX vs PDF Provenance Audit")
    parser.add_argument("-b", "--bundle", type=str, default=None, help="Specific bundle slug to audit")
    parser.add_argument("--all", action="store_true", help="Audit all discoverable bundles with DOCX+PDF assets")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent.parent
    legal_docs = root_dir / "legal_docs"

    print("=================================================================")
    print("      CCBA UNIVERSAL GATE 0: DOCX vs PDF PROVENANCE AUDIT        ")
    print("=================================================================")

    target_bundles: List[Path] = []
    if args.bundle:
        for cat in ["01_vbpl", "02_qcvn", "03_tcvn"]:
            candidate = legal_docs / cat / args.bundle
            if candidate.exists():
                target_bundles.append(candidate)
                break
    else:
        # Default or --all: scan all categories
        for cat in ["01_vbpl", "02_qcvn", "03_tcvn"]:
            cat_dir = legal_docs / cat
            if cat_dir.exists():
                for b in cat_dir.iterdir():
                    if b.is_dir() and not b.name.startswith("."):
                        p_path, d_path = find_bundle_assets(root_dir, b)
                        if p_path and d_path:
                            target_bundles.append(b)

    if not target_bundles:
        print("⚠️ Không tìm thấy gói văn bản nào có đủ tài sản DOCX và PDF để đối soát.")
        return 0

    print(f"Phát hiện {len(target_bundles)} gói văn bản có tài sản DOCX + PDF:\n")
    all_passed = True
    for b in target_bundles:
        res = verify_bundle_docx_vs_pdf(root_dir, b)
        if "error" in res:
            print(f"❌ [{b.name}]: {res['error']}")
            all_passed = False
            continue

        status_str = "✅ PASS" if res["overall_pass"] else "❌ FAIL"
        print(f"• [{b.name[:35]:<35}] | PDF: {res['pdf_pages']:<3} trang | DOCX: {res['docx_paras']:<4} đoạn | Parity: {res['text_parity_rate']:.1f}% | {status_str}")
        if not res["overall_pass"]:
            all_passed = False
            if res["missing_in_docx"]:
                print(f"  └─ Missing in DOCX: {res['missing_in_docx']}")

    print("=================================================================")
    if all_passed:
        print("🎉 PASSED GATE 0: 100% tệp DOCX khớp chuẩn xác với PDF Công báo gốc!")
        return 0
    else:
        print("❌ FAILED GATE 0: Phát hiện sai biệt dữ liệu giữa DOCX và PDF.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

