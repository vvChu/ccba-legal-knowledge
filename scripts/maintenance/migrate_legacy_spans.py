#!/usr/bin/env python3
"""Batch Migration Tool for AST Clauses Spans and QA Benchmarks.

Upgrades legacy single-line AST spans to multi-line spans (line_start < line_end)
across legal bundles and generates ground-truth QA benchmarks using
ccba_legal.gold_standard.ast_qa_generator.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

# Ensure project root in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from ccba_legal import generate_bundle_ast_and_qa
except ImportError as exc:
    print(f"[Error] Failed to import ccba_legal: {exc}")
    print("Please run within the activated virtualenv (.venv) linked to Hub packages.")
    sys.exit(1)


def migrate_bundle(bundle_dir: Path) -> dict[str, Any]:
    """Migrate a single bundle to multi-line AST spans and QA benchmark."""
    meta_file = bundle_dir / "metadata.yaml"
    title: str | None = None
    cong_bao: str | None = None
    if meta_file.exists():
        try:
            m = yaml.safe_load(meta_file.read_text(encoding="utf-8"))
            if isinstance(m, dict):
                title = m.get("title")
                cong_bao = m.get("cong_bao_number")
        except Exception:
            pass

    clauses, qa_list = generate_bundle_ast_and_qa(
        bundle_dir=bundle_dir,
        doc_title=title,
        cong_bao_number=cong_bao,
    )

    bad_spans = 0
    for c in clauses:
        ls = c.get("line_start")
        le = c.get("line_end")
        if ls is None or le is None or ls >= le:
            bad_spans += 1

    return {
        "slug": bundle_dir.name,
        "clauses_count": len(clauses),
        "qa_count": len(qa_list),
        "bad_spans": bad_spans,
        "title": title or bundle_dir.name,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate legacy AST spans to multi-line spans across OKF bundles."
    )
    parser.add_argument(
        "--category",
        default="01_vbpl",
        help="Target category directory under legal_docs/ (default: 01_vbpl)",
    )
    parser.add_argument(
        "--bundle",
        default=None,
        help="Specific bundle slug to migrate (default: all bundles in category)",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check span validity without regenerating",
    )
    args = parser.parse_args()

    category_dir = ROOT_DIR / "legal_docs" / args.category
    if not category_dir.exists():
        print(f"[Error] Category directory not found: {category_dir}")
        return 1

    bundles: list[Path] = []
    if args.bundle:
        b_path = category_dir / args.bundle
        if not b_path.exists():
            print(f"[Error] Bundle not found: {b_path}")
            return 1
        bundles = [b_path]
    else:
        bundles = sorted(
            p for p in category_dir.iterdir() if p.is_dir() and not p.name.startswith(".")
        )

    print("=================================================================")
    print("      CCBA LEGAL KNOWLEDGE — BATCH SPAN & QA MIGRATION TOOL      ")
    print("=================================================================")
    print(f"Target Directory: {category_dir}")
    print(f"Total Bundles   : {len(bundles)}")
    print(f"Mode            : {'VALIDATE ONLY' if args.check_only else 'REGENERATE & VALIDATE'}")
    print("-----------------------------------------------------------------")

    total_clauses = 0
    total_qa = 0
    total_bad = 0

    for idx, b in enumerate(bundles, start=1):
        if args.check_only:
            c_file = b / "clauses.json"
            q_file = b / "qa_benchmark.json"
            if not c_file.exists():
                print(f"[{idx:02d}/{len(bundles):02d}] ❌ {b.name}: missing clauses.json")
                total_bad += 1
                continue
            data = json.loads(c_file.read_text(encoding="utf-8"))
            clauses = data if isinstance(data, list) else data.get("clauses", [])
            bad = sum(1 for c in clauses if c.get("line_start", 0) >= c.get("line_end", 0))
            qa_c = 0
            if q_file.exists():
                qd = json.loads(q_file.read_text(encoding="utf-8"))
                qa_c = len(qd if isinstance(qd, list) else qd.get("questions", []))
            total_clauses += len(clauses)
            total_qa += qa_c
            total_bad += bad
            status = "✅ PASS" if bad == 0 else f"❌ {bad} BAD SPANS"
            print(f"[{idx:02d}/{len(bundles):02d}] {status} | {b.name:<36} | {len(clauses):4d} clauses | {qa_c:4d} QA")
        else:
            res = migrate_bundle(b)
            total_clauses += res["clauses_count"]
            total_qa += res["qa_count"]
            total_bad += res["bad_spans"]
            status = "✅ DONE" if res["bad_spans"] == 0 else f"❌ {res['bad_spans']} BAD SPANS"
            print(
                f"[{idx:02d}/{len(bundles):02d}] {status} | {res['slug']:<36} | "
                f"{res['clauses_count']:4d} clauses | {res['qa_count']:4d} QA"
            )

    print("-----------------------------------------------------------------")
    print(f"SUMMARY: Bundles: {len(bundles)} | Total Clauses: {total_clauses:,} | Total QA: {total_qa:,} | Bad Spans: {total_bad}")
    print("=================================================================")

    if total_bad > 0:
        print(f"\n[FAILED]: Encountered {total_bad} clauses with line_start >= line_end!")
        return 1

    print("\n✅ SUCCESS: 100% of clauses have multi-line spans (line_start < line_end)!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
