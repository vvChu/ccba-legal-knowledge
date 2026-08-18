import re

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\md_structural_landmarks.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out_lines = ["--- MAJOR CHAPTERS AND APPENDICES IN MD ---\n"]
for l in lines:
    m = re.search(r'Line\s+(\d+):\s+###\s+([1-7]\s+[A-ZĐÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ\s\-,:]{3,}|PHỤ LỤC\s+[A-I]|Phụ lục\s+[A-I])', l)
    if m:
        out_lines.append(f"Line {m.group(1)}: {m.group(2)}\n")

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\md_major_divisions.txt', 'w', encoding='utf-8') as f:
    f.writelines(out_lines)

print("Saved md_major_divisions.txt")
