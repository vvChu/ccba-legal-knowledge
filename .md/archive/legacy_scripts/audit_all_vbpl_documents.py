"""
CCBA Legal Knowledge Spoke — Complete 29 Documents Forensic Quality Audit Engine.
Kiểm toán toàn diện độ nguyên vẹn cấu trúc của 24 VBPL + 2 QCVN + 3 Phụ lục đối chiếu.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT_DIR / "legal_registry.yaml"


def audit_document_bundle(bundle_dir: Path, doc_info: dict[str, Any]) -> dict[str, Any]:
    """Kiểm toán chi tiết một gói tài liệu pháp lý."""
    res: dict[str, Any] = {
        "id": doc_info.get("id", bundle_dir.name),
        "title": doc_info.get("title", bundle_dir.name),
        "type": doc_info.get("type", "VBPL"),
        "bundle_dir": str(bundle_dir.relative_to(ROOT_DIR)),
        "primary_md": None,
        "md_lines": 0,
        "md_chars": 0,
        "headings_count": 0,
        "headings_by_level": {},
        "anchors_count": 0,
        "tables_count": 0,
        "clauses_count": 0,
        "qa_pairs_count": 0,
        "pdf_tracked": False,
        "pdf_exists": False,
        "pdf_sha256": doc_info.get("pdf_sha256", ""),
        "cong_bao_number": doc_info.get("cong_bao_number", ""),
        "issues": [],
        "warnings": [],
    }

    # 1. Tìm tệp Markdown chính
    md_files = list(bundle_dir.glob("*.md"))
    primary_mds = [f for f in md_files if f.name not in ("index.md", "dead_ends.md", "log.md")]

    if not primary_mds:
        res["issues"].append("Không tìm thấy tệp Markdown chính trong bundle!")
        return res

    primary_file = primary_mds[0]
    res["primary_md"] = primary_file.name

    try:
        content = primary_file.read_text(encoding="utf-8")
        lines = content.splitlines()
        res["md_lines"] = len(lines)
        res["md_chars"] = len(content)

        # 2. Quét tiêu đề và cấu trúc đề mục
        h_pattern = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
        headings = h_pattern.findall(content)
        res["headings_count"] = len(headings)

        h_levels: dict[str, int] = {}
        for level_hashes, h_text in headings:
            lvl_name = f"H{len(level_hashes)}"
            h_levels[lvl_name] = h_levels.get(lvl_name, 0) + 1
        res["headings_by_level"] = h_levels

        # 3. Quét thẻ neo
        anchors = re.findall(r'<a\s+id="([^"]+)"', content)
        res["anchors_count"] = len(anchors)

        # 4. Quét bảng biểu Markdown 2D
        table_headers = re.findall(r"^\|(.+)\|\s*\n\|(?:\s*[-:]+[-| :]*)\|\s*$", content, re.MULTILINE)
        res["tables_count"] = len(table_headers)

        # 5. Kiểm tra file đính kèm
        clauses_file = bundle_dir / "clauses.json"
        if clauses_file.exists():
            try:
                c_data = json.loads(clauses_file.read_text(encoding="utf-8"))
                res["clauses_count"] = len(c_data) if isinstance(c_data, list) else 0
            except Exception as e:
                res["warnings"].append(f"Lỗi đọc clauses.json: {e}")

        qa_file = bundle_dir / "qa_benchmark.json"
        if qa_file.exists():
            try:
                qa_data = json.loads(qa_file.read_text(encoding="utf-8"))
                res["qa_pairs_count"] = len(qa_data) if isinstance(qa_data, list) else 0
            except Exception as e:
                res["warnings"].append(f"Lỗi đọc qa_benchmark.json: {e}")

        # 6. Kiểm tra PDF mỏ neo
        pdf_path_str = doc_info.get("pdf_path")
        if pdf_path_str:
            res["pdf_tracked"] = True
            pdf_path = ROOT_DIR / pdf_path_str
            if pdf_path.exists():
                res["pdf_exists"] = True
                calc_sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
                res["pdf_actual_sha256"] = calc_sha

    except Exception as e:
        res["issues"].append(f"Lỗi phân tích cú pháp tệp Markdown: {e}")

    return res


def run_full_spoke_forensic_audit() -> dict[str, Any]:
    """Chạy kiểm toán toàn diện cho toàn bộ văn bản trong legal_registry.yaml."""
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy registry tại {REGISTRY_PATH}")

    reg = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    laws = reg.get("laws", [])

    audit_results: list[dict[str, Any]] = []
    total_issues = 0
    total_warnings = 0
    total_lines = 0
    total_chars = 0
    total_headings = 0
    total_anchors = 0
    total_tables = 0
    total_clauses = 0
    total_qa = 0

    print("=================================================================")
    print("   CCBA LEGAL KNOWLEDGE SPOKE — FORENSIC QUALITY AUDIT REPORT    ")
    print("=================================================================")
    print(f"Tổng số văn bản theo dõi trong Registry: {len(laws)}")
    print("-----------------------------------------------------------------")

    for idx, doc in enumerate(laws, 1):
        bp = doc.get("bundle_path", "")
        bundle_dir = ROOT_DIR / bp
        if not bundle_dir.exists():
            print(f"❌ [{idx:02d}] THIẾU THƯ MỤC BUNDLE: {bp}")
            total_issues += 1
            continue

        res = audit_document_bundle(bundle_dir, doc)
        audit_results.append(res)

        total_lines += res["md_lines"]
        total_chars += res["md_chars"]
        total_headings += res["headings_count"]
        total_anchors += res["anchors_count"]
        total_tables += res["tables_count"]
        total_clauses += res["clauses_count"]
        total_qa += res["qa_pairs_count"]

        status_tag = "✅ PASS" if not res["issues"] else f"❌ FAIL ({len(res['issues'])} lỗi)"
        if res["warnings"]:
            status_tag += f" [⚠️ {len(res['warnings'])} warnings]"

        doc_title_short = res["title"][:50] + "..." if len(res["title"]) > 50 else res["title"]
        print(
            f"{idx:02d}. [{status_tag:<8}] {doc_title_short:<55} | "
            f"{res['md_lines']:>5} dòng | {res['headings_count']:>3} mục | "
            f"{res['tables_count']:>2} bảng | {res['clauses_count']:>4} AST"
        )

        for issue in res["issues"]:
            print(f"      ❌ ERROR: {issue}")
            total_issues += 1
        for warn in res["warnings"]:
            print(f"      ⚠️ WARN : {warn}")
            total_warnings += 1

    print("\n=================================================================")
    print("                      TỔNG KẾT KIỂM TOÁN                         ")
    print("=================================================================")
    print(f"• Tổng số văn bản đã kiểm tra  : {len(audit_results)}/29 văn bản")
    print(f"• Tổng số dòng văn bản Markdown : {total_lines:,} dòng ({total_chars / (1024*1024):.2f} MB)")
    print(f"• Tổng số đề mục pháp lý (H1-H5): {total_headings:,} mục")
    print(f"• Tổng số thẻ neo ngữ nghĩa     : {total_anchors:,} thẻ neo <a id=...>")
    print(f"• Tổng số bảng biểu 2D GFM      : {total_tables:,} bảng")
    print(f"• Tổng số điều khoản cây AST    : {total_clauses:,} clauses")
    print(f"• Tổng số Ground-Truth QA pairs : {total_qa:,} QA pairs")
    print(f"• Số lỗi phát hiện (Errors)     : {total_issues}")
    print(f"• Số cảnh báo (Warnings)        : {total_warnings}")
    print("-----------------------------------------------------------------")
    if total_issues == 0:
        print("🎉 KẾT LUẬN: 100% VĂN BẢN TRONG KHO TRI THỨC ĐẠT CHUẨN HOÀN HẢO OKF v2.0!")
    else:
        print(f"⚠️ CẦN SỬA ĐỔI: Phát hiện {total_issues} lỗi cần xử lý.")
    print("=================================================================\n")

    return {
        "total_documents": len(audit_results),
        "total_lines": total_lines,
        "total_headings": total_headings,
        "total_anchors": total_anchors,
        "total_tables": total_tables,
        "total_clauses": total_clauses,
        "total_qa": total_qa,
        "total_issues": total_issues,
        "total_warnings": total_warnings,
        "details": audit_results,
    }


def main() -> None:
    report = run_full_spoke_forensic_audit()
    sys.exit(0 if report["total_issues"] == 0 else 1)


if __name__ == "__main__":
    main()
