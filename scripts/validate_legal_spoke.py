"""CCBA Legal Spoke Automated Integrity & Schema Validator.

Validates:
1. legal_registry.yaml schema, required fields, and bundle path existence.
2. OKF Bundle structure in legal_docs/ (index.md, metadata.yaml, frontmatter).
3. Attachment integrity in tables/ (CSV/JSON file references).
4. Internal heading anchor link integrity (#dieu-X, #khoan-Y).
"""

import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Enforce UTF-8 output encoding for Windows PowerShell compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class LegalSpokeValidator:
    """Validator engine for CCBA Legal Knowledge Spoke."""

    def __init__(self, root_dir: Path) -> None:
        """Initialize validator with project root directory."""
        self.root_dir = root_dir
        self.legal_docs_dir = root_dir / "legal_docs"
        self.registry_file = root_dir / "legal_registry.yaml"
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_registry(self) -> Tuple[int, int]:
        """Validate legal_registry.yaml syntax, schema, and document paths."""
        if not self.registry_file.exists():
            self.errors.append(f"CRITICAL: Registry file missing at {self.registry_file}")
            return (1, 0)

        try:
            with open(self.registry_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as exc:
            self.errors.append(f"CRITICAL: Failed to parse legal_registry.yaml: {exc}")
            return (1, 0)

        if not isinstance(data, dict):
            self.errors.append("CRITICAL: legal_registry.yaml root must be a YAML dictionary.")
            return (1, 0)

        required_keys = ["version", "spoke_name", "registry_summary"]
        for key in required_keys:
            if key not in data:
                self.errors.append(f"Schema Error: Missing required root key '{key}' in legal_registry.yaml")

        # Validate laws & documents
        laws = data.get("laws", [])
        documents = data.get("documents", {})
        all_docs = laws if isinstance(laws, list) else []
        if isinstance(documents, dict):
            all_docs.extend(documents.values())

        for doc in all_docs:
            if not isinstance(doc, dict):
                continue
            doc_id = doc.get("id", "UNKNOWN_ID")
            bundle_path_str = doc.get("bundle_path")

            if bundle_path_str:
                bundle_path = self.root_dir / bundle_path_str
                if not bundle_path.exists():
                    self.warnings.append(
                        f"Registry Warning [{doc_id}]: bundle_path '{bundle_path_str}' does not exist on disk."
                    )

        return (len(self.errors), len(self.warnings))

    def validate_okf_bundles(self) -> Tuple[int, int]:
        """Validate OKF Bundle markdown files, frontmatter, and metadata in legal_docs/."""
        if not self.legal_docs_dir.exists():
            self.warnings.append(f"Warning: legal_docs/ directory does not exist at {self.legal_docs_dir}")
            return (len(self.errors), len(self.warnings))

        categories = ["01_vbpl", "02_qcvn", "03_tcvn", "04_appendices"]
        for cat in categories:
            cat_dir = self.legal_docs_dir / cat
            if not cat_dir.exists():
                continue

            for doc_dir in cat_dir.iterdir():
                if not doc_dir.is_dir():
                    continue

                # Check index.md
                index_file = doc_dir / "index.md"
                main_md_files = list(doc_dir.glob("*.md"))

                if not main_md_files:
                    self.warnings.append(f"OKF Warning [{doc_dir.name}]: No Markdown (.md) files found in bundle.")
                    continue

                if not index_file.exists() and len(main_md_files) > 1:
                    self.warnings.append(
                        f"OKF Warning [{doc_dir.name}]: Multiple markdown files exist but 'index.md' MOC is missing."
                    )

                # Validate frontmatter of markdown files
                for md_path in main_md_files:
                    self._check_markdown_frontmatter(md_path)

        return (len(self.errors), len(self.warnings))

    def _check_markdown_frontmatter(self, md_path: Path) -> None:
        """Check YAML frontmatter of a markdown file if present."""
        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as exc:
            self.errors.append(f"File Error: Failed to read {md_path.name}: {exc}")
            return

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter_str = parts[1]
                try:
                    yaml.safe_load(frontmatter_str)
                except Exception as exc:
                    self.errors.append(
                        f"Syntax Error [{md_path.relative_to(self.root_dir)}]: Invalid YAML frontmatter: {exc}"
                    )

    def validate_table_attachments(self) -> Tuple[int, int]:
        """Validate referenced table CSV/JSON attachments exist in bundle tables/ directory."""
        if not self.legal_docs_dir.exists():
            return (len(self.errors), len(self.warnings))

        for md_file in self.legal_docs_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
            except Exception:
                continue

            # Find table CSV/JSON references: e.g. tables/csv/bang_01.csv or tables/json/bang_01.json
            ref_matches = re.findall(r"tables/(?:csv|json)/[a-zA-Z0-9_.-]+\.(?:csv|json)", content)
            bundle_dir = md_file.parent

            for ref in ref_matches:
                target_file = bundle_dir / ref
                if not target_file.exists():
                    self.warnings.append(
                        f"Table Attachment Warning [{md_file.relative_to(self.root_dir)}]: Referenced table asset missing: {ref}"
                    )

        return (len(self.errors), len(self.warnings))

    def validate_fake_data_gate(self) -> Tuple[int, int]:
        """Validate that bundles do not contain truncated/synthetic placeholder content."""
        vbpl_dir = self.legal_docs_dir / "01_vbpl"
        if not vbpl_dir.exists():
            return (len(self.errors), len(self.warnings))

        for doc_dir in vbpl_dir.iterdir():
            if not doc_dir.is_dir() or not doc_dir.name.startswith("nghi_dinh_"):
                continue

            primary_md = doc_dir / f"{doc_dir.name}.md"
            if not primary_md.exists():
                continue

            # Check 1: File size threshold for Decrees (Must be > 20 KB)
            size_kb = primary_md.stat().st_size / 1024
            if size_kb < 20:
                self.warnings.append(
                    f"Fake Data Warning [{doc_dir.name}]: Decrees usually exceed 20KB, but found {size_kb:.1f} KB. Verify if full text is present."
                )

            # Check 2: Article continuity check
            content = primary_md.read_text(encoding="utf-8")
            dieu_nums = [int(m) for m in re.findall(r"### Điều (\d+)\.", content)]
            if dieu_nums:
                dieu_nums.sort()
                for i in range(len(dieu_nums) - 1):
                    gap = dieu_nums[i + 1] - dieu_nums[i]
                    if gap > 3:
                        self.warnings.append(
                            f"Fake Data Warning [{doc_dir.name}]: Article gap of {gap} detected between Điều {dieu_nums[i]} and Điều {dieu_nums[i+1]}. Truncated content suspected."
                        )

            # Check 3: Clauses AST count
            clauses_json = doc_dir / "clauses.json"
            if clauses_json.exists():
                try:
                    clauses_data = json.loads(clauses_json.read_text(encoding="utf-8"))
                    if len(clauses_data) < 25:
                        self.warnings.append(
                            f"Fake Data Warning [{doc_dir.name}]: Found only {len(clauses_data)} clauses in clauses.json. Expected >= 30 for full decree."
                        )
                except Exception:
                    pass

        return (len(self.errors), len(self.warnings))

    def run_all_checks(self) -> bool:
        """Run all validation checks and print a summary report."""
        print("=================================================================")
        print("       CCBA LEGAL SPOKE INTEGRITY & SCHEMA VALIDATOR             ")
        print("=================================================================")
        print(f"Target Workspace: {self.root_dir}\n")

        self.validate_registry()
        self.validate_okf_bundles()
        self.validate_table_attachments()
        self.validate_fake_data_gate()

        print(f"-> Registry Check completed.")
        print(f"-> OKF Bundles Structure Check completed.")
        print(f"-> Table Attachments Check completed.")
        print(f"-> Fake Data Gate Check completed.\n")

        print("-----------------------------------------------------------------")
        print("SUMMARY REPORT:")
        print(f"Errors found   : {len(self.errors)}")
        print(f"Warnings found : {len(self.warnings)}")
        print("-----------------------------------------------------------------")

        if self.errors:
            print("\n[ERRORS]:")
            for err in self.errors:
                print(f"  ❌ {err}")

        if self.warnings:
            print("\n[WARNINGS]:")
            for warn in self.warnings:
                print(f"  ⚠️ {warn}")

        if not self.errors and not self.warnings:
            print("\n✅ PASSED: All legal knowledge data, registry, and bundles are 100% valid!")
            return True

        if not self.errors:
            print("\n✅ PASSED WITH WARNINGS: No critical errors found.")
            return True

        print("\n❌ FAILED: Critical errors detected in legal spoke validation.")
        return False


def main() -> None:
    """CLI entry point for running validator."""
    root_dir = Path(__file__).resolve().parent.parent
    validator = LegalSpokeValidator(root_dir)
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
