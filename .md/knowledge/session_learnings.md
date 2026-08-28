# 🧠 CCBA Platform Knowledge Base: Session Learnings & Architectural Invariants

> **Scope:** Hub (`ccba-agent-platform`) & Spokes (`ccba-legal-knowledge`, etc.)
> **Standard:** OKF v2.3 Dual-Engine, ADR 0016, ADR 0021, ADR 0030, ADR 0031, ADR 0032, ADR 0034.

---

## 1. TVPL VIP 3-Tier Download Priority & Parameter Discovery (ADR 0031)

- **Tier 1 — VIP Digital Vector Searchable PDF (`part=-100` / `#ctl00_Content_ThongTinVB_filePDFHyperLink`):**
  - **Mỏ neo Pháp lý Tối thượng Cấp 1 (Primary Anchor of Trust)**: Bản PDF số hóa toàn văn (ví dụ QCVN 02 619 trang, QCVN 06 182 trang, TT 38 1,893 trang). Chứa trọn vẹn 100% thân văn bản, toàn bộ phụ lục, bảng biểu và đồ thị.
- **Tier 2 — VIP OpenXML Word Document (`part=-1&docx=1` / `#ctl00_Content_ThongTinVB_vietnameseHyperLink_Docx`):**
  - **Nguồn Dữ Liệu Gốc Vàng (Gold Source Input)**: Nạp trực tiếp vào `docx_converter.py` để sinh ra OKF v2.2/v2.3 Markdown Bundle (phân rã biểu mẫu `templates/` và bảng tra cứu `tables/`).
- **Tier 3 — Gazette Scan PDF (`part=0` / `#ctl00_Content_ThongTinVB_pdfHyperLink`):**
  - Dự phòng khi TVPL chưa xuất bản bản PDF số hóa riêng.

---

## 2. Persistent Chromium VIP Session Engine & CLI (`python -m ccba_legal login`)

- **Profile Độc Lập:** Sử dụng `~/.gemini/antigravity/chrome_vip` để lưu Cookie phiên VIP Pro lâu dài.
- **Khởi chạy 1-Click:** Lệnh `python -m ccba_legal login` tự động mở Chrome/Edge trên cổng `9222`, cho phép đăng nhập 1 lần duy nhất, tránh bị Windows DPAPI chặn khi copy file cookie.
- **WebSocket Timeout Guard:** Bổ sung `timeout=8.0s` và bắt lỗi `(WebSocketTimeoutException, WebSocketConnectionClosedException)` trong `evaluate_js` và `navigate`, chống đơ luồng khi form ASP.NET PostBack/Reload.

---

## 3. Automated Contract Tests: CLI & Documentation Parity

- **`test_cli_doc_parity.py`:** Kiểm tra tự động tính khớp nối $100\%$ giữa các lệnh trong `cli.py` (`login`, `fetch`, `batch-fetch`, `convert`, `consolidate`, `process`) và hướng dẫn trong `SKILL.md`. Ngăn ngừa triệt để lỗi lệch pha tài liệu (Documentation Drift).

---

## 4. Spoke CI Gates Verification Pipeline (10 Master CI Gates)

Mọi văn bản trước khi nghiệm thu vào kho tri thức bắt buộc phải vượt qua tuần tự 10 cổng kiểm định không dung thứ (Zero-Tolerance) qua `python scripts/validate_legal_spoke.py`:
1. `Gate 1: Registry Integrity Check`
2. `Gate 2: OKF Bundles Structure Check`
3. `Gate 3: Table Attachments Check`
4. `Gate 4: Fake Data Gate Check`
5. `Gate 5: PDF Metadata & AST Jurisdiction Gate Check`
6. `Gate 6: Pure Normative Body & Scoped Noise Gate Check`
7. `Gate 7: Spoke Cleanliness & Zero-Wrapper Gate`
8. `Gate 8: Template & Table Structural Integrity Gate`
9. `Gate 9: Visual Parity & Footnote Monotonic Linter Gate`
10. `Gate 10: ADR Living Traceability & Self-Healing Sync`

---

## 5. Spoke `.md` Directory Hygiene & Archiving Structure (ADR 0033)

- **Cấp gốc `.\.md\`**: Chỉ chứa các file cấu hình và mỏ neo tri thức tối thượng (`workspace_context.yaml`, `codebase_architecture_analysis.md`).
- **Thư mục con chuyên biệt**:
  - `.\.md\extracted_docs\`: Lưu trữ toàn bộ file Word (`.docx`) và PDF Công báo gốc đã nạp.
  - `.\.md\knowledge\`: Lưu trữ tri thức cốt lõi (`session_learnings.md`, architectural patterns).
  - `.\.md\archive\`: Nơi lưu trữ tất cả các script thử nghiệm, kiểm toán lịch sử và khảo sát (`audits/`, `inspections/`, `legacy_harvesters/`).
  - `.\.md\backups\`: Lưu trữ các bản sao lưu config (`.bak_*`).
  - `.\.md\data\`: Lưu trữ session locks, caches và audit logs.

---

## 6. Mathematical Formula & Engineering Table Ingestion Governance (ADR 0020, ADR 0030)

### 6.1. Nhận Diện Bẫy Layout Bảng Ẩn (Formula in Table Alignment Layout):
- **Hiện tượng:** Văn bản Word TCVN/QCVN thường dùng bảng ẩn $1 \times 2$ borderless để căn trái công thức và căn phải số thứ tự `(1)`, `(2)`, `(3)`.
- **Quy tắc xử lý:** Tuyệt đối không xuất các bảng này thành file CSV/JSON rác trong `tables/`. Bộ chuyển đổi phải tự động phát hiện mẫu `(N)` và chuyển đổi thành khối công thức KaTeX có đánh số `\tag{N}`.

### 6.2. Quy Tắc Đối Chiếu Chéo 3 Bên Ký Hiệu Toán Học (Triangulation of Variables):
- **Hiện tượng:** Các ký tự Hy Lạp có dấu gạch ngang đầu (`\bar{\varepsilon}`, `\bar{\alpha}`, `\bar{b}`) rất dễ bị OCR hoặc LLM nhận diện nhầm.
- **Quy tắc xử lý:** Bắt buộc đối chiếu đồng thời 3 vị trí:
  1. Biểu thức toán học chính (Equation).
  2. Đoạn văn giải thích biến số (*"trong đó:..."*).
  3. Bảng số liệu tra cứu hệ số (ví dụ: Bảng 10 với các cột $\bar{\varepsilon}, \bar{b}, \bar{\alpha}$).

### 6.3. Kỷ Luật Trình Bày Khối Display Math KaTeX:
- Cặp dấu `$$` mở và đóng bắt buộc phải nằm trên **dòng riêng biệt hoàn toàn**, không kẹp dính comment `<!-- formula_id -->` cùng dòng để tránh lỗi render `\tag works only in display equations` và lỗi Visual Clipping.

### 6.4. Chuẩn Hóa Biến Số Trong Phần Văn Bản Giải Thích:
- $100\%$ các biến số ($c_r, z_s, h, g_Q, g_v, g_R, n_1, \beta, \gamma_f, \psi_L, \varphi_1 \dots$) trong phần giải thích *"trong đó:"* bắt buộc phải bọc trong `$ ... $`.

### 6.5. Máy Trạng Thái Thụt Lề Chú Giải Công Thức (Formula Scope State Machine - ADR 0030):
- **Cơ chế kích hoạt:** Tự động bắt đầu khi gặp trigger dẫn nhập: `trong đó:`, `với:`, `ở đây:`, `ký hiệu trong công thức:`.
- **Thụt lề an toàn trong Markdown:** Sử dụng tiền tố `&nbsp;&nbsp;&nbsp;&nbsp;` (4 khoảng trắng không ngắt dòng) cho từng dòng giải thích biến số để tránh bẫy CommonMark Indented Code Block.
- **Phân cấp thụt lề cấp 2:** Sử dụng `&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;` cho các mục con phân cấp của một biến số (ví dụ: các mức giá trị của độ cản $\beta$).

### 6.6. Quy Chuẩn Hiển Thị Đơn Vị Đo Có Số Mũ (Unit Super-Scripter Invariant - ADR 0030):
- **Hiện tượng:** Văn bản Word thường xuất các đơn vị đo dạng phẳng (`m2`, `m3`, `daN/m2`, `kg/m3`, `kN/m2`) làm giảm chất lượng thị giác so với PDF gốc.
- **Quy tắc xử lý:** Tự động chuyển đổi $100\%$ các đơn vị đo có số mũ thành định dạng LaTeX chuẩn: `$\text{m}^2$`, `$\text{m}^3$`, `$\text{daN/m}^2$`, `$\text{kg/m}^3$`, `$\text{kN/m}^2$`.
- **Phép so sánh diện tích:** Chuẩn hóa các biểu thức toán học điều kiện: `$A > A_1 = 9\text{ m}^2$`, `$A > A_2 = 36\text{ m}^2$`.

---

## 7. Universal Layout Traps & Anti-Patterns Governance Matrix (ADR 0020-0033)

| Bẫy Layout / Anti-Pattern | Bản Chất Vấn Đề | Giải Pháp Khái Quát Hóa | ADR / CI Gate Thực Thi |
| :--- | :--- | :--- | :--- |
| **1. Indented Code Block Trap** | Thụt lề 4 spaces thô biến điều khoản thành khối mã lệnh `<pre><code>`. | Strip spaces thô + Thụt lề an toàn bằng `&nbsp;&nbsp;&nbsp;&nbsp;` qua State Machine. | ADR 0029, ADR 0030 |
| **2. Lazy List Collapse** | Đoạn văn/Heading sau danh sách bị nuốt vào bullet nếu thiếu dòng trống. | Bắt buộc chèn dòng trống (`\n\n`) trước mọi Heading/Công thức/Bảng sau list. | Gate 9 (`lint_visual_parity`) |
| **3. Italics vs Math Subscript** | Dấu `_` trong biến số (`W_0`, `T_1`) bị hiểu là in nghiêng làm vỡ text. | Tự động bọc biến số có chỉ số dưới vào `$ ... $` (`$W_0$`, `$T_1$`). | KaTeX Vision Harvester |
| **4. Embedded Table Footnotes** | Dòng chú thích gộp ô ở đáy bảng làm bẩn kiểu dữ liệu cột trong CSV. | Tự động cắt hàng `CHÚ THÍCH:` ra khỏi CSV, đưa xuống Markdown `_CHÚ THÍCH:_`. | Gate 3 (`Table Attachments`) |
| **5. Flattened Form Tables** | Bảng biểu mẫu hành chính 1 cột bị duỗi thẳng thành text rời rạc. | Tách Atomic Form Templates vào `templates/phu_luc_XX/mau_YY.md`. | ADR 0021 (Gate 8) |
| **6. Mega Document Overflow** | Văn bản khổng lồ (QCVN 02 619 trang) làm tràn Context Window LLM. | Phân rã Modular Appendices trong `appendices/` + Bảng Điều Hướng 2D. | ADR 0030 |
| **7. Line Patching Drift** | Sửa đổi văn bản bằng số dòng cố định dễ bị lệch khi văn bản thay đổi. | Hợp nhất văn bản dựa trên Semantic Anchor ID bất biến (`#muc-1-4-24`). | ADR 0022 (VBHNEngine) |
| **8. Flat Unit Exponents** | Đơn vị đo dính số mũ phẳng (`m2`, `daN/m2`) làm giảm độ chính xác và tính thẩm mỹ. | Auto-convert thành LaTeX mũ: `$\text{m}^2$`, `$\text{daN/m}^2$`, `$\text{kg/m}^3$`. | ADR 0030 (Unit Super-Scripter) |

---

## 8. OKF v2.3 Dual-Engine Technical Standards Paradigm (ADR 0034)

### 8.1. Unified Centered Composite Images:
- **Nguyên tắc:** Sơ đồ hình học kỹ thuật đa nhánh ($a, b, c$, mặt đứng, mặt bằng, mặt cắt) phải được hợp nhất thành **1 file ảnh composite đơn nhất** (`hinh_*.png`) trên nền trắng RGB, nhãn phụ nhúng trực tiếp, căn giữa $100\%$ bằng `<p align="center">`.
- **Cấm tuyệt đối:** Cắt vụn sơ đồ thành các ảnh nhỏ rời rạc rồi dùng thẻ HTML dồn cục làm lệch lề tài liệu so với PDF gốc.

### 8.2. Lossless Multi-Tier Matrix Tables:
- **Nguyên tắc:** Bảo toàn $100\%$ số lượng cột của bảng tra kỹ thuật đa chiều (ví dụ: các cột tỉ lệ $b/h, h/d, \alpha$).
- **Giá trị tải trọng kép:** Định dạng các ô chứa đồng thời giá trị dương và âm (Hút âm / Đẩy dương) bằng thẻ `<br>` (ví dụ: `- 1,7<br>+ 0,0`).
- **Tách chú thích chân bảng:** Toàn bộ ghi chú điều kiện biên và chú thích giải thích ký hiệu được đưa ra ngoài khung bảng Markdown (đặt ngay bên dưới bảng) để tránh làm méo mó cấu trúc dữ liệu.

### 8.3. Pure KaTeX Mathematical Formulation:
- **Nguyên tắc:** Triệt tiêu hoàn toàn ảnh công thức scan chất lượng thấp; chuyển đổi $100\%$ công thức giải tích sang định dạng KaTeX khối có đánh số `$$ ... \tag{X.Y} $$`.

### 8.4. Dual-Engine Architecture (Visual Cards JSON + Deterministic Solvers Python):
- **Thẻ thị giác (Visual Cards JSON - `figures/cards/`):** Khai báo quy tắc phân vùng kích thước hình học (`e = min(b, 2h)`) và cây quyết định rẽ nhánh theo schema `visual_card_v1.json`.
- **Bộ giải số học xác định (Deterministic Solvers Python - `formulas/`):** Đóng gói thành các hàm thuần túy (`pure functions`) xử lý nội suy, tách kịch bản tải trọng độc lập và xuất báo cáo thuyết minh thế số từng bước (`CalculationResult.format_text_report()`).
- **Facade Master (`SymbolicFormulaSolver`):** Quản lý tập trung các công thức quy chuẩn và kết nối trực tiếp với quy trình kiểm tra tự động mô hình BIM (IFC).

---

## 9. R&D Graduation Anti-Pattern & /ccba-graduate-rd Workflow (ADR 0030, ADR 0033)

- **Anti-pattern phát hiện (2026-08-25):** Script vá `patch_tcvn2737_formulas.py` được viết nhanh trong scratch để sửa lỗi công thức TCVN 2737:2023. Khi chạy lại `python -m ccba_legal convert` từ DOCX gốc, logic vá không kích hoạt $\rightarrow$ lỗi tái phát do script nằm ngoài luồng chuyển đổi chính.
- **Giải pháp chuẩn hóa:** Tạo workflow `/ccba-graduate-rd` cưỡng chế 5 bước chuyển hóa R&D $\rightarrow$ Deep Seam Production. 3 Invariants: (1) Không để script vá tồn tại qua phiên, (2) Upstream Promotion bắt buộc, (3) 1-Pass Clean Run.
- **Tham chiếu:** Tier 3 User Workflow, ADR 0030 (Technical Standard Seam), ADR 0033 (Archive chuẩn).

---

## 10. R&D Graduation Ratification: Figure Extractor, Modernize & Visual Parity (2026-08-26)

- **Thành quả Tốt nghiệp R&D:**
  1. **Centered Figure Extraction Seam (`ccba_legal.figure_extractor`):** Hợp nhất chuẩn thẻ hình ảnh kỹ thuật căn giữa `<p align="center">...<p>` vào Deep Seam `figure_extractor.py` và xuất khẩu `extract_technical_figures`, `render_markdown_figure_card` qua `__init__.py`.
  2. **Modernize Annex Engine Seam (`ccba_legal.modernize`):** Chuyển giao `FigureAutoCompositor`, `TableMatrixBuilder`, và `MathEquationConverter` vào module chính quy `ccba_legal.modernize` (ADR 0034).
  3. **Unified Visual Parity Seam (`ccba_legal.visual_parity`):** Tích hợp toàn diện 10 quy tắc kiểm định thị giác (bao gồm chặn footnote bullet thừa, cấm gộp dòng `<br>`, và kiểm tra chuỗi đơn điệu `CHÚ THÍCH 1` khi có `CHÚ THÍCH 2`) vào `VisualParityAuditor` và hàm `lint_document`.
  4. **Zero-Wrapper Spoke CI Gate:** Tái cấu trúc `scripts/lint_visual_parity.py`, `scripts/modernize_annex_engine.py`, và `scripts/check_hub_import_depth.py` để kế thừa trực tiếp từ Hub `ccba_legal`, bảo toàn $100\%$ Shallow Import (ADR 0030 / Hub Shallow Seam Contract) và đạt $10/10$ Cổng Master CI Gate với $0$ Errors, $0$ Warnings.
  5. **Ground Truth Test Harness:** Bổ sung `test_modernize.py`, `test_figure_extractor.py` và cập nhật `test_visual_parity.py` trong Hub `ccba-legal-intel/tests/`, nâng tổng số test cases của Hub lên **154 passed (100%)**.

---

## 11. Test Suite 3-Tier Reorganization & Upstream Loop Harmonization (2026-08-26)

- **Tái Cấu Trúc Bộ Kiểm Thử 3 Phân Tầng (`tests/`):**
  - `tests/unit/`: Chứa các bộ giải toán học kỹ thuật xác định (Deterministic Solvers) — chạy siêu tốc (< 0.8s, 118 tests PASS 100%).
  - `tests/integration/`: Chứa các pipeline chuyển đổi DOCX, Crawler TVPL VIP, VBHNEngine và Spoke CI Gates (32 tests PASS 100%).
  - `tests/e2e/`: Chứa các bộ kiểm toán sâu toàn vẹn tài liệu và dữ liệu lịch sử (Milestone 1, Milestone 2, Tier 1-4).
- **Hàn Gắn Chu Trình Đóng Góp Ngược (Upstream Contribution Loop):**
  - **Liên kết hai chiều `--issue [ID]`:** Đồng bộ từ `/ccba-issue-to-hub` $\to$ `/ccba-graduate-rd` $\to$ `/ccba-contribute-to-hub` $\to$ PR tự động đóng Issue (`Closes #[ID]`).
  - **Cổng Phân Loại Quy Mô Thông Minh (Smart Scope-Aware Issue Gate):** Tự động gợi ý/tạo GitHub Issue cho các thay đổi kiến trúc/module mới ($\ge 100$ dòng) để ghi nhận Changelog & Ký ức dài hạn, đồng thời bỏ qua Issue cho các thay đổi nhỏ ($< 100$ dòng) để tránh rác Issue Tracker.

---

## 12. R&D Graduation: OKF v2.4 Universal Specification, Single-Door tab=7 & Tri-Tier Cloud Vault (2026-08-27)

- **Thành quả Tốt nghiệp R&D & Chuẩn Hóa Sản Phẩm:**
  1. **OKF v2.4 Universal Agent-Centric Specification (ADR 0036):**

     - $100\%$ mọi Bundle bắt buộc phải có thư mục `sources/` chứa PDF Công báo gốc và file Word gốc. Thư mục gốc chỉ chứa giao diện Markdown tinh gọn.
     - Phân tách rạch ròi 4 ngăn kéo chuyên biệt: `tables/` (Bảng 2D), `figures/` (Visual Cards), `annexes/` (Phụ lục kỹ thuật quy chuẩn), `templates/` (Biểu mẫu hành chính nguyên tử). Tuyệt đối cấm để thư mục `templates/` rỗng.
     - Đồng vị ma trận so sánh VBHN (`bang_so_sanh_thay_doi.md`) ngay tại gốc của Bundle để phục vụ QC Agent tra cứu với chi phí $0\text{ token}$.
  2. **Single-Door tab=7 Harvesting Protocol:**
     - Thay thế luồng nhảy 2 tab rườm rà bằng giao thức truy cập trực tiếp `tab=7` (Tải về) để tải trọn gói DOCX + PDF trong 1 lượt mở trang duy nhất.
     - Bổ sung cơ chế **Silent Auto-Verification Grace Period** (chờ ngầm 5–7 giây để Cloudflare tự động xác minh trình duyệt thật) kết hợp `Page.bringToFront` chỉ khi cần người dùng can thiệp thủ công.
  3. **Tri-Tier Cloud Binary Vault & Native Google Docs (ADR 0035):**
     - Tự động hóa upload và chuyển đổi file DOCX sang Native Google Docs trên Google Drive Vault `CCBA_Legal_Vault` phục vụ nạp 1-click vào Google NotebookLM.
     - File `.pdf` và `.docx` được bảo vệ hoàn toàn bởi `.gitignore`, giúp Git Spoke siêu nhẹ (<50MB).
  4. **Bộ Giải Quy Hoạch QCVN 01:2021/BXD:**
     - Hoàn thành 6 bộ giải xác định: Mật độ xây dựng thuần, Khoảng lùi, Khoảng cách an toàn môi trường, Bãi đỗ xe Bảng 2.19, Vát góc nút giao Mục 2.6.2, và Chỉ tiêu đất cây xanh đô thị Bảng 2.1 & 2.2.

---

## 13. R&D Graduation: Universal Ingestion Provenance Engine, Declarative Solvers & Cross-Link Parity (2026-08-28)

- **Thành quả Tốt nghiệp R&D & Chuẩn Hóa Sản Phẩm:**
  1. **Universal Gate 0 Ingestion Provenance Seam (`ccba_legal.provenance` - ADR 0016):**
     - Đưa toàn bộ logic đối soát DOCX vs PDF Công báo vào Hub (`ccba_legal.provenance`), cung cấp các hàm cốt lõi `verify_docx_against_pdf`, `check_structure_alignment`, `compute_text_parity`, `extract_docx_data`, `extract_pdf_data`.
     - Phân biệt PDF số hóa kỹ thuật số vs PDF scan hình ảnh (`is_scanned`), ngăn ngừa sai số giả lập text parity.
     - Spoke `scripts/verify_docx_against_pdf.py` chuyển thành CLI runner tinh gọn, kế thừa 100% từ Hub Deep Seam.
  2. **Declarative Formula Solver Registry (`formulas/solver.py`):**
     - Tái cấu trúc solver registry sang mô hình khai báo tập trung `_BUILTIN_FORMULA_CATALOG` kết hợp Decorator `@register_formula`.
     - Giảm 72% boilerplate code (616 dòng $\to$ 175 dòng), bảo toàn 100% 29 công thức kỹ thuật và 126 unit tests (chạy trong 0.30s).
  3. **Category-Agnostic Cloud RAG Sync (`scripts/sync_notebooklm_knowledge.py`):**
     - Loại bỏ danh mục hardcoded, tự động quét mọi thư mục phân loại dưới `legal_docs/` (`01_vbpl`, `02_qcvn`, `03_tcvn`, ...), đồng bộ trọn vẹn 308 tài sản RAG.
  4. **Dynamic Fixtures & 100% Cross-Links Integrity:**
     - Dynamic test fixtures trong `tests/conftest.py` đọc trực tiếp từ `legal_registry.yaml`.
     - 100% liên kết chéo và thẻ neo hình ảnh, bảng biểu trên toàn bộ 31 gói tri thức được chuẩn hóa chính xác tuyệt đối.
  5. **Quy Chuẩn Dọn Dẹp Scratch (Zero-Scratch Invariant):**
     - Tự động di chuyển toàn bộ script thử nghiệm sang `.md/archive/rd_scratch/`, giữ sạch 100% thư mục gốc và `scripts/`.

---

## 14. Documentation-as-Code Parity CI Governance, Shallow Path Adoption & Closed-Loop Release (2026-08-28)

- **Thành quả Quản Trị Hệ Thống & Chống Lệch Pha (Zero Doc-Code Drift):**
  1. **Tấm Khiên Kiểm Thử Tương Thích Lệnh - Mã Nguồn (test_workflow_script_parity.py):**
     - Xây dựng bài test CI tự động quét 100% các file .agents/workflows/*.md và .agents/skills/**/SKILL.md.
     - Tự động bóc tách mọi lệnh python scripts/..., python -m <package>, và liên kết tương đối. Báo lỗi chặn build ngay lập tức nếu phát hiện script đã bị đổi tên/xóa hoặc module chưa đăng ký.
     - Chuẩn hóa toàn bộ 68 workflows và 76 skills trên Hub, đồng bộ 24/24 governance tests pass 100%.
  2. **Nâng Cấp Bộ Nhận Diện Vòng Đời Spoke (spoke_adopter.py - Hub ADR-0041, ADR 0036):**
     - Nâng cấp detect_spoke_stack trong /ccba-adopt-spoke để tự động nhận diện Spoke Tri thức theo mô hình Shallow Path Cấp 1 (legal_docs/ và legal_registry.yaml ở Root), gán chính xác Archetype knowledge_corpus.
     - Cập nhật Mẫu C trong /ccba-init-spoke lên chuẩn OKF v2.4 Universal Agent-Centric.
  3. **Quy Trình Khép Kín Đóng Góp & Phát Hành (Closed-Loop Release Loop):**
     - Hoàn tất quy trình mẫu 7 bước: R&D -> /ccba-graduate-rd -> /ccba-contribute-to-hub (Hub PR #220) -> /ccba-create-pr & /ccba-release-feature (Spoke PR #1) -> sync_spoke.py --apply.
     - Cả 2 repositories Hub và Spoke đều đạt trạng thái sạch sẽ, 100% tích hợp và đồng bộ với GitHub origin.

---

## 15. Verbatim Normative Invariant, Universal Ingestion Pipeline & Gate 11 Parity Enforcement (2026-08-28)

- **Thành quả Quản Trị & Cưỡng Chế Nguyên Văn Pháp Lý (Zero Paraphrase Drift):**
  1. **Hiến pháp Bất khả xâm phạm Thân văn bản Quy phạm (Verbatim Normative Invariant - ADR 0037):**
     - Ban hành quy tắc bất biến cấm $100\%$ mọi hành vi tóm tắt, diễn đạt lại (paraphrase), lược bỏ hoặc viết tắt câu từ trong thân văn bản quy chuẩn/luật (`.md`).
     - Phân định rạch ròi 2 tầng trích xuất:
       * **Thân văn bản quy phạm:** Bắt buộc trích xuất xác định $1:1$ từ DOCX Công báo gốc bằng Python `python-docx` AST parser (không cho phép LLM can thiệp tái tạo câu chữ).
       * **Dữ liệu phái sinh:** LLM chỉ được phép phân tích ở các tệp hỗ trợ bên ngoài thân văn bản (`metadata.yaml`, `clauses.json`, `qa_benchmark.json`, `figures/cards/`, `templates/`).
  2. **Gate 11: DOCX-to-Markdown Verbatim Normative Parity Gate (`scripts/validate_legal_spoke.py`):**
     - Tích hợp cổng kiểm định thứ 11 tự động băm nhỏ và so khớp toàn bộ đoạn văn trong `sources/*.docx` với Markdown bundle.
     - Cưỡng chế tỷ lệ trùng khớp $\ge 98.0\%$. Tự động chặn đứng `git commit` và CI nếu phát hiện bất kỳ điều khoản, định nghĩa hoặc chú thích nào bị thiếu hoặc sai lệch.
  3. **Nạp & Chuẩn Hóa Chuẩn Mực QCVN 03:2022/BXD (Thông tư 05/2022/TT-BXD):**
     - Hoàn tất đóng gói toàn diện OKF v2.4 cho QCVN 03:2022/BXD đạt 100.0% Parity (12 trang PDF, 137 đoạn DOCX nguyên văn, 23 điều khoản AST `CQXD`, Bảng 1 Niên hạn thiết kế Mức 1-4, Phụ lục A Cấp hậu quả C1/C2/C3, Thẻ tính toán tham số và Mẫu thuyết minh phân cấp).
