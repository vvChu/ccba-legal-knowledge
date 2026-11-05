#!/usr/bin/env python3
"""Automated Verification Harness for /ccba-legal-ingest & Coupled Legal Skills.

Covers:
- /ccba-legal-ingest (OpenXML Sanitizer, OKF v2.4 Packager, 2D Table/KaTeX/Visual Parity)
- /ccba-tvpl-vip-crawler (TVPLSessionMutex, CookieVault, 3-Tier Acquisition Seams)
- /ccba-legal-document-tracker (LegislativeConsolidator, VBHNEngine, DualModeASTParser)
- /ccba-legal-advisor (5-Ring Legal Graph Routing & DynamicStatutoryResolver Hard Floor Guard)

Implements the 5 Core Blocks according to ADR-0009, ADR-0044, ADR-0061 & Pstack Upstream.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class LegalIngestVerificationHarness:
    """Deterministic Verification Harness for /ccba-legal-ingest & coupled legal skills."""

    def __init__(
        self,
        spoke_root: Path | None = None,
        mode: str = "full",
        evidence_out: Path | None = None,
        step_timeout: float = 180.0,
    ) -> None:
        """Initialize the /ccba-legal-ingest verification harness.

        Args:
            spoke_root: Optional explicit Spoke root path.
            mode: Verification mode ('smoke', 'graph', 'unit', 'full').
            evidence_out: Optional path to output JSON evidence report.
            step_timeout: Timeout in seconds per subprocess step.
        """
        self.spoke_root = (spoke_root or self._discover_spoke_root()).resolve()
        self.hub_root = self._discover_hub_root()
        self.mode = mode.lower()
        self.evidence_out = (
            evidence_out.resolve()
            if evidence_out
            else self.spoke_root / ".md" / "reports" / "evidence_verify_legal_ingest.json"
        )
        self.active_process: subprocess.Popen[str] | None = None
        self.step_timeout = step_timeout
        self.is_win = sys.platform == "win32"

    @staticmethod
    def _discover_spoke_root() -> Path:
        """Walk up parents to discover the Spoke root containing legal_registry.yaml."""
        candidate = Path(__file__).resolve().parent
        while candidate != candidate.parent:
            if (candidate / "legal_registry.yaml").is_file():
                return candidate
            candidate = candidate.parent
        return Path(__file__).resolve().parents[4]

    def _discover_hub_root(self) -> Path:
        """Resolve Hub root from CCBA_HUB_PATH or sibling directory."""
        env_hub = os.environ.get("CCBA_HUB_PATH")
        if env_hub:
            resolved = (self.spoke_root / env_hub).resolve()
            if resolved.is_dir():
                return resolved
        return (self.spoke_root.parent / "ccba-agent-platform").resolve()

    # =========================================================================
    # Block 1: Clean-Slate Pre-flight
    # =========================================================================
    def pre_flight_check(self) -> bool:
        """Verify runtime environment, target SKILL.md files, and ccba_legal seams."""
        print("🔍 [Block 1] Clean-Slate Pre-flight: Checking /ccba-legal-ingest pipeline...")
        if sys.version_info < (3, 10):
            print(f"❌ Python 3.10+ required. Found: {sys.version}", file=sys.stderr)
            return False

        required_skills = (
            "ccba-legal-ingest",
            "ccba-tvpl-vip-crawler",
            "ccba-legal-document-tracker",
            "ccba-legal-advisor",
        )
        for s_name in required_skills:
            s_file = self.spoke_root / ".agents" / "skills" / s_name / "SKILL.md"
            if not s_file.is_file():
                print(f"❌ Missing required skill file: {s_file}", file=sys.stderr)
                return False

        try:
            import ccba_legal  # noqa: F401
        except ImportError as exc:
            print(f"❌ Cannot import ccba_legal package: {exc}", file=sys.stderr)
            return False

        self.evidence_out.parent.mkdir(parents=True, exist_ok=True)
        print("  ✓ Runtime, 4 coupled legal skills, and ccba_legal package verified.")
        return True

    # =========================================================================
    # Block 2: Dual-Mode Process Lifecycle
    # =========================================================================
    def _spawn_process_group(self, cmd: list[str], cwd: Path | None = None) -> subprocess.Popen[str]:
        """Spawn a child process inside an isolated OS process group."""
        kwargs: dict[str, Any] = {
            "cwd": str(cwd or self.spoke_root),
            "stdout": subprocess.PIPE,
            "stderr": subprocess.STDOUT,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
        }
        if self.is_win:
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            kwargs["preexec_fn"] = os.setsid

        proc: subprocess.Popen[str] = subprocess.Popen(cmd, **kwargs)
        self.active_process = proc
        return proc

    # =========================================================================
    # Block 3: Deterministic Health Barrier
    # =========================================================================
    def deterministic_health_barrier(self) -> bool:
        """Perform fast deterministic readiness check on Ingestion & Consolidation Seams."""
        print("🛡️ [Block 3] Deterministic Health Barrier: Probing Ingestion & VBHN Seams...")
        start_time = time.monotonic()
        try:
            from ccba_legal import (
                CURRENT_OKF_VERSION,
                STANDARD_COMPARTMENTS,
                DocxCanonicalSanitizer,
                DynamicStatutoryResolver,
                LegislativeConsolidator,
                OKFBundlePackager,
                TVPLSessionMutex,
                VBHNEngine,
                VisualParityAuditor,
            )

            _ = (
                DocxCanonicalSanitizer,
                DynamicStatutoryResolver,
                LegislativeConsolidator,
                OKFBundlePackager,
                TVPLSessionMutex,
                VBHNEngine,
                VisualParityAuditor,
            )
            if CURRENT_OKF_VERSION != "2.4" or len(STANDARD_COMPARTMENTS) < 4:
                print(f"❌ Invalid OKF version ({CURRENT_OKF_VERSION}) or compartments.", file=sys.stderr)
                return False
        except Exception as exc:
            print(f"❌ Health Barrier exception: {exc}", file=sys.stderr)
            return False

        elapsed = time.monotonic() - start_time
        print(f"  ✓ Ingestion, Sanitizer & VBHN Seams ready in {elapsed:.3f}s (OKF v{CURRENT_OKF_VERSION}).")
        return True

    # =========================================================================
    # Block 4: Evidence-Capture Test Suite
    # =========================================================================
    def _run_in_memory_contract_checks(self) -> tuple[bool, str]:
        """Verify 5 in-memory contracts across ingest, crawler, consolidator, and advisor."""
        from ccba_legal import (
            CURRENT_OKF_VERSION,
            DocxCanonicalSanitizer,
            DynamicStatutoryResolver,
            StatutoryRole,
            TVPLSessionMutex,
            VBHNEngine,
            lint_document,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # FEAT-ING-001: TVPLSessionMutex lock/unlock contract
            lock_p = tmp_path / "tvpl_test.lock"
            with TVPLSessionMutex(lock_path=lock_p, timeout=2):
                if not lock_p.exists():
                    return False, "FEAT-ING-001 failed: TVPLSessionMutex did not create lock file"

            # FEAT-ING-002: DocxCanonicalSanitizer & OKF v2.4 invariant
            sanitizer = DocxCanonicalSanitizer()
            if CURRENT_OKF_VERSION != "2.4" or not hasattr(sanitizer, "sanitize"):
                return False, "FEAT-ING-002 failed: DocxCanonicalSanitizer / OKF v2.4 broken"

            # FEAT-ING-003: VisualParityAuditor lint_document detects double bullet
            bad_md = tmp_path / "bad_visual.md"
            bad_md.write_text("- - Double bullet error\n", encoding="utf-8")
            if not lint_document(bad_md):
                return False, "FEAT-ING-003 failed: lint_document missed DOUBLE_BULLET"

        # FEAT-ING-004: VBHNEngine AST merge contract
        merged = VBHNEngine().merge_documents(
            base_doc="### Điều 1. Phạm vi\nNội dung gốc.",
            amending_doc='Sửa đổi Điều 1 như sau:\n"### Điều 1. Phạm vi\nNội dung sửa đổi."',
        )
        if not merged or not hasattr(merged, "content") or not hasattr(merged, "patch_summary"):
            return False, "FEAT-ING-004 failed: VBHNEngine merge_documents contract broken"

        # FEAT-ING-005: DynamicStatutoryResolver Hard-Floor Currency check
        info_135 = DynamicStatutoryResolver.resolve(
            StatutoryRole.CONSTRUCTION_LAW, registry_path=self.spoke_root / "legal_registry.yaml"
        )
        if not info_135 or info_135.doc_number != "135/2025/QH15" or "50/2014/QH13" not in info_135.supersedes:
            return False, "FEAT-ING-005 failed: DynamicStatutoryResolver CONSTRUCTION_LAW mismatch"

        return True, "All 5 in-memory contracts (Mutex, Sanitizer, VisualParity, VBHN, Currency) PASSED."

    def _build_subprocess_steps(self) -> list[tuple[str, list[str], Path]]:
        """Assemble subprocess steps for 5-Ring Graph CLI and pytest suites."""
        steps: list[tuple[str, list[str], Path]] = []
        if self.mode in ("graph", "full"):
            steps.append(
                (
                    "5-Ring Legal Graph Routing CLI (FEAT-ING-005)",
                    [
                        sys.executable,
                        "scripts/spoke_cli.py",
                        "graph",
                        "--doc",
                        "Luat-Xay-dung-2025-135-2025-QH15",
                        "--json",
                    ],
                    self.spoke_root,
                )
            )
        if self.mode in ("unit", "full"):
            pkg_tests = self.hub_root / "packages" / "ccba-legal-intel" / "tests"
            test_targets = [
                str(pkg_tests / "test_docx_sanitizer.py"),
                str(pkg_tests / "test_okf_bundle_v2.py"),
                str(pkg_tests / "test_consolidator.py"),
                str(pkg_tests / "test_vbhn_engine.py"),
                str(pkg_tests / "test_crawler_seam.py"),
                str(pkg_tests / "test_currency_resolver.py"),
                str(pkg_tests / "test_table_grid_engine.py"),
                str(pkg_tests / "test_visual_parity.py"),
                str(self.spoke_root / "tests" / "integration" / "test_consolidator.py"),
                str(self.spoke_root / "tests" / "integration" / "test_docx_converter.py"),
                str(self.spoke_root / "tests" / "integration" / "test_fetch_tvpl_doc.py"),
                str(self.spoke_root / "tests" / "integration" / "test_gold_standard_processor.py"),
                str(self.spoke_root / "tests" / "integration" / "test_modernize_annex_engine.py"),
                str(self.spoke_root / "tests" / "integration" / "test_validate_legal_spoke.py"),
            ]
            steps.append(
                (
                    "Ingest, Sanitizer, Consolidator & Spoke Integration Suite (90 tests)",
                    [sys.executable, "-m", "pytest", *test_targets, "-q"],
                    self.spoke_root,
                )
            )
        return steps

    def _execute_subprocess_step(
        self, label: str, cmd: list[str], cwd: Path
    ) -> dict[str, Any]:
        """Run a single subprocess step and return structured step execution metadata."""
        print(f"\n--- Running: {label} ---")
        step_start = time.monotonic()
        proc = self._spawn_process_group(cmd, cwd=cwd)
        output_lines: list[str] = []
        if proc.stdout:
            for line in proc.stdout:
                output_lines.append(line)
                sys.stdout.write(line)
                sys.stdout.flush()
        try:
            proc.wait(timeout=self.step_timeout)
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            print(f"\n❌ [TIMEOUT] {label} timed out after {self.step_timeout}s!", file=sys.stderr)
            self.cleanup()
            exit_code = 124

        duration = round(time.monotonic() - step_start, 3)
        self.active_process = None
        status_str = "PASSED" if exit_code == 0 else "FAILED"
        print(f"{'✅' if exit_code == 0 else '❌'} {label} {status_str} in {duration:.2f}s")
        return {
            "label": label,
            "command": " ".join(cmd),
            "exit_code": exit_code,
            "duration_seconds": duration,
            "status": status_str,
        }

    def run_suite(self) -> int:
        """Execute test suite based on selected mode and save JSON evidence report."""
        print(f"🚀 [Block 4] Evidence-Capture Test Suite: Running in mode '{self.mode}'...")
        start_monotonic = time.monotonic()
        executed_steps: list[dict[str, Any]] = []
        overall_exit_code = 0

        if self.mode in ("smoke", "full"):
            t0 = time.monotonic()
            passed, msg = self._run_in_memory_contract_checks()
            dt = round(time.monotonic() - t0, 3)
            print(f"{'✅' if passed else '❌'} [In-Memory Pipeline Contracts] {msg} ({dt:.3f}s)")
            executed_steps.append(
                {
                    "label": "In-Memory Pipeline Contracts (FEAT-ING-001..005)",
                    "command": "in_memory_pipeline_checks",
                    "exit_code": 0 if passed else 1,
                    "duration_seconds": dt,
                    "status": "PASSED" if passed else "FAILED",
                    "message": msg,
                }
            )
            if not passed:
                overall_exit_code = 1

        if overall_exit_code == 0:
            for label, cmd, cwd in self._build_subprocess_steps():
                step_res = self._execute_subprocess_step(label, cmd, cwd)
                executed_steps.append(step_res)
                if step_res["exit_code"] != 0:
                    overall_exit_code = step_res["exit_code"]
                    break

        self._write_evidence(overall_exit_code, time.monotonic() - start_monotonic, executed_steps)
        return overall_exit_code

    def _write_evidence(
        self, exit_code: int, total_duration: float, steps: list[dict[str, Any]]
    ) -> None:
        """Persist structured verification evidence JSON to .md/reports/."""
        evidence = {
            "schema_version": "1.0",
            "skill": "ccba-verify-legal-ingest",
            "target_skills": [
                "ccba-legal-ingest",
                "ccba-tvpl-vip-crawler",
                "ccba-legal-document-tracker",
                "ccba-legal-advisor",
            ],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mode": self.mode,
            "overall_status": "PASSED" if exit_code == 0 else "FAILED",
            "overall_exit_code": exit_code,
            "total_duration_seconds": round(total_duration, 3),
            "executed_steps": steps,
        }
        self.evidence_out.write_text(
            json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"\n📊 Evidence report saved to: {self.evidence_out}")

    # =========================================================================
    # Block 5: Guaranteed Graceful Cleanup
    # =========================================================================
    def cleanup(self) -> None:
        """Terminate any active child process tree inside the finally block."""
        if self.active_process is not None and self.active_process.poll() is None:
            pid = self.active_process.pid
            try:
                if self.is_win:
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(pid)],
                        check=False,
                        capture_output=True,
                    )
                else:
                    pgid = os.getpgid(pid)
                    os.killpg(pgid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError, OSError):
                pass
            finally:
                self.active_process = None


def main() -> None:
    """CLI entrypoint for ccba-verify-legal-ingest verification harness."""
    parser = argparse.ArgumentParser(
        description="Deterministic Verification Harness for /ccba-legal-ingest & Coupled Skills"
    )
    parser.add_argument(
        "--mode",
        choices=["smoke", "graph", "unit", "full"],
        default="full",
        help="Verification mode: smoke (fast in-memory contracts), graph (5-Ring CLI), unit (90 pytest tests), full (all)",
    )
    parser.add_argument("--evidence-out", type=Path, default=None, help="Output JSON path")
    parser.add_argument("--step-timeout", type=float, default=180.0, help="Step timeout (s)")
    args = parser.parse_args()

    harness = LegalIngestVerificationHarness(
        mode=args.mode,
        evidence_out=args.evidence_out,
        step_timeout=args.step_timeout,
    )
    exit_code = 1
    try:
        if not harness.pre_flight_check():
            sys.exit(1)
        if not harness.deterministic_health_barrier():
            sys.exit(1)
        exit_code = harness.run_suite()
    except KeyboardInterrupt:
        exit_code = 130
    finally:
        harness.cleanup()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
