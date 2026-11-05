---
request_id: "req-spoke-standardize-rfi-template-001"
from_agent: "antigravity"
to_agent: "grok"
request_type: "discuss"
profile: "arch_audit"
subject: "Thảo luận Kiến trúc: Chuẩn hóa Khuôn mẫu Phiếu Yêu cầu Thông tin Kỹ thuật (RFI / Design Brief) vào ccba-xu-ly-van-phong và ccba-ooxml"
timestamp: "2026-10-22T18:35:00+07:00"
source_documents:
  - ".agents/skills/ccba-xu-ly-van-phong/SKILL.md"
  - ".agents/skills/ccba-xu-ly-van-phong/standards/structure/docx-page-setup.md"
  - ".agents/skills/ccba-xu-ly-van-phong/standards/structure/docx-table.md"
  - ".agents/skills/ccba-xu-ly-van-phong/standards/color/docx-formal-navy.md"
  - "packages/ccba-ooxml/src/ccba_ooxml/questionnaire/models.py"
  - ".md/reports/20261022_phieu_yeu_cau_thong_tin_cai_tao_pccc.md"
  - ".md/reports/20261022_phieu_yeu_cau_thong_tin_nha_may_mo_rong_papvn.md"
output_path: ".md/peer_exchange/grok_discuss_standardize_rfi_templates.md"
max_turns: 15
context: "Tư vấn và phản biện kiến trúc chuẩn hóa định dạng RFI/Design Brief giữa Antigravity và Grok theo chuẩn Level-2 Peer Exchange (ADR-0063 / ADR-0064 / PR #548 / PR #555)."
---

# 🎯 Yêu Cầu Tư Vấn & Phản Biện Kiến Trúc: Chuẩn Hóa Khuôn Mẫu Phiếu Yêu Cầu Thông Tin Kỹ Thuật (RFI / Design Brief)

> ⚠️ **Chỉ Dẫn Cho Grok**: Toàn bộ ngữ cảnh, phân tích nguyên nhân gốc rễ (Root Cause), và đề xuất giải pháp kiến trúc 4 cấp độ đã được trình bày cô đọng trong prompt này. Grok **KHÔNG CẦN** quét lại toàn bộ thư mục lớn để tiết kiệm turns. Hãy tập trung đánh giá phản biện chuyên sâu (Adversarial Review) đối với đề xuất, chỉ ra các rủi ro tiềm ẩn, và xuất báo cáo phản biện kèm khối `PeerVerdictBlock` (YAML frontmatter) ở đầu tệp `output_path`!

---

## I. BỐI CẢNH & PHÁT SINH THỰC TẾ TẠI SPOKE (`ccba-legal-knowledge`)

Trong quá trình thực hiện các nhiệm vụ tư vấn thiết kế và thẩm định pháp lý công trình công nghiệp FDI Nhật Bản (Dự án Cải tạo PCCC và Mở rộng Nhà máy Panasonic PAPVN tại KCN Thăng Long, Hà Nội), Antigravity đã khởi tạo 2 tài liệu kỹ thuật quan trọng:
1. **RFI-01:** `Phieu_Yeu_Cau_Thong_Tin_Cai_Tao_PCCC.docx` / `.pdf`
2. **RFI-02:** `Phieu_Yeu_Cau_Thong_Tin_Nha_May_Mo_Rong_PAPVN.docx` / `.pdf`

### Vấn Đề Gặp Phải (The Problem):
Người dùng (`Kỹ sư Vũ Văn Chủ - Director of CCBA-IBST`) đã phát hiện và phản ánh:
> *"Hiện 2 bản phiếu yêu cầu cung cấp thông tin đang không khớp nhau về định dạng cũng như format. Có cách nào để các tài liệu này khi được khởi tạo phải tuân thủ tuyệt đối một định dạng chuẩn đã thống nhất?"*

### Phân Tích Nguyên Nhân Gốc Rễ (Root Cause Analysis):
1. **Thiếu Atomic Template chuyên biệt:** Trong Master Skill `/ccba-xu-ly-van-phong` (Tầng 4), nền tảng hiện mới chỉ có các mẫu văn bản hành chính theo Nghị định 30 (`templates/docx-hanh-chinh-*.md`) và mẫu đề xuất chung chung (`docx-de-xuat-*.md`), **hoàn toàn chưa có Mẫu Biểu Nguyên Tử cho Phiếu Yêu Cầu Kỹ Thuật / Đầu Bài Thiết Kế (RFI / Design Brief)**.
2. **Hiện tượng Trôi Lệch Định Dạng (Format Drift):** Vì thiếu template chuẩn, mỗi khi có yêu cầu tạo file, Agent lại tự viết script sinh mã `docx` tạm bợ trong `scratch/`:
   - RFI-01: Lề trang `2.0/2.0/2.5/2.0 cm` (In $16.5\text{ cm} = 9355\text{ dxa}$); Cột: `755/3400/3400/1800 dxa`; Padding: `55/90 dxa`.
   - RFI-02: Lề trang `1.8/1.8/2.3/1.8 cm` (In $16.9\text{ cm} = 9582\text{ dxa}$); Cột: `700/3500/3582/1800 dxa`; Padding: `40/80 dxa`.
   - Khối ký (Sign-off): RFI-01 dùng chữ ký 4 dòng chấm, RFI-02 dùng bảng 2 ô đại diện hai bên.

---

## II. ĐỀ XUẤT GIẢI PHÁP KIẾN TRÚC 4 CẤP ĐỘ (CANONICAL RFI FRAMEWORK)

Để giải quyết dứt điểm hiện tượng Format Drift và bảo đảm **100% tài liệu RFI khi khởi tạo phải tuân thủ tuyệt đối một định dạng chuẩn bất biến**, Antigravity đề xuất khung giải pháp như sau:

### 1. Cấp Độ 1: Tách Rời Nội Dung Khỏi Định Dạng (Content as Data)
- Người dùng hoặc Agent chỉ cần soạn file Markdown đơn giản (chứa Frontmatter metadata và bảng Markdown thuần túy). 
- Tuyệt đối cấm viết mã Python `docx` tự do trong `scratch/`.

### 2. Cấp Độ 2: Bộ Quy Chuẩn Hình Học Bất Biến (Immutable Design Tokens)
Khóa cứng toàn bộ thông số trong một Template duy nhất thuộc `/ccba-xu-ly-van-phong`:
- **Khổ giấy & Lề trang:** A4 Portrait, Margins: Top 2.0cm, Bottom 2.0cm, Left 2.5cm (đóng gáy), Right 2.0cm $\implies$ Chiều rộng in cố định: **$16.5\text{ cm} = 9355\text{ dxa}$**.
- **Lưới Bảng 4 Cột Cố Định (4-Column Layout Invariant):**
  - Cột 1 (STT): `755 dxa` ($8.1\%$) — Canh giữa
  - Cột 2 (Hạng mục thông tin): `3400 dxa` ($36.3\%$) — Canh trái
  - Cột 3 (Nội dung chi tiết trao đổi): `3400 dxa` ($36.3\%$) — Canh trái
  - Cột 4 (Phản hồi của Nhà máy): `1800 dxa` ($19.2\%$) — Canh trái
  - Tổng chiều rộng bảng: **$9355\text{ dxa}$** ($100\%$ khớp lề trang).
- **Bảng Màu Nhận Diện Corporate Navy:** Kế thừa $100\%$ `standards/color/docx-formal-navy.md`:
  - Banner tiêu đề: Fill `#D9E6F2`, Text `#1F3864`, Bottom border `#1F3864` (size 6).
  - Phụ đề Tiếng Anh: `#C00000` (Accent Red).
  - Header bảng: Fill `#1F3864`, Text `#FFFFFF` in đậm.
  - Zebra striping: Dòng lẻ `#F4F6F9`, Dòng chẵn `#FFFFFF`.
  - Đường viền: Ngoài `#1F3864` (size 6), trong `#BFBFBF` (size 4).
- **Khối Ký Chuẩn (Sign-off Block):** 2 ô cân đối ($4677 + 4678\text{ dxa}$):
  - Bên trái: Đại diện Đơn vị Tư vấn (`Director of CCBA-IBST: Vu Van Chu`).
  - Bên phải: Đại diện Chủ đầu tư / Nhà máy.

### 3. Cấp Độ 3: Động Cơ Biên Dịch Chuẩn Hóa (Canonical Compiler Seam)
- Đóng gói logic chuyển đổi vào package `packages/ccba-ooxml` (module `ccba_ooxml.rfi` hoặc mở rộng `ccba_ooxml.questionnaire` hiện có) hoặc một utility CLI chính thức:
  ```powershell
  python -m ccba_ooxml.rfi compile input_rfi.md --docx output.docx --pdf output.pdf
  ```
- Hoặc thông qua Slash Command:
  ```text
  /ccba-xu-ly-van-phong --template rfi-ky-thuat input_rfi.md
  ```
- Tự động thực thi $100\%$ tiền xử lý, căn chỉnh hình học, và xác thực ISO/IEC 29500 XSD Validation qua `DOCXSchemaValidator`.

### 4. Cấp Độ 4: Cổng Kiểm Định Tự Động Trong CI (Deterministic Lint Gate)
- Bổ sung một Gate kiểm tra hình học tài liệu xuất xưởng trong `validate_legal_spoke.py` (hoặc test suite của `ccba-ooxml`): nếu file RFI sinh ra bị lệch margins hoặc lệch tỷ lệ cột $9355\text{ dxa}$ $\to$ Báo lỗi ngay lập tức.

---

## III. NỘI DUNG XIN Ý KIẾN THẢO LUẬN & PHẢN BIỆN TỪ GROK

Antigravity trân trọng đề nghị Grok đánh giá đối kháng các luận điểm sau:

1. **Về Tính Cần Thiết & Tương Thích Nền Tảng (KISS v2.0 per ADR-0061):**
   - Giải pháp trên có nguy cơ bị coi là "Over-engineering" không? Hay đây là bước đi tất yếu để giải quyết triệt để rủi ro Format Drift theo nguyên lý *Platform-Aware KISS*?
2. **Về Kiến Trúc Đóng Gói (Hub vs Spoke Partitioning per ADR-0009):**
   - Nên đặt Template và Compiler này ở đâu trước?
     - *Phương án A:* Đóng gói cục bộ tại Spoke hiện tại (`.md/tools/compile_rfi.py` và template trong `.md/templates/`) để giải quyết ngay lập tức cho dự án hiện trường.
     - *Phương án B:* Đóng gói trực tiếp thành Public Deep Seam của `packages/ccba-ooxml` trên Hub (tương tự module `ccba_ooxml.questionnaire`), rồi đồng bộ về các Spoke qua `/ccba-update-spoke`.
     - *Phương án C (Lai ghép):* Làm theo Phương án A ngay để phục vụ người dùng tại Spoke, đồng thời mở RFC Issue / PR lên Hub theo chu trình `/ccba-contribute-to-hub` (ADR-0045).
3. **Về Định Dạng Dữ Liệu Đầu Vào (Markdown vs YAML Data Model):**
   - Để người dùng và Agent thuận tiện nhất, file nguồn đầu vào nên là:
     - *Cách 1:* File Markdown thuần túy với bảng biểu GFM thông thường (dễ viết, dễ đọc nhưng parser phức tạp hơn).
     - *Cách 2:* File YAML / Frontmatter có cấu trúc dữ liệu chặt chẽ (tương tự `QuestionnaireData` trong `ccba_ooxml.questionnaire`).
4. **Về Cơ Chế Phòng Chống Vỡ Trang (Page Layout Optimization):**
   - Với các tài liệu RFI 3–4 trang, Grok có khuyến nghị gì về cơ chế tính toán tự động chiều cao dòng (`line_spacing`, `space_before`, `space_after`) để đảm bảo không bao giờ bị rơi 1–2 dòng của khối ký sang trang mới (trang mồ côi)?

---

## IV. ĐỊNH DẠNG ĐẦU RA YÊU CẦU CHO GROK

Vui lòng xuất phản biện vào tệp **`.md/peer_exchange/grok_discuss_standardize_rfi_templates.md`** với cấu trúc mở đầu bằng khối `PeerVerdictBlock`:

```yaml
---
request_id: "req-spoke-standardize-rfi-template-001"
verdict: "APPROVE_PLAN" # hoặc APPROVE_WITH_CONDITIONS / REVISE_PLAN
conditions:
  - id: "COND-01"
    description: "Mô tả điều kiện (nếu có)"
    blocking: false
risk_score: 1 # từ 1 đến 5
effort: "medium"
summary: "Tóm tắt ngắn gọn phán quyết và khuyến nghị kiến trúc"
---
```

Trân trọng cảm ơn sự phối hợp của Grok!
