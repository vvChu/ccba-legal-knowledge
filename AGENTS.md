# CCBA Legal Knowledge Spoke — Workspace Constitution

> [!IMPORTANT]
> **Đây là Repository Spoke Tri thức Pháp lý chính quy của CCBA Agent Platform.**
> Tất cả dữ liệu tri thức được đóng gói theo tiêu chuẩn **OKF v2.4 Universal Agent-Centric (ADR 0021, ADR 0034, ADR 0035, ADR 0036)**.

---

## 🏛️ Quy tắc Vận hành Spoke Bất Biến (Core Invariants):
1. **Mô hình Đường dẫn Nông (Shallow Path):** Thư mục `legal_docs/` nằm tại Cấp 1 của Spoke. `legal_registry.yaml` nằm tại Root.
2. **Reuse-First Gate:** Mọi thao tác cập nhật dữ liệu phải kế thừa trực tiếp từ package Hub (`packages/ccba-legal-intel`).
3. **Độc lập Mã nguồn:** Không chứa code ứng dụng frontend/backend, tập trung 100% cho OKF Markdown Bundles, RAG Metadata, Atomic Templates và Pipeline kiểm định.
4. **Ngăn Kéo Nguồn Gốc Bắt Buộc (Universal `sources/` Invariant - ADR 0036):** $100\%$ mọi Bundle bắt buộc phải có thư mục `sources/` chứa PDF Công báo gốc, file Word và các tài liệu nguồn cấu thành (`_goc.md`, `sua_doi_XX.md`). Thư mục gốc chỉ chứa giao diện Agent tinh gọn (`.md`, `metadata.yaml`, `clauses.json`, `index.md`).
5. **Phân Tách Rạch Ròi 4 Ngăn Kéo Dữ Liệu (4 Specialized Compartments - ADR 0036):**
   * `tables/`: Bảng số liệu tra cứu 2D (CSV, JSON, `tables_catalog.json`).
   * `figures/`: Thẻ thị giác tính toán tham số hóa (`cards/`, `figures_catalog.yaml`).
   * `annexes/`: Phụ lục kỹ thuật quy phạm (Technical Normative Annexes).
   * `templates/`: Biểu mẫu hành chính nguyên tử (Atomic Form Templates theo ADR 0021). Cấm để thư mục `templates/` rỗng.
6. **Đồng Vị Ma Trận So Sánh VBHN (In-Bundle Comparative Matrix - ADR 0036):** Đối với văn bản hợp nhất, `bang_so_sanh_thay_doi.md` bắt buộc phải đặt trực tiếp ngay tại gốc của Bundle.
7. **Tri-Tier Cloud Binary Vault & Native Google Docs (ADR 0035):** Toàn bộ file `.pdf` và `.docx` được bảo vệ bởi `.gitignore` và đồng bộ lên Google Drive Vault `CCBA_Legal_Vault`. File Word được tự động chuyển đổi sang Native Google Docs sẵn sàng cho Google NotebookLM.
8. **Bảo Tồn Ký Tự Gốc & Kiểm Định Thị Giác (ADR 0029 & ADR 0030):** Bảo toàn $100\%$ dấu gạch đầu dòng `-` và `+` bằng cơ chế thoát ký tự `\- ` và `&nbsp;&nbsp;\+ `; Tách chú thích ra khỏi ô bảng; Không dồn cục dòng; Bắt buộc vượt qua `lint_visual_parity.py`.
9. **Bảo Tồn Nguyên Văn Quy Phạm 100% (Verbatim Normative Invariant - ADR 0037):** Nghiêm cấm mọi hành vi tóm tắt, diễn đạt lại hoặc rút gọn thân văn bản quy phạm. Thân Markdown bắt buộc phải được trích xuất xác định $1:1$ từ DOCX Công báo gốc và vượt qua Gate 11 DOCX-to-Markdown Verbatim Parity (Parity Rate $\ge 98.0\%$).
10. **Chuẩn Hóa Cú Pháp Toán Học KaTeX Toàn Cầu (Universal KaTeX Syntax Integrity - ADR 0038):** Quét và trích xuất nguyên bản 100% công thức MathType độc lập từ DOCX sang KaTeX; Cô lập ranh giới từ Regex, bảo toàn tuyệt đối cặp ngoặc `\left[` / `\right]`; Dùng `\qquad (X)` trong các môi trường đa dòng (`aligned`, `cases`, `gather`) thay cho `\tag{...}` để đảm bảo không sinh lỗi bôi đỏ; Tách rời hoàn toàn chú thích hình ảnh `<!-- FIGURE: ... -->` ra khỏi khối `$$`.
11. **Bóc Tách Sơ Đồ Đồ Họa Độ Nét Cao & Bảo Tồn Tuyệt Đối Chú Thích Kẹp Giữa (ADR 0039):** Quét và trích xuất text/công thức từ bảng bố cục không viền; Bảo tồn $100\%$ các đoạn `CHÚ THÍCH` và `CHÚ DẪN` kẹp giữa ảnh và tiêu đề hình; Xếp dọc đa tầng (Vertical Stack) với lề an toàn $\ge 40\text{ px}$ cho hình có nhiều sơ đồ con; Quy chuẩn toàn bộ chỉ số dưới trong tiêu đề sang KaTeX; Bắt buộc vượt qua Sub-Gate 11.2 Zero-Dropped Regulatory Notes.
12. **Bóc Tách Tri Thức Đa Phương Thức Xác Định & Khử Tệp Đóng Kín (Universal Deterministic Multimodal Extraction & Zero-Closed-Binary Invariant - ADR 0040):** Bóc tách xác định 100% công thức MathType nhị phân (MTEF v3/v5) từ OLE stream mà không qua OCR hay tốn AI token; Áp dụng cơ chế 4-Tier Hybrid Formula Fallback Engine; Đồ họa vector WMF/EMF bắt buộc chuyển đổi sang Dual-Format (SVG và PNG $\ge 300\text{ DPI}$), nghiêm cấm lưu trữ file `.wmf`/`.emf` đóng kín; Tự động đồng bộ thẻ thị giác `figures/cards/hinh_{slug}.md` $1:1$ với `figures_catalog.yaml`; Bắt buộc vượt qua Gate 12 Multimodal Decoupled Asset & SVG/Cards Integrity Gate.
13. **Bóc Tách Tri Thức Bảng Biểu Xác Định Toàn Cầu (Universal Deterministic Table Knowledge Extraction & 2D Grid Regularity Invariant - ADR 0041):** Thiết lập Lưới Tọa Độ Ảo 2D (`tblGrid`); Áp dụng Hierarchical Forward-Fill có kiểm soát cho ô gộp dọc (`vMerge`) trong CSV/JSON; Phẳng hóa tiêu đề đa tầng bằng Em-dash ngữ nghĩa (`Tầng 1 — Tầng 2 — Tầng 3`); Bóc tách 100% chú thích chân bảng (`footnotes`) ra khỏi ma trận dữ liệu quan hệ; Thoát an toàn ký tự `|` trong cell và KaTeX (`\vert `); Định tuyến biểu mẫu hành chính sang `templates/`; Bắt buộc ma trận CSV đạt chuẩn $100\%$ Zero Ragged Rows.
14. **Chuẩn Hóa Cấu Trúc OpenXML DOM & Động Cơ Lai Ghép DOCX-PDF Hai Tầng (Universal Canonical OpenXML Sanitization & Hybrid Dual-Engine Invariant - ADR 0042):** Tiền xử lý 100% in-memory qua `DocxCanonicalSanitizer` (gọt `w:rsid*`, loại bỏ `w:proofErr`, gộp run liền kề đồng nhất, chuẩn hóa Unicode NFC, tiêm `xml:space="preserve"`, giải nén borderless layout tables, thăng cấp heading); bảo tồn tuyệt đối whitelist `<w:object>`, `<m:oMath>`, `<w:drawing>`; kết hợp DOCX làm khung xương AST phân cấp và PDF làm mỏ neo không gian kiểm chuẩn.

---

## 🚀 Quy trình 4 Bước Chuẩn Hóa Văn Bản Mới (Universal OKF v2.4 Pipeline):

Bất kỳ khi nào tiếp nhận một Luật, Nghị định, Thông tư, QCVN hoặc TCVN mới, Agent **bắt buộc** thực hiện tuần tự 4 bước:

### 0. Thu thập & Xác thực Nguồn gốc (Acquisition Gate — Giao thức "Một Cửa `tab=7`"):
* **Kịch bản 1 — Nạp tự động 1 lệnh toàn trình (Happy Path):**
```powershell
python -m ccba_legal ingest "<tvpl_url>" --category <01_vbpl|02_qcvn|03_tcvn> --upload-drive
```
* **Kịch bản 2 — Tiếp nhận thủ công / Fallback khi cào bị lỗi:** Nếu lệnh `ingest` bị kẹt do Cloudflare/Captcha, Agent giải quyết cục bộ để đưa đúng 2 tệp `.docx` và `.pdf` vào `sources/`. Ngay sau đó **bắt buộc** thực thi Bước 1 bằng lệnh `convert` — **nghiêm cấm tự viết Markdown bằng LLM**.
* **Kịch bản 3 — Làm mới / Thay thế file kém chất lượng:** Khi cần thay thế file scan mờ bằng bản nét, chạy `python -m ccba_legal fetch "<tvpl_url>"` để tải đè file chuẩn vào `sources/` rồi chạy lại Bước 1 `convert`.

### 1. Nạp & Chuyển đổi sang OKF v2.4 Bundle (ADR 0021, ADR 0034, ADR 0036, ADR 0037, ADR 0042):
* Thực thi lệnh chuyển đổi trích xuất nguyên văn $100\%$ qua Động cơ Lai ghép DOCX-PDF Hai tầng kết hợp Tiền xử lý DOM In-Memory `DocxCanonicalSanitizer` (Zero-LLM Paraphrase):
```powershell
python -m ccba_legal convert --docx-path "legal_docs/<category>/<doc_slug>/sources/<doc_slug>.docx" --target-bundle-dir "legal_docs/<category>/<doc_slug>"
```
* Tự động tạo thân văn bản nguyên văn $1:1$, 32+ bảng số liệu 2D (`tables/`), phụ lục biểu mẫu (`templates/`), cây điều khoản AST `clauses.json` và bộ câu hỏi `qa_benchmark.json`.

### 2. Hợp nhất Văn bản Sửa đổi (VBHN Engine - nếu có văn bản sửa đổi):
```powershell
python -m ccba_legal consolidate `
  --manifest legal_docs/02_qcvn/ten_van_ban/patch_manifest.yaml `
  --base legal_docs/02_qcvn/ten_van_ban/sources/ten_van_ban_goc.md `
  --output legal_docs/02_qcvn/ten_van_ban/
```

### 3. Kiểm định Nghiệm Thu Master CI Gate (1-Command Automation-First):
```powershell
python scripts/validate_legal_spoke.py
```
*Tự động thực thi toàn bộ 12 Cổng kiểm định tuần tự (Registry, OKF Bundles, Table Attachments, Fake Data, PDF Metadata, Pure Body, Cleanliness, Atomic Templates, Visual Parity, Self-Healing ADR Traceability, DOCX-to-Markdown Verbatim Parity, và Multimodal Decoupled Asset & SVG/Cards Integrity).*
*Tiêu chuẩn nghiệm thu:* `0 Errors, 0 Warnings, 100% Visual Parity, 100% Verbatim Match, 100% Valid Links, 100% PDF SHA-256 Match, 100% SVG/Cards Integrity`.
