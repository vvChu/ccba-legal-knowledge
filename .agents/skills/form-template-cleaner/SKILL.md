---
name: form-template-cleaner
description: Sub-skill làm sạch biểu mẫu và tự động khôi phục tiêu đề biểu mẫu bị lỗi placeholder (dấu chấm lửng) bằng AI Gateway.
role: sub_skill
master_skill: markdown-document-processing
applies_to:
  - "Phần mềm"
  - "Thẩm tra thiết kế"
  - "Thiết kế"
  - "Kiểm định"
bundle: "_core"
---

# Sub-skill: Form Template Cleaner

Kỹ năng này xử lý các biểu mẫu (tờ trình, mẫu biên bản, báo cáo) bị lỗi nhận nhầm dòng placeholder chứa dấu chấm lửng/nét đứt làm tiêu đề.

## Quy Trình Tự Động & Kiểm Định
Trong chuẩn **OKF v2.4 (ADR 0021, ADR 0036, ADR 0042)**, toàn bộ biểu mẫu được bóc tách tự động thành các tệp nguyên tử trong `templates/phu_luc_XX/mau_YY.md` và kiểm định qua Gate 8 của `scripts/validate_legal_spoke.py`.

> [!NOTE] **Ghi chú Chuẩn Hóa DOM Pha 1 (ADR 0042):**
> Ở Pha 1, `DocxCanonicalSanitizer` đã tự động giải nén (unwrap) các bảng bố cục dàn trang (Borderless Layout Tables) như khối tiêu ngữ hành chính, quốc hiệu, cơ quan ban hành và chữ ký thành văn xuôi phẳng. Nhờ đó, bộ nhận diện biểu mẫu nguyên tử không bị nhầm lẫn với các bảng dàn trang, tập trung 100% vào dữ liệu và cấu trúc thực của biểu mẫu quy phạm.

Khi cần chuyển đổi hoặc làm sạch thủ công:
```powershell
python -m ccba_legal convert --docx-path "legal_docs/<category>/<slug>/sources/<slug>.docx" --target-bundle-dir "legal_docs/<category>/<slug>"
python scripts/validate_legal_spoke.py
```

## SOP Xử lý bằng Prompt (AI-assisted Recovery)
Khi chạy CLI hoặc khi muốn viết script Python tùy chỉnh gọi AI Gateway để khôi phục tiêu đề:

1. **Nhận dạng lỗi:**
   * Phần frontmatter `title` hoặc tiêu đề chính `#` ở dòng đầu của tệp có các ký tự placeholder như `............`, `.......(1).......`, `___`.
2. **Thu thập dữ liệu ngữ cảnh:**
   * Trích xuất 20 dòng đầu tiên của tệp Markdown để làm thông tin đầu vào.
3. **Mẫu Prompt gọi AI Gateway (`ccba-ai`):**
   ```python
   from ccba_ai import ai
   
   prompt = f"""
   Phân tích 20 dòng đầu của biểu mẫu pháp luật Việt Nam sau đây và suy luận ra tiêu đề chính thức của biểu mẫu đó.
   Tiêu đề biểu mẫu thường là dòng chữ viết hoa nổi bật (ví dụ: THÔNG BÁO KHỞI CÔNG..., ĐƠN ĐỀ NGHỊ CẤP PHÉP..., BÁO CÁO KẾT QUẢ...).
   Bỏ qua các dòng placeholder chấm lửng như "........", "............(1)............", "Kính gửi: ...".
   Chỉ trả về duy nhất chuỗi tiêu đề chính thức, không thêm bất kỳ văn bản giải thích nào khác.
   Nội dung 20 dòng đầu:
   {context_lines}
   """
   extracted_title = ai.chat(prompt)
   ```
4. **Cập nhật:**
   * Đè tiêu đề chuẩn `extracted_title` vào trường `title` của frontmatter và vào dòng tiêu đề `#` của tệp.

## Phương Pháp Xác Định Tiêu Đề Chuẩn Luật (Deterministic Statutory Mapping)
Trước khi gọi AI Gateway, Agent có thể áp dụng phương pháp xác định 100% không tốn token:
1. **Quét câu văn quy định thẩm quyền trong văn bản chính:**
   * Tìm các đoạn dẫn chiếu dạng: `theo Mẫu số XX Phụ lục YY ban hành kèm theo Nghị định này...`
   * Bóc tách tiêu đề chính thức đã được Luật/Nghị định định danh (ví dụ: *Đơn đề nghị cấp chứng chỉ hành nghề*, *Giấy ủy quyền*, *Quyết định cấp giấy phép hoạt động xây dựng cho nhà thầu nước ngoài*).
2. **Cập nhật đồng bộ:**
   * Thay thế frontmatter `title: "Mẫu số XX - <TÊN_CHUẨN_LUẬT>"`
   * Thay thế tiêu đề `# Mẫu Số XX - <TÊN_CHUẨN_LUẬT>`
   * Đổi tên tệp sang dạng chuẩn slug: `mau_XX_<ten_chuan_slug>.md`
   * Cập nhật toàn bộ liên kết tương đối trong văn bản chính, `index.md` và `clauses.json`.
