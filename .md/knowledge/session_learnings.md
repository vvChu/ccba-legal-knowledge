# 🧠 CCBA Legal Knowledge Spoke: Active Architectural Invariants

> **Phạm vi:** Spoke (`ccba-legal-knowledge`) | **Chuẩn:** OKF v2.4 (ADR 0021-0066)
> **Lịch sử 56 Bài Học:** [session_learnings_history.md](archive/session_learnings_history.md) | Trần: $\le 10\text{ KB}$

---

## Miền 1. 🌐 Thu Thập & Nguồn Gốc Pháp Lý

- **RULE-1.1 [TVPL VIP 3-Tier — ADR 0031, 0035]**: *Tier 1 (`part=-100`)*: Vector PDF (zero-OCR). *Tier 2 (`part=-1&docx=1`)*: Word (`docx_converter.py`). *Tier 3 (`part=0`)*: Gazette Scan PDF.
- **RULE-1.2 [`tab=7` & Chromium VIP — ADR 0031]**: CDP port `9222` (`~/.gemini/antigravity/chrome_vip`); tải DOCX/PDF qua `tab=7` & API TVPL.
- **RULE-1.3 [Dual-PDF & Vault — ADR 0043]**: Scan $\to$ `sources/<slug>_raw_scan.pdf`; Vector PDF Word COM $\to$ `sources/<slug>.pdf` (`pdf_origin: docx_vector_rendered`, `metadata.yaml`), sync `CCBA_Legal_Vault`.
- **RULE-1.4 [POSIX Path — ADR 0035, 0036]**: `legal_registry.yaml`, `metadata.yaml` dùng `/`, cấm `\`; `spoke_cli.py ingest` `.replace("\\", "/")`; Gate 1, 2 chặn `\`.
- **RULE-1.5 [3 Khóa & Re-Ingest — PR #44, Hub #607]**: `spoke_cli.py`, `validate_legal_spoke.py` (Sub-Gate 5.3), `verify_all_docs_against_pdf.py` quét `("laws", "decrees", "standards")` & đếm 4 khu `registry_summary` theo `/{cat}/` ở `bundle_path`. Re-ingest giữ `status` (`expired`, `superseded`), `expiration_date`, `relations`, `pdf_origin`, `raw_scan_pdf` nếu payload mặc định (`active`/`effective`); cấm bịa `"Chính phủ"`, `"Thủ tướng Chính phủ"`/ngày mặc định.
- **RULE-1.6 [Vault Owner, Stub & Abuse 403 — ADR 0035, PR #65]**: Kiểm chủ `gdrive:CCBA_Legal_Vault` qua `rclone lsjson <file> --stat --metadata` (tránh Split-Brain & đệ quy treo; dùng `rclone config create gdrive drive scope=drive #` khi dính `drive~`). `VaultHydrationEngine.push_sources()` đẩy mọi `.pdf`/`.docx` ở `sources/` kể cả `pending_acquisition` $\to$ cô lập stub/file lạc trước `--push`. Gặp `403 cannotDownloadAbusiveFile`: cấm `--drive-acknowledge-abuse` ngầm; hỏi user & set `status: pending_acquisition` ở `metadata.yaml` + `legal_registry.yaml`.

---

## Miền 2. 📐 Đa Phương Thức & Toán Học KaTeX

- **RULE-2.1 [MTEF & WMF/EMF — ADR 0040]**: Bóc 100% MathType (MTEF v3/v5) OLE $\to$ KaTeX (4-Tier Hybrid Formula Fallback, zero-OCR); WMF/EMF $\to$ Dual-Format (SVG, PNG $\ge 300\text{ DPI}$), cấm `.wmf`/`.emf`.
- **RULE-2.2 [KaTeX Đa Dòng — ADR 0038, 0044]**: `aligned`/`cases`/`gather` dùng `\qquad (X)` cuối dòng thay `\tag{...}`; giữ `\left[`/`\right]`; tách `<!-- FIGURE: ... -->` khỏi `$$`.
- **RULE-2.3 [Chú Thích Sơ Đồ — ADR 0039]**: Giữ 100% `CHÚ THÍCH`/`CHÚ DẪN` giữa ảnh & tiêu đề; Vertical Stack lề $\ge 40\text{ px}$; qua Sub-Gate 11.2.

---

## Miền 3. 📊 Bảng Biểu 2D & Biểu Mẫu Nguyên Tử

- **RULE-3.1 [Lưới 2D & Forward-Fill — ADR 0041]**: Lưới 2D `tblGrid`, Hierarchical Forward-Fill (`vMerge` CSV/JSON), phẳng header Em-dash (`Tầng 1 — Tầng 2`), Zero Ragged Rows.
- **RULE-3.2 [Footnotes & Biểu Mẫu — ADR 0021, 0041]**: Tách 100% `footnotes`; thoát `|` cell & KaTeX (`\vert `); đẩy biểu mẫu sang `templates/` (cấm rỗng).
- **RULE-3.3 [Bảng Đa Phần — ADR 0044]**: Văn bản đa phần (QCVN 07) gắn tiền tố (`bang_p01_01.csv`) & `part_id` ở `tables_catalog.json`.
- **RULE-3.4 [Biểu Mẫu Đệ Quy — ADR 0021, 0028, 0036]**: Cho phép thư mục con (`templates/phu_luc_iv/*.md`); `spoke_cli.py`, `sync_notebooklm_knowledge.py`, `validate_legal_spoke.py` quét đệ quy (`glob("**/templates/**/*.md")` / `rglob("*.md")`).

---

## Miền 4. 🏛️ OpenXML DOM & Nguyên Văn Quy Phạm

- **RULE-4.1 [DocxCanonicalSanitizer — ADR 0042]**: Gọt `w:rsid*`, `w:proofErr`, gộp run đồng nhất, NFC, tiêm `xml:space="preserve"`, tách borderless layout tables qua Multi-Factor Scoring ($\ge 30\%$ số), giữ `<w:object>`, `<m:oMath>`, `<w:drawing>`.
- **RULE-4.2 [Nguyên Văn 100% — ADR 0037, ADR 0059]**: CẤM tóm tắt/diễn đạt thân quy phạm; trích 1:1 DOCX, Gate 11 Verbatim Parity $\ge 98.0\%$.
- **RULE-4.3 [Gạch Đầu Dòng — ADR 0029, 0030]**: Giữ 100% `-`, `+` qua `\- `, `&nbsp;&nbsp;\+ `; qua `lint_visual_parity.py`.
- **RULE-4.4 [Ground Truth Bilateral — ADR 0045]**: Đối xứng DOCX/PDF (`check_multi_span_coverage`); lọc `in_signatory`, `in_bibliography`; hỗ trợ `verification_scope.normative_body_pages` (`metadata.yaml`).
- **RULE-4.5 [Gate 11 VBHN Delta — ADR 0037, PR #50]**: `is_vbhn_consolidation`: `missing_paras` đối soát (`6-word sliding window` NFC) qua `sources/*_goc*.md`; khớp $\ge 98.0\%$ (`GATE_11_MIN_VERBATIM_PARITY`) $\to$ `goc_verified = True` (`0 Warnings`).

---

## Miền 5. 🛡️ CI 15 Cổng & Hiệu Lực Pháp Lý

- **RULE-5.1 [Hiệu Lực 01/07/2026]**: **Luật XD 2025** (`135/2025/QH15`), **NĐ 217/2026/NĐ-CP** (175/2024, 15/2021), **NĐ 207/2026/NĐ-CP** (06/2021), **NĐ 206/2026/NĐ-CP** (10/2021).
- **RULE-5.2 [15 Cổng Master CI — ADR 0058]**: `python scripts/validate_legal_spoke.py`: 0 Errors/Warnings, Visual Parity, Verbatim, Valid Links, PDF SHA-256, SVG/Cards, 2D Regularity, KaTeX, OKF Provenance.
- **RULE-5.3 [Machine-State Decoupling]**: CẤM commit path tuyệt đối vào `workspace_context.yaml`; cô lập Hub qua `CCBA_HUB_PATH`.
- **RULE-5.4 [Umbrella Aggregator — ADR 0058, 0066]**: Job `legal-knowledge-audit` (`"Deterministic Parity & Schema Audit"`) `needs: [...]`, `if: always()` khớp Ruleset.
- **RULE-5.5 [Monorepo Install & Pip Cache]**: Cài Hub `git+https://github.com/vvChu/ccba-agent-platform.git#subdirectory=packages/<pkg>`; cấm `cache: 'pip'` nếu thiếu `requirements.txt`/`pyproject.toml`.
- **RULE-5.6 [Pstack 5-Block & Script Budget — ADR 0009, 0044, 0066]**: Harness 5 khối `.agents/skills/<skill>/harness/`, trần $15/15$ `scripts/`.
- **RULE-5.7 [Liên Kết `index.md` (Gate 2) — ADR 0035, PR #44]**: `_validate_index_md_links` cấm `Path.exists()` trên `.pdf`/`.docx`/`./sources/`; đối chiếu `./sources/` với `metadata.yaml`, chỉ `Path.exists()` với `.md`/`.json`/`.yaml`, `./templates/`, `./tables/`, `./figures/`, `./annexes/`.
- **RULE-5.8 [Chống Treo Pipe Pstack — PR #47]**: `verify_legal*_harness.py`: cấm `subprocess.run(..., capture_output=True)` với `start_new_session=True`; dùng `subprocess.Popen` & `os.killpg(os.getpgid(proc.pid), signal.SIGKILL)` (hay `taskkill /F /T /PID`) ở `except subprocess.TimeoutExpired:` trước `proc.communicate()`.
- **RULE-5.9 [AST Span, Path Máy & Inode — ADR 0061, PR #47]**: `check_hub_import_depth.py` quét `[node.lineno, end_lineno]` (`# ccba:quarantine`/`# ccba:allow-deep-import`); `check_spoke_cleanliness.py` dùng `MACHINE_PATH_RE` bắt `r"C:\..."`, YAML không ngoặc; `Path.glob`/`rglob`/`iterdir` bọc `sorted(...)`, sort `-round(score, 4)` (cấm `reverse=True`).
- **RULE-5.10 [Release Cleanliness & Gate 10 SSOT — PR #65–#66]**: Hub `check_release_cleanliness.py` ở Spoke phải truyền `--repo-root .` (mặc định trỏ Hub). Gate 10 (`validate_legal_spoke.py`) tự ghi `docs/adr/TRACEABILITY_MATRIX.md` qua `scripts/sync_adr_matrix.py` (cấm `sync_hub_adr_matrix.py` ở Spoke này) & chuẩn dòng trống `session_learnings.md` $\to$ kiểm diff ở Cổng 0.2/0.3.

---

## Miền 6. 🧭 Đồ Thị Ngữ Cảnh & Định Danh Thể Chế

- **RULE-6.1 [Danh Xưng & `LEGACY_NATURAL_KEY_ALIASES` — PR #52–#53, Hub #671, Spark #182, IDOP #117/#120, VvC_Notes #107]**:
  - Khử lặp (`I=Institute`, `C=Center`): cấm `"Viện IBST"`, `"Viện (IBST)"`, `"Viện trưởng IBST"`, `"Trung tâm CCBA"`, `"Viện/IBST"`, `"CCBA/TT BIM"`; dùng `"Viện"`, `"IBST"`, `"Viện KHCN Xây dựng (IBST)"`, `"đơn vị thành viên thuộc IBST"` (Quy tắc 4), `"14 Viện/Trung tâm chuyên ngành thuộc IBST"`, `"CCBA"`, `"Trung tâm"`, `"IBST - CCBA"`.
  - **`LEGACY_NATURAL_KEY_ALIASES` Fail-Closed Rebind**: Đổi chuỗi hiển thị kiêm `key_field` SharePoint (`Submissions`, `ApprovalNodes`, `ProjectMembers`, `EmployeeHistory`, `ApprovalDelegations`, `ApprovalWorkflows`): cấm prefix trần (`"[Gate 1]"` — tránh `PATCH` đè hồ sơ sống); dùng `(list_name, key_field, legacy_exact_string)`, fail-closed khi 2 khóa tồn tại, `existing_map.pop(legacy_key, None)` + rebind `existing_map[new_key] = item_id` (Bước 5 $\to$ 6 $\to$ 7).
- **RULE-6.2 [4-Slice UCG, `C-DRIFT-CONTRACT` v1.1 & 3 Rào Chắn — PR #51, Hub #665, Spark #177–#181, IDOP #112–#113, VvC_Notes #105–#106]**:
  - **`C-DRIFT-CONTRACT` v1.1**: Nối `5-Ring Legal Graph` (`ccba-legal-knowledge`, `QĐ 1812/QĐ-BXD`) với `:InternalRegulation`/`:InternalClause` (`QCTK 2815`, `QCCTNB 3209`, `neo4j-graph`) qua `:DERIVED_FROM_STATUTE` (cấm sửa ngầm). Producer (`index_idop_kb.py`) xuất `governance_drift_report.json` (`contract_version: "1.1"`, `clause_id`, `drift_status: "STATUTE_SUPERSEDED"`, `superseded_statutes[]`, `replacement_statutes[]` tách `guided_by[]`, `impacted_metrics[]`, `authority_signoff_role`, `source_path`, `content_hash`) trên 4 file `.md/governance_constitution/`; Consumer (`load_governance_drift_report_items`) kiểm `is_contract_valid` & chặn `PROPOSE_GOVERNANCE_AMENDMENT` nếu thiếu `impacted_metrics`/`authority_signoff_role`.
  - **3 Rào Chắn Đối Kháng**: (1) `allocation_share` + `OVER_ALLOCATED_SHARE` giữ `495.127.049.993 VNĐ` chống fan-out `331,71 tỷ VNĐ`; (2) Tách `Ghost WIP` (`confidence >= 0.95`, không `AMBIGUOUS`) khỏi `Real WIP` theo Gate, Pareto L10 xếp `real_wip_vnd` mọi `ContractScope` (`#S1..#Sn`); (3) `Metric #7` qua `iso_week_bounds_ict(period_key)`, khóa Chủ trì nếu chứng chỉ `EXPIRED`/lỗi ngày.
  - **Semantic Cache & Hot-Reload**: Cô lập khóa Redis theo `ctx.corpus` (`SearchPipeline`), giữ 1-hop (`hop`, `graph_neighbors`, `via_source`, `edge_type`, `tags`), dùng vector `tuple[(path, mtime), ...]` thay `max(mtimes)` khi hot-reload JSON/NPZ.
