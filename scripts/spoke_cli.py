"""CCBA Legal Knowledge Spoke — Unified Deep Module CLI Facade.

Hides all low-level processing (docx conversion, AST clauses extraction,
table reconstruction, OKF v2.4 Universal packaging, registry metadata graph update,
and integrity validation) behind a single, elegant CLI seam.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

try:
    from ccba_legal.constants import CURRENT_OKF_SPEC
except ImportError:
    CURRENT_OKF_SPEC = "v2.4 Universal"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ccba_legal import convert_docx_to_okf_bundle  # noqa: E402
from scripts.validate_legal_spoke import LegalSpokeValidator  # noqa: E402


def get_spoke_stats(root_dir: Path) -> Dict[str, Any]:
    """Compute comprehensive metrics for the legal knowledge spoke."""
    registry_file = root_dir / "legal_registry.yaml"
    legal_docs_dir = root_dir / "legal_docs"

    total_md_bytes = 0
    total_clauses = 0
    total_qa = 0

    if legal_docs_dir.exists():
        for md_file in legal_docs_dir.rglob("*.md"):
            try:
                total_md_bytes += md_file.stat().st_size
            except OSError:
                pass

        for c_file in legal_docs_dir.rglob("clauses.json"):
            try:
                data = json.loads(c_file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    total_clauses += len(data)
                elif isinstance(data, dict):
                    total_clauses += len(data.get("clauses", []))
            except (json.JSONDecodeError, OSError):
                pass

        for q_file in legal_docs_dir.rglob("qa_benchmark.json"):
            try:
                data = json.loads(q_file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    total_qa += len(data)
                elif isinstance(data, dict):
                    total_qa += len(data.get("questions") or data.get("qa_entries") or [])
            except (json.JSONDecodeError, OSError):
                pass

    total_tables = len(list(legal_docs_dir.glob("**/tables/csv/*.csv"))) if legal_docs_dir.exists() else 0
    total_figures = len(list(legal_docs_dir.glob("**/figures/cards/*.md"))) if legal_docs_dir.exists() else 0
    total_templates = len(list(legal_docs_dir.glob("**/templates/*.md"))) if legal_docs_dir.exists() else 0

    doc_count = 0
    categories_count: Dict[str, int] = {}
    if registry_file.exists():
        try:
            reg_data = yaml.safe_load(registry_file.read_text(encoding="utf-8"))
            if isinstance(reg_data, dict):
                laws = reg_data.get("laws", [])
                if isinstance(laws, list):
                    doc_count = len(laws)
                    for doc in laws:
                        if isinstance(doc, dict):
                            doc_type = doc.get("type", "Khác")
                            categories_count[doc_type] = categories_count.get(doc_type, 0) + 1
        except (yaml.YAMLError, OSError):
            pass

    return {
        "doc_count": doc_count,
        "categories": categories_count,
        "total_size_mb": total_md_bytes / (1024 * 1024),
        "total_clauses": total_clauses,
        "total_qa": total_qa,
        "total_tables": total_tables,
        "total_figures": total_figures,
        "total_templates": total_templates,
    }


def print_stats_report(root_dir: Path) -> None:
    """Print human-readable statistics report."""
    stats = get_spoke_stats(root_dir)
    print("=================================================================")
    print("       CCBA LEGAL KNOWLEDGE SPOKE — METRICS REPORT               ")
    print("=================================================================")
    print(f"Target Workspace     : {root_dir}")
    print(f"Specification        : OKF {CURRENT_OKF_SPEC} (Universal Agent-Centric)")
    print(f"Total Legal Documents : {stats['doc_count']}")
    print("Document Categories  :")
    for cat, count in stats["categories"].items():
        print(f"  • {cat:<26}: {count} văn bản")
    print(f"Total Markdown Volume: {stats['total_size_mb']:.2f} MB")
    print(f"Total AST Clauses    : {stats['total_clauses']:,}")
    print(f"Total Ground-Truth QA: {stats['total_qa']:,}")
    print("-----------------------------------------------------------------")
    print("Specialized Compartments (ADR 0036):")
    print(f"  • 2D Data Tables (CSV)   : {stats['total_tables']} tables")
    print(f"  • Multimodal Figure Cards: {stats['total_figures']} visual cards")
    print(f"  • Atomic Form Templates  : {stats['total_templates']} form templates")
    print("=================================================================\n")


def main() -> None:
    """Main CLI entrypoint for Spoke Facade."""
    parser = argparse.ArgumentParser(
        description=f"CCBA Legal Knowledge Spoke Unified Management Tool (OKF {CURRENT_OKF_SPEC})."
    )
    subparsers = parser.add_subparsers(dest="command", help="Command action")

    # Command: validate
    subparsers.add_parser(
        "validate",
        help="Run 15-Gate Master integrity and schema validation checks (ADR 0041, ADR 0038)",
    )

    # Command: stats
    subparsers.add_parser(
        "stats",
        help="Print total knowledge volume, clauses count, QA benchmark, and compartment metrics",
    )

    # Command: ingest
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a .docx file into an OKF v2.4 bundle")
    ingest_parser.add_argument("docx_path", type=Path, help="Path to input .docx file")
    ingest_parser.add_argument("slug", type=str, help="Document slug (e.g. nghi_dinh_217_2026_nd_cp)")
    ingest_parser.add_argument(
        "-c", "--category", type=str, choices=["01_vbpl", "02_qcvn", "03_tcvn"], default="01_vbpl", help="Document category"
    )
    ingest_parser.add_argument("-t", "--doc-type", type=str, default="vbpl", help="Document profile type (default: vbpl)")

    # Command: sync-notebooklm
    sync_parser = subparsers.add_parser(
        "sync-notebooklm",
        help="Đồng bộ danh sách nguồn Markdown sạch lên Google NotebookLM (ADR 0023)",
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
        help="Chỉ in manifest danh mục nguồn, không gọi API",
    )

    # Command: audit
    subparsers.add_parser(
        "audit",
        help="Chạy kiểm toán pháp y toàn diện đối soát PDF Công báo gốc và Markdown",
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
        from scripts.verify_all_docs_against_pdf import main as run_pdf_audit

        code = run_pdf_audit()
        sys.exit(code)

    elif args.command == "ingest":
        target_bundle_dir = root_dir / "legal_docs" / args.category / args.slug
        sources_dir = target_bundle_dir / "sources"
        sources_dir.mkdir(parents=True, exist_ok=True)

        # Ensure docx is safely preserved in sources/ per ADR 0036 Invariant 4
        target_docx = sources_dir / f"{args.slug}.docx"
        if args.docx_path.resolve() != target_docx.resolve():
            shutil.copy2(args.docx_path, target_docx)
            input_docx = target_docx
        else:
            input_docx = args.docx_path

        res = convert_docx_to_okf_bundle(
            docx_path=input_docx,
            target_bundle_dir=target_bundle_dir,
            output_filename=f"{args.slug}.md",
            doc_type=args.doc_type,
        )
        print(f"\n[INGEST SUCCESSFUL]: {res}")

    elif args.command == "sync-notebooklm":
        import asyncio
        from scripts.sync_notebooklm_knowledge import execute_sync, get_canonical_manifest

        sources = get_canonical_manifest(root_dir)
        code = asyncio.run(execute_sync(args.notebook_id, sources, dry_run=args.dry_run))
        sys.exit(code)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()


