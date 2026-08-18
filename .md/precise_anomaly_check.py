import docx
import re
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

md_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\test_reconstructed_qcvn06.md'
with open(md_path, 'r', encoding='utf-8') as f:
    md_lines = [line.rstrip('\r\n') for line in f.readlines()]

print("=================================================================")
print("           PRECISE ANOMALY VERIFICATION AUDIT                    ")
print("=================================================================")

# 1. Check Section 1.4 dot-split anomalies (e.g. 1.4.1.7 through 1.4.7.2)
sec_14_dotsplit = []
re_14_dotsplit = re.compile(r'#*\s*(1\.4\.[0-9]\.[0-9]+)\b')
for idx, l in enumerate(md_lines):
    m = re_14_dotsplit.search(l)
    if m:
        sec_14_dotsplit.append((idx + 1, m.group(1), l))

print(f"1. Section 1.4 Dot-Split Anomalies (1.4.1.7 -> 1.4.17, etc.): {len(sec_14_dotsplit)} found")
for item in sec_14_dotsplit:
    print(f"   Line {item[0]}: {item[1]} -> {item[2]}")

# 2. Check Space-instead-of-dot anomalies (e.g. "### 4 1", "### 7 1")
space_dot_anomalies = []
re_spacedot = re.compile(r'#+\s+([1-7]|[A-I])\s+([0-9]+)\b')
for idx, l in enumerate(md_lines):
    m = re_spacedot.search(l)
    if m:
        after = l[m.end():].strip()
        if not after.isupper() or len(after) < 5:
            space_dot_anomalies.append((idx + 1, f"{m.group(1)} {m.group(2)}", l))

print(f"2. Space-Instead-Of-Dot Anomalies (### 4 1, ### 7 1, etc.): {len(space_dot_anomalies)} found")
for item in space_dot_anomalies:
    print(f"   Line {item[0]}: {item[1]} -> {item[2]}")

# 3. Check Table Residual Headings (e.g. "### 24 0", "### 1 4")
table_residual_anomalies = []
re_residual_h = re.compile(r'#+\s+([0-9]+(\s+[0-9]+)*)$')
for idx, l in enumerate(md_lines):
    m = re_residual_h.match(l.strip())
    if m:
        table_residual_anomalies.append((idx + 1, l.strip()))

print(f"3. Table Residual Headings (### 24 0, ### 1 4, etc.): {len(table_residual_anomalies)} found")
for item in table_residual_anomalies:
    print(f"   Line {item[0]}: {item[1]}")

# 4. Check Missing-Subdot Anomalies (e.g. "2.1.11" instead of "2.1.1.1")
missing_subdot_anomalies = []
re_missing_subdot = re.compile(r'#+\s+(2\.1\.11|2\.1\.12|2\.2\.11|2\.2\.12|5\.1\.11|6\.2\.11)\b')
for idx, l in enumerate(md_lines):
    m = re_missing_subdot.search(l)
    if m:
        missing_subdot_anomalies.append((idx + 1, m.group(1), l))

print(f"4. Missing-Subdot Anomalies (2.1.11 -> 2.1.1.1, etc.): {len(missing_subdot_anomalies)} found")
for item in missing_subdot_anomalies:
    print(f"   Line {item[0]}: {item[1]} -> {item[2]}")

# 5. Check Heading Levels Hierarchy
h_counts = {}
for l in md_lines:
    if l.strip().startswith("#"):
        m = re.match(r'^(#+)', l.strip())
        if m:
            lvl = len(m.group(1))
            h_counts[lvl] = h_counts.get(lvl, 0) + 1

print(f"5. Heading Hierarchy Distribution: {dict(sorted(h_counts.items()))}")
print("=================================================================")
