---
request_id: "req-spoke-standardize-rfi-template-001"
verdict: "APPROVE_WITH_CONDITIONS"
risk_score: 3
conditions:
  - id: "COND-01"
    description: "Khóa hình học theo hằng số hiện hành trong resources/docx.md và standards/structure/docx-page-setup.md: A4 11906×16838 DXA, lề trái 1701 DXA (3 cm đóng gáy), lề phải 1134 DXA (2 cm), CONTENT_WIDTH = 9071 DXA. Lưới 4 cột và hai ô ký là bộ số nguyên công bố cạnh các hằng số đó, tổng đúng 9071. Cell padding khóa theo docx-table.md (0,1 cm trên/dưới, 0,15 cm trái/phải) quy về twip nguyên một lần. Bộ lề trái 2,5 cm / tổng 9355 DXA (755+3400+3400+1800 và 4677+4678) lệch chuẩn VB ngắn và lệch cả chiều rộng VB dài 9354 DXA."
    blocking: true
  - id: "COND-02"
    description: "Màu lấy đúng standards/color/docx-formal-navy.md: header #1F3864 trên chữ #FFFFFF, zebra lẻ #F2F2F2, zebra chẵn #FFFFFF, accent #C00000 cho heading cấp 1 và điểm mấu chốt, dòng phụ đề tiếng Anh dùng Secondary #595959. Banner #D9E6F2 và zebra #F4F6F9 chỉ nhập palette sau khi được ghi thành token có tên trong chính file formal-navy."
    blocking: true
  - id: "COND-03"
    description: "Cổng hình học là test của package sở hữu template, khẳng định pgMar, tổng tblGrid, padding, mã màu, cantSplit và tblHeader. DOCXSchemaValidator giữ vai trò XML hợp lệ ISO/IEC 29500; XSD chấp nhận mọi pgMar hợp lệ nên không thay assertion token. scripts/validate_legal_spoke.py giữ 15 cổng OKF của kho quy phạm."
    blocking: true
  - id: "COND-04"
    description: "Renderer đi qua seam ooxml_processor.v1 và WordFormFiller (template read-only, TemplateProtectionError) đã mô tả trong resources/form-filling.md. Mặt mô tả mẫu nằm ở Tầng 4: templates/docx-rfi-ky-thuat.md. Lệnh /ccba-xu-ly-van-phong --template rfi-ky-thuat trỏ về API đó. Gói packages/ccba-ooxml và QuestionnaireData không có trong cây spoke này; renderer đóng trên Hub qua /ccba-contribute-to-hub. Spoke không thêm module ccba_ooxml.rfi, không thêm .md/tools/compile_rfi.py, không thêm script python-docx trong scratch/."
    blocking: true
  - id: "COND-05"
    description: "Nguồn biên dịch là YAML: masthead, danh sách block prose | table(profile rfi-4col-response-grid) | signoff. Bốn cột là profile của từng bảng vì phần mục đích, tiến độ và xác nhận bàn giao là đoạn văn; header cột 4 là dữ liệu từng phần. Markdown GFM là bản đọc. Liên kết giao Nhà máy là số hiệu QCVN/TCVN, không phải đường dẫn file:// nội bộ spoke."
    blocking: true
  - id: "COND-06"
    description: "Spacing cố định của VB ngắn: line 1.4 (340 twentieths), space after 6–7 pt. Hàng dữ liệu mang w:cantSplit. Hàng tiêu đề mang tblHeader. Khối ký là một bảng không tách; pageBreakBefore khi phần thân còn lại thấp hơn chiều cao khối ký đã đo và lưu thành hằng số. Tên, chức danh, điện thoại, email là slot; dữ liệu người thật theo Cascading Vault ADR-0059; fixture commit dùng placeholder."
    blocking: true
effort: "M"
summary: "Tách nội dung khỏi token là bước đúng và đủ nhỏ. Thông qua khung 4 cấp sau khi hình học bám CONTENT_WIDTH 9071, màu bám formal-navy, IR là YAML, renderer là WordFormFiller trên Hub, và cổng hình học nằm ngoài validate_legal_spoke.py."
---

# Phản biện kiến trúc — Khuôn mẫu RFI / Design Brief

**Phán quyết:** `APPROVE_WITH_CONDITIONS`  
**Rủi ro:** 3/5  
**Hồ sơ:** `req-spoke-standardize-rfi-template-001`  
**Người phản biện:** Grok (Adversarial Auditor)  
**Ngày:** 2026-10-22

Chẩn đoán Format Drift là đúng. Hai phiếu PCCC và PAPVN lệch lề, lệch lưới cột, lệch padding và lệch khối ký vì mỗi lần sinh file là một script `docx` riêng trong `scratch/`, trong khi Tầng 4 của `ccba-xu-ly-van-phong` chưa có mẫu RFI. Khung bốn cấp (dữ liệu, token, một renderer, một cổng) khớp nguyên lý Platform-Aware KISS. Phần cần sửa trước khi thi công là các hằng số và chỗ đặt mã: đề xuất đang tạo một chiều rộng mới, một palette mới, một module mới và một cổng CI nằm nhầm spoke.

## 1. Bằng chứng đã đối chiếu

Đã đọc các tệp được dẫn, trừ đường dẫn package vì cây spoke không chứa chúng.

| Nguồn đã mở | Kết quả |
|---|---|
| `standards/structure/docx-page-setup.md` | VB ngắn: trái **3 cm**, phải 2 cm. Content width `11906 − 1701 − 1134 = 9071` DXA. VB dài: phải 1,5 cm, width **9354** DXA, lề trái vẫn 3 cm. |
| `resources/docx.md` | `MARGIN_LEFT = 1701`, `MARGIN_RIGHT = 1134`, `CONTENT_WIDTH = 9071`. Quy tắc bảng: tổng `columnWidths` bằng `CONTENT_WIDTH`. |
| `standards/color/docx-formal-navy.md` | Header `#1F3864` / `#FFFFFF`. Zebra lẻ `#F2F2F2`. Accent `#C00000` cho H1 và điểm mấu chốt. Subtitle / caption là `#595959`. |
| `standards/structure/docx-table.md` | Padding chuẩn 0,1 cm trên/dưới, 0,15 cm trái/phải. Zebra từ 5 dòng. Cột số canh phải hoặc giữa, cột chữ canh trái. |
| `resources/form-filling.md` | `WordFormFiller` + `FormFillConfig(read_only_template=True, prevent_row_split=True)` + `page_break_keywords`. OpenXML: `w:cantSplit`, `page_break_before`. PII theo ADR-0059, vault xếp tầng, không commit hồ sơ người thật. |
| `SKILL.md` | Posture `package-bound`, seam `ooxml_processor.v1`, `package_path: packages/ccba-ooxml`. Tầng 4 là chỗ đặt template. |
| `packages/ccba-ooxml/.../questionnaire/models.py` | **Không có** trong workspace. `packages/` không tồn tại trên spoke này. |
| Hai phiếu `.md/reports/20261022_phieu_yeu_cau_*.md` | Cùng họ 4 cột ở các phần bảng, và có các phần thuần văn (mục đích, tiến độ, xác nhận). Ô dùng `<br>`, checkbox chữ, công thức, và liên kết `file://` tới bundle nội bộ. |

`11906 − 1417 − 1134 = 9355` chỉ đúng khi lề trái bị hạ xuống 1417 twip. 2,5 cm = 1417,32 twip; quy đổi nội bộ của skill (1 cm = 567 DXA) cho 2,5 cm = 1417,5 — không phải số nguyên. 755+3400+3400+1800 = 9355 và 4677+4678 = 9355 khớp nhau, và cả hai lệch `CONTENT_WIDTH` đang được skill coi là bất biến. Chiều rộng 9354 của VB dài cũng là một cạnh khác: cạnh phải thu còn 1,5 cm, cạnh trái giữ 3 cm để đóng gáy. Phiếu RFI in ra để kẹp hồ sơ nhà máy thuộc nhóm VB ngắn.

Tỷ lệ 8,1% + 36,3% + 36,3% + 19,2% = 99,9%. Bất biến cần khóa là tổng DXA nguyên, cùng kiểu với quy tắc `columnWidths` trong `resources/docx.md`.

Padding 55/90 DXA và 40/80 DXA trong phân tích gốc rễ đều chưa trùng 0,1 cm / 0,15 cm của `docx-table.md`. Cấp 2 của đề xuất khóa lề và lưới, còn padding — đúng thông số đã trôi — chưa có token.

## 2. Bốn câu hỏi

### 2.1. KISS và tính tất yếu

Tách nội dung khỏi định dạng là bước tất yếu, và đủ nhỏ. Skill đã trả tiền cho các token này: 9071 DXA, Formal Navy, mẫu bảng T3, và layout guard của `WordFormFiller`. Hai phiếu lệch nhau vì script tạm không đọc các token đó.

Phần vượt nhu cầu của hai phiếu là bốn hạng mục đi kèm:

- Một chiều rộng trang mới (9355) cạnh 9071 và 9354.
- Một module public `ccba_ooxml.rfi` trong khi seam điền form và chống xé hàng đã có.
- Một parser GFM tự do cho bảng song ngữ, checkbox, HTML và KaTeX.
- Một cổng mới trong `validate_legal_spoke.py`, vốn là 15 cổng OKF của kho quy phạm (ADR vận hành spoke: spoke này đóng gói bundle Markdown, không ôm code ứng dụng văn phòng).

Giữ bốn cấp. Điền mỗi cấp bằng hiện vật đang có.

### 2.2. Hub và Spoke

Phương án đúng là **C đã thu hẹp**.

- **Trên spoke, ngay:** một tệp Tầng 4 `templates/docx-rfi-ky-thuat.md` trích nguyên hằng số trang, màu, padding và luật `cantSplit` / `pageBreakBefore`. Tệp này là hợp đồng cho agent, không chứa bộ số thứ hai.
- **Trên Hub:** template DOCX read-only, schema YAML, và test hình học nằm trong `ccba-ooxml`, đi theo `/ccba-contribute-to-hub`. `WordFormFiller.export` đã có nhánh DOCX và PDF; cờ PDF gắn vào export đó.
- **Phương án A** (`.md/tools/compile_rfi.py` viết bằng python-docx) là cùng một lớp script với `scratch/` đã sinh ra hai phiếu lệch. Seam của skill cấm import `docx` thay thế và buộc đi qua API `ccba-ooxml`.
- **Phương án B** không thực thi được bằng một commit trong repo này: `packages/ccba-ooxml` không có mặt, `QuestionnaireData` không kiểm chứng được tại đường dẫn đã dẫn. Vendoring cả package vào spoke pháp lý phá vách ADR-0009 và bất biến “không chứa code ứng dụng” của spoke.

Cho đến khi PR Hub vào, agent dừng sinh DOCX RFI bằng script tạm. Nguồn YAML và bản mô tả template vẫn soạn được trên spoke.

### 2.3. Markdown và YAML

Nguồn biên dịch là **YAML có schema**, cùng hướng với dữ liệu mà `WordFormFiller` đang nạp. Hình dạng tài liệu:

- `masthead`: mã phiếu, dự án, địa điểm, ngày, đơn vị hai bên.
- `blocks[]`: `prose`, hoặc `table` với `profile: rfi-4col-response-grid`, hoặc `signoff`.
- Mỗi bảng mang header riêng. Cột 4 của hai phiếu đổi nhãn theo phần (“Tình trạng cung cấp”, “Ghi chú của Nhà máy”, “Phản hồi”). Vai trò cột cố định; chuỗi tiêu đề là dữ liệu.
- Ô là danh sách đoạn và checkbox chữ `[ ]` / `[X]`. V1 dùng ký tự checkbox trong token, chưa cần content control SDT.

Bốn cột áp vào **từng bảng**, không áp vào cả tệp. PHẦN mục đích, mục tiến độ và mục xác nhận bàn giao trong hai phiếu hiện là đoạn văn. Ép chúng vào lưới 4 cột tạo bảng một cột — điều `docx-table.md` cấm.

Markdown GFM giữ vai trò bản đọc cho người. Làm parser đầu vào sẽ mở một ngữ pháp thứ hai. Hai phiếu đang thể hiện các điểm vỡ của ngữ pháp đó: `<br>` trong ô, công thức đã hỏng ký tự ở phiếu PAPVN, và liên kết `file://` tuyệt đối tới bundle QCVN trên máy spoke. Bản giao Nhà máy mang số hiệu văn bản (QCVN 06:2022/BXD, QCVN 10:2025/BCA, QCVN 02:2020/BCA). Đường dẫn spoke là trợ giúp lúc soạn thảo.

### 2.4. Trang mồ côi của khối ký

Spacing là token cố định của VB ngắn: line 1.4 (340 twentieths), space after 6–7 pt, theo `docx-page-setup.md`. Thu hẹp line spacing hoặc lề theo từng phiếu là đúng cơ chế đã làm RFI-01 và RFI-02 khác nhau.

Ba chốt đã có trong `form-filling.md`:

1. `w:cantSplit` trên mọi hàng dữ liệu (`prevent_row_split`).
2. `tblHeader` trên hàng tiêu đề để trang 2–4 của phiếu 3–4 trang vẫn còn tên cột.
3. `pageBreakBefore` trên heading khối ký khi phần thân còn lại thấp hơn chiều cao khối ký. Chiều cao đó đo một lần trên template và lưu cạnh các hằng số DXA. `page_break_keywords` của `WordFormFiller` là chỗ gắn việc này.

Khối ký là một bảng hai ô, tổng bằng 9071, phần dư 1 DXA (nếu tổng lẻ) dồn về ô phải. Hai bên là slot: tổ chức, chức danh, họ tên. Mẫu đề xuất gắn sẵn một cá nhân vào ô trái sẽ lệch các phiếu có đầu mối khác — phiếu PAPVN đã có nhiều PIC. Điện thoại và email đi theo Cascading Vault ADR-0059; fixture đưa lên git dùng placeholder.

Hàng song ngữ rất cao tạo khoảng trống cuối trang. Đó là kết quả đúng của `cantSplit`. Trần của một hàng xử lý bằng cỡ chữ dòng tiếng Anh (Secondary, nhỏ hơn dòng Việt) và bằng ngân sách nội dung trong schema, không bằng cách nén lề.

## 3. Điều kiện chặn

Sáu điều kiện `COND-01` … `COND-06` trong frontmatter đều `blocking: true`. Thi công renderer bắt đầu khi các hằng số, chỗ đặt test, và schema block đã theo các điều kiện đó.

Việc làm được song song, không đụng hình học mới:

1. Thêm `templates/docx-rfi-ky-thuat.md` trích 9071 DXA, Formal Navy, padding `docx-table.md`, và luật khối ký của `form-filling.md`.
2. Chuyển hai phiếu hiện tại sang YAML fixture, placeholder cho dữ liệu cá nhân, số hiệu QCVN thay cho `file://`.
3. Mở PR Hub: profile `rfi-4col-response-grid` trên `WordFormFiller`, một template read-only, một test tổng `tblGrid`.

Xong sáu điều kiện, mọi phiếu RFI mới có một người viết hình học. Lệch lề hoặc lệch tổng cột fail ở test package, trước khi file tới Nhà máy.