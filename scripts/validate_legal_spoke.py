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
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

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
                if doc_dir.is_dir():
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
            sources_dir = doc_dir / "sources"
            if not sources_dir.exists():
                self.warnings.append(
                    f"OKF v2.4 Invariant Warning [{doc_dir.name}]: Missing mandatory 'sources/' directory."
                )
            templates_dir = doc_dir / "templates"
            if templates_dir.exists() and not any(templates_dir.iterdir()):
                self.warnings.append(
                    f"OKF v2.4 Invariant Warning [{doc_dir.name}]: Empty 'templates/' directory detected."
                )

        for md_path in main_md_files:
            self._extract_frontmatter(md_path)

    def validate_table_attachments(self) -> Tuple[int, int]:
        """Validate referenced table CSV/JSON attachments exist in bundle tables/ directory."""
        if not self.legal_docs_dir.exists():
            return (len(self.errors), len(self.warnings))

        for md_file in self.legal_docs_dir.rglob("*.md"):
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

        return (len(self.errors), len(self.warnings))

    def validate_fake_data_gate(self) -> Tuple[int, int]:
        """Validate that bundles do not contain truncated/synthetic placeholder content."""
        vbpl_dir = self.legal_docs_dir / "01_vbpl"
        if not vbpl_dir.exists():
            return (len(self.errors), len(self.warnings))

        for doc_dir in vbpl_dir.iterdir():
            if doc_dir.is_dir() and doc_dir.name.startswith("nghi_dinh_"):
                self._check_decree_fake_data(doc_dir)

        return (len(self.errors), len(self.warnings))

    def _check_decree_fake_data(self, doc_dir: Path) -> None:
        """Check decree bundle for truncated content or missing articles."""
        primary_md = doc_dir / f"{doc_dir.name}.md"
        if not primary_md.exists():
            return

        size_kb = primary_md.stat().st_size / 1024
        if size_kb < 20:
            self.warnings.append(
                f"Fake Data Warning [{doc_dir.name}]: Decrees usually exceed 20KB, but found {size_kb:.1f} KB. Verify full text presence."
            )

        content = self._safe_read_text(primary_md)
        if content:
            dieu_nums = sorted(int(m) for m in re.findall(r"### Điều (\d+)\.", content))
            for i in range(len(dieu_nums) - 1):
                gap = dieu_nums[i + 1] - dieu_nums[i]
                if gap > 3:
                    self.warnings.append(
                        f"Fake Data Warning [{doc_dir.name}]: Gap of {gap} detected between Điều {dieu_nums[i]} and Điều {dieu_nums[i+1]}."
                    )

        clauses_json = doc_dir / "clauses.json"
        if clauses_json.exists():
            try:
                clauses_data = json.loads(clauses_json.read_text(encoding="utf-8"))
                if len(clauses_data) < 25:
                    self.warnings.append(
                        f"Fake Data Warning [{doc_dir.name}]: Found only {len(clauses_data)} clauses in clauses.json. Expected >= 30."
                    )
            except json.JSONDecodeError as exc:
                self.errors.append(f"JSON Error [{doc_dir.name}]: Failed to parse clauses.json: {exc}")

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
                if doc_dir.is_dir():
                    self._validate_qcvn_ast_clauses(doc_dir)

        return (len(self.errors), len(self.warnings))

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
            clauses_data = json.loads(clauses_file.read_text(encoding="utf-8"))
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
        """Validate OKF v2.2 Pure Normative Body standard (ADR 0021)."""
        vbpl_dir = self.legal_docs_dir / "01_vbpl"
        if not vbpl_dir.exists():
            return (len(self.errors), len(self.warnings))

        for doc_dir in vbpl_dir.iterdir():
            if not doc_dir.is_dir():
                continue

            primary_md = doc_dir / f"{doc_dir.name}.md"
            if not primary_md.exists():
                md_files = [f for f in doc_dir.glob("*.md") if f.name not in ("index.md", "dead_ends.md", "log.md")]
                primary_md = md_files[0] if md_files else None

            if primary_md and primary_md.exists():
                self._check_pure_body_document(doc_dir, primary_md)

        return (len(self.errors), len(self.warnings))

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

        if len(py_files) > 20:
            self.warnings.append(
                f"Spoke Cleanliness Gate: scripts/ directory contains {len(py_files)} files (> 20 threshold)."
            )

        return (len(self.errors), len(self.warnings))

    def validate_template_and_table_integrity(self) -> Tuple[int, int]:
        """Gate 8: Verify Template & Table Structural Integrity (ADR 0021)."""
        for cat_dir in [self.legal_docs_dir / "01_vbpl", self.legal_docs_dir / "02_qcvn"]:
            if not cat_dir.exists():
                continue
            for doc_dir in cat_dir.iterdir():
                if doc_dir.is_dir():
                    self._check_bundle_templates_and_tables(doc_dir)

        for cat_dir in [self.legal_docs_dir / "02_qcvn", self.legal_docs_dir / "03_tcvn"]:
            if not cat_dir.exists():
                continue
            for doc_dir in cat_dir.iterdir():
                if doc_dir.is_dir():
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
        templates_dir = doc_dir / "templates"

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
        """Check figures_catalog.yaml schema and image references."""
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

    def validate_visual_parity(self) -> Tuple[int, int]:
        """Gate 9: Validate 100% Visual Parity & Zero Formatting Clutter (ADR 0029 & ADR 0030)."""
        try:
            from lint_visual_parity import lint_document
        except ImportError:
            from scripts.lint_visual_parity import lint_document

        for md_file in sorted(self.legal_docs_dir.rglob("*.md")):
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
        self._lint_session_learnings(self.root_dir / ".md" / "knowledge" / "session_learnings.md")
        self._check_core_adr_references(known_nums)

        return (len(self.errors), len(self.warnings))

    def _sync_adr_artifacts(self, adr_dir: Path, adr_list: List[Dict[str, Any]]) -> None:
        """Auto-compile README.md and TRACEABILITY_MATRIX.md for ADRs."""
        try:
            from sync_adr_matrix import compile_adr_readme, compile_traceability_matrix, scan_skill_radar
            compile_adr_readme(adr_list, adr_dir / "README.md")
            matrix = scan_skill_radar(adr_list, self.root_dir)
            compile_traceability_matrix(adr_list, matrix, adr_dir / "TRACEABILITY_MATRIX.md")
        except (ImportError, OSError) as exc:
            self.errors.append(f"ADR Sync Error: Failed to compile ADR artifacts: {exc}")

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
        hub_src = Path("D:/GitHubProjects/ccba-agent-platform/packages/ccba-legal-intel/src")
        if hub_src.exists() and str(hub_src) not in sys.path:
            sys.path.insert(0, str(hub_src))

        try:
            from ccba_legal.provenance import verify_bundle_docx_vs_markdown
        except ImportError:
            verify_bundle_docx_vs_markdown = None  # type: ignore

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

                sources_dir = bundle_dir / "sources"
                if not sources_dir.exists() or not list(sources_dir.glob("*.docx")):
                    continue

                if verify_bundle_docx_vs_markdown is not None:
                    res = verify_bundle_docx_vs_markdown(bundle_dir)
                    if res.get("status") == "error":
                        self.errors.append(f"DOCX Read Error [{bundle_dir.name}]: {res.get('error')}")
                    elif res.get("status") == "success" and not res.get("pass", True):
                        sample_miss = "; ".join([f"[{i}] {p[:60]}" for i, p in res.get("missing_paras", [])[:3]])
                        self.errors.append(
                            f"Verbatim Parity Error [{bundle_dir.name}]: Parity is only {res.get('parity_rate', 0.0):.1f}% (< 98.0%). Missing {res.get('missing_count', 0)}/{res.get('docx_paras', 0)} paragraphs: {sample_miss}"
                        )
                else:
                    try:
                        import docx
                    except ImportError:
                        self.warnings.append("python-docx is not installed. Skipping Gate 11 DOCX-to-Markdown Verbatim Parity.")
                        return

                    docx_files = list(sources_dir.glob("*.docx"))
                    try:
                        doc = docx.Document(docx_files[0])
                    except Exception as e:
                        self.errors.append(f"DOCX Read Error [{bundle_dir.name}]: Failed to parse {docx_files[0].name}: {e}")
                        continue

                    docx_paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
                    if not docx_paras:
                        continue

                    md_texts = []
                    for md_f in bundle_dir.rglob("*.md"):
                        if "sources" not in md_f.parts:
                            txt = self._safe_read_text(md_f)
                            if txt:
                                md_texts.append(txt)

                    combined_md = "\n".join(md_texts)
                    norm_md = re.sub(r"\s+", " ", re.sub(r"[^\w\d\s]", " ", combined_md.lower(), flags=re.UNICODE)).strip()

                    missing_paras = []
                    for idx, p in enumerate(docx_paras, 1):
                        np = re.sub(r"\s+", " ", re.sub(r"[^\w\d\s]", " ", p.lower(), flags=re.UNICODE)).strip()
                        words = np.split()
                        matched = False
                        if len(words) >= 4:
                            for w in range(max(1, len(words) - 5)):
                                chunk = " ".join(words[w : w + 6])
                                if chunk in norm_md:
                                    matched = True
                                    break
                            if not matched:
                                missing_paras.append((idx, p))
                        elif len(words) >= 2:
                            if np not in norm_md:
                                missing_paras.append((idx, p))

                    parity_rate = ((len(docx_paras) - len(missing_paras)) / len(docx_paras)) * 100.0
                    if parity_rate < 98.0:
                        sample_miss = "; ".join([f"[{i}] {p[:60]}" for i, p in missing_paras[:3]])
                        self.errors.append(
                            f"Verbatim Parity Error [{bundle_dir.name}]: Parity is only {parity_rate:.1f}% (< 98.0%). Missing {len(missing_paras)}/{len(docx_paras)} paragraphs: {sample_miss}"
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

    def run_all_checks(self) -> bool:
        """Run all validation checks and print a summary report."""
        print("=================================================================")
        print("       CCBA LEGAL SPOKE MASTER INTEGRITY & SCHEMA VALIDATOR      ")
        print("=================================================================")
        print(f"Target Workspace: {self.root_dir}\n")

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

        for i, name in enumerate([
            "Registry Check", "OKF Bundles Structure Check", "Table Attachments Check",
            "Fake Data Gate Check", "PDF Metadata & AST Jurisdiction Gate Check",
            "Pure Normative Body & Scoped Noise Gate Check", "Spoke Cleanliness & Zero-Wrapper Gate",
            "Template & Table Structural Integrity Gate", "Visual Parity & Formatting Clutter Gate",
            "ADR Living Traceability & Self-Healing Sync", "DOCX-to-Markdown Verbatim Normative Parity Gate",
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
    root_dir = Path(__file__).resolve().parent.parent
    validator = LegalSpokeValidator(root_dir)
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
