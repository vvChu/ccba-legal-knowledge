# 🧠 CCBA Legal Knowledge Spoke: Active Architectural Invariants

> **Phạm vi:** Spoke (`ccba-legal-knowledge`) | **Chuẩn:** OKF v2.4 (ADR 0021-0066)
> **Lịch sử 55 Bài Học:** [session_learnings_history.md](archive/session_learnings_history.md) | Ngân sách: $\le 10\text{ KB}$

---

## Miền 1. 🌐 Thu Thập & Nguồn Gốc Pháp Lý

- **RULE-1.1 [TVPL VIP 3-Tier — ADR 0031, ADR 0035]**: *Tier 1 (`part=-100`)*: Vector PDF (zero-OCR). *Tier 2 (`part=-1&docx=1`)*: OpenXML Word (`docx_converter.py`). *Tier 3 (`part=0`)*: Gazette Scan PDF.
- **RULE-1.2 [`tab=7` & Chromium VIP — ADR 0031]**: CDP cổng `9222` profile `~/.gemini/antigravity/chrome_vip`; tải DOCX/PDF qua `tab=7` & API TVPL.
- **RULE-1.3 [Dual-PDF & Vault — ADR 0043]**: Scan mờ $\to$ `sources/<slug>_raw_scan.pdf`; Vector PDF Word COM $\to$ `sources/<slug>.pdf` kèm `pdf_origin: docx_vector_rendered` trong `metadata.yaml`, đồng bộ `CCBA_Legal_Vault`.
- **RULE-1.4 [POSIX Path — ADR 0035, ADR 0036]**: Đường dẫn `legal_registry.yaml` & `metadata.yaml` dùng `/`, cấm `\`; `spoke_cli.py ingest` `.replace("\\", "/")`; Gate 1 & 2 chặn `\`.
- **RULE-1.5 [3 Khóa Sổ Bộ & Re-Ingest — PR #44, Hub #607]**: `spoke_cli.py`, `validate_legal_spoke.py` (Sub-Gate 5.3), `verify_all_docs_against_pdf.py` quét `("laws", "decrees", "standards")` & đếm 4 phân khu `registry_summary` theo `/{cat}/` trong `bundle_path`. Khi re-ingest, giữ `status` (`expired`, `superseded`), `expiration_date`, `relations`, `pdf_origin`, `raw_scan_pdf` nếu payload mới chỉ mang mặc định (`active`/`effective`); cấm bịa `"Chính phủ"`, `"Thủ tướng Chính phủ"` hay ngày mặc định.

---

## Miền 2. 📐 Đa Phương Thức & Toán Học KaTeX

- **RULE-2.1 [MTEF MathType & WMF/EMF — ADR 0040]**: Bóc tách 100% MathType (MTEF v3/v5) từ OLE sang KaTeX (4-Tier Hybrid Formula Fallback, zero-OCR); WMF/EMF $\to$ Dual-Format (SVG & PNG $\ge 300\text{ DPI}$), cấm lưu `.wmf`/`.emf`.
- **RULE-2.2 [KaTeX Đa Dòng — ADR 0038, ADR 0044]**: Trong `aligned`, `cases`, `gather`, dùng `\qquad (X)` cuối dòng thay `\tag{...}`; giữ `\left[`/`\right]`; tách `<!-- FIGURE: ... -->` khỏi `$$`.
- **RULE-2.3 [Chú Thích Sơ Đồ — ADR 0039]**: Giữ 100% `CHÚ THÍCH`/`CHÚ DẪN` kẹp giữa ảnh & tiêu đề hình; xếp dọc (Vertical Stack) lề $\ge 40\text{ px}$; vượt Sub-Gate 11.2.

---

## Miền 3. 📊 Bảng Biểu 2D & Mẫu Biểu Nguyên Tử

- **RULE-3.1 [Lưới 2D & Forward-Fill — ADR 0041]**: Dựng lưới 2D từ `tblGrid`, Hierarchical Forward-Fill cho `vMerge` trong CSV/JSON, phẳng hóa tiêu đề bằng Em-dash (`Tầng 1 — Tầng 2`), 100% Zero Ragged Rows.
- **RULE-3.2 [Chú Thích Bảng & Biểu Mẫu — ADR 0021, ADR 0041]**: Tách 100% `footnotes` khỏi ma trận; thoát `|` trong cell & KaTeX (`\vert `); định tuyến sang `templates/` (cấm rỗng).
- **RULE-3.3 [Bảng Đa Phần — ADR 0044]**: Văn bản nhiều phần (QCVN 07) mang tiền tố phần (`bang_p01_01.csv`) & `part_id` trong `tables_catalog.json`.
- **RULE-3.4 [Đếm Biểu Mẫu Đệ Quy — ADR 0021, ADR 0028, ADR 0036]**: Cho phép thư mục con (`templates/phu_luc_iv/*.md`); `spoke_cli.py`, `sync_notebooklm_knowledge.py`, `validate_legal_spoke.py` quét đệ quy (`glob("**/templates/**/*.md")` / `rglob("*.md")`).

---

## Miền 4. 🏛️ OpenXML DOM & Nguyên Văn Quy Phạm

- **RULE-4.1 [DocxCanonicalSanitizer — ADR 0042]**: Gọt `w:rsid*`, `w:proofErr`, gộp run đồng nhất, chuẩn hóa NFC, tiêm `xml:space="preserve"`, giải nén borderless layout tables qua Multi-Factor Scoring (mật độ số liệu $\ge 30\%$), giữ `<w:object>`, `<m:oMath>`, `<w:drawing>`.
- **RULE-4.2 [Nguyên Văn 100% — ADR 0037, ADR 0059]**: CẤM tóm tắt/diễn đạt lại thân quy phạm; trích xuất 1:1 từ DOCX & đạt Gate 11 Verbatim Parity $\ge 98.0\%$.
- **RULE-4.3 [Gạch Đầu Dòng — ADR 0029, ADR 0030]**: Bảo tồn 100% `-` và `+` bằng `\- ` và `&nbsp;&nbsp;\+ `; vượt `lint_visual_parity.py`.
- **RULE-4.4 [Ground Truth Bilateral — ADR 0045]**: Đối xứng DOCX & PDF qua `check_multi_span_coverage`; lọc `in_signatory` & `in_bibliography`; hỗ trợ `verification_scope.normative_body_pages` trong `metadata.yaml`.
- **RULE-4.5 [Gate 11 VBHN Bilateral Delta — ADR 0037, PR #50]**: Với bundle VBHN (`is_vbhn_consolidation`), các đoạn DOCX gốc bị sửa/bãi bỏ (`missing_paras`) đối soát bù trừ (`6-word sliding window` NFC) với `sources/*_goc*.md`; đạt kết hợp $\ge 98.0\%$ (`GATE_11_MIN_VERBATIM_PARITY`) $\to$ `goc_verified = True` (`0 Warnings`).

---

## Miền 5. 🛡️ CI 15 Cổng & Hiệu Lực Pháp Lý

- **RULE-5.1 [Hiệu Lực Từ 01/07/2026]**: Văn bản HIỆU LỰC: **Luật Xây dựng 2025** (`135/2025/QH15`), **NĐ 217/2026/NĐ-CP** (thay 175/2024 & 15/2021), **NĐ 207/2026/NĐ-CP** (thay 06/2021), **NĐ 206/2026/NĐ-CP** (thay 10/2021).
- **RULE-5.2 [15 Cổng Master CI — ADR 0058]**: `python scripts/validate_legal_spoke.py`: 0 Errors, 0 Warnings, 100% Visual Parity, Verbatim Match, Valid Links, PDF SHA-256, SVG/Cards, 2D Regularity, KaTeX Math, OKF Provenance.
- **RULE-5.3 [Machine-State Decoupling]**: CẤM commit đường dẫn tuyệt đối vào `workspace_context.yaml`; cô lập Hub qua `CCBA_HUB_PATH`.
- **RULE-5.4 [Umbrella Aggregator — ADR 0058, ADR 0066]**: Job `legal-knowledge-audit` (`"Deterministic Parity & Schema Audit"`) với `needs: [...]` & `if: always()` khớp 1:1 GitHub Ruleset.
- **RULE-5.5 [Monorepo Install & Pip Cache]**: Cài package Hub qua `git+https://github.com/vvChu/ccba-agent-platform.git#subdirectory=packages/<pkg>`; cấm `cache: 'pip'` khi gốc repo thiếu `requirements.txt`/`pyproject.toml`.
- **RULE-5.6 [Pstack 5-Block & Script Budget — ADR 0009, ADR 0044, ADR 0066]**: Harness 5 khối tại `.agents/skills/<skill>/harness/`, trần $15/15$ `scripts/`.
- **RULE-5.7 [Liên Kết `index.md` (Gate 2) — ADR 0035, PR #44]**: Trong `_validate_index_md_links`, cấm `Path.exists()` trên `.pdf`/`.docx` hoặc `./sources/`; kiểm tra `./sources/` khớp `metadata.yaml` & chỉ gọi `Path.exists()` cho `.md`/`.json`/`.yaml` và `./templates/`, `./tables/`, `./figures/`, `./annexes/`.
- **RULE-5.8 [Chống Treo Pipe Pstack — PR #47]**: Cấm `subprocess.run(..., capture_output=True)` khi `start_new_session=True`; dùng `subprocess.Popen` & gọi `os.killpg(os.getpgid(proc.pid), signal.SIGKILL)` (hoặc `taskkill /F /T /PID`) trong `except subprocess.TimeoutExpired:` trước `proc.communicate()`.
- **RULE-5.9 [AST Span, Đường Dẫn Máy & Inode — ADR 0061, PR #47]**: `check_hub_import_depth.py` quét `[node.lineno, end_lineno]`; `check_spoke_cleanliness.py` dùng `MACHINE_PATH_RE` bắt `r"C:\..."` & YAML không ngoặc kép; mọi `Path.glob`/`rglob`/`iterdir` bọc `sorted(...)` & sort bằng `-round(score, 4)`.

---

## Miền 6. 🧭 Đồ Thị Ngữ Cảnh Hợp Nhất & Định Danh Thể Chế

- **RULE-6.1 [Danh Xưng Pháp Nhân & `LEGACY_NATURAL_KEY_ALIASES` Fail-Closed Rebind — PR #52–#53, Hub #671, Spark #182, IDOP #117/#120, VvC_Notes #107]**:
  - Cấm lặp từ loại + chữ đầu viết tắt (`I=Institute`, `C=Center`) hoặc ghép `/`: loại bỏ `"Viện IBST"`, `"Viện (IBST)"`, `"Viện trưởng IBST"`, `"Trung tâm CCBA"`, `"Viện/IBST"`, `"CCBA/TT BIM"`; chuẩn hóa thành `"Viện"`, `"IBST"`, `"Viện KHCN Xây dựng (IBST)"`, `"đơn vị thành viên thuộc IBST"` (Quy tắc 4), `"14 Viện/Trung tâm chuyên ngành thuộc IBST"`, `"CCBA"`, `"Trung tâm"`, `"IBST - CCBA"`.
  - **`LEGACY_NATURAL_KEY_ALIASES` Fail-Closed Rebind**: Khi đổi chuỗi hiển thị đồng thời là `key_field` trên SharePoint List, cấm khớp tiền tố trần (`"[Gate 1]"` — nguy cơ `PATCH` đè hồ sơ đấu thầu đang sống); dùng bảng ánh xạ nguyên văn `(list_name, key_field, legacy_exact_string)`, kiểm tra fail-closed khi cả khóa cũ & mới cùng tồn tại, và gọi `existing_map.pop(legacy_key, None)` kèm rebind `existing_map[new_key] = item_id` xuyên suốt Bước 5 $\to$ 6 $\to$ 7.
- **RULE-6.2 [4-Slice CCBA Unified Context Graph, `C-DRIFT-CONTRACT` v1.1 & 3 Rào Chắn Dữ Liệu Đối Kháng — PR #51, Hub #665, Spark #177–#181, IDOP #112–#113, VvC_Notes #105–#106]**:
  - **Interface Contract 1 v1.1 (`C-DRIFT-CONTRACT`)**: Nối `5-Ring Legal Graph` (`ccba-legal-knowledge` + `QĐ 1812/QĐ-BXD`) với `:InternalRegulation`/`:InternalClause` (`QCTK 2815`, `QCCTNB 3209` trên `neo4j-graph`) qua `:DERIVED_FROM_STATUTE` (không tự sửa ngầm quy chế). Producer (`index_idop_kb.py`) xuất `governance_drift_report.json` (`contract_version: "1.1"`, `clause_id`, `drift_status: "STATUTE_SUPERSEDED"`, `superseded_statutes[]`, `replacement_statutes[]` tách khỏi `guided_by[]`, `impacted_metrics[]`, `authority_signoff_role`, `source_path`, `content_hash`) trên đủ 4 văn bản `.md/governance_constitution/`; Consumer (`load_governance_drift_report_items`) kiểm tra `is_contract_valid` & từ chối thẻ `PROPOSE_GOVERNANCE_AMENDMENT` khi thiếu `impacted_metrics` hoặc `authority_signoff_role`.
  - **3 Rào Chắn Dữ Liệu Đối Kháng**: (1) Trọng số `allocation_share` + guard `OVER_ALLOCATED_SHARE` bảo toàn `495.127.049.993 VNĐ` chống nhân bản fan-out `331,71 tỷ VNĐ`; (2) Tách `Ghost WIP` (chỉ khấu trừ khi `confidence >= 0.95` & không chứa `AMBIGUOUS`) khỏi `Real WIP` theo Gate, xếp hạng Pareto L10 theo `real_wip_vnd` trên mọi `ContractScope` (`#S1..#Sn`); (3) Tính `Metric #7` theo tuần ISO `iso_week_bounds_ict(period_key)` & khóa phân công Chủ trì khi có chứng chỉ `EXPIRED` hoặc lỗi ngày hiệu lực.
  - **Semantic Cache Isolation & Multi-Asset Hot-Reload**: Cô lập khóa Redis semantic cache theo `ctx.corpus` trong `SearchPipeline`, giữ trường 1-hop (`hop`, `graph_neighbors`, `via_source`, `edge_type`, `tags`), và theo dõi vector `tuple[(path, mtime), ...]` thay `max(mtimes)` đơn lẻ chống mù thay đổi khi hot-reload nhiều file JSON/NPZ.
