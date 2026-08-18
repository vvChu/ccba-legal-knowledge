"""Clean and polish QCVN 06:2022/BXD and Sửa đổi 1:2023 OKF bundle."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def clean_sua_doi_1_2023(bundle_dir: Path) -> None:
    p = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"
    if not p.exists():
        return

    text = p.read_text(encoding="utf-8")

    # 1. Remove tvpl and arbitrary anchors
    text = re.sub(r'<a id="(?:tvpllink|cumtu|dc|loai|dieu)_[^"]*"></a>', "", text)

    # 2. Fix escapes
    text = text.replace(r"\.", ".").replace(r"\(", "(").replace(r"\)", ")").replace(r"\-", "-").replace(r"\_", "_")

    # 3. Clean headings
    text = re.sub(r"__(\d+\s+[A-Z\s,–-]+)__", r"### \1", text)
    text = re.sub(r"__Sửa đổi[,\s]+bổ sung\s+([^_]+)__", r"#### Sửa đổi, bổ sung \1", text)
    text = re.sub(r"__Sửa đổi\s+([^_]+)__", r"#### Sửa đổi \1", text)
    text = re.sub(r"__Bổ sung\s+([^_]+)__", r"#### Bổ sung \1", text)

    # 4. Clean consecutive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    p.write_text(text, encoding="utf-8")
    print(f"Cleaned sua_doi_1_2023: len = {len(text)}")


def clean_qcvn_06_base(bundle_dir: Path) -> None:
    p = bundle_dir / "qcvn_06_2022_bxd.md"
    if not p.exists():
        return

    text = p.read_text(encoding="utf-8")

    # 1. Fix Section 1.4 dot-split anomalies: 1.4.1.7 -> 1.4.17 up to 1.4.7.2 -> 1.4.72
    for tens in range(1, 8):
        for units in range(0, 10):
            num = tens * 10 + units
            if 10 <= num <= 72:
                # Fix dot-split 1.4.tens.units -> 1.4.num
                text = re.sub(rf"(#+|\b)1\.4\.{tens}\.{units}\b", rf"\g<1>1.4.{num}", text)
                # Fix space-split 1.4.tens units -> 1.4.num
                text = re.sub(rf"(#+|\b)1\.4\.{tens}\s+{units}\b", rf"\g<1>1.4.{num}", text)

    # 2. Fix space-headings in Chapter 4: "### 4 1" -> "### 4.1" up to 4.35
    for i in range(1, 36):
        text = re.sub(rf"(#+)\s+4\s+{i}\b", rf"\1 4.{i}", text)

    # 3. Fix space-headings in Chapter 7: "### 7 1" -> "### 7.1" up to 7.5
    for i in range(1, 6):
        text = re.sub(rf"(#+)\s+7\s+{i}\b", rf"\1 7.{i}", text)

    # 4. Fix all 13 Level-4 subclause headings across Sections 2.1, 2.2, 5.1, 6.2 and typos
    subdot_replacements = [
        (r"(#{1,6})\s+2\.1\.11\b", r"\1 2.1.1.1"),
        (r"(#{1,6})\s+2\.1\.12\b", r"\1 2.1.1.2"),
        (r"(#{1,6})\s+2\.2\.11\b", r"\1 2.2.1.1"),
        (r"(#{1,6})\s+2\.2\.12\b", r"\1 2.2.1.2"),
        (r"(#{1,6})\s+2\.2\.13\b", r"\1 2.2.1.3"),
        (r"(#{1,6})\s+5\.1\.11\b", r"\1 5.1.1.1"),
        (r"(#{1,6})\s+5\.1\.12\b", r"\1 5.1.1.2"),
        (r"(#{1,6})\s+5\.1\.13\b", r"\1 5.1.1.3"),
        (r"(#{1,6})\s+5\.1\.14\b", r"\1 5.1.1.4"),
        (r"(#{1,6})\s+6\.2\.11\b", r"\1 6.2.1.1"),
        (r"(#{1,6})\s+6\.2\.12\b", r"\1 6.2.1.2"),
        (r"(#{1,6})\s+6\.2\.13\b", r"\1 6.2.1.3"),
        (r"(#{1,6})\s+6\.2\.14\b", r"\1 6.2.1.4"),
        (r"(#{1,6})\s+2\.5\.6\.3\s+3\b", r"\1 2.5.6.3.3"),
    ]
    for pattern, repl in subdot_replacements:
        text = re.sub(pattern, repl, text)

    # 4b. Promote plaintext heading '2 2.2.1' -> '##### 2.2.2.1' with anchor if unpromoted
    text = re.sub(
        r'(?:<a id="[^"]*"></a>\s*\n)?(?:^|\n)2\s+2\.2\.1\s+(Các cấu kiện xây dựng của nhà)',
        r'\n<a id="muc-2-2-2-1"></a>\n##### 2.2.2.1  \1',
        text,
    )

    # 5. Purge fake table residual headings like "### 24 0", "### 1 4", etc.
    text = re.sub(r"\n#+\s+[0-9]+(?:\s+[0-9]+)*\n", "\n", text)

    p.write_text(text, encoding="utf-8")
    print(f"Cleaned qcvn_06 base: len = {len(text)}")


if __name__ == "__main__":
    bundle_path = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
    clean_sua_doi_1_2023(bundle_path)
    clean_qcvn_06_base(bundle_path)
