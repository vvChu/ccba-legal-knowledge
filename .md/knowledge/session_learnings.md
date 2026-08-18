# 🧠 CCBA Legal Knowledge Spoke — Session Learnings & Knowledge Base

> **Mục đích:** Tài liệu lưu trữ các bài học kinh nghiệm (*Learnings*), mẫu hình kiến trúc (*Architectural Patterns*), giải pháp xử lý dữ liệu và tiêu chuẩn vàng (*Gold Standards*) được đúc kết qua các phiên làm việc với AI Agent trên Spoke `ccba-legal-knowledge`.

---

## 1. Mẫu Hình Xử Lý Bảng Biểu Kỹ Thuật (Table Grid & Footnote Patterns)

### A. Chuẩn Hóa Lưới Bảng 2D GFM (2D Pipe Table Normalization)
- **Vấn đề:** Khi bóc tách từ Word/DOCX chứa các ô merge hoặc header nhiều tầng, nếu xuất thành plain text dễ bị dính chuỗi `||` trên một dòng hoặc nhân bản chữ.
- **Giải pháp chuẩn hóa:**
  1. Mỗi hàng của bảng bắt buộc phải kết thúc bằng ký tự xuống dòng `\n`.
  2. Phải có dòng trống `\n\n` phía trước và phía sau bảng để trình render Markdown (như VS Code Preview, GitHub) nhận diện đúng cú pháp bảng HTML 2D.
  3. Tách toàn bộ các Chú thích chân bảng ra khỏi thân lưới bảng, đưa xuống dưới dạng văn bản độc lập.

### B. Xử Lý Chỉ Số Phụ Tham Chiếu (Superscript Footnote References)
- **Vấn đề:** Các số chỉ số phụ trong Word (như $100^{1)}$, $85^{1)}$, $1400^{2),3)}$) khi chuyển sang plain text bị dính liền thành `1001)`, `851)`, `14002),3)` $\rightarrow$ Con người và AI dễ đọc nhầm thành con số $1.001\text{ mm}$ (sai gấp 10 lần!).
- **Giải pháp chuẩn hóa:**
  1. Chuyển đổi thành thẻ HTML chuẩn: `100 <sup>1)</sup>`, `85 <sup>1)</sup>`, `thạch cao <sup>1)</sup>`.
  2. Trong AST JSON (`tables/json/*.json`): Phân tách mảng nguyên tử `numeric_value: 100`, `unit: "mm"`, `superscript_refs: [1]` theo **ADR 0004**.

### C. Phân Loại Cấu Trúc Chú Thích Chân Bảng (Footnote Taxonomy)
- Tách rạch ròi 2 nhóm:
  - `_CHÚ THÍCH:_` (Quy định chung cho toàn bảng).
  - `_GHI CHÚ CHỈ SỐ PHỤ:_` (Ghi chú giải nghĩa điều kiện riêng cho từng ô `1)`, `2)`...).

---

## 2. Mẫu Hình Định Dạng Thân Điều Khoản & Thẻ Neo Canonical

### A. Inlined Semantic Anchors
- **Vấn đề:** Đặt thẻ neo `<a id="..."></a>` trên dòng riêng biệt trước tiêu đề khiến trình xem Markdown tính toán sai tọa độ cuộn (bị che khuất phía trên).
- **Giải pháp chuẩn hóa:**
  Nhúng trực tiếp thẻ neo vào dòng tiêu đề Markdown:
  ```markdown
  ### <a id="muc-1-1-2" name="muc-1-1-2"></a>1.1.2  Quy chuẩn này áp dụng đối với các nhà và công trình sau:
  ```

### B. Chú Thích Đơn Lẻ Trong Điều Khoản (Single Clause Notes)
- Khi điều khoản chỉ có 1 chú thích đơn lẻ $\rightarrow$ Trình bày thành một đoạn văn in nghiêng duy nhất:
  ```markdown
  _CHÚ THÍCH: Trường hợp chuyển đổi nhà ở riêng lẻ sang mục đích khác thì phải tuân thủ..._
  ```
  *(Tuyệt đối không sinh thêm dòng tiêu đề `_CHÚ THÍCH:_` và gạch đầu dòng `- **CHÚ THÍCH:**` gây lặp từ).*

### C. Mục Lục Đầu Trang (Clean Table of Contents)
- Phần Mục lục ở đầu tài liệu phải là danh sách liên kết Markdown `[Tên Chương / Phụ lục](#anchor)` nằm dưới `## MỤC LỤC`, không sử dụng các thẻ tiêu đề giả (`## PHỤ LỤC...`) làm cướp thẻ neo của nội dung thực tế.

---

## 3. Hệ Thống 9 Quyết Định Kiến Trúc Đã Xác Lập (ADR Index)

1. **ADR 0001:** Dual-Track VBHN Provenance (Bản gốc 2022 + Sửa đổi 1:2023 + VBHN 2023 có nhúng Callout).
2. **ADR 0002:** Structured Table Footnote Binding Matrix.
3. **ADR 0003:** Annex Normative Guardrails (Mandatory vs Informative).
4. **ADR 0004:** Structured Array Pointer Binding cho Chỉ số phụ Đa tầng.
5. **ADR 0005:** Semantic Legal URI Scheme (`legal://[doc_id]#[clause_id]`) & Registry URL Router.
6. **ADR 0006:** Legal Precedence Hierarchy (`Luật > NĐ 217/2026 > QCVN > TCVN`) & Phân loại Defect.
7. **ADR 0007:** Dual-Layer CI Verification Gate (Pre-commit Hook + GitHub Actions).
8. **ADR 0008:** Temporal Legal Query Engine & Point-in-Time Auditing (Time-Travel RAG).
9. **ADR 0009:** Phân phối SDK dùng chung `ccba-legal-sdk` trên Hub.

---

## 4. Rào Chắn Kiểm Toán Tự Động (Quality Gates)

Mọi đóng góp dữ liệu mới vào Spoke bắt buộc phải chạy và vượt qua 3 script kiểm toán với `0 Errors, 0 Warnings, 100% Parity`:
```bash
python scripts/validate_legal_spoke.py
python scripts/verify_knowledge_integrity.py
python scripts/verify_cross_links.py
```
