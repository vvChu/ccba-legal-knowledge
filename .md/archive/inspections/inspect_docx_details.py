import zipfile
import xml.etree.ElementTree as ET
import docx

docx_path = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.docx"

with zipfile.ZipFile(docx_path, 'r') as z:
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
          'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
          'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    
    # 1. Footnotes & Endnotes
    for part in ['word/footnotes.xml', 'word/endnotes.xml']:
        if part in z.namelist():
            root = ET.fromstring(z.read(part))
            print(f"\n--- {part} ---")
            for elem in root.findall('.//w:footnote', ns) + root.findall('.//w:endnote', ns):
                fn_id = elem.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type', elem.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id'))
                texts = [''.join([t.text for t in p.findall('.//w:t', ns) if t.text]) for p in elem.findall('.//w:p', ns)]
                texts = [t for t in texts if t.strip()]
                print(f"  ID {elem.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')}: {texts}")

    # 2. Images in document.xml
    doc_xml = z.read('word/document.xml')
    doc_root = ET.fromstring(doc_xml)
    
    # Find blip references
    blips = doc_root.findall('.//*[@r:embed]', {'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'})
    print(f"\n--- Embedded Images in document.xml ({len(blips)}) ---")
    for b in blips:
        print(f"  Tag: {b.tag}, Embed ID: {b.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')}")
        
    # Find surrounding paragraphs of drawing/images
    for p_idx, p in enumerate(doc_root.findall('.//w:p', ns)):
        drawings = p.findall('.//w:drawing', ns)
        if drawings:
            p_text = ''.join([t.text for t in p.findall('.//w:t', ns) if t.text])
            print(f"  P[{p_idx}] with drawing: '{p_text}'")

doc = docx.Document(docx_path)
print(f"\n--- Tables Detail ---")
for i, tbl in enumerate(doc.tables):
    print(f"Table {i+1}: {len(tbl.rows)} rows x {len(tbl.columns)} cols")
    for r_idx, row in enumerate(tbl.rows):
        row_txt = [c.text.replace('\n', ' ').strip() for c in row.cells]
        print(f"  Row {r_idx}: {row_txt[:5]}")
