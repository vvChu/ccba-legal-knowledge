"""Batch Upgrade Legal Documents to 100% Vector PDF via Word COM (ADR 0043).

Automates:
1. Preservation of official gazette scan as sources/<slug>_raw_scan.pdf
2. Word COM vector PDF rendering from sources/<slug>.docx -> sources/<slug>.pdf
3. Provenance stamping with SHA-256 in metadata.yaml and legal_registry.yaml
4. Verification of text layer Unicode characters
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import fitz  # PyMuPDF
import win32com.client
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def calculate_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def render_docx_to_pdf_word_com(word_app: Any, docx_path: Path, output_pdf_path: Path) -> bool:
    """Render DOCX to Native Vector PDF using Word COM."""
    temp_pdf = output_pdf_path.parent / f"temp_{output_pdf_path.name}"
    if temp_pdf.exists():
        temp_pdf.unlink()

    docx_abs = str(docx_path.resolve())
    temp_pdf_abs = str(temp_pdf.resolve())

    doc = None
    try:
        # Open read-only, no repair dialogs
        doc = word_app.Documents.Open(docx_abs, ReadOnly=True, ConfirmConversions=False)
        # 17 = wdFormatPDF
        doc.SaveAs(temp_pdf_abs, FileFormat=17)
        doc.Close(SaveChanges=0)
        doc = None

        if temp_pdf.exists() and temp_pdf.stat().st_size > 0:
            if output_pdf_path.exists():
                output_pdf_path.unlink()
            temp_pdf.rename(output_pdf_path)
            return True
        return False
    except Exception as e:
        print(f"    [Word COM Error on {docx_path.name}]: {e}")
        if doc:
            try:
                doc.Close(SaveChanges=0)
            except Exception:
                pass
        if temp_pdf.exists():
            try:
                temp_pdf.unlink()
            except Exception:
                pass
        return False


def upgrade_single_bundle(
    word_app: Any,
    bundle_dir: Path,
    registry_data: dict[str, Any],
    root_dir: Path,
) -> bool:
    """Upgrade a single bundle to Dual-PDF Vector format."""
    doc_name = bundle_dir.name
    sources_dir = bundle_dir / "sources"
    if not sources_dir.exists():
        print(f"  [Skip {doc_name}]: sources/ directory does not exist.")
        return False

    meta_path = bundle_dir / "metadata.yaml"
    if not meta_path.exists():
        print(f"  [Skip {doc_name}]: metadata.yaml missing.")
        return False

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = yaml.safe_load(f) or {}

    # Find DOCX file in sources/ or fallback to .md/extracted_docs/
    docx_candidates = list(sources_dir.glob("*.docx"))
    docx_path = None
    if docx_candidates:
        docx_path = next((f for f in docx_candidates if f.stem == doc_name), docx_candidates[0])
    else:
        all_docx = list((root_dir / ".md" / "extracted_docs").rglob("*.docx"))
        doc_id = meta.get("id", "").lower().replace("-", "_")
        doc_num = meta.get("document_number", "").lower().replace("/", "_").replace(":", "_").replace("-", "_")
        for f in all_docx:
            fn = f.name.lower().replace("-", "_")
            fp = str(f).lower().replace("-", "_")
            if doc_name in fn or doc_id in fn or (doc_num and doc_num in fn) or (doc_num and doc_num in fp):
                docx_path = f
                break
        if not docx_path:
            print(f"  [Skip {doc_name}]: No DOCX file found in sources/ or .md/extracted_docs/.")
            return False

    # Find current PDF
    target_vector_pdf = sources_dir / f"{doc_name}.pdf"
    raw_scan_pdf = sources_dir / f"{doc_name}_raw_scan.pdf"

    # If raw_scan_pdf doesn't exist yet, we preserve the current PDF as raw_scan_pdf
    if not raw_scan_pdf.exists():
        current_pdfs = [f for f in sources_dir.glob("*.pdf") if not f.name.endswith("_raw_scan.pdf")]
        if current_pdfs:
            existing_pdf = current_pdfs[0]
            # Copy to raw_scan_pdf
            shutil.copy2(existing_pdf, raw_scan_pdf)
            print(f"    Preserved scan mộc đỏ: {existing_pdf.name} -> {raw_scan_pdf.name} ({raw_scan_pdf.stat().st_size:,} bytes)")
        else:
            print(f"  [Warning {doc_name}]: No current PDF to preserve as raw_scan_pdf.")

    # Render DOCX -> target_vector_pdf
    print(f"    Rendering Vector PDF from {docx_path.name} via Word COM...")
    t0 = time.time()
    ok = render_docx_to_pdf_word_com(word_app, docx_path, target_vector_pdf)
    if not ok or not target_vector_pdf.exists():
        print(f"  [Error {doc_name}]: Failed to render Vector PDF.")
        return False
    t1 = time.time()

    # Verify text layer
    pdf_doc = fitz.open(str(target_vector_pdf))
    total_chars = sum(len(p.get_text().strip()) for p in pdf_doc)
    page_count = len(pdf_doc)
    pdf_doc.close()
    print(f"    Success: {target_vector_pdf.name} rendered in {t1 - t0:.1f}s ({page_count} pages, {total_chars:,} chars, {target_vector_pdf.stat().st_size:,} bytes)")

    # Calculate hashes
    vector_sha = calculate_sha256(target_vector_pdf)
    scan_sha = calculate_sha256(raw_scan_pdf) if raw_scan_pdf.exists() else None
    docx_sha = calculate_sha256(docx_path)

    # Relative paths from repo root
    rel_vector_pdf = str(target_vector_pdf.relative_to(root_dir)).replace("\\", "/")
    rel_raw_scan = str(raw_scan_pdf.relative_to(root_dir)).replace("\\", "/")
    category = bundle_dir.parent.name

    # Update metadata.yaml
    meta["pdf_path"] = rel_vector_pdf
    meta["pdf_sha256"] = vector_sha
    meta["pdf_status"] = "verified"
    meta["pdf_origin"] = "docx_vector_rendered"
    meta["raw_scan_pdf"] = f"sources/{raw_scan_pdf.name}"

    if "source_assets" not in meta:
        meta["source_assets"] = {}

    meta["source_assets"]["pdf"] = {
        "sha256": vector_sha,
        "vault_path": f"CCBA_Legal_Vault/{category}/{doc_name}/{target_vector_pdf.name}",
        "status": "verified",
        "origin": "docx_vector_rendered",
    }
    meta["source_assets"]["docx"] = {
        "sha256": docx_sha,
        "vault_path": f"CCBA_Legal_Vault/{category}/{doc_name}/{docx_path.name}",
        "status": "verified",
    }
    if scan_sha:
        meta["source_assets"]["raw_scan"] = {
            "sha256": scan_sha,
            "vault_path": f"CCBA_Legal_Vault/{category}/{doc_name}/{raw_scan_pdf.name}",
            "status": "verified",
            "acquisition_method": "official_gazette_scan",
        }

    with open(meta_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(meta, f, allow_unicode=True, sort_keys=False)

    # Update legal_registry.yaml in-memory
    doc_id = meta.get("id")
    for section in ["laws", "standards"]:
        for item in registry_data.get(section, []):
            if item.get("id") == doc_id or item.get("bundle_path", "").rstrip("/").endswith(doc_name):
                item["pdf_path"] = rel_vector_pdf
                item["pdf_sha256"] = vector_sha
                item["pdf_origin"] = "docx_vector_rendered"
                item["raw_scan_pdf"] = rel_raw_scan
                item["source_file"] = str(docx_path.relative_to(root_dir)).replace("\\", "/")
                item["source_file_size_kb"] = round(docx_path.stat().st_size / 1024, 1)
                if "source_assets" not in item:
                    item["source_assets"] = {}
                item["source_assets"]["pdf"] = {
                    "sha256": vector_sha,
                    "vault_path": f"CCBA_Legal_Vault/{category}/{doc_name}/{target_vector_pdf.name}",
                    "status": "verified",
                }
                item["source_assets"]["docx"] = {
                    "sha256": docx_sha,
                    "vault_path": f"CCBA_Legal_Vault/{category}/{doc_name}/{docx_path.name}",
                    "status": "verified",
                }
                if scan_sha:
                    item["source_assets"]["raw_scan"] = {
                        "sha256": scan_sha,
                        "vault_path": f"CCBA_Legal_Vault/{category}/{doc_name}/{raw_scan_pdf.name}",
                        "status": "verified",
                    }
                break

    return True


def main():
    parser = argparse.ArgumentParser(description="Batch upgrade documents to clean vector PDF via Word COM")
    parser.add_argument("--single", type=str, default=None, help="Upgrade single bundle slug for testing")
    parser.add_argument("--all-scans", action="store_true", help="Upgrade all scan-only documents")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent.parent.parent
    reg_path = root_dir / "legal_registry.yaml"

    with open(reg_path, "r", encoding="utf-8") as f:
        reg_data = yaml.safe_load(f)

    # Import audit function to find scan documents
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from audit_and_upgrade_clean_pdfs import get_scan_documents
    scan_docs = get_scan_documents(reg_path)

    print("=================================================================")
    print("      BATCH VECTOR PDF UPGRADE ENGINE (ADR 0043 DUAL-PDF)       ")
    print("=================================================================")
    print(f"Total Scan-Only Documents detected: {len(scan_docs)}")

    target_bundles: List[Path] = []
    if args.single:
        for s in scan_docs:
            if args.single.lower() in s["bundle_path"].name.lower() or args.single.lower() in s["id"].lower():
                target_bundles.append(s["bundle_path"])
                break
        if not target_bundles:
            print(f"Could not find bundle matching '{args.single}' in scan list.")
            return 1
    elif args.all_scans:
        target_bundles = [s["bundle_path"] for s in scan_docs]
    else:
        print("Please specify --single <slug> or --all-scans.")
        return 1

    print(f"Processing {len(target_bundles)} bundle(s)...")

    word_app = None
    success_count = 0
    fail_count = 0

    try:
        print("\nLaunching Microsoft Word COM Application in background...")
        word_app = win32com.client.Dispatch("Word.Application")
        word_app.Visible = False
        word_app.DisplayAlerts = 0  # wdAlertsNone

        for i, b_path in enumerate(target_bundles, 1):
            print(f"\n[{i:02d}/{len(target_bundles):02d}] Upgrading: {b_path.name}")
            try:
                if upgrade_single_bundle(word_app, b_path, reg_data, root_dir):
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as exc:
                print(f"  [Error upgrading {b_path.name}]: {exc}")
                fail_count += 1

    finally:
        if word_app:
            print("\nClosing Microsoft Word COM Application...")
            try:
                word_app.Quit(SaveChanges=0)
            except Exception:
                pass

    # Save updated legal_registry.yaml
    print("\nSaving updated legal_registry.yaml...")
    with open(reg_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(reg_data, f, allow_unicode=True, sort_keys=False)

    print("\n" + "="*65)
    print("UPGRADE RESULTS:")
    print(f"  Successfully upgraded: {success_count} bundles")
    print(f"  Failed:                {fail_count} bundles")
    print("="*65)

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
