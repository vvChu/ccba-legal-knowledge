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
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'[#\*_`~\[\]\(\)]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_compact(text: str) -> str:
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\d]+', '', text.lower())
    return text

norm_md = normalize_text(raw_md)
compact_md = normalize_compact(raw_md)

# 1. Inspect first 25 paragraphs
print("=== FIRST 25 PARAGRAPHS IN DOCX ===")
for i in range(min(25, len(doc.paragraphs))):
    t = doc.paragraphs[i].text.strip()
    if t:
        cp = normalize_compact(t)
        found = cp in compact_md
        print(f"p{i:04d} (len={len(t):3d}) [Found in MD: {str(found):5s}]: {t[:70]}")

# 2. Detailed inspection of non-exact matches
print("\n=== DETAILED NON-EXACT / FLAGGED PARAGRAPHS ===")
non_exact_details = []
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    nt = normalize_text(t)
    ct = normalize_compact(t)
    if not ct:
        continue
    
    is_exact = nt in norm_md
    is_compact = ct in compact_md
    
    if not is_exact:
        non_exact_details.append({
            'index': i,
            'text': t,
            'is_compact': is_compact,
            'nt': nt,
            'ct': ct
        })

print(f"Total non-exact paragraphs: {len(non_exact_details)}")
for item in non_exact_details:
    print(f"\np{item['index']:04d} [Compact match: {item['is_compact']}]:")
    print(f"  DOCX: {item['text'][:120]}")
    # find where in normalized md it might be
    if item['is_compact']:
        # locate snippet
        snip = item['ct'][:30]
        pos = compact_md.find(snip)
        print(f"  MD snippet at char pos {pos}: found compact")

# 3. Sentence-level verification
print("\n=== SENTENCE-LEVEL LOSS AUDIT ===")
total_sentences = 0
found_sentences = 0
missing_sentences = []

for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    # split into sentences
    sentences = re.split(r'(?<=[.!?;\n])\s+', t)
    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) < 15: # skip tiny fragments
            continue
        total_sentences += 1
        s_comp = normalize_compact(s_clean)
        if s_comp in compact_md:
            found_sentences += 1
        else:
            missing_sentences.append({
                'p_index': i,
                'sentence': s_clean,
                'compact': s_comp
            })

print(f"Total substantive sentences: {total_sentences}")
print(f"Found in Markdown: {found_sentences} / {total_sentences} ({found_sentences/total_sentences*100:.2f}%)")
print(f"Missing sentences: {len(missing_sentences)}")

if missing_sentences:
    print("\nSample missing sentences:")
    for ms in missing_sentences[:10]:
        print(f"  p{ms['p_index']:04d}: {ms['sentence'][:100]}")

# 4. CHÚ THÍCH (Footnotes / Notes) audit
print("\n=== CHÚ THÍCH / NOTE AUDIT ===")
doc_notes = []
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if re.match(r'^(chú thích|ghi chú)\b', t, re.IGNORECASE):
        doc_notes.append((i, t))

print(f"Total notes in DOCX body: {len(doc_notes)}")
notes_found = 0
missing_notes = []
for i, nt_text in doc_notes:
    cnt = normalize_compact(nt_text)
    if cnt in compact_md:
        notes_found += 1
    else:
        missing_notes.append((i, nt_text))

print(f"Notes preserved in MD: {notes_found} / {len(doc_notes)} ({notes_found/len(doc_notes)*100 if doc_notes else 100:.2f}%)")
if missing_notes:
    print("Missing notes:")
    for i, nt_text in missing_notes:
        print(f"  p{i:04d}: {nt_text[:100]}")

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\challenger_deep_inspection.json', 'w', encoding='utf-8') as out:
    json.dump({
        'non_exact_details': non_exact_details,
        'total_sentences': total_sentences,
        'found_sentences': found_sentences,
        'missing_sentences': missing_sentences,
        'total_notes': len(doc_notes),
        'notes_found': notes_found,
        'missing_notes': missing_notes
    }, out, ensure_ascii=False, indent=2)

print("\nAudit saved to .md/challenger_deep_inspection.json")
