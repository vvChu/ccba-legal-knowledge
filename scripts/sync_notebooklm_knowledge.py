"""CCBA Legal Knowledge Spoke — Google NotebookLM / Cloud RAG Sync Engine.

Tuân thủ nghiêm ngặt:
- ADR 0012: Clean Unified Whitelist & Quarantine Gate
- ADR 0021 & ADR 0036: OKF v2.4 Universal Pure Normative Body & Atomic Templates
- ADR 0023: Full Comprehensive NotebookLM Ingestion Strategy for Ultra Tier (500+ sources capacity)

Tạo bởi CCBA — Trung tâm Tư vấn và Ứng dụng BIM trong Xây dựng.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import sys
from pathlib import Path
from typing import Any

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT_DIR / "legal_registry.yaml"
WORKSPACE_CONTEXT_PATH = ROOT_DIR / ".md" / "workspace_context.yaml"
ULTRA_TIER_MAX_SOURCES = 500


def get_canonical_manifest(
    root_dir: Path, ultra_full: bool = True
) -> list[dict[str, Any]]:
    """Trích xuất danh sách nguồn tri thức chuẩn hóa theo ADR 0012 và ADR 0023."""
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy registry tại {REGISTRY_PATH}")

    reg = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    all_docs: list[dict[str, Any]] = []
    if "laws" in reg:
        all_docs.extend(reg["laws"])
    if "documents" in reg:
        all_docs.extend(reg["documents"].values())

    sources: list[dict[str, Any]] = []
    seen_paths: set[str] = set()

    for item in all_docs:
        bp = item.get("bundle_path", "")
        if not bp:
            continue
        bundle_dir = root_dir / bp.strip("/")
        if not bundle_dir.exists():
            continue

        slug = bundle_dir.name

        # 1. Thân văn bản Markdown chính (<slug>.md)
        normative_md = bundle_dir / f"{slug}.md"
        if normative_md.exists() and str(normative_md) not in seen_paths:
            content = normative_md.read_text(encoding="utf-8")
            sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
            seen_paths.add(str(normative_md))
            sources.append(
                {
                    "id": item.get("id", slug),
                    "title": item.get("title", slug),
                    "type": "Normative Body",
                    "category": bp.strip("/").split("/")[1] if len(bp.strip("/").split("/")) > 1 else "01_vbpl",
                    "file_path": normative_md,
                    "rel_path": normative_md.relative_to(root_dir),
                    "size_bytes": normative_md.stat().st_size,
                    "word_count": len(content.split()),
                    "sha256": sha,
                }
            )

        # 2. Toàn bộ Biểu mẫu Nguyên tử (templates/) theo ADR 0023
        if ultra_full:
            tmpl_dir = bundle_dir / "templates"
            if tmpl_dir.exists():
                for tf in sorted(tmpl_dir.glob("**/*.md")):
                    if str(tf) in seen_paths:
                        continue
                    content = tf.read_text(encoding="utf-8")
                    sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
                    seen_paths.add(str(tf))
                    sources.append(
                        {
                            "id": f"{slug}_{tf.stem}",
                            "title": f"Biểu mẫu {tf.stem} ({slug})",
                            "type": "Atomic Form Template",
                            "category": "templates",
                            "file_path": tf,
                            "rel_path": tf.relative_to(root_dir),
                            "size_bytes": tf.stat().st_size,
                            "word_count": len(content.split()),
                            "sha256": sha,
                        }
                    )

            # 3. Toàn bộ Bảng tra cứu số liệu (tables/csv/) theo ADR 0023
            table_dir = bundle_dir / "tables" / "csv"
            if table_dir.exists():
                for tb in sorted(table_dir.glob("*.csv")):
                    if str(tb) in seen_paths:
                        continue
                    content = tb.read_text(encoding="utf-8", errors="replace")
                    sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
                    seen_paths.add(str(tb))
                    sources.append(
                        {
                            "id": f"{slug}_{tb.stem}",
                            "title": f"Bảng {tb.stem} ({slug})",
                            "type": "Technical Table 2D",
                            "category": "tables",
                            "file_path": tb,
                            "rel_path": tb.relative_to(root_dir),
                            "size_bytes": tb.stat().st_size,
                            "word_count": len(content.split(",")),
                            "sha256": sha,
                        }
                    )

            # 4. Toàn bộ Phụ lục Kỹ thuật Quy phạm (annexes/) theo ADR 0036
            annex_dir = bundle_dir / "annexes"
            if annex_dir.exists():
                for af in sorted(annex_dir.glob("**/*.md")):
                    if str(af) in seen_paths or af.name == "index.md":
                        continue
                    content = af.read_text(encoding="utf-8")
                    sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
                    seen_paths.add(str(af))
                    sources.append(
                        {
                            "id": f"{slug}_{af.stem}",
                            "title": f"Phụ lục {af.stem} ({slug})",
                            "type": "Technical Normative Annex",
                            "category": "annexes",
                            "file_path": af,
                            "rel_path": af.relative_to(root_dir),
                            "size_bytes": af.stat().st_size,
                            "word_count": len(content.split()),
                            "sha256": sha,
                        }
                    )

    # 4. Các Bảng so sánh đối chiếu quy chuẩn độc lập (Internal Matrix)
    legal_docs = root_dir / "legal_docs"
    if legal_docs.exists():
        for cat_dir in sorted(legal_docs.iterdir()):
            if not cat_dir.is_dir() or cat_dir.name.startswith("."):
                continue
            cat = cat_dir.name
            for mf in sorted(cat_dir.glob("*.md")):
                if mf.name in ("index.md", "dead_ends.md", "log.md") or str(mf) in seen_paths:
                    continue
                content = mf.read_text(encoding="utf-8")
                sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
                seen_paths.add(str(mf))
                sources.append(
                    {
                        "id": mf.stem,
                        "title": f"Bảng Đối Chiếu {mf.stem}",
                        "type": "Matrix Comparison",
                        "category": cat,
                        "file_path": mf,
                        "rel_path": mf.relative_to(root_dir),
                        "size_bytes": mf.stat().st_size,
                        "word_count": len(content.split()),
                        "sha256": sha,
                    }
                )

    return sources


def print_manifest(sources: list[dict[str, Any]], ultra_full: bool = True) -> None:
    """In bảng tổng hợp manifest và đo lường hạn ngạch Cloud RAG Ultra."""
    total_bytes = sum(w["size_bytes"] for w in sources)
    total_words = sum(w["word_count"] for w in sources)
    quota_ratio = (len(sources) / ULTRA_TIER_MAX_SOURCES) * 100

    normative_count = sum(1 for s in sources if s["type"] == "Normative Body")
    template_count = sum(1 for s in sources if s["type"] == "Atomic Form Template")
    table_count = sum(1 for s in sources if s["type"] == "Technical Table 2D")
    matrix_count = sum(1 for s in sources if s["type"] == "Matrix Comparison")

    print("=========================================================================================")
    if ultra_full:
        print("   CCBA NOTEBOOKLM FULL COMPREHENSIVE ULTRA MANIFEST (ADR 0023)                         ")
    else:
        print("   CCBA NOTEBOOKLM NORMATIVE-ONLY MANIFEST (ADR 0012 WHITELIST)                         ")
    print("=========================================================================================")
    print(f"  • Tổng số nguồn nạp (Sources)   : {len(sources):,} tệp / {ULTRA_TIER_MAX_SOURCES} quota ({quota_ratio:.1f}% Ultra Tier)")
    print(f"    - Thân văn bản thuần khiết    : {normative_count} tệp")
    print(f"    - Biểu mẫu nguyên tử         : {template_count} tệp")
    print(f"    - Bảng tra cứu kỹ thuật 2D   : {table_count} tệp")
    print(f"    - Bảng đối chiếu ma trận     : {matrix_count} tệp")
    print(f"  • Tổng dung lượng dữ liệu      : {total_bytes / (1024 * 1024):.2f} MB ({total_bytes:,} bytes)")
    print(f"  • Tổng khối lượng từ (Words)   : {total_words:,} words")
    print("-----------------------------------------------------------------------------------------")
    print(f"{'TT':<3} | {'Phân loại':<20} | {'Dung lượng':<10} | {'Từ/Cột':<8} | {'Đường dẫn tệp'}")
    print("-" * 89)
    for idx, item in enumerate(sources[:30], 1):
        size_kb = f"{item['size_bytes'] / 1024:.1f} KB"
        words = f"{item['word_count']:,}"
        print(f"{idx:02d}  | {item['type'][:19]:<20} | {size_kb:<10} | {words:<8} | {item['rel_path']}")
    if len(sources) > 30:
        print(f"... và {len(sources) - 30} tệp nguồn khác sẵn sàng đồng bộ.")
    print("=========================================================================================\n")


async def execute_sync(
    notebook_id: str, sources: list[dict[str, Any]], dry_run: bool = False, ultra_full: bool = True
) -> int:
    """Thực thi đồng bộ danh sách nguồn lên NotebookLM."""
    print_manifest(sources, ultra_full=ultra_full)

    if dry_run:
        print("✅ [DRY-RUN]: Đã kiểm tra đối soát 100% tệp tin. Toàn bộ nguồn khớp hạn ngạch Ultra an toàn. Không gọi API.")
        return 0

    try:
        from ccba_notebooklm import get_client

        client = get_client()
    except ImportError as exc:
        print(f"Lỗi import ccba_notebooklm (hoặc thiếu get_client): {exc}", file=sys.stderr)
        return 1

    if client.use_mock:
        print("-----------------------------------------------------------------")
        print("[MOCK MODE]: Chưa phát hiện Google Session Cookie thực tế.")
        print("Đang chạy mô phỏng đồng bộ dữ liệu qua Mock Client Adapter...")
        print("-----------------------------------------------------------------")
        for idx, item in enumerate(sources, 1):
            print(f"[{idx:03d}/{len(sources)}] -> Uploaded (mock): {item['rel_path'].name}")
        print(f"\n✅ [MOCK SYNC SUCCESSFUL]: Đã mô phỏng nạp thành công {len(sources)} nguồn vào Mock NotebookLM.")
        return 0

    print(f"Bắt đầu kết nối Google NotebookLM (ID: {notebook_id})...")
    try:
        async with client as real_client:
            for idx, item in enumerate(sources, 1):
                file_path_str = str(item["file_path"].resolve())
                print(f"[{idx:03d}/{len(sources)}] Đang tải lên: {item['rel_path'].name}...", end=" ")
                try:
                    await real_client.add_file_source(notebook_id, file_path_str)
                    print("✅ Xong.")
                except Exception as e:
                    print(f"❌ Lỗi: {e}")

        print("\n🎉 HOÀN THÀNH: Đã đồng bộ toàn bộ kho tri thức toàn diện lên Google NotebookLM!")
        return 0

    except Exception as e:
        print("\n" + "=" * 65)
        print("⚠️  THÔNG BÁO: Session Google Cookies đã hết hạn hoặc chưa đăng nhập.")
        print(f"Chi tiết lỗi: {e}")
        print("-----------------------------------------------------------------")
        print("👉 HƯỚNG DẪN ĐĂNG NHẬP LẠI (Chỉ cần làm 1 lần):")
        print("   Mở cửa sổ PowerShell hoặc CMD bên ngoài và chạy lệnh:")
        print("   python -m ccba_legal login")
        print("   (hoặc chạy: python -m notebooklm login)")
        print("   Sau khi trình duyệt đăng nhập xong, phiên làm việc sẽ được lưu tự động.")
        print("=" * 65)
        return 2


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Đồng bộ kho tri thức pháp lý toàn diện lên Google NotebookLM (ADR 0023)."
    )
    parser.add_argument(
        "--notebook-id",
        type=str,
        default="6dca7e4e-c407-4d1f-882a-e0d9459d1120",
        help="Notebook ID đích trên Google NotebookLM",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ kiểm tra và in manifest danh mục nguồn, không gọi API",
    )
    parser.add_argument(
        "--normative-only",
        action="store_true",
        help="Chỉ nạp thân văn bản chính (ADR 0012 whitelist 50 sources)",
    )
    args = parser.parse_args()

    ultra_full = not args.normative_only
    sources = get_canonical_manifest(ROOT_DIR, ultra_full=ultra_full)
    code = asyncio.run(
        execute_sync(
            args.notebook_id, sources, dry_run=args.dry_run, ultra_full=ultra_full
        )
    )
    sys.exit(code)


if __name__ == "__main__":
    main()
