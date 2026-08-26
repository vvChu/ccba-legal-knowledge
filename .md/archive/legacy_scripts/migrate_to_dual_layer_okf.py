"""CCBA Dual-Layer OKF v2.2 Frontmatter Migration Engine.

Automates the standardization of YAML Frontmatter across all 30 legal and technical
documents in legal_docs/ to comply with Google Cloud OKF Core Specification and
CCBA Legal & Technical Knowledge Graph Extensions.

Preserves 100% of the normative body text, markdown anchors, tables, and math formulas.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

# Enforce UTF-8 output encoding for Windows PowerShell
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class OKFSchemaMigrator:
    """Migrates existing legal markdown bundles to Dual-Layer OKF v2.2 Frontmatter."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.legal_docs_dir = root_dir / "legal_docs"
        self.registry_file = root_dir / "legal_registry.yaml"
        self.registry_map: Dict[str, Dict[str, Any]] = {}
        self.stats = {"scanned": 0, "migrated": 0, "errors": 0}

    def load_registry(self) -> None:
        """Load legal_registry.yaml to build canonical metadata lookup map."""
        if not self.registry_file.exists():
            print(f"❌ Registry file not found at {self.registry_file}")
            return

        with open(self.registry_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        all_docs: List[Dict[str, Any]] = []
        laws = data.get("laws", [])
        if isinstance(laws, list):
            all_docs.extend(laws)
        
        documents = data.get("documents", {})
        if isinstance(documents, dict):
            all_docs.extend(documents.values())
        elif isinstance(documents, list):
            all_docs.extend(documents)

        for doc in all_docs:
            if not isinstance(doc, dict):
                continue
            doc_id = doc.get("id", "")
            bundle_path = doc.get("bundle_path", "").strip("/\\")
            if doc_id:
                self.registry_map[doc_id] = doc
            if bundle_path:
                bundle_name = Path(bundle_path).name
                self.registry_map[bundle_name] = doc
                # Also store normalized relative path
                self.registry_map[bundle_path.replace("\\", "/")] = doc

        print(f"✅ Loaded {len(self.registry_map)} registry index mappings from legal_registry.yaml")

    def _determine_okf_type(self, category: str, doc_type: str) -> str:
        """Map document category to Google OKF Concept Type."""
        cat_lower = category.lower()
        doc_type_lower = doc_type.lower()
        if "02_qcvn" in cat_lower or "qcvn" in doc_type_lower or "quy chuẩn" in doc_type_lower:
            return "technical_standard_qcvn"
        if "03_tcvn" in cat_lower or "tcvn" in doc_type_lower or "tiêu chuẩn" in doc_type_lower:
            return "technical_standard_tcvn"
        if "04_appendices" in cat_lower or "phụ lục" in doc_type_lower:
            return "legal_comparative_matrix"
        return "legal_normative_body"

    def _build_tags(self, title: str, doc_type: str, category: str) -> List[str]:
        """Generate search tags based on title, type, and category."""
        tags = set()
        title_lower = title.lower()
        
        if "xây dựng" in title_lower:
            tags.add("xay_dung")
        if "phòng cháy" in title_lower or "chữa cháy" in title_lower or "pccc" in title_lower:
            tags.add("pccc")
            tags.add("an_toan_chay")
        if "đấu thầu" in title_lower:
            tags.add("dau_thau")
        if "đầu tư" in title_lower:
            tags.add("dau_tu_xay_dung")
        if "quy hoạch" in title_lower:
            tags.add("quy_hoach")
        if "quản lý dự án" in title_lower:
            tags.add("quan_ly_du_an")
        if "chi phí" in title_lower:
            tags.add("quan_ly_chi_phi")
        if "chất lượng" in title_lower:
            tags.add("quan_ly_chat_luong")
        if "hợp đồng" in title_lower:
            tags.add("hop_dong_xay_dung")
        if "nhà ở" in title_lower or "chung cư" in title_lower:
            tags.add("nha_o")

        # Category / type tags
        if "02_qcvn" in category or "QCVN" in doc_type:
            tags.add("qcvn")
            tags.add("quy_chuan_ky_thuat")
        elif "03_tcvn" in category or "TCVN" in doc_type:
            tags.add("tcvn")
            tags.add("tieu_chuan_ky_thuat")
        elif "01_vbpl" in category:
            tags.add("vbpl")
            if "Luật" in doc_type:
                tags.add("luat")
            elif "Nghị định" in doc_type:
                tags.add("nghi_dinh")
            elif "Thông tư" in doc_type:
                tags.add("thong_tu")

        return sorted(list(tags)) if tags else ["xay_dung", "phap_ly"]

    def _normalize_relations(self, raw_relations: Any) -> List[Dict[str, Any]]:
        """Normalize raw relations from dict/list into structured OKF relations list."""
        if not raw_relations:
            return []
        
        norm_list: List[Dict[str, Any]] = []
        if isinstance(raw_relations, dict):
            for rel_type, targets in raw_relations.items():
                if isinstance(targets, list):
                    for target in targets:
                        norm_list.append({"target_id": str(target), "relation_type": str(rel_type)})
                elif isinstance(targets, (str, int)):
                    norm_list.append({"target_id": str(targets), "relation_type": str(rel_type)})
        elif isinstance(raw_relations, list):
            for item in raw_relations:
                if isinstance(item, dict):
                    norm_list.append(item)
                elif isinstance(item, str):
                    norm_list.append({"target_id": item, "relation_type": "related_to"})
        return norm_list

    def migrate_bundle(self, bundle_dir: Path, category: str) -> bool:
        """Migrate a single bundle directory to Dual-Layer OKF v2.2."""
        self.stats["scanned"] += 1
        
        # 1. Find the primary markdown file
        main_md_candidates = list(bundle_dir.glob(f"{bundle_dir.name}.md"))
        if not main_md_candidates:
            all_mds = [f for f in bundle_dir.glob("*.md") if f.name not in ("index.md", "dead_ends.md", "log.md")]
            if all_mds:
                main_md_candidates = all_mds
            else:
                index_candidate = bundle_dir / "index.md"
                if index_candidate.exists():
                    main_md_candidates = [index_candidate]

        if not main_md_candidates:
            print(f"⚠️ [{bundle_dir.name}] No primary markdown file found.")
            return False

        main_md_path = main_md_candidates[0]

        # 2. Read existing content
        try:
            content = main_md_path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"❌ [{bundle_dir.name}] Failed to read {main_md_path.name}: {exc}")
            self.stats["errors"] += 1
            return False

        # 3. Separate existing Frontmatter from Body
        existing_fm: Dict[str, Any] = {}
        body_text = content
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    existing_fm = yaml.safe_load(parts[1]) or {}
                    body_text = parts[2].lstrip("\r\n")
                except Exception as exc:
                    print(f"⚠️ [{bundle_dir.name}] Warning reading existing frontmatter: {exc}")

        # 4. Lookup canonical metadata from registry
        rel_bundle_path = bundle_dir.relative_to(self.root_dir).as_posix()
        reg_entry = (
            self.registry_map.get(bundle_dir.name)
            or self.registry_map.get(rel_bundle_path)
            or self.registry_map.get(existing_fm.get("id", ""))
            or {}
        )

        # 5. Extract metadata fields with fallback hierarchy
        doc_id = (
            reg_entry.get("id")
            or existing_fm.get("id")
            or existing_fm.get("doc_id")
            or bundle_dir.name
        )
        doc_number = (
            reg_entry.get("document_number")
            or existing_fm.get("document_number")
            or "Đang cập nhật"
        )
        doc_type = (
            reg_entry.get("type")
            or existing_fm.get("type")
            or existing_fm.get("document_type")
            or ("QCVN" if "qcvn" in category else "TCVN" if "tcvn" in category else "Luật" if "luat" in bundle_dir.name else "Nghị định")
        )
        title = (
            reg_entry.get("title")
            or existing_fm.get("title")
            or f"{doc_type} {doc_number}"
        )
        issued_by = (
            reg_entry.get("issued_by")
            or existing_fm.get("issued_by")
            or ("Quốc hội" if doc_type == "Luật" else "Chính phủ" if doc_type == "Nghị định" else "Bộ Xây dựng")
        )
        signer = reg_entry.get("signer") or existing_fm.get("signer") or ""
        issued_date = str(reg_entry.get("issued_date") or existing_fm.get("issued_date") or "2026-01-01")
        effective_date = str(reg_entry.get("effective_date") or existing_fm.get("effective_date") or "2026-07-01")
        status = reg_entry.get("status") or existing_fm.get("status") or "active"

        # 6. Artifacts Inspection
        artifacts: Dict[str, Any] = {}
        if (bundle_dir / "templates").exists():
            artifacts["templates_dir"] = "./templates/"
        if (bundle_dir / "annexes").exists():
            artifacts["annexes_dir"] = "./annexes/"
        if (bundle_dir / "tables").exists():
            artifacts["tables_dir"] = "./tables/"
            if (bundle_dir / "tables" / "tables_catalog.json").exists():
                artifacts["tables_catalog"] = "./tables/tables_catalog.json"
        if (bundle_dir / "formulas").exists():
            artifacts["formulas_dir"] = "./formulas/"
        if (bundle_dir / "qa_benchmark.json").exists():
            artifacts["benchmark_file"] = "./qa_benchmark.json"

        # 7. PDF Anchor Metadata
        pdf_anchor_raw = reg_entry.get("pdf_path") or existing_fm.get("pdf_anchor")
        pdf_sha_val = reg_entry.get("pdf_sha256") or ""
        cong_bao_val = reg_entry.get("cong_bao_number") or ""

        pdf_anchor_dict: Dict[str, Any] = {}
        if isinstance(pdf_anchor_raw, dict):
            pdf_anchor_dict = pdf_anchor_raw
        elif isinstance(pdf_anchor_raw, str) and pdf_anchor_raw:
            rel_pdf = Path(pdf_anchor_raw).name
            pdf_anchor_dict["path"] = f"./{rel_pdf}" if not pdf_anchor_raw.startswith(".") else pdf_anchor_raw
            if pdf_sha_val:
                pdf_anchor_dict["sha256"] = pdf_sha_val
            if cong_bao_val:
                pdf_anchor_dict["cong_bao_number"] = cong_bao_val

        # 8. Relations handling
        raw_relations = reg_entry.get("relations") or existing_fm.get("relations") or existing_fm.get("legal_basis")
        relations_list = self._normalize_relations(raw_relations)

        # 9. Assemble Google OKF Core Spec
        okf_type = self._determine_okf_type(category, doc_type)
        resource_rel = main_md_path.relative_to(self.root_dir).as_posix()
        tags = self._build_tags(title, doc_type, category)
        description = existing_fm.get("description") or f"Tài liệu {doc_type} quy định chính quy trong hệ thống tri thức xây dựng CCBA."

        # Construct final YAML structure (ordered)
        new_frontmatter_dict: Dict[str, Any] = {
            # TẦNG 1: GOOGLE OKF CORE SPECIFICATION
            "okf_version": "2.2",
            "type": okf_type,
            "title": title,
            "description": description,
            "tags": tags,
            "timestamp": "2026-08-25T00:00:00Z",
            "resource": resource_rel,
            
            # TẦNG 2: CCBA LEGAL & TECHNICAL GRAPH EXTENSIONS
            "id": doc_id,
            "doc_id": doc_id,
            "document_number": doc_number,
            "document_type": doc_type,
            "issued_by": issued_by,
            "signer": signer,
            "issued_date": issued_date,
            "effective_date": effective_date,
            "status": status,
        }

        if pdf_anchor_dict:
            new_frontmatter_dict["pdf_anchor"] = pdf_anchor_dict
        else:
            new_frontmatter_dict["pdf_anchor"] = f"./{doc_id}.pdf"

        if relations_list:
            new_frontmatter_dict["relations"] = relations_list
        if artifacts:
            new_frontmatter_dict["artifacts"] = artifacts
        if "bim_constraints" in existing_fm:
            new_frontmatter_dict["bim_constraints"] = existing_fm["bim_constraints"]

        # Dump YAML with clean formatting
        yaml_str = yaml.dump(
            new_frontmatter_dict,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )

        # Assemble new file content
        new_file_content = f"---\n{yaml_str}---\n\n{body_text}"

        # Write back to file
        try:
            main_md_path.write_text(new_file_content, encoding="utf-8")
            self.stats["migrated"] += 1
            print(f"✨ [{bundle_dir.name}] Migrated Frontmatter -> {main_md_path.name}")
            return True
        except Exception as exc:
            print(f"❌ [{bundle_dir.name}] Failed to write {main_md_path.name}: {exc}")
            self.stats["errors"] += 1
            return False

    def run(self) -> None:
        """Run migration across all categories in legal_docs/."""
        self.load_registry()
        
        categories = ["01_vbpl", "02_qcvn", "03_tcvn", "04_appendices"]
        for cat in categories:
            cat_dir = self.legal_docs_dir / cat
            if not cat_dir.exists():
                continue
            
            print(f"\n📂 Scanning category [{cat}]...")
            for item in sorted(cat_dir.iterdir()):
                if item.is_dir():
                    self.migrate_bundle(item, cat)

        print("\n" + "=" * 60)
        print(f"🎉 MIGRATION COMPLETE:")
        print(f"   Scanned Bundles : {self.stats['scanned']}")
        print(f"   Migrated Files  : {self.stats['migrated']}")
        print(f"   Errors Count    : {self.stats['errors']}")
        print("=" * 60)


if __name__ == "__main__":
    root_path = Path(__file__).resolve().parent.parent
    migrator = OKFSchemaMigrator(root_path)
    migrator.run()
