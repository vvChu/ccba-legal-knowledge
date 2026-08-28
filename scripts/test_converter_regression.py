"""CCBA Dynamic Legal Converter Regression Test Suite.

Automatically discovers all legal bundles registered in `legal_registry.yaml`
and verifies that the conversion engine (`docx_converter.py` & `okf_v22_converter.py`)
maintains 100% compliance with OKF v2.2 Pure Normative Body & AST specifications (ADR 0021).
"""

import argparse
import json
import re
import sys
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

from ccba_legal import convert_docx_to_okf_bundle  # noqa: E402


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
        standards = data.get("standards", [])
        documents = data.get("documents", {})
        all_docs: List[Dict[str, Any]] = []

        if isinstance(laws, list):
            all_docs.extend(laws)
        if isinstance(standards, list):
            all_docs.extend(standards)
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

    def _find_testable_items(
        self, bundle_filter: Optional[str] = None
    ) -> List[Tuple[Dict[str, Any], Path, Path]]:
        """Discovers registered bundles that have matching source docx files."""
        all_docs = self.load_registered_documents()
        testable_items: List[Tuple[Dict[str, Any], Path, Path]] = []
        for doc in all_docs:
            bundle_path_str = doc.get("bundle_path", "")
            if not bundle_path_str:
                continue
            bundle_dir = self.root_dir / bundle_path_str
            if bundle_filter and bundle_filter not in bundle_dir.name:
                continue
            source_docx = self.find_source_docx(bundle_dir.name)
            if source_docx:
                testable_items.append((doc, source_docx, bundle_dir))
        return testable_items

    @staticmethod
    def _check_pure_body_noise(body_lines: List[str]) -> Tuple[bool, bool]:
        """Checks for official header noise and signature/recipient footer noise."""
        header_window = "\n".join(body_lines[:25])
        header_noise = (
            "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" in header_window
            or "Độc lập - Tự do - Hạnh phúc" in header_window
        )
        footer_window = "\n".join(body_lines[-25:]) if len(body_lines) >= 25 else "\n".join(body_lines)
        footer_noise = bool(
            re.search(
                r"(?:^|\n)(?:__\*?\s*Nơi nhận\s*:|\*+Nơi nhận\s*:|\bNơi nhận\s*:|__KT\.\s+BỘ\s+TRƯỞNG|KT\.\s+BỘ\s+TRƯỞNG)",
                footer_window,
                re.IGNORECASE,
            )
        )
        return header_noise, footer_noise

    def _verify_bundle_compliance(
        self, doc: Dict[str, Any], docx_path: Path, bundle_dir: Path, apply_conversion: bool
    ) -> Tuple[bool, str]:
        """Runs conversion (if requested) and validates OKF compliance for a single bundle."""
        doc_num = doc.get("document_number", bundle_dir.name)
        doc_type = doc.get("type", "VBPL")

        if apply_conversion:
            try:
                convert_docx_to_okf_bundle(
                    docx_path=docx_path,
                    target_bundle_dir=bundle_dir,
                    doc_type=doc_type,
                    registry_file=self.registry_path,
                )
            except Exception as e:
                return False, f"{doc_num[:30]:<32} | {doc_type:<12} | {'ERR':<10} | {'FAIL':<10} | ❌ CONVERT ERROR: {e}"

        primary_md = bundle_dir / f"{bundle_dir.name}.md"
        if not primary_md.exists():
            md_files = [f for f in bundle_dir.glob("*.md") if f.name not in ("index.md", "dead_ends.md", "log.md")]
            primary_md = md_files[0] if md_files else primary_md

        if not primary_md.exists():
            return False, f"{doc_num[:30]:<32} | {doc_type:<12} | {'0':<10} | {'MISSING':<10} | ❌ FAIL (No .md)"

        content = primary_md.read_text(encoding="utf-8")
        body_parts = content.split("---", 2)
        body_text = body_parts[2].strip() if len(body_parts) >= 3 else content
        body_lines = [line.strip() for line in body_text.splitlines() if line.strip()]

        header_noise, footer_noise = self._check_pure_body_noise(body_lines)
        pure_status = "✅ PASS" if (not header_noise and not footer_noise) else "⚠️ NOISE"

        ast_count = 0
        clauses_json = bundle_dir / "clauses.json"
        if clauses_json.exists():
            try:
                c_data = json.loads(clauses_json.read_text(encoding="utf-8"))
                ast_count = len(c_data) if isinstance(c_data, list) else 0
            except (json.JSONDecodeError, OSError):
                pass

        if not header_noise and not footer_noise and ast_count > 0:
            return True, f"{doc_num[:30]:<32} | {doc_type:<12} | {ast_count:<10} | {pure_status:<10} | ✅ PASS"

        notes = []
        if header_noise:
            notes.append("Header noise")
        if footer_noise:
            notes.append("Footer noise")
        if ast_count == 0:
            notes.append("0 AST")
        return False, f"{doc_num[:30]:<32} | {doc_type:<12} | {ast_count:<10} | {pure_status:<10} | ❌ FAIL ({', '.join(notes)})"

    def run_suite(
        self,
        bundle_filter: Optional[str] = None,
        apply_conversion: bool = False,
    ) -> bool:
        """Run regression tests across all discoverable document bundles."""
        print("==================================================================================")
        print("       CCBA DYNAMIC CONVERTER REGRESSION & SNAPSHOT TEST SUITE                    ")
        print("==================================================================================")
        print(f"Workspace Root    : {self.root_dir}")
        print(f"Mode              : {'APPLY CONVERSION' if apply_conversion else 'AUDIT & VERIFY'}\n")

        testable_items = self._find_testable_items(bundle_filter)
        print(f"Discovered {len(testable_items)} registered bundles with source DOCX assets:")
        for doc, docx, b_dir in testable_items:
            print(f"  • [{doc.get('document_number', 'N/A')}] {b_dir.name} (Source: {docx.name})")

        print("\n" + "-" * 95)
        print(f"{'Bundle / Số hiệu':<32} | {'Loại':<12} | {'AST Nodes':<10} | {'Pure Body':<10} | {'Trạng thái'}")
        print("-" * 95)

        passed_count = 0
        failed_count = 0
        for doc, docx_path, bundle_dir in testable_items:
            passed, log_line = self._verify_bundle_compliance(doc, docx_path, bundle_dir, apply_conversion)
            print(log_line)
            if passed:
                passed_count += 1
            else:
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
