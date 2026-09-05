# ADR 0041: Kiến Trúc Bóc Tách Tri Thức Bảng Biểu Xác Định Toàn Cầu (Universal Deterministic Table Knowledge Extraction Architecture)

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-09-03)  
*Hội tụ thông qua Quy trình Phỏng vấn Socrates Đối Chiếu Thiết Kế (`/ccba-grill-with-docs`) dựa trên Báo cáo Nghiên cứu Kỹ thuật `RESEARCH-TABLE-ARCHETYPE-2026-09`.*

---

## 2. Bối Cảnh (Context)
Dữ liệu bảng trong hệ thống Văn bản Quy phạm Pháp luật (VBPL), Quy chuẩn Kỹ thuật Quốc gia (QCVN) và Tiêu chuẩn Quốc gia (TCVN) ngành Xây dựng là **mỏ neo tri thức định lượng cốt tử** phục vụ tính toán tải trọng, khoảng cách an toàn cháy, kiểm tra giới hạn chịu lực và nghiệm thu công trình.

Nghiên cứu đối nghịch (**Adversarial Review**) đối với các bộ parser chuyển đổi bảng trước đây đã bóc trần **5 bẫy kỹ thuật nguy hiểm**:
1. **Lệch chỉ mục cột (Column Skew) do Merged Cells (`w:gridSpan`, `w:vMerge`):** Khi duyệt ngây thơ qua các ô gộp trong OpenXML, dữ liệu hàng bị nhân bản $K$ lần hoặc thiếu cột gây hiện tượng răng cưa (ragged array); các ô gộp dọc (`vMerge`) bị rỗng khiến các công cụ truy vấn quan hệ (Pandas, DuckDB, Polars, SQL) đọc nhầm ô trống.
2. **Ô nhiễm bảng dàn trang (Layout Table Pollution):** Chuyên viên soạn thảo thường dùng bảng Word 2 cột không viền để kẹp số hiệu công thức `(1)` hoặc Quốc hiệu/Chữ ký. Việc bốc toàn bộ thẻ `<w:tbl>` làm sinh ra hàng chục file CSV rác vào thư mục `tables/csv/`.
3. **Phá vỡ liên kết Chú thích chân bảng (Footnote Corruption):** Nuốt mất ký hiệu tham chiếu (`150(1)` biến thành `1501` làm sai lệch số liệu 10 lần), tự tiện gán số thứ tự nhân tạo (`CHÚ THÍCH 1..N`), hoặc nhồi khối văn bản chú thích dài ngoằng vào ô cuối CSV làm lệch ma trận 2D.
4. **Mất trắng tri thức đa phương thức trong ô (In-Cell Blindness):** Thuộc tính `cell.text` bỏ qua hoàn toàn đối tượng nhúng nhị phân MathType OLE và thẻ đồ họa vector WMF/EMF, biến ô công thức/sơ đồ thành chuỗi rỗng.
5. **Xung đột trực tiếp với 5/12 Cổng kiểm định Master CI:** Gate 3 (Table Attachments), Gate 8 (Table Structural Integrity), Gate 9 (Visual Parity), Gate 11 (Verbatim Parity Rate $\ge 98\%$), và Gate 12 (Multimodal Integrity).

---

## 3. Quyết Định Thiết Kế (Decision)

Hệ thống thiết lập **Kiến Trúc Bóc Tách Tri Thức Bảng Biểu Xác Định Toàn Cầu (ADR 0041)** theo các nguyên tắc cốt lõi:

### A. Hệ Thống Phân Loại 6 Hình Mẫu Bảng (Table Archetype Taxonomy)
Mọi bảng trong kho tri thức bắt buộc được nhận diện và gắn nhãn theo 6 Archetypes:
1. `FLAT_MATRIX`: Bảng số liệu phẳng chuẩn 2D, header 1 dòng, không gộp ô $\rightarrow$ Xuất Markdown GFM, `tables/csv/{slug}.csv`, `tables/json/{slug}.json`.
2. `HIERARCHICAL_GRID`: Ma trận phân cấp đa tầng (header 2–4 tầng lồng nhau, hàng phân loại toàn chiều rộng) $\rightarrow$ Phẳng hóa header có cấu trúc phân cấp, JSON lưu cây thuộc tính.
3. `IN_CELL_MULTIMODAL`: Ô chứa đồng thời văn bản, sơ đồ hình học và công thức toán $\rightarrow$ Bóc tách ảnh sang `figures/images/`, nhúng `<img ...>`, công thức chuyển thành KaTeX inline `$f(x)$`.
4. `FOOTNOTE_RICH`: Bảng quy phạm kèm hệ thống chú thích ngoại lệ/điều kiện miễn trừ $\rightarrow$ Tách rời khỏi ô CSV, bảo tồn $100\%$ ký hiệu gọi, JSON lưu dict `footnotes`.
5. `BORDERLESS_LAYOUT`: Bảng bố cục ẩn viền căn lề công thức hoặc chữ ký $\rightarrow$ **Cấm xuất vào `tables/`**, giải nén thành Markdown/KaTeX nội dòng trên thân văn bản.
6. `ADMIN_FORM`: Bảng biểu mẫu kiểm mục, nghiệm thu có ô ký tên, tickbox `[ ]`, chỗ điền chấm lửng $\rightarrow$ Định tuyến 100% về thư mục **`templates/`** (Atomic Form Templates theo ADR 0021 & ADR 0036). Không xuất CSV rác vào `tables/`.

### B. Thuật Toán Virtual 2D Grid Engine & Hierarchical Forward-Fill
- Đọc kích thước cột chuẩn từ thẻ `<w:tblGrid><w:gridCol/>` để cố định ma trận $R \times C$, loại bỏ hoàn toàn hiện tượng ragged rows.
- **Xử lý `vMerge` (Gộp dọc):**
  - Trong `tables/csv/`: Áp dụng cơ chế **Hierarchical Forward-Fill có kiểm soát** (tự động điền giá trị ô cha xuống các hàng con) để tối ưu cho phân tích số liệu Pandas/DuckDB và Agent RAG query độc lập từng hàng.
  - Trong Markdown: Giữ nguyên bố cục trực quan bản in.
  - Trong `tables/json/`: Gắn metadata `{"is_merged_continuation": true, "master_cell": [r, c]}`.
- **Xử lý Tiêu đề phân cấp đa tầng ($\ge 2$ tầng):**
  - Áp dụng chuẩn **Composite Delimited Header (`"Tầng 1 — Tầng 2 — Tầng 3"`)** đồng nhất cho cả CSV và Markdown GFM, đảm bảo mỗi cột đều mang ngữ nghĩa trọn vẹn và không bị vỡ cú pháp GFM.

### C. Rào Chắn Phân Loại Nhị Phân Xác Định (Binary Layout Classifier)
- Nhận diện tự động bảng phi quy chuẩn dựa trên thuộc tính đường viền `w:tblBorders`, tỷ lệ kích thước $R \times C$, và từ khóa quy phạm:
  - Bảng không viền kẹp công thức $\rightarrow$ Bóc tách thành KaTeX display `$$... \tag{X}$$`.
  - Bảng biểu mẫu hành chính $\rightarrow$ Định tuyến về `templates/`.

### D. Cơ Chế Footnote Decoupled & Semantic Binding
- **Nguyên tắc bất biến:** Footnote của bảng không được nằm trong ma trận dữ liệu 2D (CSV), nhưng bắt buộc phải gắn liền với bảng trong Bundle:
  - File `tables/csv/`: Chỉ chứa ma trận số liệu thuần túy $M \times N$ (không chứa hàng footnote dài ngoằng ở đáy bảng).
  - File `tables/json/`: Lưu trữ có cấu trúc gồm `matrix` và dictionary `footnotes: {"(*)": "...", "(1)": "..."}`.
  - Trong thân Markdown: Đặt ngay khối trích dẫn chú thích bên dưới bảng với tiêu đề chuẩn `**CHÚ THÍCH:**`, bảo tồn $100\%$ các gạch đầu dòng `&nbsp;&nbsp;\- ` và ký hiệu tham chiếu gốc trong ô (`150 (*)`, `REI 60 (1)`). Nghiêm cấm tự tiện đổi thành số thứ tự nhân tạo (`CHÚ THÍCH 1..N`).

### E. In-Cell Multimodal & KaTeX Isolation
- Tích hợp đệ quy **MTEF Parser (`mtef_parser.py` - ADR 0040)**: Quét từng paragraph trong ô, chuyển đổi MathType nhị phân sang KaTeX inline `$f(x)$`. Tuyệt đối không dùng block `$$` trong ô bảng Markdown.
- Bóc tách đồ họa vector WMF/EMF sang SVG và PNG 300 DPI, nhúng vào cell bằng `<img src="..." width="..." alt="...">`.

### F. Nâng Cấp Master CI Gate 8 (Table Structural & Regularity Integrity Gate)
Cập nhật Cổng kiểm định Gate 8 trong `scripts/validate_legal_spoke.py` để cưỡng chế:
1. **Grid Regularity:** $100\%$ các hàng dữ liệu trong file CSV phải có cùng số lượng cột bằng số cột của `gridCol` ($Cols_{row} == Cols_{grid}$).
2. **Zero Layout Tables in `tables/`:** $0$ file CSV nào trong `tables/csv/` là bảng dàn trang ẩn viền hoặc bảng biểu mẫu hành chính.
3. **Footnote Reference Parity:** $100\%$ ký hiệu tham chiếu footnote trong ô dữ liệu (`(*)`, `(1)`) phải có mục giải nghĩa tương ứng trong khối chú thích.

---

## 4. Hệ Quả & Tác Động (Consequences)

### Tích Cực
- **Độ chính xác truy vấn số liệu đạt 100%:** Ma trận CSV phẳng hoàn chỉnh, không còn ô rỗng `NaN` do gộp dọc, giúp AI Agent tra cứu thông số kỹ thuật tức thì với độ tin cậy tuyệt đối.
- **Sạch sẽ kho dữ liệu (Clean Compartments):** Thư mục `tables/` chỉ chứa bảng số liệu kỹ thuật đích thực; toàn bộ biểu mẫu hành chính được gom về `templates/` theo đúng ADR 0021.
- **Bảo toàn nguyên văn quy phạm (Zero-Dropped Notes):** Mọi điều kiện miễn trừ, hệ số nhân an toàn trong footnote được bảo tồn nguyên vẹn và liên kết ngữ nghĩa với từng ô dữ liệu.
- **Tuân thủ toàn diện 12 Cổng CI:** Không sinh lỗi vỡ bảng pipe, không sinh lỗi nhân bản từ vựng, không rớt tỷ lệ Verbatim Parity.

### Hạn Chế & Chi Phí
- Cần cập nhật `table_handler.py` và `table_extractor.py` trong package Hub (`ccba-legal-intel`).
- Cần chạy lại validation để đảm bảo toàn bộ 37 văn bản hiện hữu đều vượt qua các tiêu chí mới của Gate 8.
