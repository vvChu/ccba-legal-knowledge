import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("legal_docs/02_qcvn/qcvn_06_2022_bxd/sources/qcvn_06_2022_bxd_goc_2022.md", "r", encoding="utf-8") as f:
    goc_text = f.read()

with open("legal_docs/02_qcvn/qcvn_06_2022_bxd/qcvn_06_2022_bxd.md", "r", encoding="utf-8") as f:
    md_text = f.read()

pattern = re.compile(r"^#+\s+([0-9A-Z\.]+)\s+(.*)", re.M)
goc_matches = pattern.findall(goc_text)
md_matches = pattern.findall(md_text)

print(f"Goc headings: {len(goc_matches)}, MD headings: {len(md_matches)}")

goc_nums = {m[0].strip("."): m[1].strip() for m in goc_matches}
md_nums = {m[0].strip("."): m[1].strip() for m in md_matches}

mutations = []
for num, title in md_nums.items():
    if num not in goc_nums:
        # Check if collapsing a dot matches goc
        # e.g., 1.1.1.0 -> 1.1.10, 3.1.1.0 -> 3.1.10, 4.2.7 -> 4.27, A.2.2.8 -> A.2.28
        collapsed = re.sub(r"\.([0-9])\.([0-9])$", r".\1\2", num)
        if collapsed in goc_nums:
            mutations.append((num, collapsed, title))

print(f"Found {len(mutations)} heading mutations:")
for old, new, t in mutations:
    print(f"  {old} -> {new}: {t[:50]}")
