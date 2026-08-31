# ADR 0038: Chuẩn Hóa Cú Pháp KaTeX Toàn Cầu & Bóc Tách Khối Công Thức Độc Lập (Universal KaTeX Mathematical Syntax Integrity)

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-08-31)

## 2. Bối Cảnh (Context)
Trong các Tiêu chuẩn Kỹ thuật Xây dựng (TCVN 5574, TCVN 2737, QCVN 06...), các công thức toán học và phương trình cơ học kết cấu là **Mỏ neo Tính toán Định lượng Cốt lõi**.
1. **Lỗi bỏ sót công thức độc lập (Standalone Equation Image Dropping):** Trong các tệp DOCX tiêu chuẩn Việt Nam, nhiều công thức toán MathType được chèn dưới dạng khối ảnh độc lập trên các paragraph rỗng (`p.text == ""`). Converter engine trước đây gặp lệnh kiểm tra rỗng quá sớm dẫn tới bỏ qua các đoạn này, làm biến mất hàng trăm công thức toán học quan trọng.
2. **Lỗi xung đột toán tử Regex làm gãy lệnh `\left[` / `\right]`:** Khi chuẩn hóa toán tử so sánh `\le` (nhỏ hơn hoặc bằng), biểu thức chính quy thiếu ranh giới từ đã vô tình bắt trúng tiền tố `le` trong lệnh `\left[`, biến `\left[` thành `\le ft[`. Điều này khiến KaTeX không tìm thấy cặp mở ngoặc tương ứng với `\right]`, gây lỗi cú pháp hiển thị màu đỏ trên toàn bộ Markdown reader.
3. **Lỗi `\tag` bên trong môi trường đa dòng (`aligned`, `gather`, `cases`):** Trong chuẩn KaTeX/MathJax, lệnh `\tag{...}` chỉ được phép sử dụng ở cấp top-level equation. Khi đặt `\tag` bên trong `\begin{aligned}`, KaTeX báo lỗi `KaTeX parse error: \tag works only at top level` và làm khối công thức bị bôi đỏ.
4. **Lỗi bọc `$$` ngoài chú thích hình ảnh:** Các chuỗi chú dẫn `<!-- FIGURE: ... -->` bị bao bọc trong khối `$$...$$` khiến Markdown hiển thị chuỗi chú thích dạng raw text thay vì render hình ảnh.

---

## 3. Quyết Định Thiết Kế (Decision)

Hệ thống thiết lập **Quy chuẩn Cú pháp Toán học KaTeX Toàn cầu (ADR 0038)** với 4 rào chắn bảo vệ:

### A. Cơ Chế Bóc Tách Khối Công Thức Độc Lập (Standalone Formula Run Inspection)
- `_process_paragraph_block` trong `strategy.py` quét toàn bộ `rIds` trong XML của các đoạn văn bản rỗng (`not text`).
- Đối chiếu với `ctx.formula_overrides` và `ctx.rid_to_katex` để xuất khối KaTeX chuẩn hóa `\n$${f_latex}$$\n<!-- formula_id: "{fid}" -->\n\n`.

### B. Cô Lập Ranh Giới Từ Regex Cho Ký Tự Hy Lạp & Toán Tử So Sánh
- Không bao giờ gộp toán tử so sánh (`le`, `ge`) vào regex phân tách ký tự Hy Lạp không có ranh giới từ.
- Sử dụng quy tắc ranh giới số `([0-9])` và tự động khôi phục các biến thể bị gãy: `\le ft` $\rightarrow$ `\left`, `\le q` $\rightarrow$ `\le`, `\ge q` $\rightarrow$ `\ge`.

### C. Chuẩn Hóa Đánh Số Công Thức Đa Dòng (Multiline Environment Tagging Rule)
- Đối với công thức đơn cấp cao nhất: Sử dụng `\tag{X}` trong `$$...$$`.
- Đối với các hệ phương trình / điều kiện đa dòng (`\begin{aligned}`, `\begin{gather}`, `\begin{cases}`): Nghiêm cấm đặt `\tag{...}` bên trong môi trường. Thay vào đó, sử dụng khoảng đệm căn phải tiêu chuẩn `\qquad (X)` cho từng dòng, đảm bảo 100% tương thích với mọi Markdown renderer và VS Code KaTeX extension.

### D. Tách Rời Tuyệt Đối Khối Chú Thích Hình Ảnh & Biểu Thức Toán Học
- Mọi chuỗi chú dẫn hình `<!-- FIGURE: ... -->` hoặc `<!-- DIAGRAM ... -->` phải được phát hiện và xuất độc lập ra luồng Markdown, tuyệt đối không được bao bọc bên trong dấu mở/đóng toán học `$$`.

---

## 4. Hệ Quả & Lợi Ích (Consequences)
- **100% Không Lỗi Cú Pháp Toán Học (Zero KaTeX Errors):** Toàn bộ 228 công thức của TCVN 5574:2018 và các tiêu chuẩn kỹ thuật hiển thị sắc nét, chuẩn mực, không có bất kỳ dòng chữ báo lỗi màu đỏ nào.
- **Bảo Toàn 100% Khối Lượng Quy Chuẩn Định Lượng:** Không còn hiện tượng mất mát công thức MathType dạng khối ảnh độc lập.
- **Tương Thích Mọi Nền Tảng (Universal Rendering):** Tương thích hoàn hảo trên VS Code Markdown Preview, GitHub Web, Google NotebookLM và AI QC Pipeline.
