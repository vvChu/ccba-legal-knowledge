"""CCBA Legal Knowledge Spoke — Unified Deep Module CLI Facade.

Hides all low-level processing (docx conversion, AST clauses extraction,
table reconstruction, OKF v0.2 packaging, registry metadata graph update,
and integrity validation) behind a single, elegant CLI seam.
"""

import argparse
import sys
import yaml
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.docx_converter import convert_docx_to_okf_bundle
from scripts.validate_legal_spoke import LegalSpokeValidator

def get_spoke_stats(root_dir: Path) -> dict:
    """Compute comprehensive metrics for the legal knowledge spoke."""
    registry_file = root_dir / "legal_registry.yaml"
    legal_docs_dir = root_dir / "legal_docs"

    total_md_bytes = 0
    total_clauses = 0
    total_qa = 0

    if legal_docs_dir.exists():
        for md_file in legal_docs_dir.rglob("*.md"):
            total_md_bytes += md_file.stat().st_size

        for c_file in legal_docs_dir.rglob("clauses.json"):
            try:
                data = yaml.safe_load(c_file.read_text(encoding="utf-8"))
                total_clauses += len(data) if isinstance(data, list) else 0
            except Exception:
                pass

        for q_file in legal_docs_dir.rglob("qa_benchmark.json"):
            try:
                data = yaml.safe_load(q_file.read_text(encoding="utf-8"))
                total_qa += len(data) if isinstance(data, list) else 0
            except Exception:
                pass

    doc_count = 0
    categories_count = {}
    if registry_file.exists():
        try:
            reg_data = yaml.safe_load(registry_file.read_text(encoding="utf-8"))
            laws = reg_data.get("laws", [])
            doc_count = len(laws)
            for doc in laws:
                doc_type = doc.get("type", "Khác")
                categories_count[doc_type] = categories_count.get(doc_type, 0) + 1
        except Exception:
            pass

    return {
        "doc_count": doc_count,
        "categories": categories_count,
        "total_size_mb": total_md_bytes / (1024 * 1024),
        "total_clauses": total_clauses,
        "total_qa": total_qa,
    }

def print_stats_report(root_dir: Path) -> None:
    """Print human-readable statistics report."""
    stats = get_spoke_stats(root_dir)
    print("=================================================================")
    print("       CCBA LEGAL KNOWLEDGE SPOKE — METRICS REPORT               ")
    print("=================================================================")
    print(f"Target Workspace     : {root_dir}")
    print(f"Total Legal Documents : {stats['doc_count']}")
    print(f"Document Categories  :")
    for cat, count in stats["categories"].items():
        print(f"  • {cat:<20}: {count} văn bản")
    print(f"Total Markdown Volume: {stats['total_size_mb']:.2f} MB")
    print(f"Total AST Clauses    : {stats['total_clauses']:,}")
    print(f"Total Ground-Truth QA: {stats['total_qa']:,}")
    print("=================================================================\n")

def main() -> None:
    """Main CLI entrypoint for Spoke Facade."""
    parser = argparse.ArgumentParser(description="CCBA Legal Knowledge Spoke Unified Management Tool.")
    subparsers = parser.add_subparsers(dest="command", help="Command action")

    # Command: validate
    subparsers.add_parser("validate", help="Run integrity and schema validation checks (includes Fake Data Gate)")

    # Command: stats
    subparsers.add_parser("stats", help="Print total knowledge volume, clauses count, and QA benchmark metrics")

    # Command: ingest
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a .docx file into an OKF v0.2 bundle")
    ingest_parser.add_argument("docx_path", type=Path, help="Path to input .docx file")
    ingest_parser.add_argument("slug", type=str, help="Document slug (e.g. nghi_dinh_217_2026_nd_cp)")
    ingest_parser.add_argument("-t", "--doc-type", type=str, default="vbpl", help="Document profile type (default: vbpl)")

    # Command: sync-notebooklm
    sync_parser = subparsers.add_parser(
        "sync-notebooklm",
        help="Đồng bộ danh sách 32 nguồn Markdown sạch lên Google NotebookLM (ADR 0012)",
    )
    sync_parser.add_argument(
        "--notebook-id",
        type=str,
        default="6dca7e4e-c407-4d1f-882a-e0d9459d1120",
        help="Notebook ID đích trên Google NotebookLM",
    )
    sync_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ in manifest danh mục 32 tệp, không gọi API",
    )

    # Command: audit
    subparsers.add_parser(
        "audit",
        help="Chạy kiểm toán pháp y toàn diện 29 văn bản trong kho tri thức",
    )

    args = parser.parse_args()
    root_dir = Path(__file__).resolve().parent.parent

    if args.command == "validate":
        validator = LegalSpokeValidator(root_dir)
        success = validator.run_all_checks()
        sys.exit(0 if success else 1)

    elif args.command == "stats":
        print_stats_report(root_dir)

    elif args.command == "audit":
        from scripts.audit_all_vbpl_documents import run_full_spoke_forensic_audit

        report = run_full_spoke_forensic_audit()
        sys.exit(0 if report["total_issues"] == 0 else 1)

    elif args.command == "ingest":
        target_bundle_dir = root_dir / "legal_docs" / "01_vbpl" / args.slug
        res = convert_docx_to_okf_bundle(
            docx_path=args.docx_path,
            target_bundle_dir=target_bundle_dir,
            output_filename=f"{args.slug}.md",
            doc_type=args.doc_type,
        )
        print(f"\n[INGEST SUCCESSFUL]: {res}")

    elif args.command == "sync-notebooklm":
        import asyncio
        from scripts.sync_notebooklm_knowledge import execute_sync, get_canonical_whitelist

        whitelist = get_canonical_whitelist(root_dir)
        code = asyncio.run(execute_sync(args.notebook_id, whitelist, dry_run=args.dry_run))
        sys.exit(code)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
