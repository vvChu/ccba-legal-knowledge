"""CLI Interface for CCBA Legislative Consolidator (delegates to Hub SDK)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ccba_legal.consolidator import LegislativeConsolidator


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="CCBA Legislative Consolidator — Automated OKF v2.0 Legal Document Patching & VBHN Engine."
    )
    parser.add_argument(
        "--manifest",
        "-m",
        required=True,
        help="Path to patch_manifest.yaml",
    )
    parser.add_argument(
        "--base",
        "-b",
        required=True,
        help="Path to base legal document Markdown file (*.md)",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output directory for generated OKF v2.0 artifacts",
    )
    parser.add_argument(
        "--amending",
        "-a",
        default=None,
        help="Optional path to amending document Markdown file (*.md) for content extraction",
    )

    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    base_path = Path(args.base)
    output_dir = Path(args.output)
    amending_path = Path(args.amending) if args.amending else None

    print("=================================================================")
    print("        CCBA LEGISLATIVE CONSOLIDATOR (Hub SDK Engine)          ")
    print("=================================================================")
    print(f"📄 Manifest: {manifest_path}")
    print(f"📄 Base Document: {base_path}")
    print(f"📁 Output Directory: {output_dir}")
    if amending_path:
        print(f"📄 Amending Document: {amending_path}")
    print("-----------------------------------------------------------------")

    consolidator = LegislativeConsolidator.from_manifest_file(manifest_path)
    result = consolidator.consolidate(
        base_md_path=base_path,
        output_dir=output_dir,
        amending_md_path=amending_path,
    )

    print(f"Consolidation Status: {result.status}")
    print(f"Target Bundle: {result.bundle_dir}")
    print(f"Patches Applied: {len(result.patches_applied)}")
    if result.errors:
        print(f"Errors: {result.errors}")
        sys.exit(1)

    print("✅ Consolidation completed successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()
