# ADR 0039: Bóc Tách Sơ Đồ Đồ Họa Độ Nét Cao & Bảo Tồn Tuyệt Đối Chú Thích Kẹp Giữa (Universal High-Fidelity Diagram Extraction & Annotation Governance)

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-09-01)

## 2. Bối Cảnh (Context)
Trong các Tiêu chuẩn Kỹ thuật Quy chuẩn Xây dựng (TCVN 2737, TCVN 5574, QCVN 06...), các sơ đồ hình vẽ đồ họa, phân vùng khí động và biểu đồ tra cứu là **Thành phần Trực quan Bắt buộc**.
1. **Lỗi nuốt text trong bảng bố cục không viền (Borderless Diagram Layout Table Drop):** Người soạn thảo DOCX thường dùng bảng 2 cột không viền để đặt hình ảnh ở cột trái và công thức/chú dẫn phụ bên phải (ví dụ: $e = \min(b; 2h)$, $b\text{ là cạnh vuông góc hướng gió}$). Bộ trích xuất ảnh cũ chỉ lấy ảnh raster và bỏ qua text ở ô bên cạnh.
2. **Lỗi rơi rụng Chú thích kẹp giữa (Sandwiched Notes & Legend Dropping):** Các đoạn `CHÚ THÍCH 1`, `CHÚ THÍCH 2` hoặc `CHÚ DẪN` nằm giữa ảnh và tiêu đề hình `Hình X — ...` bị cơ chế dò ngược lùi của converter cũ nuốt mất, làm mất đi các điều kiện nội suy kỹ thuật quan trọng.
3. **Lỗi co cụm và cắt xén mép kích thước (Horizontal Squeeze & Dimension Clipping):** Việc ghép ngang các sơ đồ con đa phần tử ($a, b, c$) vào cùng một hàng ngang làm co hẹp bề rộng, dẫn đến việc bị crop mất đường dóng kích thước ở cạnh biên hoặc mất chú giải dưới đáy.
4. **Lỗi thẻ HTML trong tiêu đề hình ảnh:** Tiêu đề hình ảnh sinh ra các thẻ HTML `<sub>` không đồng bộ (`c<sub>e</sub>`, `c<sub>x</sub>`, `c<sub>β</sub>`, `k<sub>λ</sub>`), làm giảm tính nhất quán thẩm mỹ với các biểu thức KaTeX trong thân văn bản.

---

## 3. Quyết Định Thiết Kế (Decision)

Hệ thống thiết lập **Tiêu chuẩn Bóc tách Sơ đồ Đồ họa & Bảo tồn Chú giải Toàn diện (ADR 0039)**:

### A. Cơ Chế Bóc Tách Bảng Bố Cục Không Viền (Universal Layout-Table Inspector)
- Quét toàn diện các bảng 2 cột không viền trong tệp DOCX. Nếu bảng chứa 1 ô ảnh raster và 1 ô text ngắn chứa tham số/công thức hình học, converter tự động nhận diện đây là *Layout Diagram Table* và trích xuất nguyên vẹn khối chú dẫn tham số gắn liền với hình ảnh.

### B. Cơ Chế Bảo Tồn Tuyệt Đối Chú Thích & Chú Dẫn Kẹp Giữa (Sandwiched Annotation Preserver)
- Trong `figure_handler.py`, quét toàn bộ vùng đệm văn bản nằm giữa khối ảnh và tiêu đề hình ảnh.
- Cưỡng chế trích xuất và bảo toàn $100\%$ các đoạn `CHÚ THÍCH` (kể cả đánh số 1, 2, 3...) và `CHÚ DẪN`, đặt trang trọng và chuẩn xác ngay bên dưới hình ảnh trong Markdown.

### C. Quy Chuẩn Xếp Dọc Đa Tầng & Chống Cắt Xén Mép (Vertical Multi-Tier Stacking & Safe Canvas Margin)
- Đối với các hình có nhiều sơ đồ con phức tạp (như Hình F.1, F.4, F.6, F.7), ưu tiên áp dụng bố cục **Xếp dọc đa tầng (Vertical Stack)** theo thứ tự logic $a) \rightarrow b) \rightarrow c)$.
- Thiết lập bề rộng canvas tiêu chuẩn ($660 - 720\text{ px}$) cùng khoảng đệm an toàn tối thiểu $\ge 40\text{ px}$ ở cả 4 cạnh, bảo đảm $100\%$ đường dóng kích thước và nhãn phụ không bao giờ bị cắt xén.

### D. Chuẩn Hóa KaTeX Cho Toàn Bộ Tiêu Đề Hình & Bảng (Universal KaTeX Caption Normalization)
- Mọi ký hiệu chỉ số dưới trong tiêu đề hình ảnh và bảng biểu được tự động chuyển đổi từ HTML `<sub>` sang KaTeX chuẩn (`$c_e$`, `$c_x$`, `$c_\beta$`, `$c_{x\infty}$`, `$k_\lambda$`), đảm bảo tính nhất quán toán học toàn cầu.

### E. Cổng Kiểm Định Chống Rơi Rụng Chú Thích (Gate 11.2 Zero-Dropped Regulatory Notes CI Gate)
- Tích hợp kiểm định tự động trong `scripts/validate_legal_spoke.py`: Đối soát $100\%$ từng đoạn `CHÚ THÍCH` và `CHÚ DẪN` trong tệp DOCX gốc với Markdown. Bất kỳ sự thiếu sót nào đều kích hoạt lỗi chặn quy trình nghiệm thu.

---

## 4. Hệ Quả & Lợi Ích (Consequences)
- **100% Bảo Tồn Nguyên Văn Chú Thích Quy Phạm:** Không bao giờ bị mất bất kỳ chú thích kỹ thuật, điều kiện nội suy hay chú dẫn sơ đồ nào.
- **Hình Ảnh Sơ Đồ Đạt Chuẩn Xuất Bản:** Sơ đồ sắc nét, đầy đủ kích thước và nhãn phụ, tương thích $100\%$ với PDF Công báo gốc.
- **Tự Động Hóa Toàn Trình:** Các workflows nạp tài liệu mới (`ccba-legal-ingest`) chạy tự động $100\%$ mà không cần can thiệp thủ công.
