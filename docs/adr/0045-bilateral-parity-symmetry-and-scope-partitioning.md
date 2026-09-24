# ADR 0045: Kiểm Định Ground Truth Parity Song Mã & Phân Định Phạm Vi Thân Quy Phạm (Bilateral Parity Symmetry & Scope Partitioning Invariant)

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-09-24)  
*Hội tụ thông qua Chu trình Học tập Kiến trúc `/learn` & Đợt Thẩm định Đối kháng Chuyên sâu (RULE-4.4 session_learnings.md).*

---

## 2. Bối Cảnh (Context)
Trong quá trình mở rộng kho tri thức pháp lý lên 57 văn bản quy phạm và vận hành hệ thống kiểm định ban đêm (Nightly Telemetry):
1. **Điểm Nghẽn Nhánh Vector PDF & Tính Mong Manh Thuật Toán:**
   - Một số văn bản quy chuẩn, tiêu chuẩn và văn bản quy phạm pháp luật không có tệp `.docx` gốc trong Công báo mà chỉ có tệp Vector PDF số hóa.
   - Nhánh kiểm tra Vector PDF trước đây sử dụng giải thuật cửa sổ trượt 8 từ cứng nhắc, dễ bị gãy chuỗi so khớp khi gặp công thức KaTeX nội dòng, thẻ neo HTML (`<a id="...">`) hoặc sự đảo lộn thứ tự dòng của bảng biểu nhiều cột.
2. **Bất Đối Xứng Giải Thuật (Algorithmic Asymmetry):**
   - Nhánh PDF được trang bị state-machine nhận diện ranh giới hành chính (`in_signatory`, `in_bibliography`), nhưng nhánh DOCX lại thiếu các bộ lọc tương đương, tạo ra rủi ro rớt điểm bất đối xứng khi xử lý các tệp DOCX có danh sách nơi nhận dài.
3. **Thách Thức Từ Các Văn Bản Quy Phạm Có Phụ Lục Kỹ Thuật Quy Mô Lớn:**
   - Các thông tư như Thông tư 38/2026/TT-BXD có 2 trang thân Thông tư nhưng đi kèm 8 phụ lục định mức dự toán với 1.891 trang; hoặc Nghị định 105/2025/NĐ-CP có 37 trang thân quy phạm kèm 66 trang biểu mẫu hành chính.
   - Theo chuẩn OKF v2.4 (ADR 0036), các phụ lục định mức và biểu mẫu được phân tách rạch ròi sang `templates/` và `tables/`. Việc đối soát toàn văn tệp PDF công báo nguyên khối với thân Markdown đơn lẻ sẽ làm sai lệch điểm Parity.
4. **Nguy Cơ Bẫy Cắt Xén Nhân Tạo (Vacuous Pass Anti-Pattern):**
   - Cần một rào chắn chống lại hành vi tùy tiện cắt ngắn phạm vi kiểm tra để né tránh các phụ lục quy phạm chưa được số hóa (như từng cân nhắc cắt NĐ 210 tại trang 21).

---

## 3. Quyết Định Thiết Kế (Decision)

Hệ thống thiết lập **Bất biến Kiểm Định Ground Truth Parity Song Mã & Phân Định Phạm Vi Thân Quy Phạm (ADR 0045)**:

### A. Đối Xứng Song Mã & Giải Thuật Block Multi-Span Coverage
1. **Giải Thuật Block Multi-Span Coverage:**
   - Cả hai nhánh DOCX và Vector PDF áp dụng giải thuật đối soát `check_multi_span_coverage(p_words, norm_md, min_span=4, min_ratio=0.70)` trên từng khối đoạn văn bản (`page.get_text("blocks")` đối với PDF và paragraph blocks đối với DOCX).
   - Tỷ lệ bao phủ từ vựng tích lũy tối thiểu đạt $70\%$ trên từng khối đoạn văn bản, mang lại độ dung sai tự nhiên đối với ô bảng biểu đa cột và công thức toán học nội dòng.
2. **Chuẩn Hóa Văn Bản Triệt Để:**
   - Bóc sạch toàn bộ thẻ HTML trình diễn (`re.sub(r"</?[a-zA-Z][^>]*>", " ", text)`).
   - Làm phẳng cú pháp link Markdown (`[text](url)` $\rightarrow$ `text`).
   - Lọc bỏ các số trang độc lập dạng `^\d+$` sinh ra từ header/footer PDF.
3. **Đồng Bộ Đối Xứng State-Machine Hai Chiều (Bilateral Symmetry):**
   - Cả 2 nhánh DOCX và PDF bắt buộc nhận diện nhất quán:
     * `in_preamble`: Tự động bỏ qua căn cứ pháp lý ban hành mở đầu (ADR 0021 Pure Body).
     * `in_signatory`: Tự động nhận diện khối danh sách gửi nhận và chức danh ký duyệt hành chính (`Nơi nhận:`, `KT. BỘ TRƯỞNG`, `KT. THỦ TƯỚNG`, `TM. CHÍNH PHỦ`, `THỦ TƯỚNG`, `PHÓ THỦ TƯỚNG`, `THỨ TRƯỞNG`) và tự động kích hoạt trở lại khi gặp `PHỤ LỤC`.
     * `in_bibliography`: Tự động nhận diện và bỏ qua danh mục tài liệu tham khảo không quy phạm cuối tiêu chuẩn.

### B. Phân Định Phạm Vi Thân Quy Phạm & Rào Chắn Chống Cắt Xén Nhân Tạo (Anti-Vacuous Pass)
1. **Khai Báo Phạm Vi Thân Quy Phạm (`verification_scope`):**
   - Đối với các văn bản có hàng trăm/hàng nghìn trang biểu mức định mức dự toán hoặc biểu mẫu hành chính đã được bóc tách độc lập sang `templates/`, `tables/` hoặc `annexes/`, cho phép khai báo phạm vi trong `metadata.yaml`:
     ```yaml
     verification_scope:
       normative_body_pages: [start_page, end_page]
     ```
2. **Quy Tắc Đối Soát Bù Trừ Đối Tượng Ngoại Vi (Anti-Vacuous Pass Invariant):**
   - Khai báo `verification_scope.normative_body_pages` chỉ được chấp nhận là HỢP LỆ khi và chỉ khi:
     * Phần nội dung nằm ngoài phạm vi trang thân quy phạm đã được kiểm chứng có mặt đầy đủ trong `templates/` (biểu mẫu hành chính) HOẶC `tables/` (bảng số liệu/định mức) HOẶC `annexes/` (phụ lục kỹ thuật quy phạm).
     * Nghiêm cấm tuyệt đối việc sử dụng `verification_scope` khi cả 3 ngăn kéo trên đều rỗng.
3. **Bảo Tồn Phụ Lục Quy Phạm Kỹ Thuật (Normative Annex Preservation):**
   - Đối với các phụ lục mang tính quy phạm kỹ thuật (như Phụ lục điều chỉnh giá hợp đồng của NĐ 210/2026/NĐ-CP hoặc Phụ lục tính toán của TCVN 7336:2021), bắt buộc trích xuất nguyên văn $100\%$ vào thư mục `annexes/phu_luc_*.md`, không được phép cắt bỏ khỏi phạm vi kiểm soát tri thức.

---

## 4. Hệ Quả & Tác Động (Consequences)

### Tích Cực
- Đạt tỷ lệ $100\%$ văn bản quy phạm vượt qua Gate 11 Verbatim Parity ($57/57$ văn bản đạt chuẩn $\ge 98.0\%$).
- Đảm bảo tính nhất quán tuyệt đối giữa hai định dạng nguồn DOCX và Vector PDF, triệt tiêu nguy cơ rớt điểm tiềm ẩn khi xuất hiện file DOCX mới.
- Thiết lập rào chắn dữ liệu vững chắc ngăn ngừa việc cắt xén phụ lục nhân tạo, bảo toàn toàn vẹn tri thức pháp lý theo chuẩn OKF v2.4.

---
*Biên soạn bởi CCBA Agent Architecture Council.*
