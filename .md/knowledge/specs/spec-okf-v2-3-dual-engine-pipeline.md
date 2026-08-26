# Đặc Tả Kỹ Thuật: OKF v2.3 Dual-Engine Technical Standards Pipeline

- **Mã Đặc Tả:** `SPEC-OKF-V2-3-DUAL-ENGINE`
- **Trạng Thái:** `ready-for-agent`
- **Ngày Ban Hành:** 2026-08-26
- **Căn Cứ Kiến Trúc:** [ADR 0020](docs/adr/0020-hybrid-symbolic-formula-solver-engine.md), [ADR 0021](docs/adr/0021-okf-v2-2-pure-normative-body-legal-graph.md), [ADR 0030](docs/adr/0030-visual-parity-and-2d-navigation-matrix.md), [ADR 0034](docs/adr/0034-okf-v2-3-dual-engine-technical-standards.md)

---

## Problem Statement

Các tiêu chuẩn quy chuẩn kỹ thuật xây dựng Việt Nam (TCVN, QCVN) chứa cấu trúc thông tin phi tuyến tính phức tạp:
1. **Sơ đồ hình học đa nhánh và nhiều mặt bằng/mặt cắt:** Các hình vẽ bị cắt vụn và chèn inline làm lệch lề tài liệu, vỡ cấu trúc và mất nhãn phân vùng ($a, b, c$).
2. **Ma trận bảng tra đa chiều:** Các bảng tra chứa nhiều cột và giá trị tải trọng kép (Hút âm và Đẩy dương đồng thời) dễ bị cắt cụt dữ liệu khi chuyển đổi Markdown.
3. **Công thức giải tích thế số đan xen:** Các phương trình toán học thường bị quét thành ảnh bitmap chất lượng thấp, không thể tìm kiếm, không thể trích xuất biến số.
4. **Rủi ro ảo giác tính toán của LLM:** Khi AI Agent hoặc công cụ kiểm tra quy chuẩn BIM trực tiếp yêu cầu LLM tính toán hoặc tra bảng, LLM thường gặp hiện tượng sai lệch số học (arithmetic hallucination) và không có khả năng giải trình từng bước minh bạch.
5. **Xử lý thủ công tốn kém:** Việc chuyển đổi từng phụ lục bằng tay mất từ 1-2 ngày mỗi phụ lục và thiếu tính nhất quán giữa các bộ tiêu chuẩn.

---

## Solution

Xây dựng và chuẩn hóa **Đường Ống Xử Lý Tiêu Chuẩn Kỹ Thuật Song Mã (OKF v2.3 Dual-Engine Pipeline)** kết hợp giữa **Tài liệu Markdown Trực quan Hoàn mỹ (Human-Readable Visual Parity)** và **Bộ máy Tính toán Xác định (Machine-Executable Deterministic Engine)**:

1. **Auto-Compositor Module:** Tự động phát hiện các sơ đồ hình học đa nhánh trong DOCX/PDF và ghép thành các ảnh đơn nhất căn giữa (`hinh_*.png`) trên nền trắng, nhúng trực tiếp nhãn phụ (`a)`, `b)`, `c)`).
2. **Lossless Table Matrix Builder:** Tự động giữ nguyên $100\%$ các cột của bảng tra kỹ thuật, chuẩn hóa các ô giá trị kép bằng `<br>`, và đưa chú thích điều kiện biên ra ngoài khung bảng.
3. **KaTeX Math Converter:** Tự động chuyển đổi $100\%$ công thức giải tích sang định dạng LaTeX khối `$$ ... \tag{X.Y} $$`.
4. **Parametric Visual Cards Schema:** Đóng gói mỗi sơ đồ hình học thành file JSON (`figures/cards/*.json`) khai báo quy tắc phân vùng kích thước (`e = min(b, 2h)`) và cây quyết định rẽ nhánh.
5. **Deterministic Symbolic Solvers:** Đóng gói mỗi công thức/bảng tra thành các hàm Python thuần túy trong `formulas/` với khả năng xuất báo cáo thế số giải trình từng bước (`CalculationResult.format_text_report()`).
6. **Master CI Gate Enforcement:** Tích hợp kiểm định tự động vào `scripts/validate_legal_spoke.py` đảm bảo $0$ lỗi layout, $0$ lỗi link, và $100\%$ độ khớp số học.

---

## User Stories

1. As a **BIM Compliance Auditor**, I want to automatically calculate aerodynamic pressure coefficients ($c_e$, $c_x$) for complex building geometries without LLM hallucination, so that my audit reports are $100\%$ legally binding and accurate.
2. As a **Structural Engineer**, I want step-by-step mathematical substitution reports generated automatically from the standards, so that I can submit transparent calculation notes to the Department of Construction (Sở Xây dựng) and Fire Police (PC07).
3. As a **Legal Knowledge Engineer**, I want to convert new annexes of TCVN standards from DOCX/PDF to OKF v2.3 in under 1 minute via a single CLI command, so that I don't have to manually format tables and composite images.
4. As an **AI Agent Architect**, I want a standardized JSON schema for Parametric Visual Cards, so that any downstream AI agent can query geometric zone boundaries unambiguously.
5. As a **BIM Automation Developer**, I want deterministic solver functions exposed via a unified Facade (`SymbolicFormulaSolver.solve`), so that I can plug standard engineering formulas directly into IFC model checking workflows.
6. As a **Quality Control Auditor**, I want automated unit tests verifying solver results against Ground Truth table values, so that any regression or formula bug is caught instantly before merging.
7. As a **Reader / Consultant**, I want all figures in the technical annexes centered, crisp, and high-resolution with integrated sub-figure labels, so that reading the Markdown standard is identical to the official print gazette.
8. As a **RAG Pipeline Engineer**, I want mathematical formulas formatted in pure KaTeX math blocks with equation numbers (`\tag{...}`), so that chunking and semantic search retrieve clean, legible equations instead of broken raster image tags.
9. As a **Civil Engineer**, I want wind load solvers to automatically split dual-value load cases (suction vs pressure) and perform same-sign linear interpolation, so that I don't misinterpret regulatory notes in the tables.
10. As a **Platform Maintainer**, I want all technical annexes governed by a 10-layer Master CI Gate, so that zero formatting clutter, broken links, or fake data ever enter the repository.

---

## Implementation Decisions

### 1. Visual Card JSON Schema (`visual_card_v1.json`)
Mỗi Visual Card tuân thủ schema JSON thống nhất:
```json
{
  "$schema": "https://ccba.vn/schemas/visual_card_v1.json",
  "card_id": "FIG_TCVN2737_FX",
  "figure_number": "F.X",
  "standard": "TCVN 2737:2023",
  "title": "Tên sơ đồ",
  "image_relpath": "figures/images/hinh_f_x.png",
  "normative_clauses": ["F.X.1", "F.X.2"],
  "associated_tables": ["Bảng F.X"],
  "formula_id": "F_WIND_TCVN2737_FX",
  "governing_parameters": ["param1", "param2"],
  "input_parameters": {
    "param1": { "description": "Mô tả", "unit": "m", "type": "float" }
  },
  "dimension_rules": {
    "e_dimension": "min(building_width_b, 2.0 * building_height_h)"
  },
  "zones_definition": { ... }
}
```

### 2. Deterministic Formula Solvers Architecture
- Toàn bộ hàm tính toán phải là `pure functions` nhận tham số số học và trả về `CalculationResult`.
- Hỗ trợ lưu trữ đa vùng (`zone_values: dict[str, float]`) và đa kịch bản tải trọng (`scenarios: dict[str, dict[str, float]]`).
- Tự động xuất báo cáo giải trình thế số theo mẫu:
  * 1. Thông số đầu vào
  * 2. Kết quả phân vùng / Kịch bản tải trọng
  * 3. Các bước thế số giải trình với công thức LaTeX
  * 4. Ghi chú điều kiện biên & Chú thích quy chuẩn
  * 5. Kết luận tuân thủ

### 3. Master Solver Facade (`SymbolicFormulaSolver`)
- Quản lý registry tập trung ánh xạ `formula_id` $\to$ `(callable, FormulaMetadata)`.
- Cung cấp phương thức `solve(formula_id, params)` kiểm tra kiểu dữ liệu và bắt lỗi tham số an toàn.

### 4. Spoke Master CI Gate Integration
- Cổng kiểm định số 9 (`Gate 9: Visual Parity & Formatting Clutter`) và Cổng số 10 (`Gate 10: Living Traceability`) trong `validate_legal_spoke.py` đóng vai trò rào chắn tự động.

---

## Testing Decisions

1. **Unit Testing Strategy (TDD):**
   - Mỗi solver phải có ít nhất 4 nhóm test cases:
     * *Direct Lookup Test:* Kiểm tra các điểm nút chính xác có sẵn trong bảng.
     * *Boundary Condition Test:* Kiểm tra các giá trị biên nhỏ nhất và lớn nhất.
     * *Linear Interpolation Test:* Kiểm tra giá trị nội suy tại các góc trung gian với Ground Truth đã tính toán giải tích.
     * *Dual Scenario Test:* Kiểm tra sự phân tách đúng đắn giữa kịch bản Hút âm và kịch bản Đẩy dương.
2. **Visual Card Integrity Test:**
   - Kiểm tra mọi thẻ JSON trong `figures/cards/` có thể được nạp và tính toán kích thước vùng hợp lệ qua `VisualCardEngine`.
3. **Master CI Gate Test:**
   - Chạy `python scripts/validate_legal_spoke.py` đảm bảo 10/10 gates vượt qua với 0 errors và 0 warnings.

---

## Out of Scope

- Không xây dựng giao diện frontend người dùng (UI rendering) trực tiếp trong Spoke này (Spoke tập trung $100\%$ vào Tri thức Pháp lý, Markdown OKF, Metadata RAG và Solvers).
- Không nhúng mã nguồn parsing mô hình 3D IFC phức tạp vào thư mục `formulas/` (việc kết nối `ifcopenshell` sẽ do các package chuyên biệt của Platform thực hiện, gọi qua `SymbolicFormulaSolver`).

---

## Further Notes

- Kế hoạch áp dụng tiếp theo: Phụ lục E (Hệ số hiệu ứng giật $G_f$), Phụ lục C (Bản đồ phân vùng áp lực gió $W_0$), Phụ lục D (Minh họa dạng địa hình), và Phụ lục G (Độ võng & chuyển vị).
