"""CCBA Deep Markdown Anomaly & Artifact Scanner."""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"

def scan_bundle():
    files = list(BUNDLE_DIR.glob("*.md"))
    suspicious_patterns = [
        (r"\bNone\b", "Literal None"),
        (r"\bnull\b", "Literal null"),
        (r"\bundefined\b", "Literal undefined"),
        (r"#+\s+#+", "Duplicate hashes"),
        (r'<a\s+id=""', "Empty anchor id"),
        (r"\]\(\s*#\s*\)", "Empty link target"),
        (r"\|\s*\|\s*---", "Broken pipe separator"),
        (r"\|\s*_\s*\|", "Cell trailing underscore artifact"),
        (r"\|\s*\|", "Double pipe inside cell"),
    ]

    total_issues = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        print(f"\nScanning: {f.name} ({len(text):,} chars, {len(text.splitlines())} lines)...")
        file_issues = 0
        for pattern, name in suspicious_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Filter out intentional text if any
                if name == "Double pipe inside cell" and f.name == "tables/README.md":
                    continue
                print(f"  ⚠️ Found {len(matches)} occurrences of [{name}]")
                file_issues += len(matches)
                total_issues += len(matches)
        if file_issues == 0:
            print("  ✅ 100% Sạch sẽ, không phát hiện lỗi định dạng bất thường.")

    print("\n" + "=" * 65)
    if total_issues == 0:
        print("🎉 TẤT CẢ TỆP MARKDOWN ĐỀU ĐẠT CHUẨN 100% ZERO FORMAT ANOMALY!")
    else:
        print(f"⚠️ Tổng cộng phát hiện {total_issues} điểm cần rà soát.")
    print("=" * 65)

if __name__ == "__main__":
    scan_bundle()
