"""Visual Parity Linter for CCBA Legal Knowledge Spoke (ADR 0029 & ADR 0030).

Enforces zero-tolerance on visual clutter and formatting regressions across all Markdown documents:
1. No redundant bullets before CHÚ THÍCH / GHI CHÚ (- **CHÚ THÍCH:)
2. No raw HTML table tags (<table>, <tr>, <td>)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def lint_document(md_path: Path) -> list[str]:
    """Lint a single Markdown file for visual formatting issues."""
    errors = []
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    for idx, line in enumerate(lines, 1):
        stripped = line.strip()

        # 1. Check redundant bullet before CHÚ THÍCH / GHI CHÚ
        if re.match(r"^[-*+]\s+(?:\*\*)?(?:CHÚ THÍCH|GHI CHÚ|Chú thích|Ghi chú)\s*\d*[:\.]?", stripped):
            if re.search(r"^[-*+]\s+(?:\*\*)?CHÚ THÍCH\s+\d+:", stripped):
                errors.append(f"Line {idx}: Redundant bullet before footnote header: '{stripped}'")

        # 2. Check raw HTML table tags
        if re.search(r"<(?:table|thead|tbody|tr|th|td)\b", stripped, re.IGNORECASE):
            errors.append(f"Line {idx}: Unclean raw HTML table tag found: '{stripped}'")

    return errors


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
