"""CCBA Structured Footnote Binding Matrix Upgrader.

Implements ADR 0002 for all 64 tables in tables/json/*.json:
1. Parses cell values into structured_cells with numeric_value, unit, condition_refs.
2. Categorizes footnotes into normative_condition, exception, definition.
3. Updates tables_catalog.json with condition metrics.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.stdout.reconfigure(encoding="utf-8")

BUNDLE_DIR = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
JSON_DIR = BUNDLE_DIR / "tables" / "json"
CATALOG_PATH = BUNDLE_DIR / "tables" / "tables_catalog.json"

def parse_cell(cell_str: str, col_header: str = "") -> Dict[str, Any]:
    c = cell_str.strip()
    if not c or c == "-":
        return {"raw": c, "numeric_value": None, "unit": None, "condition_refs": []}

    # Detect footnote references like '1 400 5)' or '20 1)' or '2 200 4)'
    m_fn = re.search(r"(\d+(?:\s+\d+)*(?:[,\.]\d+)?)\s*(\d+)\)", c)
    condition_refs = []
    num_val = None

    if m_fn:
        num_str = m_fn.group(1).replace(" ", "").replace(",", ".")
        try:
            num_val = float(num_str) if "." in num_str else int(num_str)
        except ValueError:
            num_val = None
        condition_refs.append(int(m_fn.group(2)))
    else:
        # Standard pure number like '6 000' or '50' or '2,5'
        m_num = re.match(r"^(\d+(?:\s+\d+)*(?:[,\.]\d+)?)$", c)
        if m_num:
            num_str = m_num.group(1).replace(" ", "").replace(",", ".")
            try:
                num_val = float(num_str) if "." in num_str else int(num_str)
            except ValueError:
                num_val = None

    # Detect unit from column header or cell text
    unit = None
    combined_context = f"{col_header} {c}".lower()
    if "m2" in combined_context or "m²" in combined_context:
        unit = "m2"
    elif "m3" in combined_context or "m³" in combined_context:
        unit = "m3"
    elif "l/s" in combined_context:
        unit = "L/s"
    elif "mpa" in combined_context:
        unit = "MPa"
    elif "phút" in combined_context or "min" in combined_context:
        unit = "min"
    elif "giờ" in combined_context or " h" in combined_context:
        unit = "h"
    elif re.search(r"\b(m|mét)\b", combined_context):
        unit = "m"

    return {
        "raw": c,
        "numeric_value": num_val,
        "unit": unit,
        "condition_refs": condition_refs,
    }

def classify_footnote(fn_text: str, idx: int) -> Dict[str, Any]:
    t = fn_text.strip()
    fn_id = idx + 1
    m_id = re.search(r"CHÚ THÍCH\s*(\d+)?", t, re.IGNORECASE)
    m_sub = re.match(r"^\s*(\d+)\)\s+", t)

    if m_id and m_id.group(1):
        fn_id = int(m_id.group(1))
    elif m_sub:
        fn_id = int(m_sub.group(1))

    # Classify type
    t_lower = t.lower()
    fn_type = "normative_condition"
    if any(k in t_lower for k in ["trừ", "ngoại trừ", "cho phép không", "không áp dụng"]):
        fn_type = "exception"
    elif any(k in t_lower for k in ["là", "được hiểu là", "nghĩa là", "được xác định bằng"]):
        fn_type = "definition"
    elif any(k in t_lower for k in ["phải", "bắt buộc", "không được", "tối đa", "tối thiểu"]):
        fn_type = "normative_condition"

    return {
        "id": fn_id,
        "type": fn_type,
        "legal_status": "normative" if "ghi chú" not in t_lower else "informative",
        "text": t,
    }

def upgrade_all_tables() -> None:
    json_files = list(JSON_DIR.glob("*.json"))
    upgraded_count = 0
    total_conditions = 0

    catalog_data = {}
    if CATALOG_PATH.exists():
        try:
            catalog_data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        except Exception:
            catalog_data = {}

    for jf in json_files:
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception:
            continue

        headers = data.get("headers", [])
        raw_rows = data.get("rows", [])
        raw_footnotes = data.get("footnotes", [])

        # Build structured cells
        structured_rows = []
        table_conditions = 0

        for r in raw_rows:
            structured_row = []
            for col_idx, cell_val in enumerate(r):
                col_h = headers[col_idx] if col_idx < len(headers) else ""
                parsed = parse_cell(str(cell_val), col_h)
                if parsed["condition_refs"]:
                    table_conditions += len(parsed["condition_refs"])
                structured_row.append(parsed)
            structured_rows.append(structured_row)

        # Build structured footnotes
        structured_footnotes = []
        for idx, fn in enumerate(raw_footnotes):
            structured_footnotes.append(classify_footnote(str(fn), idx))

        data["structured_rows"] = structured_rows
        data["structured_footnotes"] = structured_footnotes
        data["has_normative_conditions"] = table_conditions > 0 or any(f["type"] == "normative_condition" for f in structured_footnotes)

        jf.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        upgraded_count += 1
        total_conditions += table_conditions

        # Update catalog entry
        t_stem = jf.stem
        for cat_item in catalog_data:
            if cat_item.get("file_stem") == t_stem or cat_item.get("table_id") == t_stem:
                cat_item["has_normative_conditions"] = data["has_normative_conditions"]
                cat_item["condition_bindings_count"] = table_conditions

    if catalog_data:
        CATALOG_PATH.write_text(json.dumps(catalog_data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Đã nâng cấp {upgraded_count} bảng sang Structured Footnote Binding Matrix.")
    print(f"✅ Đã nhận diện và liên kết {total_conditions} điều kiện ràng buộc số học.")

def main() -> None:
    print("=================================================================")
    print("      UPGRADING STRUCTURED FOOTNOTE BINDING MATRIX (ADR 0002)    ")
    print("=================================================================")
    upgrade_all_tables()
    print("=================================================================")

if __name__ == "__main__":
    main()
