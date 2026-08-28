import docx
import sys
sys.stdout.reconfigure(encoding="utf-8")

doc = docx.Document(r".md/extracted_docs/qcvn_04_2021_bxd/qcvn_04_2021_bxd.docx")
for i, p in enumerate(doc.paragraphs[:100]):
    t = p.text.strip()
    if t:
        print(f"{i:2d}: {t[:60]}")
