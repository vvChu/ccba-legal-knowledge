---
request_id: req-20261105-signoff-codebase-review-fixes-001
verdict: APPROVE_WITH_CONDITIONS
conditions:
- id: SPEC-06-TIMEOUT
  description: Per-step 300s timeout in the three verification harnesses is applied
    only after the stdout read loop finishes. A child that stays alive with the pipe
    open never reaches proc.wait, so SIGTERM/SIGKILL escalation does not run. Cleanup
    uses time.sleep(0.2) and verify_legal_harness.py sends SIGKILL without a poll.
    Arm the timeout while streaming, then SIGTERM, proc.wait(timeout=5), then SIGKILL
    on the process group.
  blocking: true
  source_profiles: []
- id: SPEC-08-CROSSLINKS
  description: scripts/verify_cross_links.py treats a missing .pdf/.docx/.doc link,
    or a target named sources, as valid whenever metadata.yaml exists. It does not
    match the link basename to pdf_path, raw_scan_pdf, or source_file. Bring that
    fallback in line with validate_legal_spoke._validate_index_md_links (RULE-5.7).
    Gate 2 itself already enforces the basename contract.
  blocking: true
  source_profiles: []
- id: STD-SORT-RESIDUAL
  description: validate_legal_spoke.py still walks several cat_dir.iterdir() and rglob()
    calls without sorted(). Wrap scans that append ordered findings so diagnostics
    stay inode-stable.
  blocking: false
  source_profiles: []
- id: STD-03-WSLPATH
  description: check_hub_import_depth.py wslpath subprocess sets encoding utf-8 and
    omits errors=replace. UnicodeDecodeError is outside the OSError/SubprocessError
    handler.
  blocking: false
  source_profiles: []
- id: SPEC-01-FIGURES
  description: sync_notebooklm_knowledge.get_canonical_manifest stores PurePosixPath
    rel_path for normative markdown, templates, CSV tables, annexes, and comparison
    matrices. Figure visual cards are absent from the manifest.
  blocking: false
  source_profiles: []
risk_score: 3
summary: Registry isolation, POSIX rel paths, pre-commit root, decree section routing,
  test realignment, UTF-8 on the main subprocesses, deterministic sort keys, and AST
  guardrails are in place. Gate 2 already matches RULE-5.7. Sign-off stays conditional
  because the harness timeout does not cover a hung child and verify_cross_links.py
  still accepts missing binaries from metadata.yaml presence alone. Cited smoke runs
  do not exercise the subprocess timeout path.
telemetry:
  session_id: 7b7b9a49-b881-4134-9ef2-d4884d782213
  primary_model: grok-4.7-build
  input_tokens: 738197
  output_tokens: 14865
  reasoning_tokens: 9253
  cached_read_tokens: 582272
  total_tokens: 753062
  model_calls: 16
  turn_count: 2
  cost_usd: 0.2353
  cost_mode: exact
  duration_seconds: 49.06
  degraded_reasoning: false
---

## Delta verification

| ID | Claim | Verdict | Evidence |
|---|---|---|---|
| SPEC-01 | Manifest and parity load registry from the injected root | Pass | `get_canonical_manifest` uses `root_dir / "legal_registry.yaml"`. `_load_registry` uses `self.root_dir / "legal_registry.yaml"`. Module-level `REGISTRY_PATH` / `REGISTRY_FILE` remain unused by those loaders. |
| SPEC-02 | Relative paths are POSIX | Pass with gap | `PurePosixPath(...as_posix())` on the five collected NotebookLM types. Parity tickets use `.relative_to(self.root_dir).as_posix()`. Figure cards are not emitted (SPEC-01-FIGURES). Cited line spans are stale. |
| SPEC-03 / STD-06 | Pre-commit and ADR root resolve to the repo | Pass | `setup_pre_commit.py` line 16: `parent.parent`. Hook runs `scripts/_guardrails/check_spoke_cleanliness.py` then `scripts/validate_legal_spoke.py`. `except OSError`. `sync_adr_matrix.py` line 240: same root; `sorted(skills_dir.glob("*/SKILL.md"))` at line 165. |
| SPEC-04 | Deleted `verify_knowledge_integrity` import removed | Pass | `test_pair_13_verify_script_measures_100_percent_content` and `test_pair_14_verify_script_measures_100_percent_headings` call `LegalSpokeValidator`. Names differ from the sign-off map. |
| SPEC-07 | Registry counts are floors, not a frozen 91 | Pass | `test_spoke_stats_computation`: `sum(reg_cats.values()) == len(stats_entries)`, `doc_count >= 106`, floors 53 / 17 / 33 / 3. Actual lines are 60–81. |
| SPEC-04b | Vault-missing DOCX skips | Pass | `test_m2_adversarial.py` skips at the two `docx.Document(DOCX_PATH)` sites (lines 160 and 221). |
| SPEC-05 | Nghị định routes to `decrees` | Pass | `spoke_cli.py` 1216–1222: slug `nghi_dinh*`, type containing `nghị định`, or `NĐ-CP` selects `decrees`; other `01_vbpl` stays `laws`; else `standards`. An already matched entry stays in its current section. |
| SPEC-06 / RULE-5.6 | 300s timeout and process-group kill | Fail | All three harnesses set `step_timeout: float = 300.0`, `os.setsid` / `CREATE_NEW_PROCESS_GROUP`, and `os.killpg`. `wait(timeout=self.step_timeout)` sits after the stdout loop. Grace is `time.sleep(0.2)`, and the knowledge harness SIGKILLs without a poll. Smoke evidence does not run this path. |
| SPEC-08 / RULE-5.7 | Gitignored binary links attested from metadata | Split | Gate 2 `_validate_index_md_links` skips `exists()` for `.pdf`/`.docx`/`sources` and requires `sources/` plus basename of `pdf_path` / `raw_scan_pdf` / `source_file`. `verify_cross_links.py` 49–58 returns success when `metadata.yaml` exists and does not read `pdf_sha256`, `vault_path`, or `source_url`. |
| STD-01..03 | Subprocess UTF-8 | Pass with gap | `hydrate_sources_from_vault.py` rclone calls and both `validate_legal_spoke.py` `subprocess.run` calls set `encoding="utf-8", errors="replace"`. `check_hub_import_depth.py` wslpath sets encoding only (STD-03-WSLPATH). |
| STD-04, 05, 22, 23 | Imports and machine-path annotation | Pass | `verify_legal_harness.py` imports `Tuple`. `validate_legal_spoke.py` imports `unicodedata` and uses it at Gate 11. Windows drive candidates carry `# ccba:allow-machine-path`. |
| STD-07..12 | Deterministic order | Pass with gap | RAG sort key `(-round(x[0], 4), x[1])` and `random.Random(42)`. Roadmap key `(-round(float(final_score), 4), document_number)`. Formula, cross-link, DOCX/PDF, and parity scans are sorted. Many `validate_legal_spoke.py` `iterdir()` / `rglob()` calls remain unsorted. |
| STD-13..15 | Typed catalog, AST docstrings, import span | Pass | `load_catalog` returns `list[dict[str, Any]]`. `_collect_docstring_lines` covers module, class, and function docstrings. Hub-import scan checks `[lineno, end_lineno]` for `ccba:quarantine` and `noqa`. |

## Conditions to close before FINAL_ACCEPT

1. **SPEC-06-TIMEOUT (blocking).** Stream output under the 300s budget. On expiry, signal the process group with SIGTERM, wait up to 5 seconds, then SIGKILL. Poll before the second signal in `verify_legal_harness.py`.
2. **SPEC-08-CROSSLINKS (blocking).** Accept a missing binary link only when the href is under `sources/` and the basename matches `pdf_path`, `raw_scan_pdf`, or `source_file` in that bundle's `metadata.yaml`.
3. **STD-SORT-RESIDUAL, STD-03-WSLPATH, SPEC-01-FIGURES (non-blocking).** Sort ordered validator walks, set `errors="replace"` on `wslpath`, and include figure cards in the NotebookLM manifest if that source type is in scope.

Master Gate 2, pre-commit root, decree routing, POSIX registry paths, and the cited unit/integration alignment can stay. Smoke PASS does not cover the hung-child path.