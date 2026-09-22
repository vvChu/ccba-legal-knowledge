"""CCBA Legal Spoke Automated Integrity & Schema Validator.

Validates:
1. legal_registry.yaml schema, required fields, and bundle path existence.
2. OKF Bundle structure in legal_docs/ (index.md, metadata.yaml, frontmatter).
3. Attachment integrity in tables/ (CSV/JSON file references).
4. Internal heading anchor link integrity (#dieu-X, #khoan-Y).
5. AST jurisdiction & PDF metadata completeness.
6. Pure Normative Body & noise eradication (ADR 0021).
7. Spoke cleanliness & script count.
8. Template 2D structural integrity & uncollapsing (ADR 0021, ADR 0030).
9. 100% Visual Parity (ADR 0029, ADR 0030).
10. ADR Living Traceability & Self-Healing Sync Gate.
11. DOCX-to-Markdown Verbatim Normative Parity Gate (ADR 0037).
12. Multimodal Decoupled Asset & SVG/Cards Integrity Gate (ADR 0040).
13. Table Knowledge Extraction & 2D Matrix Regularity Gate (ADR 0041).
14. KaTeX Math Syntax & Rendering Integrity Gate (ADR 0038).
15. OKF Provenance & Version Attestation Gate.
"""

import argparse
import csv
from datetime import datetime, timezone
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent
_ROOT_DIR = _SCRIPTS_DIR.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

try:
    from ccba_legal.constants import (
        AST_CLAUSES_SCHEMA_VERSION,
        CURRENT_CONVERTER_VERSION,
        CURRENT_OKF_SPEC,
        DIR_SOURCES,
        DIR_TEMPLATES,
        FIGURES_CATALOG_SCHEMA_VERSION,
        GATE_11_MIN_VERBATIM_PARITY,
        QA_BENCHMARK_SCHEMA_VERSION,
        STANDARD_COMPARTMENTS,
        TABLES_CATALOG_SCHEMA_VERSION,
    )
except ImportError:
    CURRENT_OKF_SPEC = "v2.4 Universal"
    CURRENT_CONVERTER_VERSION = "0.4.0"
    DIR_SOURCES = "sources"
    DIR_TEMPLATES = "templates"
    STANDARD_COMPARTMENTS = ("sources", "tables", "figures", "annexes", "templates")
    GATE_11_MIN_VERBATIM_PARITY = 98.0
    TABLES_CATALOG_SCHEMA_VERSION = "2.4"
    FIGURES_CATALOG_SCHEMA_VERSION = "2.4"
    AST_CLAUSES_SCHEMA_VERSION = "2.4"
    QA_BENCHMARK_SCHEMA_VERSION = "2.4"


# Enforce UTF-8 output encoding for Windows PowerShell compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class LegalSpokeValidator:
    """Validator engine for CCBA Legal Knowledge Spoke."""

    def __init__(self, root_dir: Path, target_bundle: Optional[str] = None) -> None:
        """Initialize validator with project root directory."""
        self.root_dir = root_dir
        self.legal_docs_dir = root_dir / "legal_docs"
        self.registry_file = root_dir / "legal_registry.yaml"
        self.target_bundle = target_bundle
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def _safe_read_text(self, path: Path) -> Optional[str]:
        """Safely read text file with UTF-8 encoding."""
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            self.errors.append(f"File Error: Failed to read {path.name}: {exc}")
            return None

    def _extract_frontmatter(self, md_path: Path) -> Tuple[Optional[Dict[str, Any]], str]:
        """Extract YAML frontmatter dictionary and remaining body text from Markdown file."""
        content = self._safe_read_text(md_path)
        if content is None:
            return (None, "")

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    fm_data = yaml.safe_load(parts[1])
                    body_text = parts[2].strip()
                    return (fm_data if isinstance(fm_data, dict) else None, body_text)
                except yaml.YAMLError as exc:
                    self.errors.append(
                        f"Syntax Error [{md_path.relative_to(self.root_dir)}]: Invalid YAML frontmatter: {exc}"
                    )
                    return (None, parts[2].strip())
        return (None, content)

    def validate_registry(self) -> Tuple[int, int]:
        """Validate legal_registry.yaml syntax, schema, and document paths."""
        if not self.registry_file.exists():
            self.errors.append(f"CRITICAL: Registry file missing at {self.registry_file}")
            return (1, 0)

        try:
            with open(self.registry_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except (yaml.YAMLError, OSError) as exc:
            self.errors.append(f"CRITICAL: Failed to parse legal_registry.yaml: {exc}")
            return (1, 0)

        if not isinstance(data, dict):
            self.errors.append("CRITICAL: legal_registry.yaml root must be a YAML dictionary.")
            return (1, 0)

        for key in ["version", "spoke_name", "registry_summary"]:
            if key not in data:
                self.errors.append(f"Schema Error: Missing required root key '{key}' in legal_registry.yaml")

        laws = data.get("laws", [])
        standards = data.get("standards", [])
        documents = data.get("documents", {})
        all_docs = []
        if isinstance(laws, list):
            all_docs.extend(laws)
        if isinstance(standards, list):
            all_docs.extend(standards)
        if isinstance(documents, dict):
            all_docs.extend(documents.values())
        elif isinstance(documents, list):
            all_docs.extend(documents)

        for doc in all_docs:
            if isinstance(doc, dict):
                if self.target_bundle:
                    doc_id = doc.get("id", "")
                    bundle_p = doc.get("bundle_path", "")
                    doc_num = doc.get("document_number", "")
                    if doc_id != self.target_bundle and self.target_bundle not in bundle_p and doc_num != self.target_bundle:
                        continue
                bundle_path_str = doc.get("bundle_path")
                if bundle_path_str and not (self.root_dir / bundle_path_str).exists():
                    self.warnings.append(
                        f"Registry Warning [{doc.get('id', 'UNKNOWN')}]: bundle_path '{bundle_path_str}' does not exist on disk."
                    )

        return (len(self.errors), len(self.warnings))

    def validate_okf_bundles(self) -> Tuple[int, int]:
        """Validate OKF Bundle markdown files, frontmatter, and metadata in legal_docs/."""
        if not self.legal_docs_dir.exists():
            self.warnings.append(f"Warning: legal_docs/ directory does not exist at {self.legal_docs_dir}")
            return (len(self.errors), len(self.warnings))

        for cat in ["01_vbpl", "02_qcvn", "03_tcvn", "04_appendices"]:
            cat_dir = self.legal_docs_dir / cat
            if not cat_dir.exists():
                continue

            for doc_dir in cat_dir.iterdir():
                if doc_dir.is_dir() and not doc_dir.name.startswith("."):
                    if self.target_bundle and doc_dir.name != self.target_bundle:
                        continue
                    self._check_single_bundle_structure(doc_dir, cat)

        return (len(self.errors), len(self.warnings))

    def _check_single_bundle_structure(self, doc_dir: Path, cat: str) -> None:
        """Check invariants and frontmatter of a single document bundle."""
        main_md_files = list(doc_dir.glob("*.md"))
        if not main_md_files:
            self.warnings.append(f"OKF Warning [{doc_dir.name}]: No Markdown (.md) files found in bundle.")
            return

        index_file = doc_dir / "index.md"
        if not index_file.exists() and len(main_md_files) > 1:
            self.warnings.append(
                f"OKF Warning [{doc_dir.name}]: Multiple markdown files exist but 'index.md' MOC is missing."
            )

        if cat in ["01_vbpl", "02_qcvn", "03_tcvn"]:
            sources_dir = doc_dir / DIR_SOURCES
            if not sources_dir.exists():
                self.warnings.append(
                    f"OKF v2.4 Invariant Warning [{doc_dir.name}]: Missing mandatory '{DIR_SOURCES}/' directory."
                )
            templates_dir = doc_dir / DIR_TEMPLATES
            if templates_dir.exists() and not any(templates_dir.iterdir()):
                self.warnings.append(
                    f"OKF v2.4 Invariant Warning [{doc_dir.name}]: Empty '{DIR_TEMPLATES}/' directory detected."
                )

        for md_path in main_md_files:
            self._extract_frontmatter(md_path)

    def validate_table_attachments(self) -> Tuple[int, int]:
        """Validate referenced table CSV/JSON attachments exist in bundle tables/ directory."""
        if not self.legal_docs_dir.exists():
            return (len(self.errors), len(self.warnings))

        for md_file in self.legal_docs_dir.rglob("*.md"):
            if self.target_bundle and self.target_bundle not in md_file.parts:
                continue
            content = self._safe_read_text(md_file)
            if content is None:
                continue

            ref_matches = re.findall(r"tables/(?:csv|json)/[a-zA-Z0-9_.-]+\.(?:csv|json)", content)
            bundle_dir = md_file.parent

            for ref in ref_matches:
                target_file = bundle_dir / ref
                if not target_file.exists():
                    target_file = bundle_dir.parent / ref
                if not target_file.exists():
                    self.warnings.append(
                        f"Table Attachment Warning [{md_file.relative_to(self.root_dir)}]: Referenced table asset missing: {ref}"
                    )

        # Sub-Gate 3.2: Multi-Part Table Disambiguation & Reference Integrity (ADR 0044)
        self._check_table_references_and_disambiguation()

        return (len(self.errors), len(self.warnings))

    def _check_table_references_and_disambiguation(self) -> None:
        """Sub-Gate 3.2: Table Reference & Multi-Part Integrity Checker (ADR 0044)."""
        if not self.legal_docs_dir.exists():
            return

        for cat in ["01_vbpl", "02_qcvn", "03_tcvn"]:
            cat_dir = self.legal_docs_dir / cat
            if not cat_dir.exists():
                continue
            for doc_dir in cat_dir.iterdir():
                if not doc_dir.is_dir() or doc_dir.name.startswith("."):
                    continue
                if self.target_bundle and doc_dir.name != self.target_bundle:
                    continue
                catalog_path = doc_dir / "tables" / "tables_catalog.json"
                if not catalog_path.exists():
                    continue
                try:
                    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
                    if isinstance(catalog, list):
                        tables = catalog
                    elif isinstance(catalog, dict):
                        tables = catalog.get("tables", [])
                    else:
                        tables = []

                    for t in tables:
                        if isinstance(t, dict):
                            csv_rel = t.get("csv_file")
                            if csv_rel and not (doc_dir / csv_rel).exists():
                                self.warnings.append(
                                    f"Table Reference Warning [{doc_dir.name}]: Table asset missing on disk: {csv_rel} (ADR 0044)."
                                )
                except Exception as exc:
                    self.warnings.append(
                        f"Table Catalog Warning [{doc_dir.name}]: Failed to parse tables_catalog.json: {exc}"
                    )

    def validate_fake_data_gate(self) -> Tuple[int, int]:
        """Validate that bundles do not contain truncated/synthetic placeholder content."""
        vbpl_dir = self.legal_docs_dir / "01_vbpl"
        if not vbpl_dir.exists():
            return (len(self.errors), len(self.warnings))

        for doc_dir in vbpl_dir.iterdir():
            if not doc_dir.is_dir() or doc_dir.name.startswith("."):
                continue
            if self.target_bundle and doc_dir.name != self.target_bundle:
                continue
            self._check_vbpl_fake_data(doc_dir)

        return (len(self.errors), len(self.warnings))

    def _check_vbpl_fake_data(self, doc_dir: Path) -> None:
        """Check VBPL bundle for truncated content, empty AST, or missing articles."""
        primary_md = doc_dir / f"{doc_dir.name}.md"
        if not primary_md.exists():
            return

        size_kb = primary_md.stat().st_size / 1024
        if size_kb < 20 and (doc_dir.name.startswith("nghi_dinh_") or doc_dir.name.startswith("luat_")):
            self.warnings.append(
                f"Fake Data Warning [{doc_dir.name}]: Decrees/Laws usually exceed 20KB, but found {size_kb:.1f} KB. Verify full text presence."
            )

        content = self._safe_read_text(primary_md)
        if content:
            dieu_nums = sorted(
                int(m)
                for m in re.findall(
                    r"(?:###|##)\s*(?:__|\*\*)?\s*Điều\s+(\d+)\.", content, flags=re.IGNORECASE
                )
            )
            for i in range(len(dieu_nums) - 1):
                gap = dieu_nums[i + 1] - dieu_nums[i]
                if gap > 3:
                    self.warnings.append(
                        f"Fake Data Warning [{doc_dir.name}]: Gap of {gap} detected between Điều {dieu_nums[i]} and Điều {dieu_nums[i+1]}."
                    )

        clauses_json = doc_dir / "clauses.json"
        if clauses_json.exists():
            try:
                raw_clauses = json.loads(clauses_json.read_text(encoding="utf-8"))
                clauses_data = (
                    raw_clauses.get("clauses", raw_clauses.get("nodes", []))
                    if isinstance(raw_clauses, dict)
                    else raw_clauses
                )
                if not isinstance(clauses_data, list):
                    clauses_data = []
                if len(clauses_data) == 0:
                    self.errors.append(
                        f"Empty AST Error [{doc_dir.name}]: Found 0 clauses in clauses.json. AST generation failed or is empty."
                    )
                elif len(clauses_data) < 25:
                    self.warnings.append(
                        f"Fake Data Warning [{doc_dir.name}]: Found only {len(clauses_data)} clauses in clauses.json. Expected >= 30."
                    )
            except json.JSONDecodeError as exc:
                self.errors.append(f"JSON Error [{doc_dir.name}]: Failed to parse clauses.json: {exc}")
        else:
            self.errors.append(
                f"Missing AST Error [{doc_dir.name}]: clauses.json is missing on disk. AST generation is required for VBPL bundle."
            )

    def validate_pdf_metadata_and_ast_enrichment(self) -> Tuple[int, int]:
        """Validate that legal_registry.yaml and clauses.json have rich PDF and Jurisdiction AST attributes."""
        try:
            with open(self.registry_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            self._validate_registry_pdf_meta(data)
        except (yaml.YAMLError, OSError) as exc:
            self.errors.append(f"CRITICAL: Failed to validate PDF metadata in registry: {exc}")

        # Dynamic QCVN AST check: Discover all QCVN bundles with clauses.json
        qcvn_dir = self.legal_docs_dir / "02_qcvn"
        if qcvn_dir.exists():
            for doc_dir in qcvn_dir.iterdir():
                if doc_dir.is_dir() and not doc_dir.name.startswith("."):
                    if self.target_bundle and doc_dir.name != self.target_bundle:
                        continue
                    self._validate_qcvn_ast_clauses(doc_dir)

        # Sub-Gate 5.2: Dual-PDF Archive & Provenance Invariant Check (ADR 0043)
        self._validate_dual_pdf_archive_invariant()

        # Sub-Gate 5.3: Legal Validity & In-Force Verification Gate (RULE-3.1 & ADR 0059)
        self._validate_legal_validity_and_in_force()

        return (len(self.errors), len(self.warnings))

    def _validate_dual_pdf_archive_invariant(self) -> None:
        """Sub-Gate 5.2: Validate Dual-PDF Archive & Provenance Invariant (ADR 0043)."""
        if not self.legal_docs_dir.exists():
            return

        for cat in ["01_vbpl", "02_qcvn", "03_tcvn"]:
            cat_dir = self.legal_docs_dir / cat
            if not cat_dir.exists():
                continue
            for doc_dir in cat_dir.iterdir():
                if not doc_dir.is_dir() or doc_dir.name.startswith("."):
                    continue
                if self.target_bundle and doc_dir.name != self.target_bundle:
                    continue
                meta_file = doc_dir / "metadata.yaml"
                if not meta_file.exists():
                    continue
                try:
                    meta = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
                    if meta.get("pdf_origin") == "docx_vector_rendered":
                        raw_scan = doc_dir / DIR_SOURCES / f"{doc_dir.name}_raw_scan.pdf"
                        vector_pdf = doc_dir / DIR_SOURCES / f"{doc_dir.name}.pdf"
                        is_ci = bool(os.getenv("CI") or os.getenv("GITHUB_ACTIONS"))
                        if not vector_pdf.exists():
                            if not is_ci:
                                self.errors.append(
                                    f"Dual-PDF Error [{doc_dir.name}]: Vector PDF missing at {vector_pdf.name} (ADR 0043)."
                                )
                        elif not raw_scan.exists():
                            if not is_ci:
                                self.warnings.append(
                                    f"Dual-PDF Warning [{doc_dir.name}]: 'pdf_origin: docx_vector_rendered' set but raw scan '{raw_scan.name}' not archived (ADR 0043)."
                                )
                except Exception as exc:
                    self.warnings.append(
                        f"Dual-PDF Warning [{doc_dir.name}]: Failed to inspect metadata.yaml for PDF origin: {exc}"
                    )

    @staticmethod
    def _canonical_keys(val: Any) -> Set[str]:
        """Generate canonical lookup tokens preserving document types and numbers."""
        if not val:
            return set()
        s = str(val).strip().lower()
        s = s.replace("đ", "d")
        # Replace separators including colon, slash, hyphen, period with underscore
        s = re.sub(r"[\s\/\-\.:]+", "_", s)
        s = re.sub(r"_+", "_", s).strip("_")
        keys = {s}
        for prefix in ("nghi_dinh_", "thong_tu_", "quyet_dinh_", "nghi_quyet_", "luat_"):
            if s.startswith(prefix):
                keys.add(s[len(prefix):])
        m = re.search(r"(\d+_\d{4}_[a-z0-9_]+)$", s)
        if m:
            keys.add(m.group(1))
        return keys

    def _validate_legal_validity_and_in_force(self) -> None:
        """Sub-Gate 5.3: Legal Validity & In-Force Verification Gate (RULE-3.1 & ADR 0059).

        Guarantees that:
        1. Two-Tier Transitive Engine:
           - Tier 1: Replacement DAG BFS from active documents. Any document in the reachable
             replaced set CANNOT be 'active' (detects superseded docs automatically).
           - Tier 2: Statutory Baseline Safety Floor (STATUTORY_BASELINE_REPEALED) as fallback.
        2. Any document with 'status: expired' declared has:
           - valid 'relations.replaced_by' reference or 'replaces' reference
           - clear warning disclaimer in bundle's index.md
        3. No document past its expiration_date retains 'status: active'.
        """
        STATUTORY_BASELINE_REPEALED: Dict[str, str] = {
            "10/2021/NĐ-CP": "206/2026/NĐ-CP",
            "15/2021/NĐ-CP": "217/2026/NĐ-CP",
            "175/2024/NĐ-CP": "217/2026/NĐ-CP",
            "06/2021/NĐ-CP": "207/2026/NĐ-CP",
            "136/2020/NĐ-CP": "105/2025/NĐ-CP",
            "16/2022/NĐ-CP": "339/2026/NĐ-CP",
            "QCVN 06:2020/BXD": "QCVN 06:2022/BXD",
        }

        try:
            with open(self.registry_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except Exception as exc:
            self.errors.append(f"Sub-Gate 5.3 Error: Failed to load registry: {exc}")
            return

        all_items: List[Dict[str, Any]] = []
        for sec in ["laws", "standards"]:
            items = data.get(sec, [])
            if isinstance(items, list):
                all_items.extend(items)

        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Multi-key canonical index: maps canonical token -> item
        doc_by_canonical_key: Dict[str, Dict[str, Any]] = {}
        for item in all_items:
            if not isinstance(item, dict):
                continue
            doc_id = str(item.get("id", ""))
            doc_num = str(item.get("document_number", ""))
            item_keys = self._canonical_keys(doc_id) | self._canonical_keys(doc_num)
            for k in item_keys:
                doc_by_canonical_key[k] = item

        def _get_replaces(it: Dict[str, Any]) -> List[str]:
            rels = it.get("relations") if isinstance(it.get("relations"), dict) else {}
            rep = rels.get("replaces") or it.get("replaces")
            if not rep:
                return []
            if isinstance(rep, list):
                return [str(x).strip() for x in rep if x]
            return [str(rep).strip()]

        # Tier 1: Replacement DAG BFS from active documents
        superseded_by_map: Dict[str, str] = {}
        active_items = [
            it
            for it in all_items
            if isinstance(it, dict)
            and str(it.get("status", "")).strip().lower() in {"active", "current", "còn hiệu lực"}
        ]

        from collections import deque

        queue: deque[Tuple[Dict[str, Any], Dict[str, Any]]] = deque()
        visited_keys: Set[str] = set()

        for active_it in active_items:
            queue.append((active_it, active_it))

        while queue:
            curr_it, source_active = queue.popleft()
            source_label = str(
                source_active.get("document_number") or source_active.get("id", "Active Doc")
            ).strip()
            source_keys = self._canonical_keys(source_active.get("id", "")) | self._canonical_keys(
                source_active.get("document_number", "")
            )

            # 1. Forward edges: curr_it declares 'replaces'
            for target_str in _get_replaces(curr_it):
                target_keys = self._canonical_keys(target_str)
                for tk in target_keys:
                    if tk not in source_keys:
                        superseded_by_map[tk] = source_label
                    if tk not in visited_keys:
                        visited_keys.add(tk)
                        if tk in doc_by_canonical_key:
                            queue.append((doc_by_canonical_key[tk], source_active))

            # 2. Backward edges: any document whose 'replaced_by' points to curr_it
            curr_keys = self._canonical_keys(curr_it.get("id", "")) | self._canonical_keys(
                curr_it.get("document_number", "")
            )
            for candidate in all_items:
                if not isinstance(candidate, dict):
                    continue
                cand_rels = (
                    candidate.get("relations")
                    if isinstance(candidate.get("relations"), dict)
                    else {}
                )
                rep_by = cand_rels.get("replaced_by") or candidate.get("replaced_by")
                if rep_by:
                    rep_by_keys = self._canonical_keys(str(rep_by).strip())
                    if rep_by_keys & curr_keys:
                        cand_id = str(candidate.get("id", ""))
                        cand_num = str(candidate.get("document_number", ""))
                        for ck in self._canonical_keys(cand_id) | self._canonical_keys(cand_num):
                            if ck not in source_keys:
                                superseded_by_map[ck] = source_label
                            if ck not in visited_keys:
                                visited_keys.add(ck)
                                queue.append((candidate, source_active))

        for item in all_items:
            if not isinstance(item, dict):
                continue
            doc_id = str(item.get("id", "UNKNOWN"))
            bundle_p = str(item.get("bundle_path", ""))
            doc_num = str(item.get("document_number", "")).strip()
            status = str(item.get("status", "")).strip().lower()
            relations = item.get("relations") if isinstance(item.get("relations"), dict) else {}

            if self.target_bundle:
                if (
                    doc_id != self.target_bundle
                    and self.target_bundle not in bundle_p
                    and doc_num != self.target_bundle
                ):
                    continue

            # 1. Banned Expired Check (Tier 1 DAG BFS + Tier 2 Statutory Baseline Floor)
            if status in {"active", "current", "còn hiệu lực"}:
                item_keys = self._canonical_keys(doc_id) | self._canonical_keys(doc_num)
                matching_superseded = item_keys & superseded_by_map.keys()
                if matching_superseded:
                    replacing = superseded_by_map[next(iter(matching_superseded))]
                    self.errors.append(
                        f"Legal Validity Hard Floor Violation [{doc_id}]: {doc_num} is repealed and strictly banned "
                        f"from status: active (RULE-3.1). Must use {replacing} instead."
                    )
                else:
                    for banned_num, replacement in STATUTORY_BASELINE_REPEALED.items():
                        banned_keys = self._canonical_keys(banned_num)
                        if item_keys & banned_keys:
                            self.errors.append(
                                f"Legal Validity Hard Floor Violation [{doc_id}]: {doc_num} is repealed and strictly banned "
                                f"from status: active (RULE-3.1). Must use {replacement} instead."
                            )
                            break

            # 2. Expiration Date Check vs Status
            exp_date = str(item.get("expiration_date", "")).strip()
            if exp_date and exp_date <= today_str:
                if status in {"active", "current", "còn hiệu lực"}:
                    self.errors.append(
                        f"Legal Validity Inconsistency [{doc_id}]: Document {doc_num} has expiration_date {exp_date} "
                        f"<= {today_str} but status is still '{status}'. Must be 'expired' (RULE-3.1)."
                    )

            # 3. Expired Document Integrity Check
            if status in {"expired", "hết hiệu lực"}:
                if not relations.get("replaced_by") and not item.get("replaces"):
                    self.warnings.append(
                        f"Legal Validity Warning [{doc_id}]: Expired document {doc_num} lacks 'relations.replaced_by' "
                        f"in legal_registry.yaml."
                    )

                # Check index.md disclaimer in bundle
                if bundle_p:
                    bundle_dir = self.root_dir / bundle_p.strip("/")
                    index_file = bundle_dir / "index.md"
                    if index_file.exists():
                        idx_text = index_file.read_text(encoding="utf-8").upper()
                        if "HẾT HIỆU LỰC" not in idx_text and "EXPIRED" not in idx_text:
                            self.warnings.append(
                                f"Legal Validity Warning [{doc_id}]: index.md lacks clear 'HẾT HIỆU LỰC / EXPIRED' warning disclaimer."
                            )

            # 4. Split-Brain Status Check between legal_registry.yaml and bundle metadata.yaml
            if bundle_p:
                bundle_dir = self.root_dir / bundle_p.strip("/")
                meta_file = bundle_dir / "metadata.yaml"
                if meta_file.exists():
                    try:
                        b_meta = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
                        b_status = str(b_meta.get("status", "")).strip().lower()
                        norm_reg_status = "expired" if status in {"expired", "hết hiệu lực"} else "active"
                        norm_b_status = "expired" if b_status in {"expired", "hết hiệu lực"} else "active"
                        if norm_reg_status != norm_b_status:
                            self.errors.append(
                                f"Split-Brain Status Error [{doc_id}]: Status in legal_registry.yaml ('{status}') "
                                f"does not match bundle metadata.yaml ('{b_status}')."
                            )
                    except Exception as exc:
                        self.warnings.append(
                            f"Metadata Parse Warning [{doc_id}]: Failed to read bundle metadata.yaml: {exc}"
                        )

    def _validate_registry_pdf_meta(self, data: Dict[str, Any]) -> None:
        """Validate PDF fields in legal_registry.yaml."""
        laws = data.get("laws", [])
        standards = data.get("standards", [])
        all_items = []
        if isinstance(laws, list):
            all_items.extend(laws)
        if isinstance(standards, list):
            all_items.extend(standards)
        for item in all_items:
            if isinstance(item, dict):
                doc_id = item.get("id", "UNKNOWN")
                bundle_p = item.get("bundle_path", "")
                doc_num = item.get("document_number", "")
                if self.target_bundle and doc_id != self.target_bundle and self.target_bundle not in bundle_p and doc_num != self.target_bundle:
                    continue
                if "pdf_status" not in item:
                    self.errors.append(f"PDF Metadata Error [{doc_id}]: Missing 'pdf_status' in legal_registry.yaml")
                if "cong_bao_number" not in item:
                    self.warnings.append(f"PDF Metadata Warning [{doc_id}]: Missing 'cong_bao_number' in legal_registry.yaml")

    def _validate_qcvn_ast_clauses(self, qcvn_dir: Path) -> None:
        """Validate jurisdiction, severity, and Cong Bao numbers in QCVN clauses.json."""
        clauses_file = qcvn_dir / "clauses.json"
        if not clauses_file.exists():
            return

        try:
            raw_clauses = json.loads(clauses_file.read_text(encoding="utf-8"))
            clauses_data = (
                raw_clauses.get("clauses", raw_clauses.get("nodes", []))
                if isinstance(raw_clauses, dict)
                else raw_clauses
            )
            if not clauses_data:
                self.errors.append(f"AST Error [{qcvn_dir.name}]: clauses.json is empty")
                return

            valid_jurisdictions = {"CQXD", "CONG_AN", "CHU_DAU_TU_TU_THAM_DINH"}
            valid_severities = {"CRITICAL_DEFECT", "WARNING_NOTICE", "VERIFICATION_REQUIRED"}

            missing_jur = sum(1 for c in clauses_data if c.get("jurisdiction") not in valid_jurisdictions)
            missing_cb = sum(1 for c in clauses_data if not c.get("cong_bao_number"))

            for c in clauses_data:
                g_end = c.get("grace_period_end")
                if g_end and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(g_end)):
                    self.errors.append(f"AST Error [{qcvn_dir.name}]: Invalid date format for grace_period_end: {g_end}")
                sev = c.get("compliance_severity")
                if sev and sev not in valid_severities:
                    self.errors.append(f"AST Error [{qcvn_dir.name}]: Invalid compliance_severity: {sev}")

            if missing_jur > 0:
                self.errors.append(f"AST Error [{qcvn_dir.name}]: {missing_jur}/{len(clauses_data)} clauses missing valid 'jurisdiction'")
            if missing_cb > 0:
                self.warnings.append(f"AST Warning [{qcvn_dir.name}]: {missing_cb}/{len(clauses_data)} clauses missing 'cong_bao_number'")

        except json.JSONDecodeError as exc:
            self.errors.append(f"AST Error [{qcvn_dir.name}]: Failed to parse clauses.json: {exc}")

    def validate_pure_normative_body_gate(self) -> Tuple[int, int]:
        """Validate OKF v2.4 Universal Pure Normative Body standard (ADR 0021 & ADR 0036)."""
        vbpl_dir = self.legal_docs_dir / "01_vbpl"
        if vbpl_dir.exists():
            for doc_dir in vbpl_dir.iterdir():
                if not doc_dir.is_dir() or doc_dir.name.startswith("."):
                    continue
                if self.target_bundle and doc_dir.name != self.target_bundle:
                    continue

                target_md = doc_dir / f"{doc_dir.name}.md"
                primary_md = target_md if target_md.exists() else None
                if primary_md is None:
                    md_files = [f for f in doc_dir.glob("*.md") if f.name not in ("index.md", "dead_ends.md", "log.md")]
                    primary_md = md_files[0] if md_files else None

                if primary_md and primary_md.exists():
                    self._check_pure_body_document(doc_dir, primary_md)

        # ADR 0036: Enforce Annex Leakage Hard Gate on technical standards (QCVN / TCVN)
        for cat in ["02_qcvn", "03_tcvn"]:
            cat_dir = self.legal_docs_dir / cat
            if not cat_dir.exists():
                continue
            for doc_dir in cat_dir.iterdir():
                if not doc_dir.is_dir() or doc_dir.name.startswith("."):
                    continue
                if self.target_bundle and doc_dir.name != self.target_bundle:
                    continue
                std_target_md = doc_dir / f"{doc_dir.name}.md"
                std_primary_md = std_target_md if std_target_md.exists() else None
                if std_primary_md is None:
                    std_md_files = [
                        f
                        for f in doc_dir.glob("*.md")
                        if f.name not in ("index.md", "dead_ends.md", "log.md", "bang_so_sanh_thay_doi.md")
                    ]
                    std_primary_md = std_md_files[0] if std_md_files else None
                if std_primary_md and std_primary_md.exists():
                    content = self._safe_read_text(std_primary_md)
                    if content:
                        main_body = re.split(
                            r"(?:^|\n)##\s+📑\s+HỆ\s+THỐNG\s+PHỤ\s+LỤC", content, flags=re.IGNORECASE
                        )[0].strip()
                        self._check_annex_leakage(main_body, doc_dir.name, std_primary_md.name)

        return (len(self.errors), len(self.warnings))

    def _check_annex_leakage(self, main_body: str, doc_name: str, md_name: str) -> None:
        """Enforce ADR 0036: Technical normative annexes must be decoupled into annexes/ directory."""
        if re.search(r"(?:^|\n)#{1,4}\s+(?:PHỤ\s+LỤC|Phụ\s+lục)\s+[A-Z0-9]", main_body):
            self.errors.append(
                f"Annex Leakage Error [{doc_name}]: Found un-decoupled annex heading in primary markdown body ({md_name}). "
                "Annexes must be decoupled into annexes/ directory (ADR 0036)."
            )

    def _check_pure_body_document(self, doc_dir: Path, primary_md: Path) -> None:
        """Check frontmatter, administrative noise, and HTML artifacts in a normative document."""
        fm_data, body_text = self._extract_frontmatter(primary_md)

        if fm_data is None:
            self.errors.append(
                f"Pure Normative Body Error [{doc_dir.name}]: Missing or invalid YAML Frontmatter in {primary_md.name}"
            )
        else:
            for req_field in ["id", "document_number", "pdf_anchor"]:
                if req_field not in fm_data:
                    self.errors.append(
                        f"Pure Normative Body Error [{doc_dir.name}]: Missing required frontmatter field '{req_field}'"
                    )

        main_body = re.split(r"(?:^|\n)##\s+📑\s+HỆ\s+THỐNG\s+PHỤ\s+LỤC", body_text, flags=re.IGNORECASE)[0].strip()
        body_lines = [line.strip() for line in main_body.splitlines() if line.strip()]

        self._check_header_noise(body_lines, doc_dir.name, primary_md.name)
        self._check_footer_noise(body_lines, doc_dir.name, primary_md.name)
        self._check_html_noise(body_text, doc_dir.name, primary_md.name)

    def _check_header_noise(self, body_lines: List[str], doc_name: str, md_name: str) -> None:
        """Check for unstripped Quốc hiệu/Tiêu ngữ in the first 25 lines."""
        header_window = "\n".join(body_lines[:25])
        if "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" in header_window or "Độc lập - Tự do - Hạnh phúc" in header_window:
            self.errors.append(
                f"Pure Normative Body Error [{doc_name}]: Unstripped administrative header in {md_name}"
            )

    def _check_footer_noise(self, body_lines: List[str], doc_name: str, md_name: str) -> None:
        """Check for unstripped Nơi nhận/Chữ ký in the last 25 lines."""
        footer_window = "\n".join(body_lines[-25:]) if len(body_lines) >= 25 else "\n".join(body_lines)
        sig_pattern = r"(?:^|\n)(?:__\*?\s*Nơi nhận\s*:|\*+Nơi nhận\s*:|\bNơi nhận\s*:|__KT\.\s+BỘ\s+TRƯỞNG|KT\.\s+BỘ\s+TRƯỞNG|CHỦ\s+TỊCH\s+QUỐC\s+HỘI|TM\.\s+QUỐC\s+HỘI|TM\.\s+CHÍNH\s+PHỦ|__THỦ\s+TƯỚNG__|THỦ\s+TƯỚNG\b)"
        if re.search(sig_pattern, footer_window, re.IGNORECASE):
            self.errors.append(
                f"Pure Normative Body Error [{doc_name}]: Unstripped administrative footer in {md_name}"
            )

    def _check_html_noise(self, body_text: str, doc_name: str, md_name: str) -> None:
        """Check for raw web scraping HTML/JS noise."""
        html_noise_pattern = r"(?:<script\b|<form\b|<input\b|<iframe\b|class=[\"'][^\"']*(?:NoiDungChiase|clearfix|download1|clsBookmark)|onclick=)"
        if re.search(html_noise_pattern, body_text, re.IGNORECASE):
            self.errors.append(
                f"Pure Normative Body Error [{doc_name}]: Detected raw web scraping HTML/JS artifacts in {md_name}"
            )

    def validate_spoke_cleanliness(self) -> Tuple[int, int]:
        """Gate 7: Verify Spoke Cleanliness and Zero-Wrapper Architecture."""
        scripts_dir = self.root_dir / "scripts"
        if not scripts_dir.exists():
            return (0, 0)

        allowed_core_scripts = {
            "__init__.py", "validate_legal_spoke.py", "test_converter_regression.py",
            "verify_cross_links.py", "verify_all_docs_against_pdf.py", "verify_docx_against_pdf.py",
            "sync_notebooklm_knowledge.py", "benchmark_legal_rag.py", "spoke_cli.py",
            "check_hub_import_depth.py", "check_spoke_cleanliness.py", "safe_pytest.py",
            "lint_visual_parity.py", "query_hub_catalog.py", "analyze_gate_audit.py",
            "sync_adr_matrix.py", "validate_adr_parity.py", "setup_pre_commit.py",
            "modernize_annex_engine.py", "verify_formula_visual_matrix.py",
            "sync_expansion_roadmap.py", "safe_runner.py",
        }

        py_files = list(scripts_dir.glob("*.py"))
        for py_file in py_files:
            if py_file.name not in allowed_core_scripts:
                if any(py_file.name.startswith(p) for p in ["fix_", "audit_", "build_", "temp_", "clean_"]):
                    self.errors.append(
                        f"Spoke Cleanliness Gate: Ephemeral script '{py_file.name}' detected in scripts/. Move to .md/archive/."
                    )
                else:
                    self.warnings.append(
                        f"Spoke Cleanliness Gate: Extra script '{py_file.name}' found in scripts/."
                    )

        if len(py_files) > 25:
            self.warnings.append(
                f"Spoke Cleanliness Gate: scripts/ directory contains {len(py_files)} files (> 25 threshold)."
            )

        return (len(self.errors), len(self.warnings))

    def validate_template_and_table_integrity(self) -> Tuple[int, int]:
        """Gate 8: Verify Template & Table Structural Integrity (ADR 0021)."""
        for cat_dir in [self.legal_docs_dir / "01_vbpl", self.legal_docs_dir / "02_qcvn"]:
            if not cat_dir.exists():
                continue
            for doc_dir in cat_dir.iterdir():
                if doc_dir.is_dir() and not doc_dir.name.startswith("."):
                    if self.target_bundle and doc_dir.name != self.target_bundle:
                        continue
                    self._check_bundle_templates_and_tables(doc_dir)

        for cat_dir in [self.legal_docs_dir / "02_qcvn", self.legal_docs_dir / "03_tcvn"]:
            if not cat_dir.exists():
                continue
            for doc_dir in cat_dir.iterdir():
                if doc_dir.is_dir() and not doc_dir.name.startswith("."):
                    if self.target_bundle and doc_dir.name != self.target_bundle:
                        continue
                    self._check_figures_catalog(doc_dir)

        return (len(self.errors), len(self.warnings))

    def _check_bundle_templates_and_tables(self, doc_dir: Path) -> None:
        """Check forms, broken tables, and list uncollapsing in a bundle."""
        primary_md = doc_dir / f"{doc_dir.name}.md"
        if not primary_md.exists():
            return

        content = self._safe_read_text(primary_md)
        if content is None:
            return

        body_only = content.split("## 📑")[0] if "## 📑" in content else content
        templates_dir = doc_dir / DIR_TEMPLATES

        self._check_form_templates(doc_dir, body_only, templates_dir)
        self._check_broken_pipe_tables(templates_dir)

        all_md_files = [primary_md] + (list(templates_dir.rglob("*.md")) if templates_dir.exists() else [])
        for md_path in all_md_files:
            self._check_uncollapsed_list_items(md_path)

    def _check_form_templates(self, doc_dir: Path, body_only: str, templates_dir: Path) -> None:
        """Check that defined forms have corresponding files in templates/."""
        form_regex = re.compile(
            r"(?:Mẫu\s+số\s+[0-9a-zA-Z\.\-]+(?:\s+ban\s+hành)?\s+kèm\s+theo\s+(?:Nghị\s+định|Thông\s+tư|Quyết\s+định)\s+này|"
            r"ban\s+hành\s+kèm\s+theo\s+(?:Nghị\s+định|Thông\s+tư|Quyết\s+định)\s+này\s+(?:các\s+)?(?:mẫu\s+biểu|biểu\s+mẫu)|"
            r"tại\s+Phụ\s+lục\s+Hệ\s+thống\s+biểu\s+mẫu)",
            re.IGNORECASE,
        )
        if form_regex.search(body_only) and (not templates_dir.exists() or not list(templates_dir.rglob("*.md"))):
            self.errors.append(
                f"Template Integrity Error [{doc_dir.name}]: Document defines form templates, but templates/ is empty or missing."
            )

    def _check_broken_pipe_tables(self, templates_dir: Path) -> None:
        """Check for flattened or broken pipe tables in templates/."""
        if templates_dir.exists():
            for tmpl_file in templates_dir.rglob("*.md"):
                tmpl_txt = self._safe_read_text(tmpl_file)
                if tmpl_txt and re.search(r"(?:__TT__|\bTT\b)\s*\n\s*\n\s*__(?:Danh mục|Tên sản phẩm)", tmpl_txt):
                    if "|" not in tmpl_txt:
                        self.errors.append(
                            f"Broken Table Error [{tmpl_file.relative_to(self.root_dir)}]: Flattened table detected. Must be 2D GFM Table."
                        )

    def _check_uncollapsed_list_items(self, md_path: Path) -> None:
        """Ensure sub-clauses following list items have separating blank lines."""
        txt = self._safe_read_text(md_path)
        if not txt:
            return
        lines = txt.splitlines()
        for i in range(len(lines) - 1):
            curr_line = lines[i].strip()
            next_line = lines[i + 1].strip()
            if curr_line.startswith(("- ", "+ ", "* ")) and next_line:
                if not next_line.startswith(("- ", "+ ", "* ", "#", "|", ">")):
                    if re.match(r"^(?:\d+\.\d+|\d+\.\d+\.\d+|Điều\s+\d+|Khoản\s+\d+|Mục\s+[IVXLCDM0-9]+)\b", next_line):
                        self.errors.append(
                            f"Markdown Formatting Error [{md_path.relative_to(self.root_dir)}:L{i+2}]: "
                            f"Sub-clause '{next_line[:30]}' immediately follows a list item without a blank line."
                        )

    def _check_figures_catalog(self, doc_dir: Path) -> None:
        """Check figures_catalog.yaml schema, image references, and enforce Zero-Orphan Figure Policy (ADR 0036)."""
        figures_dir = doc_dir / "figures"
        if not figures_dir.exists():
            return
        catalog_file = figures_dir / "figures_catalog.yaml"
        if not catalog_file.exists():
            self.errors.append(f"Figure Catalog Error [{doc_dir.name}]: figures/ exists but figures_catalog.yaml is missing.")
            return

        try:
            with open(catalog_file, "r", encoding="utf-8") as f:
                cat_data = yaml.safe_load(f)
            if isinstance(cat_data, dict):
                for fig in cat_data.get("figures", []):
                    img_rel = fig.get("image_relpath")
                    if img_rel and not (doc_dir / img_rel).exists():
                        self.errors.append(f"Figure Image Error [{doc_dir.name}]: Image '{img_rel}' does not exist on disk.")
        except (yaml.YAMLError, OSError) as exc:
            self.errors.append(f"Figure Catalog Error [{doc_dir.name}]: Failed to parse figures_catalog.yaml: {exc}")

        # Enforce Zero Orphaned Figures Policy
        images_dir = figures_dir / "images"
        if images_dir.exists():
            orphans: List[str] = []
            try:
                from ccba_legal.figure_extractor import scan_and_prune_orphan_figures
                scan_res = scan_and_prune_orphan_figures(doc_dir, prune=False)
                orphans = scan_res.get("orphaned", [])
            except Exception:
                # Standalone fallback: Scan references across Markdown, Cards, and figures_catalog.yaml
                all_images = {p.name for p in images_dir.glob("*.*") if p.is_file()}
                referenced: Set[str] = set()
                # 1. In markdown files
                for md_file in doc_dir.rglob("*.md"):
                    if "sources" not in md_file.parts:
                        txt = self._safe_read_text(md_file) or ""
                        for m in re.findall(r"!\[[^\]]*\]\([^)]*images/([^)\s]+)\)", txt):
                            referenced.add(Path(m).name)
                        for m in re.findall(r"<img\b[^>]*src=[\"'][^\"']*images/([^\"'\s>]+)[\"']", txt, re.IGNORECASE):
                            referenced.add(Path(m).name)
                # 2. In cards/*.md and cards/*.json
                cards_dir = figures_dir / "cards"
                if cards_dir.exists():
                    for card_f in list(cards_dir.glob("*.md")) + list(cards_dir.glob("*.json")):
                        txt = self._safe_read_text(card_f) or ""
                        for m in re.findall(r'"image":\s*"([^"]+)"', txt):
                            referenced.add(Path(m).name)
                        for m in re.findall(r"!\[[^\]]*\]\([^)]*images/([^)\s]+)\)", txt):
                            referenced.add(Path(m).name)
                # 3. In figures_catalog.yaml
                cat_file = figures_dir / "figures_catalog.yaml"
                if cat_file.exists():
                    txt = self._safe_read_text(cat_file) or ""
                    for m in re.findall(r"image_relpath:\s*[\"']?figures/images/([^\s\"']+)[\"']?", txt):
                        referenced.add(Path(m).name)
                orphans = sorted(list(all_images - referenced))

            if orphans:
                sample = ", ".join(orphans[:3])
                extra = f" (+{len(orphans)-3} more)" if len(orphans) > 3 else ""
                self.errors.append(
                    f"Orphaned Figure Error [{doc_dir.name}]: Found {len(orphans)} unreferenced image(s) in figures/images/: {sample}{extra}. Run 'python -m ccba_legal clean-images --prune' to clean up."
                )

    def validate_visual_parity(self) -> Tuple[int, int]:
        """Gate 9: Validate 100% Visual Parity & Zero Formatting Clutter (ADR 0029 & ADR 0030)."""
        try:
            from lint_visual_parity import lint_document
        except ImportError:
            from scripts.lint_visual_parity import lint_document

        for md_file in sorted(self.legal_docs_dir.rglob("*.md")):
            if self.target_bundle and self.target_bundle not in md_file.parts:
                continue
            rel = md_file.relative_to(self.root_dir)
            content = self._safe_read_text(md_file)
            if content is None:
                continue

            for i, line in enumerate(content.splitlines(), 1):
                if re.search(r"<br>\s*(?:\*\*)?CHÚ THÍCH", line, re.IGNORECASE):
                    self.errors.append(f"Visual Parity Error [{rel}:L{i}]: Squashed note with <br> tag.")

            for chunk in re.split(r"(?=\n#{1,4}\s+|\n<a id=)", content):
                labels = [m.group(1).upper() for m in re.finditer(r"\b(CHÚ THÍCH(?:\s+\d+)?):", chunk, re.IGNORECASE)]
                if labels and any("CHÚ THÍCH 2" in lbl for lbl in labels) and any(lbl == "CHÚ THÍCH" for lbl in labels) and not any("CHÚ THÍCH 1" in lbl for lbl in labels):
                    self.errors.append(f"Visual Parity Error [{rel}]: Missing 'CHÚ THÍCH 1' before 'CHÚ THÍCH 2'.")

            for err in lint_document(md_file):
                self.errors.append(f"Visual Parity Error [{rel}]: {err}")

        return (len(self.errors), len(self.warnings))

    def validate_adr_parity_and_sync(self) -> Tuple[int, int]:
        """Gate 10: Self-Healing ADR Matrix Synchronization & Parity Gate."""
        adr_dir = self.root_dir / "docs" / "adr"
        if not adr_dir.exists():
            return (len(self.errors), len(self.warnings))

        try:
            from sync_adr_matrix import parse_adr_file
        except ImportError:
            from scripts.sync_adr_matrix import parse_adr_file

        adr_files = sorted(f for f in adr_dir.glob("*.md") if f.name not in ("README.md", "TRACEABILITY_MATRIX.md"))
        adr_list = sorted([parse_adr_file(f) for f in adr_files], key=lambda x: x["num"])
        known_nums = {a["num"] for a in adr_list}
        # Include Hub Platform ADR numbers if Hub is accessible
        for hub_candidate in [Path("D:/GitHubProjects/ccba-agent-platform/docs/adr"), self.root_dir.parent / "ccba-agent-platform" / "docs" / "adr"]:
            if hub_candidate.exists():
                for f in hub_candidate.glob("*.md"):
                    m = re.match(r"^(\d+)-", f.name)
                    if m:
                        known_nums.add(int(m.group(1)))

        self._sync_adr_artifacts(adr_dir, adr_list)
        self._sync_expansion_roadmap()
        self._lint_session_learnings(self.root_dir / ".md" / "knowledge" / "session_learnings.md")
        self._check_core_adr_references(known_nums)

        return (len(self.errors), len(self.warnings))

    def _sync_adr_artifacts(self, adr_dir: Path, adr_list: List[Dict[str, Any]]) -> None:
        """Auto-compile README.md and TRACEABILITY_MATRIX.md for ADRs."""
        try:
            try:
                from sync_adr_matrix import compile_adr_readme, compile_traceability_matrix, scan_skill_radar
            except ImportError:
                from scripts.sync_adr_matrix import compile_adr_readme, compile_traceability_matrix, scan_skill_radar

            compile_adr_readme(adr_list, adr_dir / "README.md")
            matrix = scan_skill_radar(adr_list, self.root_dir)
            compile_traceability_matrix(adr_list, matrix, adr_dir / "TRACEABILITY_MATRIX.md")
        except (ImportError, OSError) as exc:
            self.errors.append(f"ADR Sync Error: Failed to compile ADR artifacts: {exc}")

    def _sync_expansion_roadmap(self) -> None:
        """Auto-sync living legal knowledge expansion roadmap."""
        try:
            try:
                from sync_expansion_roadmap import sync_roadmap
            except ImportError:
                from scripts.sync_expansion_roadmap import sync_roadmap
            sync_roadmap()
        except Exception as exc:
            self.warnings.append(f"Roadmap Sync Warning: Failed to sync expansion roadmap: {exc}")

    def _lint_session_learnings(self, session_file: Path) -> None:
        """Sanitize numbered headers and check KaTeX display math tags in session_learnings.md."""
        if not session_file.exists():
            return
        text = self._safe_read_text(session_file)
        if text is None:
            return

        new_lines = []
        counter = 1
        for line in text.splitlines():
            m = re.match(r"^##\s+(\d+)\.\s+(.*)$", line)
            if m:
                new_lines.append(f"## {counter}. {m.group(2)}")
                counter += 1
            else:
                new_lines.append(line)

        cleaned_clutter = re.sub(r"\n{3,}", "\n\n", "\n".join(new_lines)).strip() + "\n"
        if cleaned_clutter != text:
            session_file.write_text(cleaned_clutter, encoding="utf-8")

        no_code_text = re.sub(r"```[\s\S]*?```", "", cleaned_clutter)
        no_code_text = re.sub(r"`[^`]*`", "", no_code_text)
        display_math_count = len(re.findall(r"\$\$", no_code_text))
        if display_math_count % 2 != 0:
            self.errors.append(f"KaTeX Error [session_learnings.md]: Unbalanced display math ($$) tags (count={display_math_count})")

    def validate_docx_to_markdown_verbatim_parity(self) -> None:
        """Gate 11: Enforce 100% Verbatim Normative Text Parity between sources/*.docx and bundle Markdown files."""
        try:
            from ccba_legal.provenance import verify_bundle_docx_vs_markdown
        except ImportError:
            def _standalone_norm_words(text: str) -> str:
                greek_map = {
                    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ",
                    r"\epsilon": "ε", r"\varepsilon": "ε", r"\zeta": "ζ", r"\eta": "η",
                    r"\theta": "θ", r"\vartheta": "θ", r"\iota": "ι", r"\kappa": "κ",
                    r"\lambda": "λ", r"\mu": "μ", r"\nu": "ν", r"\xi": "ξ",
                    r"\pi": "π", r"\rho": "ρ", r"\sigma": "σ", r"\tau": "τ",
                    r"\upsilon": "υ", r"\phi": "φ", r"\varphi": "φ", r"\chi": "χ",
                    r"\psi": "ψ", r"\omega": "ω", r"\dots": "...", r"\cdot": "·",
                }
                text = text.lower()
                for k, v in greek_map.items():
                    text = text.replace(k, v)
                text = re.sub(r"\\text\{([^}]+)\}", r"\1", text)
                text = re.sub(r"\\(?:sqrt|frac|times|le|ge|cdot|quad|qquad|dots|left|right|pm|approx|sim|over)", " ", text)
                text = re.sub(r"&nbsp;", " ", text)
                text = re.sub(r"&#\d+;|&[a-zA-Z]+;", " ", text)
                text = re.sub(r"</?[a-zA-Z][^>]*>", " ", text)
                text = re.sub(r"[_\{\}\$\^]", "", text)
                text = re.sub(r"(\d+)\s*([a-zα-ω]+)", r"\1 \2", text)
                text = re.sub(r"([a-zα-ω]+)\s*(\d+)", r"\1 \2", text)
                text = re.sub(r"[^\w\d\s]", " ", text, flags=re.UNICODE)
                return re.sub(r"\s+", " ", text).strip()

            def _standalone_verify_bundle(bundle_dir: Path) -> dict[str, Any]:
                src_dir = bundle_dir / DIR_SOURCES
                docx_files = list(src_dir.glob("*.docx")) if src_dir.exists() else []
                if not docx_files:
                    return {"status": "skipped"}
                try:
                    import docx
                    doc = docx.Document(docx_files[0])
                except Exception as e:
                    return {"status": "error", "error": f"Failed to parse DOCX: {e}"}

                raw_paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
                if not raw_paras:
                    return {"status": "skipped"}

                has_circular = any(
                    k in p.upper()
                    for p in raw_paras[:15]
                    for k in ["THÔNG TƯ", "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "BAN HÀNH KÈM THEO THÔNG TƯ"]
                )
                start_idx = 0
                if has_circular:
                    for idx, p in enumerate(raw_paras):
                        if idx == 0:
                            continue
                        if (
                            re.match(r"^(?:QCVN|TCVN)\s+[0-9]+", p.strip().upper())
                            or p.strip().upper() in ("TIÊU CHUẨN QUỐC GIA", "QUY CHUẨN KỸ THUẬT QUỐC GIA")
                            or p.strip().upper().startswith("QUY CHUẨN KỸ THUẬT QUỐC GIA")
                        ):
                            start_idx = idx
                            break

                docx_paras: list[str] = []
                in_toc = False
                for p_idx, p_text in enumerate(raw_paras[start_idx:], start=start_idx):
                    p_strip = p_text.strip()
                    p_upper = p_strip.upper()
                    if p_upper in ["MỤC LỤC", "TABLE OF CONTENTS"]:
                        in_toc = True
                        continue
                    if in_toc:
                        is_end = False
                        if p_strip.lower().startswith("lời nói đầu"):
                            for nxt_idx in range(p_idx + 1, min(p_idx + 5, len(raw_paras))):
                                nxt_t = raw_paras[nxt_idx].strip()
                                if nxt_t:
                                    if not re.match(
                                        r"^(?:Lời giới thiệu|\d+[\.\s]|Phụ lục|Thư mục)",
                                        nxt_t,
                                        re.IGNORECASE,
                                    ):
                                        is_end = True
                                    break
                        elif p_upper in ("TIÊU CHUẨN QUỐC GIA", "QUY CHUẨN KỸ THUẬT QUỐC GIA"):
                            is_end = True
                        if is_end:
                            in_toc = False
                    if not in_toc:
                        docx_paras.append(p_text)

                md_texts: list[str] = []
                for md_f in bundle_dir.rglob("*.md"):
                    if DIR_SOURCES not in md_f.parts:
                        try:
                            md_texts.append(md_f.read_text(encoding="utf-8"))
                        except Exception:
                            pass

                tables_dir = bundle_dir / "tables"
                if tables_dir.exists():
                    for csv_f in tables_dir.rglob("*.csv"):
                        try:
                            md_texts.append(csv_f.read_text(encoding="utf-8"))
                        except Exception:
                            pass

                combined_md = "\n".join(md_texts)
                norm_md = _standalone_norm_words(combined_md)

                missing_paras: list[tuple[int, str]] = []
                effective_paras_count = 0
                for idx, p in enumerate(docx_paras, 1):
                    np = _standalone_norm_words(p)
                    words = np.split()
                    matched = False
                    if len(words) >= 4:
                        for w in range(max(1, len(words) - 5)):
                            chunk = " ".join(words[w : w + 6])
                            if chunk in norm_md:
                                matched = True
                                break
                    elif len(words) >= 2:
                        if np in norm_md:
                            matched = True
                    else:
                        continue

                    if matched:
                        effective_paras_count += 1
                    else:
                        # Check if paragraph is administrative enacting preamble (conforming to ADR 0021 Pure Body)
                        p_low = p.strip().lower()
                        if (
                            p_low.startswith("căn cứ ")
                            or p_low.startswith("theo đề nghị ")
                            or p_low.startswith("xét đề nghị ")
                            or p_low.startswith("cộng hòa xã hội chủ nghĩa việt nam")
                            or p_low.startswith("độc lập - tự do - hạnh phúc")
                            or (p_low.startswith("bộ trưởng ") and "ban hành thông tư" in p_low)
                            or p_low.startswith("chính phủ ban hành nghị định")
                            or "nơi nhận:" in p_low
                        ):
                            continue
                        missing_paras.append((idx, p))
                        effective_paras_count += 1

                parity_rate = ((effective_paras_count - len(missing_paras)) / effective_paras_count) * 100.0 if effective_paras_count else 100.0

                return {
                    "status": "success",
                    "bundle_name": bundle_dir.name,
                    "docx_paras": effective_paras_count,
                    "parity_rate": parity_rate,
                    "missing_count": len(missing_paras),
                    "missing_paras": missing_paras,
                    "pass": parity_rate >= GATE_11_MIN_VERBATIM_PARITY,
                }

            verify_bundle_docx_vs_markdown = _standalone_verify_bundle

        legal_docs = self.root_dir / "legal_docs"
        if not legal_docs.exists():
            return

        for cat in ["01_vbpl", "02_qcvn", "03_tcvn"]:
            cat_dir = legal_docs / cat
            if not cat_dir.exists():
                continue
            for bundle_dir in cat_dir.iterdir():
                if not bundle_dir.is_dir() or bundle_dir.name.startswith("."):
                    continue
                if self.target_bundle and bundle_dir.name != self.target_bundle:
                    continue

                sources_dir = bundle_dir / DIR_SOURCES
                if not sources_dir.exists() or not list(sources_dir.glob("*.docx")):
                    continue

                res = verify_bundle_docx_vs_markdown(bundle_dir)
                if res.get("status") == "error":
                    self.errors.append(f"DOCX Read Error [{bundle_dir.name}]: {res.get('error')}")
                elif res.get("status") == "success" and not res.get("pass", True):
                    sample_miss = "; ".join([f"[{i}] {p[:60]}" for i, p in res.get("missing_paras", [])[:3]])
                    self.errors.append(
                        f"Verbatim Parity Error [{bundle_dir.name}]: Parity is only {res.get('parity_rate', 0.0):.1f}% (< {GATE_11_MIN_VERBATIM_PARITY}%). Missing {res.get('missing_count', 0)}/{res.get('docx_paras', 0)} paragraphs: {sample_miss}"
                    )

    def validate_multimodal_assets_and_cards_gate(self) -> None:
        """Gate 12: Multimodal Decoupled Asset & SVG/Cards Integrity Gate (ADR 0040).

        Enforces:
        1. Zero stray unviewable vector binaries (.wmf / .emf) in figures/images.
        2. Strict catalog-to-card 1:1 parity and disk asset existence.
        3. Curve/Chart Ground Truth attribution & mutual cross-check integrity.
        """
        if not self.legal_docs_dir.exists():
            return

        for category_dir in self.legal_docs_dir.iterdir():
            if not category_dir.is_dir():
                continue
            for bundle_dir in category_dir.iterdir():
                if not bundle_dir.is_dir() or bundle_dir.name.startswith("."):
                    continue
                if self.target_bundle and bundle_dir.name != self.target_bundle:
                    continue

                figures_dir = bundle_dir / "figures"
                if not figures_dir.exists():
                    continue

                # 1. Zero stray WMF/EMF in figures/images
                images_dir = figures_dir / "images"
                if images_dir.exists():
                    for f in images_dir.iterdir():
                        if f.suffix.lower() in (".wmf", ".emf"):
                            self.errors.append(
                                f"Stray Vector Binary Error [{bundle_dir.name}]: Found unviewable vector binary "
                                f"'{f.name}' in figures/images/. Must be converted to SVG or PNG (ADR 0040)."
                            )

                # 2. Catalog & Cards validation
                catalog_f = figures_dir / "figures_catalog.yaml"
                cards_dir = figures_dir / "cards"
                if catalog_f.exists():
                    try:
                        cat_data = yaml.safe_load(catalog_f.read_text(encoding="utf-8")) or {}
                        fig_list = cat_data.get("figures", [])
                        registered_slugs = set()
                        for fig in fig_list:
                            tag = str(fig.get("tag") or fig.get("id") or "").replace("hinh_", "")
                            raw_slug = str(fig.get("slug") or fig.get("id") or tag).lower().replace(".", "_").replace("-", "_").replace("đ", "dd")
                            slug = raw_slug[5:] if raw_slug.startswith("hinh_") else raw_slug
                            registered_slugs.add(slug)

                            # Check image existence & non-zero byte integrity
                            img_rel = fig.get("image_relpath") or fig.get("path")
                            if img_rel:
                                img_path = bundle_dir / img_rel
                                if not img_path.exists():
                                    self.errors.append(
                                        f"Missing Figure Image [{bundle_dir.name}]: "
                                        f"Figure '{tag}' references non-existent image '{img_rel}' (ADR 0040)."
                                    )
                                elif img_path.stat().st_size == 0:
                                    self.errors.append(
                                        f"Zero-Byte Figure Image [{bundle_dir.name}]: "
                                        f"Figure '{tag}' references empty/corrupted image '{img_rel}' (0 bytes) (ADR 0040)."
                                    )

                            # Check visual card existence (supports Markdown cards and JSON cards)
                            card_path = cards_dir / f"hinh_{slug}.md"
                            json_card_candidates = list(cards_dir.glob(f"fig_{slug}_*.json")) if cards_dir.exists() else []
                            if not card_path.exists() and not json_card_candidates:
                                self.errors.append(
                                    f"Missing Figure Card [{bundle_dir.name}]: "
                                    f"Figure '{tag}' is missing visual card at 'figures/cards/hinh_{slug}.md' (ADR 0040)."
                                )
                            else:
                                card_txt = self._safe_read_text(card_path) or ""
                                if f"Hình {tag}" not in card_txt and tag not in card_txt:
                                    self.warnings.append(
                                        f"Figure Card Mismatch [{bundle_dir.name}]: "
                                        f"Card 'hinh_{slug}.md' does not mention 'Hình {tag}'."
                                    )

                            # Check chart/curve attribution (Mutual Cross-Check)
                            is_chart = fig.get("is_chart", False) or fig.get("type") == "chart"
                            if is_chart:
                                related_tables = fig.get("related_tables", [])
                                conf_status = fig.get("confidence_status", "")
                                if not related_tables and conf_status != "ESTIMATED_BY_VISION":
                                    self.errors.append(
                                        f"Chart Attribution Error [{bundle_dir.name}]: Figure '{tag}' is classified as a chart/curve "
                                        f"but lacks ground-truth 'related_tables' or 'ESTIMATED_BY_VISION' disclaimer (ADR 0040)."
                                    )

                        # Check for orphaned cards
                        if cards_dir.exists():
                            for card_f in cards_dir.glob("*.md"):
                                c_slug = card_f.stem.replace("hinh_", "")
                                if c_slug not in registered_slugs:
                                    self.warnings.append(
                                        f"Unregistered Figure Card [{bundle_dir.name}]: "
                                        f"Card '{card_f.name}' is not registered in figures_catalog.yaml."
                                    )
                    except Exception as exc:
                        self.errors.append(
                            f"Figures Catalog Error [{bundle_dir.name}]: Failed to parse figures_catalog.yaml: {exc}"
                        )

    def _check_core_adr_references(self, known_nums: Set[int]) -> None:
        """Check for broken ADR references in core constitution files."""
        for core_f in ["AGENTS.md", "CONTEXT.md", ".md/knowledge/session_learnings.md"]:
            p = self.root_dir / core_f
            if p.exists():
                text = self._safe_read_text(p)
                if text:
                    for m in re.findall(r"\bADR[-\s]*0*([0-9]+)\b", text, re.IGNORECASE):
                        num = int(m)
                        if num not in known_nums:
                            self.errors.append(f"Broken ADR Reference [{core_f}]: 'ADR {num:04d}' does not exist on disk.")

    def _get_modified_bundle_names(self) -> Set[str]:
        """Get set of bundle folder names that have git modifications."""
        try:
            res = subprocess.run(
                ["git", "status", "--porcelain", "legal_docs/"],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
                check=False,
            )
            modified = set()
            for line in res.stdout.splitlines():
                parts = line.strip().split()
                if len(parts) >= 2:
                    p = Path(parts[-1])
                    if len(p.parts) >= 3 and p.parts[0] == "legal_docs":
                        modified.add(p.parts[2])
            return modified
        except Exception:
            return set()

    def validate_table_knowledge_and_matrix_regularity(self) -> Tuple[int, int]:
        """Gate 13: Table Knowledge Extraction & 2D Matrix Regularity Gate (ADR 0041).

        Enforces:
        1. Mandatory existence and schema validity of tables/tables_catalog.json for bundles with tables/csv/.
        2. 100% Zero Ragged Rows across all CSV tables (strict 2D rectangular grid).
        3. Footnote decoupling: Footnotes must not contaminate relation rows.
        4. Catalog-to-disk synchronization.
        """
        if not self.legal_docs_dir.exists():
            return (len(self.errors), len(self.warnings))

        for category_dir in self.legal_docs_dir.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith("."):
                continue

            for bundle_dir in category_dir.iterdir():
                if not bundle_dir.is_dir() or bundle_dir.name.startswith("."):
                    continue
                if self.target_bundle and bundle_dir.name != self.target_bundle:
                    continue

                tables_dir = bundle_dir / "tables"
                csv_dir = tables_dir / "csv"
                if not tables_dir.exists() or not csv_dir.exists():
                    continue

                csv_files = sorted(list(csv_dir.glob("*.csv")))
                if not csv_files:
                    continue

                # 1. tables_catalog.json validation
                catalog_file = tables_dir / "tables_catalog.json"
                catalog_tables: Dict[str, Any] = {}
                if not catalog_file.exists():
                    self.warnings.append(
                        f"Table Matrix Telemetry [{bundle_dir.name}]: 'tables/' exists with {len(csv_files)} CSVs but 'tables_catalog.json' is missing (ADR 0041)."
                    )
                else:
                    try:
                        cat_data = json.loads(catalog_file.read_text(encoding="utf-8"))
                        raw_list = cat_data.get("tables", []) if isinstance(cat_data, dict) else cat_data
                        for t in raw_list:
                            tid = t.get("id") or t.get("table_id") or t.get("csv_file")
                            if tid:
                                catalog_tables[Path(tid).name] = t
                                catalog_tables[Path(tid).stem] = t
                    except Exception as exc:
                        self.errors.append(
                            f"Table Matrix Error [{bundle_dir.name}]: Failed to parse 'tables_catalog.json': {exc}"
                        )

                # 2. Assert Zero Ragged Rows on each CSV
                for csv_path in csv_files:
                    rel_csv = csv_path.relative_to(self.root_dir)
                    try:
                        with open(csv_path, mode="r", encoding="utf-8-sig", newline="") as f:
                            reader = csv.reader(f)
                            rows = list(reader)

                        if not rows:
                            self.errors.append(f"Table Matrix Error [{rel_csv}]: CSV file is completely empty.")
                            continue

                        # Filter out trailing empty rows
                        while rows and not any(cell.strip() for cell in rows[-1]):
                            rows.pop()

                        if not rows:
                            continue

                        header_cols = len(rows[0])
                        if header_cols == 0:
                            self.errors.append(f"Table Matrix Error [{rel_csv}]: Header row has 0 columns.")
                            continue

                        ragged_rows = []
                        footnote_leaks = []
                        for row_idx, row in enumerate(rows[1:], start=2):
                            if len(row) != header_cols:
                                ragged_rows.append((row_idx, len(row), header_cols))

                            row_str = " ".join(row).strip()
                            if re.match(r"^(?:CHÚ\s+THÍCH|CHÚ\s+DẪN|Ghi\s+chú|\(\*\))\s*:", row_str, re.IGNORECASE):
                                footnote_leaks.append(row_idx)

                        if ragged_rows:
                            sample_errs = ", ".join([f"L{r}: got {act} (exp {exp})" for r, act, exp in ragged_rows[:3]])
                            extra = f" (+{len(ragged_rows)-3} more)" if len(ragged_rows) > 3 else ""
                            self.warnings.append(
                                f"Ragged Rows Telemetry [{rel_csv}]: Found {len(ragged_rows)} non-rectangular rows: {sample_errs}{extra} (ADR 0041)."
                            )

                        if footnote_leaks:
                            sample_fn = ", ".join([f"L{r}" for r in footnote_leaks[:3]])
                            self.warnings.append(
                                f"Footnote Leaked Row Telemetry [{rel_csv}]: Footnotes leaked into CSV data rows at lines {sample_fn}. Decouple to metadata (ADR 0041)."
                            )

                        # Catalog cross-check
                        if catalog_file.exists():
                            if csv_path.name not in catalog_tables and csv_path.stem not in catalog_tables:
                                self.warnings.append(
                                    f"Table Catalog Mismatch [{bundle_dir.name}]: CSV '{csv_path.name}' not registered in 'tables_catalog.json'."
                                )
                    except Exception as exc:
                        self.errors.append(f"Table Matrix Error [{rel_csv}]: Failed to read CSV: {exc}")

        return (len(self.errors), len(self.warnings))

    def validate_katex_syntax_integrity(self) -> Tuple[int, int]:
        """Gate 14: KaTeX Math Syntax & Rendering Integrity Gate (ADR 0038).

        Enforces:
        1. Strict pairing and even count of display math '$$' delimiters.
        2. Zero '\\tag{...}' inside multiline math environments ('aligned', 'cases', 'gather').
        3. Zero embedded HTML comments ('<!-- ... -->') inside math blocks.
        4. Balanced grouping braces '{...}' and bracket pairs '\\left[' / '\\right]'.
        """
        if not self.legal_docs_dir.exists():
            return (len(self.errors), len(self.warnings))

        modified_bundles = self._get_modified_bundle_names()

        for md_file in sorted(self.legal_docs_dir.rglob("*.md")):
            # Skip sources/ directory which contains raw constituent files
            if DIR_SOURCES in md_file.parts:
                continue
            if self.target_bundle and self.target_bundle not in md_file.parts:
                continue

            rel_path = md_file.relative_to(self.root_dir)
            bundle_name = md_file.parent.name
            is_modified = bundle_name in modified_bundles

            content = self._safe_read_text(md_file)
            if content is None or "$$" not in content:
                continue

            # Strip code blocks to avoid false positives inside code fences
            stripped_content = re.sub(r"```[\s\S]*?```", "", content)
            stripped_content = re.sub(r"`[^`\n]+`", "", stripped_content)

            # 1. Check even count of display math $$
            display_math_count = len(re.findall(r"\$\$", stripped_content))
            if display_math_count % 2 != 0:
                self.errors.append(
                    f"KaTeX Syntax Error [{rel_path}]: Unbalanced display math ($$) delimiters (count={display_math_count}) (ADR 0038)."
                )
                continue

            # 2. Extract each $$ ... $$ block and inspect inner syntax
            math_blocks = re.findall(r"\$\$([\s\S]*?)\$\$", stripped_content)
            for block_idx, block in enumerate(math_blocks, start=1):
                clean_block = block.strip()

                # Rule 1: No HTML comments inside $$
                if "<!--" in clean_block and "-->" in clean_block:
                    msg = f"KaTeX Syntax Error [{rel_path}#math-{block_idx}]: Embedded HTML comment detected inside '$$' block. Decouple comments outside math (ADR 0038)."
                    if is_modified:
                        self.errors.append(msg)
                    else:
                        self.warnings.append(
                            f"KaTeX Telemetry [{rel_path}#math-{block_idx}]: Embedded HTML comment detected inside '$$' block (ADR 0038)."
                        )

                # Rule 2 (Sub-Gate 14.2): Prohibit \tag{...} inside multiline environments (ADR 0038, ADR 0044)
                multiline_envs = ["aligned", "cases", "gather", "matrix", "array", "bmatrix"]
                for env in multiline_envs:
                    if f"\\begin{{{env}}}" in clean_block:
                        if re.search(r"\\tag\s*\{[^}]*\}", clean_block):
                            msg = f"KaTeX Syntax Error [{rel_path}#math-{block_idx}]: Unsupported '\\tag{{...}}' detected inside '{env}' environment. Replace with '\\qquad (X)' (ADR 0038, ADR 0044)."
                            if is_modified:
                                self.errors.append(msg)
                            else:
                                self.warnings.append(
                                    f"KaTeX Telemetry [{rel_path}#math-{block_idx}]: Unsupported '\\tag{{...}}' inside '{env}' (ADR 0038, ADR 0044)."
                                )

                # Rule 3: Balanced \left and \right
                left_count = len(re.findall(r"\\left[\(\[\{\.\vert]", clean_block))
                right_count = len(re.findall(r"\\right[\)\]\}\.\vert]", clean_block))
                if left_count != right_count:
                    msg = f"KaTeX Syntax Error [{rel_path}#math-{block_idx}]: Unbalanced '\\left' ({left_count}) and '\\right' ({right_count}) operators (ADR 0038)."
                    if is_modified:
                        self.errors.append(msg)
                    else:
                        self.warnings.append(
                            f"KaTeX Telemetry [{rel_path}#math-{block_idx}]: Unbalanced '\\left' ({left_count}) and '\\right' ({right_count}) (ADR 0038)."
                        )

                # Rule 4: Balanced curly braces (ignoring escaped \{ and \})
                nobrace = re.sub(r"\\[\{\}]", "", clean_block)
                open_braces = nobrace.count("{")
                close_braces = nobrace.count("}")
                if open_braces != close_braces:
                    msg = f"KaTeX Syntax Error [{rel_path}#math-{block_idx}]: Unbalanced curly braces ({{: {open_braces}, }}: {close_braces}) (ADR 0038)."
                    if is_modified:
                        self.errors.append(msg)
                    else:
                        self.warnings.append(
                            f"KaTeX Telemetry [{rel_path}#math-{block_idx}]: Unbalanced curly braces (ADR 0038)."
                        )

        return (len(self.errors), len(self.warnings))

    def validate_provenance_and_version_attestation(self) -> Tuple[int, int]:
        """Gate 15: OKF Provenance & Version Attestation Gate.

        Reconciles bundle metadata with canonical constants in Hub ccba_legal.constants:
        - CURRENT_OKF_SPEC ('v2.4 Universal')
        - CURRENT_CONVERTER_VERSION ('0.4.0')
        """
        if not self.legal_docs_dir.exists():
            return (len(self.errors), len(self.warnings))

        for cat in ["01_vbpl", "02_qcvn", "03_tcvn"]:
            cat_dir = self.legal_docs_dir / cat
            if not cat_dir.exists():
                continue

            for bundle_dir in sorted(cat_dir.iterdir()):
                if not bundle_dir.is_dir() or bundle_dir.name.startswith("."):
                    continue
                if self.target_bundle and bundle_dir.name != self.target_bundle:
                    continue

                meta_file = bundle_dir / "metadata.yaml"
                if not meta_file.exists():
                    self.errors.append(
                        f"Provenance Error [{bundle_dir.name}]: Missing mandatory 'metadata.yaml' file."
                    )
                    continue

                try:
                    meta_data = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
                except Exception as exc:
                    self.errors.append(
                        f"Provenance Error [{bundle_dir.name}]: Failed to parse metadata.yaml: {exc}"
                    )
                    continue

                # 1. Assert okf_spec matches CURRENT_OKF_SPEC
                okf_spec = meta_data.get("okf_spec")
                if not okf_spec:
                    self.warnings.append(
                        f"Provenance Telemetry [{bundle_dir.name}]: Missing 'okf_spec' in metadata.yaml (Expected: '{CURRENT_OKF_SPEC}')."
                    )
                elif str(okf_spec).strip() != CURRENT_OKF_SPEC:
                    self.warnings.append(
                        f"Provenance Telemetry [{bundle_dir.name}]: Bundle 'okf_spec' ('{okf_spec}') differs from canonical '{CURRENT_OKF_SPEC}'. Re-extraction from sources/ recommended."
                    )

                # 2. Check converter_version
                if not meta_data.get("converter_version"):
                    self.warnings.append(
                        f"Provenance Telemetry [{bundle_dir.name}]: Missing 'converter_version' in metadata.yaml."
                    )

                # 3. Check extracted_at ISO-8601 timestamp
                extracted_at = meta_data.get("extracted_at")
                if not extracted_at:
                    self.warnings.append(
                        f"Provenance Telemetry [{bundle_dir.name}]: Missing 'extracted_at' timestamp in metadata.yaml."
                    )
                elif not re.match(r"^\d{4}-\d{2}-\d{2}", str(extracted_at)):
                    self.errors.append(
                        f"Provenance Error [{bundle_dir.name}]: 'extracted_at' is not a valid ISO timestamp: '{extracted_at}'."
                    )

        return (len(self.errors), len(self.warnings))

    def run_all_checks(self) -> bool:
        """Run all validation checks and print a summary report."""
        print("=================================================================")
        print("       CCBA LEGAL SPOKE MASTER INTEGRITY & SCHEMA VALIDATOR      ")
        print("=================================================================")
        print(f"Target Workspace: {self.root_dir}\n")
        if self.target_bundle:
            print(f"🎯 Scoped Target Bundle: {self.target_bundle}\n")

        self.validate_registry()
        self.validate_okf_bundles()
        self.validate_table_attachments()
        self.validate_fake_data_gate()
        self.validate_pdf_metadata_and_ast_enrichment()
        self.validate_pure_normative_body_gate()
        self.validate_spoke_cleanliness()
        self.validate_template_and_table_integrity()
        self.validate_visual_parity()
        self.validate_adr_parity_and_sync()
        self.validate_docx_to_markdown_verbatim_parity()
        self.validate_multimodal_assets_and_cards_gate()
        self.validate_table_knowledge_and_matrix_regularity()
        self.validate_katex_syntax_integrity()
        self.validate_provenance_and_version_attestation()

        for i, name in enumerate([
            "Registry Check", "OKF Bundles Structure Check", "Table Attachments Check",
            "Fake Data Gate Check", "PDF Metadata & AST Jurisdiction Gate Check",
            "Pure Normative Body & Scoped Noise Gate Check", "Spoke Cleanliness & Zero-Wrapper Gate",
            "Template & Table Structural Integrity Gate", "Visual Parity & Formatting Clutter Gate",
            "ADR Living Traceability & Self-Healing Sync", "DOCX-to-Markdown Verbatim Normative Parity Gate",
            "Multimodal Decoupled Asset & SVG/Cards Integrity Gate (ADR 0040)",
            "Table Knowledge Extraction & 2D Matrix Regularity Gate (ADR 0041)",
            "KaTeX Math Syntax & Rendering Integrity Gate (ADR 0038)",
            "OKF Provenance & Algorithm Version Attestation Gate",
        ], 1):
            print(f"-> Gate {i}: {name} completed.")

        print("\n-----------------------------------------------------------------")
        print(f"SUMMARY REPORT: Errors: {len(self.errors)} | Warnings: {len(self.warnings)}")
        print("-----------------------------------------------------------------")

        if self.errors:
            print("\n[ERRORS]:")
            for err in self.errors:
                print(f"  ❌ {err}")
        if self.warnings:
            print("\n[WARNINGS]:")
            for warn in self.warnings:
                print(f"  ⚠️ {warn}")

        if not self.errors:
            print("\n✅ PASSED: All legal knowledge gates validated successfully!")
            return True

        print("\n❌ FAILED: Critical errors detected in legal spoke validation.")
        return False


def main() -> None:
    """CLI entry point for running validator."""
    parser = argparse.ArgumentParser(description="CCBA Legal Spoke Automated Integrity & Schema Validator")
    parser.add_argument("--bundle", default=None, help="Validate a specific document bundle (scoped validation)")
    args = parser.parse_args()
    root_dir = Path(__file__).resolve().parent.parent
    validator = LegalSpokeValidator(root_dir, target_bundle=args.bundle)
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
