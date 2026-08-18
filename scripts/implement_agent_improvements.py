"""CCBA Legal Knowledge Enhancement Engine.

Implements 3 major improvements for QCVN 06:2022/BXD:
1. Amended status flags in tables/json/*.json for tables modified by TT 09/2023.
2. Tables Catalog and Interactive Roadmap (tables/README.md & tables_catalog.json).
3. Amendment 1:2023 AST Clause Tree (clauses_sd1.json).
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.stdout.reconfigure(encoding="utf-8")

BUNDLE_DIR = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
JSON_DIR = BUNDLE_DIR / "tables" / "json"
CSV_DIR = BUNDLE_DIR / "tables" / "csv"


def apply_improvement_1_amended_flags() -> None:
    """Flag all tables modified or replaced by Amendment 1:2023 (TT 09/2023/TT-BXD)."""
    amended_map = {
        "bang_06_phan_nhom_nha1_dua_tren": {
            "is_amended": True,
            "amended_by": "Thông tư 09/2023/TT-BXD (Sửa đổi 1:2023)",
            "amendment_anchor": "sd1-bang-6",
            "amendment_type": "modified_content",
            "summary": "Sửa đổi nội dung phân nhóm công năng F1.2, F4.3, F5.1.",
        },
        "bang_07_luu_luong_nuoc_tu_mang": {
            "is_amended": True,
            "amended_by": "Thông tư 09/2023/TT-BXD (Sửa đổi 1:2023)",
            "amendment_anchor": "sd1-bang-7",
            "amendment_type": "repealed_footnote",
            "summary": "Bãi bỏ CHÚ THÍCH 3 của Bảng 7.",
        },
        "bang_10_luu_luong_nuoc_chua_chay": {
            "is_amended": True,
            "amended_by": "Thông tư 09/2023/TT-BXD (Sửa đổi 1:2023)",
            "amendment_anchor": "sd1-bang-10",
            "amendment_type": "completely_replaced",
            "summary": "Thay thế toàn bộ Bảng 10 cũ bằng Bảng 10 mới: 'Lưu lượng nước cho chữa cháy ngoài nhà cho nhà nhóm F5 không có lỗ mở trên mái có chiều rộng trên 60 m'.",
        },
        "bang_a_1_gioi_han_chiu_lua_toi": {
            "is_amended": True,
            "amended_by": "Thông tư 09/2023/TT-BXD (Sửa đổi 1:2023)",
            "amendment_anchor": "sd1-bang-a-1",
            "amendment_type": "modified_footnote",
            "summary": "Sửa đổi CHÚ THÍCH 2 về tường ngoài không chịu lực.",
        },
        "bang_g_1_khoang_cach_gioi_han_phep": {
            "is_amended": True,
            "amended_by": "Thông tư 09/2023/TT-BXD (Sửa đổi 1:2023)",
            "amendment_anchor": "sd1-bang-g-1",
            "amendment_type": "added_footnote",
            "summary": "Bổ sung CHÚ THÍCH 3 về diện tích sàn phòng học.",
        },
        "bang_h_1_nha_o_ky_tuc_xa": {
            "is_amended": True,
            "amended_by": "Thông tư 09/2023/TT-BXD (Sửa đổi 1:2023)",
            "amendment_anchor": "sd1-bang-h-1",
            "amendment_type": "modified_table_cell",
            "summary": "Sửa đổi diện tích khoang cháy và số tầng cho phép nhà F1.2.",
        },
        "bang_h_9_nha_san_xuat": {
            "is_amended": True,
            "amended_by": "Thông tư 09/2023/TT-BXD (Sửa đổi 1:2023)",
            "amendment_anchor": "sd1-bang-h-9",
            "amendment_type": "modified_content_and_footnotes",
            "summary": "Sửa đổi diện tích khoang cháy nhà hạng C bậc III, IV; sửa đổi 4) và bổ sung 5) về chiều cao nhà đến 22m.",
        },
    }

    count = 0
    for stem, meta in amended_map.items():
        jf = JSON_DIR / f"{stem}.json"
        if jf.exists():
            data = json.loads(jf.read_text(encoding="utf-8"))
            data["amendment_status"] = meta
            jf.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            count += 1

    print(f"✅ Cải tiến 1: Đã gắn cờ Sửa đổi 1:2023 (amendment_status) cho {count} bảng kỹ thuật.")


def apply_improvement_2_tables_catalog() -> None:
    """Generate tables_catalog.json and tables/README.md catalog index."""
    catalog: List[Dict[str, Any]] = []

    # Map groups
    group_map = {
        "bang_0": "1. Bảng cốt lõi Chính văn (Chương 2 - Chương 5)",
        "bang_1": "1. Bảng cốt lõi Chính văn (Chương 2 - Chương 5)",
        "bang_a": "2. Phụ lục A - Nhà chiều cao PCCC trên 50m / Có tầng hầm",
        "bang_b": "3. Phụ lục B - Phân loại tính nguy hiểm cháy của vật liệu",
        "bang_c": "4. Phụ lục C - Khói và sản phẩm phân hủy nhiệt",
        "bang_d": "5. Phụ lục D - Phân cấp nguy hiểm cháy kết cấu",
        "bang_e": "6. Phụ lục E - Khoảng cách phòng cháy chống cháy",
        "bang_f": "7. Phụ lục F - Giới hạn chịu lửa danh định kết cấu xây dựng",
        "bang_g": "8. Phụ lục G - Khoảng cách và giải pháp thoát nạn",
        "bang_h": "9. Phụ lục H - Bậc chịu lửa, số tầng và diện tích khoang cháy",
        "bang_i": "10. Phụ lục I - Cấp nước chữa cháy ngoài nhà",
    }

    for jf in sorted(JSON_DIR.glob("*.json")):
        data = json.loads(jf.read_text(encoding="utf-8"))
        stem = jf.stem

        group_name = "11. Bảng kỹ thuật khác"
        for p, g in group_map.items():
            if stem.startswith(p):
                group_name = g
                break

        is_amended = data.get("amendment_status", {}).get("is_amended", False)
        amended_summary = data.get("amendment_status", {}).get("summary", "")

        item = {
            "table_id": data.get("table_id", stem),
            "file_stem": stem,
            "group": group_name,
            "title": data.get("title", stem),
            "columns_count": len(data.get("headers", [])),
            "rows_count": len(data.get("rows", [])),
            "footnotes_count": len(data.get("footnotes", [])),
            "is_amended": is_amended,
            "amendment_summary": amended_summary,
            "json_path": f"tables/json/{stem}.json",
            "csv_path": f"tables/csv/{stem}.csv",
        }
        catalog.append(item)

    # Save JSON catalog
    catalog_json_path = BUNDLE_DIR / "tables" / "tables_catalog.json"
    catalog_json_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

    # Generate Markdown README.md
    md_lines = [
        "# 📚 Mục lục & Bản đồ 64 Bảng Kỹ thuật QCVN 06:2022/BXD & Sửa đổi 1:2023",
        "",
        "> **Tổng số bảng:** 64 bảng kỹ thuật | **Định dạng sẵn có:** GFM Markdown, JSON, CSV (RFC-4180)",
        "> **Phiên bản cập nhật:** Tích hợp quy chuẩn gốc 2022 và các sửa đổi theo Thông tư 09/2023/TT-BXD.",
        "",
        "---",
        "",
    ]

    current_group = ""
    for item in catalog:
        if item["group"] != current_group:
            current_group = item["group"]
            md_lines.extend([f"## {current_group}", "", "| ID Bảng | Tên bảng kỹ thuật | Số cột | Số dòng | Chú thích | Tình trạng Sửa đổi 1:2023 | Tệp tải về |", "|:---|:---|:---:|:---:|:---:|:---:|:---:|"])

        amended_badge = "🔥 **Đã sửa đổi (TT 09/2023)**" if item["is_amended"] else "✅ Nguyên bản 2022"
        fn_badge = f"{item['footnotes_count']} chú thích" if item["footnotes_count"] > 0 else "0"
        links = f"[JSON](json/{item['file_stem']}.json) \| [CSV](csv/{item['file_stem']}.csv)"

        md_lines.append(f"| `{item['table_id']}` | {item['title']} | {item['columns_count']} | {item['rows_count']} | {fn_badge} | {amended_badge} | {links} |")
        md_lines.append("")

    readme_path = BUNDLE_DIR / "tables" / "README.md"
    readme_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"✅ Cải tiến 2: Đã tạo tables/README.md và tables_catalog.json cho 64 bảng kỹ thuật!")


def apply_improvement_3_sd1_ast_tree() -> None:
    """Generate clauses_sd1.json AST index for Amendment 1:2023 (TT 09/2023/TT-BXD)."""
    sd_file = BUNDLE_DIR / "sua_doi_1_2023_qcvn_06_2022_bxd.md"
    text = sd_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    sd_clauses: List[Dict[str, Any]] = []

    for i, line in enumerate(lines):
        m_anchor = re.match(r'<a id="(sd1-[^"]+)"></a>', line.strip())
        if m_anchor:
            anchor_id = m_anchor.group(1)
            # Find next heading or text
            title = ""
            for j in range(i + 1, min(len(lines), i + 5)):
                if lines[j].startswith("#") or lines[j].strip().startswith("“") or lines[j].strip():
                    title = re.sub(r"^#+\s*", "", lines[j]).strip()
                    break

            # Find cross link to base doc
            cross_link_m = re.search(r"\(qcvn_06_2022_bxd\.md#([^\)]+)\)", title)
            target_base_anchor = cross_link_m.group(1) if cross_link_m else None

            # Clean title
            clean_title = re.sub(r"\[([^\]]+)\]\(qcvn_06_2022_bxd\.md#[^\)]+\)", r"\1", title)

            sd_clauses.append({
                "anchor": anchor_id,
                "line_number": i + 1,
                "title": clean_title,
                "target_base_anchor": target_base_anchor,
                "document_file": "sua_doi_1_2023_qcvn_06_2022_bxd.md",
            })

    out_file = BUNDLE_DIR / "clauses_sd1.json"
    out_file.write_text(json.dumps(sd_clauses, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Cải tiến 3: Đã lập cây chỉ mục AST clauses_sd1.json gồm {len(sd_clauses)} nút sửa đổi!")


def main() -> None:
    print("=================================================================")
    print("      TRIỂN KHAI 3 CẢI TIẾN NÂNG CAO TRI THỨC QCVN 06:2022        ")
    print("=================================================================")
    apply_improvement_1_amended_flags()
    apply_improvement_2_tables_catalog()
    apply_improvement_3_sd1_ast_tree()
    print("=================================================================")


if __name__ == "__main__":
    main()
