"""setup_pre_commit.py - Install automated Pre-Commit Verification Hook."""

from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def install_hook() -> bool:
    root_dir = Path.cwd()
    git_dir = root_dir / ".git"
    if not git_dir.exists():
        print(f"[ERROR] .git directory not found in: {root_dir}")
        return False

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    pre_commit_path = hooks_dir / "pre-commit"

    # Hook script content (Bash/POSIX compatible with Git Bash / Windows Git)
    hook_script = """#!/bin/sh
# CCBA Legal Knowledge Automated Pre-Commit Gate
echo "================================================================="
echo "   [PRE-COMMIT HOOK] RUNNING CCBA SPOKE CLEANLINESS CHECK        "
echo "================================================================="

python scripts/check_spoke_cleanliness.py
RESULT_CLEAN=$?

if [ $RESULT_CLEAN -ne 0 ]; then
    echo ""
    echo "❌ COMMIT REJECTED: Cleanliness check or staged binary guard failed."
    echo "Please fix the issues above before committing."
    exit 1
fi

echo "================================================================="
echo "   [PRE-COMMIT HOOK] RUNNING CCBA 15-GATE MASTER VALIDATOR       "
echo "================================================================="

python scripts/validate_legal_spoke.py
RESULT=$?

if [ $RESULT -ne 0 ]; then
    echo ""
    echo "❌ COMMIT REJECTED: Master Validator detected errors."
    echo "Please fix the issues above before committing."
    exit 1
fi

echo "✅ PRE-COMMIT PASSED: Repository is 100% clean and verified."
exit 0
"""
    pre_commit_path.write_text(hook_script, encoding="utf-8")

    # Set executable permission
    try:
        current_stat = os.stat(pre_commit_path)
        os.chmod(pre_commit_path, current_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except Exception:
        pass

    print(f"✅ Successfully installed Git Pre-Commit Hook at: {pre_commit_path}")
    return True


if __name__ == "__main__":
    if not install_hook():
        sys.exit(1)
