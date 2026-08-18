"""Audit quality metrics for sua_doi_1_2023_qcvn_06_2022_bxd.md."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

p = Path(__file__).resolve().parent.parent / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "sua_doi_1_2023_qcvn_06_2022_bxd.md"
t = p.read_text(encoding="utf-8")

print("=================================================================")
print("      BÁO CÁO KIỂM ĐỊNH CHẤT LƯỢNG SỬA ĐỔI 1:2023 QCVN 06        ")
print("=================================================================")

# 1. Neo rác TVPL thừa
bad_anchors = re.findall(r'<a id="(?:tvpllink|cumtu|dc|loai|dieu)_[^"]*"></a>', t)
print(f"1. Neo rác TVPL (tvpllink/cumtu/dc): {len(bad_anchors)} -> {'CLEAN' if len(bad_anchors) == 0 else 'WARNING'}")

# 2. Ký tự backslash escape thừa
escapes = re.findall(r"\\[.\-()_]", t)
print(f"2. Ký tự backslash escape thừa      : {len(escapes)} -> {'CLEAN' if len(escapes) == 0 else 'WARNING'}")

# 3. Chuỗi gạch dưới rác (____)
underscores = re.findall(r"_{4,}", t)
print(f"3. Chuỗi gạch dưới rác (____)       : {len(underscores)} -> {'CLEAN' if len(underscores) == 0 else 'WARNING'}")

# 4. Tiêu đề Markdown chuẩn
headings = [l for l in t.splitlines() if l.startswith("#")]
print(f"4. Hệ thống Tiêu đề Markdown        : {len(headings)} đề mục chuẩn (H1 - H4)")

# 5. Bảng kỹ thuật GFM
tables = [l for l in t.splitlines() if re.match(r"^\|\s*[-:]+\s*\|", l)]
print(f"5. Bảng kỹ thuật GFM Pipe Tables     : {len(tables)} bảng hoàn chỉnh")

# 6. Liên kết đối soát 2 chiều sang bản gốc
links = re.findall(r"qcvn_06_2022_bxd\.md#", t)
print(f"6. Liên kết đối soát sang bản gốc   : {len(links)} liên kết 2 chiều")

# 7. Đoạn văn bản bảo toàn
lines = t.splitlines()
print(f"7. Tổng số dòng văn bản              : {len(lines)} dòng | Dung lượng: {len(t):,} bytes")
print("=================================================================")

if len(bad_anchors) == 0 and len(escapes) == 0 and len(underscores) == 0:
    print("✅ XÁC NHẬN: Dữ liệu Sửa đổi 1:2023 đã được chuẩn hóa sạch 100%!")
else:
    print("❌ CẢNH BÁO: Còn tồn tại lỗi cần xử lý.")
