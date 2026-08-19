"""Table Extractor Engine with Descriptive File Slugs.

Parses HTML/Markdown/Docx table blocks and exports structured JSON and CSV files
with highly descriptive filenames (e.g., bang_01_gioi_han_chiu_lua_bo_phan_ngan_chay.json).
"""

import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

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

def extract_table_from_text_block(table_title: str, block_lines: list[str]) -> dict | None:
    """Extract 2D structured table dictionary from raw text lines."""
    num_match = re.search(r"Bảng\s+([A-Z0-9]+(?:\.[0-9]+)?)", table_title, re.IGNORECASE)
    table_num = num_match.group(1) if num_match else "0"

    raw_tokens: list[str] = []
    footnotes: list[str] = []

    for line in block_lines:
        line_str = line.strip()
        clean_str = re.sub(r"<a id=\"[^\"]+\"></a>", "", line_str)
        clean_str = re.sub(r"^[#*\s|]+", "", clean_str).strip(" |")

        if not clean_str or clean_str == "---":
            continue

        if re.match(r"^\d+\)\s+", clean_str) or clean_str.startswith("CHÚ THÍCH"):
            footnotes.append(clean_str)
            continue

        if "\t" in clean_str:
            parts = [p.strip(" |") for p in clean_str.split("\t") if p.strip()]
            raw_tokens.extend(parts)
        else:
            raw_tokens.append(clean_str)

    if len(raw_tokens) < 2:
        return None

    header_end = 1
    for tok_idx, tok in enumerate(raw_tokens[1:], 1):
        if re.match(r"^\d+[\.\)]?\s*", tok) or re.search(r"\b(REI|EI|R|E|P|F\d)\s*\d*", tok):
            header_end = tok_idx
            break

    cols_count = max(1, header_end)
    headers = raw_tokens[:cols_count]
    data_tokens = raw_tokens[cols_count:]

    rows: list[dict] = []
    for chunk_idx in range(0, len(data_tokens), cols_count):
        chunk = data_tokens[chunk_idx : chunk_idx + cols_count]
        if any(chunk):
            if len(chunk) < cols_count:
                chunk.extend([""] * (cols_count - len(chunk)))
            row_dict = {headers[c_idx]: chunk[c_idx] for c_idx in range(cols_count)}
            rows.append(row_dict)

    slug = make_descriptive_table_slug(table_num, table_title)

    return {
        "table_id": slug,
        "title": table_title,
        "headers": headers,
        "rows": rows,
        "total_rows": len(rows),
        "footnotes": footnotes,
    }

def save_table_exports(table_dict: dict, tables_dir: Path) -> tuple[Path, Path]:
    """Save structured table dict into tables/json/ and tables/csv/ with descriptive slug."""
    json_dir = tables_dir / "json"
    csv_dir = tables_dir / "csv"
    json_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)

    slug = table_dict["table_id"]
    json_path = json_dir / f"{slug}.json"
    csv_path = csv_dir / f"{slug}.csv"

    json_path.write_text(json.dumps(table_dict, ensure_ascii=False, indent=2), encoding="utf-8")

    headers = table_dict.get("headers", [])
    rows = table_dict.get("rows", [])
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for r_dict in rows:
            writer.writerow([r_dict.get(h, "") for h in headers])

    return json_path, csv_path

def parse_and_extract_all_tables(target_path: Path, content: str = "") -> tuple[str, list[str]]:
    """Scan target_path or bundle_dir and extract structured tables."""
    if target_path.is_dir():
        bundle_dir = target_path
        tables_dir = bundle_dir / "tables"
        md_files = list(bundle_dir.glob("*.md"))
        if not md_files and not content:
            return "", []
        text = content if content else md_files[0].read_text(encoding="utf-8")
    else:
        md_path = target_path
        tables_dir = md_path.parent / "tables"
        text = content if content else md_path.read_text(encoding="utf-8")

    table_pattern = re.compile(
        r"(?:###|\*\*|#)*\s*(Bảng\s+[A-Z0-9]+(?:\.[0-9]+)?\s*[-–:]\s*[^\n\*\#]+)(.*?)(?=\n<a id=\"muc-|\n### |\n# |\n(?:#|\*)*\s*Bảng|\Z)",
        re.DOTALL | re.IGNORECASE,
    )

    generated_files = []
    for match in table_pattern.finditer(text):
        title = match.group(1).strip()
        body = match.group(2).splitlines()
        tdict = extract_table_from_text_block(title, body)
        if tdict:
            jpath, cpath = save_table_exports(tdict, tables_dir)
            generated_files.extend([str(jpath), str(cpath)])

    return text, generated_files
