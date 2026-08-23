"""Build full consolidated QCVN 04:2021/BXD Hợp Nhất 2026 Dual-Track Markdown."""

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_04_2021_bxd"
BASE_MD = BUNDLE_DIR / "qcvn_04_2021_bxd.md"
SD1_MD = BUNDLE_DIR / "sua_doi_01_2026_qcvn_04_2021_bxd.md"
HOPNHAT_MD = BUNDLE_DIR / "qcvn_04_2021_bxd_hop_nhat_2026.md"
CLAUSES_FILE = BUNDLE_DIR / "clauses.json"
QA_FILE = BUNDLE_DIR / "qa_benchmark.json"

def build_hopnhat():
    base_text = BASE_MD.read_text(encoding="utf-8")
    sd1_text = SD1_MD.read_text(encoding="utf-8")

    lines = []
    lines.append("# QCVN 04:2021/BXD — HỢP NHẤT 2026")
    lines.append("")
    lines.append("## QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ NHÀ CHUNG CƯ")
    lines.append("")
    lines.append("*(Văn bản hợp nhất giữa [QCVN 04:2021/BXD (TT 03/2021/TT-BXD)](qcvn_04_2021_bxd.md) và [Sửa đổi 01:2026 QCVN 04:2021/BXD (TT 31/2026/TT-BXD)](sua_doi_01_2026_qcvn_04_2021_bxd.md) theo cơ chế Dual-Track chuẩn OKF v2.0)*")
    lines.append("")
    lines.append("## MỤC LỤC")
    lines.append("")
    lines.append("- [1  QUY ĐỊNH CHUNG](#muc-1)")
    lines.append("- [2  QUY ĐỊNH KỸ THUẬT](#muc-2)")
    lines.append("- [3  QUY ĐỊNH VỀ QUẢN LÝ](#muc-3)")
    lines.append("- [4  TRÁCH NHIỆM CỦA TỔ CHỨC, CÁ NHÂN](#muc-4)")
    lines.append("- [5  TỔ CHỨC THỰC HIỆN](#muc-5)")
    lines.append("")
    lines.append("## Lời nói đầu")
    lines.append("")
    lines.append("QCVN 04:2021/BXD do Viện Khoa học Công nghệ Xây dựng biên soạn, Vụ Khoa học Công nghệ và Môi trường trình duyệt, Bộ Khoa học và Công nghệ thẩm định, Bộ Xây dựng ban hành kèm theo Thông tư số 03/2021/TT-BXD ngày 19 tháng 5 năm 2021 của Bộ trưởng Bộ Xây dựng.")
    lines.append("")
    lines.append("Sửa đổi 01:2026 QCVN 04:2021/BXD do Viện Khoa học công nghệ xây dựng biên soạn, Cục Quản lý nhà và thị trường bất động sản trình thẩm định, Vụ Khoa học công nghệ môi trường và Vật liệu xây dựng thẩm định, Bộ Xây dựng ban hành kèm theo Thông tư số 31/2026/TT-BXD ngày 15 tháng 06 năm 2026 của Bộ trưởng Bộ Xây dựng (có hiệu lực từ ngày 15 tháng 12 năm 2026).")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Process base lines
    base_lines = base_text.splitlines()
    
    idx_muc1 = 0
    for i, l in enumerate(base_lines):
        if '<a id="muc-1"></a>' in l:
            idx_muc1 = i
            break
            
    base_content = "\n".join(base_lines[idx_muc1:])
    
    # 1. Insert 1.1.3 after 1.1.2
    sd1_113 = """
#### <a id="muc-1-1-3" name="muc-1-1-3"></a>1.1.3 *(Bổ sung bởi Sửa đổi 01:2026)*

Các quy định liên quan đến chỗ để xe, chỗ để xe điện và khu vực đổi pin áp dụng đối với nhà chung cư xây mới và nhà chung cư hiện hữu.
"""
    base_content = re.sub(
        r'(<a id="muc-1-1-2"></a>\s*### 1\.1\.2\s*[\s\S]*?)(?=<a id="muc-1-2">)',
        r'\1' + sd1_113.strip() + '\n\n',
        base_content
    )
    
    # 2. Append QCVN 10:2025/BCA to 1.3
    sd1_13_extra = """
QCVN 10:2025/BCA, *Quy chuẩn kỹ thuật quốc gia về trang bị, bố trí phương tiện phòng cháy, chữa cháy, cứu nạn, cứu hộ cho nhà và công trình.* *(Bổ sung bởi Sửa đổi 01:2026)*
"""
    base_content = re.sub(
        r'(<a id="muc-1-3"></a>\s*### 1\.3[\s\S]*?)(?=<a id="muc-1-4">)',
        r'\1\n' + sd1_13_extra.strip() + '\n\n',
        base_content
    )
    
    # 3. Append 1.4.31 to 1.4.34 to 1.4
    sd1_defs = """
#### <a id="muc-1-4-31" name="muc-1-4-31"></a>1.4.31  Nhà chung cư hiện hữu *(Bổ sung bởi Sửa đổi 01:2026)*

Nhà chung cư đã được nghiệm thu, đưa vào sử dụng theo quy định của pháp luật về xây dựng trước thời điểm quy chuẩn này có hiệu lực.

#### <a id="muc-1-4-32" name="muc-1-4-32"></a>1.4.32  Khu vực sạc xe điện *(Bổ sung bởi Sửa đổi 01:2026)*

Khu vực có chức năng chuyên để sạc xe điện, gồm một hoặc nhiều chỗ sạc được bố trí tập trung, được trang bị hệ thống cấp điện, thiết bị sạc và các biện pháp an toàn cần thiết để thực hiện việc sạc năng lượng cho xe điện.

#### <a id="muc-1-4-33" name="muc-1-4-33"></a>1.4.33  Chỗ sạc *(Bổ sung bởi Sửa đổi 01:2026)*

Vị trí đỗ dành cho một xe để thực hiện sạc điện.

#### <a id="muc-1-4-34" name="muc-1-4-34"></a>1.4.34  Khu vực đổi pin *(Bổ sung bởi Sửa đổi 01:2026)*

Khu vực lắp đặt tủ đổi pin cho xe mô tô điện, xe gắn máy điện, xe đạp điện, nơi pin có thể hoán đổi.
"""
    base_content = re.sub(
        r'(<a id="muc-1-4"></a>\s*### 1\.4[\s\S]*?)(?=<a id="muc-2">)',
        r'\1\n' + sd1_defs.strip() + '\n\n',
        base_content
    )
    
    # 4. Extract 2.10 and 2.11 from SD1
    m_sd1_ch2 = re.search(r"### <a id=\"sd1-muc-2-10\"[\s\S]*?(?=---|\Z)", sd1_text)
    if not m_sd1_ch2:
        m_sd1_ch2 = re.search(r"(?:### <a id=\"sd1-muc-2-10\"|2\.10\s*Yêu cầu về chỗ để xe điện)[\s\S]*?(?=---|\Z)", sd1_text)
    sd1_tech_section = m_sd1_ch2.group(0).strip() if m_sd1_ch2 else ""
    
    # Clean anchor prefixes in SD1 section: sd1-muc- -> muc-
    sd1_tech_section = re.sub(r'id="sd1-muc-([^"]+)"\s*name="sd1-muc-([^"]+)"', r'id="muc-\1" name="muc-\1"', sd1_tech_section)
    sd1_tech_section = re.sub(r'<a id="sd1-muc-([^"]+)"></a>', r'<a id="muc-\1"></a>', sd1_tech_section)
    
    sd1_tech_block = f"""
> [!IMPORTANT]
> **BỔ SUNG QUY ĐỊNH KỸ THUẬT VỀ XE ĐIỆN, TRẠM SẠC VÀ ĐỔI PIN (SỬA ĐỔI 01:2026 / TT 31/2026/TT-BXD):**

{sd1_tech_section}
"""
    # Insert 2.10 and 2.11 after 2.9 (before Chapter 3)
    base_content = re.sub(
        r'(<a id="muc-2-9"></a>\s*### 2\.9[\s\S]*?)(?=<a id="muc-3">)',
        r'\1\n' + sd1_tech_block.strip() + '\n\n---\n\n',
        base_content
    )
    
    # 5. Chapter 3 additions: 3.3 additions, 3.4, 3.5
    sd1_ch3_add = """
> [!IMPORTANT]
> **Quy định chuyển tiếp đối với khu vực để xe điện, trạm sạc, đổi pin (Sửa đổi 01:2026):**
> - Đối với chỗ để xe, khu vực để xe điện, khu vực sạc xe điện, khu vực đổi pin của nhà chung cư xây mới, nhà chung cư hiện hữu thực hiện như sau:
>   + Thiết kế về phòng cháy và chữa cháy khu vực để xe điện, khu vực sạc xe điện, khu vực đổi pin đã được cơ quan có thẩm quyền thẩm định hoặc thẩm duyệt, hoặc đáp ứng các yêu cầu của cơ quan có thẩm quyền theo quy định pháp luật về phòng cháy và chữa cháy trước thời điểm quy chuẩn này có hiệu lực, thì tiếp tục thực hiện.
>   + Thiết kế về phòng cháy và chữa cháy đã được cơ quan có thẩm quyền thẩm định hoặc thẩm duyệt nhưng chưa có khu vực để xe điện, khu vực sạc xe điện, khu vực đổi pin trước thời điểm quy chuẩn này có hiệu lực, phải rà soát để tuân thủ các quy định của quy chuẩn này.
>   + Thiết kế về phòng cháy và chữa cháy đối với khu vực để xe điện, khu vực sạc xe điện, khu vực đổi pin sau thời điểm quy chuẩn này có hiệu lực phải tuân thủ các quy định của quy chuẩn này.

<a id="muc-3-4"></a>
### 3.4 *(Bổ sung bởi Sửa đổi 01:2026)*

Chủ đầu tư, chủ sở hữu, ban quản trị, đơn vị quản lý, khai thác vận hành khu vực để xe điện, khu vực sạc xe điện, khu vực đổi pin thực hiện việc quản lý, vận hành đảm bảo hoạt động an toàn, đúng công năng thiết kế phải tuân thủ các quy định của quy chuẩn này.

<a id="muc-3-5"></a>
### 3.5 *(Bổ sung bởi Sửa đổi 01:2026)*

Khu vực để xe điện, khu vực sạc xe điện, khu vực đổi pin phải được giám sát 24/24 giờ.
"""
    base_content = re.sub(
        r'(<a id="muc-3-3"></a>\s*### 3\.3[\s\S]*?)(?=<a id="muc-4">)',
        r'\1\n' + sd1_ch3_add.strip() + '\n\n',
        base_content
    )
    
    # 6. Chapter 4 additions: 4.1a, 4.1b, 4.3 update
    sd1_ch4_add = """
<a id="muc-4-1a"></a>
### 4.1a *(Bổ sung bởi Sửa đổi 01:2026)*

Mọi tổ chức, cá nhân khi tham gia các hoạt động liên quan lắp đặt, quản lý, vận hành khu vực để xe điện, khu vực sạc xe điện, khu vực đổi pin của nhà chung cư phải tuân thủ các quy định của quy chuẩn này.

<a id="muc-4-1b"></a>
### 4.1b *(Bổ sung bởi Sửa đổi 01:2026)*

Cơ quan có thẩm quyền theo quy định pháp luật về phòng cháy chữa cháy có trách nhiệm kiểm tra việc tuân thủ các quy định của quy chuẩn này.
"""
    base_content = re.sub(
        r'(<a id="muc-4-1"></a>\s*### 4\.1[\s\S]*?)(?=<a id="muc-4-2">)',
        r'\1\n' + sd1_ch4_add.strip() + '\n\n',
        base_content
    )
    
    # Update 4.3
    base_content = re.sub(
        r'<a id="muc-4-3"></a>\s*### 4\.3[\s\S]*?(?=<a id="muc-5">)',
        r'<a id="muc-4-3"></a>\n### 4.3 *(Sửa đổi bởi Sửa đổi 01:2026)*\n\nTrong quá trình triển khai thực hiện, nếu có vướng mắc, mọi ý kiến gửi về Bộ Xây dựng để được hướng dẫn và xử lý.\n\n',
        base_content
    )

    full_md = "\n".join(lines) + base_content
    HOPNHAT_MD.write_text(full_md, encoding="utf-8")
    print(f"✅ Generated Full Consolidated OKF Markdown: {HOPNHAT_MD} ({HOPNHAT_MD.stat().st_size:,} bytes)")

    # Parse clauses for clauses.json
    clauses = []
    clause_pattern = re.compile(
        r'(?:<a id="([^"]+)"></a>\s*)?(?:###|####)\s*(?:<a id="([^"]+)"[^>]*></a>\s*)?([0-9]+(?:\.[0-9]+[a-z]?)*)\s*(.*?)(?=\n(?:<a id="[^"]+"></a>\s*)?(?:###|####|\Z))',
        re.DOTALL
    )

    for m in clause_pattern.finditer(full_md):
        cid1, cid2, num, rest = m.groups()
        cid = cid2 or cid1 or f"muc-{num.replace('.', '-')}"
        rest_lines = rest.strip().splitlines()
        title_line = rest_lines[0] if rest_lines else ""
        content = "\n".join(rest_lines[1:]).strip() if len(rest_lines) > 1 else ""
        full_title = f"{num} {title_line}".strip()

        clauses.append({
            "id": cid,
            "clause_number": num,
            "title": full_title,
            "content": content
        })

    CLAUSES_FILE.write_text(json.dumps(clauses, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Generated AST Clauses: {CLAUSES_FILE} ({len(clauses)} clauses)")

    # Build QA benchmark
    qa_list = []
    for c in clauses:
        num = c["clause_number"]
        title = c["title"]
        qa_list.append({
            "question": f"Quy định kỹ thuật tại mục {num} ({title}) của QCVN 04:2021/BXD (Hợp nhất 2026) quy định như thế nào?",
            "ground_truth_clause": num,
            "ground_truth_id": c["id"],
            "expected_keywords": [w for w in title.split() if len(w) > 3][:4]
        })

    QA_FILE.write_text(json.dumps(qa_list, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Generated QA Benchmark: {QA_FILE} ({len(qa_list)} QA pairs)")

if __name__ == "__main__":
    build_hopnhat()
