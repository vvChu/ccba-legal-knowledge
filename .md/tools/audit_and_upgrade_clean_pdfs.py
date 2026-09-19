"""Audit and upgrade clean Vector PDFs for legal documents (ADR 0031 & ADR 0043)."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

import fitz  # PyMuPDF
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def calculate_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def is_pdf_scan_only(pdf_path: Path, max_pages: int = 5) -> tuple[bool, int]:
    """Check if PDF has virtually no extractable Unicode text layer."""
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        return True, 0
    try:
        doc = fitz.open(str(pdf_path))
        total_len = 0
        pages_to_check = min(len(doc), max_pages)
        for i in range(pages_to_check):
            total_len += len(doc[i].get_text().strip())
        doc.close()
        # If average length per page is under 15 characters, it is a scan / image
        is_scan = (total_len / max(1, pages_to_check)) < 15
        return is_scan, total_len
    except Exception as e:
        print(f"  [Error reading PDF {pdf_path.name}]: {e}")
        return True, 0


def get_scan_documents(registry_path: Path) -> list[dict[str, Any]]:
    with open(registry_path, "r", encoding="utf-8") as f:
        reg = yaml.safe_load(f)

    docs = reg.get("laws", []) + reg.get("standards", [])
    scan_docs = []

    for d in docs:
        pdf_path_str = d.get("pdf_path")
        if not pdf_path_str:
            continue
        p = Path(pdf_path_str)
        if not p.is_absolute():
            p = registry_path.parent / p
        
        if not p.exists():
            continue

        is_scan, text_len = is_pdf_scan_only(p)
        if is_scan:
            bundle_p = Path(d.get("bundle_path", ""))
            if not bundle_p.is_absolute():
                bundle_p = registry_path.parent / bundle_p
            
            docx_p = p.with_suffix(".docx")
            has_docx = docx_p.exists() and docx_p.stat().st_size > 0

            # Also check if docx is in .md/extracted_docs
            alt_docx = registry_path.parent / ".md" / "extracted_docs" / f"{p.stem}.docx"

            scan_docs.append({
                "id": d["id"],
                "document_number": d.get("document_number", ""),
                "title": d.get("title", ""),
                "pdf_path": p,
                "bundle_path": bundle_p,
                "source_url": d.get("source_url", ""),
                "has_docx": has_docx,
                "docx_path": docx_p if has_docx else (alt_docx if alt_docx.exists() else None),
                "text_len": text_len,
            })
    return scan_docs


def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    reg_file = root_dir / "legal_registry.yaml"

    print("=================================================================")
    print("      AUDIT SCAN-ONLY DOCUMENTS IN LEGAL REPOSITORY             ")
    print("=================================================================")

    scan_docs = get_scan_documents(reg_file)
    print(f"\nTotal Scan-Only Documents Found: {len(scan_docs)}")

    all_docx = list((root_dir / ".md" / "extracted_docs").rglob("*.docx"))
    print(f"Total DOCX in .md/extracted_docs: {len(all_docx)}\n")

    found_docx_count = 0
    missing_docx_count = 0

    for i, s in enumerate(scan_docs, 1):
        docx_file = s["docx_path"]
        
        # If not direct docx, search in extracted_docs
        if not (docx_file and docx_file.exists()):
            slug = s["pdf_path"].stem.lower()
            doc_id = s["id"].lower().replace("-", "_")
            doc_num = s["document_number"].lower().replace("/", "_").replace(":", "_").replace("-", "_")
            
            candidates = []
            for f in all_docx:
                fn = f.name.lower().replace("-", "_")
                fp = str(f).lower().replace("-", "_")
                if doc_id in fn or doc_id in fp or slug in fn or doc_num in fn:
                    candidates.append(f)
            if candidates:
                docx_file = candidates[0]
                s["docx_path"] = docx_file

        if docx_file and docx_file.exists():
            found_docx_count += 1
            status_str = f"FOUND ({docx_file.name})"
        else:
            missing_docx_count += 1
            status_str = "MISSING DOCX"

        print(f"[{i:02d}] {s['id']:<35} | {status_str:<40} | URL: {s['source_url']}")

    print("\n" + "="*65)
    print(f"SUMMARY:")
    print(f"  Total Scan Documents:       {len(scan_docs)}")
    print(f"  Scan Docs WITH DOCX file:   {found_docx_count}")
    print(f"  Scan Docs WITHOUT DOCX file:{missing_docx_count}")
    print("="*65)


if __name__ == "__main__":
    main()
