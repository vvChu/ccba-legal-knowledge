# 🧠 CCBA Legal Knowledge Spoke: Active Architectural Invariants (Compacted Working Memory)

> **Phạm vi áp dụng:** Spoke Tri thức Pháp lý (`ccba-legal-knowledge`)
> **Tiêu chuẩn:** OKF v2.4 Universal Agent-Centric, ADR 0021, 0029, 0030, 0031, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0058, 0059.
> **Tra cứu Chi tiết Lịch sử & Đầy đủ 53 Bài Học:** [session_learnings_history.md](archive/session_learnings_history.md) | Ngân sách bộ nhớ: $\le 10\text{ KB}$

---

## Miền 1. 🌐 Thu Thập & Xác Thực Nguồn Gốc Pháp Lý (Acquisition, Ingestion & Provenance)

- **RULE-1.1 [TVPL VIP 3-Tier Download Priority — ADR 0031 & ADR 0035]**:
  - *Tier 1 (`part=-100`)*: VIP Digital Vector PDF (Mỏ neo pháp lý tối thượng, độ nét 100%, zero-OCR).
  - *Tier 2 (`part=-1&docx=1`)*: VIP OpenXML Word Document (Nguồn dữ liệu gốc vàng nạp vào `docx_converter.py`).
  - *Tier 3 (`part=0`)*: Gazette Scan PDF (Bản scan Công báo dự phòng).
- **RULE-1.2 [Giao Thức Một Cửa `tab=7` & Chromium VIP Session — ADR 0031]**:
  - Sử dụng Chromium CDP trên cổng `9222` độc lập với profile `~/.gemini/antigravity/chrome_vip`. Toàn bộ thao tác tải file DOCX/PDF bắt buộc đi qua giao thức `tab=7` và API tham số hóa TVPL.
- **RULE-1.3 [Lưu Trữ Song Song Dual-PDF & Vault Drive — ADR 0043]**:
  - Bản scan mờ lưu thành `sources/<slug>_raw_scan.pdf`. Bản Vector PDF kết xuất từ Word COM lưu thành `sources/<slug>.pdf` kèm cờ `pdf_origin: docx_vector_rendered` trong `metadata.yaml`. Đồng bộ cả 2 lên Google Drive Vault `CCBA_Legal_Vault`.
- **RULE-1.4 [Chuẩn Hóa Đường Dẫn POSIX Toàn Cầu — ADR 0035 & ADR 0036]**:
  - 100% đường dẫn trong `legal_registry.yaml` và bundle `metadata.yaml` (`bundle_path`, `pdf_path`, `raw_scan_pdf`, `source_file`, `vault_path`) BẮT BUỘC dùng dấu gạch chéo thuận POSIX `/`, nghiêm cấm tuyệt đối dấu gạch chéo ngược Windows `\`.
  - Mọi pipeline nạp văn bản (`spoke_cli.py ingest`) bắt buộc tự động chuẩn hóa qua `.replace("\\", "/")`.
  - Gate 1 và Gate 2 trong `validate_legal_spoke.py` tự động kích hoạt lỗi định dạng `Registry Format Error` / `OKF Metadata Format Error` nếu phát hiện ký tự `\`.

---

## Miền 2. 📐 Bóc Tách Đa Phương Thức & Chuẩn Hóa Toán Học KaTeX (Multimodal & KaTeX Integrity)

- **RULE-2.1 [Bóc Tách Xác Định MTEF MathType & Khử Tệp Đóng Kín — ADR 0040]**:
  - Bóc tách 100% công thức MathType nhị phân (MTEF v3/v5) từ OLE stream sang KaTeX, không qua OCR hay tốn AI token.
  - Áp dụng 4-Tier Hybrid Formula Fallback Engine. Vector WMF/EMF bắt buộc chuyển sang Dual-Format (SVG và PNG $\ge 300\text{ DPI}$). Nghiêm cấm lưu file `.wmf`/`.emf` nhị phân đóng kín.
- **RULE-2.2 [Cú Pháp Toán Học KaTeX Đa Dòng & Bảo Toàn Dấu — ADR 0038 & ADR 0044]**:
  - Trong các môi trường đa dòng (`aligned`, `cases`, `gather`), BẮT BUỘC dùng `\qquad (X)` ở cuối dòng thay cho `\tag{...}` để đảm bảo không sinh lỗi bôi đỏ KaTeX.
  - Bảo tồn tuyệt đối cặp ngoặc `\left[` / `\right]`. Tách chú thích hình `<!-- FIGURE: ... -->` ra khỏi khối KaTeX `$$`.
- **RULE-2.3 [Bảo Tồn Chú Thích Kẹp Giữa Sơ Đồ Đồ Họa — ADR 0039]**:
  - Bảo tồn 100% các đoạn `CHÚ THÍCH` và `CHÚ DẪN` kẹp giữa ảnh và tiêu đề hình. Xếp dọc đa tầng (Vertical Stack) lề an toàn $\ge 40\text{ px}$. Bắt buộc vượt qua Sub-Gate 11.2 Zero-Dropped Regulatory Notes.

---

## Miền 3. 📊 Cấu Trúc Bảng Biểu 2D & Mẫu Biểu Nguyên Tử (Deterministic Tables & Form Templates)

- **RULE-3.1 [Lưới Tọa Độ Ảo 2D & Forward-Fill Có Kiểm Soát — ADR 0041]**:
  - Thiết lập lưới tọa độ 2D từ `tblGrid`. Áp dụng Hierarchical Forward-Fill có kiểm soát cho ô gộp dọc (`vMerge`) trong CSV/JSON.
  - Phẳng hóa tiêu đề đa tầng bằng Em-dash ngữ nghĩa (`Tầng 1 — Tầng 2 — Tầng 3`). 100% CSV đạt chuẩn Zero Ragged Rows.
- **RULE-3.2 [Tách Rời Chú Thích Bảng & Định Tuyến Biểu Mẫu — ADR 0021 & ADR 0041]**:
  - Bóc tách 100% chú thích chân bảng (`footnotes`) ra khỏi ma trận dữ liệu quan hệ. Thoát an toàn ký tự `|` trong cell và KaTeX (`\vert `).
  - Tách các biểu mẫu hành chính nguyên tử sang thư mục `templates/`, cấm để thư mục `templates/` rỗng.
- **RULE-3.3 [Định Danh Bảng Quy Chuẩn Đa Phần — ADR 0044]**:
  - Văn bản có nhiều phần (QCVN 07) bắt buộc bảng phải mang tiền tố mã định danh (ví dụ `bang_p01_01.csv`) và khai báo `part_id` trong `tables_catalog.json`.
- **RULE-3.4 [Thu Thập & Đếm Biểu Mẫu Hành Chính Đệ Quy — ADR 0021, ADR 0028 & ADR 0036]**:
  - Biểu mẫu hành chính nguyên tử được phép tổ chức theo thư mục con phụ lục (ví dụ `templates/phu_luc_iv/*.md`) theo đặc tả ADR 0028.
  - Mọi công cụ đếm hoặc lập manifest (`spoke_cli.py`, `sync_notebooklm_knowledge.py`, `validate_legal_spoke.py`) BẮT BUỘC sử dụng quét đệ quy (`glob("**/templates/**/*.md")` hoặc `rglob("*.md")`) để bảo toàn 100% biểu mẫu (mốc kiểm chuẩn 128 templates tại PR #16).

---

## Miền 4. 🏛️ Chuẩn Hóa OpenXML DOM & Bảo Tồn Nguyên Văn Quy Phạm (OpenXML Sanitizer & Verbatim Parity)

- **RULE-4.1 [Tiền Xử Lý In-Memory DocxCanonicalSanitizer — ADR 0042]**:
  - Gọt sạch `w:rsid*`, loại bỏ `w:proofErr`, gộp run liền kề đồng nhất, chuẩn hóa Unicode NFC, tiêm `xml:space="preserve"`.
  - Giải nén borderless layout tables qua Multi-Factor Scoring (mật độ số liệu $\ge 30\%$). Bảo tồn tuyệt đối whitelist `<w:object>`, `<m:oMath>`, `<w:drawing>`.
- **RULE-4.2 [Bảo Tồn Nguyên Văn Quy Phạm 100% — ADR 0037 & ADR 0059]**:
  - NGHIÊM CẤM mọi hành vi tóm tắt, diễn đạt lại hoặc rút gọn thân văn bản quy phạm. Thân Markdown bắt buộc trích xuất xác định 1:1 từ DOCX và đạt Gate 11 Verbatim Parity $\ge 98.0\%$.
- **RULE-4.3 [Bảo Tồn Ký Tự Gốc & Thoát Ký Tự Gạch Đầu Dòng — ADR 0029 & ADR 0030]**:
  - Bảo tồn 100% dấu gạch đầu dòng `-` và `+` bằng cơ chế thoát ký tự `\- ` và `&nbsp;&nbsp;\+ `. Không dồn cục dòng; vượt qua `lint_visual_parity.py`.
- **RULE-4.4 [Ground Truth Engine Bilateral Symmetry & Scope Partitioning — ADR 0045]**:
  - Đồng bộ đối xứng 100% giữa nhánh DOCX và PDF trong Parity Engine: áp dụng giải thuật Block Multi-span Coverage (`check_multi_span_coverage`) kết hợp bóc thẻ HTML và flat Markdown link.
  - Áp dụng state-machine lọc ranh giới ký duyệt (`in_signatory`: `Nơi nhận:`, `KT. BỘ TRƯỞNG`, `TM. CHÍNH PHỦ`, `THỦ TƯỚNG`, `PHÓ THỦ TƯỚNG`, `THỨ TRƯỞNG`) và tài liệu tham khảo (`in_bibliography`).
  - Hỗ trợ phân tách phạm vi trang thân quy phạm `verification_scope.normative_body_pages` trong `metadata.yaml` cho các thông tư có hàng nghìn trang biểu mức định mức dự toán được bóc tách riêng sang `templates/` và `tables/`.

---

## Miền 5. 🛡️ Hệ Thống Kiểm Định CI 15 Cổng & Hiệu Lực Pháp Lý Tuyệt Đối (CI Gates & Legal Governance)

- **RULE-5.1 [Rào Chắn Hiệu Lực Pháp Lý Tuyệt Đối — Từ 01/07/2026]**:
  - Mọi văn bản pháp luật viện dẫn BẮT BUỘC ĐANG CÓ HIỆU LỰC.
  - VĂN BẢN HIỆN HÀNH: **Luật Xây dựng 2025** (Luật số `135/2025/QH15`), **Nghị định 217/2026/NĐ-CP** (Quản lý Hoạt động Xây dựng — thay thế NĐ 175/2024 & NĐ 15/2021), **Nghị định 207/2026/NĐ-CP** (Quản lý Chất lượng & Bảo trì — thay thế NĐ 06/2021).
- **RULE-5.2 [15 Cổng Kiểm Định Nghiệm Thu Master CI Gate — ADR 0058]**:
  - Thực thi tự động: `python scripts/validate_legal_spoke.py`.
  - Tiêu chuẩn nghiệm thu 100%: 0 Errors, 0 Warnings, 100% Visual Parity, 100% Verbatim Match, 100% Valid Links, 100% PDF SHA-256 Match, 100% SVG/Cards Integrity, 100% 2D Regularity, 100% KaTeX Math Integrity, 100% OKF Provenance Attestation.
- **RULE-5.3 [Single-User Multi-Device & Machine-State Decoupling]**:
  - Khi clone Spoke về nhiều máy (Windows, Linux, WSL), CẤM commit đường dẫn ổ đĩa tuyệt đối vào `workspace_context.yaml`. Đường dẫn Hub cô lập qua biến môi trường `CCBA_HUB_PATH`.
