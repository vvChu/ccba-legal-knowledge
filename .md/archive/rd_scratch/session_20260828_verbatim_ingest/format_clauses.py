import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import json
from pathlib import Path

bundle_dir = Path("legal_docs/02_qcvn/qcvn_03_2022_bxd")
clauses_file = bundle_dir / "clauses.json"

clauses_list = [
    {
        "clause_id": "muc-1",
        "anchor": "1-quy-dinh-chung",
        "title": "1. QUY ĐỊNH CHUNG",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-1-1",
        "anchor": "11-pham-vi-dieu-chinh",
        "title": "1.1. Phạm vi điều chỉnh",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "dieu-1-1-1",
        "anchor": "111",
        "title": "1.1.1. Tiêu chí phân cấp công trình",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "dieu-1-1-2",
        "anchor": "112",
        "title": "1.1.2. Đối tượng công trình áp dụng",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "dieu-1-1-3",
        "anchor": "113",
        "title": "1.1.3. Mục đích áp dụng cấp công trình",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-1-2",
        "anchor": "12-doi-tuong-ap-dung",
        "title": "1.2. Đối tượng áp dụng",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-1-3",
        "anchor": "13-giai-thich-tu-ngu",
        "title": "1.3. Giải thích từ ngữ",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "WARNING_NOTICE",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-2",
        "anchor": "2-quy-dinh-ky-thuat",
        "title": "2. QUY ĐỊNH KỸ THUẬT",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-2-1",
        "anchor": "21-cap-hau-qua-cua-cong-trinh",
        "title": "2.1. Cấp hậu quả của công trình",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "dieu-2-1-1",
        "anchor": "211",
        "title": "2.1.1. Phân loại 3 cấp hậu quả C1, C2, C3",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "dieu-2-1-2",
        "anchor": "212",
        "title": "2.1.2. Áp dụng Phụ lục A xác định cấp hậu quả",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "dieu-2-1-3",
        "anchor": "213",
        "title": "2.1.3. Trách nhiệm xác định cấp hậu quả trong nhiệm vụ thiết kế",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-2-2",
        "anchor": "22-thoi-han-su-dung-theo-thiet-ke-cua-cong-trinh",
        "title": "2.2. Thời hạn sử dụng theo thiết kế của công trình",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "dieu-2-2-1",
        "anchor": "221",
        "title": "2.2.1. Phân mức thời hạn sử dụng Mức 1 - 4 (Bảng 1)",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "dieu-2-2-2",
        "anchor": "222",
        "title": "2.2.2. Thời hạn sử dụng của bộ phận kết cấu chính",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "dieu-2-2-3",
        "anchor": "223",
        "title": "2.2.3. Hết thời hạn sử dụng theo thiết kế",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "WARNING_NOTICE",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "dieu-2-2-4",
        "anchor": "224",
        "title": "2.2.4. Phù hợp vật liệu và cấu kiện với niên hạn",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-2-3",
        "anchor": "23-phan-loai-cong-trinh-theo-muc-dich-an-toan-chay",
        "title": "2.3. Phân loại công trình theo mục đích an toàn cháy",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CONG_AN",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-3",
        "anchor": "3-to-chuc-thuc-hien",
        "title": "3. TỔ CHỨC THỰC HIỆN",
        "source_file": "qcvn_03_2022_bxd.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "WARNING_NOTICE",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "phu-luc-a",
        "anchor": "phu-luc-a-cap-hau-qua-cua-cong-trinh-xay-dung",
        "title": "PHỤ LỤC A: CẤP HẬU QUẢ CỦA CÔNG TRÌNH XÂY DỰNG",
        "source_file": "annexes/phu_luc_a_cap_hau_qua_cong_trinh.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-a-1",
        "anchor": "a1-cac-cong-trinh-co-cap-c3-hau-qua-lon",
        "title": "A.1. Các công trình có cấp C3 (Hậu quả lớn)",
        "source_file": "annexes/phu_luc_a_cap_hau_qua_cong_trinh.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-a-2",
        "anchor": "a2-cac-cong-trinh-co-cap-c1-hau-qua-nho",
        "title": "A.2. Các công trình có cấp C1 (Hậu quả nhỏ)",
        "source_file": "annexes/phu_luc_a_cap_hau_qua_cong_trinh.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    },
    {
        "clause_id": "muc-a-3",
        "anchor": "a3-cac-cong-trinh-co-cap-c2-hau-qua-trung-binh",
        "title": "A.3. Các công trình có cấp C2 (Hậu quả trung bình)",
        "source_file": "annexes/phu_luc_a_cap_hau_qua_cong_trinh.md",
        "jurisdiction": "CQXD",
        "compliance_severity": "CRITICAL_DEFECT",
        "cong_bao_number": "05/2022/TT-BXD"
    }
]

clauses_file.write_text(json.dumps(clauses_list, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"✅ Formatted clauses.json with {len(clauses_list)} clauses.")
