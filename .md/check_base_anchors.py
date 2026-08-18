import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"
SD1_MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.md"

with open(BASE_MD_PATH, 'r', encoding='utf-8') as f:
    base_md = f.read()

with open(SD1_MD_PATH, 'r', encoding='utf-8') as f:
    sd1_md = f.read()

base_anchors = re.findall(r'<a\s+id="([^"]+)">\s*</a>', base_md)
print(f"Base QCVN 06 Anchors Count: {len(base_anchors)}")
print(f"Base QCVN 06 Sample Anchors: {base_anchors[:20]}")

sd1_links = re.findall(r'\[([^\]]+)\]\(qcvn_06_2022_bxd\.md#([^\)]+)\)', sd1_md)
print(f"\nSD1 Cross-links Count: {len(sd1_links)}")

matched = []
unmatched = []
for label, target in sd1_links:
    if target in base_anchors:
        matched.append((label, target))
    else:
        unmatched.append((label, target))

print(f"Direct Target Anchor Matches in Base: {len(matched)}")
print(f"Target Anchors Not Found in Base: {len(unmatched)}")
print(f"\nSample Unmatched Target Anchors:")
for u in unmatched[:15]:
    print(f"  Link: [{u[0]}](qcvn_06_2022_bxd.md#{u[1]})")

# Check if target is a heading in base (e.g. "1.1.10", "1.5.5")
heading_matches = 0
for u in unmatched:
    # search if the clause number exists in base_md
    m = re.search(r'(?:muc-|bang-|dieu-)?([a-z0-9\-]+)', u[1])
    if m:
        clause_id = m.group(1).replace('-', '.')
        if f"### {clause_id}" in base_md or f"## {clause_id}" in base_md or f"#### {clause_id}" in base_md or f"**{clause_id}**" in base_md:
            heading_matches += 1

print(f"Unmatched Anchors that exist as Text/Headings in Base: {heading_matches} / {len(unmatched)}")
