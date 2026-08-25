# ADR 0029: Verbatim Bullet Parity & Markdown Escaping Protocol

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-08-22)

## 2. Bối Cảnh (Context)
Trong văn bản quy phạm pháp luật Việt Nam, dấu gạch đầu dòng `-` và dấu cộng `+` có giá trị phân cấp pháp lý nghiêm ngặt (dưới Điểm là các Gạch đầu dòng `-`, dưới Gạch đầu dòng là các Dấu cộng `+`).
Khi chuyển đổi từ DOCX sang Markdown chuẩn, parser Markdown thông thường tự động biến dấu `-` và `+` thành thẻ HTML `<ul><li>` dạng chấm tròn bullet, làm mất hoàn toàn ký tự gốc của văn bản luật.

## 3. Quyết Định Thiết Kế (Decision)
1. **Cơ chế Thoát Ký Tự Bắt Buộc (Verbatim Escaping):**
   - Dấu gạch đầu dòng cấp 1: Bắt buộc chuyển thành `\- ` (Backslash Escaped Dash).
   - Dấu cộng cấp 2: Bắt buộc chuyển thành `&nbsp;&nbsp;\+ ` (Indented Escaped Plus).
2. **Cưỡng Chế Zero-Clutter Bằng Linter Gate:**
   - Bộ linter `lint_visual_parity.py` kiểm tra $100\%$ các dòng văn bản, nghiêm cấm dồn cục nhiều ý trên 1 dòng hoặc dùng sai chuẩn bullet.

## 4. Hệ Quả (Consequences)
- Bảo toàn $100\%$ ký tự gốc của Công báo và văn bản pháp lý.
- Đảm bảo hiển thị thị giác nguyên bản khi render trên mọi trình đọc Markdown và web.
