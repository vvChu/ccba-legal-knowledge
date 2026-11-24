# Walkthrough: Phát Hành Tính Năng PR #79 — Dọn 24 Vị Trí Bold-Glue `____`, Gỡ `_recheck_parity_nfc` & Đồng Bộ Fallback CI (2026-11-24)

> **Mục tiêu:** Đóng vòng hậu hợp nhất Hub `vvChu/ccba-agent-platform#892` (`PR #895` / `5d1a8af8`), dọn sạch toàn bộ `24` vị trí `____` bold-glue trên `8` văn bản quy phạm `active`, gỡ hàm vá tạm `_recheck_parity_nfc` tại validator Spoke, đồng bộ rule #13 `MALFORMED_BOLD_GLUE` vào nhánh fallback CI và bổ sung kiểm thử hồi quy.
> **Trạng thái:** ✅ **MERGED VÀO MAIN (`PR #79`, Squash Commit `b0b5d12`)**
> - **Spoke PR #79:** [vvChu/ccba-legal-knowledge#79](https://github.com/vvChu/ccba-legal-knowledge/pull/79) — Feature Commits: `ca6027f`, `ff7a5aa` → Squash Merge Commit: `b0b5d12` (`2026-11-24T05:48:57Z`, `6/6` CI Checks Passed, `0` Copilot comments)
> - **Branch cleanup:** Đã xóa local & remote `fix/clean-bold-glue-and-remove-nfc-recheck`
> - **Issue liên quan:** Hub [vvChu/ccba-agent-platform#892](https://github.com/vvChu/ccba-agent-platform/issues/892) (`CLOSED` sau Hub PR `#895`)

## 1. Tóm Tắt Thay Đổi (`PR #79`, `11` tệp, `+89/-77`)
- **Dọn `24` vị trí `____` bold-glue trên `8` văn bản VBPL `active` (`0` thay đổi từ vựng quy phạm):**
  - `20` vị trí bị `MALFORMED_BOLD_GLUE` bắt: [`thong_tu_31_2026_tt_bxd.md`](../../../legal_docs/01_vbpl/thong_tu_31_2026_tt_bxd/thong_tu_31_2026_tt_bxd.md) (`9`), [`luat_dat_dai_2024_31_2024_qh15.md`](../../../legal_docs/01_vbpl/luat_dat_dai_2024_31_2024_qh15/luat_dat_dai_2024_31_2024_qh15.md) (`8` trên `5` dòng), [`luat_kien_truc_2019_40_2019_qh14.md`](../../../legal_docs/01_vbpl/luat_kien_truc_2019_40_2019_qh14/luat_kien_truc_2019_40_2019_qh14.md) (`1`), [`nghi_dinh_17_2025_nd_cp.md`](../../../legal_docs/01_vbpl/nghi_dinh_17_2025_nd_cp/nghi_dinh_17_2025_nd_cp.md) (`1`), [`thong_tu_20_2026_tt_bkhcn.md`](../../../legal_docs/01_vbpl/thong_tu_20_2026_tt_bkhcn/thong_tu_20_2026_tt_bkhcn.md) (`1`).
  - `4` vị trí bold-glue ngoài regex (đứng sau `“` hoặc trước `\[`): [`luat_57_2024_qh15.md`](../../../legal_docs/01_vbpl/luat_57_2024_qh15/luat_57_2024_qh15.md) (`1`), [`14_vbhn_bgddt.md`](../../../legal_docs/01_vbpl/14_vbhn_bgddt/14_vbhn_bgddt.md) (`1` + gỡ `__` lẻ thừa cuối liên kết footnote), [`83_vbhn_tt_bxd.md`](../../../legal_docs/01_vbpl/83_vbhn_tt_bxd/83_vbhn_tt_bxd.md) (`2`).
- **Gỡ hàm vá tạm `_recheck_parity_nfc` tại [`validate_legal_spoke.py`](../../../scripts/validate_legal_spoke.py) (`-56` dòng):**
  - Xóa `@classmethod def _recheck_parity_nfc` và lời gọi tại Gate 11 sau khi `ccba_legal.provenance` (Hub PR `#895`) đã chuẩn hóa NFC tại nguồn (`106/107` bundle DOCX đạt trực tiếp, `qcvn_06_2022_bxd` qua `goc_verified` VBHN).
  - Giữ nguyên `@staticmethod def _norm_words_nfc` cho nhánh standalone fallback `_standalone_verify_bundle` khi chạy trên GitHub Actions CI không cài `ccba-legal-intel`.
- **Đồng bộ fallback CI & bổ sung test hồi quy:**
  - [`lint_visual_parity.py`](../../../scripts/lint_visual_parity.py) (`+19` dòng): đồng bộ 1:1 `_MALFORMED_BOLD_GLUE_RE`, `_is_bold_glue_exempt` (`templates/` & `sources/`), và `in_code_fence` vào nhánh fallback.
  - [`test_validate_legal_spoke.py`](../../../tests/integration/test_validate_legal_spoke.py) (`+49` dòng): bổ sung `test_lint_visual_parity_fallback_detects_malformed_bold_glue` giả lập chặn `ccba_legal` trong `sys.modules`.

## 2. Ma Trận Nghiệm Thu Kiểm Định (`PR #79`)

| Cổng Kiểm Định | Lệnh Thực Thi | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :---: |
| **TRIHT Pre & Post Cleanliness** | `check_release_cleanliness.py --phase pre/post --repo-root .` | Clean 100%, 100% Hermetic | ✅ **PASSED** |
| **Visual Parity Linter (`.venv` & CI Fallback)** | `.venv/bin/python scripts/lint_visual_parity.py` (cả 2 chế độ) | `1220` tệp, `Total errors : 0` | ✅ **PASSED** |
| **Master Legal 15 CI Gates (`.venv` & CI Fallback)** | `.venv/bin/python scripts/validate_legal_spoke.py` (full & `--skip-pdf-vault` chặn `ccba_legal`) | `Errors: 0 \| Warnings: 0` | ✅ **PASSED** |
| **Cleanliness & Import Depth** | `check_spoke_cleanliness.py` + `check_hub_import_depth.py` | Script Budget `15/15`, `48` file(s) `0` vi phạm | ✅ **PASSED** |
| **Unit & Integration Tests** | `pytest tests/unit tests/integration/test_validate_legal_spoke.py -q` | `144 passed in 0.07s` | ✅ **PASSED** |
| **Door Triage & Diff Hygiene** | `ccba_harness door-triage --enforce-tradeoff-card` + `sanitize_review_diff.py` | `ONE_WAY_DOOR` (`tradeoff_card_valid: true`), `0` secrets | ✅ **PASSED** |
| **GitHub Actions CI & Copilot** | `gh pr checks 79` + `audit_pr_comments.py --pr 79` | `6/6` CI Checks Passed, `0` Copilot comments | ✅ **PASSED** |

---

## Lịch Sử Trước Đó — PR #75 — Đồng Bộ Hub Skills & Guardrails (2026-11-24)

> **Mục tiêu:** Ghi nhận kết quả đồng bộ Spoke `/ccba-update-spoke` từ Hub `ccba-agent-platform@6a21510f` (bao gồm RFCs `#873`/`#877`, `#874`/`#880`, `#882`, `#884`, `#870`), dọn `6` skill `scope: hub`, cập nhật `scripts/_guardrails/*` và làm mới `docs/adr/TRACEABILITY_MATRIX.md` qua Gate 10.
> **Trạng thái:** ✅ **MERGED VÀO MAIN (`PR #75`, Squash Commit `67356cf`)**
> - **Spoke PR #75:** [vvChu/ccba-legal-knowledge#75](https://github.com/vvChu/ccba-legal-knowledge/pull/75) — Feature Commit: `9347c44` → Squash Merge Commit: `67356cf` (`6/6` CI Checks Passed, `0` Copilot comments)
> - **Branch cleanup:** Đã xóa local & remote `chore/sync-hub-skills-20261124`

## 1. Tóm Tắt Thay Đổi & Đồng Bộ Hub → Spoke (`PR #75`)
- **Đồng bộ `.agents/skills/` cục bộ (gitignored theo `.gitignore:21`):**
  - **57** skill cập nhật từ Hub (`platform-loader`, `ccba-legal-ingest`, `ccba-maskara`, `ccba-update-spoke`, v.v.) + **2** guardrails (`check_spoke_cleanliness.py`, `_module_size_budget.py`).
  - **6** skill `scope: hub` được dọn khỏi Spoke: `ccba-autoresearch`, `ccba-build-skill`, `ccba-graduate-rd`, `ccba-init-spoke`, `ccba-spoke-adopter`, `ccba-sync-upstream`.
  - **10** thành phần đặc thù Spoke được bảo toàn: `ccba-infrastructure-manager`, `ccba-verify-legal-ingest`, `ccba-verify-legal-intel`, `ccba-verify-legal-knowledge`, `form-template-cleaner` và 5 workflow `.bak`.
  - **Snapshot sao lưu:** `.md/backups/agents_backup_20261124_002942`; dry-run sau đồng bộ đạt `0 mới, 0 cập nhật, 82 không đổi, 0 dọn dẹp cũ, 10 giữ nguyên nội bộ`.
- **Thay đổi được Git theo dõi (4 tệp):**
  - [`check_spoke_cleanliness.py`](../../../scripts/_guardrails/check_spoke_cleanliness.py): bổ sung `_iter_budget_files` và cập nhật `DEFAULT_PRODUCTION_ROOTS`.
  - [`_module_size_budget.py`](../../../scripts/_guardrails/_module_size_budget.py): đồng bộ `frontend/src` trong `DEFAULT_PRODUCTION_ROOTS`.
  - [`guardrails_manifest.json`](../../../scripts/_guardrails/guardrails_manifest.json): cập nhật SHA-256 manifest khớp 100% các guardrails vừa đồng bộ.
  - [`TRACEABILITY_MATRIX.md`](../../../docs/adr/TRACEABILITY_MATRIX.md): Gate 10 `sync_adr_matrix.py` cập nhật ma trận liên kết ADR (`0030`, `0033`, `0040`, `0041`, `0044`, `0045`) sau khi dọn 6 skill `scope: hub`.

## 2. Ma Trận Nghiệm Thu Kiểm Định (`PR #75`)

| Cổng Kiểm Định | Lệnh Thực Thi | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :---: |
| **TRIHT Pre & Post Cleanliness** | `check_release_cleanliness.py --phase pre/post --repo-root .` | Clean 100%, 100% Hermetic | ✅ **PASSED** |
| **Skills Governance GPI** | `validate_skills.py --enforce-gpi .agents/skills` | **77/77** `SKILL.md` đạt chuẩn tất cả CI Gates | ✅ **PASSED** |
| **Master Legal 15 CI Gates** | `python3 scripts/validate_legal_spoke.py` | **113/113** bundles, **15/15** Gates (`Errors: 0 \| Warnings: 0`) | ✅ **PASSED** |
| **Cleanliness & Guardrail Manifest** | `python3 scripts/_guardrails/check_spoke_cleanliness.py` | Script Budget 15/15, Guardrail Manifest khớp SHA-256 | ✅ **PASSED** |
| **Hub Import Depth** | `python3 scripts/_guardrails/check_hub_import_depth.py` | Quét **48** file(s), 0 vi phạm | ✅ **PASSED** |
| **Verify-Patch (ADR-0058)** | `python3 -m ccba_harness verify-patch -c ...` | **3/3** commands passed (`24644.2 ms`) | ✅ **PASSED** |
| **GitHub Actions CI & Copilot** | `gh pr checks 75` + `audit_pr_comments.py` | **6/6** CI Checks Passed, **0** Copilot comments | ✅ **PASSED** |

---

## Lịch Sử Trước Đó — PR #71, PR #72 & PR #73 — Hoàn Tất Issue #59 (`107 → 113` OKF v2.4 Bundles & Session Retrospective)

> **Mục tiêu:** Hoàn tất thu thập, chuẩn hóa OKF v2.4 Universal (ADR-0059) và đồng bộ Google Drive Vault cho toàn bộ 6 văn bản gốc thuộc **Issue #59** (`31/2026/TT-BXD`, `258/QĐ-TTg`, `93/2025/QH15`, `267/2025/NĐ-CP`, `268/2025/NĐ-CP`, `20/2026/TT-BKHCN`), đối soát nguyên văn `31/2026/TT-BXD` ↔ `QCVN 04`, và tổng kết tri thức cuối phiên (`RULE-1.7`, `RULE-4.6`, History `#57`).  
> **Trạng thái:** ✅ **MERGED VÀO MAIN (`Issue #59 CLOSED`, `113` văn bản)**  
> - **Spoke PR #71 (Micro-PR 2A):** [vvChu/ccba-legal-knowledge#71](https://github.com/vvChu/ccba-legal-knowledge/pull/71) — Merge Commit: `23eabba` (`6/6` CI Checks Passed)  
> - **Spoke PR #72 (Micro-PR 2B):** [vvChu/ccba-legal-knowledge#72](https://github.com/vvChu/ccba-legal-knowledge/pull/72) — Merge Commit: `6f4de09` (`6/6` CI Checks Passed, `Closes #59`)  
> - **Spoke PR #73 (Retrospective):** [vvChu/ccba-legal-knowledge#73](https://github.com/vvChu/ccba-legal-knowledge/pull/73) — Merge Commit: `c309a49` (`6/6` CI Checks Passed, `0` Copilot comments)  
> - **Issue liên quan:** [vvChu/ccba-legal-knowledge#59](https://github.com/vvChu/ccba-legal-knowledge/issues/59) (`CLOSED`, `labels: []`)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (`PR #71` – `PR #73`)

### A. Micro-PR 2A — Nạp `31/2026/TT-BXD`, `258/QĐ-TTg` & Đối Soát `QCVN 04` (`PR #71`)
- **Thông tư `31/2026/TT-BXD`** ([`thong_tu_31_2026_tt_bxd.md`](../../../legal_docs/01_vbpl/thong_tu_31_2026_tt_bxd/thong_tu_31_2026_tt_bxd.md)): Ban hành `--archetype VBPL_ADMIN` (`4` AST clauses, `status: pending_effective`, `effective_date: '2026-12-15'`, `relations.amends: ['QCVN-04-2021-BXD']`, `5/5` cross-links); đối soát nguyên văn với [`sua_doi_01_2026_qcvn_04_2021_bxd.md`](../../../legal_docs/02_qcvn/qcvn_04_2021_bxd/sources/sua_doi_01_2026_qcvn_04_2021_bxd.md) đạt `0.9784` khớp từ (7/7 nhóm sửa đổi khớp 100%); backfill `sha256` & `pdf_sha256` cho `SD1-2026-QCVN-04` tại [`qcvn_04_2021_bxd/metadata.yaml`](../../../legal_docs/02_qcvn/qcvn_04_2021_bxd/metadata.yaml) và liên kết tại [`qcvn_04_2021_bxd/index.md`](../../../legal_docs/02_qcvn/qcvn_04_2021_bxd/index.md).
  - DOCX (`15,359 B`): `c060c2cafe5201227391ef75635c7463ce5fd335a785eb9f80fb0a4586196ebc` | PDF (`536,097 B`, `14p`): `4863c9fa9cc07c9379c1e33c5c1b4981a4fea2de773cbe0edc96a6f65eb7055b`.
- **Quyết định `258/QĐ-TTg`** ([`quyet_dinh_258_qd_ttg_2023.md`](../../../legal_docs/01_vbpl/quyet_dinh_258_qd_ttg_2023/quyet_dinh_258_qd_ttg_2023.md)): Chuẩn hóa `--archetype VBPL_ADMIN` (`9` AST clauses, `status: active`, `effective_date: '2023-03-17'`, `5/5` cross-links).
  - DOCX (`10,052 B`): `c2e70d324c0eb1dab75ca2b1694e920270421aa2d8107264ee25c57e13ec0314` | PDF (`446,425 B`, `4p`): `e41d6a7f53322ac320a0aa5712ffe93378f9fd1a8f50adbeaaa9e677c53a49e8`.

### B. Micro-PR 2B — Cụm KH&CN: `93/2025/QH15`, `267/2025/NĐ-CP`, `268/2025/NĐ-CP` & `20/2026/TT-BKHCN` (`PR #72`)
- **Luật `93/2025/QH15`** ([`luat_93_2025_qh15.md`](../../../legal_docs/01_vbpl/luat_93_2025_qh15/luat_93_2025_qh15.md)): `409` AST clauses, `1` table (`bang_01.csv`), `enacted_by: [nghi_dinh_267_2025_nd_cp, nghi_dinh_268_2025_nd_cp]`, `replaces: [29/2013/QH13]`, `6/6` cross-links.
  - DOCX (`55,167 B`): `c54c348ab97c9b44e9da3177f36e8483534bc56b96109a3a67180eb8dbbf661a` | PDF (`2,671,283 B`, `52p`): `18e9ba52ff3a0eb6f43f20d723bb42a4cb95d2f91e1c02752b831ae055fdb2f9`.
- **Nghị định `267/2025/NĐ-CP`** ([`nghi_dinh_267_2025_nd_cp.md`](../../../legal_docs/01_vbpl/nghi_dinh_267_2025_nd_cp/nghi_dinh_267_2025_nd_cp.md)): `289` AST clauses, `enacts: [luat_93_2025_qh15]`, `replaces: [08/2014/NĐ-CP, 70/2018/NĐ-CP]`, `related_statutes: [thong_tu_20_2026_tt_bkhcn]`, cắt `Nơi nhận:` chuẩn Gate 6 (`line_end: 1791`), `5/5` cross-links.
  - DOCX (`44,814 B`): `8744720a4253c6c7c60f98edf97a2abc3141a1097d66f0ca78d5679f51364848` | PDF (`2,872,816 B`, `63p`): `cab99dad7ec00774636da92d862306c17b8726c3ef84395ca0d1c2f787cb32f4`.
- **Nghị định `268/2025/NĐ-CP`** ([`nghi_dinh_268_2025_nd_cp.md`](../../../legal_docs/01_vbpl/nghi_dinh_268_2025_nd_cp/nghi_dinh_268_2025_nd_cp.md)): `340` AST clauses, `1` table (`bang_01.csv`), `enacts: [luat_93_2025_qh15]`, `replaces: [13/2019/NĐ-CP]`, ghép PDF 293 trang (`677733.pdf`), cắt `Nơi nhận:` (`line_end: 2181`), `6/6` cross-links.
  - DOCX (`434,885 B`): `084d96e6389d6ee834dbe406686c55e723e1e206fc524f701aacdc3ecef7d13f` | PDF (`102,315,245 B`, `293p`): `28c8bc46044ff70c2e10fa33b6c0f93472288b03b16771b8f2b3ef6b997a1332`.
- **Thông tư `20/2026/TT-BKHCN`** ([`thong_tu_20_2026_tt_bkhcn.md`](../../../legal_docs/01_vbpl/thong_tu_20_2026_tt_bkhcn/thong_tu_20_2026_tt_bkhcn.md)): `62` AST clauses, `12` tables, `6` templates (`phu_luc_i` & `phu_luc_ii`), `amends: [36/2025/TT-BKHCN, 43/2025/TT-BKHCN, 01/2026/TT-BKHCN, 10/2026/TT-BKHCN]`, `related_statutes: [nghi_dinh_267_2025_nd_cp]`, chuẩn metadata & cắt `Nơi nhận:` (`line_end: 427`), `7/7` cross-links.
  - DOCX (`31,422 B`): `d5d66a279b57e6f58cee075352b0b30fe2e45fb17c16fce354fcf663a570d4ca` | PDF (`1,285,616 B`, `28p`): `e2c5d447f79de67f40573d40a59bedfb9983afc56ea9209938dc9fc18f9bcb2c`.
- **Cloud Vault (`macvnboy@gmail.com`):** Đẩy có phạm vi `--bundle` và xác minh đủ **`12/12`** tệp nguồn DOCX/PDF (`4` từ PR #71 + `8` từ PR #72) qua `rclone lsjson --stat --metadata`; đồng bộ [`legal_registry.yaml`](../../../legal_registry.yaml) lên **113 văn bản** (`01_vbpl: 59`, `02_qcvn: 17`, `03_tcvn: 34`, `04_appendices: 3`).

### C. Session Retrospective & ADR Traceability (`PR #73`)
- Cập nhật [`session_learnings.md`](../../../.md/knowledge/session_learnings.md) (`9.93 KB <= 10.0 KB`, giữ nguyên toàn bộ `32/32` `RULE-X.Y`, bổ sung **`RULE-1.7`** & **`RULE-4.6`**), ghi mục `#57` vào [`session_learnings_history.md`](../../../.md/knowledge/archive/session_learnings_history.md) và cập nhật [`log.md`](../../../.md/knowledge/log.md); đồng bộ ADR Matrix qua [`scripts/sync_adr_matrix.py`](../../../scripts/sync_adr_matrix.py) (`45` ADRs, `154` cross-references).

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix — Issue #59)

| Cổng Kiểm Định | Loại Kiểm Tra | Lệnh Thực Thi / Workflow | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :--- | :---: |
| **Master Legal CI Gates** | 15 Cổng Tri thức (Full) | `python3 scripts/validate_legal_spoke.py` | **113/113 bundles, 15/15 Gates (`Errors: 0 \| Warnings: 0`)** | ✅ **PASSED** |
| **Cross-Links & Anchors** | Liên kết 6 gói mới + QCVN 04 | `python3 scripts/verify_cross_links.py --bundle <slug>` | **TT31 `5/5`, QD258 `5/5`, L93 `6/6`, ND267 `5/5`, ND268 `6/6`, TT20 `7/7`, QCVN04 `18/18`** | ✅ **PASSED** |
| **Cleanliness & Budget** | Vệ sinh Spoke & Release | `check_spoke_cleanliness.py` + `check_release_cleanliness.py --phase post --repo-root .` | **15/15 scripts, 0 leaks, 100% Hermetic** | ✅ **PASSED** |
| **Hub Import Depth** | Kiến trúc Seam | `python3 scripts/_guardrails/check_hub_import_depth.py` | **48 files scanned, 0 violations** | ✅ **PASSED** |
| **Pstack Smoke & Verify-Patch** | Unit Tests + ADR-0058 | `verify_legal_harness.py --mode smoke --skip-pdf-vault` + `verify-patch` | **126 passed (`0.04s`) + `3/3` verify-patch PASSED (`24,987.4 ms`)** | ✅ **PASSED** |
| **Governance & Memory Gates** | Skills GPI / Wiki / Docs / 10 KB | `validate_skills.py`, `wiki_health_linter.py`, `compact_session_learnings.py`, `validate_docs.py` | **77 skills OK, `9.93 KB <= 10.0 KB`, Wiki/Docs PASSED** | ✅ **PASSED** |
| **Cloud Vault Owner Audit** | Toàn vẹn `CCBA_Legal_Vault` | `rclone lsjson <file> --stat --metadata` | **12/12 binaries verified (`owner: macvnboy@gmail.com`)** | ✅ **PASSED** |
| **Spoke GitHub Actions CI** | 6 Jobs / PR trên GitHub | `gh pr checks 71`, `gh pr checks 72`, `gh pr checks 73` | **6/6 Checks Passed trên cả PR #71, PR #72 và PR #73** | ✅ **PASSED** |
| **Copilot / Bugbot Audit** | AI Review Gate | `audit_pr_comments.py --pr 73` | **0 unresolved comments (Clean)** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

<details>
<summary>Nhấn để xem chi tiết PR #68 (Part of Issue #59 — Phát hành ngày 2026-11-23)</summary>

### Walkthrough: Phát Hành Tính Năng PR #68 (Đối Soát Hiệu Lực `QCVN 04` / `TT 31/2026`, `APPENDIX-SD-2026` & `NĐ 212/2026` — Part of Issue #59)

> **Mục tiêu:** Giải quyết triệt để mâu thuẫn hiệu lực `pending_effective` (`2026-12-15`) của Sửa đổi 01:2026 QCVN 04:2021/BXD (Thông tư `31/2026/TT-BXD`), nâng cấp Sub-Gate 5.3 ngăn chặn khai báo `active` cho văn bản/sửa đổi chưa đến ngày hiệu lực, đồng bộ lại cây điều khoản VBHN QCVN 04 (`161` clauses), viết lại chuẩn xác phụ lục `APPENDIX-SD-2026-QCVN-04` và đính chính metadata Nghị định `212/2026/NĐ-CP` theo nguyên văn DOCX gốc.  
> **Trạng thái:** ✅ **MERGED VÀO MAIN** *(Part of Issue #59)*  
> - **Spoke PR #68:** [vvChu/ccba-legal-knowledge#68](https://github.com/vvChu/ccba-legal-knowledge/pull/68) — Merge Commit: `2b69931` (Squash and merge, `6/6` CI Checks Passed)  
> - **Issue liên quan:** [vvChu/ccba-legal-knowledge#59](https://github.com/vvChu/ccba-legal-knowledge/issues/59)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (Spoke PR #68)

### A. Nâng Cấp Sub-Gate 5.3 & Integration Tests (`scripts/validate_legal_spoke.py`)
- Bổ sung `_normalize_lifecycle_bucket`, `_validate_amendments_future_dates`, và `_validate_future_effective_dates` tại [`scripts/validate_legal_spoke.py`](../../../scripts/validate_legal_spoke.py) để phân tách rạch ròi 3 nhóm `expired`, `pending_effective`, `active` (ADR-0050), cưỡng chế trạng thái `pending_effective` khi `effective_date > today` ở cả cấp văn bản lẫn `amendments[]` trong [`legal_registry.yaml`](../../../legal_registry.yaml) và `metadata.yaml`.
- Bổ sung 3 integration tests tại [`tests/integration/test_validate_legal_spoke.py`](../../../tests/integration/test_validate_legal_spoke.py) dùng mốc tương lai bất biến `"2099-12-31"`.

### B. Đồng Bộ `QCVN 04:2021/BXD`, `APPENDIX-SD-2026-QCVN-04` & Đính Chính `NĐ 212/2026/NĐ-CP`
- **Gói `qcvn_04_2021_bxd`:** Sửa [`patch_manifest.yaml`](../../../legal_docs/02_qcvn/qcvn_04_2021_bxd/patch_manifest.yaml) (gỡ câu tóm tắt tự chèn tại `muc-2-2-17`, bỏ lặp heading `2.2.17` và `4.3`), chạy lại `python -m ccba_legal consolidate` sinh đồng bộ [`qcvn_04_2021_bxd.md`](../../../legal_docs/02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md), [`clauses.json`](../../../legal_docs/02_qcvn/qcvn_04_2021_bxd/clauses.json) (`161` clauses), [`qa_benchmark.json`](../../../legal_docs/02_qcvn/qcvn_04_2021_bxd/qa_benchmark.json), [`bang_so_sanh_thay_doi.md`](../../../legal_docs/02_qcvn/qcvn_04_2021_bxd/bang_so_sanh_thay_doi.md); cập nhật [`metadata.yaml`](../../../legal_docs/02_qcvn/qcvn_04_2021_bxd/metadata.yaml), [`index.md`](../../../legal_docs/02_qcvn/qcvn_04_2021_bxd/index.md) phân tầng hiệu lực theo ADR-0013 và xóa `qcvn_04_2021_bxd.md.bak`.
- **Phụ lục `bang_so_sanh_sua_doi_2026`:** Chuyển `status: pending_effective` đồng bộ trong [`bang_so_sanh_sua_doi_2026.md`](../../../legal_docs/04_appendices/bang_so_sanh_sua_doi_2026/bang_so_sanh_sua_doi_2026.md), [`metadata.yaml`](../../../legal_docs/04_appendices/bang_so_sanh_sua_doi_2026/metadata.yaml) và [`legal_registry.yaml`](../../../legal_registry.yaml); viết lại bảng đối chiếu 7 nhóm khớp nguyên văn `sources/sua_doi_01_2026_qcvn_04_2021_bxd.md` và sửa `13/13` liên kết chéo.
- **Nghị định `212/2026/NĐ-CP`:** Đính chính `issued_date: '2026-06-17'` và `signer: Phạm Gia Túc` khớp DOCX gốc tại [`metadata.yaml`](../../../legal_docs/01_vbpl/nghi_dinh_212_2026_nd_cp/metadata.yaml), phần header [`nghi_dinh_212_2026_nd_cp.md`](../../../legal_docs/01_vbpl/nghi_dinh_212_2026_nd_cp/nghi_dinh_212_2026_nd_cp.md) và [`legal_registry.yaml`](../../../legal_registry.yaml); ghi nhận lỗi thư mời (`212/2026/NĐ-CP` không ban hành `10/01/2026`, khả năng nhầm từ `22/2026/NĐ-CP` ngày `16/01/2026`).

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Loại Kiểm Tra | Lệnh Thực Thi / Workflow | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :--- | :---: |
| **Integration Tests** | Sub-Gate 5.3 & Consolidator | `pytest tests/integration/test_validate_legal_spoke.py tests/integration/test_consolidator.py` | **27 passed in 0.06s** | ✅ **PASSED** |
| **Master Legal CI Gates** | 15 Cổng Tri thức | `python3 scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors, 0 Warnings)** | ✅ **PASSED** |
| **Cross-Links & Anchors** | Liên kết chéo | `python3 scripts/verify_cross_links.py --bundle qcvn_04_2021_bxd` + script kiểm tra `bang_so_sanh_sua_doi_2026.md` | **17/17 QCVN 04, 13/13 Appendix, 6/6 index OK** | ✅ **PASSED** |
| **Cleanliness & Budget** | Vệ sinh Spoke | `python3 scripts/_guardrails/check_spoke_cleanliness.py` | **15/15 scripts, 0 leaks** | ✅ **PASSED** |
| **Hub Import Depth** | Kiến trúc Seam | `python3 scripts/_guardrails/check_hub_import_depth.py` | **48 files scanned, 0 violations** | ✅ **PASSED** |
| **Pstack Smoke Harness** | Toàn trình TRIHT | `python3 .agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode smoke --skip-pdf-vault` | **126 unit tests + 15-Gate smoke PASSED** | ✅ **PASSED** |
| **Spoke GitHub Actions CI** | 6 Jobs trên GitHub | `gh pr checks 68` | **6/6 Checks Passed** | ✅ **PASSED** |
| **Copilot / Bugbot Audit** | AI Review Gate | `python3 ../ccba-agent-platform/scripts/validation/audit_pr_comments.py` | **0 unresolved comments (Clean)** | ✅ **PASSED** |

</details>

<details>
<summary>Nhấn để xem chi tiết PR #65 (Phát hành ngày 2026-11-22)</summary>

### Walkthrough: Phát Hành Tính Năng PR #65 (Đồng Bộ Cloud Vault `macvnboy@gmail.com` & Backfill `source_assets` 13 Bundles — Issue #64)

> **Mục tiêu:** Giải quyết dứt điểm bất đồng bộ Cloud Vault (`CCBA_Legal_Vault`), backfill metadata `source_assets` cho Nhóm 2 (`2` bundles) và Nhóm 3 (`9` bundles), khắc phục lệch SHA-256 `qcvn_02_2020_bca.docx`, ghi nhận ngoại lệ Google Drive `403 cannotDownloadAbusiveFile` cho `qcvn_13_2018_bxd.docx` và hoàn tất đẩy toàn bộ tệp nguồn hợp lệ lên tài khoản chuẩn `macvnboy@gmail.com`.  
> **Trạng thái:** ✅ **MERGED VÀO MAIN**  
> - **Spoke PR #65:** [vvChu/ccba-legal-knowledge#65](https://github.com/vvChu/ccba-legal-knowledge/pull/65) — Merge Commit: `a8b7d4f` (Squash and merge, `6/6` CI Checks Passed)  
> - **Issue liên quan:** [vvChu/ccba-legal-knowledge#64](https://github.com/vvChu/ccba-legal-knowledge/issues/64) (`CLOSED`)  
> - **Cloud Vault chuẩn:** `gdrive:CCBA_Legal_Vault` trên `macvnboy@gmail.com` (Folder ID `1MREnTZmEu74GtV9UTpVMf_4hYBdMDK4Z`)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (Spoke PR #65)

### A. Đồng Bộ Cloud Vault Trên Tài Khoản Thống Nhất (`macvnboy@gmail.com`)
- Kết nối lại `rclone gdrive:` trên máy Linux sang `macvnboy@gmail.com` khớp 1:1 với kho `CCBA_Legal_Vault` của máy Windows (`138` tệp verified trước đó, thiếu đúng `74` tệp Nhóm 1).
- Di dời tệp thử nghiệm lạc `test_vector.pdf` khỏi `legal_docs/01_vbpl/nghi_dinh_217_2026_nd_cp/sources/` sang `.md/scratch/` và tạm tách bản stub 1 trang `nghi_dinh_339_2026_nd_cp.pdf` (`968 bytes`, MuPDF) trong lúc `--push` để không đẩy tệp rác/stub giả lên Cloud Vault.
- Thực thi `python3 scripts/hydrate_sources_from_vault.py --push`: kiểm tra `245` tệp (`136` đã có sẵn, **`109` tải lên thành công**, `0` lỗi).

### B. Cập Nhật Metadata & Registry (`14` Tệp YAML — Strict Atomic Scope)
- **Nhóm 2 (`2` bundles — `metadata.yaml` + [`legal_registry.yaml`](../../../legal_registry.yaml)):**
  - `01_vbpl/10_2021_nd_cp`: Chuyển `source_assets.pdf.status` $\to$ `verified` (`4bfc3197...`) và bổ sung `source_assets.docx` (`verified`, `fe681f67...`).
  - `01_vbpl/nghi_dinh_339_2026_nd_cp`: Giữ `source_assets.pdf.status: pending_acquisition` (stub `968 bytes`) và bổ sung `source_assets.docx` (`verified`, `bd8568cc...`).
- **Nhóm 3 (`9` bundles — backfill `source_assets` `pdf` + `docx` vào `metadata.yaml` khớp `legal_registry.yaml`):**
  - `01_vbpl/14_vbhn_bgddt`, `01_vbpl/83_vbhn_tt_bxd`, `01_vbpl/quyet_dinh_1812_qd_bxd_2026`, `01_vbpl/thong_tu_02_2024_tt_bkhdt`, `01_vbpl/thong_tu_03_2024_tt_bkhdt`, `01_vbpl/thong_tu_08_2021_tt_bxd`, `01_vbpl/thong_tu_105_2025_tt_btc`, `03_tcvn/tcvn_5065_1990`, `03_tcvn/tcvn_8793_2011`.
- **Xử lý lệch SHA-256 & Ngoại lệ (`2` bundles — `metadata.yaml` + `legal_registry.yaml`):**
  - `02_qcvn/qcvn_02_2020_bca`: Cập nhật `sha256` & `source_assets.docx.sha256` sang `d21aeef240cdea2cd2b258ec828e82864035310242921f3e6f4e2c077073e2de`.
  - `02_qcvn/qcvn_13_2018_bxd`: Chuyển `source_assets.docx.status` $\to$ `pending_acquisition` do Google Drive chặn tải `403 cannotDownloadAbusiveFile` (chờ thu thập lại bản sạch từ TVPL).

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Loại Kiểm Tra | Lệnh Thực Thi / Workflow | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :--- | :---: |
| **Cloud Vault Parity** | Toàn vẹn Vault | `python3 scripts/hydrate_sources_from_vault.py --verify-only` | **232/232 verified, 0 missing, 0 mismatch** | ✅ **PASSED** |
| **Master Legal CI Gates** | 15 Cổng Tri thức | `python3 scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors, 0 Warnings)** | ✅ **PASSED** |
| **Cleanliness & Budget** | Vệ sinh Spoke | `python3 scripts/_guardrails/check_spoke_cleanliness.py` | **15/15 scripts, 0 leaks** | ✅ **PASSED** |
| **Hub Import Depth** | Kiến trúc Seam | `python3 scripts/_guardrails/check_hub_import_depth.py` | **48 files scanned, 0 violations** | ✅ **PASSED** |
| **Visual Parity Gate** | Trình bày Markdown | `python3 scripts/lint_visual_parity.py` | **1133 files scanned, 0 errors** | ✅ **PASSED** |
| **Unit Test Suite** | Kiểm thử đơn vị | `pytest tests/unit -q` | **126 passed in 0.04s** | ✅ **PASSED** |
| **Spoke GitHub Actions CI** | 6 Jobs trên GitHub | `gh pr checks 65` | **6/6 Checks Passed** | ✅ **PASSED** |
| **Copilot / Bugbot Audit** | AI Review Gate | `python3 ../ccba-agent-platform/scripts/validation/audit_pr_comments.py --pr 65` | **0 unresolved comments (Clean)** | ✅ **PASSED** |

</details>

<details>
<summary>Nhấn để xem chi tiết PR #47</summary>

### Walkthrough: Phát Hành Tính Năng PR #47 (Khắc Phục Toàn Trình Codebase Review, Gia Cố Pstack Verification Harnesses & Đồng Bộ 100% E2E Suite OKF v2.4)

> **Mục tiêu:** Giải quyết toàn bộ 20 phát hiện chặn từ đợt kiểm tra chéo song song `/ccba-code-review` (`Standards` + `Spec`) và 5 điều kiện nghiệm thu từ Grok 4.7; gia cố 2 bộ kiểm tra vệ sinh Spoke (`check_spoke_cleanliness.py`, `check_hub_import_depth.py`), 3 Pstack Verification Harnesses (bảo vệ tiến trình con bằng `Popen(..., start_new_session=True)` + `os.killpg` chống treo pipe), các cổng kiểm định OKF v2.4 (`validate_legal_spoke.py`, `verify_cross_links.py`), và đồng bộ 100% bộ kiểm thử `tests/e2e/` (`428 passed, 4 skipped, 0 failed`).
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **Spoke PR #47:** [vvChu/ccba-legal-knowledge#47](https://github.com/vvChu/ccba-legal-knowledge/pull/47) — Merge Commit: `b5b832d` (Squash and merge, 6/6 CI Checks Passed)
> - **Biên bản Thẩm định Grok 4.7:** Round 1 (`APPROVE_WITH_CONDITIONS`, Session `7b7b9a49-b881-4134-9ef2-d4884d782213`) & Round 2 (`FINAL_ACCEPT`, Risk: 1/5, 0 Blocking Conditions, Session `6e2ea3db-d153-4502-b98d-4f92501976d7`).

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (Spoke PR #47)

### A. Gia Cố Spoke Guardrails & Pstack Verification Harnesses
- Cập nhật `scripts/_guardrails/check_spoke_cleanliness.py` (mẫu Regex `MACHINE_PATH_RE` theo ADR-0061, sắp xếp tất định `sorted()` trên mọi phép duyệt thư mục) và `scripts/_guardrails/check_hub_import_depth.py` (quét toàn bộ dải dòng AST `[lineno..end_lineno]` để nhận diện `# ccba:quarantine` và `# ccba:allow-deep-import` trên câu lệnh import nhiều dòng).
- Chuyển đổi `run_cmd` trong 3 Pstack Verification Harnesses (`verify_legal_harness.py`, `verify_legal_intel_harness.py`, `verify_legal_ingest_harness.py`) từ `subprocess.run` sang `subprocess.Popen(..., start_new_session=True)` kèm `os.killpg(..., signal.SIGKILL)` khi `TimeoutExpired`, khử triệt để lỗi treo pipe khi tiến trình con sinh tiến trình cháu giữ mở `stdout`/`stderr`.

### B. Chuẩn Hóa Tất Định & Cổng Kiểm Định OKF v2.4 (`scripts/` & `.md/tools/`)
- Áp dụng **Filesystem Inode Ordering Invariance** (`sorted(...)`) và **Multi-Key Deterministic Sorting** (`-round(score, 4)`) cùng xử lý ngoại lệ tường minh (không dùng bare `except Exception: pass`) trên 14 kịch bản kiểm định trong `scripts/` và `.md/tools/verify_ground_truth_parity.py`.
- Nâng cấp `scripts/validate_legal_spoke.py` (Gate 2 bắt lỗi liên kết hỏng tới tài liệu cấu thành, Gate 8 quét đệ quy `rglob("*.md")`, Gate 12 kiểm tra đồng bộ $1:1$ thẻ thị giác `figures/cards/*.md` và cấm tệp `.wmf`/`.emf` đóng kín) và `scripts/verify_cross_links.py` (bóc tách đầy đủ cú pháp `[label](href)` kèm `urllib.parse.unquote`).

### C. Đồng Bộ 100% Bộ Kiểm Thử `tests/` Với Kiến Trúc OKF v2.4
- Cập nhật `tests/conftest.py` và 4 tệp kiểm thử trong `tests/e2e/` (`test_tier1_feature_coverage.py`, `test_tier2_boundaries.py`, `test_tier3_cross_features.py`, `test_tier4_real_world.py`) để phản ánh cấu trúc VBHN hợp nhất của `qcvn_06_2022_bxd`, phụ lục tách rời `annexes/*.md` (ADR 0036) và bảng dữ liệu 2D tách chú thích (ADR 0041), nâng tỷ lệ vượt qua toàn bộ pytest suite lên **100% (`428 passed, 4 skipped, 0 failed`)**.

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Loại Kiểm Tra | Lệnh Thực Thi / Workflow | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :--- | :---: |
| **Maskara Secret Gate** | Bảo mật mã nguồn | `python -m ccba_maskara.cli scan --staged` / CI | **0 secret leaks** | ✅ **PASSED** |
| **Cleanliness & Budget** | Vệ sinh Spoke | `python scripts/_guardrails/check_spoke_cleanliness.py` | **15/15 scripts, 0 leaks** | ✅ **PASSED** |
| **Hub Import Depth** | Kiến trúc Seam | `python scripts/_guardrails/check_hub_import_depth.py` | **44 files scanned, 0 violations** | ✅ **PASSED** |
| **Full Pytest Suite** | Unit + Integration + E2E | `python -m pytest tests/unit/ tests/integration/ tests/e2e/ -q` | **428 passed, 4 skipped, 0 failed** | ✅ **PASSED** |
| **Master Legal CI Gates**| 15 Cổng Tri thức | `python scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors)** | ✅ **PASSED** |
| **Spoke GitHub Actions CI**| 6 Jobs trên GitHub | `gh pr checks 47` | **6/6 Checks Passed** | ✅ **PASSED** |
| **Copilot / Bugbot Audit**| AI Review Gate | `python ../ccba-agent-platform/scripts/validation/audit_pr_comments.py --pr 47` | **0 unresolved comments (Clean)** | ✅ **PASSED** |

</details>

<details>
<summary>Nhấn để xem chi tiết PR #44 & Hub PR #607 (Phát hành ngày 2026-11-05)</summary>

### PR #44 & Hub PR #607: Gia Cố Toàn Trình Pipeline `/ccba-legal-ingest`, Đồng Bộ Sổ Bộ 106 Bundles & Khóa Cổng Liên Kết Gate 2
- **T-01:** Đồng bộ khối `decrees:` (19 văn bản) và mở rộng Sub-Gate 5.3 lên **106/106 bundles**.
- **T-02:** Chuẩn hóa sinh `index.md` / `metadata.yaml` và bổ sung `_validate_index_md_links` trong Gate 2.
- **T-03:** Hợp nhất điểm vào ingest một cửa, hỗ trợ ADR 0043 Dual-PDF fallback và trích xuất DOCX header hints offline.
- **T-04:** Chuẩn hóa Nightly Telemetry và làm mới hàng đợi Provenance 106 bundles.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #40 (Phát hành ngày 2026-10-21)</summary>

### PR #40: Nạp Quyết Định 1812/QĐ-BXD 2026 Từ Điển Dữ Liệu Quốc Gia Về Hoạt Động Xây Dựng v1.0 & Đồng Bộ Spoke Guardrails
- **Tài liệu nguồn xác thực SHA-256 (`sources/`)**:
  - `quyet_dinh_1812_qd_bxd_2026.docx`: `35,186 bytes` (`d6e7c7d3fdd25a187fe66eeddfaf843741dc8054e575b0a0718652ed1f6a2e19`)
  - `quyet_dinh_1812_qd_bxd_2026.pdf`: `921,231 bytes`, 38 trang (`db769ac3c9f7795152aa7f8989b71974e9e2e18ef5afe0a87b8737a77627942e`)
- **Cấu trúc Bundle `legal_docs/01_vbpl/quyet_dinh_1812_qd_bxd_2026/`**:
  - Văn bản quy phạm nguyên văn `quyet_dinh_1812_qd_bxd_2026.md` (2,875 dòng, Verbatim Parity 100%).
  - Bảng từ điển dữ liệu 2D `tables/csv/bang_01.csv` & `tables/json/bang_01.json` (176 hàng dữ liệu x 9 cột, Zero Ragged Rows).
  - Cây điều khoản `clauses.json`, `qa_benchmark.json`, `metadata.yaml` và đăng ký vào `legal_registry.yaml` (liên kết `guided_by`: `nghi_dinh_212_2026_nd_cp`, `thong_tu_39_2026_tt_bxd`).
- **Đồng Bộ Layer-1 Constitution & Hiện Đại Hóa CI Matrix**:
  - Đồng bộ `.agents/AGENTS.md` từ Hub `ccba-agent-platform` và di chuyển bộ kiểm chuẩn về `scripts/_guardrails/`.
  - Cập nhật `scripts/spoke_cli.py` loại bỏ các trường sandbox tạm thời (`docx_path`, `pdf_path`, `attachments`, `links`) khi nạp `metadata_handoff.json`.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #37 (Phát hành ngày 2026-10-12)</summary>

### PR #37: Mạng Tri Thức Pháp Lý 5 Vành Đai Luật Xây Dựng 2025 & Suy Diễn Ngược Hai Chiều Trên RAM
- **Ontology 5 vành đai** kết nối Luật Xây dựng 2025 (`135/2025/QH15`) với 7 Nghị định thi hành, Nghị định xử phạt `339/2026/NĐ-CP`, 6 QCVN cốt lõi và phân cấp địa phương.
- **Động cơ suy diễn ngược 2 chiều trên RAM** (`build_bidirectional_legal_graph`) và Sub-Gate 5.4 / Sub-Gate 2.1.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #32 (Phát hành ngày 2026-10-06)</summary>

### PR #32: Triển Khai Pstack Verification Harness, Features Map & Hiện Đại Hóa Ma Trận 6 CI Gates
- **Kiến trúc Pstack 5 khối độc lập**: Clean-Slate Pre-flight, Dual-Mode Lifecycle, Deterministic Health Barrier, Evidence-Capture Suite, Guaranteed Cleanup ($300.0\text{ s}$ timeout).
- **Lập Bản Đồ 9 Tính Năng Quy Phạm**: Trong `features/INDEX.md` kèm quy tắc COND-01 chống gian lận dữ liệu.
- **Tái cấu trúc Ma trận CI 6 cổng song song**: Phân rã 1 job nguyên khối thành 5 cổng song song kèm Master Aggregator Gate khớp $1:1$ GitHub Ruleset `#23696513`.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #30 (Phát hành ngày 2026-10-05)</summary>

### PR #30: Số Hóa 6 Tiêu Chuẩn PCCC & Đường Đất Yếu, Cài Đặt Maskara Guardrail, Spoke Đạt 96 Bundles
- **Số hóa toàn diện 6 tiêu chuẩn**: `QCVN 02:2020/BCA`, `TCVN 13456:2022`, `TCVN 6379:2024`, `TCVN 7568-14:2025`, `TCCS 41:2022/TCĐBVN`, `TCCS 39:2022/TCĐBVN`.
- **Cài đặt Client-Side Guardrail**: Cài đặt `.githooks/pre-commit` kích hoạt `ccba-maskara` trước mỗi commit.
- **Đồng bộ Tri-Tier Cloud Vault**: 18 tệp nhị phân nguồn lên Google Drive Vault `gdrive:CCBA_Legal_Vault`.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #21 (Phát hành ngày 2026-10-03)</summary>

### PR #21: Đồng Bộ Cloud RAG NotebookLM & Ưu Tiên 6 Văn Bản Đấu Thầu 2024–2026 Vào Living Roadmap
- **Khắc phục lỗi xác thực Playwright (`notebooklm-py`)**: Truy vết và hotfix lỗi race condition / premature commit tại `browser_capture.py`.
- **Thực thi đồng bộ 65 nguồn văn bản quy phạm**: Tải mới 37 nguồn tri thức vào sổ tay `CCBA_Legal_Knowledge_Base_2026`.
- **Nghiên cứu thể chế & bổ sung 6 văn bản đấu thầu**: NĐ 349/2026, Luật 57/2024, NĐ 225/2025, TT 05/2024, TT 105/2025, TT 03/2024.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #19 (Phát hành ngày 2026-10-03)</summary>

### PR #19: Nạp 2 Văn Bản Luật Tier 1 (Luật Nhà Ở 2023 & Luật Đất Đai 2024)
- **Luật Nhà ở 2023 (`27/2023/QH15`)**: 978 AST clauses, 1 bảng dữ liệu, 978 QA pairs.
- **Luật Đất đai 2024 (`31/2024/QH15`)**: 1,500 AST clauses, 2 bảng dữ liệu, 1,500 QA pairs.
- **Sổ bộ Pháp lý (`legal_registry.yaml`)**: Nâng từ 70 lên 72 văn bản pháp quy.
- **Google Drive Vault (`CCBA_Legal_Vault`)**: Tải lên và xác thực 100% SHA-256 cho 4 tệp DOCX/PDF gốc.

</details>
