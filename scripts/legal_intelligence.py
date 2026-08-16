#!/usr/bin/env python3
"""Legal Intelligence Pipeline CLI wrapper.

Thin adapter delegating to LegalIntelPipeline in `ccba_legal.coordinator`
with Gold Standard OKF post-processing and raw backup to .md/extracted_docs/.
"""

import os
import shutil
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure root directory is on sys.path
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from ccba_legal import LegalIntelPipeline
from scripts.gold_standard_processor import process_okf_bundle

# Enforce UTF-8 output on Windows
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def load_env_credentials() -> None:
    """Nạp biến môi trường từ local .env hoặc tự động kế thừa từ Hub (ccba-agent-platform)."""
    load_dotenv(".env")
    if not os.environ.get("TVPL_USERNAME"):
        hub_env = Path("D:/GitHubProjects/ccba-agent-platform/.env")
        if hub_env.exists():
            load_dotenv(hub_env)


def sync_raw_backup_and_post_process(output_dir: Path) -> None:
    """Backup raw files to .md/extracted_docs and run Gold Standard Processor."""
    extracted_docs_dir = Path(".md/extracted_docs")
    extracted_docs_dir.mkdir(parents=True, exist_ok=True)

    for bundle in output_dir.glob("*"):
        if bundle.is_dir():
            # 1. Post-process OKF bundle
            process_okf_bundle(bundle)

            # 2. Backup raw file to .md/extracted_docs/
            raw_backup_target = extracted_docs_dir / bundle.name
            raw_backup_target.mkdir(parents=True, exist_ok=True)

            for item in bundle.glob("*.md"):
                if item.name not in ("index.md", "dead_ends.md", "log.md"):
                    shutil.copy2(item, raw_backup_target / item.name)


def main() -> None:
    """Run the Legal Intelligence Pipeline CLI."""
    load_env_credentials()
    root_registry = Path("legal_registry.yaml")
    root_output_dir = Path("legal_docs/01_vbpl")
    root_output_dir.mkdir(parents=True, exist_ok=True)
    pipeline = LegalIntelPipeline(output_dir=root_output_dir, registry_path=root_registry)

    ret_code = pipeline.run_cli(sys.argv[1:])
    if ret_code == 0:
        sync_raw_backup_and_post_process(root_output_dir)

    sys.exit(ret_code)


if __name__ == "__main__":
    main()
