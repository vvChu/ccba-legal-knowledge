"""CCBA Master Docx to Gold Standard OKF Engine.

Performs 100% clean end-to-end processing of QCVN 06:2022/BXD from official .docx:
1. Cleans old generated target files.
2. Converts .docx using Mammoth + python-docx.
3. Purges duplicate residual paragraph text blocks (e.g. after Bảng 11).
4. Reconstructs all 60 2D GFM Markdown Pipe Tables with rowspan/colspan unmerging.
5. Packs Gold Standard OKF v0.2 Bundle with descriptive table file slugs
   (e.g., bang_01_gioi_han_chiu_lua_bo_phan_ngan_chay.json).
"""

import csv
import json
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from docx import Document
import mammoth
from scripts.gold_standard_processor import process_okf_bundle

sys.stdout.reconfigure(encoding="utf-8")

def vietnamese_to_ascii(text: str) -> str:
    """Convert Vietnamese accented text to unaccented ASCII."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "D")
    return text

def make_descriptive_table_slug(table_num: str, title: str = "") -> str:
    """Generate clean descriptive slug for table filenames."""
    num_str = table_num.lower().replace(".", "_")
    if re.match(r"^\d+$", num_str):
        num_str = f"{int(num_str):02d}"

    base_prefix = f"bang_{num_str}"
    if not title:
        return base_prefix

    title_clean = re.sub(r"^(?:Bảng|Table)\s+[A-Z0-9]+(?:\.[0-9]+)?\s*[-–:]\s*", "", title, flags=re.IGNORECASE).strip()
    ascii_title = vietnamese_to_ascii(title_clean).lower()
    words = re.findall(r"\b[a-z0-9]+\b", ascii_title)

    stopwords = {"va", "cua", "cho", "cac", "thuc", "hien", "tuong", "ung", "voi", "chung", "nhung", "theo", "đoi", "doi"}
    filtered = [w for w in words if w not in stopwords][:5]

    if filtered:
        return f"{base_prefix}_{'_'.join(filtered)}"
    return base_prefix

def clean_duplicate_paragraph_tables(md_text: str) -> str:
    """Purge unformatted duplicate paragraph text blocks that mimic table contents."""
    p11_duplicate = re.compile(
        r"__3\.\s*Phòng câu lạc bộ[^\n]*\n\s*1\s+Nhà ở[^\n]*\n.*?2,5\s*\n",
        re.DOTALL | re.IGNORECASE,
    )
    md_text = p11_duplicate.sub("", md_text)

    p_dup_general = re.compile(
        r"\n1\s+Nhà ở,\s*nhà chung cư\s*\n.*?5\s+Nhà hành chính - phụ trợ[^\n]*\n.*?2,5\s*\n",
        re.DOTALL | re.IGNORECASE,
    )
    md_text = p_dup_general.sub("\n", md_text)
    return md_text

def extract_docx_tables_map(docx_path: Path) -> dict[str, dict]:
    """Extract clean 2D table grid from docx file via python-docx with unmerged cells."""
    doc = Document(docx_path)
    table_data_map: dict[str, dict] = {}

    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    title_pattern = re.compile(
        r"^(?:Bảng|Table)\s+([A-Z0-9]+(?:\.[0-9]+)?)\s*[-–:]\s*(.+)$",
        re.IGNORECASE,
    )

    table_titles: list[dict] = []
    for p_idx, text in enumerate(paragraphs):
        match = title_pattern.match(text)
        if match:
            table_titles.append({
                "num": match.group(1),
                "title": f"Bảng {match.group(1)} - {match.group(2).strip()}",
                "p_idx": p_idx,
            })

    for idx, table in enumerate(doc.tables):
        table_info = table_titles[idx] if idx < len(table_titles) else {
            "num": str(idx + 1),
            "title": f"Bảng {idx + 1}",
        }

        num_str = table_info["num"]
        table_title_full = table_info["title"]
        slug = make_descriptive_table_slug(num_str, table_title_full)

        grid: list[list[str]] = []
        footnotes: list[str] = []

        for row in table.rows:
            row_cells = [c.text.replace("\n", " ").strip() for c in row.cells]

            if len(set(row_cells)) == 1 and (row_cells[0].startswith("CHÚ THÍCH") or re.match(r"^\d+\)\s+", row_cells[0]) or len(row_cells[0]) > 80):
                if row_cells[0] and row_cells[0] not in footnotes:
                    footnotes.append(row_cells[0])
                continue

            grid.append(row_cells)

        if not grid:
            continue

        headers = grid[0]
        rows = grid[1:]

        clean_rows = []
        for r in rows:
            clean_r = [re.sub(r"\s+", " ", cell).strip() for cell in r]
            if any(clean_r):
                clean_rows.append(clean_r)

        table_data_map[slug] = {
            "num": num_str,
            "title": table_title_full,
            "headers": headers,
            "rows": clean_rows,
            "footnotes": footnotes,
            "cols_count": len(headers),
        }

    return table_data_map

def save_descriptive_table_exports(table_map: dict[str, dict], target_bundle_dir: Path):
    """Save structured table JSONs and CSVs into tables/json/ and tables/csv/ with descriptive slugs."""
    tables_dir = target_bundle_dir / "tables"
    json_dir = tables_dir / "json"
    csv_dir = tables_dir / "csv"

    # Clean old table directory
    if tables_dir.exists():
        shutil.rmtree(tables_dir)

    json_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)

    for slug, tdata in table_map.items():
        headers = tdata["headers"]
        rows_matrix = tdata["rows"]
        footnotes = tdata["footnotes"]

        rows_dict_list = []
        for r in rows_matrix:
            row_dict = {headers[c_idx]: r[c_idx] if c_idx < len(r) else "" for c_idx in range(len(headers))}
            rows_dict_list.append(row_dict)

        table_json_dict = {
            "table_id": slug,
            "title": tdata["title"],
            "headers": headers,
            "rows": rows_dict_list,
            "total_rows": len(rows_dict_list),
            "footnotes": footnotes,
        }

        # Save JSON
        json_file = json_dir / f"{slug}.json"
        json_file.write_text(json.dumps(table_json_dict, ensure_ascii=False, indent=2), encoding="utf-8")

        # Save CSV
        csv_file = csv_dir / f"{slug}.csv"
        with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if headers:
                writer.writerow(headers)
            for r in rows_matrix:
                writer.writerow(r)

def master_rebuild_from_docx(docx_path: Path, target_bundle_dir: Path) -> dict:
    """Master rebuild pipeline from .docx to OKF Bundle with descriptive file slugs."""
    if not docx_path.exists():
        raise FileNotFoundError(f"Input file not found: {docx_path}")

    # Step 1: Wipe old target directory
    print(f"[1/5] Wiping old target directory: {target_bundle_dir}...")
    if target_bundle_dir.exists():
        shutil.rmtree(target_bundle_dir)
    target_bundle_dir.mkdir(parents=True, exist_ok=True)

    for f in docx_path.parent.glob("*_from_docx.md"):
        f.unlink()

    # Step 2: Convert .docx to raw markdown via Mammoth
    print(f"[2/5] Converting {docx_path.name} to Markdown via Mammoth...")
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
        raw_md = result.value

    # Step 3: Purge duplicate paragraph tables & normalize headings
    print("[3/5] Purging duplicate text blocks & normalizing headings...")
    cleaned_md = clean_duplicate_paragraph_tables(raw_md)

    cleaned_md = cleaned_md.replace(r"\.", ".").replace(r"\-", "-").replace(r"\(", "(").replace(r"\)", ")")
    cleaned_md = re.sub(r'<a id="[^"]+"></a>\s*__(\d+(?:\.\d+)*)\.?\s*([^_]+)__', r"### \1 \2", cleaned_md)
    cleaned_md = re.sub(r"__(\d+(?:\.\d+)*)\.?\s*([^_]+)__", r"### \1 \2", cleaned_md)
    cleaned_md = re.sub(r"__Bảng\s+([A-Z0-9]+(?:\.[0-9]+)?)\s*[-–:]\s*([^_]+)__", r"### Bảng \1 - \2", cleaned_md)
    cleaned_md = re.sub(r"(###\s*)+", "### ", cleaned_md)

    target_md_path = target_bundle_dir / "qcvn_06_2022_bxd.md"
    target_md_path.write_text(cleaned_md, encoding="utf-8")

    # Step 4: Reconstruct 2D GFM Pipe Tables & export descriptive table JSON/CSV files
    print("[4/5] Reconstructing 2D GFM Pipe Tables & exporting descriptive table slugs...")
    table_map = extract_docx_tables_map(docx_path)
    print(f"  [Matrix Extractor] Extracted {len(table_map)} tables from .docx matrix")

    save_descriptive_table_exports(table_map, target_bundle_dir)

    md_content = target_md_path.read_text(encoding="utf-8")
    replaced_count = 0

    for slug, tdata in table_map.items():
        tnum = tdata["num"]
        ttitle = tdata["title"]
        headers = tdata["headers"]
        rows = tdata["rows"]
        footnotes = tdata["footnotes"]
        cols_count = tdata["cols_count"]

        tanchor = f"bang-{tnum.lower().replace('.', '-')}"

        md_lines = [
            f'<a id="{tanchor}"></a>',
            f"### {ttitle}\n",
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * cols_count) + " |",
        ]
        for r in rows:
            if len(r) < cols_count:
                r = r + [""] * (cols_count - len(r))
            md_lines.append("| " + " | ".join(r[:cols_count]) + " |")

        if footnotes:
            md_lines.append("\n" + "\n".join(f"_{fn}_" for fn in footnotes))

        md_lines.append("\n")
        new_table_block = "\n".join(md_lines)

        pattern = re.compile(
            rf"(?:<a id=\"[^\"]+\"></a>\n)?(?:###|\*\*|#)*\s*Bảng\s+{re.escape(tnum)}\s*[-–:].*?(?=\n<a id=\"muc-|\n### |\n# |\n(?:#|\*)*\s*Bảng|\Z)",
            re.DOTALL | re.IGNORECASE,
        )

        if pattern.search(md_content):
            md_content = pattern.sub(new_table_block, md_content, count=1)
            replaced_count += 1

    target_md_path.write_text(md_content, encoding="utf-8")
    print(f"  [Table Reconstructor] Replaced {replaced_count} tables with 100% 2D Pipe Tables")

    # Step 5: Pack Gold Standard OKF v0.2 Bundle
    print("[5/5] Packing Gold Standard OKF v0.2 Bundle...")
    okf_result = process_okf_bundle(target_bundle_dir)
    return okf_result

if __name__ == "__main__":
    docx_file = Path(".md/extracted_docs/qcvn_06_2022_bxd/qcvn_06_2022_bxd.docx")
    bundle_dir = Path("legal_docs/02_qcvn/qcvn_06_2022_bxd")
    res = master_rebuild_from_docx(docx_file, bundle_dir)
    print("\n[DESCRIPTIVE TABLE SLUGS REBUILD COMPLETE]:", res)
