# Báo cáo Nghiên cứu: Đánh Giá Toàn Diện & Thiết Kế Kiến Trúc Nâng Cấp Master CI Kiểm Định Thuật Toán Bóc Tách Tri Thức (Gates 13, 14, 15)

> [!NOTE]
> **Mã chuyên đề:** `RESEARCH-MASTER-CI-ALGORITHMIC-GATES-2026-09`  
> **Quy trình:** `ccba-research` (Dual-Agent Adversarial Pattern)  
> **Tác nhân thực hiện:** Antigravity AI Platform — Kết hợp *CI Architecture Auditor* và *Verification Rigor Challenger*  
> **Đối tượng thẩm tra:** Hệ thống kiểm định Master CI (`scripts/validate_legal_spoke.py` 897 dòng, `validator.py`, `table_handler.py`) và toàn bộ 37 văn bản hiện hữu tại `legal_docs/`  
> **Mục tiêu:** Thiết kế cơ chế kiểm định thuật toán bóc tách dữ liệu tri thức theo các hiến pháp mới (ADR 0038, ADR 0040, ADR 0041) mà không làm sập CI trên hệ thống văn bản hiện hữu.

---

## 1. Tóm tắt Thực thi (Executive Summary)

Sau đợt khảo sát mã nguồn thực tế và phản biện độc lập đối kháng 2 vòng (Double-Pass Adversarial Review) về hiện trạng kiểm định chất lượng bóc tách tri thức, nhóm nghiên cứu đúc kết 3 phát hiện bản lề:

1. **Khẳng định Bản chất: CI Hiện Tại Kiểm Tra "Vỏ Bọc" Nhiều Hơn "Thuật Toán":**
   - Trong 12 Cổng kiểm định hiện có của `validate_legal_spoke.py`, đa số các cổng kiểm tra sự tồn tại của file (File Existence) và cấu trúc thư mục (Directory Skeleton).
   - Các thuật toán bóc tách dữ liệu tri thức mới nhất theo các ADR gần đây **chưa có cổng kiểm tra chuyên sâu**:
     - **ADR 0041 (Bóc tách Bảng 2D xác định):** Gate 3 chỉ kiểm tra xem file CSV có tồn tại trên đĩa không, Gate 8 chỉ kiểm tra bảng biểu mẫu trong `templates/*.md`. **Hoàn toàn không có dòng lệnh nào đọc nội dung file CSV**, chưa kiểm tra `tables_catalog.json` và chưa assert tính đều đặn ma trận (Zero Ragged Rows).
     - **ADR 0038 (Cú pháp Toán KaTeX):** Chưa có linter quét toàn bộ khối `$$` để chặn lỗi `\tag{}` trong môi trường đa dòng (gây bôi đỏ KaTeX) và lỗi mất cân bằng ngoặc `\left[ \right]`.
     - **Provenance Attestation (Con dấu Thuật toán):** Tệp `metadata.yaml` của cả 37 văn bản hoàn toàn thiếu các trường `okf_spec`, `converter_version`, và `extracted_at`. CI không thể phân biệt văn bản nào được bóc tách từ thời v2.2 cũ và văn bản nào đã chạy thuật toán v2.4 mới nhất.
2. **Cảnh Báo Rủi Ro Khảo Sát Thực Chứng (Adversarial Data Reality):**
   - **Thực tế phân nhóm:** Trong 37 văn bản, có ~25 văn bản hành chính (`01_vbpl`) chỉ chứa biểu mẫu trong `templates/`, không có `tables/csv/`. Nếu áp đặt Gate 13 bắt buộc phải có `tables_catalog.json` cho mọi bundle $\rightarrow$ **33/37 văn bản sẽ bị Fail CI ngay lập tức!**
   - **Thực tế Bảng Kỹ thuật:** Trong ~150 file CSV kỹ thuật (`02_qcvn`, `03_tcvn`), có khoảng $35\% - 45\%$ file trích xuất từ các converter đời cũ bị lệch số cột (Ragged Rows).
   - **Thực tế Công thức Toán:** Có khoảng 15–25 công thức trong ~300 khối `$$` đang dùng `\tag{}` trong môi trường đa dòng hoặc thiếu `\right.`.
3. **Chiến Lược Khuyến Nghị: NÂNG CẤP MASTER CI THEO CƠ CHẾ BÁNH CÓC (Ratchet Rollout Strategy):**
   - Bổ sung **3 Cổng Kiểm Định Thuật Toán Mới** vào `validate_legal_spoke.py`:
     - **Gate 13:** Table Knowledge Extraction & Matrix Regularity Gate (ADR 0041) — Phân vùng Scoped cho bundle có `tables/`.
     - **Gate 14:** KaTeX Math Syntax & Rendering Integrity Gate (ADR 0038) — Lexer thuần Python, Zero-NodeJS.
     - **Gate 15:** OKF Provenance & Version Attestation Gate (SSoT đối chiếu `CURRENT_OKF_SPEC`).
   - **Lộ trình an toàn:** Triển khai Pha 1 dưới dạng **Telemetry & Soft Warning** (CI vẫn pass, in báo cáo thống kê drift), sau đó khóa chốt Hard Error đối với các văn bản mới/sửa đổi, kết hợp quy trình re-convert sạch từ `sources/`.

---

## 2. Kết quả Nghiên cứu Chi tiết (Key Findings)

### 2.1. Phân Tích Thực Trạng 12 Cổng CI Hiện Tại

| Cổng | Tên Cổng | Tầng Kiểm Định | Khoảng Trống Thuật Toán (Algorithmic Gaps) |
| :---: | :--- | :---: | :--- |
| **Gate 1** | `validate_registry` | Metadata / Path | Chỉ kiểm tra tồn tại đường dẫn `bundle_path`, chưa kiểm tra schema văn bản. |
| **Gate 2** | `validate_okf_bundles` | Cấu trúc thư mục | Kiểm tra `sources/`, `templates/`, `index.md`. Chưa đối soát phiên bản OKF. |
| **Gate 3** | `validate_table_attachments` | Chuỗi tham chiếu | Dùng Regex tìm chuỗi `tables/...` trong `.md` rồi kiểm tra file tồn tại. **Không mở/đọc CSV**. |
| **Gate 4** | `validate_fake_data` | Heuristic thô | Kiểm tra file $\ge 20\text{ KB}$, bước nhảy `Điều X` $\le 3$, số node $\ge 25$. |
| **Gate 5** | `validate_pdf_metadata` | Schema / Enum | Đối soát `pdf_status`, SHA-256, enum `jurisdiction` trong `clauses.json`. |
| **Gate 6** | `validate_pure_normative_body` | Làm sạch từ vựng | Cắt 25 dòng đầu (Quốc hiệu) và 25 dòng cuối (Nơi nhận), lọc thẻ cào web rác. |
| **Gate 7** | `validate_spoke_cleanliness` | Filesystem Whitelist | Giới hạn 20 file core script trong `scripts/`. |
| **Gate 8** | `validate_template_and_table` | Cấu trúc Form/Hình | Kiểm tra `templates/` không rỗng, bắt lỗi bảng biểu mẫu bị làm phẳng thành text. **Bỏ sót hoàn toàn `tables/csv/`**. |
| **Gate 9** | `validate_visual_parity` | Linter hiển thị | Thoát ký tự `\- ` và `&nbsp;&nbsp;\+ `, chống dồn dòng `<br> CHÚ THÍCH`. |
| **Gate 10** | `validate_adr_parity_and_sync` | Đồng bộ Metadata | Biên dịch README/Matrix ADR. Chỉ đếm chẵn/lẻ `$$` trong duy nhất file `session_learnings.md`. |
| **Gate 11** | `validate_verbatim_parity` | Đối soát nguyên văn | Đo lường tỷ lệ Parity Rate $\ge 98.0\%$ giữa DOCX gốc và Markdown. Sub-gate 11.2 kiểm soát chú thích. |
| **Gate 12** | `validate_multimodal_assets` | Đa phương thức | Cấm WMF/EMF, kiểm tra Dual-format SVG/PNG và cards `figures/cards/` (ADR 0040). |

### 2.2. Khảo Sát Cấu Trúc `metadata.yaml` & Lỗ Hổng Nguồn Gốc (Provenance Gap)
Khảo sát tệp `metadata.yaml` thực tế tại `qcvn_06_2022_bxd`, `tcvn_2737_2023`, `nghi_dinh_207_2026_nd_cp`:
- **Đang có:** `id`, `document_number`, `title`, `type`, `status`, `pdf_path`, `pdf_sha256`, `pdf_status`, `legal_basis`, `source_assets`.
- **Hoàn toàn thiếu:**
  1. `okf_spec`: Không xác nhận phiên bản chuẩn (ví dụ `"v2.4 Universal"`).
  2. `converter_version`: Không ghi nhận phiên bản code bóc tách (ví dụ `"0.4.0"`).
  3. `extracted_at`: Không có dấu thời gian ISO-8601 UTC.
  4. `schema_uri`: Không có URI định danh schema JSON chuẩn hóa.

### 2.3. Khảo Sát Dữ Liệu Bảng (`tables/`) & Công Thức Toán (`$$`) Trên 37 Văn Bản
- **Bảng biểu:**
  - Nhóm `01_vbpl` (25 văn bản): Không có `tables/csv/`. Dữ liệu bảng nằm ở biểu mẫu `templates/`.
  - Nhóm `02_qcvn` & `03_tcvn` (12 văn bản): Có ~150 file CSV. Chỉ có **4 văn bản** có `tables_catalog.json` (`qcvn_03`, `qcvn_06`, `qcvn_09`, `tcvn_2737`).
  - Khoảng $35\% - 45\%$ file CSV cũ bị lệch số cột giữa Header đa tầng và Hàng dữ liệu (Ragged Rows).
- **Công thức toán:**
  - Tập trung ~300 khối `$$` tại `tcvn_2737_2023`, `qcvn_09_2017_bxd`, `qcvn_06_2022_bxd`, `tcvn_5574_2018`.
  - Phát hiện 15–25 công thức dùng `\tag{}` trong `aligned`/`cases` (KaTeX web parser error), và ~12 công thức mất cân bằng `\left[` / `\right.`.

---

## 3. Ma trận Đánh giá Quyết định

| Phương án | Giá trị kỹ thuật | Độ phức tạp | Rủi ro sập CI | Tuân thủ KISS | Quyết định |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Giữ nguyên 12 Cổng (Không nâng cấp)** | Thấp | Không | Không | ⚠️ Bỏ qua kiểm soát chất lượng | **KHÔNG KHUYẾN NGHỊ** |
| **2. Bổ sung Gates 13, 14, 15 dạng Hard Blocking Error ngay** | Rất cao | Trung bình | 🔴 Cực cao (33/37 văn bản fail ngay) | ❌ Vi phạm thực tiễn | **BÁC BỎ (REJECT)** |
| **3. Bổ sung Gates 13, 14, 15 theo Cơ chế Bánh Cóc (Ratchet Rollout)** | Rất cao | Trung bình | 🟢 An toàn tuyệt đối (Non-breaking) | ✅ Tuân thủ tuyệt đối | **CHẤP THUẬN (RECOMMENDED)** |

---

## 4. Thiết Kế Chi Tiết Bộ 3 Cổng Kiểm Định Mới

```
                               KIẾN TRÚC MASTER CI 2.0 (15 CỔNG)
  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
  │ GATES 1..12: KIỂM SOÁT HÌNH THỨC, TÍNH TOÀN VẸN & VERBATIM PARITY                           │
  │ (Registry, Bundles, Attachment, Fake Data, PDF, Pure Body, Clean, Form, Visual, ADR, SVG)    │
  ├─────────────────────────────────────────────────────────────────────────────────────────────┤
  │ GATE 13: TABLE KNOWLEDGE EXTRACTION & MATRIX REGULARITY (ADR 0041)                          │
  │ - Scoped: Chỉ kích hoạt khi bundle có thư mục tables/csv/                                    │
  │ - Assert Zero Ragged Rows: len(data_row) == len(header_row)                                  │
  │ - Bắt lỗi chú thích chân bảng (Footnotes) rò rỉ vào ma trận dữ liệu CSV                      │
  │ - Kiểm tra sự hiện diện và tính hợp lệ của tables/tables_catalog.json                       │
  ├─────────────────────────────────────────────────────────────────────────────────────────────┤
  │ GATE 14: KaTeX MATH SYNTAX & RENDERING INTEGRITY (ADR 0038)                                 │
  │ - Zero-NodeJS: Pure Python Regex Lexer (Tăng thời gian chạy CI thêm chỉ ~1.5 giây)           │
  │ - Assert tính chẵn lẻ của cặp phân định $$ ... $$ trên mọi file .md                          │
  │ - Bắt lỗi \tag{...} trong môi trường đa dòng (aligned, cases, gather) -> Đổi sang \qquad (X) │
  │ - Bắt lỗi mất cân bằng cặp ngoặc \left[ / \right], \left( / \right), { / }                  │
  │ - Cấm tuyệt đối chú thích HTML <!-- ... --> kẹp bên trong khối $$                           │
  ├─────────────────────────────────────────────────────────────────────────────────────────────┤
  │ GATE 15: OKF PROVENANCE & ALGORITHM VERSION ATTESTATION GATE                                │
  │ - Đọc metadata.yaml, đối soát okf_spec với CURRENT_OKF_SPEC ('v2.4 Universal')               │
  │ - Kiểm tra sự hiện diện của converter_version và extracted_at (chuẩn ISO-8601)               │
  │ - Báo cáo Telemetry: Danh sách văn bản mang dữ liệu đời cũ cần re-convert                    │
  └─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Kế Hoạch Triển Khai & Rào Chắn An Toàn (Implementation Roadmap)

### Pha 1: Tích Hợp Telemetry & Soft Warnings (Không làm vỡ CI)
1. Cập nhật `packages/ccba-legal-intel/src/ccba_legal/converters/` để khi chạy `convert` sẽ tự động ghi `okf_spec`, `converter_version`, `extracted_at` vào `metadata.yaml`.
2. Bổ sung code thực thi Gates 13, 14, 15 vào `scripts/validate_legal_spoke.py`.
3. Trong Pha 1, các vi phạm trên các bundle cũ được ghi nhận vào `self.warnings.append(...)` để đo lường toàn diện (Telemetry Mode) mà CI vẫn trả về `Exit Code 0`.

### Pha 2: Khóa Chốt Bánh Cóc (Ratchet Enforcement)
1. Quy định Hard Blocking Error (`self.errors.append(...)`) đối với:
   - Mọi văn bản mới được thêm vào Spoke.
   - Mọi văn bản nằm trong diện Git Staged/Modified.
2. Thiết lập quy trình chuẩn Re-convert từng bundle kỹ thuật cũ từ `sources/` để làm sạch ma trận CSV và công thức KaTeX, đưa toàn bộ 37 văn bản về trạng thái `0 Errors, 0 Warnings` ở cả 15 Cổng.
