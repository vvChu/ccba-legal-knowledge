import docx
import re
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)
with open(md_path, 'r', encoding='utf-8') as f:
    md_lines = [line.rstrip('\r\n') for line in f.readlines()]

# Let's inspect all headings and clauses in DOCX
docx_paras = []
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t:
        docx_paras.append({
            'idx': i,
            'text': t,
            'style': p.style.name if p.style else ''
        })

# Check all MD lines for headings, bold items, and numbering anomalies
anomalies = []

# 1. Check dot-split anomalies like 1.4.1.7 instead of 1.4.17
re_dotsplit = re.compile(r'(#+|__|\*\*)\s*([0-9]+\.[0-9]+)\.([0-9])\.([0-9]+)\b')
for idx, l in enumerate(md_lines):
    m = re_dotsplit.search(l)
    if m:
        full_dotted = f"{m.group(2)}.{m.group(3)}.{m.group(4)}"
        candidate_split = f"{m.group(2)}.{m.group(3)}{m.group(4)}"
        # Exclude known fixed typos like 2.2.13 -> 2.2.1.3
        if candidate_split in ("2.2.13", "2.5.6.33"):
            continue
        # Check against docx paragraphs: if full_dotted is NOT in docx, but candidate_split IS in docx
        in_docx_dotted = any(full_dotted in p['text'] for p in docx_paras)
        in_docx_candidate = any(candidate_split in p['text'] for p in docx_paras)
        if not in_docx_dotted and in_docx_candidate:
            anomalies.append({
                'type': 'dot_split_anomaly',
                'line': idx + 1,
                'found': full_dotted,
                'expected': candidate_split,
                'raw': l[:120]
            })

# 2. Check space-instead-of-dot anomalies like "### 4 1", "### 7 1"
re_spacedot = re.compile(r'#{1,6}\s+([1-7]|[A-I])\s+([0-9]+)\b')
for idx, l in enumerate(md_lines):
    m = re_spacedot.search(l)
    if m:
        # Avoid matching Chapter titles like "### 1 QUY ĐỊNH CHUNG"
        # Only if second part is digits and not followed by all caps chapter title
        after = l[m.end():].strip()
        if not after.isupper() or len(after) < 5:
            anomalies.append({
                'type': 'space_instead_of_dot',
                'line': idx + 1,
                'found': f"{m.group(1)} {m.group(2)}",
                'expected': f"{m.group(1)}.{m.group(2)}",
                'raw': l[:120]
            })

# 3. Check table residual numbers as headings like "### 24 0", "### 1 4"
re_residual_h = re.compile(r'#{1,6}\s+([0-9]+(\s+[0-9]+)*)$')
for idx, l in enumerate(md_lines):
    m = re_residual_h.match(l.strip())
    if m:
        anomalies.append({
            'type': 'table_residual_heading',
            'line': idx + 1,
            'found': l.strip(),
            'raw': l[:120]
        })

# 4. Check heading levels: all headings are ### (H3)
h_level_counts = {}
for idx, l in enumerate(md_lines):
    if l.strip().startswith('#'):
        m = re.match(r'^(#+)', l.strip())
        if m:
            lvl = len(m.group(1))
            h_level_counts[lvl] = h_level_counts.get(lvl, 0) + 1

# 5. Check missing dots in 4-digit numbers like "2.1.11" which should be "2.1.1.1"
# Let's cross-check with DOCX
re_4digit = re.compile(r'(#{1,6}|__|\*\*)\s*([0-9]+\.[0-9]+\.[0-9]{2,})\b')
for idx, l in enumerate(md_lines):
    m = re_4digit.search(l)
    if m:
        num = m.group(2)
        # check if this num in DOCX exists as dotted e.g. 2.1.1.1
        # if num is 2.1.11, candidate is 2.1.1.1
        parts = num.split('.')
        if len(parts) == 3 and len(parts[2]) == 2:
            candidate = f"{parts[0]}.{parts[1]}.{parts[2][0]}.{parts[2][1]}"
            # check if candidate in docx
            if any(candidate in p['text'] for p in docx_paras):
                anomalies.append({
                    'type': 'missing_subdot_anomaly',
                    'line': idx + 1,
                    'found': num,
                    'expected': candidate,
                    'raw': l[:120]
                })

# 6. Check escape characters
re_escapes = re.compile(r'\\[\._\-*#\[\]\(\)]')
escape_list = []
for idx, l in enumerate(md_lines):
    escs = re_escapes.findall(l)
    if escs:
        escape_list.append({
            'line': idx + 1,
            'escapes': list(set(escs)),
            'raw': l[:120]
        })

# Summary report
out_summary = {
    'total_lines_md': len(md_lines),
    'heading_level_counts': h_level_counts,
    'total_anomalies': len(anomalies),
    'anomalies_by_type': {},
    'anomalies': anomalies,
    'total_escape_lines': len(escape_list),
    'escape_sample': escape_list[:40]
}

for a in anomalies:
    t = a['type']
    out_summary['anomalies_by_type'][t] = out_summary['anomalies_by_type'].get(t, 0) + 1

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\comprehensive_anomaly_report.json', 'w', encoding='utf-8') as out:
    json.dump(out_summary, out, ensure_ascii=False, indent=2)

print("=================================================================")
print(f"ANOMALY DETECTION RESULT: {len(anomalies)} anomalies found")
print(f"Heading Levels: {h_level_counts}")
print(f"Anomalies by type: {out_summary['anomalies_by_type']}")
print("=================================================================")
print("Comprehensive anomaly report saved.")
