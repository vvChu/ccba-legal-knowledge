# Application Features Map & Verification Matrix — CCBA Legal Knowledge Spoke

Tài liệu này quản trị ma trận tính năng và cổng kiểm định tự động cho Spoke Tri thức Pháp lý `ccba-legal-knowledge` theo tiêu chuẩn Pstack Phase 2, ADR-0009 và ADR-0044.

---

## 1. Bảng Ánh Xạ Tính Năng & Bài Kiểm Định (Features Verification Matrix)

| Mã Tính Năng | Tên Tính Năng Quy Chuẩn | Thành Phần / Tập Tin Kiểm Tra | Kịch Bản Kiểm Định (Verification Harness) | Trạng Thái | Last Verified |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `FEAT-LEG-001` | Legal Registry & Metadata Schema | `legal_registry.yaml` | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode smoke` | `stable` | 2026-10-06 |
| `FEAT-LEG-002` | OKF v2.4 Universal Compartments | `legal_docs/**` (`sources`, `tables`, `figures`, `templates`) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode smoke` | `stable` | 2026-10-06 |
| `FEAT-LEG-003` | Spoke Cleanliness & Script Budget (ADR-0044) | `scripts/` (budget $\le 15$ tệp), không rò rỉ machine state | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode cleanliness` | `stable` | 2026-10-06 |
| `FEAT-LEG-004` | 15-Gate Master CI Validation | Toàn bộ 15 Cổng kiểm định chất lượng quy phạm | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-10-06 |
| `FEAT-LEG-005` | Scoped Document Bundle Verification | Kiểm định đơn lẻ từng bundle tài liệu (`--bundle`) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode bundle --bundle <slug>` | `stable` | 2026-10-06 |
| `FEAT-LEG-006` | Verbatim Normative Parity (Gate 11) | Tỷ lệ khớp nguyên văn DOCX $\to$ MD $\ge 98.0\%$ (ADR-0037) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-10-06 |
| `FEAT-LEG-007` | Multimodal Decoupled Asset & Cards (Gate 12) | Vector SVG/PNG $\ge 300\text{ DPI}$, Visual Cards (ADR-0040) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-10-06 |
| `FEAT-LEG-008` | Table Knowledge 2D Regularity (Gate 13) | Bảng tra 2D, Zero Ragged Rows, phẳng hóa em-dash (ADR-0041) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-10-06 |
| `FEAT-LEG-009` | KaTeX Math Syntax & Rendering (Gate 14) | Cú pháp KaTeX đa dòng `\qquad (X)`, không lỗi đỏ (ADR-0038) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-10-06 |

---

## 2. Quy Trình Vận Hành & Khắc Phục Lệch Hợp Đồng (COND-01)

1. **Khi nạp văn bản mới:** Chạy `python .agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode bundle --bundle <doc_slug>`.
2. **Trước khi commit/push:** Chạy `python .agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode smoke` hoặc `--mode full`.
3. **Khi bài kiểm định thất bại:** Thực hiện **Pre-Remediation Provenance Check** theo `maintain_drift_guide.md`.
   - Nếu là **Lệch Hợp Đồng (Contract Drift)** (nâng cấp schema, thêm cổng kiểm định): cập nhật harness tương ứng.
   - Nếu là **Lỗi Hồi Quy (Regression)** (văn bản mất bảng, lỗi cú pháp KaTeX, lệch verbatim): **CẤM SỬA HARNESS**, sửa nội dung bundle trong `legal_docs/`.
