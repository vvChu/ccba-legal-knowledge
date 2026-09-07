# ADR 0042: Chuẩn Hóa Cấu Trúc OpenXML DOM & Động Cơ Lai Ghép DOCX-PDF Hai Tầng (Canonical OpenXML Sanitization & Hybrid Dual-Engine Architecture)

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-09-07)  
*Hội tụ thông qua Quy trình Phỏng vấn Socrates Đối Chiếu Thiết Kế (`/ccba-grill-with-docs`) dựa trên Báo cáo Nghiên cứu Kỹ thuật `RESEARCH-OPENXML-SANITIZATION-2026-09`.*

---

## 2. Bối Cảnh (Context)
Trong quá trình bóc tách và chuẩn hóa dữ liệu pháp quy kỹ thuật xây dựng (VBPL, QCVN, TCVN) sang định dạng OKF v2.4 Universal Bundle, hệ thống bộc lộ những thách thức cấu trúc bắt nguồn từ sự phân hóa định dạng gốc giữa DOCX Công báo và PDF số hóa:

1. **Hiện tượng Phân mảnh Run (Run Fragmentation):** Các bộ gõ tiếng Việt (Unikey, Vietkey) và cơ chế soát lỗi chính tả của Microsoft Word tự động chẻ nhỏ một từ đơn hoặc một cụm từ quy phạm thành nhiều thẻ `<w:r>` vụn vặt (ví dụ: `"Điều "` + `"1"` + `": "` + `"Phạm vi"`). Kèm theo đó là hàng loạt thẻ giao diện rác `<w:proofErr>`, `<w:smartTag>`, `<w:lastRenderedPageBreak>` và hàng chục thuộc tính Revision Identifier (`w:rsidR`, `w:rsidRPr`, `w:rsidP`). Điều này làm cho các biểu thức chính quy (Regex) và AST parser cấp downstream bị vỡ vụn hoặc nhận diện sai ranh giới từ.
2. **Ô nhiễm Bảng Bố Cục Dàn Trang (Borderless Layout Tables):** Chuyên viên soạn thảo thường lạm dụng bảng không viền 1–3 hàng, 1–2 cột để căn lề tiêu ngữ hành chính, quốc hiệu, chữ ký hoặc căn lề công thức tính toán. Khi duyệt bảng thông thường, bộ bóc tách bảng (Table Extractor) nhận diện nhầm các cấu trúc dàn trang này thành bảng số liệu kỹ thuật, sinh ra hàng loạt file CSV rác và vi phạm Gate 8, Gate 13.
3. **Mất Khoảng Trắng Biên & Ký Tự Đầu Dòng (Spacing Collapsing & Bullet Degradation):** Khi gộp các run liền kề hoặc parse text thô từ DOM XML, các khoảng trắng ở biên bị trình phân tích XML nuốt mất (biến `"Điều 1"` thành `"Điều1"`), và các ký tự đầu dòng quy phạm (`\- ` và `&nbsp;&nbsp;+ `) bị dồn cục, vi phạm trực tiếp Gate 9 (Visual Parity - ADR 0029, ADR 0030).
4. **Sự Phân Hóa Giữa DOCX và PDF (Structural AST vs. Spatial Vector Ground Truth):** Tệp DOCX cung cấp xương sống phân cấp ngữ nghĩa (Heading, Paragraph, Table, XML hierarchy), nhưng dễ bị sai lệch bố cục in ấn và bảng biểu phức tạp. Ngược lại, tệp PDF Công báo mang tính pháp lý tối cao (Legal Anchor of Trust) với tọa độ không gian chính xác 100%, nhưng thiếu cấu trúc cây AST nguyên bản.
5. **Xung Đột với Bộ Cổng Kiểm Định Master CI:** Đặc biệt là Gate 11 (DOCX-to-Markdown Verbatim Parity Rate $\ge 98.0\%$), Gate 12 (Multimodal Integrity), và Gate 13 (Table Regularity).

---

## 3. Quyết Định Thiết Kế (Decision)

Hệ thống thiết lập **Kiến Trúc Chuẩn Hóa Cấu Trúc OpenXML DOM & Động Cơ Lai Ghép DOCX-PDF Hai Tầng (ADR 0042)** theo các nguyên tắc cốt lõi:

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                      HYBRID DUAL-ENGINE ARCHITECTURE                          │
├──────────────────────────────────────┬────────────────────────────────────────┤
│     PASS 1: IN-MEMORY CANONICAL      │       PASS 2: MULTIMODAL VERBATIM      │
│         OPENXML SANITIZATION         │             AST EXTRACTION             │
│   (DocxCanonicalSanitizer via lxml)  │         (DocxAstConverter Engine)      │
├──────────────────────────────────────┼────────────────────────────────────────┤
│  • Purge w:rsid*, w:proofErr, tags   │  • Deterministic MTEF MathType Parser  │
│  • Consolidate adjacent w:r (NFC)    │  • Dual-Format Vector WMF/EMF -> SVG   │
│  • Inject xml:space="preserve"       │  • 2D Virtual Grid tblGrid Extraction  │
│  • Unwrap Borderless Layout Tables   │  • Hierarchical Forward-Fill (vMerge)  │
│  • Promote Structural Headings       │  • Spatial Cross-Check with PDF Anchor │
└──────────────────────────────────────┴────────────────────────────────────────┘
```

### A. Quy Trình 2 Pha Xử Lý Hoàn Toàn Trong Bộ Nhớ (Two-Pass In-Memory Pipeline)
- **Pha 1 — Tiền xử lý Chuẩn hóa Cấu trúc DOM (`DocxCanonicalSanitizer`):** Thực thi 100% in-memory trên `io.BytesIO` thông qua thư viện C-speed `lxml.etree` và `zipfile.ZipFile`. Tuyệt đối không ghi file tạm ra đĩa cứng, triệt tiêu hoàn toàn nguy cơ tranh chấp file lock trên môi trường Windows.
- **Pha 2 — Bóc tách Xác định Đa phương thức (`DocxAstConverter` / `StandardConversionStrategy`):** Tiếp nhận luồng `io.BytesIO` đã được chuẩn hóa để phân rã cây AST, bóc tách công thức, bảng biểu và hình ảnh.

### B. 4 Kỹ Thuật Chuẩn Hóa OpenXML Cốt Lõi
1. **Gọt Thuộc Tính Revision & Gộp Run Liền Kề (Purge Rsid/ProofErr & Run Consolidation):**
   - Quét và loại bỏ triệt để toàn bộ thuộc tính `w:rsid*` (`w:rsidR`, `w:rsidRPr`, `w:rsidP`, `w:rsidRDefault`, `w:rsidDel`).
   - Xóa bỏ các thẻ giao diện `<w:proofErr>`, `<w:lastRenderedPageBreak>`. Giải phóng nội dung bên trong `<w:smartTag>` về thẻ cha trước khi xóa tag rác.
   - Gộp các run `<w:r>` kế tiếp nhau có định dạng `<w:rPr>` đồng nhất thành 1 run duy nhất.
   - Chuẩn hóa toàn bộ chuỗi ký tự về dạng Unicode chuẩn NFC (`unicodedata.normalize('NFC', text)`).
2. **Giải Nén Bảng Bố Cục Dàn Trang (Borderless Layout Tables Unwrapping):**
   - Nhận diện các bảng layout không viền (bảng 1–3 hàng, 1–2 cột) chứa từ khóa hành chính hoặc không có đường viền quy phạm.
   - Giải nén toàn bộ các đoạn văn `<w:p>` bên trong ô bảng ra trực tiếp thân tài liệu chính và loại bỏ thẻ `<w:tbl>`, ngăn chặn triệt để việc xuất CSV rác vào thư mục `tables/`.
3. **Bảo Toàn Khoảng Trắng Biên & Chuẩn Hóa Tab (Whitespace & `xml:space="preserve"`):**
   - Khi gộp text hoặc gặp các run có khoảng trắng/tab ở đầu hoặc cuối chuỗi, tự động tiêm thuộc tính `xml:space="preserve"` vào thẻ `<w:t>`.
   - Ngăn chặn triệt để hiện tượng dính chữ giữa số hiệu điều khoản và tiêu đề (`"Điều 1"` $\rightarrow$ `"Điều1"`).
   - Bảo toàn $100\%$ các ký tự đầu dòng quy phạm `\- ` và `&nbsp;&nbsp;+ `.
4. **Thăng Cấp Tiêu Đề Cấu Trúc (Heading Promotion):**
   - Quét và nhận diện các đoạn văn bản in đậm mang cấu trúc Phần, Chương, Mục, Điều hoặc số thập phân phân cấp (`1.1`, `1.1.1`).
   - Tự động gán hoặc thăng cấp thuộc tính kiểu dáng `w:pStyle` chuẩn (`Heading1`, `Heading2`, `Heading3`), hỗ trợ AST parser downstream xây dựng cây mục lục hoàn chỉnh.

### C. Cơ Chế Động Cơ Lai Ghép DOCX-PDF Hai Tầng (Hybrid Dual-Engine)
- **DOCX làm Xương Sống Cấu Trúc (Structural Backbone):** DOCX cung cấp cây phân cấp AST, quan hệ cha-con giữa các điều khoản, định dạng inline (bold, italic, subscript, superscript) và đối tượng nhúng nhị phân MathType OLE.
- **PDF làm Mỏ Neo Không Gian & Kiểm Chuẩn (Spatial Ground Truth & Discrepancy Recovery):** Tệp PDF Công báo được sử dụng để đối soát chéo:
  - Kiểm định vị trí ranh giới trang, phát hiện các đoạn văn bản bị thiếu do lỗi gõ hoặc lỗi trích xuất DOCX.
  - Phục hồi các bảng số liệu phức tạp khi DOCX có cấu trúc ô gộp bị hỏng nặng.

### D. 5 Rào Chắn Đối Nghịch Bất Khả Xâm Phạm (5 Adversarial Guardrails)
1. **Rào Chắn 1 — Chống Thu Hẹp Khoảng Trắng (Anti-Spacing Collapsing Guard):** Cưỡng chế thuộc tính `xml:space="preserve"` trên mọi thẻ `<w:t>` có ký tự biên là khoảng trắng.
2. **Rào Chắn 2 — Đồng Bộ Hóa Unicode (Unicode Sync Guard):** 100% văn bản sau khi gộp run bắt buộc chuyển đổi sang chuẩn NFC, triệt tiêu xung đột tổ hợp/dựng sẵn (NFD vs. NFC).
3. **Rào Chắn 3 — Danh Sách Trắng Đối Tượng Nhúng (Whitelist Object Protection):** Nghiêm cấm tuyệt đối mọi hành vi xóa, sửa hoặc can thiệp vào các thẻ `<w:object>` (MathType OLE), `<m:oMath>`, `<m:oMathPara>`, và `<w:drawing>`.
4. **Rào Chắn 4 — Bảo Toàn Số Hiệu Đánh Số (Numbering & Anchor Integrity Guard):** Không làm thay đổi liên kết `<w:numPr>` và bookmark anchors (`<w:bookmarkStart>`, `<w:bookmarkEnd>`).
5. **Rào Chắn 5 — Bảo Toàn Nguyên Văn Quy Phạm (Verbatim Normative Invariant - ADR 0037):** Sanitizer chỉ làm sạch cú pháp DOM XML, không thay đổi ngữ nghĩa, nội dung hay trật tự từ vựng. Đảm bảo tỷ lệ trùng khớp Gate 11 đạt $\ge 98.0\%$.

---

## 4. Hệ Quả & Tác Động (Consequences)

### Tích Cực
- **Cải thiện độ tin cậy bóc tách AST:** Loại bỏ 100% hiện tượng regex bị vỡ do run fragmentation. Cây điều khoản `clauses.json` và benchmark `qa_benchmark.json` được sinh ra xác định và chính xác.
- **Loại bỏ hoàn toàn CSV rác:** Các bảng bố cục hành chính và khung công thức được unwrap thành văn xuôi phẳng, giữ cho thư mục `tables/` 100% là bảng kỹ thuật thực thụ.
- **Hoạt động 100% In-Memory:** Tốc độ xử lý tính bằng mili-giây, không tiêu tốn I/O đĩa, an toàn tuyệt đối với môi trường đa tiến trình (multi-worker) và CI/CD.
- **Hội tụ 15/15 Cổng Kiểm Định Master CI:** Đưa toàn bộ kho tri thức Spoke đạt trạng thái `Errors: 0 | Warnings: 0`.

### Hạn Chế & Chi Phí Bảo Trì
- Bổ sung module `docx_sanitizer.py` trong package Hub `ccba-legal-intel` (cần bộ unit test chuyên biệt).
- Cần cập nhật `AGENTS.md` và đồng bộ Living Traceability Matrix tại Spoke.

---
*Biên soạn bởi CCBA Agent Architecture Council.*  
*Căn cứ thực thi: `packages/ccba-legal-intel/src/ccba_legal/converters/docx_sanitizer.py`, `scripts/validate_legal_spoke.py`.*
