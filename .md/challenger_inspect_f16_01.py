import sys
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tests.conftest import parse_docx_qcvn, parse_markdown_qcvn

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

docx_path = Path(r'd:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx')
md_path = Path(r'd:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md')

docx_bundle = parse_docx_qcvn(docx_path)
md_bundle = parse_markdown_qcvn(md_path)

substantive_paras = [p for p in docx_bundle.body_paragraphs if len(p) > 30]
print(f"Total substantive paragraphs: {len(substantive_paras)}")

unmatched_f16 = []
for idx, p in enumerate(substantive_paras):
    sample = re.sub(r"\s+", " ", p[:40]).strip().lower()
    if sample not in md_bundle.normalized_text:
        clean_p = re.sub(r'[^\w\d]+', '', p.lower())
        clean_md = re.sub(r'[^\w\d]+', '', md_bundle.normalized_text)
        is_compact_in_md = clean_p[:40] in clean_md
        unmatched_f16.append({
            'idx': idx,
            'sample': sample,
            'full': p,
            'is_compact_in_md': is_compact_in_md
        })

print(f"\nUnmatched substantive paragraphs in test_f16_01: {len(unmatched_f16)}")
for item in unmatched_f16:
    print(f"\n--- Item {item['idx']} (Compact in MD: {item['is_compact_in_md']}) ---")
    print(f"Sample: '{item['sample']}'")
    print(f"Full: {item['full'][:120]}")
