# 🧠 CCBA Legal Knowledge Spoke: Active Architectural Invariants (Compacted Working Memory)

> **Phạm vi:** Spoke Tri thức Pháp lý (`ccba-legal-knowledge`) | **Chuẩn:** OKF v2.4 (ADR 0021-0066)
> **Chi tiết Lịch sử 55 Bài Học:** [session_learnings_history.md](archive/session_learnings_history.md) | Ngân sách: $\le 10\text{ KB}$

---

## Miền 1. 🌐 Thu Thập & Xác Thực Nguồn Gốc Pháp Lý

- **RULE-1.1 [TVPL VIP 3-Tier Download Priority — ADR 0031 & ADR 0035]**:
  - *Tier 1 (`part=-100`)*: VIP Digital Vector PDF (zero-OCR). *Tier 2 (`part=-1&docx=1`)*: VIP OpenXML Word (`docx_converter.py`). *Tier 3 (`part=0`)*: Gazette Scan PDF dự phòng.
- **RULE-1.2 [Giao Thức Một Cửa `tab=7` & Chromium VIP Session — ADR 0031]**:
  - Dùng Chromium CDP cổng `9222` profile `~/.gemini/antigravity/chrome_vip`; tải DOCX/PDF qua `tab=7` và API TVPL.
- **RULE-1.3 [Lưu Trữ Song Song Dual-PDF & Vault Drive — ADR 0043]**:
  - Scan mờ lưu `sources/<slug>_raw_scan.pdf`; Vector PDF từ Word COM lưu `sources/<slug>.pdf` kèm `pdf_origin: docx_vector_rendered` trong `metadata.yaml`, đồng bộ `CCBA_Legal_Vault`.
- **RULE-1.4 [Chuẩn Hóa Đường Dẫn POSIX Toàn Cầu — ADR 0035 & ADR 0036]**:
  - 100% đường dẫn trong `legal_registry.yaml` & `metadata.yaml` dùng `/`, cấm `\`. `spoke_cli.py ingest` chuẩn hóa `.replace("\\", "/")`; Gate 1 & 2 chặn `\`.
- **RULE-1.5 [Quét Hợp Nhất 3 Khóa Sổ Bộ & Bảo Toàn Hiệu Lực Re-Ingest — PR #44 & Hub PR #607]**:
  - Công cụ đọc/ghi `legal_registry.yaml` (`spoke_cli.py`, `validate_legal_spoke.py` Sub-Gate 5.3, `verify_all_docs_against_pdf.py`) quét hợp nhất `("laws", "decrees", "standards")` và đếm 4 phân khu trong `registry_summary` theo `/{cat}/` trong `bundle_path`.
  - Khi re-ingest văn bản đã tồn tại, bảo toàn `status` (`expired`, `superseded`), `expiration_date`, `relations`, `pdf_origin`, `raw_scan_pdf` khi payload mới chỉ mang mặc định (`active`/`effective`); cấm bịa `"Chính phủ"`, `"Thủ tướng Chính phủ"` hay ngày mặc định.

---

## Miền 2. 📐 Bóc Tách Đa Phương Thức & Chuẩn Hóa Toán Học KaTeX

- **RULE-2.1 [Bóc Tách Xác Định MTEF MathType & Khử Tệp Đóng Kín — ADR 0040]**:
  - Bóc tách 100% MathType nhị phân (MTEF v3/v5) từ OLE stream sang KaTeX (4-Tier Hybrid Formula Fallback Engine, zero-OCR). Vector WMF/EMF chuyển sang Dual-Format (SVG & PNG $\ge 300\text{ DPI}$); cấm lưu `.wmf`/`.emf` đóng kín.
- **RULE-2.2 [Cú Pháp Toán Học KaTeX Đa Dòng & Bảo Toàn Dấu — ADR 0038 & ADR 0044]**:
  - Trong môi trường đa dòng (`aligned`, `cases`, `gather`), dùng `\qquad (X)` cuối dòng thay `\tag{...}`; bảo tồn `\left[` / `\right]`; tách `<!-- FIGURE: ... -->` khỏi khối `$$`.
- **RULE-2.3 [Bảo Tồn Chú Thích Kẹp Giữa Sơ Đồ Đồ Họa — ADR 0039]**:
  - Bảo tồn 100% `CHÚ THÍCH` / `CHÚ DẪN` kẹp giữa ảnh và tiêu đề hình; xếp dọc đa tầng (Vertical Stack) lề $\ge 40\text{ px}$; vượt qua Sub-Gate 11.2 Zero-Dropped Regulatory Notes.

---

## Miền 3. 📊 Cấu Trúc Bảng Biểu 2D & Mẫu Biểu Nguyên Tử

- **RULE-3.1 [Lưới Tọa Độ Ảo 2D & Forward-Fill Có Kiểm Soát — ADR 0041]**:
  - Dựng lưới 2D từ `tblGrid`, Hierarchical Forward-Fill có kiểm soát cho `vMerge` trong CSV/JSON, phẳng hóa tiêu đề đa tầng bằng Em-dash (`Tầng 1 — Tầng 2`), đạt 100% Zero Ragged Rows.
- **RULE-3.2 [Tách Rời Chú Thích Bảng & Định Tuyến Biểu Mẫu — ADR 0021 & ADR 0041]**:
  - Bóc tách 100% `footnotes` khỏi ma trận dữ liệu; thoát `|` trong cell và KaTeX (`\vert `); định tuyến biểu mẫu hành chính sang `templates/`, cấm để `templates/` rỗng.
- **RULE-3.3 [Định Danh Bảng Quy Chuẩn Đa Phần — ADR 0044]**:
  - Văn bản nhiều phần (QCVN 07) mang tiền tố mã phần (`bang_p01_01.csv`) và khai báo `part_id` trong `tables_catalog.json`.
- **RULE-3.4 [Thu Thập & Đếm Biểu Mẫu Hành Chính Đệ Quy — ADR 0021, ADR 0028 & ADR 0036]**:
  - Cho phép thư mục con phụ lục (`templates/phu_luc_iv/*.md`); mọi công cụ (`spoke_cli.py`, `sync_notebooklm_knowledge.py`, `validate_legal_spoke.py`) quét đệ quy (`glob("**/templates/**/*.md")` hoặc `rglob("*.md")`).

---

## Miền 4. 🏛️ Chuẩn Hóa OpenXML DOM & Bảo Tồn Nguyên Văn Quy Phạm

- **RULE-4.1 [Tiền Xử Lý In-Memory DocxCanonicalSanitizer — ADR 0042]**:
  - Gọt `w:rsid*`, `w:proofErr`, gộp run đồng nhất, chuẩn hóa NFC, tiêm `xml:space="preserve"`, giải nén borderless layout tables qua Multi-Factor Scoring (mật độ số liệu $\ge 30\%$), bảo tồn `<w:object>`, `<m:oMath>`, `<w:drawing>`.
- **RULE-4.2 [Bảo Tồn Nguyên Văn Quy Phạm 100% — ADR 0037 & ADR 0059]**:
  - CẤM tóm tắt hay diễn đạt lại thân quy phạm; trích xuất 1:1 từ DOCX và đạt Gate 11 Verbatim Parity $\ge 98.0\%$.
- **RULE-4.3 [Bảo Tồn Ký Tự Gốc & Thoát Ký Tự Gạch Đầu Dòng — ADR 0029 & ADR 0030]**:
  - Bảo tồn 100% dấu `-` và `+` bằng `\- ` và `&nbsp;&nbsp;\+ `; vượt qua `lint_visual_parity.py`.
- **RULE-4.4 [Ground Truth Engine Bilateral Symmetry & Scope Partitioning — ADR 0045]**:
  - Đồng bộ đối xứng nhánh DOCX & PDF qua Block Multi-span Coverage (`check_multi_span_coverage`); lọc ký duyệt (`in_signatory`) & tài liệu tham khảo (`in_bibliography`); hỗ trợ `verification_scope.normative_body_pages` trong `metadata.yaml`.
- **RULE-4.5 [Gate 11 VBHN Bilateral Delta Verification — ADR 0037 & PR #50]**:
  - Với bundle VBHN (`is_vbhn_consolidation`), các đoạn DOCX gốc bị sửa/bãi bỏ (`missing_paras`) được đối soát bù trừ (`6-word sliding window` NFC) với `sources/*_goc*.md`; nếu tỷ lệ khớp kết hợp $\ge 98.0\%$ (`GATE_11_MIN_VERBATIM_PARITY`) thì xác nhận `goc_verified = True` (`0 Warnings`).

---

## Miền 5. 🛡️ Hệ Thống Kiểm Định CI 15 Cổng & Hiệu Lực Pháp Lý Tuyệt Đối

- **RULE-5.1 [Rào Chắn Hiệu Lực Pháp Lý Tuyệt Đối — Từ 01/07/2026]**:
  - Văn bản viện dẫn ĐANG CÓ HIỆU LỰC: **Luật Xây dựng 2025** (`135/2025/QH15`), **NĐ 217/2026/NĐ-CP** (thay NĐ 175/2024 & 15/2021), **NĐ 207/2026/NĐ-CP** (thay NĐ 06/2021), **NĐ 206/2026/NĐ-CP** (thay NĐ 10/2021).
- **RULE-5.2 [15 Cổng Kiểm Định Nghiệm Thu Master CI Gate — ADR 0058]**:
  - Chạy `python scripts/validate_legal_spoke.py`: 0 Errors, 0 Warnings, 100% Visual Parity, Verbatim Match, Valid Links, PDF SHA-256, SVG/Cards, 2D Regularity, KaTeX Math, OKF Provenance.
- **RULE-5.3 [Single-User Multi-Device & Machine-State Decoupling]**:
  - CẤM commit đường dẫn tuyệt đối vào `workspace_context.yaml`; cô lập đường dẫn Hub qua `CCBA_HUB_PATH`.
- **RULE-5.4 [Umbrella Master Aggregator Gate & Ruleset Alignment — ADR 0058 & ADR 0066]**:
  - Duy trì job `legal-knowledge-audit` (`"Deterministic Parity & Schema Audit"`) với `needs: [...]` và `if: always()` khớp 1:1 GitHub Ruleset.
- **RULE-5.5 [Git Monorepo Subdirectory Install & Pip Cache Fallback trong CI]**:
  - Cài package từ Hub qua `git+https://github.com/vvChu/ccba-agent-platform.git#subdirectory=packages/<pkg>`; cấm `cache: 'pip'` khi gốc repo không có `requirements.txt`/`pyproject.toml`.
- **RULE-5.6 [Pstack 5-Block Verification Harness & Script Budget — ADR 0009, ADR 0044, ADR 0066]**:
  - Harness tuân thủ 5 khối Pstack trong `.agents/skills/<skill>/harness/`, bảo vệ trần $15/15$ scripts tại `scripts/`.
- **RULE-5.7 [Kiểm Định Liên Kết `index.md` An Toàn `.gitignore` Trên CI (Gate 2) — ADR 0035 & PR #44]**:
  - Trong `_validate_index_md_links`, cấm gọi `Path.exists()` trên `.pdf`/`.docx` hoặc `./sources/`; kiểm tra tiền tố `./sources/` khớp `metadata.yaml` và chỉ gọi `Path.exists()` cho `.md`/`.json`/`.yaml` và ngăn kéo Git (`./templates/`, `./tables/`, `./figures/`, `./annexes/`).
- **RULE-5.8 [Chống Treo Pipe Tiến Trình Con Trong Pstack Harnesses — PR #47]**:
  - Cấm `subprocess.run(..., capture_output=True)` khi bật `start_new_session=True`; dùng `subprocess.Popen` và gọi `os.killpg(os.getpgid(proc.pid), signal.SIGKILL)` (hoặc `taskkill /F /T /PID`) trong `except subprocess.TimeoutExpired:` trước `proc.communicate()`.
- **RULE-5.9 [Dải Dòng AST, Quét Đường Dẫn Máy & Bất Biến Thứ Tự Inode — ADR 0061 & PR #47]**:
  - `check_hub_import_depth.py` quét `[node.lineno, end_lineno]`; `check_spoke_cleanliness.py` dùng `MACHINE_PATH_RE` bắt cả `r"C:\..."` và đường dẫn YAML không ngoặc kép; mọi `Path.glob`/`rglob`/`iterdir` bọc `sorted(...)` và sort đa tiêu chí bằng `-round(score, 4)`.

---

## Miền 6. 🧭 Đồ Thị Ngữ Cảnh Hợp Nhất & Định Danh Thể Chế

- **RULE-6.1 [Chuẩn Hóa Danh Xưng Pháp Nhân `IBST` / `Viện` / `Viện KHCN Xây dựng (IBST)` — PR #52]**:
  - Cấm lặp từ loại + chữ đầu viết tắt (`I=Institute`, `C=Center`) hoặc ghép `/`: cấm viết `"Viện IBST"`, `"Trung tâm CCBA"`, `"Viện/IBST"`, `"CCBA/TT BIM"`; dùng chuẩn `"IBST"`, `"Viện"`, `"Viện KHCN Xây dựng (IBST)"`, `"14 Viện/Trung tâm chuyên ngành thuộc IBST"`, `"CCBA"`, `"Trung tâm"`, `"IBST - CCBA"`.
- **RULE-6.2 [Kiến Trúc 4-Slice CCBA Unified Context Graph & Interface Contract 1 v1.1 — PR #51]**:
  - Nối `5-Ring Legal Graph` (`ccba-legal-knowledge` + `QĐ 1812/QĐ-BXD`) với `:InternalRegulation` / `:InternalClause` (`QCTK 2815`, `QCCTNB 3209` trên `neo4j-graph`) qua `:DERIVED_FROM_STATUTE`; gắn cờ `drift_status: "STATUTE_SUPERSEDED"` và xuất `governance_drift_report.json` (`Interface Contract 1 v1.1`) mà không tự sửa ngầm văn bản nội bộ.


