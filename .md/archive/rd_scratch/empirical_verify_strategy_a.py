import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(".")
LEGAL_DOCS = ROOT / "legal_docs"

# 1. Measure all files in repository
all_md_files = list(LEGAL_DOCS.rglob("*.md"))

# Strategy A: Clean Unified Repository
# - All 01_vbpl files
# - Only *_hop_nhat_*.md in 02_qcvn
# - All bang_so_sanh_*.md in 04_appendices
# - Exclude index.md and obsolete base/amending individual docs
strat_a_files = []
strat_b_files = []

for f in all_md_files:
    if f.name == "index.md":
        continue
    rel = f.relative_to(LEGAL_DOCS)
    parts = rel.parts
    strat_b_files.append(f)
    
    if parts[0] == "01_vbpl":
        strat_a_files.append(f)
    elif parts[0] == "02_qcvn":
        if "_hop_nhat_" in f.name:
            strat_a_files.append(f)
    elif parts[0] == "04_appendices":
        strat_a_files.append(f)

def get_stats(file_list):
    total_bytes = sum(f.stat().st_size for f in file_list)
    total_words = 0
    total_lines = 0
    for f in file_list:
        text = f.read_text(encoding="utf-8")
        total_words += len(text.split())
        total_lines += len(text.splitlines())
    return len(file_list), total_bytes, total_words, total_lines

count_a, bytes_a, words_a, lines_a = get_stats(strat_a_files)
count_b, bytes_b, words_b, lines_b = get_stats(strat_b_files)

print(f"=== CHIẾN LƯỢC A (Clean Unified Repository) ===")
print(f"Tổng số nguồn (Sources): {count_a}")
print(f"Tổng dung lượng        : {bytes_a / 1024:.1f} KB")
print(f"Tổng số từ (Words)     : {words_a:,} từ")
print(f"Tổng số dòng           : {lines_a:,} dòng")

print(f"\n=== CHIẾN LƯỢC B (Full Historical Archive) ===")
print(f"Tổng số nguồn (Sources): {count_b}")
print(f"Tổng dung lượng        : {bytes_b / 1024:.1f} KB")
print(f"Tổng số từ (Words)     : {words_b:,} từ")
print(f"Tổng số dòng           : {lines_b:,} dòng")

# 2. Check Specific Contradictions in Real Data
print("\n=== KIỂM CHỨNG XUNG ĐỘT DỮ LIỆU THỰC TẾ (REAL DATA CONTRADICTIONS) ===")

# Example 1: QCVN 04 - Mục 2.2.17 (Chỗ để xe)
base_qcvn04 = (LEGAL_DOCS / "02_qcvn" / "qcvn_04_2021_bxd" / "qcvn_04_2021_bxd.md").read_text(encoding="utf-8")
hopnhat_qcvn04 = (LEGAL_DOCS / "02_qcvn" / "qcvn_04_2021_bxd" / "qcvn_04_2021_bxd_hop_nhat_2026.md").read_text(encoding="utf-8")

def extract_section(text, sec_id):
    m = re.search(rf'(<a id="{sec_id}".*?)(?=<a id="muc-|\Z)', text, re.DOTALL)
    return m.group(1).strip() if m else "NOT FOUND"

sec_base_2217 = extract_section(base_qcvn04, "muc-2-2-17")
sec_hn_2217 = extract_section(hopnhat_qcvn04, "muc-2-2-17")

print("\n--- [QCVN 04: Mục 2.2.17 Chỗ để xe & Trạm sạc xe điện] ---")
print(f"[Bản Gốc 2021] Số từ: {len(sec_base_2217.split())} từ")
print(f"Trích dẫn Bản Gốc: {sec_base_2217[:200]}...")
print(f"\n[Bản Hợp Nhất 2026] Số từ: {len(sec_hn_2217.split())} từ")
print(f"Trích dẫn Bản Hợp Nhất: {sec_hn_2217[:200]}...")

# Example 2: QCVN 06 - Bảng 6 / Điều 2.2.1
base_qcvn06 = (LEGAL_DOCS / "02_qcvn" / "qcvn_06_2022_bxd" / "qcvn_06_2022_bxd.md").read_text(encoding="utf-8")
hopnhat_qcvn06 = (LEGAL_DOCS / "02_qcvn" / "qcvn_06_2022_bxd" / "qcvn_06_2022_bxd_hop_nhat_2023.md").read_text(encoding="utf-8")

# Let's see differences in term 1.4.31 vs original
print("\n--- [Kiểm tra độ phủ thông tin của Bảng Đối Chiếu Thay Đổi] ---")
bang_ss_04 = (LEGAL_DOCS / "04_appendices" / "bang_so_sanh_sua_doi_2026" / "bang_so_sanh_sua_doi_2026.md").read_text(encoding="utf-8")
print(f"Dung lượng Bảng So Sánh QCVN 04: {len(bang_ss_04.split())} từ")
