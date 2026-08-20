"""CCBA Legal Knowledge Spoke — Visual & Footnote Parity CI Gate (Gate 4).

Audits all Markdown documents in legal_docs/ for:
1. Double bullets (- -  or * * ).
2. Trapped table footnotes inside table cells (| _1) ... |).
3. Concatenated inline dashes inside notes (: - ...; - ...).
4. Raw unformatted table superscripts (REI 60 1) instead of <sup>1)</sup>).
5. Consecutive/redundant _CHÚ THÍCH:_ headers.
6. Unbulleted technical classification codes (LT, BC, SK, ĐT, K0..3).
"""

import sys
import re
from pathlib import Path

# Enforce UTF-8 output encoding for Windows PowerShell compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def audit_visual_parity(legal_docs_root: Path = Path("legal_docs")) -> int:
    all_md_files = sorted(list(legal_docs_root.rglob("*.md")))
    critical_issues = []
    warning_issues = []

    for md_path in all_md_files:
        if md_path.name in ("index.md", "dead_ends.md", "log.md", "README.md"):
            continue

        rel_path = md_path.relative_to(legal_docs_root)
        content = md_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        # 1. Check double bullets
        for idx, l in enumerate(lines, 1):
            if re.match(r"^\s*[-*]\s+[-*]\s+", l):
                critical_issues.append(f"[{rel_path}:L{idx}] DOUBLE_BULLET: {l.strip()}")

        # 2. Check consecutive _CHÚ THÍCH:_ headers
        for idx, l in enumerate(lines, 1):
            if l.strip() == "_CHÚ THÍCH:_" and idx < len(lines):
                next_lines = [lines[j].strip() for j in range(idx, min(len(lines), idx+3)) if lines[j].strip()]
                if len(next_lines) > 1 and next_lines[1] == "_CHÚ THÍCH:_":
                    critical_issues.append(f"[{rel_path}:L{idx}] DUPLICATE_NOTE_HEADER: Consecutive _CHÚ THÍCH:_")

        # 3. Check trapped table footnotes in table rows
        for idx, l in enumerate(lines, 1):
            if l.startswith("|") and re.search(r"\|\s*(_[1-9]\)|_CHÚ THÍCH|_GHI CHÚ|_Đối với)", l):
                critical_issues.append(f"[{rel_path}:L{idx}] TRAPPED_TABLE_FOOTNOTE: {l.strip()[:70]}...")

        # 4. Check concatenated inline dashes inside notes
        for idx, l in enumerate(lines, 1):
            stripped = l.strip()
            if re.search(r"(?:như sau|điều kiện sau|sau đây|bao gồm):\s*-\s+.*?[;.]\s*-\s+", stripped, re.IGNORECASE):
                critical_issues.append(f"[{rel_path}:L{idx}] CONCATENATED_INLINE_DASHES: {stripped[:80]}...")

        # 5. Check for unformatted in-table superscripts (e.g. REI 60 1) )
        in_table = False
        for idx, l in enumerate(lines, 1):
            stripped = l.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                in_table = True
                raw_sup = re.findall(r"\b([A-Z]{1,4}\s*\d+|\d+)\s+([1-9]\))(?!\<|/sup)", stripped)
                if raw_sup:
                    critical_issues.append(f"[{rel_path}:L{idx}] RAW_TABLE_SUPERSCRIPT: {raw_sup} in {stripped[:60]}...")
            else:
                in_table = False

        # 6. Check for unbulleted standard classification codes (LT1..4, BC1..3, SK1..3, ĐT1..4, K0..3)
        for idx, l in enumerate(lines, 1):
            st = l.strip()
            if re.match(r"^(LT[1-4]|BC[1-3]|SK[1-3]|ĐT[1-4]|Ch[1-4]|K[0-3])\s+\(", st):
                critical_issues.append(f"[{rel_path}:L{idx}] UNBULLETED_CLASSIFICATION: {st[:50]}")

    print("=================================================================")
    print("   CCBA VISUAL & FOOTNOTE PARITY AUDIT GATE (GATE 4)             ")
    print("=================================================================")
    print(f"Total Markdown Files Audited: {len(all_md_files)}")
    print(f"Critical Formatting Errors  : {len(critical_issues)}")
    print(f"Format Warnings             : {len(warning_issues)}")
    print("-----------------------------------------------------------------")

    if critical_issues:
        print("❌ FAILED: The following visual parity errors must be resolved:\n")
        for err in critical_issues[:25]:
            print(f"  -> {err}")
        if len(critical_issues) > 25:
            print(f"  ... and {len(critical_issues) - 25} more errors.")
        return 1

    print("✅ PASSED: 100% Visual Parity, Clean Lists & Footnotes Verified!")
    print("=================================================================\n")
    return 0

if __name__ == "__main__":
    sys.exit(audit_visual_parity())
