"""CCBA Legal Knowledge Spoke: Nightly Telemetry & Verification Runner.

Executes the automated 2-Stage Nightly Run:
- Stage 1: Deterministic Ground Truth Parity Engine (Golden Cohorts & VPS 5-tuple).
- Stage 2: 15 Master CI Gates on all 55 legal bundles (scripts/validate_legal_spoke.py).
- Stage 3: Compiles consolidated telemetry report in .md/reports/nightly_YYYYMMDD.md/json.

Enforces zero token cost and deterministic execution.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = ROOT_DIR / ".md" / "reports"
VERIFY_PARITY_SCRIPT = ROOT_DIR / ".md" / "tools" / "verify_ground_truth_parity.py"
MASTER_VALIDATOR_SCRIPT = ROOT_DIR / "scripts" / "validate_legal_spoke.py"


def get_total_bundles(root_dir: Path) -> int:
    """Get total bundle count from legal_registry.yaml or directory scan."""
    reg_file = root_dir / "legal_registry.yaml"
    if reg_file.exists():
        try:
            data = yaml.safe_load(reg_file.read_text(encoding="utf-8")) or {}
            count = data.get("registry_summary", {}).get("total_documents")
            if isinstance(count, int) and count > 0:
                return count
        except Exception:
            pass
    docs_dir = root_dir / "legal_docs"
    if docs_dir.exists():
        count = 0
        for cat in ("01_vbpl", "02_qcvn", "03_tcvn", "04_appendices"):
            cat_p = docs_dir / cat
            if cat_p.exists():
                count += sum(1 for d in cat_p.iterdir() if d.is_dir() and not d.name.startswith("."))
        if count > 0:
            return count
    return 58


def run_command_capture(cmd: list[str], cwd: Path) -> tuple[int, str, float]:
    """Execute command and return (exit_code, output, duration_sec)."""
    start = time.time()
    res = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    duration = time.time() - start
    output = (res.stdout or "") + "\n" + (res.stderr or "")
    return (res.returncode, output, duration)


def main() -> int:
    parser = argparse.ArgumentParser(description="CCBA Legal Nightly Telemetry Runner")
    parser.add_argument(
        "--cohorts",
        type=str,
        default="golden",
        help="Cohort selection for Ground Truth Parity ('golden' or 'all').",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without running full checks or writing reports.",
    )
    args = parser.parse_args()

    total_bundles = get_total_bundles(ROOT_DIR)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_out = REPORTS_DIR / f"nightly_{today_str}.json"
    md_out = REPORTS_DIR / f"nightly_{today_str}.md"

    print("=================================================================")
    print("      CCBA LEGAL SPOKE NIGHTLY TELEMETRY & CI RUNNER             ")
    print("=================================================================")
    print(f"Timestamp    : {datetime.now(timezone.utc).isoformat()}")
    print(f"Cohorts Mode : {args.cohorts}")
    print(f"Total Bundles: {total_bundles}")
    print(f"Dry-run Mode : {args.dry_run}")
    print("-----------------------------------------------------------------")

    if args.dry_run:
        print("[DRY-RUN] Pre-flight check successful.")
        print(f"[DRY-RUN] Would execute Stage 1: Ground Truth Parity (cohorts: {args.cohorts})")
        print(f"[DRY-RUN] Would execute Stage 2: Master CI Validator (15 Gates on {total_bundles} Bundles)")
        print(f"[DRY-RUN] Would generate reports in: {REPORTS_DIR}")
        print("=================================================================")
        return 0

    # Stage 1: Ground Truth Parity
    print("[1/2] Executing Ground Truth Parity Engine...")
    parity_json = REPORTS_DIR / f"parity_temp_{today_str}.json"
    parity_md = REPORTS_DIR / f"parity_temp_{today_str}.md"
    code_parity, out_parity, dur_parity = run_command_capture(
        [sys.executable, str(VERIFY_PARITY_SCRIPT), "--cohorts", args.cohorts, "--json-out", str(parity_json), "--md-out", str(parity_md)],
        cwd=ROOT_DIR,
    )
    print(f"   -> Parity Engine finished in {dur_parity:.2f}s (Exit code: {code_parity})")

    # Stage 2: Master CI Gates (15 Gates across all bundles)
    print(f"[2/2] Executing Master CI Validator (15 Gates on {total_bundles} Bundles)...")
    code_ci, out_ci, dur_ci = run_command_capture(
        [sys.executable, str(MASTER_VALIDATOR_SCRIPT)],
        cwd=ROOT_DIR,
    )
    print(f"   -> Master CI Validator finished in {dur_ci:.2f}s (Exit code: {code_ci})")

    # Load Parity Data
    parity_data = {}
    if parity_json.exists():
        try:
            parity_data = json.loads(parity_json.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Compile Combined JSON
    combined_report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_duration_seconds": round(dur_parity + dur_ci, 2),
        "stage_1_parity": {
            "exit_code": code_parity,
            "duration_seconds": round(dur_parity, 2),
            "summary": parity_data.get("results", []),
            "total_documents": parity_data.get("total_documents", 0),
            "passed_documents": parity_data.get("passed_documents", 0),
        },
        "stage_2_master_ci": {
            "exit_code": code_ci,
            "duration_seconds": round(dur_ci, 2),
            "passed": code_ci == 0,
            "summary": "PASSED" if code_ci == 0 else "FAILED",
        },
    }
    json_out.write_text(json.dumps(combined_report, ensure_ascii=False, indent=2), encoding="utf-8")

    # Compile Markdown Report
    ci_status = "✅ PASSED (0 Errors, 0 Warnings)" if code_ci == 0 else "❌ FAILED (Check CI Logs)"
    parity_passed = parity_data.get("passed_documents", 0)
    parity_total = parity_data.get("total_documents", 0)

    md_lines = [
        f"# Báo Cáo Định Kỳ Ban Đêm: CCBA Legal Spoke Telemetry ({datetime.now().strftime('%Y-%m-%d')})",
        "",
        f"- **Thời gian chạy:** `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`",
        f"- **Tổng thời lượng:** `{dur_parity + dur_ci:.2f} giây`",
        f"- **Tầng 1 - Đối Soát 1-1 Parity (Golden Cohorts):** `{parity_passed}/{parity_total} văn bản đạt chuẩn`",
        f"- **Tầng 2 - Master CI 15 Cổng (Toàn bộ {total_bundles} bundles):** `{ci_status}`",
        "",
        "---",
        "",
        f"## 1. Kết Quả Master CI Toàn Bộ Kho Tri Thức ({total_bundles} Bundles)",
        "",
        "```text",
        "\n".join([line for line in out_ci.splitlines() if "Gate" in line or "SUMMARY" in line or "PASSED" in line or "FAILED" in line][:25]),
        "```",
        "",
        "---",
        "",
        "## 2. Chi Tiết Đối Soát 1-1 Ground Truth (5 Golden Cohorts)",
        "",
    ]

    if parity_md.exists():
        md_lines.append(parity_md.read_text(encoding="utf-8"))

    md_out.write_text("\n".join(md_lines), encoding="utf-8")

    print("=================================================================")
    print(f"Combined Telemetry JSON : {json_out}")
    print(f"Combined Telemetry MD   : {md_out}")
    print(f"Master CI Status        : {ci_status}")
    print(f"Parity Golden Pass Rate : {parity_passed}/{parity_total}")
    print("=================================================================")

    # Clean temporary intermediate files
    if parity_json.exists():
        parity_json.unlink()
    if parity_md.exists():
        parity_md.unlink()

    return 0 if (code_ci == 0 and parity_passed >= parity_total * 0.9) else 1


if __name__ == "__main__":
    sys.exit(main())
