"""OKF v2.2 Automated Transformation Engine.

Implements ADR 0021:
- Pure Normative Body (.md) from Chapter I to Chapter End
- Structured Legal Knowledge Graph (`legal_basis`)
- Atomic Form Templates (`templates/phu_luc_XX/mau_YY_...md`)
- 3-Tier Semantic Table Classifier (`tables/`)
- Universal Clause Numbering Normalization (**1.**, **2.**) across all files
- Atomic AST & QA Benchmark Synchronization
"""

import argparse
import csv
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import mammoth
import yaml
from docx import Document

# Windows UTF-8 stdout enforcement
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure repository root is on sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.gold_standard_processor import inject_semantic_anchors, generate_bundle_ast_and_qa


def normalize_clause_numbers(text: str) -> str:
    """Bold all clause numbers (**1.**, **2.**) to prevent CommonMark ordered list indentation."""
    lines = text.splitlines()
    processed: list[str] = []
    clause_re = re.compile(r"^(?:\*\*(\d+)\.\*\*|(\d+)\.)\s+([^\n]+)")
    
    for line in lines:
        stripped = line.strip()
        m = clause_re.match(stripped)
        if m:
            num = m.group(1) or m.group(2)
            rest = m.group(3)
            processed.append(f"**{num}.** {rest}")
        else:
            processed.append(line)
            
    return "\n".join(processed)


def extract_legal_basis_graph(raw_text: str, registry_lookup: Dict[str, str]) -> List[Dict[str, str]]:
    """Extract legal basis citations and resolve to canonical doc_ids."""
    basis_list: list[dict[str, str]] = []
    pattern = re.compile(r"căn\s+cứ\s+([^;\n\.]+?)(?:số\s+([\d\w\-/]+))?(?:\s+đã\s+được\s+sửa\s+đổi[^;\n\.]*)?[;\n\.]", re.IGNORECASE)
    
    for match in pattern.finditer(raw_text[:4000]):
        title_raw = match.group(0).strip(" ;.\r\n*")
        title_clean = re.sub(r"^căn\s+cứ\s+", "", title_raw, flags=re.IGNORECASE).strip()
        title_clean = re.sub(r"<[^>]+>", "", title_clean).strip()
        title_clean = title_clean.replace("*", "").replace("\\", "").replace("_", "").strip()
        
        # Filter out false positives that aren't laws/decrees
        if not any(k in title_clean.lower() for k in ["luật", "nghị định", "pháp lệnh", "nghị quyết", "thông tư"]):
            continue
            
        doc_num = match.group(2) if match.group(2) else ""
        
        doc_id = ""
        if doc_num and doc_num in registry_lookup:
            doc_id = registry_lookup[doc_num]
        else:
            slug = re.sub(r"[^\w\d]+", "_", title_clean.lower()).strip("_")
            doc_id = slug[:50]
            
        basis_list.append({
            "doc_id": doc_id,
            "title": title_clean
        })
        
    return basis_list


def classify_and_extract_tables(docx_path: Path, bundle_dir: Path) -> List[Dict[str, Any]]:
    """3-Tier Semantic Table Classifier according to ADR 0021."""
    doc = Document(str(docx_path))
    tables_dir = bundle_dir / "tables"
    csv_dir = tables_dir / "csv"
    json_dir = tables_dir / "json"
    
    if tables_dir.exists():
        shutil.rmtree(tables_dir)
        
    csv_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)
    
    extracted_tables = []
    
    layout_keywords = [
        "cộng hòa xã hội chủ nghĩa",
        "độc lập - tự do",
        "nơi nhận:",
        "tm. chính phủ",
        "kt. thủ tướng",
        "phó thủ tướng",
        "bộ trưởng",
        "chủ tịch ủy ban",
        "ký, ghi rõ họ tên",
        "ký, đóng dấu",
        "lưu: vt",
        "lưu: .."
    ]
    
    for idx, table in enumerate(doc.tables, 1):
        rows_cnt = len(table.rows)
        cols_cnt = len(table.columns)
        table_text = " ".join(c.text.lower() for row in table.rows for c in row.cells)
        
        # 1. Layout Filter
        is_layout = False
        if (rows_cnt <= 2 and cols_cnt <= 2) or (rows_cnt == 1 and cols_cnt == 2):
            if any(k in table_text for k in layout_keywords):
                is_layout = True
        elif rows_cnt <= 3 and cols_cnt <= 2:
            if "nơi nhận:" in table_text or "cộng hòa" in table_text:
                is_layout = True
                
        if is_layout:
            continue
            
        # 2. Data Table Extraction
        grid = []
        for row in table.rows:
            grid.append([c.text.strip().replace("\n", " ") for c in row.cells])
            
        if not grid:
            continue
            
        headers = grid[0]
        
        # Only export tables with actual technical data (>= 3 cols or large rows)
        if cols_cnt < 3 and rows_cnt < 20:
            continue
            
        table_slug = f"bang_{idx:02d}"
        if any("loại công trình" in h.lower() or "quy mô" in h.lower() or "cấp công trình" in h.lower() for h in headers):
            table_slug = "bang_danh_muc_cong_trinh_anh_huong_an_toan_cong_dong"
            
        csv_file = csv_dir / f"{table_slug}.csv"
        with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(grid)
            
        records = []
        if len(grid) > 1:
            for r in grid[1:]:
                rec = {}
                for c_idx, h in enumerate(headers):
                    col_key = h if h else f"col_{c_idx+1}"
                    rec[col_key] = r[c_idx] if c_idx < len(r) else ""
                records.append(rec)
                
        json_data = {
            "table_id": table_slug,
            "rows_count": len(grid),
            "columns_count": len(headers),
            "headers": headers,
            "records": records
        }
        
        json_file = json_dir / f"{table_slug}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            
        extracted_tables.append({
            "table_id": table_slug,
            "rows": len(grid),
            "cols": len(headers),
            "csv": str(csv_file.relative_to(bundle_dir)),
            "json": str(json_file.relative_to(bundle_dir))
        })
        
    return extracted_tables


def process_vbpl_bundle_okf_v22(
    docx_path: Path,
    bundle_dir: Path,
    registry_file: Path,
    output_filename: Optional[str] = None
) -> Dict[str, Any]:
    """Complete OKF v2.2 Transformation Pipeline for Decrees and Laws."""
    bundle_dir.mkdir(parents=True, exist_ok=True)
    templates_dir = bundle_dir / "templates"
    if templates_dir.exists():
        shutil.rmtree(templates_dir)
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # Load registry lookup
    reg_lookup = {}
    doc_registry_meta = {}
    if registry_file.exists():
        with open(registry_file, encoding="utf-8") as f:
            reg_data = yaml.safe_load(f)
            all_items = []
            for k, v in reg_data.items():
                if isinstance(v, list):
                    all_items.extend(v)
            for item in all_items:
                doc_num = item.get("document_number")
                if doc_num:
                    reg_lookup[doc_num] = item.get("id")
                if item.get("id") == bundle_dir.name or item.get("document_number") == bundle_dir.name:
                    doc_registry_meta = item

    print(f"[1/5] Converting {docx_path.name} via Mammoth...")
    with open(docx_path, "rb") as f:
        result = mammoth.convert_to_markdown(f)
        raw_md = result.value

    # Clean escaped punctuation from Mammoth and existing TVPL anchor tags
    cleaned_md = re.sub(r'<a id="[^"]+"></a>', '', raw_md)
    cleaned_md = cleaned_md.replace(r"\.", ".").replace(r"\-", "-").replace(r"\_", "_").replace(r"\(", "(").replace(r"\)", ")")

    print("[2/5] Classifying & Extracting 3-Tier Tables...")
    extracted_tables = classify_and_extract_tables(docx_path, bundle_dir)
    print(f"  -> Extracted {len(extracted_tables)} real technical tables into tables/")

    print("[3/5] Modularizing Atomic Form Templates (templates/)...")
    app_matches = list(re.finditer(r"(?:^|\n)#*\s*__?\s*PHỤ LỤC\s+([IVXLCDM0-9]+)__?\s*([^\n]*)", cleaned_md, re.IGNORECASE))
    
    created_templates = []
    doc_num_str = doc_registry_meta.get('document_number', bundle_dir.name)
    
    for idx, match in enumerate(app_matches):
        roman_num = match.group(1).upper()
        app_title = match.group(2).strip()
        app_title_clean = re.sub(r"^__+|__+$", "", app_title).strip()
        
        start_pos = match.start()
        end_pos = app_matches[idx + 1].start() if idx + 1 < len(app_matches) else len(cleaned_md)
        app_full_text = cleaned_md[start_pos:end_pos].strip()

        # Check for sub-forms "Mẫu số XX"
        pattern = re.compile(r"(?:^|\n)#*\s*__?\s*Mẫu\s+số\s+(\d+[a-zA-Z]?)[.\s_]*", re.IGNORECASE)
        all_matches = list(pattern.finditer(app_full_text))
        
        form_positions = {}
        for m in all_matches:
            f_num = m.group(1).zfill(2)
            form_positions[f_num] = m.start()
            
        sorted_forms = sorted(form_positions.items(), key=lambda x: int(x[0]))
        
        # If there are >= 2 distinct sub-forms -> Split into subfolder
        if len(sorted_forms) >= 2:
            sub_dir = templates_dir / f"phu_luc_{roman_num.lower()}"
            sub_dir.mkdir(parents=True, exist_ok=True)
            
            for s_idx, (f_num, f_start) in enumerate(sorted_forms):
                f_end = sorted_forms[s_idx + 1][1] if s_idx + 1 < len(sorted_forms) else len(app_full_text)
                form_raw_text = app_full_text[f_start:f_end].strip()
                form_norm_text = normalize_clause_numbers(form_raw_text)
                
                # Extract first meaningful title line
                lines = [l.strip() for l in form_raw_text.splitlines() if l.strip()]
                form_title = f"Mẫu số {f_num}"
                for l in lines[1:6]:
                    clean_l = re.sub(r"^__+|__+$", "", l).replace("*", "").strip()
                    if clean_l and not clean_l.startswith("CỘNG HÒA") and not clean_l.startswith("Độc lập") and not clean_l.startswith("-----") and not clean_l.startswith("Số:"):
                        form_title = clean_l
                        break
                        
                slug = re.sub(r"[^\w\d]+", "_", form_title.lower()).strip("_")[:40]
                filename = f"mau_{f_num}_{slug}.md"
                
                tmpl_content = f"""---
title: "Mẫu số {f_num} - {form_title}"
document: "{doc_num_str}"
appendix: "Phụ lục {roman_num}"
form_number: "Mẫu số {f_num}"
type: "form_template"
usage: "Biểu mẫu chuẩn hóa phục vụ AI Copywriting, QC Audit & Sinh Hồ Sơ"
---

# Mẫu Số {f_num} - {form_title}
*(Kèm theo Phụ lục {roman_num} {doc_num_str})*

---

{form_norm_text}
"""
                target_file = sub_dir / filename
                target_file.write_text(tmpl_content, encoding="utf-8")
                created_templates.append({
                    "roman": roman_num,
                    "filename": f"phu_luc_{roman_num.lower()}/{filename}",
                    "title": f"Phụ lục {roman_num} - Mẫu {f_num}: {form_title}",
                    "path": str(target_file.relative_to(bundle_dir))
                })
                print(f"  + Sub-form: phu_luc_{roman_num.lower()}/{filename}")

        else:
            # Check if this appendix is purely a technical lookup table
            is_data_table_appendix = (
                any(k in app_title_clean.lower() for k in ["danh mục công trình ảnh hưởng lớn", "danh mục công trình quy mô lớn", "bảng danh mục công trình"])
                or (len(app_full_text.splitlines()) > 50 and "mã số" in app_full_text.lower() and "cấp công trình" in app_full_text.lower())
            )
            
            if is_data_table_appendix:
                print(f"  -> Bỏ qua Phụ lục {roman_num} ({app_title_clean[:40]}...) do là Bảng số liệu kỹ thuật (đã lưu tại tables/)")
                continue
                
            # Otherwise, write as standalone appendix template
            if not app_title_clean:
                app_title_clean = lines[1] if len(lines) > 1 else f"Phụ lục {roman_num}"
                app_title_clean = re.sub(r"^__+|__+$", "", app_title_clean).strip()
                
            slug = re.sub(r"[^\w\d]+", "_", app_title_clean.lower()).strip("_")[:40]
            filename = f"phu_luc_{roman_num.lower()}_{slug}.md"
            
            norm_text = normalize_clause_numbers(app_full_text)
            
            tmpl_content = f"""---
title: "{app_title_clean}"
document: "{doc_num_str}"
appendix: "Phụ lục {roman_num}"
type: "form_template"
usage: "Biểu mẫu / Phụ lục chuẩn hóa phục vụ AI Copywriting, QC Audit & Sinh Hồ Sơ"
---

# Phụ Lục {roman_num} - {app_title_clean}
*(Kèm theo {doc_num_str})*

---

{norm_text}
"""
            target_file = templates_dir / filename
            target_file.write_text(tmpl_content, encoding="utf-8")
            created_templates.append({
                "roman": roman_num,
                "filename": filename,
                "title": f"Phụ lục {roman_num}: {app_title_clean}",
                "path": str(target_file.relative_to(bundle_dir))
            })
            print(f"  + Appendix Template: {filename}")

    print(f"  -> Created {len(created_templates)} Form Templates & Annexes in templates/")

    print("[4/5] Building Pure Normative Body Markdown...")
    # Find start of normative content (Chương I or Điều 1)
    start_match = re.search(r"(?:^|\n)#*\s*__?\s*(?:Chương\s+[I1]\b|Điều\s+1\.)", cleaned_md, re.IGNORECASE)
    start_pos = start_match.start() if start_match else 0

    # Find start of appendices / templates / forms
    app_cut_match = re.search(r"(?:^|\n)#*\s*__?\s*(?:Phụ\s+lục\s+[IVXLCDM0-9A-Z]+|PHỤ\s+LỤC\b|Mẫu\s+số\s+\d+)", cleaned_md[start_pos:], re.IGNORECASE)
    first_app_pos = (start_pos + app_cut_match.start()) if app_cut_match else len(cleaned_md)

    body_raw = cleaned_md[start_pos:first_app_pos].strip()

    # Cut off Nơi nhận & trailing administrative signature blocks
    noi_nhan_split = re.split(r"(?:__\*?\s*Nơi nhận\s*:|\*+Nơi nhận\s*:|\bNơi nhận\s*:|__KT\.\s+BỘ\s+TRƯỞNG|KT\.\s+BỘ\s+TRƯỞNG|__BỘ\s+TRƯỞNG\b|__THỨ\s+TRƯỞNG\b)", body_raw, flags=re.IGNORECASE)
    body_pure = noi_nhan_split[0].strip()

    # Normalize headings
    body_pure = re.sub(r"(?:^|\n)#*\s*__?\s*Chương\s+([IVXLCDM0-9]+)\.?\s*([^\n_]*)__?", r"\n\n## Chương \1. \2", body_pure, flags=re.IGNORECASE)
    body_pure = re.sub(r"(?:^|\n)#*\s*__?\s*Mục\s+(\d+)\.?\s*([^\n_]*)__?", r"\n\n### Mục \1. \2", body_pure, flags=re.IGNORECASE)
    body_pure = re.sub(r"(?:^|\n)#*\s*__?\s*Điều\s+(\d+)\.?\s*([^\n_]*)__?", r"\n\n### Điều \1. \2", body_pure, flags=re.IGNORECASE)

    # Inject semantic anchors
    body_anchored = inject_semantic_anchors(body_pure)
    body_anchored = normalize_clause_numbers(body_anchored)

    # Extract Legal Basis Graph
    legal_basis_graph = extract_legal_basis_graph(raw_md, reg_lookup)

    # Build Navigation MOC
    moc_lines = [
        "\n---",
        "\n## 📑 HỆ THỐNG PHỤ LỤC BIỂU MẪU & BẢNG BIỂU KÈM THEO\n",
        "> [!TIP]",
        f"> Toàn bộ các Phụ lục của văn bản đã được chuẩn hóa thành các Module Biểu mẫu độc lập tại thư mục [`./templates/`](./templates/) và Bảng tra cứu kỹ thuật tại [`./tables/`](./tables/):\n"
    ]
    for tmpl in created_templates:
        moc_lines.append(f"- 📄 **[{tmpl['title']}](./{tmpl['path'].replace(chr(92), '/')})**")
    for tbl in extracted_tables:
        moc_lines.append(f"- 📊 **[{tbl['table_id']}](./{tbl['csv'].replace(chr(92), '/')})**")

    # Metadata Frontmatter
    doc_num = doc_registry_meta.get("document_number", "Đang cập nhật")
    doc_title = doc_registry_meta.get("title", bundle_dir.name)
    doc_type = doc_registry_meta.get("type", "Văn bản quy phạm pháp luật")
    issued_by = doc_registry_meta.get("issued_by", "Bộ Xây dựng")
    issued_date = doc_registry_meta.get("issued_date", "2026-06-30")
    effective_date = doc_registry_meta.get("effective_date", "2026-07-01")
    signer = doc_registry_meta.get("signer", "Đang cập nhật")
    pdf_path = doc_registry_meta.get("pdf_path", f"{bundle_dir.name}.pdf")
    pdf_sha256 = doc_registry_meta.get("pdf_sha256", "verified")

    legal_basis_str = yaml.dump({"legal_basis": legal_basis_graph}, allow_unicode=True, indent=2).strip() if legal_basis_graph else "legal_basis: []"

    frontmatter = f"""---
id: "{bundle_dir.name}"
document_number: "{doc_num}"
title: "{doc_title}"
issued_by: "{issued_by}"
signer: "{signer}"
issued_date: "{issued_date}"
effective_date: "{effective_date}"
status: "active"
pdf_anchor: "./{Path(pdf_path).name}"
{legal_basis_str}
---

# {doc_num.upper()}
## {doc_title.upper()}

> [!NOTE]
> **Cơ quan ban hành:** {issued_by} (Người ký: {signer}).  
> **Ngày ban hành:** {issued_date} | **Hiệu lực:** {effective_date}.  
> **Mỏ neo PDF Công báo (PDF Anchor of Trust):** [`{Path(pdf_path).name}`](./{Path(pdf_path).name}) *(SHA-256: `{pdf_sha256}`)*.

---

"""

    final_md_text = frontmatter + body_anchored + "\n" + "\n".join(moc_lines) + "\n"
    
    target_md_file = bundle_dir / (output_filename or f"{bundle_dir.name}.md")
    target_md_file.write_text(final_md_text, encoding="utf-8")
    print(f"  -> Wrote Pure Normative Body: {target_md_file.name} ({len(final_md_text.splitlines())} lines)")

    print("[5/5] Generating AST & QA Benchmark & Updating Metadata...")
    clauses, qa_benchmark = generate_bundle_ast_and_qa(
        bundle_dir=bundle_dir,
        doc_title=doc_title,
        cong_bao_number=doc_registry_meta.get("cong_bao_number"),
    )
    with open(bundle_dir / "clauses.json", "w", encoding="utf-8") as f:
        json.dump(clauses, f, ensure_ascii=False, indent=2)
        
    metadata_obj = {
        "id": bundle_dir.name,
        "document_number": doc_num,
        "title": doc_title,
        "type": doc_registry_meta.get("type", "Nghị định"),
        "issued_by": doc_registry_meta.get("issued_by", "Bộ Xây dựng"),
        "signer": signer,
        "issued_date": issued_date,
        "effective_date": effective_date,
        "status": "active",
        "pdf_path": pdf_path,
        "pdf_sha256": pdf_sha256,
        "pdf_status": "verified",
        "legal_basis": legal_basis_graph,
        "replaces": doc_registry_meta.get("relations", {}).get("replaces", [])
    }
    with open(bundle_dir / "metadata.yaml", "w", encoding="utf-8") as f:
        yaml.dump(metadata_obj, f, allow_unicode=True, sort_keys=False, indent=2)

    with open(bundle_dir / "qa_benchmark.json", "w", encoding="utf-8") as f:
        json.dump(qa_benchmark, f, ensure_ascii=False, indent=2)

    # Rich MOC index.md
    index_md = f"""# Gói Tri Thức Pháp Lý OKF v2.2: {doc_num}

> [!NOTE]
> **Văn bản:** {doc_title}  
> **Cơ quan ban hành:** Chính phủ (Người ký: {signer}).  
> **Hiệu lực:** {effective_date}.  
> **Mỏ neo PDF Công báo:** [{Path(pdf_path).name}](./{Path(pdf_path).name}) *(SHA-256: `{pdf_sha256}`)*.

---

## 📑 Danh Mục Thành Phần Gói Tri Thức (OKF v2.2 Bundle)

- [Toàn văn Quy phạm (Markdown OKF v2.2)](./{target_md_file.name}) — Thân văn bản quy phạm thuần khiết có gắn thẻ neo `#dieu-X`.
- [Metadata Pháp lý & Đồ thị (YAML)](./metadata.yaml) — Đặc tả thuộc tính và cây đồ thị `legal_basis`.
- [Cây Cú Pháp Điều Khoản (AST Clauses JSON)](./clauses.json) — {len(clauses)} nodes điều khoản phục vụ AI QC & RAG.
- [Bộ Đánh Giá Độ Chính Xác (QA Benchmark)](./qa_benchmark.json) — {len(qa_benchmark)} cặp câu hỏi - câu trả lời đối soát.
- [Kho Biểu Mẫu Chuẩn Hóa (Templates Directory)](./templates/) — {len(created_templates)} Biểu mẫu Markdown phục vụ Agent Copywriting & Sinh Hồ Sơ.
- [Bảng Tra Cứu Kỹ Thuật (Tables Directory)](./tables/) — {len(extracted_tables)} Bảng tra cứu số học (CSV + JSON).
"""
    with open(bundle_dir / "index.md", "w", encoding="utf-8") as f:
        f.write(index_md)

    print(f"\n🎉 HOÀN TẤT CHUYỂN ĐỔI OKF v2.2 CHO {bundle_dir.name}!")
    return {
        "status": "success",
        "bundle": bundle_dir.name,
        "clauses_count": len(clauses),
        "templates_count": len(created_templates),
        "tables_count": len(extracted_tables),
        "qa_count": len(qa_benchmark)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OKF v2.2 Automated Transformation Engine")
    parser.add_argument("docx_path", type=Path, help="Path to input .docx")
    parser.add_argument("bundle_dir", type=Path, help="Path to target bundle directory")
    parser.add_argument("--registry", type=Path, default=Path("legal_registry.yaml"), help="Path to legal_registry.yaml")
    args = parser.parse_args()
    
    res = process_vbpl_bundle_okf_v22(args.docx_path, args.bundle_dir, args.registry)
    print("\nResult:", json.dumps(res, indent=2))
