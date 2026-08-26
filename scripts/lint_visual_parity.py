"""Visual Parity Linter for CCBA Legal Knowledge Spoke (ADR 0029 & ADR 0030).

Enforces zero-tolerance on visual clutter and formatting regressions across all Markdown documents
by delegating to Hub Deep Seam `ccba_legal.visual_parity`.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Enforce UTF-8 output encoding for Windows PowerShell
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from ccba_legal import lint_document
except ImportError:
    from ccba_legal.visual_parity import lint_document


def main() -> int:
    print("=================================================================")
    print("       CCBA LEGAL SPOKE VISUAL PARITY & LINTER GATE              ")
    print("=================================================================")

    workspace_root = Path(__file__).resolve().parent.parent
    legal_docs_dir = workspace_root / "legal_docs"

    total_files = 0
    total_errors = 0

    md_files = sorted(legal_docs_dir.rglob("*.md"))
    for md_file in md_files:
        total_files += 1
        rel_path = md_file.relative_to(workspace_root)
        errs = lint_document(md_file)
        if errs:
            print(f"❌ [FAIL] {rel_path} ({len(errs)} issues):")
            for e in errs[:5]:
                print(f"   - {e}")
            if len(errs) > 5:
                print(f"   ... and {len(errs) - 5} more issues.")
            total_errors += len(errs)

    print("-----------------------------------------------------------------")
    print(f"Scanned files : {total_files}")
    print(f"Total errors  : {total_errors}")
    print("-----------------------------------------------------------------")

    if total_errors == 0:
        print("✅ PASSED: 100% Visual Parity & Zero Formatting Clutter!")
        return 0
    else:
        print("❌ FAILED: Please fix visual formatting errors listed above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
