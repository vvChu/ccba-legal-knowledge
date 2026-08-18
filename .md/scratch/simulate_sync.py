import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
from pathlib import Path

repo_root = Path(r"d:\GitHubProjects\ccba-legal-knowledge")
bundle_dir = repo_root / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
md_path = bundle_dir / "qcvn_06_2022_bxd.md"

md_lines = md_path.read_text(encoding="utf-8").splitlines()

# Parse all anchors in order
anchor_pattern = re.compile(r'<a id="([^"]+)"></a>')

nodes = []
for idx, line in enumerate(md_lines, 1):
    m = anchor_pattern.search(line)
    if m:
        anchor_id = m.group(1)
        # Heading text
        heading_text = ""
        # Check next line or this line
        for offset in range(1, 4):
            if idx - 1 + offset < len(md_lines):
                cand = md_lines[idx - 1 + offset].strip()
                if cand.startswith("#") or cand.startswith("**") or cand:
                    heading_text = cand
                    break
        clean_title = re.sub(r"^[#\s\*]+", "", heading_text).strip()
        clean_title = re.sub(r"[\*]+$", "", clean_title).strip()
        
        nodes.append({
            "anchor": anchor_id,
            "clause_id": anchor_id,
            "title": clean_title,
            "line_start": idx,
            "line_end": idx, # to be calculated or same line
        })

# Compute line_end properly for AST (line before next node, or end of file)
for i in range(len(nodes) - 1):
    nodes[i]["line_end"] = max(nodes[i]["line_start"], nodes[i+1]["line_start"] - 1)
nodes[-1]["line_end"] = len(md_lines)

print(f"Extracted {len(nodes)} AST nodes from MD.")

# Generate corresponding QA pairs
qa_pairs = []
for node in nodes:
    anchor = node["anchor"]
    title = node["title"]
    
    # Format human-friendly question and answer
    if anchor.startswith("chuong-"):
        ch_num = anchor.split("-")[1]
        question = f"Chương {ch_num} quy định về nội dung gì?"
        answer = f"Quy định tại {title}."
    elif anchor.startswith("phu-luc-"):
        pl_id = anchor.split("-")[2].upper()
        question = f"Phụ lục {pl_id} quy định về nội dung gì?"
        answer = f"Quy định tại {title}."
    elif anchor.startswith("bang-"):
        t_id = anchor.replace("bang-", "").replace("-", ".").upper()
        question = f"Bảng {t_id} quy định về nội dung gì?"
        answer = f"Quy định tại {title}."
    elif anchor.startswith("muc-"):
        sec_id = anchor.replace("muc-", "").replace("-", ".").upper()
        question = f"Mục {sec_id} quy định về nội dung gì?"
        answer = f"Chi tiết quy định tại {title}."
    else:
        question = f"Nội dung điều khoản {anchor} quy định gì?"
        answer = f"Chi tiết quy định tại {title}."
        
    # Ensure min lengths
    if len(question) <= 10:
        question = f"Quy chuẩn quy định nội dung gì tại mục {anchor}?"
    if len(answer) <= 15:
        answer = f"Chi tiết nội dung kỹ thuật quy định tại {title}."
        
    qa_pairs.append({
        "question": question,
        "answer": answer,
        "anchor": anchor
    })

print(f"Generated {len(qa_pairs)} QA pairs.")

# Validate QA questions uniqueness
questions = [q["question"] for q in qa_pairs]
dup_q = set([x for x in questions if questions.count(x) > 1])
print(f"Duplicate questions count: {len(dup_q)}")
if dup_q:
    print(f"Sample duplicates: {list(dup_q)[:5]}")

# Validate boundary conditions
print(f"First QA pair: {qa_pairs[0]}")
print(f"Last QA pair: {qa_pairs[-1]}")
print(f"First AST node: {nodes[0]}")
print(f"Last AST node: {nodes[-1]}")
