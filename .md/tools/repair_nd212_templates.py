"""Repair corrupted template titles and filenames in ND 212/2026/ND-CP."""
import re
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
BUNDLE_DIR = ROOT / "legal_docs" / "01_vbpl" / "nghi_dinh_212_2026_nd_cp"
TEMPLATES_DIR = BUNDLE_DIR / "templates" / "phu_luc_iii"

FORM_MAPPING = {
    "mau_01": {
        "new_name": "mau_01_don_de_nghi_cap_chung_chi_hanh_nghe.md",
        "title": "Mẫu số 01 - ĐƠN ĐỀ NGHỊ CẤP CHỨNG CHỈ HÀNH NGHỀ HOẠT ĐỘNG XÂY DỰNG",
        "h1": "# Mẫu Số 01 - ĐƠN ĐỀ NGHỊ CẤP CHỨNG CHỈ HÀNH NGHỀ HOẠT ĐỘNG XÂY DỰNG",
    },
    "mau_02": {
        "new_name": "mau_02_don_de_nghi_cap_chuyen_doi_chung_chi_hanh_nghe.md",
        "title": "Mẫu số 02 - ĐƠN ĐỀ NGHỊ CẤP CHUYỂN ĐỔI CHỨNG CHỈ HÀNH NGHỀ HOẠT ĐỘNG XÂY DỰNG",
        "h1": "# Mẫu Số 02 - ĐƠN ĐỀ NGHỊ CẤP CHUYỂN ĐỔI CHỨNG CHỈ HÀNH NGHỀ HOẠT ĐỘNG XÂY DỰNG",
    },
    "mau_03": {
        "new_name": "mau_03_mau_chung_chi_hanh_nghe_hoat_dong_xay_dung.md",
        "title": "Mẫu số 03 - MẪU CHỨNG CHỈ HÀNH NGHỀ HOẠT ĐỘNG XÂY DỰNG",
        "h1": "# Mẫu Số 03 - MẪU CHỨNG CHỈ HÀNH NGHỀ HOẠT ĐỘNG XÂY DỰNG",
    },
    "mau_04": {
        "new_name": "mau_04_don_de_nghi_cap_giay_phep_hoat_dong_xay_dung_to_chuc.md",
        "title": "Mẫu số 04 - ĐƠN ĐỀ NGHỊ CẤP GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG (Đối với nhà thầu là tổ chức)",
        "h1": "# Mẫu Số 04 - ĐƠN ĐỀ NGHỊ CẤP GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG (Đối với nhà thầu là tổ chức)",
    },
    "mau_05": {
        "new_name": "mau_05_bao_cao_cong_viec_du_an_3_nam_gan_nhat.md",
        "title": "Mẫu số 05 - BÁO CÁO CÁC CÔNG VIỆC/DỰ ÁN ĐÃ THỰC HIỆN TRONG 3 NĂM GẦN NHẤT",
        "h1": "# Mẫu Số 05 - BÁO CÁO CÁC CÔNG VIỆC/DỰ ÁN ĐÃ THỰC HIỆN TRONG 3 NĂM GẦN NHẤT",
    },
    "mau_06": {
        "new_name": "mau_06_giay_uy_quyen.md",
        "title": "Mẫu số 06 - GIẤY ỦY QUYỀN",
        "h1": "# Mẫu Số 06 - GIẤY ỦY QUYỀN",
    },
    "mau_07": {
        "new_name": "mau_07_don_de_nghi_cap_giay_phep_hoat_dong_xay_dung_ca_nhan.md",
        "title": "Mẫu số 07 - ĐƠN ĐỀ NGHỊ CẤP GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG (Đối với nhà thầu là cá nhân)",
        "h1": "# Mẫu Số 07 - ĐƠN ĐỀ NGHỊ CẤP GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG (Đối với nhà thầu là cá nhân)",
    },
    "mau_08": {
        "new_name": "mau_08_quyet_dinh_cap_giay_phep_hoat_dong_xay_dung_nha_thau_nuoc_ngoai.md",
        "title": "Mẫu số 08 - QUYẾT ĐỊNH CẤP GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG CHO NHÀ THẦU NƯỚC NGOÀI",
        "h1": "# Mẫu Số 08 - QUYẾT ĐỊNH CẤP GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG CHO NHÀ THẦU NƯỚC NGOÀI",
    },
    "mau_09": {
        "new_name": "mau_09_quyet_dinh_cap_giay_phep_hoat_dong_xay_dung_ca_nhan.md",
        "title": "Mẫu số 09 - QUYẾT ĐỊNH CẤP GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG CHO CÁ NHÂN",
        "h1": "# Mẫu Số 09 - QUYẾT ĐỊNH CẤP GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG CHO CÁ NHÂN",
    },
    "mau_10": {
        "new_name": "mau_10_quyet_dinh_dieu_chinh_giay_phep_hoat_dong_xay_dung_nha_thau_nuoc_ngoai.md",
        "title": "Mẫu số 10 - QUYẾT ĐỊNH ĐIỀU CHỈNH GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG CHO NHÀ THẦU NƯỚC NGOÀI",
        "h1": "# Mẫu Số 10 - QUYẾT ĐỊNH ĐIỀU CHỈNH GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG CHO NHÀ THẦU NƯỚC NGOÀI",
    },
    "mau_11": {
        "new_name": "mau_11_don_de_nghi_dieu_chinh_giay_phep_hoat_dong_xay_dung.md",
        "title": "Mẫu số 11 - ĐƠN ĐỀ NGHỊ ĐIỀU CHỈNH GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG",
        "h1": "# Mẫu Số 11 - ĐƠN ĐỀ NGHỊ ĐIỀU CHỈNH GIẤY PHÉP HOẠT ĐỘNG XÂY DỰNG",
    },
    "mau_12": {
        "new_name": "mau_12_thong_bao_tinh_hinh_hoat_dong_cua_nha_thau_nuoc_ngoai.md",
        "title": "Mẫu số 12 - THÔNG BÁO TÌNH HÌNH HOẠT ĐỘNG CỦA NHÀ THẦU NƯỚC NGOÀI",
        "h1": "# Mẫu Số 12 - THÔNG BÁO TÌNH HÌNH HOẠT ĐỘNG CỦA NHÀ THẦU NƯỚC NGOÀI",
    },
    "mau_13": {
        "new_name": "mau_13_thong_bao_van_phong_dieu_hanh_cua_nha_thau_nuoc_ngoai.md",
        "title": "Mẫu số 13 - THÔNG BÁO VĂN PHÒNG ĐIỀU HÀNH CỦA NHÀ THẦU NƯỚC NGOÀI",
        "h1": "# Mẫu Số 13 - THÔNG BÁO VĂN PHÒNG ĐIỀU HÀNH CỦA NHÀ THẦU NƯỚC NGOÀI",
    },
}

def repair():
    renamed_map = {}
    
    # 1. Update and rename template files
    for old_file in list(TEMPLATES_DIR.glob("*.md")):
        prefix = old_file.name[:6]
        if prefix in FORM_MAPPING:
            info = FORM_MAPPING[prefix]
            content = old_file.read_text(encoding="utf-8")
            
            # Replace frontmatter title
            content = re.sub(r'title:\s*"[^"]*"', f'title: "{info["title"]}"', content, count=1)
            
            # Replace H1 heading
            content = re.sub(r'^#\s+Mẫu\s+Số\s+\d+.*$', info["h1"], content, flags=re.MULTILINE, count=1)
            
            new_file = TEMPLATES_DIR / info["new_name"]
            if old_file != new_file:
                old_file.unlink()
            new_file.write_text(content, encoding="utf-8")
            renamed_map[old_file.name] = info["new_name"]
            print(f"Repaired: {old_file.name} -> {info['new_name']}")

    # 2. Update links in main markdown file
    main_md = BUNDLE_DIR / "nghi_dinh_212_2026_nd_cp.md"
    if main_md.exists():
        text = main_md.read_text(encoding="utf-8")
        for old_name, new_name in renamed_map.items():
            text = text.replace(old_name, new_name)
        
        # Also clean up the link text in main_md
        for prefix, info in FORM_MAPPING.items():
            num = prefix[4:]
            pattern = rf'(\*\*Phụ lục III - Mẫu {num}:)[^\n]*(\]\(\./templates/phu_luc_iii/{info["new_name"]}\)\*\*)'
            replacement = rf'\1 {info["title"][10:]}\2'
            text = re.sub(pattern, replacement, text)
            
        main_md.write_text(text, encoding="utf-8")
        print("Updated links in main markdown file.")

    # 3. Update index.md
    index_md = BUNDLE_DIR / "index.md"
    if index_md.exists():
        text = index_md.read_text(encoding="utf-8")
        for old_name, new_name in renamed_map.items():
            text = text.replace(old_name, new_name)
        index_md.write_text(text, encoding="utf-8")
        print("Updated links in index.md.")

    # 4. Update clauses.json if any
    clauses_file = BUNDLE_DIR / "clauses.json"
    if clauses_file.exists():
        text = clauses_file.read_text(encoding="utf-8")
        for old_name, new_name in renamed_map.items():
            text = text.replace(old_name, new_name)
        clauses_file.write_text(text, encoding="utf-8")
        print("Updated links in clauses.json.")

if __name__ == "__main__":
    repair()
