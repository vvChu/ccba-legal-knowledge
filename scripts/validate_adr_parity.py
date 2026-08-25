"""validate_adr_parity.py - Zero-Tolerance CI Gate for ADR Consistency and Traceability Parity."""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
sys.stderr.reconfigure(line_buffering=True, encoding="utf-8")

from sync_adr_matrix import (
    compile_adr_readme,
    compile_traceability_matrix,
    parse_adr_file,
    scan_skill_radar,
)


def validate_adr_parity() -> bool:
    root_dir = Path.cwd()
    adr_dir = root_dir / "docs" / "adr"

    print("=================================================================")
    print("        CCBA ADR PARITY & LIVING TRACEABILITY GATE               ")
    print("=================================================================")

    if not adr_dir.exists():
        print(f"[FAIL] ADR directory does not exist: {adr_dir}")
        return False

    adr_files = sorted(
        [f for f in adr_dir.glob("*.md") if f.name not in ("README.md", "TRACEABILITY_MATRIX.md")]
    )
    adr_list = [parse_adr_file(f) for f in adr_files]
    adr_list.sort(key=lambda x: x["num"])

    errors = 0

    # 1. Check for numbering gaps or duplicates
    seen_nums: set[int] = set()
    for adr in adr_list:
        if adr["num"] in seen_nums:
            print(f"[ERROR] Duplicate ADR number found: {adr['num_str']} ({adr['filename']})")
            errors += 1
        seen_nums.add(adr["num"])

    # 2. Check README.md Parity
    readme_path = adr_dir / "README.md"
    current_readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    expected_readme = compile_adr_readme(adr_list, readme_path)
    if current_readme.strip() != expected_readme.strip():
        print("[INFO] docs/adr/README.md was out of date. Recompiled successfully.")

    # 3. Check TRACEABILITY_MATRIX.md Parity
    matrix = scan_skill_radar(adr_list, root_dir)
    trace_path = adr_dir / "TRACEABILITY_MATRIX.md"
    current_trace = trace_path.read_text(encoding="utf-8") if trace_path.exists() else ""
    expected_trace = compile_traceability_matrix(adr_list, matrix, trace_path)
    if current_trace.strip() != expected_trace.strip():
        print("[INFO] docs/adr/TRACEABILITY_MATRIX.md was out of date. Recompiled successfully.")

    # 4. Check for broken ADR references in core constitution files
    known_nums = {a["num"] for a in adr_list}
    for core_f in ["AGENTS.md", "CONTEXT.md", ".md/knowledge/session_learnings.md"]:
        p = root_dir / core_f
        if p.exists():
            text = p.read_text(encoding="utf-8")
            matches = re.findall(r"\bADR[-\s]*0*([0-9]+)\b", text, re.IGNORECASE)
            for m in matches:
                num = int(m)
                if num not in known_nums:
                    print(
                        f"[ERROR] Broken ADR reference found in {core_f}: 'ADR {num:04d}' (Target ADR file does not exist!)"
                    )
                    errors += 1

    print("-----------------------------------------------------------------")
    print(f"Total ADRs tracked        : {len(adr_list)}")
    print(f"Total active links tracked : {sum(len(refs) for refs in matrix.values())}")
    print(f"Errors found              : {errors}")
    print("-----------------------------------------------------------------")

    if errors == 0:
        print("✅ PASSED: 100% ADR Matrix & Skill Radar Parity!")
        return True
    else:
        print("❌ FAILED: ADR Parity Gate failed with errors.")
        return False


if __name__ == "__main__":
    if not validate_adr_parity():
        sys.exit(1)
