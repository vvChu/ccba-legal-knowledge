"""
Inspect how sections 2.1.1, 2.2.1, 5.1.1, 6.2.1 are formatted in qcvn_06_2022_bxd.md
"""
import sys
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MD_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md")
md_lines = MD_PATH.read_text(encoding="utf-8").splitlines()

def inspect_around(keywords, window=10):
    for i, line in enumerate(md_lines):
        for kw in keywords:
            if kw in line:
                print(f"=== Found '{kw}' at line {i+1} ===")
                start = max(0, i - 3)
                end = min(len(md_lines), i + window)
                for j in range(start, end):
                    print(f"{j+1:4d}: {md_lines[j]}")
                print("-" * 50)
                break

print("--- 2.1.1 ---")
inspect_around(["2.1.1", "Việc phân nhóm chất"], 10)

print("--- 2.2.1 ---")
inspect_around(["2.2.1", "Cấu kiện xây dựng được phân loại"], 10)

print("--- 5.1.1 ---")
inspect_around(["5.1.1", "Việc trang bị cấp nước chữa cháy"], 10)

print("--- 6.2.1 ---")
inspect_around(["6.2.1", "Chiều rộng thông thủy của mặt đường cho xe"], 10)

print("--- Bảng F.2 ---")
inspect_around(["F.2", "Tường ngoài không chịu lực"], 10)
