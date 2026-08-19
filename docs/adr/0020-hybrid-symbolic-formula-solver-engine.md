# ADR 0020: Hybrid Symbolic Formula Solver Engine for Normative Engineering Calculations

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-19
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0011: Atomic Clause Chunking](0011-atomic-clause-rag-chunking-strategy.md), [ADR 0016: Dual-Track Hybrid PDF Anchor](0016-dual-track-hybrid-pdf-anchor-of-trust.md), [ADR 0019: Tiered Audit Persona](0019-tiered-audit-persona-and-self-audit-affidavit.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Các quy chuẩn kỹ thuật xây dựng và PCCC Việt Nam (như QCVN 06:2022/BXD, QCVN 04:2021/BXD, TCVN 7336:2021, TCVN 3890:2023) chứa nhiều công thức kỹ thuật và bảng tra đa chiều:
- Công thức tính toán thủy lực, lưu lượng cấp nước chữa cháy, áp suất dư buồng thang bộ, lưu lượng hút khói hành lang, diện tích khoang cháy theo bậc chịu lửa.
- Khi triển khai AI QC Audit Pipeline:
  * Nếu để Large Language Models (LLMs) tự tính toán số học trực tiếp từ văn bản quy chuẩn (*Mental Arithmetic / In-context Calculation*), sẽ phát sinh rủi ro **sai số số học (Arithmetic Drift / Calculation Hallucination)** đối với các phép tính căn bậc hai, phân số hoặc số mũ.
  * Các cơ quan thẩm duyệt (Sở Xây dựng, Cảnh sát PC07) yêu cầu bảng tính giải trình phải minh bạch từng bước thế số và kết quả số học phải tuyệt đối chính xác theo quy chuẩn.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định thiết lập **Động Cơ Tính Toán Công Thức Kỹ Thuật Lai Ghép (Hybrid Symbolic Formula Solver Engine)**:

1. **Phân Công Vai Trò Kiến Trúc (Architectural Role Separation):**
   - **LLM / AI Vision:** Đóng vai trò **Trích xuất Tham số (Parameter Extractor)** — đọc bản vẽ thiết kế để lấy các biến đầu vào (Diện tích $S$, Chiều cao $H$, Thể tích $V$, Bậc chịu lửa, Hạng nguy hiểm cháy).
   - **Python Formula Solver Engine (`formulas/`):** Đóng vai trò **Thực Thi Phép Tính Số Học Xác Định ($100\%$ Deterministic Calculator)** — nhận tham số đầu vào và chạy các hàm thuần túy (`pure functions`) để trả về kết quả số học chính xác.

2. **Cấu Trúc Mô-đun Công Thức (`formulas/`):**
   Mỗi công thức kỹ thuật trong quy chuẩn được đóng gói thành một hàm Python độc lập:
   ```python
   # formulas/fire_water_calc.py
   def calc_outdoor_fire_water_demand(
       building_volume_m3: float, 
       fire_resistance_rating: str, 
       hazard_category: str
   ) -> dict:
       """Tính toán lưu lượng nước chữa cháy ngoài nhà theo Bảng 8 QCVN 06:2022/BXD."""
       ...
   ```

3. **Liên Kết Hai Chiều (Bi-directional Linking in OKF Markdown):**
   - Trong tệp Markdown quy chuẩn, mỗi công thức được gắn kèm `formula_id`:
     ```markdown
     $$Q = q \times N$$ <!-- formula_id: "F_FIRE_WATER_Q06" -->
     ```
   - Cây AST `clauses.json` lưu trường `formula_ref: "formulas.fire_water_calc.calc_outdoor_fire_water_demand"`.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Độ chính xác số học $100\%$:** Triệt tiêu hoàn toàn rủi ro ảo giác tính toán của LLM.
- **Minh bạch giải trình:** Hệ thống có thể tự động xuất báo cáo thế số chi tiết từng bước (Step-by-step substitution report) nộp Sở Xây dựng và Cảnh sát PC07.
- **Kiểm thử hồi quy tự động:** Toàn bộ công thức được bảo vệ bằng hệ thống Unit Tests với dữ liệu kiểm chuẩn (*Ground Truth Benchmark*).

### Đánh đổi:
- Cần công sức mã hóa và duy trì thư viện các hàm tính toán kỹ thuật trong thư mục `formulas/`.
