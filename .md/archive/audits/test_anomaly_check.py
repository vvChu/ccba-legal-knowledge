import docx
import re
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\test_reconstructed_qcvn06.md'

doc = docx.Document(docx_path)
with open(md_path, 'r', encoding='utf-8') as f:
    md_lines = [line.rstrip('\r\n') for line in f.readlines()]

docx_paras = []
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t:
        docx_paras.append({
            'idx': i,
            'text': t,
            'style': p.style.name if p.style else ''
        })

anomalies = []

# 1. Check dot-split anomalies like 1.4.1.7 instead of 1.4.17
re_dotsplit = re.compile(r'(###|####|#####|__|\*\*)\s*([0-9]+\.[0-9]+)\.([0-9])\.([0-9]+)')
for idx, l in enumerate(md_lines):
    m = re_dotsplit.search(l)
    if m:
        orig = f"{m.group(2)}.{m.group(3)}.{m.group(4)}"
        fixed = f"{m.group(2)}.{m.group(3)}{m.group(4)}"
        anomalies.append({
            'type': 'dot_split_anomaly',
            'line': idx + 1,
            'found': orig,
            'expected': fixed,
            'raw': l[:120]
        })

# 2. Check space-instead-of-dot anomalies like "### 4 1", "### 7 1"
re_spacedot = re.compile(r'###\s+([1-7]|[A-I])\s+([0-9]+)\b')
for idx, l in enumerate(md_lines):
    m = re_spacedot.search(l)
    if m:
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
re_residual_h = re.compile(r'###\s+([0-9]+(\s+[0-9]+)*)$')
for idx, l in enumerate(md_lines):
    m = re_residual_h.match(l.strip())
    if m:
        anomalies.append({
            'type': 'table_residual_heading',
            'line': idx + 1,
            'found': l.strip(),
            'raw': l[:120]
        })

# 4. Check heading levels distribution
h_level_counts = {}
for idx, l in enumerate(md_lines):
    if l.strip().startswith('#'):
        m = re.match(r'^(#+)', l.strip())
        if m:
            lvl = len(m.group(1))
            h_level_counts[lvl] = h_level_counts.get(lvl, 0) + 1

# 5. Check missing dots in 4-digit numbers like "2.1.11" which should be "2.1.1.1"
re_4digit = re.compile(r'(###|####|#####|__|\*\*)\s*([0-9]+\.[0-9]+\.[0-9]{2,})\b')
for idx, l in enumerate(md_lines):
    m = re_4digit.search(l)
    if m:
        num = m.group(2)
        parts = num.split('.')
        if len(parts) == 3 and len(parts[2]) == 2:
            candidate = f"{parts[0]}.{parts[1]}.{parts[2][0]}.{parts[2][1]}"
            if any(candidate in p['text'] for p in docx_paras):
                anomalies.append({
                    'type': 'missing_subdot_anomaly',
                    'line': idx + 1,
                    'found': num,
                    'expected': candidate,
                    'raw': l[:120]
                })

print(f"Total lines: {len(md_lines)}")
print(f"Heading level counts: {h_level_counts}")
print(f"Total anomalies: {len(anomalies)}")
if anomalies:
    for a in anomalies[:20]:
        print(f"  [{a['type']}] line {a['line']}: {a['raw']}")
