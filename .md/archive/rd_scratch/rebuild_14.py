import docx
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(".")
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_04_2021_bxd"
BASE_MD = BUNDLE_DIR / "qcvn_04_2021_bxd.md"

doc = docx.Document(r".md/extracted_docs/qcvn_04_2021_bxd/qcvn_04_2021_bxd.docx")

# Parse definitions
defs = []
current_num = None
current_term = None
current_body = []
in_14 = False

for p in doc.paragraphs:
    t = p.text.strip()
    if not t:
        continue
    if "1.4" in t and "Giải thích từ ngữ" in t:
        in_14 = True
        continue
    if in_14:
        if "2." in t and "QUY ĐỊNH KỸ THUẬT" in t or t.startswith("2  Quy định kỹ thuật"):
            break
        # Match 1.4.X
        m = re.match(r"^1\.4\.(\d+)$", t)
        if m:
            if current_num:
                defs.append((current_num, current_term, current_body))
            current_num = f"1.4.{m.group(1)}"
            current_term = None
            current_body = []
        elif current_num and current_term is None:
            current_term = t
        elif current_num:
            current_body.append(t)

if current_num:
    defs.append((current_num, current_term, current_body))

print(f"Total definitions parsed: {len(defs)}")

# Format section 1.4
lines_14 = []
lines_14.append('<a id="muc-1-4"></a>')
lines_14.append("### 1.4  Giải thích từ ngữ")
lines_14.append("")
lines_14.append("Trong quy chuẩn này, các thuật ngữ, định nghĩa dưới đây được hiểu như sau:")
lines_14.append("")

for num, term, body_paras in defs:
    anchor_id = f"muc-{num.replace('.', '-')}"
    lines_14.append(f'#### <a id="{anchor_id}" name="{anchor_id}"></a>{num}  {term}')
    lines_14.append("")
    
    # Process paragraphs and notes
    notes = [p for p in body_paras if p.startswith("CHÚ THÍCH") or p.startswith("GHI CHÚ")]
    main_paras = [p for p in body_paras if not (p.startswith("CHÚ THÍCH") or p.startswith("GHI CHÚ"))]
    
    for p in main_paras:
        lines_14.append(p)
        lines_14.append("")
        
    if len(notes) == 1:
        note_clean = re.sub(r'^(?:GHI CHÚ|CHÚ THÍCH):\s*', '', notes[0])
        lines_14.append(f'_CHÚ THÍCH: {note_clean}_')
        lines_14.append("")
    elif len(notes) > 1:
        lines_14.append("_CHÚ THÍCH:_")
        for n in notes:
            # Check CHÚ THÍCH X:
            m_note = re.match(r'^(?:CHÚ THÍCH|GHI CHÚ)\s*(\d+):\s*(.*)', n)
            if m_note:
                lines_14.append(f"- **CHÚ THÍCH {m_note.group(1)}:** {m_note.group(2)}")
            else:
                lines_14.append(f"- {n}")
        lines_14.append("")

sec_14_md = "\n".join(lines_14)

# Replace in BASE_MD
base_text = BASE_MD.read_text(encoding="utf-8")
base_text = re.sub(
    r'<a id="muc-1-4"></a>\s*### 1\.4[\s\S]*?(?=<a id="muc-2">)',
    sec_14_md + "\n",
    base_text
)
BASE_MD.write_text(base_text, encoding="utf-8")
print("✅ Replaced section 1.4 in base QCVN 04 markdown with polished notes!")
