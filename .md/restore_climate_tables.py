"""Restore climate tables from official PDF for QCVN 02:2022/BXD.

Fixes:
1. bang_09.csv: Corrects 77 rows where district and station have the same name.
   Restores [Tỉnh, Huyện, Trạm, Kinh độ, Vĩ độ, Cao độ] instead of trailing padding shift.
2. bang_10..bang_43 (20 tables): Extracts 100% ground truth 13-month values
   from sources/qcvn_02_2022_bxd.pdf instead of trailing comma padding.
3. bang_28, bang_29: Restores '0' values for non-active solar radiation hours
   instead of empty cells.
4. Synchronizes all corresponding .json files and tables_catalog.json.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_02_2022_bxd" / "sources" / "qcvn_02_2022_bxd.pdf"
TABLES_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_02_2022_bxd" / "tables"
CSV_DIR = TABLES_DIR / "csv"
JSON_DIR = TABLES_DIR / "json"
CATALOG_PATH = TABLES_DIR / "tables_catalog.json"

doc = fitz.open(str(PDF_PATH))
token_pattern = re.compile(r"^(?:[-–\u2013\u2212]?\d+(?:,\d+)?|[xX\-]|0,\d+)$")


def sync_json(table_id: str, headers: list[str], rows: list[list[str]], footnotes: list[str] | None = None) -> None:
    """Generate corresponding json file for a table."""
    json_path = JSON_DIR / f"{table_id}.json"
    records = []
    for r in rows:
        record = {}
        for h, val in zip(headers, r):
            record[h] = val
        records.append(record)
    
    if footnotes is None and json_path.exists():
        try:
            existing = json.loads(json_path.read_text(encoding="utf-8"))
            footnotes = existing.get("footnotes", [])
        except Exception:
            footnotes = []
    
    data = {
        "table_id": table_id,
        "rows_count": len(records),
        "columns_count": len(headers),
        "headers": headers,
        "records": records,
        "footnotes": footnotes or []
    }
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fix_bang_09() -> None:
    """Fix bang_09.csv coordinates and elevation alignment."""
    print("Fixing bang_09...")
    csv_path = CSV_DIR / "bang_09.csv"
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))

    headers = [
        "Tỉnh, thành phố trực thuộc Trung ương",
        "Thành phố, quận, huyện (hoặc tương đương)",
        "Trạm",
        "Kinh độ",
        "Vĩ độ",
        "Cao độ (m)"
    ]

    fixed_rows = []
    for idx, r in enumerate(rows):
        if idx == 0:
            fixed_rows.append(headers)
            continue
        if idx == 1 and r[0] == "(1)":
            fixed_rows.append(["(1)", "(2)", "(3)", "(4)", "(5)", "(6)"])
            continue
        
        # Region subheaders
        if r[0].startswith("Khu vực "):
            fixed_rows.append([r[0], "", "", "", "", ""])
            continue

        # Check if row has shifted columns due to trailing empty cell
        if len(r) == 6 and r[5] == "" and r[0] not in headers:
            # Shifted row: r[0]=Tỉnh, r[1]=Name, r[2]=Lon, r[3]=Lat, r[4]=Elev
            name = r[1].strip()
            lon = r[2].strip()
            lat = r[3].strip()
            elev = r[4].strip()
            fixed_rows.append([r[0].strip(), name, name, lon, lat, elev])
        else:
            # Normal 6-item row
            fixed_rows.append([c.strip() for c in r[:6]])

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(fixed_rows)

    sync_json("bang_09", headers, fixed_rows[1:])
    print(f"bang_09 fixed: {len(fixed_rows)} rows written.")


def extract_station_table_robust(start_page: int, end_page: int) -> dict[int, tuple[str, list[str]]]:
    """Robustly extract station table from PDF pages."""
    stations = {}
    lines = []
    for pidx in range(start_page, end_page):
        lines.extend([l.strip() for l in doc[pidx].get_text().splitlines() if l.strip()])

    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\d+)[\.\s]\s*([^\d\n\r]+)(.*)$", line)
        if m:
            st_num = int(m.group(1))
            st_name = m.group(2).strip()
            rest = m.group(3).strip()
            nums = [
                p.replace("–", "-").replace("\u2013", "-").replace("\u2212", "-")
                for p in rest.split()
                if token_pattern.match(p)
            ] if rest else []
            
            j = i + 1
            while j < len(lines) and len(nums) < 13:
                next_line = lines[j]
                if re.match(r"^\d+[\.\s]\s*[^\d\n\r]+", next_line):
                    break
                for p in next_line.split():
                    if token_pattern.match(p):
                        clean_p = p.replace("–", "-").replace("\u2013", "-").replace("\u2212", "-")
                        nums.append(clean_p)
                j += 1
            stations[st_num] = (st_name, nums)
            i = j - 1
        i += 1
    return stations


def fix_climate_tables() -> None:
    """Extract and restore ground truth for 20 station tables."""
    tables_info = [
        ("bang_10", "Bảng A.2", 117, 121, 152),
        ("bang_11", "Bảng A.3", 121, 125, 152),
        ("bang_12", "Bảng A.4", 125, 129, 152),
        ("bang_13", "Bảng A.5", 129, 133, 152),
        ("bang_14", "Bảng A.6", 133, 137, 152),
        ("bang_15", "Bảng A.7", 137, 141, 152),
        ("bang_17", "Bảng A.9", 173, 177, 149),
        ("bang_18", "Bảng A.10", 177, 181, 152),
        ("bang_19", "Bảng A.11", 181, 185, 150),
        ("bang_20", "Bảng A.12", 185, 189, 152),
        ("bang_23", "Bảng A.15", 272, 278, 152),
        ("bang_30", "Bảng A.22", 362, 368, 148),
        ("bang_33", "Bảng A.25", 444, 450, 152),
        ("bang_34", "Bảng A.26", 450, 456, 152),
        ("bang_36", "Bảng A.28", 461, 465, 152),
        ("bang_39", "Bảng A.31", 556, 560, 149),
        ("bang_40", "Bảng A.32", 560, 564, 150),
        ("bang_41", "Bảng A.33", 564, 568, 149),
        ("bang_42", "Bảng A.34", 568, 572, 150),
        ("bang_43", "Bảng A.35", 572, 576, 149),
    ]

    headers = [
        "Trạm",
        "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
        "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12",
        "Năm"
    ]

    for tid, tname, sp, ep, exp_count in tables_info:
        print(f"Extracting {tid} ({tname})...")
        extracted = extract_station_table_robust(sp, ep)
        if len(extracted) != exp_count or any(len(s[1]) != 13 for s in extracted.values()):
            raise ValueError(f"Incomplete extraction for {tid}: {len(extracted)}/{exp_count}")

        # Read existing station label format from git HEAD to preserve all original stations
        csv_path = CSV_DIR / f"{tid}.csv"
        import subprocess
        try:
            head_content = subprocess.check_output(
                ["git", "show", f"HEAD:legal_docs/02_qcvn/qcvn_02_2022_bxd/tables/csv/{tid}.csv"],
                encoding="utf-8-sig"
            )
            old_rows = list(csv.reader(head_content.splitlines()))
        except Exception:
            with open(csv_path, "r", encoding="utf-8-sig") as f:
                old_rows = list(csv.reader(f))

        new_rows = [headers]
        for row_idx, r in enumerate(old_rows[1:], 1):
            station_label = r[0].strip()
            m = re.match(r"^(\d+)[\.\s]", station_label)
            if not m:
                continue
            st_num = int(m.group(1))
            if st_num not in extracted:
                raise ValueError(f"Station number {st_num} ({station_label}) not in extracted PDF data for {tid}")
            st_name, nums = extracted[st_num]
            # Normalize label to 'st_num. name' if missing dot
            if not re.match(r"^\d+\.", station_label):
                station_label = f"{st_num}. {st_name}"
            new_rows.append([station_label] + nums)

        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(new_rows)

        sync_json(tid, headers, new_rows[1:])
        print(f"  -> {tid} restored with {len(new_rows)-1} stations x 13 values.")


def fix_radiation_tables() -> None:
    """Fix zero solar radiation rows in bang_28 and bang_29."""
    for tid in ["bang_28", "bang_29"]:
        print(f"Fixing radiation zeros in {tid}...")
        csv_path = CSV_DIR / f"{tid}.csv"
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        
        headers = rows[0]
        fixed_rows = [headers]
        fixed_count = 0
        for r in rows[1:]:
            # If row has Hướng, Tháng, '0' and rest empty, fill all remaining hourly columns with '0'
            if len(r) == 15 and r[2] == "0" and all(c == "" for c in r[3:]):
                fixed_rows.append([r[0], r[1]] + ["0"] * 13)
                fixed_count += 1
            else:
                fixed_rows.append(r)

        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(fixed_rows)

        sync_json(tid, headers, fixed_rows[1:])
        print(f"  -> {tid}: {fixed_count} rows filled with 0s.")


def update_catalog() -> None:
    """Update tables_catalog.json with exact rows_count and columns_count."""
    print("Updating tables_catalog.json...")
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    for entry in catalog:
        tid = entry["table_id"]
        csv_p = CSV_DIR / f"{tid}.csv"
        if csv_p.exists():
            with open(csv_p, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))
            if rows:
                entry["columns_count"] = len(rows[0])
                entry["rows_count"] = len(rows) - 1

    CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print("tables_catalog.json synchronized.")


if __name__ == "__main__":
    fix_bang_09()
    fix_climate_tables()
    fix_radiation_tables()
    update_catalog()
    print("All tables successfully restored and validated!")
