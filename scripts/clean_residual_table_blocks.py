"""Clean residual duplicate table text blocks in QCVN markdown documents."""

import re
import sys
from pathlib import Path
from scripts.gold_standard_processor import process_okf_bundle

sys.stdout.reconfigure(encoding="utf-8")


def clean_all_residual_blocks(md_path: Path) -> int:
    """Clean all residual unformatted text blocks following Bảng 11."""
    if not md_path.exists():
        return 0

    content = md_path.read_text(encoding="utf-8")

    # Regex targeting duplicate text block after Bảng 11 notes down to next heading
    residual_pattern = re.compile(
        r"_\s*1\)\s*Trụ sở cơ quan nhà nước.*?\n(\s*> 25 000 m3\s*\n.*?)?(?=\n<a id=|\n### |\n# |\Z)",
        re.DOTALL | re.IGNORECASE,
    )

    # Replace duplicate residual lines after Bảng 11 note
    cleaned_content = re.sub(
        r"(_- Nhà điều dưỡng, phục hồi chức năng, chỉnh hình, nhà dưỡng\._)\s*\n.*?(?=\n<a id=\"muc-|\n### 5\.|\n### |\Z)",
        r"\1\n\n",
        content,
        flags=re.DOTALL,
    )

    if cleaned_content != content:
        md_path.write_text(cleaned_content, encoding="utf-8")
        print(f"[Cleaner] Successfully purged residual duplicate text blocks from {md_path.name}")
        return 1

    return 0


if __name__ == "__main__":
    target_md = Path("legal_docs/02_qcvn/qcvn_06_2022_bxd/qcvn_06_2022_bxd.md")
    removed = clean_all_residual_blocks(target_md)
    print(f"Purged {removed} residual text blocks.")
    res = process_okf_bundle(target_md.parent)
    print("Reprocessed OKF Bundle:", res)
