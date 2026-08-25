# 🧠 CCBA Platform Knowledge Base: Session Learnings & Architectural Invariants

> **Scope:** Hub (`ccba-agent-platform`) & Spokes (`ccba-legal-knowledge`, etc.)
> **Standard:** OKF v2.2, ADR 0016, ADR 0021, ADR 0031, ADR 0032.

---

## 1. TVPL VIP 3-Tier Download Priority & Parameter Discovery (ADR 0031)

- **Tier 1 — VIP Digital Vector Searchable PDF (`part=-100` / `#ctl00_Content_ThongTinVB_filePDFHyperLink`):**
  - **Mỏ neo Pháp lý Tối thượng Cấp 1 (Primary Anchor of Trust)**: Bản PDF số hóa toàn văn (ví dụ QCVN 02 619 trang, QCVN 06 182 trang, TT 38 1,893 trang). Chứa trọn vẹn 100% thân văn bản, toàn bộ phụ lục, bảng biểu và đồ thị.
- **Tier 2 — VIP OpenXML Word Document (`part=-1&docx=1` / `#ctl00_Content_ThongTinVB_vietnameseHyperLink_Docx`):**
  - **Nguồn Dữ Liệu Gốc Vàng (Gold Source Input)**: Nạp trực tiếp vào `docx_converter.py` để sinh ra OKF v2.2 Markdown Bundle (phân rã biểu mẫu `templates/` và bảng tra cứu `tables/`).
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

## 4. Spoke CI Gates Verification Pipeline

Mọi văn bản trước khi nghiệm thu vào kho tri thức bắt buộc phải vượt qua tuần tự 5 cổng kiểm định không dung thứ (Zero-Tolerance):
1. `python scripts/lint_visual_parity.py` (0 lỗi layout/thoát ký tự `\- ` và `&nbsp;&nbsp;\+ `)
2. `python scripts/validate_legal_spoke.py` (0 lỗi schema, AST, bảng biểu)
3. `python scripts/test_converter_regression.py` (100% gói vượt qua kiểm thử hồi quy)
4. `python scripts/verify_all_docs_against_pdf.py` (100% PDF Verified & SHA-256 Valid)
5. `python scripts/verify_cross_links.py` (100% liên kết điều khoản và phụ lục hợp lệ)

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

## 6. Mathematical Formula & Engineering Table Ingestion Governance (ADR 0030, ADR 0031, ADR 0020)

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







## 9. R&D Graduation Anti-Pattern & /ccba-graduate-rd Workflow (ADR 0030, ADR 0033)

- **Anti-pattern phát hiện (2026-08-25):** Script vá `patch_tcvn2737_formulas.py` được viết nhanh trong scratch để sửa lỗi công thức TCVN 2737:2023. Khi chạy lại `python -m ccba_legal convert` từ DOCX gốc, logic vá không kích hoạt → lỗi tái phát do script nằm ngoài luồng chuyển đổi chính.
- **Giải pháp chuẩn hóa:** Tạo workflow `/ccba-graduate-rd` cưỡng chế 5 bước chuyển hóa R&D → Deep Seam Production. 3 Invariants: (1) Không để script vá tồn tại qua phiên, (2) Upstream Promotion bắt buộc, (3) 1-Pass Clean Run.
- **Tham chiếu:** Tier 3 User Workflow, ADR 0030 (Technical Standard Seam), ADR 0033 (Archive chuẩn).
