import docx
import re
import json

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)
with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()
    md_lines = md_content.splitlines()

# 1. DOCX Headings & Clauses extraction
# We look for all numbered clauses like X.Y, X.Y.Z, X.Y.Z.W, or Phụ lục headings, or Bang headings
re_clause = re.compile(r'^(([1-7]|[A-I])\.[0-9]+(\.[0-9]+)*)\s*(.*)$')
re_appendix = re.compile(r'^(PHỤ LỤC|Phụ lục)\s+([A-I])\b(.*)$', re.IGNORECASE)
re_table = re.compile(r'^(Bảng|BẢNG)\s+([A-I0-9]+(\.[0-9]+)?|[0-9]+)\s*[-–:]\s*(.*)$', re.IGNORECASE)
re_chapter = re.compile(r'^([1-7])\s+([A-ZĐÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ\s\-,:]{3,})$')

docx_structure = []
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    
    # Skip table of contents at the beginning (paragraphs 0 to 50)
    if i < 22:
        continue
        
    m_chap = re_chapter.match(t)
    m_app = re_appendix.match(t)
    m_tbl = re_table.match(t)
    m_cls = re_clause.match(t)
    
    entry = None
    if m_chap:
        entry = {'type': 'chapter', 'p_idx': i, 'id': m_chap.group(1), 'title': m_chap.group(2).strip(), 'raw': t}
    elif m_app:
        entry = {'type': 'appendix', 'p_idx': i, 'id': m_app.group(2).upper(), 'title': m_app.group(3).strip(), 'raw': t}
    elif m_tbl:
        entry = {'type': 'table', 'p_idx': i, 'id': m_tbl.group(2), 'title': m_tbl.group(4).strip(), 'raw': t}
    elif m_cls:
        entry = {'type': 'clause', 'p_idx': i, 'id': m_cls.group(1), 'title': m_cls.group(4).strip(), 'raw': t}
    elif p.style and p.style.name.startswith('Heading'):
        entry = {'type': 'heading_style', 'p_idx': i, 'id': '', 'title': t, 'raw': t}
        
    if entry:
        docx_structure.append(entry)

print(f"Total DOCX structural items extracted: {len(docx_structure)}")

# 2. Markdown Headings & Clauses extraction
md_structure = []
for idx, line in enumerate(md_lines):
    l_strip = line.strip()
    if not l_strip:
        continue
    
    # Match markdown headings or bold clause headers
    # e.g., ### 1.1 ..., ### Bảng 1 ..., __A.1.1.1__ ...
    is_struct = False
    stype = 'unknown'
    sid = ''
    stitle = ''
    
    m_md_h = re.match(r'^(#+)\s*(.*)$', l_strip)
    m_md_b = re.match(r'^(__|\*\*)([A-I0-9\.\s]+)(__|\*\*)\s*(.*)$', l_strip)
    
    if m_md_h:
        htext = m_md_h.group(2).strip()
        m_chap = re_chapter.match(htext)
        m_app = re_appendix.match(htext)
        m_tbl = re_table.match(htext)
        m_cls = re_clause.match(htext)
        
        if m_chap:
            stype = 'chapter'; sid = m_chap.group(1); stitle = m_chap.group(2).strip()
        elif m_app:
            stype = 'appendix'; sid = m_app.group(2).upper(); stitle = m_app.group(3).strip()
        elif m_tbl:
            stype = 'table'; sid = m_tbl.group(2); stitle = m_tbl.group(4).strip()
        elif m_cls:
            stype = 'clause'; sid = m_cls.group(1); stitle = m_cls.group(4).strip()
        else:
            stype = f"h{len(m_md_h.group(1))}"; stitle = htext
            
        md_structure.append({
            'line': idx + 1,
            'type': stype,
            'id': sid,
            'title': stitle,
            'raw': l_strip
        })
    elif m_md_b:
        b_id = m_md_b.group(2).strip()
        b_rem = m_md_b.group(4).strip()
        m_app = re_appendix.match(b_id)
        m_cls = re_clause.match(b_id)
        m_tbl = re_table.match(b_id)
        
        if m_app:
            stype = 'appendix'; sid = m_app.group(2).upper(); stitle = b_rem
        elif m_cls:
            stype = 'clause'; sid = m_cls.group(1); stitle = b_rem
        elif m_tbl:
            stype = 'table'; sid = m_tbl.group(2); stitle = b_rem
        else:
            stype = 'bold_header'; sid = b_id; stitle = b_rem
            
        md_structure.append({
            'line': idx + 1,
            'type': stype,
            'id': sid,
            'title': stitle,
            'raw': l_strip
        })

print(f"Total MD structural items extracted: {len(md_structure)}")

# 3. Cross comparison
docx_clauses = [item for item in docx_structure if item['type'] == 'clause']
md_clauses = [item for item in md_structure if item['type'] == 'clause']

print(f"DOCX clauses: {len(docx_clauses)}")
print(f"MD clauses: {len(md_clauses)}")

# Check matching clauses
docx_clause_ids = set(c['id'] for c in docx_clauses)
md_clause_ids = set(c['id'] for c in md_clauses)

missing_in_md = sorted(list(docx_clause_ids - md_clause_ids))
extra_in_md = sorted(list(md_clause_ids - docx_clause_ids))

print(f"Clause IDs in DOCX but missing in MD: {len(missing_in_md)}")
print(f"Clause IDs in MD but not in DOCX: {len(extra_in_md)}")

out_result = {
    'docx_clause_count': len(docx_clauses),
    'md_clause_count': len(md_clauses),
    'missing_in_md_count': len(missing_in_md),
    'missing_in_md_sample': missing_in_md,
    'extra_in_md_count': len(extra_in_md),
    'extra_in_md_sample': extra_in_md,
    'docx_structure_sample': docx_structure[:50],
    'md_structure_sample': md_structure[:50]
}

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\clause_parity_audit.json', 'w', encoding='utf-8') as out:
    json.dump(out_result, out, ensure_ascii=False, indent=2)

print("Clause parity audit completed.")
