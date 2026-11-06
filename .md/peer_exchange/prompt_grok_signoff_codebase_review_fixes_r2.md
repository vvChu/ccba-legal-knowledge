---
request_id: "req-20261105-signoff-codebase-review-fixes-002"
from_agent: "antigravity"
to_agent: "grok"
request_type: "review"
profile: "signoff_diff"
resume_session_id: "7b7b9a49-b881-4134-9ef2-d4884d782213"
fork_session: true
subject: "Stage 3 Round 2 Sign-off: Đã đóng hoàn tất 2 Blocking Conditions (SPEC-06-TIMEOUT, SPEC-08-CROSSLINKS) & 3 Non-blocking Conditions (STD-SORT-RESIDUAL, STD-03-WSLPATH, SPEC-01-FIGURES)"
timestamp: "2026-11-05T21:52:00+07:00"
source_documents:
  - /home/vvc/ccba/ccba-legal-knowledge/.md/peer_exchange/grok_signoff_codebase_review_fixes.md
output_path: ".md/peer_exchange/grok_signoff_codebase_review_fixes_r2.md"
target_files:
  - /home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py
  - /home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py
  - /home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/verify_cross_links.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/_guardrails/check_hub_import_depth.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/sync_notebooklm_knowledge.py
---

# 🎯 Yêu Cầu Nghiệm Thu Vòng 2 (`FINAL_ACCEPT` — Resuming `7b7b9a49-b881-4134-9ef2-d4884d782213`)

Chúng tôi đã tiếp thu nguyên bản (`[ADOPT_AS_IS]`) và khắc phục triệt để cả **2 điều kiện chặn** (`SPEC-06-TIMEOUT`, `SPEC-08-CROSSLINKS`) cùng **3 điều kiện khuyến nghị** (`STD-SORT-RESIDUAL`, `STD-03-WSLPATH`, `SPEC-01-FIGURES`):

1. **`SPEC-06-TIMEOUT` (Blocking — Armed Streaming Watchdog & 5s Grace before `SIGKILL`):**
   - Tại `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py` (dòng `289-325`, `383-395`), `.agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py` (dòng `261-297`, `378-388`), và `.agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py` (dòng `278-314`, `400-410`):
     - Kích hoạt `threading.Timer(self.step_timeout, _on_timeout)` ngay trước vòng lặp đọc `for line in proc.stdout:` để cắt đứt tiến trình con bị treo khi vẫn giữ mở stdout pipe.
     - Trong `cleanup()`, gửi `os.killpg(pgid, signal.SIGTERM)`, chờ `self.active_process.wait(timeout=5.0)`, sau đó kiểm tra `if self.active_process.poll() is None: os.killpg(pgid, signal.SIGKILL)`.
     - Đã kiểm thử thực thi với tiến trình con giả lập giữ mở stdout pipe và `time.sleep(30)` ở `step_timeout=0.5`: ngắt chính xác sau `0.50s` và trả về `exit_code = 124`.

2. **`SPEC-08-CROSSLINKS` (Blocking — `RULE-5.7` Basename & `sources/` Contract in `verify_cross_links.py`):**
   - Tại `scripts/verify_cross_links.py` (dòng `36-105`):
     - Hàm `_is_valid_gitignored_source_link(target_rel_path, target_file_path, bundle_dir)` tải `metadata.yaml`, bắt buộc đường dẫn nằm trong `sources/` và khớp basename với `pdf_path` / `raw_scan_pdf` (cho `.pdf`) hoặc `source_file` / `{bundle_dir.name}.docx` (cho `.docx`/`.doc`), đồng nhất 100% với `validate_legal_spoke._validate_index_md_links`.

3. **`STD-SORT-RESIDUAL` (Non-blocking — Inode-Stable Walks in `validate_legal_spoke.py`):**
   - Tại `scripts/validate_legal_spoke.py` (dòng `334`, `345`, `444`, `479`, `514`, `612`, `638`, `1130`, `1288`, `1318`, `1330`, `1355`, `1380`, `1452`, `1468`, `1567`, `1789`, `1798`, `1877`, `1936`, `1939`, `1952`, `2043`, `2106`, `2110`): Đã bọc `sorted(...)` cho toàn bộ các vòng lặp `.iterdir()`, `.glob()`, `.rglob()`.

4. **`STD-03-WSLPATH` (Non-blocking — `errors="replace"` on `wslpath`):**
   - Tại `scripts/_guardrails/check_hub_import_depth.py` (dòng `56-64`): Bổ sung `errors="replace"` vào `subprocess.run(["wslpath", "-u", raw], ...)`.

5. **`SPEC-01-FIGURES` (Non-blocking — Figure Visual Cards in `sync_notebooklm_knowledge.py`):**
   - Tại `scripts/sync_notebooklm_knowledge.py` (dòng `176-198`): Bổ sung thu thập `figures/cards/*.md` (`type: "Figure Visual Card"`, `rel_path: PurePosixPath(fc.relative_to(root_dir).as_posix())`) vào `get_canonical_manifest(..., ultra_full=True)` (thu thập đủ 476 thẻ hình).

Đề nghị Grok kiểm tra nhanh các vị trí vừa cập nhật và cấp phán quyết **`FINAL_ACCEPT`**.
