import docx
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

docx_path = r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx'
md_path = r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md'

doc = docx.Document(docx_path)
with open(md_path, 'r', encoding='utf-8') as f:
    raw_md = f.read()

def normalize_text(text: str) -> str:
    # Unicode normalize
    text = unicodedata.normalize('NFC', text)
    # Remove markdown tags, anchors, formatting
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'[#\*_`~\[\]\(\)]', ' ', text)
    # Normalize whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_compact(text: str) -> str:
    text = unicodedata.normalize('NFC', text)
    # Remove markdown formatting and punctuation for deep substring search
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\d]+', '', text.lower())
    return text

norm_md_full = normalize_text(raw_md)
compact_md = normalize_compact(raw_md)

print("Markdown total characters:", len(raw_md))
print("Markdown normalized characters:", len(norm_md_full))
print("Markdown compact characters:", len(compact_md))

# Check every docx paragraph
results = []
exact_matches = 0
prefix_only_matches = 0
suffix_only_matches = 0
full_compact_matches = 0
missing_paragraphs = []

for i, p in enumerate(doc.paragraphs):
    raw_t = p.text.strip()
    if not raw_t:
        continue
    
    norm_p = normalize_text(raw_t)
    comp_p = normalize_compact(raw_t)
    
    if len(norm_p) == 0 or len(comp_p) == 0:
        continue
        
    is_full_exact = norm_p in norm_md_full
    is_compact_match = comp_p in compact_md
    
    prefix = comp_p[:min(40, len(comp_p))]
    suffix = comp_p[-min(40, len(comp_p)):]
    mid_start = max(0, len(comp_p)//2 - 20)
    middle = comp_p[mid_start:mid_start+40]
    
    prefix_found = prefix in compact_md if len(prefix) >= 10 else (norm_p.lower() in norm_md_full.lower())
    suffix_found = suffix in compact_md if len(suffix) >= 10 else (norm_p.lower() in norm_md_full.lower())
    middle_found = middle in compact_md if len(middle) >= 10 else (norm_p.lower() in norm_md_full.lower())
    
    status = "UNKNOWN"
    if is_compact_match:
        status = "EXACT_OR_COMPACT_MATCH"
        full_compact_matches += 1
        if is_full_exact:
            exact_matches += 1
    elif prefix_found and suffix_found:
        status = "INTERIOR_VARIATION" # maybe formatting/punctuation difference inside
    elif prefix_found and not suffix_found:
        status = "POTENTIAL_TRUNCATION"
        prefix_only_matches += 1
        missing_paragraphs.append({
            'index': i,
            'status': status,
            'text': raw_t,
            'norm_len': len(norm_p),
            'prefix': prefix,
            'suffix': suffix
        })
    elif suffix_found and not prefix_found:
        status = "POTENTIAL_LEADING_LOSS"
        suffix_only_matches += 1
        missing_paragraphs.append({
            'index': i,
            'status': status,
            'text': raw_t,
            'norm_len': len(norm_p),
            'prefix': prefix,
            'suffix': suffix
        })
    else:
        status = "MISSING_OR_HEAVILY_ALTERED"
        missing_paragraphs.append({
            'index': i,
            'status': status,
            'text': raw_t,
            'norm_len': len(norm_p)
        })
        
    results.append({
        'index': i,
        'status': status,
        'len': len(norm_p),
        'text_snip': raw_t[:80]
    })

print(f"\n--- PARITY RESULTS ---")
print(f"Total non-empty paragraphs evaluated: {len(results)}")
print(f"Full compact matches: {full_compact_matches} / {len(results)} ({full_compact_matches/len(results)*100:.2f}%)")
print(f"Exact verbatim matches: {exact_matches} / {len(results)} ({exact_matches/len(results)*100:.2f}%)")
print(f"Discrepancies / Anomalies flagged: {len(missing_paragraphs)}")

if missing_paragraphs:
    print("\n--- SAMPLE FLAGGED PARAGRAPHS ---")
    for m in missing_paragraphs[:15]:
        print(f"p{m['index']:04d} [{m['status']}]: {m['text'][:100]}")

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\challenger_deep_parity_results.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total_evaluated': len(results),
        'full_compact_matches': full_compact_matches,
        'exact_matches': exact_matches,
        'flagged_count': len(missing_paragraphs),
        'flagged_items': missing_paragraphs
    }, f, ensure_ascii=False, indent=2)

print("Saved report to .md/challenger_deep_parity_results.json")
