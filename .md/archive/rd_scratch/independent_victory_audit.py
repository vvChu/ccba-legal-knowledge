import os, re, json, glob
from pathlib import Path

target_dir = Path("legal_docs/03_tcvn/tcvn_2737_2023")
md_files = [target_dir / "tcvn_2737_2023.md"] + sorted((target_dir / "annexes").glob("*.md"))

print(f"=== CHECK 1: MARKDOWN FILES & HEADINGS ===")
print(f"Found {len(md_files)} markdown files in {target_dir}")

display_formula_pattern = re.compile(r"\$\$(.*?)\$\$", re.DOTALL)
formula_tag_pattern = re.compile(r"\\tag\{([^}]+)\}")
formula_id_pattern = re.compile(r'<!--\s*formula_id:\s*"([^"]+)"\s*-->')

display_formulas = []
decimal_comma_violations = []

for mf in md_files:
    text = mf.read_text(encoding="utf-8")
    matches = list(display_formula_pattern.finditer(text))
    for m in matches:
        f_body = m.group(1).strip()
        tag_match = formula_tag_pattern.search(f_body)
        tag = tag_match.group(1) if tag_match else None
        
        post_text = text[m.end():m.end()+150]
        id_match = formula_id_pattern.search(post_text)
        fid = id_match.group(1) if id_match else None
        
        display_formulas.append((mf.name, tag, fid, f_body))
        
        # Check decimal comma in numbers like 0,5 without {}
        comma_matches = re.findall(r"\d,\d", f_body)
        if comma_matches:
            decimal_comma_violations.append((mf.name, tag, comma_matches, f_body))

print(f"\n=== CHECK 2: FORMULAS & KATEX INTEGRITY ===")
print(f"Total display formulas found: {len(display_formulas)}")
print(f"Decimal comma violations (d,d without {{}}): {len(decimal_comma_violations)}")
if decimal_comma_violations:
    for v in decimal_comma_violations:
        print(f"  VIOLATION: {v[0]} tag={v[1]}: {v[2]}")

tags_by_file = {}
for mf_name, tag, fid, _ in display_formulas:
    tags_by_file.setdefault(mf_name, []).append((tag, fid))

for fname, flist in tags_by_file.items():
    print(f"\n--- {fname} ({len(flist)} formulas) ---")
    for tag, fid in flist:
        print(f"  Tag: {tag} | ID: {fid}")

# CHECK 3: TABLES
print(f"\n=== CHECK 3: TABLES AUDIT ===")
json_tables = list((target_dir / "tables" / "json").glob("*.json"))
csv_tables = list((target_dir / "tables" / "csv").glob("*.csv"))
print(f"JSON tables count: {len(json_tables)}")
print(f"CSV tables count: {len(csv_tables)}")

broken_tables = []
for jf in json_tables:
    try:
        data = json.loads(jf.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            broken_tables.append((jf.name, "Not a JSON dict"))
        for k in ["table_id", "title", "columns", "rows"]:
            if k not in data:
                broken_tables.append((jf.name, f"Missing key '{k}'"))
    except Exception as e:
        broken_tables.append((jf.name, str(e)))

print(f"JSON tables validation errors: {len(broken_tables)}")
if broken_tables:
    for b in broken_tables:
        print(f"  Table error: {b[0]} -> {b[1]}")

# CHECK 4: FIGURES & VISUAL ASSETS
print(f"\n=== CHECK 4: FIGURES & VISUAL ASSETS AUDIT ===")
cards = list((target_dir / "figures" / "cards").glob("*.json"))
images = list((target_dir / "figures" / "images").glob("hinh_*.png"))
print(f"Visual Cards count: {len(cards)}")
print(f"Standardized Figures (hinh_*.png) count: {len(images)}")

# Check image references in markdown
img_ref_pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
broken_img_refs = []
legacy_img_refs = []

for mf in md_files:
    text = mf.read_text(encoding="utf-8")
    for match in img_ref_pattern.finditer(text):
        alt = match.group(1)
        src = match.group(2)
        if "image" in src.lower() and not src.startswith("../figures/images/hinh_"):
            legacy_img_refs.append((mf.name, src))
        
        # Check if target exists
        resolved = (mf.parent / src).resolve()
        if not resolved.exists():
            broken_img_refs.append((mf.name, src, str(resolved)))

print(f"Legacy image references: {len(legacy_img_refs)}")
print(f"Broken image references: {len(broken_img_refs)}")
if broken_img_refs:
    for b in broken_img_refs:
        print(f"  Broken image: {b[0]} -> {b[1]}")

# CHECK 5: LIST ITEM ESCAPING (ADR 0029)
print(f"\n=== CHECK 5: LIST ITEM ESCAPING (ADR 0029) ===")
unescaped_lists = []
unescaped_bullet_pattern = re.compile(r"^(?:\s*)[-+]\s+[^-\s]", re.MULTILINE)

for mf in md_files:
    text = mf.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_yaml = False
    in_table = False
    in_code = False
    
    for idx, line in enumerate(lines, 1):
        if line.strip() == "---":
            in_yaml = not in_yaml
            continue
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_yaml or in_code:
            continue
        if line.strip().startswith("|") or line.strip().startswith("$$") or line.strip().startswith("<") or line.strip().startswith(">"):
            continue
        
        # Check raw unescaped list bullet like "- Text" or "+ Text"
        s = line.lstrip()
        if (s.startswith("- ") or s.startswith("+ ")) and not (s.startswith(r"\- ") or s.startswith(r"\+ ")):
            # Check if it's a markdown list
            unescaped_lists.append((mf.name, idx, line))

print(f"Unescaped legal bullets found: {len(unescaped_lists)}")
if unescaped_lists:
    for u in unescaped_lists[:10]:
        print(f"  Line {u[1]} in {u[0]}: {u[2]}")

