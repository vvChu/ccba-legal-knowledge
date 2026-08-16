"""Batch convert and register all 12 authentic Circular docx files to OKF v0.2 Markdown bundles."""

import os
import shutil
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.docx_converter import convert_docx_to_okf_bundle

CIRCULAR_MAP = [
    {
        "slug": "thong_tu_101_2026_tt_bqp",
        "doc_number": "101/2026/TT-BQP",
        "docx_name": "101_2026_TT-BQP_713990.docx",
        "title": "Thông tư 101/2026/TT-BQP quy định chi tiết trong lĩnh vực quốc phòng theo Luật Xây dựng 2025",
        "issued_by": "Bộ Quốc phòng",
        "guided_by": "Luat-Xay-dung-2025-135-2025-QH15"
    },
    {
        "slug": "thong_tu_32_2026_tt_bxd",
        "doc_number": "32/2026/TT-BXD",
        "docx_name": "32_2026_TT-BXD_711676.docx",
        "title": "Thông tư 32/2026/TT-BXD quy định chi tiết một số điều của Nghị định 207/2026/NĐ-CP về quản lý chất lượng",
        "issued_by": "Bộ Xây dựng",
        "guided_by": "nghi_dinh_207_2026_nd_cp"
    },
    {
        "slug": "thong_tu_33_2026_tt_bxd",
        "doc_number": "33/2026/TT-BXD",
        "docx_name": "33_2026_TT-BXD_712404.docx",
        "title": "Thông tư 33/2026/TT-BXD về đánh giá an toàn công trình trong quá trình khai thác, sử dụng",
        "issued_by": "Bộ Xây dựng",
        "guided_by": "nghi_dinh_207_2026_nd_cp"
    },
    {
        "slug": "thong_tu_34_2026_tt_bxd",
        "doc_number": "34/2026/TT-BXD",
        "docx_name": "34_2026_TT-BXD_712306.docx",
        "title": "Thông tư 34/2026/TT-BXD quy định chi tiết về cấp công trình xây dựng phục vụ quản lý hoạt động xây dựng",
        "issued_by": "Bộ Xây dựng",
        "guided_by": "nghi_dinh_207_2026_nd_cp"
    },
    {
        "slug": "thong_tu_36_2026_tt_bxd",
        "doc_number": "36/2026/TT-BXD",
        "docx_name": "36_2026_TT-BXD_712408.docx",
        "title": "Thông tư 36/2026/TT-BXD hướng dẫn xác định và quản lý chi phí đầu tư xây dựng",
        "issued_by": "Bộ Xây dựng",
        "guided_by": "nghi_dinh_206_2026_nd_cp"
    },
    {
        "slug": "thong_tu_37_2026_tt_bxd",
        "doc_number": "37/2026/TT-BXD",
        "docx_name": "37_2026_TT-BXD_712395.docx",
        "title": "Thông tư 37/2026/TT-BXD hướng dẫn phương pháp xác định định mức dự toán và chỉ tiêu kinh tế kỹ thuật",
        "issued_by": "Bộ Xây dựng",
        "guided_by": "nghi_dinh_206_2026_nd_cp"
    },
    {
        "slug": "thong_tu_38_2026_tt_bxd",
        "doc_number": "38/2026/TT-BXD",
        "docx_name": "38_2026_TT-BXD_712406.docx",
        "title": "Thông tư 38/2026/TT-BXD ban hành hệ thống định mức xây dựng quốc gia",
        "issued_by": "Bộ Xây dựng",
        "guided_by": "nghi_dinh_206_2026_nd_cp"
    },
    {
        "slug": "thong_tu_39_2026_tt_bxd",
        "doc_number": "39/2026/TT-BXD",
        "docx_name": "39_2026_TT-BXD_712407.docx",
        "title": "Thông tư 39/2026/TT-BXD hướng dẫn cơ sở dữ liệu quốc gia về hoạt động xây dựng",
        "issued_by": "Bộ Xây dựng",
        "guided_by": "nghi_dinh_212_2026_nd_cp"
    },
    {
        "slug": "thong_tu_40_2026_tt_bxd",
        "doc_number": "40/2026/TT-BXD",
        "docx_name": "40_2026_TT-BXD_712405.docx",
        "title": "Thông tư 40/2026/TT-BXD hướng dẫn xác định chi phí bảo trì công trình xây dựng",
        "issued_by": "Bộ Xây dựng",
        "guided_by": "nghi_dinh_207_2026_nd_cp"
    },
    {
        "slug": "thong_tu_41_2026_tt_bxd",
        "doc_number": "41/2026/TT-BXD",
        "docx_name": "41_2026_TT-BXD_697288.docx",
        "title": "Thông tư 41/2026/TT-BXD về quản lý chất lượng sản phẩm, hàng hóa vật liệu xây dựng",
        "issued_by": "Bộ Xây dựng",
        "guided_by": "nghi_dinh_209_2026_nd_cp"
    },
    {
        "slug": "thong_tu_73_2026_tt_btc",
        "doc_number": "73/2026/TT-BTC",
        "docx_name": "73_2026_TT-BTC_712590.docx",
        "title": "Thông tư 73/2026/TT-BTC quy định hệ thống mẫu biểu trong công tác quyết toán vốn đầu tư",
        "issued_by": "Bộ Tài chính",
        "guided_by": "nghi_dinh_193_2026_nd_cp"
    },
    {
        "slug": "thong_tu_79_2026_tt_btc",
        "doc_number": "79/2026/TT-BTC",
        "docx_name": "79_2026_TT-BTC_713348.docx",
        "title": "Thông tư 79/2026/TT-BTC quy định thu, chi của Chủ đầu tư, Ban QLDA sử dụng vốn ngân sách nhà nước",
        "issued_by": "Bộ Tài chính",
        "guided_by": "nghi_dinh_193_2026_nd_cp"
    }
]

def process_and_register_all_circulars():
    root_dir = Path(__file__).resolve().parent.parent
    extracted_base = root_dir / ".md" / "extracted_docs"
    bundle_base = root_dir / "legal_docs" / "01_vbpl"
    registry_file = root_dir / "legal_registry.yaml"

    print("=================================================================")
    print("       BATCH CIRCULARS (THÔNG TƯ) CONVERSION ENGINE             ")
    print("=================================================================\n")

    converted = []
    for item in CIRCULAR_MAP:
        slug = item["slug"]
        docx_name = item["docx_name"]

        # Step 1: Ensure directory in extracted_docs
        src_docx = extracted_base / docx_name
        target_dir = extracted_base / slug
        target_dir.mkdir(parents=True, exist_ok=True)
        dst_docx = target_dir / docx_name

        if src_docx.exists():
            shutil.move(str(src_docx), str(dst_docx))

        if not dst_docx.exists():
            print(f"⚠️ [WARNING] File missing for {slug}: {dst_docx}")
            continue

        target_bundle_dir = bundle_base / slug
        print(f"---> Converting {slug} ({docx_name})...")

        res = convert_docx_to_okf_bundle(
            docx_path=dst_docx,
            target_bundle_dir=target_bundle_dir,
            output_filename=f"{slug}.md",
            doc_type="vbpl"
        )
        md_file = target_bundle_dir / f"{slug}.md"
        size_kb = md_file.stat().st_size / 1024 if md_file.exists() else 0
        res["size_kb"] = size_kb
        converted.append((item, res))

    # Step 2: Register in legal_registry.yaml
    if registry_file.exists():
        data = yaml.safe_load(registry_file.read_text(encoding="utf-8"))
        laws = data.get("laws", [])
        existing_ids = {doc.get("id") for doc in laws if isinstance(doc, dict)}

        new_entries_count = 0
        for item, res in converted:
            slug = item["slug"]
            doc_id = slug
            if doc_id in existing_ids:
                continue

            entry = {
                "id": doc_id,
                "document_number": item["doc_number"],
                "title": item["title"],
                "type": "Thông tư",
                "issued_by": item["issued_by"],
                "issued_date": "2026-06-30",
                "effective_date": "2026-07-01",
                "status": "active",
                "bundle_path": f"legal_docs/01_vbpl/{slug}/",
                "source_url": f"https://thuvienphapluat.vn/van-ban/{doc_id}.aspx",
                "relations": {
                    "guided_by": item["guided_by"]
                }
            }
            laws.append(entry)
            new_entries_count += 1

        data["laws"] = laws
        data["registry_summary"]["total_documents"] = len(laws)
        data["registry_summary"]["categories"]["01_vbpl"] = len(laws)

        registry_file.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(f"\n[REGISTRY UPDATE]: Added {new_entries_count} Circular entries. Total documents: {len(laws)}")

    print("\n=================================================================")
    print("CONVERSION & REGISTRY SUMMARY REPORT:")
    print("=================================================================")
    for item, res in converted:
        print(f"✅ {item['slug']:<28}: Size={res['size_kb']:.1f} KB | Clauses={res.get('clauses_count', 0)} | QA={res.get('qa_count', 0)}")

if __name__ == "__main__":
    process_and_register_all_circulars()
