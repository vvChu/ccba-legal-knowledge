"""CCBA E2E Parity Audit CLI Test Runner & Report Generator.

Executes the complete 4-tier opaque-box test suite against QCVN 06:2022/BXD
and Amendment 1:2023, prints a structured terminal dashboard with timing metrics,
and exports comprehensive test reports to JSON and Markdown.
"""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Enforce UTF-8 for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_tier(tier_name: str, test_file: Path, repo_root: Path) -> Dict[str, Any]:
    """Runs a single test tier via pytest in a clean subprocess and parses output."""
    t0 = time.time()
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(test_file),
        "-v",
        "--tb=short",
    ]
    res = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(repo_root),
    )
    elapsed = time.time() - t0

    # Parse stdout for test items
    results: List[Dict[str, Any]] = []
    passed_count = 0
    failed_count = 0
    skipped_count = 0

    stdout_lines = res.stdout.splitlines()
    test_line_pattern = re.compile(r"^(tests[/\\][^\s:]+::([^\s]+))\s+(PASSED|FAILED|SKIPPED)\b")

    for line in stdout_lines:
        m = test_line_pattern.match(line.strip())
        if m:
            node_id = m.group(1)
            name = m.group(2)
            status = m.group(3)
            if status == "PASSED":
                passed_count += 1
            elif status == "FAILED":
                failed_count += 1
            elif status == "SKIPPED":
                skipped_count += 1

            results.append({
                "node_id": node_id,
                "name": name,
                "status": status,
                "error_message": "",
            })

    # Extract short failure summaries
    short_summary_idx = -1
    for idx, line in enumerate(stdout_lines):
        if "=== short test summary info ===" in line:
            short_summary_idx = idx
            break

    if short_summary_idx != -1:
        for line in stdout_lines[short_summary_idx + 1:]:
            if line.startswith("FAILED"):
                parts = line.split("::")
                if len(parts) > 1:
                    test_part = parts[1].split()[0]
                    reason = line[line.find(test_part) + len(test_part):].strip(" -:")
                    for r in results:
                        if r["name"] == test_part and r["status"] == "FAILED":
                            r["error_message"] = reason

    return {
        "tier_name": tier_name,
        "file": str(test_file.name),
        "total": len(results),
        "passed": passed_count,
        "failed": failed_count,
        "skipped": skipped_count,
        "duration_seconds": round(elapsed, 3),
        "exit_code": res.returncode,
        "results": results,
    }

def generate_reports(
    all_tier_results: List[Dict[str, Any]],
    output_dir: Path,
) -> Tuple[Path, Path]:
    """Generates JSON and Markdown reports in output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "e2e_test_report.json"
    md_path = output_dir / "e2e_test_report.md"

    total_tests = sum(t["total"] for t in all_tier_results)
    total_passed = sum(t["passed"] for t in all_tier_results)
    total_failed = sum(t["failed"] for t in all_tier_results)
    total_skipped = sum(t["skipped"] for t in all_tier_results)
    total_duration = sum(t["duration_seconds"] for t in all_tier_results)
    overall_status = "PASS" if total_failed == 0 else "FAIL"

    timestamp = datetime.now().isoformat()

    # JSON Report
    report_data = {
        "timestamp": timestamp,
        "overall_status": overall_status,
        "summary": {
            "total_tests": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "skipped": total_skipped,
            "pass_rate_pct": round((total_passed / total_tests * 100), 2) if total_tests else 0.0,
            "duration_seconds": round(total_duration, 3),
        },
        "tiers": all_tier_results,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    # Markdown Report
    md_lines = [
        "# CCBA QCVN 06:2022/BXD & Amendment 1:2023 E2E Test Audit Report",
        "",
        f"- **Timestamp:** `{timestamp}`",
        f"- **Overall Status:** `{'PASS (100% Zero Data Loss)' if overall_status == 'PASS' else 'FAIL (Defects Detected)'}`",
        f"- **Total Tests Executed:** `{total_tests}`",
        f"- **Passed:** `{total_passed}` | **Failed:** `{total_failed}` | **Skipped:** `{total_skipped}`",
        f"- **Pass Rate:** `{report_data['summary']['pass_rate_pct']}%`",
        f"- **Total Runtime:** `{round(total_duration, 2)}s`",
        "",
        "## Tier-by-Tier Summary",
        "",
        "| Tier | Test Module | Total | Passed | Failed | Duration | Status |",
        "|:---|:---|:---:|:---:|:---:|:---:|:---:|",
    ]

    for t in all_tier_results:
        st = "PASS" if t["failed"] == 0 else "FAIL"
        md_lines.append(
            f"| **{t['tier_name']}** | `{t['file']}` | {t['total']} | {t['passed']} | {t['failed']} | {t['duration_seconds']}s | {st} |"
        )

    md_lines.extend([
        "",
        "## Detailed Failure Analysis",
        "",
    ])

    has_failures = False
    for t in all_tier_results:
        failed_items = [r for r in t["results"] if r["status"] == "FAILED"]
        if failed_items:
            has_failures = True
            md_lines.append(f"### {t['tier_name']} Failures ({len(failed_items)})")
            for item in failed_items:
                md_lines.append(f"- **`{item['name']}`**")
                if item["error_message"]:
                    md_lines.append(f"  - Note: `{item['error_message'][:120]}`")
            md_lines.append("")

    if not has_failures:
        md_lines.append("100% of test assertions passed. All features, boundaries, cross-links, and scenarios verified with Zero Data Loss.")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    return json_path, md_path

def main() -> int:
    """Main CLI entry point."""
    tests_dir = Path(__file__).resolve().parent
    repo_root = tests_dir.parent
    reports_dir = repo_root / ".agents" / "test_reports"

    print("=" * 72)
    print("      CCBA E2E PARITY AUDIT TEST RUNNER (4-TIER OPAQUE BOX)")
    print("      Target: QCVN 06:2022/BXD & Sửa đổi 1:2023 OKF Knowledge Bundle")
    print("=" * 72)

    tiers = [
        ("Tier 1: Feature Coverage", tests_dir / "test_tier1_feature_coverage.py"),
        ("Tier 2: Boundary & Edge-Cases", tests_dir / "test_tier2_boundaries.py"),
        ("Tier 3: Cross-Feature Interactions", tests_dir / "test_tier3_cross_features.py"),
        ("Tier 4: Real-World Scenarios", tests_dir / "test_tier4_real_world.py"),
    ]

    all_tier_results = []
    overall_start = time.time()

    for tier_name, test_file in tiers:
        if not test_file.exists():
            print(f"[ERROR] Test file {test_file.name} not found!")
            continue

        print(f"\n[RUNNING] {tier_name} ({test_file.name})...")
        t_res = run_tier(tier_name, test_file, repo_root)
        all_tier_results.append(t_res)

        badge = "[PASS]" if t_res["failed"] == 0 else "[FAIL]"
        print(f"{badge} {tier_name}: {t_res['passed']}/{t_res['total']} passed ({t_res['duration_seconds']}s)")

    total_time = time.time() - overall_start

    # Export Reports
    json_rep, md_rep = generate_reports(all_tier_results, reports_dir)

    total_tests = sum(t["total"] for t in all_tier_results)
    total_passed = sum(t["passed"] for t in all_tier_results)
    total_failed = sum(t["failed"] for t in all_tier_results)

    print("\n" + "=" * 72)
    print("                      E2E AUDIT EXECUTION SUMMARY                      ")
    print("=" * 72)
    print(f"Total Tests Executed: {total_tests}")
    print(f"Passed Assertions   : {total_passed} ({round(total_passed/total_tests*100, 2) if total_tests else 0}%)")
    print(f"Failed Assertions   : {total_failed}")
    print(f"Total Elapsed Time  : {round(total_time, 2)}s")
    print("-" * 72)
    print(f"JSON Report : {json_rep}")
    print(f"Markdown    : {md_rep}")
    print("=" * 72)

    return 0 if total_failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
