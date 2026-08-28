import re
from pathlib import Path

target_dir = Path("legal_docs/03_tcvn/tcvn_2737_2023")
md_files = [target_dir / "tcvn_2737_2023.md"] + sorted((target_dir / "annexes").glob("*.md"))

img_pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")

total_images = 0
for mf in md_files:
    text = mf.read_text(encoding="utf-8")
    lines = text.splitlines()
    for idx, line in enumerate(lines, 1):
        m = img_pattern.search(line)
        if m:
            total_images += 1
            alt = m.group(1)
            src = m.group(2)
            print(f"{mf.name}:{idx} -> Alt: '{alt}' | Src: '{src}'")

print(f"Total figure embeds in markdown: {total_images}")
