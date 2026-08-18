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

f_paras = docx_bundle.chapter_paragraphs.get("F", [])
print(f"Total paragraphs in chapter_paragraphs['F']: {len(f_paras)}")

substantive_f = [p for p in f_paras if len(p) > 30]
print(f"Substantive paragraphs in F (>30 chars): {len(substantive_f)}")

clean_md = re.sub(r'[^\w\d]+', '', md_bundle.normalized_text)

for idx, p in enumerate(substantive_f):
    sample = re.sub(r"\s+", " ", p[:40]).strip().lower()
    in_md = sample in md_bundle.normalized_text
    print(f"[{idx:02d}] match={in_md}: '{sample}'")
    if not in_md:
        print(f"   FULL TEXT: {p}")
        clean_p = re.sub(r'[^\w\d]+', '', p.lower())
        comp_found = clean_p[:40] in clean_md
        print(f"   Compact in MD: {comp_found}")
