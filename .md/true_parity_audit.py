import docx
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)
with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Strip markdown formatting: #, *, _, `, etc.
clean_md = re.sub(r'[#\*_`\<\>\[\]\(\)]', '', md_content)
# Normalize spaces
clean_md = ' '.join(clean_md.split())

def norm_clean(t):
    # remove all non-alphanumeric except dots and digits
    return re.sub(r'[^\w\d]+', '', t.lower())

norm_md_str = norm_clean(clean_md)

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

true_audit = []
overall_matched = 0
overall_total = 0

all_unmatched_details = []

print("=================================================================")
print("     QCVN 06:2022/BXD TRUE PARAGRAPH PARITY AUDIT               ")
print("=================================================================")

for name, start_p, end_p in section_boundaries:
    sec_paras = []
    for i in range(start_p, min(end_p+1, len(doc.paragraphs))):
        t = doc.paragraphs[i].text.strip()
        if t:
            sec_paras.append((i, t))
            
    total = len(sec_paras)
    matched = 0
    missing = []
    
    for p_idx, t in sec_paras:
        nt = norm_clean(t)
        # check snippet of 25 characters
        snip = nt[:25] if len(nt) >= 25 else nt
        if len(snip) >= 5 and snip in norm_md_str:
            matched += 1
        elif len(snip) < 5 and (t.lower() in clean_md.lower() or nt in norm_md_str):
            matched += 1
        else:
            missing.append({'docx_p_idx': p_idx, 'text': t})
            all_unmatched_details.append({'section': name, 'docx_p_idx': p_idx, 'text': t})
            
    overall_total += total
    overall_matched += matched
    
    rate = f"{(matched/total*100):.2f}%" if total else "0%"
    print(f"{name:12s}: {matched:3d}/{total:3d} ({rate}) - Missing: {len(missing)}")
    
    true_audit.append({
        'section': name,
        'docx_range': f"p{start_p}-p{end_p}",
        'total_docx_paras': total,
        'matched': matched,
        'missing_count': len(missing),
        'parity_rate': f"{(matched/total*100):.2f}%" if total else "0%",
        'missing_samples': [m['text'][:100] for m in missing[:5]]
    })

print("-----------------------------------------------------------------")
print(f"OVERALL PARITY: {overall_matched}/{overall_total} ({(overall_matched/overall_total*100):.2f}%)")
print(f"TOTAL MISSING : {len(all_unmatched_details)}")
print("=================================================================")

result = {
    'overall_total_docx_paras': overall_total,
    'overall_matched': overall_matched,
    'overall_missing': overall_total - overall_matched,
    'overall_parity_rate': f"{(overall_matched/overall_total*100):.2f}%",
    'section_audit': true_audit,
    'total_unmatched': len(all_unmatched_details),
    'unmatched_details': all_unmatched_details
}

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\true_parity_audit.json', 'w', encoding='utf-8') as out:
    json.dump(result, out, ensure_ascii=False, indent=2)

print("True parity audit saved.")
