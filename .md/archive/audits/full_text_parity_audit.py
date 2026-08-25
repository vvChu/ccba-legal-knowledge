import docx
import json
import re

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)
with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Normalize text for fuzzy matching: lowercase, strip punctuation and whitespace
def norm(t):
    return re.sub(r'[\s\.,:;\-_/\(\)\[\]"\'“”‘’]+', '', t.lower())

norm_md = norm(md_content)

docx_para_audit = []
missing_in_md = []
matched_in_md = []

# Chapters & Appendices ranges in DOCX
# p0 - p21: TOC
# p22 - p233: Chapter 1
# p234 - p442: Chapter 2
# p443 - p715: Chapter 3
# p716 - p829: Chapter 4
# p830 - p1079: Chapter 5
# p1080 - p1205: Chapter 6
# p1206 - p1211: Chapter 7
# p1212 - p1466: Appendix A
# p1467 - p1496: Appendix B
# p1497 - p1570: Appendix C
# p1571 - p1738: Appendix D
# p1739 - p1768: Appendix E
# p1769 - p1796: Appendix F
# p1797 - p1849: Appendix G
# p1850 - p1967: Appendix H
# p1968 - p2036: Appendix I

for i, p in enumerate(doc.paragraphs):
    if i < 22:
        continue # Skip TOC
    t = p.text.strip()
    if not t:
        continue
        
    nt = norm(t)
    # Check if first 30 chars of normalized text is in normalized MD
    snip = nt[:30] if len(nt) >= 30 else nt
    
    is_match = snip in norm_md if len(snip) >= 5 else (t in md_content)
    
    entry = {
        'docx_p_idx': i,
        'text': t,
        'style': p.style.name if p.style else '',
        'matched': is_match
    }
    
    docx_para_audit.append(entry)
    if is_match:
        matched_in_md.append(entry)
    else:
        missing_in_md.append(entry)

print(f"Total evaluated DOCX paragraphs: {len(docx_para_audit)}")
print(f"Matched paragraphs in MD: {len(matched_in_md)} ({len(matched_in_md)/len(docx_para_audit)*100:.2f}%)")
print(f"Missing/Unmatched paragraphs in MD: {len(missing_in_md)} ({len(missing_in_md)/len(docx_para_audit)*100:.2f}%)")

# Breakdown by Chapter and Appendix
section_boundaries = [
    ("Chapter 1", 22, 233),
    ("Chapter 2", 234, 442),
    ("Chapter 3", 443, 715),
    ("Chapter 4", 716, 829),
    ("Chapter 5", 830, 1079),
    ("Chapter 6", 1080, 1205),
    ("Chapter 7", 1206, 1211),
    ("Appendix A", 1212, 1466),
    ("Appendix B", 1467, 1496),
    ("Appendix C", 1497, 1570),
    ("Appendix D", 1571, 1738),
    ("Appendix E", 1739, 1768),
    ("Appendix F", 1769, 1796),
    ("Appendix G", 1797, 1849),
    ("Appendix H", 1850, 1967),
    ("Appendix I", 1968, 2036),
]

section_breakdown = []
for name, start_p, end_p in section_boundaries:
    sec_paras = [e for e in docx_para_audit if start_p <= e['docx_p_idx'] <= end_p]
    sec_matched = [e for e in sec_paras if e['matched']]
    sec_missing = [e for e in sec_paras if not e['matched']]
    
    total = len(sec_paras)
    matched = len(sec_matched)
    rate = (matched / total * 100) if total else 0
    
    section_breakdown.append({
        'section': name,
        'docx_range': f"p{start_p}-p{end_p}",
        'total_paras': total,
        'matched_paras': matched,
        'missing_paras': len(sec_missing),
        'parity_rate': f"{rate:.1f}%",
        'missing_examples': [m['text'][:120] for m in sec_missing[:5]]
    })

report = {
    'total_docx_paragraphs': len(docx_para_audit),
    'total_matched': len(matched_in_md),
    'total_missing': len(missing_in_md),
    'overall_parity_rate': f"{len(matched_in_md)/len(docx_para_audit)*100:.2f}%",
    'section_breakdown': section_breakdown,
    'all_missing_paragraphs': missing_in_md
}

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\full_text_parity_audit.json', 'w', encoding='utf-8') as out:
    json.dump(report, out, ensure_ascii=False, indent=2)

print("Full text parity audit completed.")
