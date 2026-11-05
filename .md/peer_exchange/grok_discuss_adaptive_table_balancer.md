---
request_id: "req-spoke-adaptive-table-balancer-001"
verdict: "APPROVE_WITH_CONDITIONS"
risk_score: 2
conditions:
  - id: "COND-07"
    description: "Tham số hóa Heuristic đo ký tự theo cỡ chữ (Font-Scale Parametrization): CẤM dùng hệ số cứng '50 DXA/ký tự' cho mọi bảng. BẮT BUỘC tính bề rộng ký tự theo công thức co dãn: char_width_dxa = round(font_size_pt * 5.8) (ví dụ Arial 8.5 pt = 49 DXA, Times New Roman 13 pt = 75 DXA). Đồng thời, mọi vai trò cột bắt buộc phải có sàn chặn dưới an toàn (Floor Constraint W_min): ROLE_INDEX >= 600 DXA, ROLE_DISCRETE >= 1400 DXA, ROLE_FEEDBACK >= 2200 DXA."
    blocking: true
  - id: "COND-08"
    description: "Hỗ trợ Phân bổ Đa cột Trọng tâm (Multi-Primary Weighted Distribution): Mở rộng mô hình phân bổ không gian dư thừa cho phép nhiều cột mang vai trò PRIMARY hoặc COMPARATIVE thông qua tỷ lệ trọng số (weight ratio). Với bảng so sánh song song (Quy định cũ vs Quy định mới, Ý kiến thẩm tra vs Giải trình tư vấn), phần không gian dư thừa W_residual = W_available - sum(W_ancillary) bắt buộc chia đều 1:1 hoặc theo trọng số w_j / sum(w_k), không để mô hình 1 cột PRIMARY đơn lẻ gây nghẽn cấu trúc."
    blocking: true
  - id: "COND-09"
    description: "Bảo toàn Tính tương thích ngược & Cơ chế Opt-In (Strict OpenXML Invariant): Cưỡng chế cơ chế kiểm tra điều kiện hình học trước khi tiêm tblLayout='fixed': Tổng các giá trị gridCol trong w:tblGrid BẮT BUỘC bằng chính xác w:tblW (sai số 0 DXA). Hàm sinh bảng thích ứng trong packages/ccba-ooxml phải là Seam mới độc lập (build_adaptive_fixed_table) hoặc kích hoạt qua cờ layout_mode='adaptive_fixed', không can thiệp ngầm làm hỏng các bảng có gridSpan phức tạp hoặc nested tables cũ."
    blocking: true
  - id: "COND-10"
    description: "Tuân thủ Ranh giới Spoke vs Hub (ADR-0061 & ADR-0045): Nghiêm cấm Spoke ccba-legal-knowledge tự tạo module Python nội bộ trong scripts/ hoặc packages/. Toàn bộ mã nguồn động cơ Cân bằng Cột Thích ứng đóng gói trực tiếp trên Hub monorepo tại packages/ccba-ooxml/src/ccba_ooxml/table/grid_balancer.py và tài liệu đặc tả Tầng 2 tại standards/structure/docx-table-grid-invariants.md. Spoke chỉ cập nhật PR #559 và giữ vững ngân sách 15/15 scripts."
    blocking: true
effort: "S"
summary: "Phê duyệt kiến trúc điển hình hóa Động cơ Cân bằng Cột Thích ứng và Bất biến OpenXML Fixed Grid. Giải pháp giải quyết dứt điểm lỗi Word AutoFit gây méo cột, giảm ngoạn mục 45% số trang in, và tạo ra năng lực cốt lõi cho ccba-xu-ly-van-phong, ccba-completion-checklist và ccba-legal-advisor. Yêu cầu tuân thủ 4 điều kiện phong tỏa COND-07 đến COND-10."
---

# Phản Biện Kiến Trúc — Điển Hình Hóa Động Cơ Cân Bằng Cột Thích Ứng (Adaptive Table Balancer)

- **Phán quyết Thẩm định:** **`APPROVE_WITH_CONDITIONS`** (Chấp thuận kèm 4 Điều kiện Phong tỏa Kỹ thuật)
- **Điểm Rủi ro Kiến trúc:** **2/5** (Rủi ro thấp, giá trị thực tiễn rất cao)
- **Hồ sơ Thẩm định:** `req-spoke-adaptive-table-balancer-001`
- **Chuyên gia Phản biện:** Grok 4.7 xhigh (Adversarial Auditor & Gatekeeper)
- **Ngày lập:** 2026-10-23
- **Thực thể Đề xuất:** Antigravity (Pair Architect & Builder) & Kỹ sư Vũ Văn Chủ (Giám đốc Trung tâm CCBA)

---

## 1. ĐÁNH GIÁ TỔNG QUAN & PHÂN TÍCH HIỆU QUẢ THỰC CHỨNG

Grok đánh giá rất cao việc Antigravity và Kỹ sư Vũ Văn Chủ đã **phát hiện và truy vết đến tận cùng bản chất OpenXML DOM** của hiện tượng bất đối xứng thị giác (Visual Asymmetry) giữa Microsoft Word và PDF Engine (LibreOffice).

### Những Điểm Sáng Vượt Trội của Đề Xuất:
1. **Truy đúng nguyên nhân gốc rễ (Accurate RCA):** Khẳng định chính xác sự thiếu vắng của `<w:tblLayout w:val="fixed"/>` và `<w:tblGrid>` là nguồn cơn kích hoạt thuật toán `AutoFit to Contents` của Microsoft Word, dẫn đến hiện tượng Cột 2 tự động nở to đè bẹp Cột 3 và Cột 4.
2. **Hiệu quả thực chứng ngoạn mục (Measured Empirical Value):**
   - RFI 01: Từ **11 trang** giảm xuống còn **6 trang** (giảm $-45.5\%$ số trang in).
   - RFI 02: Từ **5 trang** giảm xuống còn **4 trang** (giảm $-20.0\%$ số trang in).
   - Cột 2 (Nội dung & Đề xuất) được mở rộng thêm **$+21.2\%$ diện tích** ($3400 \to 4121\text{ DXA}$), giải phóng hoàn toàn không gian cho khối `💡 Đề xuất của Tư vấn` trải dài thanh thoát trên 2 dòng liền mạch thay vì bị bẻ vụn thành 5 dòng ngắn.
3. **Tầm nhìn nền tảng (Platform Architectural Vision):** Việc đề xuất điển hình hóa từ một script cục bộ thành một Seam dùng chung cho `/ccba-xu-ly-van-phong`, `ccba-completion-checklist`, và `ccba-legal-advisor` hoàn toàn khớp với triết lý **Platform-Aware KISS (ADR-0061)**: Giải quyết một lần ở tầng Seam của Hub, toàn bộ các Spoke tự động hưởng lợi.

---

## 2. PHẢN BIỆN ADVERSARIAL CHI TIẾT ĐỐI VỚI 4 CÂU HỎI THAM VẤN

### Câu hỏi 1: Về Giả định Đo lường Ký tự (Font Metrics vs Heuristic)
- **Phản biện của Grok:**
  Hệ số `50 DXA/ký tự` hiện tại là đúng và tối ưu cho phông chữ không chân cỡ nhỏ (Arial 8.5 pt - 9.5 pt). Tuy nhiên, nếu mang nguyên vẹn con số 50 DXA này áp dụng cho văn bản hành chính theo Nghị định 30 (vốn bắt buộc dùng phông có chân **Times New Roman cỡ 13 pt - 14 pt**), hệ thống sẽ gặp sự cố nghiêm trọng:
  - Bề rộng trung bình của một ký tự Times New Roman 13 pt là khoảng $72 - 78\text{ DXA}$ (lớn hơn 50% so với Arial 8.5 pt).
  - Khi đó, Cột `DISCRETE` hoặc `INDEX` sẽ bị tính thiếu không gian, khiến văn bản bị rớt dòng ngoài ý muốn.
- **Ràng buộc phong tỏa (COND-07):**
  Bắt buộc tham số hóa bề rộng ký tự theo cỡ phông:
  $$\text{char\_width\_dxa} = \text{round}(\text{font\_size\_pt} \times 5.8)$$
  Đồng thời, áp đặt **Sàn an toàn tối thiểu (Floor Constraints)** không thể phá vỡ:
  - $W_{\text{INDEX}} \ge 600\text{ DXA}$
  - $W_{\text{DISCRETE}} \ge 1400\text{ DXA}$
  - $W_{\text{FEEDBACK}} \ge 2200\text{ DXA}$

---

### Câu hỏi 2: Về Độ Phủ của 5 Vai Trò Ngữ Nghĩa (Taxonomy & Multi-Primary Columns)
- **Phản biện của Grok:**
  Mô hình 5 vai trò ngữ nghĩa (`INDEX`, `DISCRETE`, `FEEDBACK`, `COMPARATIVE`, `PRIMARY`) là rất toàn diện, phản ánh đúng các dạng bảng trong ngành xây dựng và pháp lý.
  Tuy nhiên, **điểm nghẽn tiềm ẩn** nằm ở công thức $W_{\text{primary}} = W_{\text{available}} - \sum W_{\text{ancillary}}$: Nó chỉ đúng khi trong bảng chỉ có DUY NHẤT 1 cột văn bản dài.
  Trong thực tế CCBA có rất nhiều bảng có **2 cột văn bản dài song song**:
  - Bảng so sánh VBHN (Quy định cũ vs Quy định mới).
  - Biên bản giải trình thẩm tra thiết kế (Ý kiến thẩm tra vs Giải trình của Tư vấn).
  - Bảng đối chiếu tiêu chuẩn tương đương (Tiêu chuẩn Việt Nam vs Tiêu chuẩn Quốc tế/NFPA).
- **Ràng buộc phong tỏa (COND-08):**
  Bộ phân bổ phải hỗ trợ mảng nhiều cột `PRIMARY` hoặc `COMPARATIVE`. Khi phát hiện có $k \ge 2$ cột chính, phần không gian dôi dư $W_{\text{residual}}$ sẽ được phân chia theo tỷ lệ trọng số:
  $$W_j = W_{\text{residual}} \times \frac{w_j}{\sum_{m=1}^k w_m}$$
  Mặc định với 2 cột so sánh là tỷ lệ $1:1$ (mỗi bên nhận 50% phần dư).

---

### Câu hỏi 3: Về Khả Năng Tương Thích Ngược & Cơ Chế Opt-In
- **Phản biện của Grok:**
  Trong chuẩn OpenXML ECMA-376, bảng có thuộc tính `<w:tblLayout w:val="fixed"/>` đòi hỏi tính kỷ luật hình học tuyệt đối. Nếu một bảng có ô gộp ngang (`w:gridSpan`) ở nhiều tầng mà tổng độ rộng của các ô con không khớp chính xác với tọa độ trong `<w:tblGrid>`, Microsoft Word sẽ gặp lỗi hiển thị nghiêm trọng.
- **Ràng buộc phong tỏa (COND-09):**
  - Không được ghi đè hành vi của các hàm tạo bảng nguyên thủy cũ trong `python-docx`.
  - Phải cung cấp một Seam API mới độc lập: `build_adaptive_fixed_table()` trong package `packages/ccba-ooxml`.
  - Bắt buộc kiểm tra điều kiện tiên quyết: $\sum \text{gridCol} == \text{tblW}$ (sai số tuyệt đối $= 0\text{ DXA}$).

---

### Câu hỏi 4: Về Phân Định Ranh Giới Spoke vs Hub (ADR-0061)
- **Phản biện của Grok:**
  Spoke `ccba-legal-knowledge` hiện đang duy trì ngân sách script ở mức tối ưu ($15/15$ scripts quy chuẩn, bảo toàn 15 cổng kiểm định CI).
  Tuyệt đối không được "tiện tay" tạo thêm module Python mới hoặc công cụ tiện ích trong thư mục `scripts/` của Spoke này.
- **Ràng buộc phong tỏa (COND-10):**
  - Spoke chỉ giữ vai trò là "nơi ươm tạo thực chứng" (Incubation Ground).
  - Toàn bộ code triển khai Seam `grid_balancer.py` và cập nhật tiêu chuẩn Tầng 2 (`docx-table-grid-invariants.md`) phải được đẩy lên Hub monorepo (`packages/ccba-ooxml`).
  - Cập nhật thông tin vào Pull Request [vvChu/ccba-agent-platform#559](https://github.com/vvChu/ccba-agent-platform/pull/559).

---

## 3. KẾT LUẬN & CHỈ THỊ HÀNH ĐỘNG

Grok chính thức phê duyệt đề xuất điển hình hóa Động cơ Cân bằng Cột Thích ứng với phán quyết:
$$\mathbf{VERDICT = APPROVE\_WITH\_CONDITIONS}$$

### Các Bước Triển Khai Tiếp Theo:
1. ✅ **Ghi nhận 4 điều kiện phong tỏa COND-07 đến COND-10** vào hồ sơ đề xuất RFC trên Hub monorepo.
2. ✅ **Cập nhật PR #559 trên Hub**: Bổ sung tài liệu đặc tả `docx-table-grid-invariants.md` tại Tầng 2 của `ccba-xu-ly-van-phong` với công thức cỡ phông và cơ chế phân bổ đa cột chính.
3. ✅ **Báo cáo kết quả thảo luận cho Kỹ sư Vũ Văn Chủ**: Trình bày rõ ràng cơ chế phân bổ theo vai trò ngữ nghĩa và khẳng định tính sẵn sàng của giải pháp trên toàn bộ các dòng sản phẩm văn phòng của CCBA.
