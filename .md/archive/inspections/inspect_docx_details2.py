import sys
import zipfile
import xml.etree.ElementTree as ET
import docx

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.docx"

with zipfile.ZipFile(docx_path, 'r') as z:
    doc_xml = z.read('word/document.xml')
    root = ET.fromstring(doc_xml)
    
    print(f"=== ALL XML TAGS WITH 'image' or 'blip' or 'drawing' or 'pict' ===")
    for elem in root.iter():
        if any(k in elem.tag.lower() for k in ['blip', 'image', 'drawing', 'pict', 'graphic']):
            print(f"Tag: {elem.tag}, attrib: {elem.attrib}")

    # Check relationships
    if 'word/_rels/document.xml.rels' in z.namelist():
        rels_xml = z.read('word/_rels/document.xml.rels')
        rels_root = ET.fromstring(rels_xml)
        print("\n=== DOCUMENT.XML RELATIONSHIPS ===")
        for rel in rels_root:
            print(f"ID: {rel.attrib.get('Id')}, Type: {rel.attrib.get('Type')}, Target: {rel.attrib.get('Target')}")

