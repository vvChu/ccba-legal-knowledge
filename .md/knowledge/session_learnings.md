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
