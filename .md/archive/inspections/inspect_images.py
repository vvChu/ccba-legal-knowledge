import sys
import zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.docx"

with zipfile.ZipFile(docx_path, 'r') as z:
    doc_xml = z.read('word/document.xml')
    root = ET.fromstring(doc_xml)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
          'v': 'urn:schemas-microsoft-com:vml',
          'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
    
    for i, p in enumerate(root.findall('.//w:p', ns)):
        imagedatas = p.findall('.//v:imagedata', ns)
        if imagedatas:
            for img in imagedatas:
                rel_id = img.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                p_text = ''.join([t.text for t in p.findall('.//w:t', ns) if t.text])
                print(f"Paragraph {i} has image {rel_id}: '{p_text}'")

