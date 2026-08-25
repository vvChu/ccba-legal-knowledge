import docx
import re
import json

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)

# Extract paragraphs from DOCX with index
docx_data = []
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t:
        docx_data.append({
            'p_idx': i,
            'text': t,
            'style': p.style.name if p.style else '',
            'is_bold': any(r.bold for r in p.runs)
        })

# Read MD lines
with open(md_path, 'r', encoding='utf-8') as f:
    md_lines = [l.rstrip('\r\n') for l in f.readlines()]

# Parse Chapters and Appendices inventory
# Major sections:
# Chapter 1: 1. QUY ĐỊNH CHUNG
# Chapter 2: 2. PHÂN LOẠI KỸ THUẬT VỀ CHÁY
# Chapter 3: 3. BẢO ĐẢM AN TOÀN CHO NGƯỜI
# Chapter 4: 4. NGĂN CHẶN CHÁY LAN
# Chapter 5: 5. CẤP NƯỚC CHỮA CHÁY
# Chapter 6: 6. CHỮA CHÁY VÀ CỨU NẠN
# Chapter 7: 7. QUY ĐỊNH VỀ QUẢN LÝ
# Phụ lục A: QUY ĐỊNH BỔ SUNG ĐỐI VỚI MỘT SỐ NHÓM NHÀ CỤ THỂ
# Phụ lục B: PHÂN LOẠI VẬT LIỆU XÂY DỰNG THEO CÁC ĐẶC TÍNH KỸ THUẬT VỀ CHÁY
# Phụ lục C: HẠNG NGUY HIỂM CHÁY VÀ CHÁY NỔ CỦA NHÀ, CÔNG TRÌNH VÀ GIAN PHÒNG THEO CÔNG NĂNG
# Phụ lục D: CÁC QUY ĐỊNH VỀ KHOẢNG CÁCH PHÒNG CHÁY CHỐNG CHÁY
# Phụ lục E: CÁC YÊU CẦU VỀ TRANG BỊ HỆ THỐNG CẤP NƯỚC CHỮA CHÁY
# Phụ lục F: GIỚI HẠN CHỊU LỬA DANH ĐỊNH CỦA MỘT SỐ KẾT CẤU CẤU KIỆN
# Phụ lục G: KHOẢNG CÁCH ĐẾN CÁC LỐI THOÁT NẠN VÀ CHIỀU RỘNG CỦA LỐI THOÁT NẠN
# Phụ lục H: BẬC CHỊU LỬA VÀ CÁC YÊU CẦU VỀ AN TOÀN CHÁY ĐỐI VỚI NHÀ, CÔNG TRÌNH, KHOANG CHÁY
# Phụ lục I: CƠ SỞ TÍNH TOÁN BẬC CHỊU LỬA VÀ SỐ TẦNG CHO PHÉP CỦA NHÀ

sections_def = [
    {"id": "CH1", "name": "Chương 1: Quy định chung", "pattern_docx": r"^(1\s+QUY ĐỊNH CHUNG|1\.\s+QUY ĐỊNH CHUNG)", "pattern_md": r"^###\s+1\s+QUY ĐỊNH CHUNG"},
    {"id": "CH2", "name": "Chương 2: Phân loại kỹ thuật về cháy", "pattern_docx": r"^(2\s+PHÂN LOẠI|2\.\s+PHÂN LOẠI)", "pattern_md": r"^###\s+2\s+PHÂN LOẠI"},
    {"id": "CH3", "name": "Chương 3: Bảo đảm an toàn cho người", "pattern_docx": r"^(3\s+BẢO ĐẢM|3\.\s+BẢO ĐẢM)", "pattern_md": r"^###\s+3\s+BẢO ĐẢM"},
    {"id": "CH4", "name": "Chương 4: Ngăn chặn cháy lan", "pattern_docx": r"^(4\s+NGĂN CHẶN|4\.\s+NGĂN CHẶN)", "pattern_md": r"^###\s+4\s+NGĂN CHẶN"},
    {"id": "CH5", "name": "Chương 5: Cấp nước chữa cháy", "pattern_docx": r"^(5\s+CẤP NƯỚC|5\.\s+CẤP NƯỚC)", "pattern_md": r"^###\s+5\s+CẤP NƯỚC"},
    {"id": "CH6", "name": "Chương 6: Chữa cháy và cứu nạn", "pattern_docx": r"^(6\s+CHỮA CHÁY|6\.\s+CHỮA CHÁY)", "pattern_md": r"^###\s+6\s+CHỮA CHÁY"},
    {"id": "CH7", "name": "Chương 7: Quy định về quản lý", "pattern_docx": r"^(7\s+QUY ĐỊNH|7\.\s+QUY ĐỊNH)", "pattern_md": r"^###\s+7\s+QUY ĐỊNH"},
    {"id": "PLA", "name": "Phụ lục A", "pattern_docx": r"^PHỤ LỤC\s+A\b", "pattern_md": r"^###\s+PHỤ LỤC\s+A\b"},
    {"id": "PLB", "name": "Phụ lục B", "pattern_docx": r"^PHỤ LỤC\s+B\b", "pattern_md": r"^###\s+PHỤ LỤC\s+B\b"},
    {"id": "PLC", "name": "Phụ lục C", "pattern_docx": r"^PHỤ LỤC\s+C\b", "pattern_md": r"^###\s+PHỤ LỤC\s+C\b"},
    {"id": "PLD", "name": "Phụ lục D", "pattern_docx": r"^PHỤ LỤC\s+D\b", "pattern_md": r"^###\s+PHỤ LỤC\s+D\b"},
    {"id": "PLE", "name": "Phụ lục E", "pattern_docx": r"^PHỤ LỤC\s+E\b", "pattern_md": r"^###\s+PHỤ LỤC\s+E\b"},
    {"id": "PLF", "name": "Phụ lục F", "pattern_docx": r"^PHỤ LỤC\s+F\b", "pattern_md": r"^###\s+PHỤ LỤC\s+F\b"},
    {"id": "PLG", "name": "Phụ lục G", "pattern_docx": r"^PHỤ LỤC\s+G\b", "pattern_md": r"^###\s+PHỤ LỤC\s+G\b"},
    {"id": "PLH", "name": "Phụ lục H", "pattern_docx": r"^PHỤ LỤC\s+H\b", "pattern_md": r"^###\s+PHỤ LỤC\s+H\b"},
    {"id": "PLI", "name": "Phụ lục I", "pattern_docx": r"^PHỤ LỤC\s+I\b", "pattern_md": r"^###\s+PHỤ LỤC\s+I\b"},
]

# Find start line in MD and start para in DOCX for each section
inventory = []
for s in sections_def:
    docx_match = None
    for p in docx_data:
        if re.search(s['pattern_docx'], p['text'], re.IGNORECASE):
            docx_match = p
            break
            
    md_match = None
    for idx, l in enumerate(md_lines):
        if re.search(s['pattern_md'], l.strip(), re.IGNORECASE):
            md_match = {'line_num': idx + 1, 'text': l.strip()}
            break
            
    inventory.append({
        'id': s['id'],
        'name': s['name'],
        'docx_start_p': docx_match['p_idx'] if docx_match else None,
        'docx_text': docx_match['text'] if docx_match else None,
        'md_start_line': md_match['line_num'] if md_match else None,
        'md_text': md_match['text'] if md_match else None,
    })

# Check numbering corruption patterns in MD
# e.g., 1.4.1.7 instead of 1.4.17
corruption_patterns = []
re_bad_num = re.compile(r'###\s+(([0-9A-I]+\.)+[0-9]+)')
for idx, l in enumerate(md_lines):
    m = re.search(r'###\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\b', l)
    if m:
        # Check if this 4-part number like 1.4.1.7 was really 1.4.17
        num_str = m.group(1)
        # Check if third part is 1 and 4th part is 0-9
        parts = num_str.split('.')
        if len(parts) == 4 and parts[0] == '1' and parts[1] == '4':
            corruption_patterns.append({
                'line': idx + 1,
                'found': num_str,
                'expected': f"{parts[0]}.{parts[1]}.{parts[2]}{parts[3]}",
                'raw': l
            })

# Check escape characters in MD
escape_issues = []
for idx, l in enumerate(md_lines):
    # check for \. or \_ or \[ or \] or \* in unusual places
    escaped = re.findall(r'\\[\._\-*#\[\]\(\)]', l)
    if escaped:
        escape_issues.append({
            'line': idx + 1,
            'escapes': list(set(escaped)),
            'raw': l[:120]
        })

report = {
    'inventory': inventory,
    'corruption_patterns_sample': corruption_patterns,
    'total_corruption_detected': len(corruption_patterns),
    'escape_issues_count': len(escape_issues),
    'escape_issues_sample': escape_issues[:30]
}

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\detailed_survey_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("Detailed survey report generated.")
