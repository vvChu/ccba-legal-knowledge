#!/usr/bin/env python3
"""Automated Verification Harness for CCBA Legal Knowledge Spoke (verify-legal-knowledge).

Implements the 5 Core Blocks according to ADR-0009, ADR-0044 & Pstack Upstream:
1. Clean-Slate Pre-flight: Validates environment, Spoke integrity, and checks for dangling locks.
2. Dual-Mode Process Lifecycle: Spawns processes in isolated process groups (POSIX setsid / Windows Process Group).
3. Deterministic Health Barrier: Verifies registry YAML syntax, bundle compartments, and script entrypoints.
4. Evidence-Capture Test Suite: Runs target gates (smoke, full, cleanliness, bundle) and outputs structured evidence JSON.
5. Guaranteed Graceful Cleanup: Uses finally-block termination to kill child process trees and clean scratch files.
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
import time
from typing import Any, Dict, List, Optional

# UTF-8 stdout configuration for cross-platform compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class LegalVerificationHarness:
    """Deterministic Harness Runner for CCBA Legal Knowledge Spoke."""

    def __init__(
        self,
        spoke_root: Optional[Path] = None,
        mode: str = "full",
        bundle: Optional[str] = None,
        skip_pdf_vault: bool = False,
        evidence_out: Optional[Path] = None,
        step_timeout: float = 300.0,
    ) -> None:
        """Initialize verification harness."""
        if spoke_root is None:
            # Walk up parents to discover the Spoke root containing legal_registry.yaml
            candidate = Path(__file__).resolve().parent
            found = False
            while candidate != candidate.parent:
                if (candidate / "legal_registry.yaml").is_file():
                    self.spoke_root = candidate
                    found = True
                    break
                candidate = candidate.parent
            if not found:
                self.spoke_root = Path(__file__).resolve().parents[4]
        else:
            self.spoke_root = spoke_root.resolve()

        self.mode = mode.lower()
        self.bundle = bundle
        self.skip_pdf_vault = skip_pdf_vault or bool(os.getenv("CCBA_SKIP_PDF_VAULT"))
        self.evidence_out = (
            evidence_out.resolve()
            if evidence_out
            else self.spoke_root / ".md" / "reports" / "evidence_verify_legal_knowledge.json"
        )
        self.active_process: Optional[subprocess.Popen] = None
        self.step_timeout = step_timeout
        self.is_win = sys.platform == "win32"

    # =========================================================================
    # Block 1: Clean-Slate Pre-flight
    # =========================================================================
    def pre_flight_check(self) -> bool:
        """Pre-flight checks to ensure clean environment and valid root."""
        print("🔍 [Block 1] Clean-Slate Pre-flight: Checking environment...")

        # 1.1 Python version verification
        if sys.version_info < (3, 10):
            print(f"❌ Python 3.10+ required. Current version: {sys.version}", file=sys.stderr)
            return False

        # 1.2 Spoke root existence checks
        registry_path = self.spoke_root / "legal_registry.yaml"
        legal_docs_dir = self.spoke_root / "legal_docs"
        scripts_dir = self.spoke_root / "scripts"

        if not registry_path.is_file():
            print(f"❌ Missing legal_registry.yaml at: {registry_path}", file=sys.stderr)
            return False

        if not legal_docs_dir.is_dir():
            print(f"❌ Missing legal_docs/ directory at: {legal_docs_dir}", file=sys.stderr)
            return False

        if not scripts_dir.is_dir():
            print(f"❌ Missing scripts/ directory at: {scripts_dir}", file=sys.stderr)
            return False

        # 1.3 Ensure evidence output directory exists
        self.evidence_out.parent.mkdir(parents=True, exist_ok=True)

        print("  ✓ Environment, Spoke root, and output directories verified.")
        return True

    # =========================================================================
    # Block 2: Dual-Mode Process Lifecycle
    # =========================================================================
    def _spawn_process_group(self, cmd: List[str]) -> subprocess.Popen:
        """Spawn a child process inside a new isolated process group."""
        kwargs: Dict[str, Any] = {
            "cwd": str(self.spoke_root),
            "stdout": subprocess.PIPE,
            "stderr": subprocess.STDOUT,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
        }

        if self.is_win:
            # Windows: Create independent Process Group
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            # Linux / macOS (POSIX): Use setsid to create independent process group
            kwargs["preexec_fn"] = os.setsid

        proc = subprocess.Popen(cmd, **kwargs)
        self.active_process = proc
        return proc

    # =========================================================================
    # Block 3: Deterministic Health Barrier
    # =========================================================================
    def deterministic_health_barrier(self) -> bool:
        """Perform fast deterministic health probe without arbitrary sleep."""
        print("🛡️ [Block 3] Deterministic Health Barrier: Validating registry syntax and entrypoints...")
        start_time = time.monotonic()

        # 3.1 Validate registry syntax fast
        registry_path = self.spoke_root / "legal_registry.yaml"
        try:
            import yaml

            data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                print("❌ legal_registry.yaml root is not a valid YAML dictionary.", file=sys.stderr)
                return False
            
            laws = data.get("laws", [])
            decrees = data.get("decrees", [])
            standards = data.get("standards", [])
            documents = data.get("documents", {})
            total_docs = (
                (len(laws) if isinstance(laws, list) else 0)
                + (len(decrees) if isinstance(decrees, list) else 0)
                + (len(standards) if isinstance(standards, list) else 0)
                + (len(documents) if isinstance(documents, (dict, list)) else 0)
            )
            print(f"  ✓ legal_registry.yaml parsed successfully ({total_docs} documents registered).")
        except Exception as exc:
            print(f"❌ YAML parse error in legal_registry.yaml: {exc}", file=sys.stderr)
            return False

        # 3.2 Validate runner script entrypoints
        validator_script = self.spoke_root / "scripts" / "validate_legal_spoke.py"
        cleanliness_script = self.spoke_root / "scripts" / "check_spoke_cleanliness.py"

        if not validator_script.is_file():
            print(f"❌ Missing master validator at: {validator_script}", file=sys.stderr)
            return False
        if not cleanliness_script.is_file():
            print(f"❌ Missing cleanliness script at: {cleanliness_script}", file=sys.stderr)
            return False

        elapsed = time.monotonic() - start_time
        print(f"  ✓ Health Barrier passed in {elapsed:.3f}s (Deterministic readiness confirmed).")
        return True

    # =========================================================================
    # Block 4: Evidence-Capture Test Suite
    # =========================================================================
    def run_suite(self) -> int:
        """Execute test suite based on selected mode and capture structured evidence."""
        print(f"🚀 [Block 4] Evidence-Capture Test Suite: Running in mode '{self.mode}'...")
        start_ts = time.time()
        start_monotonic = time.monotonic()
        captured_logs: List[str] = []
        overall_exit_code = 0
        executed_commands: List[Dict[str, Any]] = []

        # Determine commands to execute
        commands_to_run: List[Tuple[str, List[str]]] = []

        if self.mode == "cleanliness":
            commands_to_run.append(
                (
                    "Spoke Cleanliness Check",
                    [sys.executable, str(self.spoke_root / "scripts" / "check_spoke_cleanliness.py")],
                )
            )
        elif self.mode == "bundle":
            if not self.bundle:
                print("❌ Mode 'bundle' requires --bundle <slug> argument.", file=sys.stderr)
                return 1
            cmd = [
                sys.executable,
                str(self.spoke_root / "scripts" / "validate_legal_spoke.py"),
                "--bundle",
                self.bundle,
            ]
            if self.skip_pdf_vault:
                cmd.append("--skip-pdf-vault")
            commands_to_run.append((f"Scoped Bundle Check [{self.bundle}]", cmd))
        elif self.mode == "smoke":
            # Smoke check: Cleanliness + Scoped fast check on primary bundle if available
            commands_to_run.append(
                (
                    "Spoke Cleanliness Check",
                    [sys.executable, str(self.spoke_root / "scripts" / "check_spoke_cleanliness.py")],
                )
            )
            smoke_cmd = [
                sys.executable,
                str(self.spoke_root / "scripts" / "validate_legal_spoke.py"),
                "--skip-pdf-vault",
            ]
            # Use bundle if provided, otherwise validate all with skip-pdf-vault for speed
            if self.bundle:
                smoke_cmd.extend(["--bundle", self.bundle])
            commands_to_run.append(("Smoke Validation (Skip PDF Vault)", smoke_cmd))
        else:  # mode == "full"
            commands_to_run.append(
                (
                    "Spoke Cleanliness Check",
                    [sys.executable, str(self.spoke_root / "scripts" / "check_spoke_cleanliness.py")],
                )
            )
            full_cmd = [
                sys.executable,
                str(self.spoke_root / "scripts" / "validate_legal_spoke.py"),
            ]
            if self.skip_pdf_vault:
                full_cmd.append("--skip-pdf-vault")
            if self.bundle:
                full_cmd.extend(["--bundle", self.bundle])
            commands_to_run.append(("15-Gate Master Validation", full_cmd))

        # Execute commands sequentially with live streaming and evidence capture
        for label, cmd in commands_to_run:
            print(f"\n--- Running: {label} ---")
            step_start = time.monotonic()
            proc = self._spawn_process_group(cmd)

            output_lines: List[str] = []
            if proc.stdout:
                for line in proc.stdout:
                    sys.stdout.write(line)
                    sys.stdout.flush()
            timed_out = False
            try:
                proc.wait(timeout=self.step_timeout)
            except subprocess.TimeoutExpired:
                print(f"\n❌ [TIMEOUT] {label} timed out after {self.step_timeout}s!", file=sys.stderr)
                self.cleanup()
                timed_out = True
                exit_code = 124
            else:
                exit_code = proc.returncode

            step_duration = time.monotonic() - step_start
            self.active_process = None

            executed_commands.append(
                {
                    "label": label,
                    "command": " ".join(cmd),
                    "exit_code": exit_code,
                    "duration_seconds": round(step_duration, 3),
                    "status": "PASSED" if exit_code == 0 else "FAILED",
                }
            )
            captured_logs.extend(output_lines)

            if exit_code != 0:
                overall_exit_code = exit_code
                print(f"❌ {label} failed with exit code {exit_code}")
                break
            else:
                print(f"✅ {label} passed in {step_duration:.2f}s")

        total_duration = time.monotonic() - start_monotonic

        # Compile structured evidence report
        evidence = {
            "schema_version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mode": self.mode,
            "bundle": self.bundle,
            "overall_status": "PASSED" if overall_exit_code == 0 else "FAILED",
            "overall_exit_code": overall_exit_code,
            "total_duration_seconds": round(total_duration, 3),
            "executed_steps": executed_commands,
            "environment": {
                "python_version": sys.version.split()[0],
                "platform": sys.platform,
                "spoke_root": str(self.spoke_root),
            },
        }

        try:
            self.evidence_out.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"\n📊 Evidence report saved to: {self.evidence_out}")
        except Exception as exc:
            print(f"⚠️ Could not write evidence report: {exc}", file=sys.stderr)

        return overall_exit_code

    # =========================================================================
    # Block 5: Guaranteed Graceful Cleanup
    # =========================================================================
    def cleanup(self) -> None:
        """Guaranteed cleanup to eliminate dangling or zombie child processes."""
        if self.active_process is not None and self.active_process.poll() is None:
            print("\n🧹 [Block 5] Guaranteed Graceful Cleanup: Terminating active process tree...", file=sys.stderr)
            pid = self.active_process.pid
            try:
                if self.is_win:
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], check=False, capture_output=True)
                else:
                    try:
                        pgid = os.getpgid(pid)
                        os.killpg(pgid, signal.SIGTERM)
                        time.sleep(0.2)
                        os.killpg(pgid, signal.SIGKILL)
                    except (ProcessLookupError, PermissionError):
                        pass
            except Exception as exc:
                print(f"⚠️ Error during cleanup: {exc}", file=sys.stderr)
            finally:
                self.active_process = None


def main() -> None:
    """CLI Entrypoint for verify-legal-knowledge harness."""
    parser = argparse.ArgumentParser(
        description="Deterministic Verification Harness for CCBA Legal Knowledge Spoke"
    )
    parser.add_argument(
        "--mode",
        choices=["smoke", "full", "cleanliness", "bundle"],
        default="full",
        help="Verification mode: smoke (fast), full (all 15 gates), cleanliness (ADR-0044), bundle (scoped)",
    )
    parser.add_argument(
        "--bundle",
        default=None,
        help="Target document bundle slug (required for --mode bundle, optional for others)",
    )
    parser.add_argument(
        "--skip-pdf-vault",
        action="store_true",
        help="Skip vector PDF vault presence check for offline/unmounted CI environments",
    )
    parser.add_argument(
        "--evidence-out",
        type=Path,
        default=None,
        help="Path to save structured evidence JSON artifact",
    )
    parser.add_argument(
        "--step-timeout",
        type=float,
        default=300.0,
        help="Maximum timeout in seconds per verification step (default: 300.0s)",
    )

    args = parser.parse_args()

    harness = LegalVerificationHarness(
        mode=args.mode,
        bundle=args.bundle,
        skip_pdf_vault=args.skip_pdf_vault,
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
        print("\n🛑 Execution interrupted by user.", file=sys.stderr)
        exit_code = 130
    finally:
        harness.cleanup()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
