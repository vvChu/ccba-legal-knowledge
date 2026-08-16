import os
import sys
import json
import yaml
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent

def test_gate_requirements():
    print("=== GATE EVALUATION (MILESTONES 3 & 4) VERIFICATION ===")
    
    registry_path = ROOT_DIR / "legal_registry.yaml"
    assert registry_path.exists(), f"legal_registry.yaml missing at {registry_path}"
    
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f)
        
    print("[PASS] legal_registry.yaml parsed successfully via yaml.safe_load()")

    
    laws = registry.get("laws", [])
    law_ids = {doc["id"] for doc in laws if "id" in doc}
    print(f"[PASS] Found {len(laws)} entries under 'laws:' in legal_registry.yaml")
    
    decree_slugs = [
        "nghi_dinh_217_2026_nd_cp",
        "nghi_dinh_207_2026_nd_cp",
        "nghi_dinh_212_2026_nd_cp",
        "nghi_dinh_206_2026_nd_cp",
        "nghi_dinh_210_2026_nd_cp",
        "nghi_dinh_209_2026_nd_cp",
        "nghi_dinh_193_2026_nd_cp",
    ]
    
    # 1. Verify bundle_path & relations.guided_by
    for doc in laws:
        doc_id = doc.get("id")
        bundle_path_str = doc.get("bundle_path")
        assert bundle_path_str, f"Document {doc_id} missing bundle_path"
        
        bundle_dir = ROOT_DIR / bundle_path_str
        assert bundle_dir.exists(), f"bundle_path '{bundle_path_str}' for doc {doc_id} does not exist on disk"
        assert bundle_dir.is_dir(), f"bundle_path '{bundle_path_str}' for doc {doc_id} is not a directory"
        
        relations = doc.get("relations", {})
        if "guided_by" in relations:
            guided_by_id = relations["guided_by"]
            assert guided_by_id in law_ids, f"Doc {doc_id} relations.guided_by target '{guided_by_id}' not found in laws"
            print(f"[PASS] Doc {doc_id} relations.guided_by -> '{guided_by_id}' verified valid")

    print("[PASS] All bundle_path entries exist on disk and all guided_by references are valid")

    # 2. Check 7 decree bundles
    decree_count = 0
    for doc in laws:
        doc_id = doc.get("id")
        if doc_id not in decree_slugs:
            continue
            
        decree_count += 1
        bundle_dir = ROOT_DIR / doc.get("bundle_path")
        print(f"\n--- Stress Testing Decree Bundle: {doc_id} ---")
        
        # Check main .md
        md_files = list(bundle_dir.glob("*.md"))
        main_md = [f for f in md_files if f.name != "index.md"]
        assert len(main_md) > 0, f"No main markdown file found in bundle {bundle_dir}"
        main_md_path = main_md[0]
        assert main_md_path.stat().st_size > 5000, f"Main markdown file {main_md_path.name} size <= 5KB ({main_md_path.stat().st_size} bytes)"
        print(f"  [PASS] Main markdown file: {main_md_path.name} ({main_md_path.stat().st_size} bytes)")
        
        # Check index.md
        index_md_path = bundle_dir / "index.md"
        assert index_md_path.exists(), f"index.md missing in bundle {bundle_dir}"
        
        # Check clauses.json
        clauses_json_path = bundle_dir / "clauses.json"
        assert clauses_json_path.exists(), f"clauses.json missing in bundle {bundle_dir}"
        with open(clauses_json_path, "r", encoding="utf-8") as f:
            clauses_data = json.load(f)
        assert isinstance(clauses_data, list), f"clauses.json in {doc_id} is not a JSON list"
        assert len(clauses_data) >= 10, f"clauses.json in {doc_id} has {len(clauses_data)} clauses (< 10)"
        print(f"  [PASS] clauses.json valid JSON with {len(clauses_data)} clauses (>= 10 requirement met)")
        
        # Check qa_benchmark.json
        qa_json_path = bundle_dir / "qa_benchmark.json"
        assert qa_json_path.exists(), f"qa_benchmark.json missing in bundle {bundle_dir}"
        with open(qa_json_path, "r", encoding="utf-8") as f:
            qa_data = json.load(f)
        assert isinstance(qa_data, list), f"qa_benchmark.json in {doc_id} is not a JSON list"
        assert len(qa_data) >= 5, f"qa_benchmark.json in {doc_id} has {len(qa_data)} Q&A pairs (< 5)"
        print(f"  [PASS] qa_benchmark.json valid JSON with {len(qa_data)} Q&A pairs (>= 5 requirement met)")
        
        # Check anchor integrity between JSON and main MD file
        with open(main_md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
            
        for clause in clauses_data:
            c_id = clause.get("clause_id") or clause.get("id")
            if c_id:
                anchor = f'id="{c_id}"'
                assert anchor in md_content, f"Clause anchor {anchor} not found in {main_md_path.name}"
                
        print(f"  [PASS] All {len(clauses_data)} clause HTML anchors present in main markdown file")

    assert decree_count == 7, f"Expected 7 decree bundles, found {decree_count}"
    print(f"\n[PASS] Verified all 7 decree bundles successfully!")
    print("\n=== ALL GATE VERIFICATION TESTS PASSED ===")


if __name__ == "__main__":
    test_gate_requirements()
