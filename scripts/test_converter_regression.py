"""CCBA Dynamic Legal Converter Regression Test Suite.

Automatically discovers all legal bundles registered in `legal_registry.yaml`
and verifies that the conversion engine (`docx_converter.py` & `okf_v22_converter.py`)
maintains 100% compliance with OKF v2.2 Pure Normative Body & AST specifications (ADR 0021).
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# Enforce UTF-8 stdout encoding for Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure repository root is on sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.docx_converter import convert_docx_to_okf_bundle


class ConverterRegressionSuite:
    """Dynamic Regression Suite that expands automatically as new documents are registered."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.registry_path = root_dir / "legal_registry.yaml"
        self.extracted_docs_dir = root_dir / ".md" / "extracted_docs"
        self.legal_docs_dir = root_dir / "legal_docs"

    def load_registered_documents(self) -> List[Dict[str, Any]]:
        """Load and return all registered laws, decrees, and circulars."""
        if not self.registry_path.exists():
            print(f"Error: Registry not found at {self.registry_path}", file=sys.stderr)
            return []

        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        laws = data.get("laws", [])
        documents = data.get("documents", {})
        all_docs: List[Dict[str, Any]] = []

        if isinstance(laws, list):
            all_docs.extend(laws)
        if isinstance(documents, dict):
            all_docs.extend(documents.values())

        return all_docs

    def find_source_docx(self, bundle_name: str) -> Optional[Path]:
        """Locate source .docx file in .md/extracted_docs/ or sources/."""
        # 1. Check in .md/extracted_docs/<bundle_name>/
        target_dir = self.extracted_docs_dir / bundle_name
        if target_dir.exists():
            docx_files = list(target_dir.glob("*.docx"))
            if docx_files:
                return docx_files[0]

        # 2. Check in legal_docs/**/<bundle_name>/
        for cat in ["01_vbpl", "02_qcvn", "03_tcvn"]:
            cat_bundle = self.legal_docs_dir / cat / bundle_name
            if cat_bundle.exists():
                docx_files = list(cat_bundle.glob("*.docx"))
                if docx_files:
                    return docx_files[0]

        return None

    def run_suite(
        self,
        bundle_filter: Optional[str] = None,
        apply_conversion: bool = False
    ) -> bool:
        """Run regression tests across all discoverable document bundles."""
        print("==================================================================================")
        print("       CCBA DYNAMIC CONVERTER REGRESSION & SNAPSHOT TEST SUITE                    ")
        print("==================================================================================")
        print(f"Workspace Root    : {self.root_dir}")
        print(f"Mode              : {'APPLY CONVERSION' if apply_conversion else 'AUDIT & VERIFY'}\n")

        all_docs = self.load_registered_documents()
        testable_items: List[Tuple[Dict[str, Any], Path, Path]] = []

        for doc in all_docs:
            bundle_path_str = doc.get("bundle_path", "")
            if not bundle_path_str:
                continue

            bundle_dir = self.root_dir / bundle_path_str
            bundle_name = bundle_dir.name

            if bundle_filter and bundle_filter not in bundle_name:
                continue

            source_docx = self.find_source_docx(bundle_name)
            if source_docx:
                testable_items.append((doc, source_docx, bundle_dir))

        print(f"Discovered {len(testable_items)} registered bundles with source DOCX assets:")
        for doc, docx, b_dir in testable_items:
            print(f"  • [{doc.get('document_number', 'N/A')}] {b_dir.name} (Source: {docx.name})")

        print("\n" + "-" * 95)
        print(f"{'Bundle / Số hiệu':<32} | {'Loại':<12} | {'AST Nodes':<10} | {'Pure Body':<10} | {'Trạng thái'}")
        print("-" * 95)

        passed_count = 0
        failed_count = 0
        skipped_count = 0

        for doc, docx_path, bundle_dir in testable_items:
            doc_num = doc.get("document_number", bundle_dir.name)
            doc_type = doc.get("type", "VBPL")

            if apply_conversion:
                try:
                    convert_docx_to_okf_bundle(
                        docx_path=docx_path,
                        target_bundle_dir=bundle_dir,
                        doc_type=doc_type,
                        registry_file=self.registry_path
                    )
                except Exception as e:
                    print(f"{doc_num[:30]:<32} | {doc_type:<12} | {'ERR':<10} | {'FAIL':<10} | ❌ CONVERT ERROR: {e}")
                    failed_count += 1
                    continue

            # Verify bundle output standards
            primary_md = bundle_dir / f"{bundle_dir.name}.md"
            clauses_json = bundle_dir / "clauses.json"

            if not primary_md.exists():
                md_files = [f for f in bundle_dir.glob("*.md") if f.name not in ("index.md", "dead_ends.md", "log.md")]
                if md_files:
                    primary_md = md_files[0]

            if not primary_md.exists():
                print(f"{doc_num[:30]:<32} | {doc_type:<12} | {'0':<10} | {'MISSING':<10} | ❌ FAIL (No .md)")
                failed_count += 1
                continue

            content = primary_md.read_text(encoding="utf-8")
            body_parts = content.split("---", 2)
            body_text = body_parts[2].strip() if len(body_parts) >= 3 else content
            body_lines = [l.strip() for l in body_text.splitlines() if l.strip()]

            # Pure Normative Body Header & Footer check
            header_noise = False
            footer_noise = False

            header_window = "\n".join(body_lines[:25])
            if "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" in header_window or "Độc lập - Tự do - Hạnh phúc" in header_window:
                header_noise = True

            footer_window = "\n".join(body_lines[-25:]) if len(body_lines) >= 25 else "\n".join(body_lines)
            if re.search(r"(?:^|\n)(?:__\*?\s*Nơi nhận\s*:|\*+Nơi nhận\s*:|\bNơi nhận\s*:|__KT\.\s+BỘ\s+TRƯỞNG|KT\.\s+BỘ\s+TRƯỞNG)", footer_window, re.IGNORECASE):
                footer_noise = True

            pure_status = "✅ PASS" if (not header_noise and not footer_noise) else "⚠️ NOISE"

            # AST count
            ast_count = 0
            if clauses_json.exists():
                try:
                    c_data = json.loads(clauses_json.read_text(encoding="utf-8"))
                    ast_count = len(c_data)
                except Exception:
                    pass

            if not header_noise and not footer_noise and ast_count > 0:
                print(f"{doc_num[:30]:<32} | {doc_type:<12} | {ast_count:<10} | {pure_status:<10} | ✅ PASS")
                passed_count += 1
            else:
                status_note = []
                if header_noise:
                    status_note.append("Header noise")
                if footer_noise:
                    status_note.append("Footer noise")
                if ast_count == 0:
                    status_note.append("0 AST")
                print(f"{doc_num[:30]:<32} | {doc_type:<12} | {ast_count:<10} | {pure_status:<10} | ❌ FAIL ({', '.join(status_note)})")
                failed_count += 1

        print("-" * 95)
        print("📊 TỔNG KẾT KIỂM THỬ HỒI QUY:")
        print(f"  • Tổng số gói kiểm tra: {len(testable_items)}")
        print(f"  • Đạt chuẩn (PASS)   : {passed_count}")
        print(f"  • Cảnh báo / Thất bại : {failed_count}")
        print("==================================================================================")

        return failed_count == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="CCBA Legal Converter Regression Test Suite")
    parser.add_argument("-b", "--bundle", type=str, default=None, help="Filter by bundle name or document number")
    parser.add_argument("--apply", action="store_true", help="Re-run converter across discovered bundles")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    suite = ConverterRegressionSuite(root)
    success = suite.run_suite(bundle_filter=args.bundle, apply_conversion=args.apply)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
