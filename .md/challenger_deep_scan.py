"""
Comprehensive Deep Adversarial Scanner for Base QCVN 06:2022/BXD
Author: challenger_m1_1
"""
import sys
import re
import json
import docx
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MD_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md")
DOCX_PATH = Path(r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx")

md_raw = MD_PATH.read_text(encoding="utf-8")
md_lines = md_raw.splitlines()
doc = docx.Document(str(DOCX_PATH))

print("=" * 80)
print("COMPREHENSIVE ADVERSARIAL DEEP SCAN")
print("=" * 80)

# 1. Audit all headings with space separated digits (e.g. `2 2.2.1`, `3 1`, `### 4 1`)
space_digits_headings = []
for idx, line in enumerate(md_lines):
    # Match any line starting with numbers separated by spaces e.g. "2 2.2.1", "1 4", etc.
    if re.match(r'^(#+\s+)?\d+\s+\d+(\.\d+)*\b', line):
        # Exclude table rows and lists
        if not line.startswith('|') and not line.startswith('-') and not line.startswith('*'):
            space_digits_headings.append((idx + 1, line))

print(f"\n[1] Potential space-separated heading bugs: {len(space_digits_headings)}")
for line_no, text in space_digits_headings[:20]:
    print(f"  Line {line_no:4d}: {text[:100]}")

# 2. Audit all heading numbers for consistency and missing dots
# Check all #+ lines
heading_numbers = []
heading_anomalies = []
for idx, line in enumerate(md_lines):
    m = re.match(r'^(#+)\s+([A-Za-z0-9\._\-]+)(?:\s+(.*))?$', line)
    if m:
        hashes = m.group(1)
        num = m.group(2)
        title = m.group(3) or ""
        level = len(hashes)
        
        # Check for unformatted space-split numbers
        if re.match(r'^\d+\s+\d+', num):
            heading_anomalies.append({
                "line": idx + 1,
                "type": "space_number",
                "text": line
            })
            
        # Check for missing subdots e.g. 2.1.11, 2.2.13, 5.1.11..14, 6.2.11..14
        if re.match(r'^\d+\.\d+\.\d{2,}$', num):
            heading_anomalies.append({
                "line": idx + 1,
                "type": "missing_subdot",
                "num": num,
                "text": line
            })
            
        # Check for dot-split bugs e.g. 1.4.1.7, 1.4.2.5
        if re.match(r'^1\.4\.\d+\.\d+$', num):
            heading_anomalies.append({
                "line": idx + 1,
                "type": "dot_split",
                "num": num,
                "text": line
            })

print(f"\n[2] Heading Anomalies detected: {len(heading_anomalies)}")
for a in heading_anomalies:
    print(f"  Line {a['line']:4d} [{a['type']}]: {a['text'][:100]}")

# 3. Check for unpromoted headings in plaintext
# E.g. lines starting with "X.Y.Z.W" or "PHỤ LỤC" without #
unpromoted_headings = []
for idx, line in enumerate(md_lines):
    stripped = line.strip()
    if not stripped or stripped.startswith('#') or stripped.startswith('|') or stripped.startswith('<') or stripped.startswith('-') or stripped.startswith('*') or stripped.startswith('_'):
        continue
    # Check if line looks like a clause header: e.g. "2 2.2.1", "2.2.1.1", "A.1.1"
    if re.match(r'^(?:[1-7]|[A-I])\.\d+(?:\.\d+)*\s+[A-ZĐÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐĨŨƠƯ]', stripped):
        unpromoted_headings.append((idx + 1, stripped))
    elif re.match(r'^\d+\s+\d+\.\d+', stripped):
        unpromoted_headings.append((idx + 1, stripped))

print(f"\n[3] Unpromoted heading lines (plain text instead of markdown heading): {len(unpromoted_headings)}")
for line_no, text in unpromoted_headings[:20]:
    print(f"  Line {line_no:4d}: {text[:100]}")

# 4. Check all 64 table anchors and headers
tables_found = re.findall(r'^(?:<a id="bang-([^"]+)"></a>\s*\n)?###\s+Bảng\s+([A-Za-z0-9\._]+)\s*[-–—:]\s*(.*)', md_raw, re.MULTILINE)
print(f"\n[4] Total table headers found: {len(tables_found)}")

# 5. Check all Appendix headers
print("\n[5] Appendix Headers Audit:")
for app in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
    m = re.findall(rf'^##\s+PHỤ\s+LỤC\s+{app}\b.*', md_raw, re.MULTILINE | re.IGNORECASE)
    print(f"  Phụ lục {app}: {len(m)} match(es) -> {m}")

# 6. Check footnotes / CHÚ THÍCH across the entire markdown
chuthich_lines = [line for line in md_lines if "CHÚ THÍCH" in line or "Chú thích" in line]
print(f"\n[6] Lines containing 'CHÚ THÍCH': {len(chuthich_lines)}")

# Save report
report_data = {
    "space_digits_headings": space_digits_headings,
    "heading_anomalies": heading_anomalies,
    "unpromoted_headings": unpromoted_headings,
    "tables_count": len(tables_found),
    "chuthich_count": len(chuthich_lines)
}
with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\challenger_deep_scan.json', 'w', encoding='utf-8') as f:
    json.dump(report_data, f, ensure_ascii=False, indent=2)

print("\nDeep scan finished.")
