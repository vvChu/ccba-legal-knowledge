#!/usr/bin/env python3
"""Automated Verification Harness for /ccba-legal-intel (ccba-verify-legal-intel).

Implements the 5 Core Blocks according to ADR-0009, ADR-0044, ADR-0061 & Pstack Upstream:
1. Clean-Slate Pre-flight: Validates Python runtime, Spoke root, and ccba_legal package import.
2. Dual-Mode Process Lifecycle: Spawns CLI/pytest subprocesses in isolated process groups.
3. Deterministic Health Barrier: Verifies LegalKnowledgeEngine initialization and CLI readiness.
4. Evidence-Capture Test Suite: Runs contract smoke checks, CLI probes, and unit test suite.
5. Guaranteed Graceful Cleanup: Uses finally-block termination to eliminate zombie processes.
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
import threading
import time
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class LegalIntelVerificationHarness:
    """Deterministic Verification Harness for /ccba-legal-intel skill & engine."""

    def __init__(
        self,
        spoke_root: Path | None = None,
        mode: str = "full",
        evidence_out: Path | None = None,
        step_timeout: float = 300.0,
    ) -> None:
        """Initialize the /ccba-legal-intel verification harness.

        Args:
            spoke_root: Optional explicit Spoke root path.
            mode: Verification mode ('smoke', 'cli', 'unit', 'full').
            evidence_out: Optional path to output JSON evidence report.
            step_timeout: Timeout in seconds per subprocess step.
        """
        self.spoke_root = (spoke_root or self._discover_spoke_root()).resolve()
        self.hub_root = self._discover_hub_root()
        self.mode = mode.lower()
        self.evidence_out = (
            evidence_out.resolve()
            if evidence_out
            else self.spoke_root / ".md" / "reports" / "evidence_verify_legal_intel.json"
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
        sibling = (self.spoke_root.parent / "ccba-agent-platform").resolve()
        return sibling

    # =========================================================================
    # Block 1: Clean-Slate Pre-flight
    # =========================================================================
    def pre_flight_check(self) -> bool:
        """Verify runtime environment, Spoke corpus, and ccba_legal availability."""
        print("🔍 [Block 1] Clean-Slate Pre-flight: Checking /ccba-legal-intel environment...")
        if sys.version_info < (3, 10):
            print(f"❌ Python 3.10+ required. Found: {sys.version}", file=sys.stderr)
            return False

        registry_path = self.spoke_root / "legal_registry.yaml"
        skill_path = self.spoke_root / ".agents" / "skills" / "ccba-legal-intel" / "SKILL.md"
        if not registry_path.is_file() or not skill_path.is_file():
            print("❌ Missing legal_registry.yaml or ccba-legal-intel/SKILL.md.", file=sys.stderr)
            return False

        try:
            import ccba_legal  # noqa: F401
        except ImportError as exc:
            print(f"❌ Cannot import ccba_legal package: {exc}", file=sys.stderr)
            return False

        self.evidence_out.parent.mkdir(parents=True, exist_ok=True)
        print("  ✓ Runtime, ccba-legal-intel skill, and ccba_legal package verified.")
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
        """Perform fast deterministic readiness check on LegalKnowledgeEngine without sleep."""
        print("🛡️ [Block 3] Deterministic Health Barrier: Probing LegalKnowledgeEngine...")
        start_time = time.monotonic()
        try:
            from ccba_legal import LegalKnowledgeEngine

            engine = LegalKnowledgeEngine(
                registry_path=self.spoke_root / "legal_registry.yaml",
                corpus_dir=self.spoke_root / "legal_docs",
            )
            results = engine.search("Luật Xây dựng", top_k=3)
            if not results:
                print("❌ Health Barrier failed: Engine search returned empty list.", file=sys.stderr)
                return False
        except Exception as exc:
            print(f"❌ Health Barrier exception: {exc}", file=sys.stderr)
            return False

        elapsed = time.monotonic() - start_time
        print(f"  ✓ LegalKnowledgeEngine ready in {elapsed:.3f}s ({len(results)} probe hits).")
        return True

    # =========================================================================
    # Block 4: Evidence-Capture Test Suite
    # =========================================================================
    def _run_in_memory_contract_checks(self) -> tuple[bool, str]:
        """Verify core Deep Seam contracts of /ccba-legal-intel in-process."""
        from ccba_legal import LegalKnowledgeEngine
        from ccba_legal.lexicon import parse_national_construction_id

        engine = LegalKnowledgeEngine(
            registry_path=self.spoke_root / "legal_registry.yaml",
            corpus_dir=self.spoke_root / "legal_docs",
        )
        hits = engine.search("Luật Xây dựng", top_k=3)
        if not hits or len(hits) > 3:
            return False, f"FEAT-INT-001 failed: expected 1..3 hits, got {len(hits)}"

        clause_res = engine.get_clause("Luat-Xay-dung-2025-135-2025-QH15", "d1")
        clause_txt = clause_res.get("content", "") if isinstance(clause_res, dict) else str(clause_res)
        if "Phạm vi điều chỉnh" not in clause_txt:
            return False, "FEAT-INT-002 failed: Clause d1 missing 'Phạm vi điều chỉnh'"

        try:
            engine.find_bundle_dir("../../etc/passwd")
            return False, "FEAT-INT-002 failed: CWE-22 path traversal was not blocked!"
        except ValueError:
            pass

        table_res = engine.get_table("qcvn_06_2022_bxd", "bang_01", format="markdown")
        table_md = table_res.get("content", "") if isinstance(table_res, dict) else str(table_res)
        if "Tường ngăn cháy" not in table_md or "REI 150" not in table_md:
            return False, "FEAT-INT-003 failed: Table bang_01 missing expected cells"

        parsed_id = parse_national_construction_id("012511153271")
        if not parsed_id.is_valid or parsed_id.province_code != "01" or parsed_id.kind != "PLANNING":
            return False, "FEAT-INT-004 failed: National Construction ID parser mismatch"

        return True, "All 4 in-memory Deep Seam contracts (Search, Clause+CWE22, Table, Lexicon) PASSED."

    def _build_subprocess_steps(self) -> list[tuple[str, list[str], Path]]:
        """Assemble subprocess verification steps based on selected mode."""
        steps: list[tuple[str, list[str], Path]] = []
        if self.mode in ("cli", "full"):
            steps.extend(
                [
                    (
                        "CLI Query Seam (FEAT-INT-001)",
                        [sys.executable, "-m", "ccba_legal", "query", "Luật Xây dựng"],
                        self.spoke_root,
                    ),
                    (
                        "CLI Get-Clause Seam (FEAT-INT-002)",
                        [
                            sys.executable,
                            "-m",
                            "ccba_legal",
                            "get-clause",
                            "--doc",
                            "Luat-Xay-dung-2025-135-2025-QH15",
                            "--clause",
                            "d1",
                        ],
                        self.spoke_root,
                    ),
                    (
                        "CLI Get-Table Seam (FEAT-INT-003)",
                        [
                            sys.executable,
                            "-m",
                            "ccba_legal",
                            "get-table",
                            "--doc",
                            "qcvn_06_2022_bxd",
                            "--table",
                            "bang_01",
                            "--format",
                            "markdown",
                        ],
                        self.spoke_root,
                    ),
                ]
            )
        if self.mode in ("unit", "full"):
            pkg_tests = self.hub_root / "packages" / "ccba-legal-intel" / "tests"
            if pkg_tests.is_dir():
                target_files = [
                    str(pkg_tests / "test_legal_knowledge_engine.py"),
                    str(pkg_tests / "test_cli_doc_parity.py"),
                    str(pkg_tests / "test_lexicon_harvester.py"),
                    str(pkg_tests / "test_legal_to_pptx_seam.py"),
                    str(pkg_tests / "test_sync_spoke.py"),
                ]
                steps.append(
                    (
                        "Package Unit Test Suite (FEAT-INT-001..005)",
                        [sys.executable, "-m", "pytest", *target_files, "-q"],
                        self.hub_root,
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
        timed_out = threading.Event()

        def _on_timeout() -> None:
            if not timed_out.is_set():
                timed_out.set()
                print(
                    f"\n❌ [TIMEOUT] {label} timed out after {self.step_timeout}s!",
                    file=sys.stderr,
                )
                self.cleanup()

        timer = threading.Timer(self.step_timeout, _on_timeout)
        timer.daemon = True
        timer.start()
        try:
            if proc.stdout:
                for line in proc.stdout:
                    output_lines.append(line)
                    sys.stdout.write(line)
                    sys.stdout.flush()
            remaining = max(0.0, self.step_timeout - (time.monotonic() - step_start))
            proc.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            _on_timeout()
        finally:
            timer.cancel()

        exit_code = (
            124
            if timed_out.is_set()
            else (proc.returncode if proc.returncode is not None else 124)
        )

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
            print(f"{'✅' if passed else '❌'} [In-Memory Seam Contracts] {msg} ({dt:.3f}s)")
            executed_steps.append(
                {
                    "label": "In-Memory Seam Contracts (FEAT-INT-001..004)",
                    "command": "in_memory_contract_checks",
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
            "skill": "ccba-verify-legal-intel",
            "target_skill": "ccba-legal-intel",
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
                    try:
                        self.active_process.wait(timeout=5.0)
                    except subprocess.TimeoutExpired:
                        if self.active_process.poll() is None:
                            os.killpg(pgid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                pass
            finally:
                self.active_process = None


def main() -> None:
    """CLI entrypoint for ccba-verify-legal-intel verification harness."""
    parser = argparse.ArgumentParser(
        description="Deterministic Verification Harness for /ccba-legal-intel"
    )
    parser.add_argument(
        "--mode",
        choices=["smoke", "cli", "unit", "full"],
        default="full",
        help="Verification mode: smoke (fast in-memory contracts), cli (CLI subcommands), unit (package pytest), full (all)",
    )
    parser.add_argument("--evidence-out", type=Path, default=None, help="Output JSON path")
    parser.add_argument("--step-timeout", type=float, default=300.0, help="Step timeout (s)")
    args = parser.parse_args()

    harness = LegalIntelVerificationHarness(
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
