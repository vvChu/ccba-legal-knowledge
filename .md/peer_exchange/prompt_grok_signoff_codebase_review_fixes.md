---
request_id: "req-20261105-signoff-codebase-review-fixes-001"
from_agent: "antigravity"
to_agent: "grok"
request_type: "review"
profile: "signoff_diff"
subject: "Acceptance Sign-off: Khắc phục 20 lỗi Blocking & 11 cải tiến từ Parallel Codebase Review (/ccba-code-review)"
timestamp: "2026-11-05T21:42:00+07:00"
source_documents:
  - /home/vvc/ccba/ccba-legal-knowledge/AGENTS.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/knowledge/session_learnings.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/knowledge/specs/spec-deterministic-zero-data-loss-legal-pipeline.md
output_path: ".md/peer_exchange/grok_signoff_codebase_review_fixes.md"
target_files:
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/setup_pre_commit.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/sync_adr_matrix.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/sync_notebooklm_knowledge.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/hydrate_sources_from_vault.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/benchmark_legal_rag.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/sync_expansion_roadmap.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/verify_formula_visual_matrix.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/verify_cross_links.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/verify_docx_against_pdf.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/verify_all_docs_against_pdf.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/query_hub_catalog.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/_guardrails/check_spoke_cleanliness.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/_guardrails/check_hub_import_depth.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py
  - /home/vvc/ccba/ccba-legal-knowledge/.md/tools/verify_ground_truth_parity.py
  - /home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py
  - /home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py
  - /home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py
  - /home/vvc/ccba/ccba-legal-knowledge/tests/e2e/test_tier3_cross_features.py
  - /home/vvc/ccba/ccba-legal-knowledge/tests/e2e/test_m2_adversarial.py
  - /home/vvc/ccba/ccba-legal-knowledge/tests/integration/test_spoke_cli.py
---

# 🎯 Yêu Cầu Nghiệm Thu Mã Nguồn (Acceptance Sign-off — Parallel Codebase Review Fixes)

Chúng tôi đã thực hiện kiểm toán song song toàn bộ codebase (`/ccba-code-review` ở chế độ `codebase parallel` trên 2 trục: **Standards** và **Spec**) và hoàn tất khắc phục **20 lỗi Blocking** + **11 điểm cải tiến** trên **22 tệp**.

## 📍 Bản Đồ Vị Trí Thay Đổi (Exact Line Ranges để đọc kiểm chứng nhanh trong $\le 8$ lượt tool)

### I. Trục Đặc Tả & Kiến Trúc (`SPEC-01` .. `SPEC-08`)

1. **`SPEC-01` & `SPEC-02` (Workspace Root Isolation & POSIX Path Contract):**
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/sync_notebooklm_knowledge.py` (dòng `46-195`):
     - `get_canonical_manifest(root_dir)` đọc `registry_path = root_dir / "legal_registry.yaml"` thay vì hằng toàn cục `REGISTRY_PATH`, cho phép cô lập `tmp_path` khi test.
     - Toàn bộ 6 loại tài nguyên (`normative_markdown`, `comparative_matrix`, `technical_annex`, `form_template`, `table_schema_catalog`, `figure_visual_card`) lưu `rel_path` dưới dạng `PurePosixPath(path.relative_to(root_dir).as_posix())`.
   - `/home/vvc/ccba/ccba-legal-knowledge/.md/tools/verify_ground_truth_parity.py` (dòng `61-65`, `155-395`):
     - `_load_registry` đọc `self.root_dir / "legal_registry.yaml"`.
     - Toàn bộ 16 vị trí sinh đường dẫn tương đối (`bundle_path`, `markdown_file`, `docx_file`, `pdf_file`, `tables`, `templates`, `figures`) chuẩn hóa sang `.relative_to(self.root_dir).as_posix()`.

2. **`SPEC-03` & `STD-06` (Pre-commit Path & Root Directory Resolution):**
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/setup_pre_commit.py` (dòng `14-58`):
     - Đổi `root_dir = Path(__file__).resolve().parent.parent` (trước đó thiếu `.parent` nên trỏ nhầm vào `scripts/.git`).
     - Trỏ hook pre-commit về `scripts/_guardrails/check_spoke_cleanliness.py` và thu hẹp `except OSError:`.
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/sync_adr_matrix.py` (dòng `14-48`):
     - Đổi `root_dir = Path(__file__).resolve().parent.parent` và bọc `sorted(skills_dir.glob("*/SKILL.md"))`.

3. **`SPEC-04` & `SPEC-07` (Test Suite Alignment & Registry Invariants):**
   - `/home/vvc/ccba/ccba-legal-knowledge/tests/e2e/test_tier3_cross_features.py` (dòng `156-175`):
     - Thay thế import mô-đun đã xóa `scripts.verify_knowledge_integrity` bằng `LegalSpokeValidator` trong `test_pair_13_validate_spoke_and_knowledge_integrity` và `test_pair_14_knowledge_integrity_and_docx_parser`.
   - `/home/vvc/ccba/ccba-legal-knowledge/tests/e2e/test_m2_adversarial.py` (dòng `20-35`):
     - Bổ sung guard `if not DOCX_PATH.exists(): pytest.skip(...)` theo ADR 0035 Cloud Binary Vault.
   - `/home/vvc/ccba/ccba-legal-knowledge/tests/integration/test_spoke_cli.py` (dòng `164-185`):
     - Kiểm tra bất biến `sum(reg_cats.values()) == len(stats_entries)` (`106` văn bản) và ngưỡng sàn tối thiểu từng phân khu thay vì khóa cứng con số `91` văn bản cũ.

4. **`SPEC-05` (Decree Routing in Spoke CLI):**
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py` (dòng `194-214`):
     - Sửa `default_section_key` trong lệnh `ingest`: phân loại Nghị định (`nghi_dinh*` hoặc `NĐ-CP`) vào `"decrees"` thay vì gộp chung vào `"laws"`.

5. **`SPEC-06` (`SIGKILL` Process-Group Escalation & `300.0s` Timeout — `RULE-5.6`):**
   - `/home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py` (dòng `204-246`) và `/home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py` (dòng `209-251`):
     - Đặt `step_timeout: float = 300.0` và bổ sung leo thang `SIGTERM` $\to$ `proc.wait(timeout=5)` $\to$ `SIGKILL` trên toàn bộ process group (`os.killpg`).

6. **`SPEC-08` (Cloud Vault Link Fallback — `RULE-5.7`):**
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/verify_cross_links.py` (dòng `45-100`):
     - Bổ sung kiểm tra fallback qua `metadata.yaml` (`pdf_sha256` / `vault_path` / `source_url`) khi xác thực liên kết `.pdf`/`.docx`/`sources` không có mặt cục bộ do `.gitignore`.

### II. Trục Tiêu Chuẩn Mã Nguồn & Guardrails (`STD-01` .. `STD-23`)

1. **Explicit Subprocess UTF-8 Encoding (`STD-01` .. `STD-03`):**
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/hydrate_sources_from_vault.py` (dòng `82-122`), `/home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py` (dòng `515-527`, `878-888`), `/home/vvc/ccba/ccba-legal-knowledge/scripts/_guardrails/check_hub_import_depth.py` (dòng `143-152`): Bổ sung `encoding="utf-8", errors="replace"`.

2. **Missing Imports & Machine-Path Annotation (`STD-04`, `STD-05`, `STD-22`, `STD-23`):**
   - `/home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py` (dòng `21`, `300-355`): Bổ sung `Tuple` vào `typing` import và dọn biến không dùng `start_ts`, `timed_out`.
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py` (dòng `14`, `20-35`): Bổ sung `import unicodedata` cho Gate 11 và dọn các hằng import không dùng.
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/hydrate_sources_from_vault.py` (dòng `28-40`): Gắn `# ccba:allow-machine-path` cho đường dẫn fallback Windows và bọc `sorted(...)` cho `.glob` / `.rglob`.

3. **Multi-Key Deterministic Sorting & Inode Invariance (`STD-07` .. `STD-12`):**
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/benchmark_legal_rag.py` (dòng `50-73`): Thay `reverse=True` bằng `key=lambda x: (-round(x[0], 4), x[1])` và dùng `random.Random(42).sample(...)`.
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/sync_expansion_roadmap.py` (dòng `94-160`): Thay `reverse=True` bằng `key=lambda x: (-round(float(x["final_score"]), 4), str(x.get("document_number", "")))` và bọc `sorted(...)` cho `.rglob` / `.glob`.
   - Bọc `sorted(...)` cho toàn bộ lệnh quét thư mục trong `verify_formula_visual_matrix.py`, `verify_ground_truth_parity.py`, `validate_legal_spoke.py`, `verify_cross_links.py`, `verify_docx_against_pdf.py`, `verify_all_docs_against_pdf.py`.

4. **AST-Based Docstring & Multiline Import Span Guardrails (`STD-13` .. `STD-15`):**
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/query_hub_catalog.py` (dòng `23-49`): Định kiểu đầy đủ `list[dict[str, Any]]`.
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/_guardrails/check_spoke_cleanliness.py` (dòng `140-265`): Dùng AST `_collect_docstring_lines` cho tệp `.py` thay vì đếm chuỗi `"""` thủ công dễ bị lệch trạng thái khi gặp `"""` nội dòng.
   - `/home/vvc/ccba/ccba-legal-knowledge/scripts/_guardrails/check_hub_import_depth.py` (dòng `94-129`): Quét toàn bộ dải dòng `[node.lineno, end_lineno]` cho chú thích `# ccba:quarantine` / `# noqa` trên câu lệnh import nhiều dòng.

## ✅ Bằng Chứng Kiểm Định Thực Thi

- `python3 scripts/_guardrails/check_spoke_cleanliness.py` $\to$ **PASS** (`15/15` scripts, `0` leaks).
- `python3 scripts/_guardrails/check_hub_import_depth.py` $\to$ **PASS** (`44` files scanned, `0` violations).
- `python3 -m pytest tests/unit/ tests/integration/ -q` $\to$ **PASS** (`174 passed in 29.60s`).
- `python3 -m pytest tests/e2e/test_tier3_cross_features.py -k "test_pair_13 or test_pair_14" -q` $\to$ **PASS** (`2 passed in 1.55s`).
- `python3 .agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode smoke` $\to$ **PASS** (`15/15` Gates, `0 Errors`).
- `python3 .agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py --mode smoke` $\to$ **PASS** (`4/4` Deep Seam contracts).
- `python3 .agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py --mode smoke` $\to$ **PASS** (`5/5` Pipeline contracts).

Đề nghị Grok thẩm định các thay đổi trên và cấp phán quyết nghiệm thu (`FINAL_ACCEPT` / `APPROVE` / `APPROVE_WITH_CONDITIONS` / `REJECT`).
