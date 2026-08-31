#!/usr/bin/env python3
# Copyright (c) 2026 CCBA. All rights reserved.
"""Golden Snapshot & Regression Test Suite for OKF Legal Converters."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import yaml


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = WORKSPACE_ROOT / ".md" / "cache" / "golden_snapshots.json"


def compute_file_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    if not file_path.exists():
        return ""
    h = hashlib.sha256()
    h.update(file_path.read_bytes())
    return h.hexdigest()


def capture_doc_snapshot(bundle_dir: Path) -> dict[str, Any]:
    """Capture snapshot of an OKF legal bundle."""
    slug = bundle_dir.name
    md_file = bundle_dir / f"{slug}.md"
    clauses_file = bundle_dir / "clauses.json"
    qa_file = bundle_dir / "qa_benchmark.json"
    tables_file = bundle_dir / "tables" / "tables_catalog.json"
    figures_file = bundle_dir / "figures" / "figures_catalog.yaml"

    clauses_count = 0
    if clauses_file.exists():
        try:
            data = json.loads(clauses_file.read_text(encoding="utf-8"))
            clauses_count = len(data) if isinstance(data, list) else len(data.get("clauses", []))
        except Exception:
            pass

    tables_count = 0
    if tables_file.exists():
        try:
            t_data = json.loads(tables_file.read_text(encoding="utf-8"))
            tables_count = t_data.get("total_tables", len(t_data.get("tables", [])))
        except Exception:
            pass

    figures_count = 0
    if figures_file.exists():
        try:
            f_data = yaml.safe_load(figures_file.read_text(encoding="utf-8"))
            figures_count = len(f_data.get("figures", [])) if isinstance(f_data, dict) else len(f_data)
        except Exception:
            pass

    return {
        "slug": slug,
        "category": bundle_dir.parent.name,
        "md_sha256": compute_file_sha256(md_file),
        "md_lines": len(md_file.read_text(encoding="utf-8").splitlines()) if md_file.exists() else 0,
        "clauses_count": clauses_count,
        "tables_count": tables_count,
        "figures_count": figures_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Legal Knowledge Converter Regression Test Harness")
    parser.add_argument("--snapshot", action="store_true", help="Capture and save golden snapshot of all 35 bundles")
    parser.add_argument("--verify", action="store_true", help="Verify current bundles against saved snapshot")
    parser.add_argument("--doc", type=str, default="", help="Specific doc slug to verify")
    args = parser.parse_args()

    legal_docs = WORKSPACE_ROOT / "legal_docs"
    bundle_dirs = [p for p in legal_docs.glob("*/*") if p.is_dir() and not p.name.startswith(".")]

    if args.snapshot or not SNAPSHOT_PATH.exists():
        SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
        snapshots = {}
        for b in sorted(bundle_dirs):
            snapshots[b.name] = capture_doc_snapshot(b)
        SNAPSHOT_PATH.write_text(json.dumps(snapshots, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ Saved Golden Snapshot for {len(snapshots)} bundles at {SNAPSHOT_PATH}")
        return 0

    if args.verify:
        snapshots = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        targets = [b for b in bundle_dirs if not args.doc or b.name == args.doc]
        mismatches = 0

        print(f"\n🔍 Verifying {len(targets)} bundles against Golden Snapshot...")
        for b in sorted(targets):
            slug = b.name
            if slug not in snapshots:
                print(f"⚠️ [NEW BUNDLE] {slug} not found in snapshot!")
                continue

            current = capture_doc_snapshot(b)
            golden = snapshots[slug]

            diffs = []
            if current["md_sha256"] != golden["md_sha256"]:
                diffs.append(f"MD SHA-256 changed (lines: {golden['md_lines']} -> {current['md_lines']})")
            if current["clauses_count"] != golden["clauses_count"]:
                diffs.append(f"Clauses count changed ({golden['clauses_count']} -> {current['clauses_count']})")
            if current["tables_count"] != golden["tables_count"]:
                diffs.append(f"Tables count changed ({golden['tables_count']} -> {current['tables_count']})")
            if current["figures_count"] != golden["figures_count"]:
                diffs.append(f"Figures count changed ({golden['figures_count']} -> {current['figures_count']})")

            if diffs:
                print(f"❌ [MISMATCH] {slug}: {', '.join(diffs)}")
                mismatches += 1
            else:
                print(f"✅ [MATCH] {slug} (Lines: {current['md_lines']}, Clauses: {current['clauses_count']}, Tables: {current['tables_count']}, Figs: {current['figures_count']})")

        if mismatches > 0:
            print(f"\n❌ REGRESSION DETECTED: {mismatches} bundles differed from snapshot!")
            return 1
        print(f"\n🎉 100% REGRESSION-FREE: All {len(targets)} bundles perfectly match snapshot!")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
