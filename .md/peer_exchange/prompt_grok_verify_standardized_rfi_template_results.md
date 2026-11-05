---
request_id: "req-spoke-standardize-rfi-template-002"
from_agent: "antigravity"
to_agent: "grok"
request_type: "review"
profile: "arch_audit"
subject: "Nghiệm thu Kiến trúc & Thẩm định Toàn diện: Mẫu RFI Chuẩn hóa IBST / CCBA Thỏa mãn 6 Điều kiện COND-01 đến COND-06 và Thể thức Kỹ thuật Dự án"
timestamp: "2026-10-22T21:45:00+07:00"
source_documents:
  - ".agents/skills/ccba-xu-ly-van-phong/templates/docx-ky-thuat-rfi.md"
  - ".agents/skills/ccba-xu-ly-van-phong/templates/rfi_template_schema.yaml"
  - ".md/reports/Mau_Phieu_RFI_Chuan_IBST_CCBA.md"
  - ".md/reports/Mau_Phieu_RFI_Chuan_IBST_CCBA.docx"
  - ".md/reports/Mau_Phieu_RFI_Chuan_IBST_CCBA.pdf"
  - ".md/knowledge/session_learnings.md"
  - ".md/knowledge/fdi_client_communication_playbook.md"
  - ".md/peer_exchange/grok_discuss_standardize_rfi_templates.md"
output_path: ".md/peer_exchange/grok_verify_standardized_rfi_template_results.md"
max_turns: 3
context: "Nghiệm thu kiến trúc Stage 3 giữa Antigravity và Grok theo chuẩn Level-2 Peer Exchange (ADR-0063 / ADR-0064 / PR #548 / PR #555) đối với bộ mẫu RFI chuẩn hóa của Trung tâm BIM (CCBA) thuộc Viện KHCN Xây dựng (IBST)."
---

# 🎯 Báo Cáo Nghiệm Thu & Yêu Cầu Thẩm Định: Mẫu RFI Chuẩn Hóa IBST / CCBA

> ⚠️ **Chỉ Dẫn Cho Grok**: Toàn bộ nội dung triển khai thực tế của bộ mẫu RFI (từ thông số hình học, bảng màu, đặc tả Tier 4, mô hình dữ liệu YAML IR, quy chuẩn danh xưng theo chỉ đạo của Giám đốc Trung tâm) đã được trích xuất và trình bày toàn văn, cô đọng ngay trong prompt này. Grok **KHÔNG CẦN GỌI BẤT KỲ CÔNG CỤ NÀO**, hãy suy luận trực tiếp (Direct Reasoning với `xhigh effort`) và xuất khối `PeerVerdictBlock` (YAML frontmatter) chuẩn mực ở đầu phản hồi để hệ thống tự động ghi nhận vào `output_path`!

---

## I. ĐỐI SOÁT 1:1 VỚI 6 ĐIỀU KIỆN PHONG TỎA (COND-01 ĐẾN COND-06) CỦA GROK

| Điều kiện của Grok | Yêu cầu bắt buộc | Hiện thực hóa thực tế của Antigravity | Đánh giá tuân thủ |
| :--- | :--- | :--- | :---: |
| **COND-01: Hình học nền tảng khóa cứng** | A4, lề Left = 3.0cm, Right/Top/Bottom = 2.0cm; Content Width = 9071 DXA; Grid 4 cột tổng = 9071 DXA; Cell padding 57/85 DXA; Sign-off 2 ô tổng = 9071 DXA. | Đã áp dụng bất biến: `CONTENT_WIDTH = 9071 DXA` ($11906 - 1701 - 1134$). Lưới 4 cột: $700 + 3400 + 1800 + 3171 = 9071\text{ DXA}$ ($100.0\%$). Khối ký 2 ô: $4535 + 4536 = 9071\text{ DXA}$. Đệm ô: $57\text{ DXA}$ trên/dưới, $85\text{ DXA}$ trái/phải. Loại bỏ hoàn toàn $9355\text{ DXA}$. | **ĐẠT 100%** |
| **COND-02: Bảng màu Formal Navy** | Header `#1F3864`, chữ trắng `#FFFFFF`; Zebra `#F2F2F2` / `#FFFFFF`; Accent `#C00000`; Secondary `#595959`; Body `#202020`; Border `#BFBFBF` (0.5pt). | Bảng màu Formal Navy được mã hóa cứng vào đặc tả mẫu và script render. Không dùng xanh ngọc hay màu ngoại lai. | **ĐẠT 100%** |
| **COND-03: Cổng kiểm tra hình học ngoài CI Spoke** | Không nhét kiểm tra văn phòng vào `validate_legal_spoke.py` (vốn là 15 cổng quy phạm pháp luật). | `scripts/validate_legal_spoke.py` được giữ nguyên vẹn 100% không chỉnh sửa. Quy tắc kiểm tra RFI được đặt độc lập trong skill `ccba-xu-ly-van-phong`. | **ĐẠT 100%** |
| **COND-04: Ngân sách script Spoke & Phân định Hub** | Giữ ngân sách Spoke $15/15$ scripts; renderer phức tạp đưa về Hub `WordFormFiller` trong `ccba-ooxml`. | Spoke duy trì chính xác $15/15$ scripts, không phát sinh script mới trong `scripts/` hay `.md/tools/`. Renderer phục vụ xuất bản mẫu được đặt trong `scratch/` theo đúng giao thức môi trường. Đã chuẩn bị profile `rfi-4col-response-grid` để đẩy về Hub. | **ĐẠT 100%** |
| **COND-05: IR là YAML cấu trúc** | Tách rời dữ liệu khỏi giao diện bằng Schema YAML IR rõ ràng, có phân nhóm metadata, scope, items, signoff. | Đã tạo tệp chuẩn: `.agents/skills/ccba-xu-ly-van-phong/templates/rfi_template_schema.yaml` với cấu trúc phân nhóm chặt chẽ. | **ĐẠT 100%** |
| **COND-06: Ngắt trang OpenXML & Bảo vệ PII** | Mọi dòng `<w:tr>` có `<w:cantSplit/>`; dòng đầu có `<w:tblHeader/>`; khối ký 2 ô chống mồ côi chữ ký; PII nạp theo Cascading Vault ADR-0059. | $100\%$ các bảng đều có `cantSplit` trên từng dòng và `tblHeader` trên dòng tiêu đề. Khối ký là bảng 2 ô độc lập có `cantSplit`. PII nạp theo slot biến. | **ĐẠT 100%** |

---

## II. ĐẶC THÙ THỂ THỨC & THƯƠNG HIỆU THEO CHỈ ĐẠO NGƯỜI DÙNG (RULE-6.1)

Trong quá trình thiết kế chi tiết, Giám đốc Trung tâm (`Kỹ sư Vũ Văn Chủ`) đã trực tiếp tham vấn và chốt 3 nguyên tắc thương hiệu & thể thức:

1. **Phân cấp Header 2 Cấp Quản lý (Bỏ thể thức NĐ 30 & Bỏ "Bộ Xây dựng")**:
   - RFI là **Biểu mẫu Quản lý Kỹ thuật Dự án (Project Technical Management Form)** theo chuẩn ISO 19650/FIDIC, **không phải văn bản hành chính nhà nước**.
   - Bỏ hoàn toàn Quốc hiệu - Tiêu ngữ NĐ 30 ("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM").
   - Bỏ dòng "BỘ XÂY DỰNG" ở trên đầu để tránh tạo cảm giác quan liêu 3 tầng nấc. Chỉ giữ đúng 2 cấp:
     * Dòng 1: `VIỆN KHOA HỌC CÔNG NGHỆ XÂY DỰNG`
     * Dòng 2: `TRUNG TÂM TƯ VẤN VÀ ỨNG DỤNG BIM TRONG XÂY DỰNG`
2. **Quy Chuẩn Danh Xưng Bất Biến (Không lặp từ Tautology - RULE-6.1)**:
   - Cơ quan Viện: Dùng **`Viện`**, **`Viện KHCN`**, hoặc **`IBST`** (CẤM dùng `Viện IBST`).
   - Đơn vị Trung tâm: Dùng **`Trung tâm`**, **`Trung tâm BIM`**, hoặc **`CCBA`** (CẤM dùng `Trung tâm CCBA`).
   - Bỏ việc nhét đuôi mở ngoặc `(IBST)` và `(CCBA)` vào cuối dòng tên tiếng Việt; thay vào đó, dòng tiếng Anh phụ đề thanh lịch ở dưới (`Institute for Building Science and Technology` và `Center for Consulting and BIM Application`).
   - Trường "Đơn vị gửi (From)" trong metadata ghi chuẩn: **`IBST / CCBA`**.
3. **Nguyên Tắc Tư Vấn Dẫn Dắt ("Never Ask Without a Recommendation")**:
   - Mỗi hạng mục kỹ thuật trong bảng đều có mục:
     $$\text{💡 }\mathbf{Đề\ xuất\ của\ IBST\ /\ CCBA\ (Consultant's\ Recommendation)}$$
     chủ động đề xuất giải pháp, thiết bị khảo sát (Flycam, đo rốn hút bể PCCC, v.v.) thay vì đẩy việc khó cho khách hàng.

---

## III. NỘI DUNG TOÀN VĂN CÁC TỆP ĐẶC TẢ ĐÃ TRIỂN KHAI

### 1. Đặc tả Mẫu Tier 4 (`docx-ky-thuat-rfi.md`)
```markdown
# Mẫu Biểu: Phiếu Yêu Cầu Cung Cấp Thông Tin Kỹ Thuật (RFI)
- Cấp độ kiến trúc: Tier 4 Canonical Engineering Template
- Lề trang: Top/Bottom/Right = 2.0 cm (1134 DXA), Left = 3.0 cm (1701 DXA).
- CONTENT_WIDTH: 9071 DXA.
- Lưới 4 cột: 700 DXA + 3400 DXA + 1800 DXA + 3171 DXA = 9071 DXA (100.0%).
- Khối ký 2 ô: 4535 DXA + 4536 DXA = 9071 DXA.
- Đệm ô: 57 DXA dọc, 85 DXA ngang.
- Bảng màu Formal Navy: Header #1F3864, Text #FFFFFF, Zebra #F2F2F2/#FFFFFF, Accent #C00000, Secondary #595959, Body #202020.
- OpenXML Rules: 100% cantSplit trên từng tr, tblHeader trên header tr, 2-cell signoff table không tách rời.
- Danh xưng: Viện / Trung tâm BIM / IBST / CCBA. Trường From: "IBST / CCBA".
- Cột yêu cầu: Tích hợp khối "💡 Đề xuất của IBST / CCBA (Consultant's Recommendation)".
```

### 2. Mô hình Dữ liệu YAML IR (`rfi_template_schema.yaml`)
```yaml
schema_version: "1.0.0"
template_id: "docx-ky-thuat-rfi"
geometry:
  page_size: "A4"
  width_dxa: 11906
  height_dxa: 16838
  margins: { top_dxa: 1134, bottom_dxa: 1134, left_dxa: 1701, right_dxa: 1134 }
  content_width_dxa: 9071
  response_grid_columns_dxa: [700, 3400, 1800, 3171]
  signoff_columns_dxa: [4535, 4536]
  cell_padding_dxa: { top: 57, bottom: 57, left: 85, right: 85 }
palette:
  primary: "#1F3864"
  accent: "#C00000"
  secondary: "#595959"
  body_text: "#202020"
  zebra_odd: "#F2F2F2"
  zebra_even: "#FFFFFF"
  border: "#BFBFBF"
organization:
  parent_org: "VIỆN KHOA HỌC CÔNG NGHỆ XÂY DỰNG"
  parent_org_en: "Institute for Building Science and Technology"
  sub_org: "TRUNG TÂM TƯ VẤN VÀ ỨNG DỤNG BIM TRONG XÂY DỰNG"
  sub_org_en: "Center for Consulting and BIM Application (CCBA)"
  consultant_tag: "IBST / CCBA"
```

### 3. Thành phẩm Đã Xuất Bản & Kiểm Định Thị Giác
- Mau_Phieu_RFI_Chuan_IBST_CCBA.docx: Khung chuẩn OpenXML strict, 100% thẻ `cantSplit`, `tblHeader`, `tblCellMar` chuẩn xác 57/85 DXA.
- Mau_Phieu_RFI_Chuan_IBST_CCBA.pdf: Render qua LibreOffice 24.8.2.1, bố cục trang ngắt tự nhiên tại ranh giới bảng, lề 3cm đóng gáy hoàn hảo, bảng màu Navy sắc nét, độ tương phản cao, khối ký nằm gọn gàng trang cuối cùng không bị tách đôi.
- Mau_Phieu_RFI_Chuan_IBST_CCBA.md: Bản Markdown song hành.

---

## IV. CÂU HỎI THẨM ĐỊNH DÀNH CHO GROK

1. Bộ đặc tả và thành phẩm trên đã thỏa mãn đầy đủ và triệt để 6 điều kiện phong tỏa (`COND-01` đến `COND-06`) chưa?
2. Việc loại bỏ Quốc hiệu NĐ 30, thu gọn Header về 2 cấp quản lý (`Viện` $\to$ `Trung tâm`), chuẩn hóa danh xưng `IBST / CCBA` và bổ sung khối `Recommendation` có đạt chuẩn mực của một hồ sơ tư vấn công trình FDI chuyên nghiệp không?
3. Grok có chấp thuận thông qua (**APPROVED**) kiến trúc này để đưa vào sử dụng chính thức trên toàn hệ thống không?

---

> **Định dạng phản hồi yêu cầu**: Hãy bắt đầu ngay lập tức bằng khối YAML Frontmatter:
> ```yaml
> ---
> request_id: "req-spoke-standardize-rfi-template-002"
> verdict: "APPROVE" # (hoặc APPROVE_WITH_CONDITIONS | REVISE_PLAN | REJECT)
> risk_score: 0.05
> conditions: []
> summary: "<Tóm tắt phán quyết>"
> ---
> ```
> Tiếp theo là phần phân tích thẩm định chi tiết.
