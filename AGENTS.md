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

### 1. Nạp & Chuyển đổi sang OKF v2.4 Bundle (ADR 0021, ADR 0034, ADR 0036, ADR 0037):
* Thực thi lệnh chuyển đổi trích xuất nguyên văn $100\%$ bằng Deterministic Python-docx AST parser (Zero-LLM Paraphrase):
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
*Tự động thực thi toàn bộ 11 Cổng kiểm định tuần tự (Registry, OKF Bundles, Table Attachments, Fake Data, PDF Metadata, Pure Body, Cleanliness, Atomic Templates, Visual Parity, Self-Healing ADR Traceability, và DOCX-to-Markdown Verbatim Parity).*
*Tiêu chuẩn nghiệm thu:* `0 Errors, 0 Warnings, 100% Visual Parity, 100% Verbatim Match, 100% Valid Links, 100% PDF SHA-256 Match`.
