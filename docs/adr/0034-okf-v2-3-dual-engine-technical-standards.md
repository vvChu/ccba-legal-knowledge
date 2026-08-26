# ADR 0034: OKF v2.3 Dual-Engine Technical Standards Paradigm (Parametric Visual Cards, Lossless Table Matrices & Deterministic Solvers)

- **Trạng thái:** ACCEPTED & ADOPTED (Đã chấp thuận & Áp dụng)
- **Ngày quyết định:** 2026-08-26
- **Tác giả:** CCBA Legal Intelligence & Engineering Automation Architecture Team
- **Liên quan:** [ADR 0020: Hybrid Symbolic Formula Solver Engine](0020-hybrid-symbolic-formula-solver-engine.md), [ADR 0021: OKF v2.2 Pure Normative Body](0021-okf-v2-2-pure-normative-body-legal-graph.md), [ADR 0027: Specialized AST Converter for TCVN/QCVN](0027-tcvn-qcvn-specialized-ast-converter.md), [ADR 0030: Visual Parity & 2D Annex Navigation Matrix](0030-visual-parity-and-2d-navigation-matrix.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Văn bản quy chuẩn kỹ thuật xây dựng (TCVN, QCVN, Eurocode, ASCE, ISO) có cấu trúc thông tin phi tuyến tính và phức tạp hơn rất nhiều so với văn bản quy phạm pháp luật hành chính thông thường (Luật, Nghị định, Thông tư):
1. **Sơ đồ hình học đa nhánh (Multi-branching Geometric Figures):** Một hình vẽ kỹ thuật thường bao gồm nhiều mặt cắt, mặt bằng và các trường hợp rẽ nhánh hình học theo tỷ lệ kích thước (ví dụ: Hình F.1 phân nhánh theo $L > 4h, 2h < L \le 4h, L \le 2h$; Hình F.6 có mặt cắt trên đỉnh và 2 mặt bằng góc gió $\theta = 0^\circ, 90^\circ$ bên dưới).
2. **Ma trận bảng tra đa chiều với giá trị kép (Multi-Tier Matrix Tables with Dual Values):** Các bảng tra hệ số khí động (như Bảng F.3a, F.5a, F.6 trong TCVN 2737:2023) chứa đồng thời áp lực hút âm và áp lực đẩy dương trên cùng một ô, phụ thuộc vào góc dốc $\alpha$ và góc hướng gió $\theta$.
3. **Công thức giải tích thế số đan xen (Analytical Math Equations):** Chứa nhiều ký tự Hy Lạp, chỉ số dưới, số mũ và công thức phân đoạn.
4. **Nhu cầu tự động hóa thẩm duyệt thiết kế BIM:** Large Language Models (LLMs) dễ bị ảo giác số học (hallucination) khi tra bảng đa trị hoặc nội suy phi tuyến tính; các công cụ kiểm tra mô hình BIM (IFC) cần các hàm tính toán xác định ($100\%$ deterministic) thay vì prompt LLM ngẫu nhiên.

---

## 2. Quyết Định Kiến Trúc: Chuẩn OKF v2.3 (Decision)

Chúng tôi quyết định nâng cấp chuẩn đóng gói tri thức pháp lý lên **OKF v2.3 Dual-Engine Technical Standards Paradigm**, cưỡng chế thực hiện **4 Trụ Cột Bất Biến**:

```
                    ┌────────────────────────────────────────────────────────┐
                    │      CHUẨN OKF v2.3 DUAL-ENGINE TECHNICAL STANDARDS    │
                    └────────────────────────────────────────────────────────┘
                                                 │
         ┌───────────────────────┬───────────────┴───────────────┬───────────────────────┐
         ▼                       ▼                               ▼                       ▼
【TRỤ CỘT 1: FIGURES】    【TRỤ CỘT 2: TABLES】           【TRỤ CỘT 3: MATH】    【TRỤ CỘT 4: DUAL-ENGINE】
Unified Centered        Lossless Multi-Tier             Pure KaTeX Blocks       Visual Cards (JSON)
Composite Images        Matrix Tables                   `$$ ... \tag{X.Y} $$`    + Solvers (Python)
```

### 🖼️ Trụ cột 1 — Unified Centered Composite Images (Ảnh ghép đơn nhất căn giữa)
- **Cấm:** Tuyệt đối không chèn các mảnh ảnh nhỏ cắt rời rạc rồi dùng thẻ HTML inline (`<p align="center">`) dồn cục làm vỡ layout văn bản gốc.
- **Quy tắc:** Sử dụng công cụ tự động (`PIL.Image`) để ghép các sơ đồ mặt cắt, mặt bằng và nhãn phụ (`a)`, `b)`, `c)`) thành **một file ảnh composite đơn nhất** (`hinh_*.png`) trên nền trắng chuẩn RGB, căn giữa đồng nhất bằng `<p align="center">`.

### 📊 Trụ cột 2 — Lossless Multi-Tier Matrix Tables (Bảo toàn ma trận bảng tra đa chiều)
- **Quy tắc:** Bảo toàn $100\%$ số cột của bảng tra theo văn bản gốc.
- **Giá trị kép:** Các ô chứa đồng thời giá trị dương và âm (ví dụ: $-1{,}7 / +0{,}0$) được định dạng bằng thẻ `<br>` (ví dụ: `- 1,7<br>+ 0,0`).
- **Tách chú thích:** Toàn bộ ghi chú điều kiện biên và chú dẫn ký hiệu được đưa ra ngoài khung bảng Markdown (đặt ngay bên dưới bảng) để tránh làm méo mó cấu trúc bảng.

### 🧮 Trụ cột 3 — Pure KaTeX Mathematical Formulation (100% Công thức Toán học KaTeX)
- **Quy tắc:** Triệt tiêu hoàn toàn các ảnh bitmap công thức scan mờ.
- **Định dạng:** Mọi phương trình kỹ thuật phải được biểu diễn bằng KaTeX khối kèm số hiệu phương trình:
  ```latex
  $$V(z_e)_{3600\text{s}, 50} = 0{,}68 \cdot V_{3\text{s}, 50} \cdot \left(\frac{z_e}{10}\right)^{\bar{\alpha}} \tag{F.2}$$
  ```

### ⚙️ Trụ cột 4 — Kiến Trúc Song Mã (Visual Cards & Deterministic Solvers)
- **Thẻ thị giác tham số hóa (Visual Cards JSON - `figures/cards/`):**
  * Mỗi sơ đồ hình học quan trọng được đặc tả bằng 1 file JSON theo schema `visual_card_v1.json`, khai báo tham số đầu vào (`length_L`, `height_h`, `building_width_b`), quy tắc phân vùng kích thước (`e = min(b, 2h)`), và cây quyết định rẽ nhánh.
  * Engine nạp thẻ (`formulas/visual_card_engine.py`) chịu trách nhiệm tính toán kích thước thực tế của từng phân vùng khí động từ kích thước hình học mô hình công trình.
- **Bộ giải tính toán số học xác định (Deterministic Solvers - `formulas/`):**
  * Mỗi bảng tra và công thức giải tích được lập trình thành hàm Python thuần túy (`pure functions`) trong `formulas/wind_load_tcvn2737.py` (hoặc module tương ứng).
  * Xử lý nội suy 2 chiều, phân tách kịch bản tải trọng độc lập (Trường hợp Hút âm vs Trường hợp Đẩy dương), và xuất báo cáo thuyết minh thế số từng bước (`CalculationResult.format_text_report()`).
  * Đăng ký tập trung vào `SymbolicFormulaSolver` Facade.

---

## 3. Quy Trình Kiểm Định Nghiệm Thu (Verification & CI Gate)

Mọi văn bản quy chuẩn kỹ thuật đóng gói theo OKF v2.3 bắt buộc vượt qua:
1. **Master CI Validator (`validate_legal_spoke.py`):** $10/10$ Cổng kiểm định (Registry, Bundles, Tables, Fake Data, PDF Metadata, Pure Body, Cleanliness, Atomic Templates, Visual Parity, Living Traceability) $\to$ **0 Errors, 0 Warnings**.
2. **Formula & Visual Card Unit Test Suite:** Bộ kiểm thử tự động với dữ liệu kiểm chuẩn (*Ground Truth Benchmark*) kiểm tra tính đúng đắn số học $100\%$ và tính toàn vẹn của Visual Cards JSON.

---

## 4. Hệ Quả (Consequences)

### Tích cực:
- **Trải nghiệm đọc thị giác hoàn hảo:** Bố cục tài liệu Markdown hiển thị sắc nét, cân đối, trung thực $100\%$ với bản in PDF Công báo gốc.
- **Triệt tiêu ảo giác tính toán:** Toàn bộ phép tính kỹ thuật được giao cho Python thực thi xác định, đảm bảo tính pháp lý tuyệt đối cho hồ sơ thẩm tra.
- **Sẵn sàng tích hợp BIM tự động:** Các Visual Cards và Solvers có thể kết nối trực tiếp với mô hình IFC (`ifcopenshell`) để tự động kiểm tra quy chuẩn thiết kế.

### Đánh đổi:
- Cần đầu tư công sức xây dựng Visual Cards và Solvers kèm bộ Unit Test Ground Truth cho mỗi phụ lục kỹ thuật mới.
