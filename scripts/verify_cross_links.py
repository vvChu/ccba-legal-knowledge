"""Exhaustive Link and Destination Verifier for QCVN 06:2022 and Sửa đổi 1:2023."""

import re
import sys
from pathlib import Path
from typing import List, Tuple

sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
base_file = bundle_dir / "qcvn_06_2022_bxd.md"
sd_file = bundle_dir / "sua_doi_1_2023_qcvn_06_2022_bxd.md"

base_text = base_file.read_text(encoding="utf-8")
sd_text = sd_file.read_text(encoding="utf-8")

print("=================================================================")
print("          KIỂM TRA TÍNH HỢP LỆ VÀ ĐÍCH ĐẾN CỦA TOÀN BỘ LINK       ")
print("=================================================================")

# 1. Extract all anchors
base_anchors = set(re.findall(r'<a id="([^"]+)"', base_text))
sd_anchors = set(re.findall(r'<a id="([^"]+)"', sd_text))
print(f"Tổng số thẻ neo trong file gốc (qcvn_06_2022_bxd.md)    : {len(base_anchors)}")
print(f"Tổng số thẻ neo trong file Sửa đổi 1 (sua_doi_1_2023...) : {len(sd_anchors)}")

# 2. Check all links in Sửa đổi 1 -> Base doc
raw_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', sd_text)
print(f"Tổng số liên kết (Links) trong file Sửa đổi 1             : {len(raw_links)}")

broken_links: List[Tuple[str, str, str]] = []
valid_links: List[Tuple[str, str]] = []

for text, target in raw_links:
    if target.startswith("qcvn_06_2022_bxd.md#"):
        anchor = target.split("#", 1)[1]
        if anchor in base_anchors:
            valid_links.append((text, target))
        else:
            broken_links.append((text, target, f"Thẻ neo '{anchor}' không tồn tại trong qcvn_06_2022_bxd.md"))
    elif target.startswith("#"):
        anchor = target[1:]
        if anchor in sd_anchors:
            valid_links.append((text, target))
        else:
            broken_links.append((text, target, f"Thẻ neo nội bộ '{anchor}' không tồn tại"))
    else:
        valid_links.append((text, target))

print("-----------------------------------------------------------------")
print(f"✅ Liên kết Sửa đổi 1 -> Bản gốc HỢP LỆ: {len(valid_links)} / {len(raw_links)}")
print(f"❌ Liên kết Sửa đổi 1 BỊ HỎNG          : {len(broken_links)}")

# 3. Check internal links in Base Doc
base_internal_links = re.findall(r'\[([^\]]+)\]\(#([^)]+)\)', base_text)
base_broken = []
for text, anchor in base_internal_links:
    if anchor not in base_anchors:
        base_broken.append((text, f"#{anchor}"))

print(f"✅ Liên kết Nội bộ trong file gốc HỢP LỆ : {len(base_internal_links) - len(base_broken)} / {len(base_internal_links)}")
print(f"❌ Liên kết Nội bộ file gốc BỊ HỎNG    : {len(base_broken)}")
print("-----------------------------------------------------------------")

if not broken_links and not base_broken:
    print("🎉 TẤT CẢ LIÊN KẾT ĐỀU CHÍNH XÁC NƠI ĐÍCH 100%!")
else:
    if broken_links:
        print("Chi tiết link hỏng tại Sửa đổi 1:")
        for t, tg, r in broken_links:
            print(f"  ❌ [{t}]({tg}) -> {r}")
    if base_broken:
        print("Chi tiết link nội bộ hỏng tại file gốc:")
        for t, tg in base_broken:
            print(f"  ❌ [{t}]({tg})")
print("=================================================================")
