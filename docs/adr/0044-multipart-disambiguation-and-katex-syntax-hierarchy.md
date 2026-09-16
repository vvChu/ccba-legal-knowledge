# ADR 0044: Định Danh Bảng Quy Chuẩn Đa Phần & Cú Pháp Toán Học Đa Dòng KaTeX (Multi-Part Disambiguation & KaTeX Syntax Hierarchy Invariant)

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-09-14)  
*Hội tụ thông qua Chu trình Học tập Kiến trúc `/ccba-grilling` & `/learn` (Mục 46 session_learnings.md).*

---

## 2. Bối Cảnh (Context)
Trong quá trình chuẩn hóa các quy chuẩn kỹ thuật quốc gia đa phần (như QCVN 07:2023/BXD gồm 10 phần độc lập từ 07-1 đến 07-10):
1. **Xung Đột Đặt Tên Tệp Bảng Biểu (Table Name Collision):** Mỗi phần độc lập trong quy chuẩn đều có "Bảng 1", "Bảng 2", "Bảng 3"... Nếu lưu theo định dạng `bang_01.csv`, `bang_02.csv`, các phần sau sẽ ghi đè lên dữ liệu của phần trước, gây mất mát dữ liệu nghiêm trọng và vi phạm Gate 3, Gate 13.
2. **Lỗi Biên Dịch KaTeX Trong Môi Trường Đa Dòng (KaTeX Multiline Tag Syntax Error):**
   - Tiêu chuẩn KaTeX/LaTeX quy định: `\tag{...}` chỉ hợp lệ ở cấp ngoài cùng của khối phương trình đơn dòng `$$ ... \tag{1} $$`.
   - Khi công thức có nhiều dòng sử dụng các môi trường như `aligned`, `cases`, `gather`, việc chèn `\tag{...}` bên trong môi trường sẽ gây lỗi cú pháp KaTeX ("\tag not allowed inside environment"), khiến công thức bị bôi đỏ và gãy hiển thị trên giao diện web.

---

## 3. Quyết Định Thiết Kế (Decision)

Hệ thống thiết lập **Bất biến Định danh Bảng Quy chuẩn Đa phần & Phân tầng Cú pháp Toán học KaTeX (ADR 0044)**:

### A. Phân Định Danh Bảng Biểu Đa Phần (Multi-Part Disambiguation)
1. **Tiền Tố Phân Phần Bắt Buộc:** Đối với các văn bản quy chuẩn có nhiều phần độc lập, toàn bộ bảng biểu 2D bắt buộc phải gắn tiền tố định danh của phần tương ứng:
   - Ví dụ: Phần 1: `bang_p01_01.csv`, `bang_p01_02.csv` (hoặc `bang_07_1_01.csv`).
   - Phần 2: `bang_p02_01.csv`, `bang_p02_02.csv`.
2. **Khai Báo Metadata Bảng (`tables_catalog.json`):**
   - Bắt buộc khai báo trường `part_id` (ví dụ: `"part_id": "07-1"`) trong từng bản ghi bảng để phân định rõ phạm vi áp dụng.
   - Nghiêm cấm mọi hành vi ghi đè trùng lặp tệp bảng giữa các phần.
3. **Cưỡng Chế Kiểm Định (Sub-Gate 3.2):**
   - Bộ kiểm định `validate_legal_spoke.py` quét toàn bộ `tables_catalog.json` để phát hiện trùng lặp mã `table_id` và đối chiếu sự tồn tại của tệp trên đĩa.

### B. Phân Tầng Cú Pháp Đánh Số Công Thức KaTeX (KaTeX Syntax Hierarchy)
1. **Khối Đơn Dòng (Single-line Display Math):**
   - Được phép sử dụng lệnh chuẩn `\tag{X}` ở cuối khối công thức:
     ```latex
     $$ F = m \cdot a \tag{1} $$
     ```
2. **Khối Đa Dòng (Multiline Math Environments: `aligned`, `cases`, `gather`):**
   - Tuyệt đối cấm sử dụng lệnh `\tag{...}` bên trong khối đa dòng.
   - Bắt buộc sử dụng khoảng cách ngữ nghĩa `\qquad (X)` ở cuối dòng biểu thức tương ứng:
     ```latex
     $$ \begin{aligned}
     A &= B + C \qquad &(1) \\
     D &= E \times F \qquad &(2)
     \end{aligned} $$
     ```
3. **Cưỡng Chế Kiểm Định (Sub-Gate 14.2):**
   - Bộ linter KaTeX trong `validate_legal_spoke.py` tự động quét AST Markdown, báo lỗi nếu phát hiện `\tag{` nằm trong phạm vi các môi trường đa dòng.

---

## 4. Hệ Quả & Tác Động (Consequences)

### Tích Cực
- Triệt tiêu 100% nguy cơ ghi đè dữ liệu bảng biểu trong các quy chuẩn đồ sộ đa phần (như QCVN 07:2023/BXD với 32+ bảng).
- Đảm bảo 100% công thức toán học KaTeX hiển thị mượt mà, không sinh lỗi bôi đỏ hay lỗi cú pháp trên mọi nền tảng hiển thị.
- Hoàn thiện bộ kiểm chuẩn Sub-Gate 3.2 và 14.2 cho Master CI.

---
*Biên soạn bởi CCBA Agent Architecture Council.*  
*Căn cứ thực thi: Invariant 16 `AGENTS.md`, Sub-Gate 3.2 & 14.2 `scripts/validate_legal_spoke.py`.*
