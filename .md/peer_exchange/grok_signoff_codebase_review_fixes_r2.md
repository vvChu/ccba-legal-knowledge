---
request_id: req-20261105-signoff-codebase-review-fixes-002
verdict: FINAL_ACCEPT
conditions: []
risk_score: 1
summary: All five round-1 conditions are closed in code. The three harnesses arm a
  threading.Timer before the stdout read and escalate SIGTERM, wait(5s), then SIGKILL
  on the process group. verify_cross_links.py accepts a missing binary only under
  sources/ with a metadata basename match. Ordered validator walks are sorted, wslpath
  uses errors=replace, and figure cards enter the NotebookLM manifest as POSIX rel
  paths.
telemetry:
  session_id: 6e2ea3db-d153-4502-b98d-4f92501976d7
  primary_model: grok-4.7-build
  input_tokens: 329524
  output_tokens: 6298
  reasoning_tokens: 4459
  cached_read_tokens: 241024
  total_tokens: 335822
  model_calls: 4
  turn_count: 3
  cost_usd: 0.114
  cost_mode: exact
  duration_seconds: 96.08
  degraded_reasoning: false
---

## Delta verification (round 2)

| ID | Prior condition | Verdict | Evidence |
|---|---|---|---|
| SPEC-06-TIMEOUT | Timeout must fire while stdout stays open; 5s grace before SIGKILL | Closed | `verify_legal_harness.py` 290–321 and 374–396, `verify_legal_intel_harness.py` 262–293 and 366–388, `verify_legal_ingest_harness.py` 279–310 and 388–410. Each imports `threading`, starts `threading.Timer(self.step_timeout, _on_timeout)` before `for line in proc.stdout`, and sets exit code 124 from `timed_out`. `cleanup()` sends `os.killpg(SIGTERM)`, `active_process.wait(timeout=5.0)`, then `SIGKILL` only when `poll()` is still `None`. Windows uses `taskkill /F /T`. The 0.50s hang run is the submitter’s attestation; the control flow matches that result. |
| SPEC-08-CROSSLINKS | Basename plus `sources/` contract, same as Gate 2 | Closed | `verify_cross_links.py` 36–79 and 96–102. `_is_valid_gitignored_source_link` loads `metadata.yaml`, requires `sources/` (or a resolved `sources` directory), and matches `.pdf` to `pdf_path` / `raw_scan_pdf` (fallback `{bundle}.pdf`) and `.docx`/`.doc` to `source_file` (fallback `{bundle}.docx`). A missing metadata file or a basename miss returns false. `yaml` is imported. |
| STD-SORT-RESIDUAL | Inode-stable ordered walks | Closed | Claimed `validate_legal_spoke.py` loops at 334, 345, 444, 479, 514, 612, 638, 1130, 1288, 1318, 1330, 1355, 1380, 1452, 1468, 1567, 1789, 1798, 1877, 1936, 1939, 1952, 2043, 2106, and 2110 are wrapped in `sorted(...)`. Remaining bare `iterdir` / `glob` uses are emptiness or set probes (lines 365, 1371, 1449, 1884). |
| STD-03-WSLPATH | `errors="replace"` on `wslpath` | Closed | `check_hub_import_depth.py` 56–63 sets `encoding="utf-8"` and `errors="replace"` on `subprocess.run(["wslpath", "-u", raw], ...)`. |
| SPEC-01-FIGURES | Figure visual cards in the manifest | Closed | `sync_notebooklm_knowledge.py` 176–197, inside `ultra_full`, appends `figures/cards/*.md` with `type: "Figure Visual Card"` and `rel_path: PurePosixPath(...as_posix())`, scanned with `sorted(cards_dir.glob("*.md"))`. The stated count of 476 cards was not re-counted in this pass. |

Round-1 blockers SPEC-06-TIMEOUT and SPEC-08-CROSSLINKS are cleared. No new blocking defect showed up in these seven files.