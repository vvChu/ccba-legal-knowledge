"""
Comprehensive Adversarial Mutation Testing Matrix for CCBA Milestone 5.
Author: Challenger 2 (Empirical Challenger)
Validates test suite sensitivity and oracle resistance across all 4 Tiers.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_MD = REPO_ROOT / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "qcvn_06_2022_bxd.md"
SD1_MD = REPO_ROOT / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "sua_doi_1_2023_qcvn_06_2022_bxd.md"
CLAUSES_JSON = REPO_ROOT / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "clauses.json"
QA_JSON = REPO_ROOT / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "qa_benchmark.json"
TABLES_JSON_DIR = REPO_ROOT / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "tables" / "json"
TABLES_CSV_DIR = REPO_ROOT / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "tables" / "csv"
REGISTRY_YAML = REPO_ROOT / "legal_registry.yaml"
METADATA_YAML = REPO_ROOT / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "metadata.yaml"


class MutationTester:
    def __init__(self):
        self.results = []
        self.backups = {}
        self.extra_created_files = []

    def backup(self, path: Path):
        if path not in self.backups and path.exists():
            self.backups[path] = path.read_bytes()

    def restore_all(self):
        for path, data in self.backups.items():
            path.write_bytes(data)
        for extra_file in self.extra_created_files:
            if extra_file.exists():
                extra_file.unlink()
        self.extra_created_files = []

    def run_pytest_test(self, test_node_id: str) -> tuple[int, str]:
        cmd = [sys.executable, "-m", "pytest", test_node_id, "-q"]
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        stdout = res.stdout or ""
        stderr = res.stderr or ""
        return res.returncode, stdout + stderr

    def run_integrity_script(self) -> tuple[int, str]:
        cmd = [sys.executable, "scripts/verify_knowledge_integrity.py"]
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        stdout = res.stdout or ""
        stderr = res.stderr or ""
        return res.returncode, stdout + stderr

    def run_spoke_validator(self) -> tuple[int, str]:
        cmd = [sys.executable, "scripts/validate_legal_spoke.py"]
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        stdout = res.stdout or ""
        stderr = res.stderr or ""
        return res.returncode, stdout + stderr

    def test_mutation(
        self,
        mutation_id: str,
        category: str,
        description: str,
        apply_fn,
        target_verify_fn,
        target_name: str,
    ):
        print(f"[*] Testing {mutation_id}: {description}...")
        try:
            apply_fn()
            ret_code, output = target_verify_fn()
            killed = (ret_code != 0)
            status = "KILLED (PASS)" if killed else "SURVIVED (BUG/FAIL)"
            self.results.append({
                "mutation_id": mutation_id,
                "category": category,
                "description": description,
                "target": target_name,
                "killed": killed,
                "status": status,
                "output_snippet": output.strip().splitlines()[-3:] if output else [],
            })
            print(f"    -> Status: {status} (ret_code={ret_code})")
        finally:
            self.restore_all()


def main():
    tester = MutationTester()
    tester.backup(BASE_MD)
    tester.backup(SD1_MD)
    tester.backup(CLAUSES_JSON)
    tester.backup(QA_JSON)
    tester.backup(REGISTRY_YAML)
    tester.backup(METADATA_YAML)

    table_1 = TABLES_JSON_DIR / "bang_01_gioi_han_chiu_lua_loai.json"
    table_e4a = TABLES_JSON_DIR / "bang_e_4a_ty_le_tong_dien_tich.json"
    tester.backup(table_1)
    tester.backup(table_e4a)

    # 1. MUT_01: Delete body paragraph -> test_f16_01 Zero Data Loss Invariant
    def mut_01_apply():
        lines = BASE_MD.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if "Quy chuẩn này áp dụng đối với" in line:
                del lines[i]
                break
        BASE_MD.write_text("\n".join(lines), encoding="utf-8")

    tester.test_mutation(
        "MUT_01",
        "Text & Content Parity",
        "Delete body paragraph from Chapter 1 in base MD",
        mut_01_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f16_01_zero_data_loss_invariant"),
        "test_f16_01_zero_data_loss_invariant",
    )

    # 2. MUT_02: Dot-split anomaly in heading (1.4.1.7)
    def mut_02_apply():
        content = BASE_MD.read_text(encoding="utf-8")
        content = content.replace("#### 1.4.17", "#### 1.4.1.7")
        BASE_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_02",
        "Heading Hierarchy",
        "Introduce dot-split bug (1.4.1.7) into Section 1.4",
        mut_02_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f2_01_no_dot_split_anomalies"),
        "test_f2_01_no_dot_split_anomalies",
    )

    # 3. MUT_03: Space-separated heading in Chapter 4
    def mut_03_apply():
        content = BASE_MD.read_text(encoding="utf-8")
        content = content.replace("### 4.1", "### 4 1")
        BASE_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_03",
        "Heading Hierarchy",
        "Introduce space-separated heading (### 4 1) in Chapter 4",
        mut_03_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f2_02_no_space_separated_chapter4_headings"),
        "test_f2_02_no_space_separated_chapter4_headings",
    )

    # 4. MUT_04: Definition 1.4.1 number altered in base MD
    def mut_04_apply():
        content = BASE_MD.read_text(encoding="utf-8")
        content = content.replace("#### 1.4.1 ", "#### 1.4.999 ")
        BASE_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_04",
        "Definitions & Sections",
        "Alter Section 1.4.1 definition number in base MD",
        mut_04_apply,
        lambda: tester.run_integrity_script(),
        "scripts/verify_knowledge_integrity.py",
    )

    # 5. MUT_05: Unclosed quotation mark in base MD
    def mut_05_apply():
        content = BASE_MD.read_text(encoding="utf-8")
        content = content + '\n"Unbalanced quote test\n'
        BASE_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_05",
        "Syntax & Formatting",
        "Introduce unbalanced double quotation mark in base MD",
        mut_05_apply,
        lambda: tester.run_pytest_test("tests/test_tier2_boundaries.py::test_b3_13_quotation_marks_consistency"),
        "test_b3_13_quotation_marks_consistency",
    )

    # 6. MUT_06: Delete canonical table JSON bang_e_4a
    def mut_06_apply():
        if table_e4a.exists():
            table_e4a.unlink()

    tester.test_mutation(
        "MUT_06",
        "Tables & Schema",
        "Delete canonical table JSON bang_e_4a",
        mut_06_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f6_01_bang_e_4a_json_csv_exists"),
        "test_f6_01_bang_e_4a_json_csv_exists",
    )

    # 7. MUT_07: Corrupt cell value in Table 1 JSON
    def mut_07_apply():
        data = json.loads(table_1.read_text(encoding="utf-8"))
        table_1_text = json.dumps(data, ensure_ascii=False)
        table_1_text = table_1_text.replace("REI 150", "REI 999")
        table_1.write_text(table_1_text, encoding="utf-8")

    tester.test_mutation(
        "MUT_07",
        "Tables & RAG Query",
        "Corrupt REI 150 parameter to REI 999 in Table 1 JSON",
        mut_07_apply,
        lambda: tester.run_pytest_test("tests/test_tier4_real_world.py::test_scenario_s1_fire_compartment_rag_query"),
        "test_scenario_s1_fire_compartment_rag_query",
    )

    # 8. MUT_08: Inject delimiter separator row into Table 1 JSON rows
    def mut_08_apply():
        data = json.loads(table_1.read_text(encoding="utf-8"))
        data["rows"].insert(0, ["---", "---", "---"])
        table_1.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    tester.test_mutation(
        "MUT_08",
        "Tables & Schema",
        "Inject delimiter separator row into Table 1 JSON rows",
        mut_08_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f5_02_json_no_separator_row_in_rows"),
        "test_f5_02_json_no_separator_row_in_rows",
    )

    # 9. MUT_09: CSV row count mismatch with JSON
    csv_table_1 = TABLES_CSV_DIR / "bang_01_gioi_han_chiu_lua_loai.csv"
    tester.backup(csv_table_1)

    def mut_09_apply():
        content = csv_table_1.read_text(encoding="utf-8")
        content += "\nFake row,extra,cell,data\n"
        csv_table_1.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_09",
        "Tables & Schema",
        "Add extraneous row to Table 1 CSV causing JSON mismatch",
        mut_09_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f5_05_csv_row_count_matches_json"),
        "test_f5_05_csv_row_count_matches_json",
    )

    # 10. MUT_10: Create duplicate file bang_61.json
    dup_table = TABLES_JSON_DIR / "bang_61.json"

    def mut_10_apply():
        dup_table.write_text('{"headers": [], "rows": []}', encoding="utf-8")
        tester.extra_created_files.append(dup_table)

    tester.test_mutation(
        "MUT_10",
        "Tables & Schema",
        "Create forbidden duplicate file bang_61.json",
        mut_10_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f5_07_no_duplicate_bang_61_to_64_files"),
        "test_f5_07_no_duplicate_bang_61_to_64_files",
    )

    # 11. MUT_11: Delete all footnotes from JSON tables
    def mut_11_apply():
        for jf in TABLES_JSON_DIR.glob("*.json"):
            tester.backup(jf)
            d = json.loads(jf.read_text(encoding="utf-8"))
            if "footnotes" in d:
                d["footnotes"] = []
                jf.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")

    tester.test_mutation(
        "MUT_11",
        "Footnotes",
        "Wipe footnotes arrays from all JSON table assets",
        mut_11_apply,
        lambda: tester.run_pytest_test("tests/test_tier3_cross_features.py::test_pair_05_table_footnotes_to_md_render_sync"),
        "test_pair_05_table_footnotes_to_md_render_sync",
    )

    # 12. MUT_12: Delete an embedded table from base MD
    def mut_12_apply():
        content = BASE_MD.read_text(encoding="utf-8")
        content = content.replace("### Bảng E.4a", "### Bảng Deleted")
        lines = content.splitlines()
        new_lines = []
        skip = False
        for line in lines:
            if "### Bảng Deleted" in line:
                skip = True
            elif skip and line.startswith("### "):
                skip = False
            if not skip:
                new_lines.append(line)
        BASE_MD.write_text("\n".join(new_lines), encoding="utf-8")

    tester.test_mutation(
        "MUT_12",
        "Tables & Schema",
        "Delete embedded GFM table from base MD",
        mut_12_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f7_05_all_64_tables_embedded_in_md"),
        "test_f7_05_all_64_tables_embedded_in_md",
    )

    # 13. MUT_13: Remove first directive in SD1 MD
    def mut_13_apply():
        content = SD1_MD.read_text(encoding="utf-8")
        content = content.replace("1.1.2", "9.9.9")
        SD1_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_13",
        "Amendment SĐ1:2023",
        "Remove first directive 1.1.2 from SĐ1 MD",
        mut_13_apply,
        lambda: tester.run_pytest_test("tests/test_tier2_boundaries.py::test_b4_01_sd1_first_directive_boundary"),
        "test_b4_01_sd1_first_directive_boundary",
    )

    # 14. MUT_14: Corrupt YAML frontmatter in SD1
    def mut_14_apply():
        content = SD1_MD.read_text(encoding="utf-8")
        content = content.replace("id: SD1-2023-QCVN-06", "id: [broken yaml invalid")
        SD1_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_14",
        "Amendment SĐ1:2023",
        "Corrupt YAML frontmatter in SĐ1 MD",
        mut_14_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f9_06_sd1_frontmatter_valid"),
        "test_f9_06_sd1_frontmatter_valid",
    )

    # 15. MUT_15: Inject underscore artifact in SD1
    def mut_15_apply():
        content = SD1_MD.read_text(encoding="utf-8")
        content += "\nPhụ lục ____ bị bãi bỏ.\n"
        SD1_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_15",
        "Amendment SĐ1:2023",
        "Inject underscore artifact (____) into SĐ1 MD",
        mut_15_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f9_03_sd1_no_underscore_artifacts"),
        "test_f9_03_sd1_no_underscore_artifacts",
    )

    # 16. MUT_16: Cross-link pointing to non-existent anchor in base QCVN
    def mut_16_apply():
        content = SD1_MD.read_text(encoding="utf-8")
        content = content.replace("qcvn_06_2022_bxd.md#muc-1-1", "qcvn_06_2022_bxd.md#muc-non-existent-fake")
        SD1_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_16",
        "Amendment SĐ1:2023",
        "Corrupt hyperlink target to non-existent anchor in base QCVN",
        mut_16_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f11_03_sd1_hyperlink_targets_exist_in_base"),
        "test_f11_03_sd1_hyperlink_targets_exist_in_base",
    )

    # 17. MUT_17: Corrupt Table 10 GFM grid dimension in SD1
    def mut_17_apply():
        content = SD1_MD.read_text(encoding="utf-8")
        content = content.replace(
            "| Bậc chịu lửa của nhà | Cấp nguy hiểm cháy kết cấu của nhà |",
            "| Bậc chịu lửa của nhà |"
        )
        SD1_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_17",
        "Amendment SĐ1:2023",
        "Corrupt Table 10 column count in SĐ1 MD",
        mut_17_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f10_02_sd1_table_10_grid_dimensions"),
        "test_f10_02_sd1_table_10_grid_dimensions",
    )

    # 18. MUT_18: Delete a clause from clauses.json
    def mut_18_apply():
        data = json.loads(CLAUSES_JSON.read_text(encoding="utf-8"))
        data = data[:-1]
        CLAUSES_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    tester.test_mutation(
        "MUT_18",
        "AST Clause Tree",
        "Delete last clause from clauses.json",
        mut_18_apply,
        lambda: tester.run_pytest_test("tests/test_tier3_cross_features.py::test_pair_12_ast_clauses_to_qa_benchmark_bijection"),
        "test_pair_12_ast_clauses_to_qa_benchmark_bijection",
    )

    # 19. MUT_19: Invert line range in clauses.json
    def mut_19_apply():
        data = json.loads(CLAUSES_JSON.read_text(encoding="utf-8"))
        data[0]["line_start"] = 100
        data[0]["line_end"] = 50
        CLAUSES_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    tester.test_mutation(
        "MUT_19",
        "AST Clause Tree",
        "Invert line start/end range (100 > 50) in clauses.json",
        mut_19_apply,
        lambda: tester.run_pytest_test("tests/test_tier2_boundaries.py::test_b5_04_ast_no_inverted_ranges"),
        "test_b5_04_ast_no_inverted_ranges",
    )

    # 20. MUT_20: Point QA benchmark to non-existent anchor
    def mut_20_apply():
        data = json.loads(QA_JSON.read_text(encoding="utf-8"))
        data[0]["anchor"] = "non-existent-anchor-xyz"
        QA_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    tester.test_mutation(
        "MUT_20",
        "QA Benchmark",
        "Corrupt QA benchmark anchor to point to non-existent target",
        mut_20_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f13_04_qa_anchors_exist_in_markdown"),
        "test_f13_04_qa_anchors_exist_in_markdown",
    )

    # 21. MUT_21: Empty answer in QA benchmark
    def mut_21_apply():
        data = json.loads(QA_JSON.read_text(encoding="utf-8"))
        data[0]["answer"] = ""
        QA_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    tester.test_mutation(
        "MUT_21",
        "QA Benchmark",
        "Empty answer string in QA benchmark pair",
        mut_21_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f13_06_qa_questions_and_answers_non_empty"),
        "test_f13_06_qa_questions_and_answers_non_empty",
    )

    # 22. MUT_22: Corrupt legal_registry.yaml schema
    def mut_22_apply():
        content = REGISTRY_YAML.read_text(encoding="utf-8")
        content = content.replace("version: 0.3.0", "bad_version_format: [")
        REGISTRY_YAML.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_22",
        "Legal Spoke & Registry",
        "Corrupt required schema fields in legal_registry.yaml",
        mut_22_apply,
        lambda: tester.run_spoke_validator(),
        "scripts/validate_legal_spoke.py",
    )

    # 23. MUT_23: Delete Appendix A heading -> test_f2_06
    def mut_23_apply():
        content = BASE_MD.read_text(encoding="utf-8")
        content = content.replace("## PHỤ LỤC A", "## PHỤ LỤC X")
        BASE_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_23",
        "Heading & Appendix Structure",
        "Rename/Delete Appendix A main heading in base MD",
        mut_23_apply,
        lambda: tester.run_pytest_test("tests/test_tier1_feature_coverage.py::test_f2_06_appendix_main_titles_present"),
        "test_f2_06_appendix_main_titles_present",
    )

    # 24. MUT_24: Corrupt bidirectional navigation in S5 -> test_scenario_s5
    def mut_24_apply():
        content = SD1_MD.read_text(encoding="utf-8")
        content = content.replace("qcvn_06_2022_bxd.md#", "broken_target.md#")
        SD1_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_24",
        "Real-World Scenarios",
        "Corrupt cross-link base file target in SD1",
        mut_24_apply,
        lambda: tester.run_pytest_test("tests/test_tier4_real_world.py::test_scenario_s5_bidirectional_cross_reference_navigation"),
        "test_scenario_s5_bidirectional_cross_reference_navigation",
    )

    # 25. MUT_25: Corrupt water flow override in Table 10 -> test_scenario_s4
    def mut_25_apply():
        content = SD1_MD.read_text(encoding="utf-8")
        content = content.replace("sd1-bang-10", "corrupted-anchor")
        SD1_MD.write_text(content, encoding="utf-8")

    tester.test_mutation(
        "MUT_25",
        "Real-World Scenarios",
        "Corrupt anchor in SĐ1 Table 10",
        mut_25_apply,
        lambda: tester.run_pytest_test("tests/test_tier4_real_world.py::test_scenario_s4_amendment_water_flow_override"),
        "test_scenario_s4_amendment_water_flow_override",
    )

    # Summarize results
    total = len(tester.results)
    killed = sum(1 for r in tester.results if r["killed"])
    kill_rate = (killed / total) * 100

    print("\n" + "=" * 80)
    print("           ADVERSARIAL MUTATION STRESS TESTING SUMMARY")
    print("=" * 80)
    print(f"Total Mutants Tested : {total}")
    print(f"Mutants Killed       : {killed} ({kill_rate:.1f}%)")
    print(f"Mutants Survived     : {total - killed}")
    print("=" * 80)

    # Save mutation results to JSON
    out_file = REPO_ROOT / ".md" / "challenger2_mutation_matrix_results.json"
    out_file.write_text(json.dumps({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_mutations": total,
        "mutations_killed": killed,
        "kill_rate_pct": kill_rate,
        "results": tester.results,
    }, indent=2), encoding="utf-8")
    print(f"Saved mutation matrix results to: {out_file}")


if __name__ == "__main__":
    main()
