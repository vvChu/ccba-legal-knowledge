import sys
import zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.docx"

with zipfile.ZipFile(docx_path, 'r') as z:
    doc_xml = z.read('word/document.xml')
    root = ET.fromstring(doc_xml)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    all_p = root.findall('.//w:p', ns)
    
    for target in [351, 586, 629]:
        print(f"\n=== AROUND PARAGRAPH {target} ===")
        start = max(0, target - 3)
        end = min(len(all_p), target + 4)
        for idx in range(start, end):
            p = all_p[idx]
            txt = ''.join([t.text for t in p.findall('.//w:t', ns) if t.text]).strip()
            print(f"  P[{idx}]: {txt[:100]}")
