# Application Features Map & Verification Matrix — CCBA Legal Knowledge Spoke

Tài liệu này quản trị ma trận tính năng và cổng kiểm định tự động cho toàn bộ hệ sinh thái Spoke Tri thức Pháp lý `ccba-legal-knowledge` qua **3 Trụ cột Kiểm định (`verify-<app>`)** theo tiêu chuẩn Pstack Phase 2 (v0.15.36), ADR-0009 và ADR-0044:
1. **`ccba-verify-legal-knowledge`**: Kiểm định Kho dữ liệu OKF v2.4 & 15 Cổng Master CI Gate.
2. **`ccba-verify-legal-intel`**: Kiểm định Động cơ Truy xuất, Tra cứu Điều/Khoản, Bảng 2D & Từ điển Quốc gia (`/ccba-legal-intel`).
3. **`ccba-verify-legal-ingest`**: Kiểm định Chu trình Thu thập VIP, Tiền xử lý OpenXML, Hợp nhất VBHN & Tư vấn Đồ thị 5 Vành đai (`/ccba-legal-ingest`, `/ccba-tvpl-vip-crawler`, `/ccba-legal-document-tracker`, `/ccba-legal-advisor`).

---

## 1. Trụ Cột 1: Kho Tri Thức Pháp Lý & 15 Cổng CI (`ccba-verify-legal-knowledge`)

| Mã Tính Năng | Tên Tính Năng Quy Chuẩn | Thành Phần / Tập Tin Kiểm Tra | Kịch Bản Kiểm Định (Verification Harness) | Trạng Thái | Last Verified |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `FEAT-LEG-001` | Legal Registry & Metadata Schema | `legal_registry.yaml` (106 văn bản) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode smoke` | `stable` | 2026-11-04 |
| `FEAT-LEG-002` | OKF v2.4 Universal Compartments | `legal_docs/**` (`sources`, `tables`, `figures`, `templates`) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode smoke` | `stable` | 2026-11-04 |
| `FEAT-LEG-003` | Spoke Cleanliness & Script Budget (ADR-0044) | `scripts/` (budget $\le 15$ tệp), không rò rỉ machine state | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode cleanliness` | `stable` | 2026-11-04 |
| `FEAT-LEG-004` | 15-Gate Master CI Validation | Toàn bộ 15 Cổng kiểm định chất lượng quy phạm | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-11-04 |
| `FEAT-LEG-005` | Scoped Document Bundle Verification | Kiểm định đơn lẻ từng bundle tài liệu (`--bundle`) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode bundle --bundle <slug>` | `stable` | 2026-11-04 |
| `FEAT-LEG-006` | Verbatim Normative Parity (Gate 11) | Tỷ lệ khớp nguyên văn DOCX $\to$ MD $\ge 98.0\%$ (ADR-0037) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-11-04 |
| `FEAT-LEG-007` | Multimodal Decoupled Asset & Cards (Gate 12) | Vector SVG/PNG $\ge 300\text{ DPI}$, Visual Cards (ADR-0040) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-11-04 |
| `FEAT-LEG-008` | Table Knowledge 2D Regularity (Gate 13) | Bảng tra 2D, Zero Ragged Rows, phẳng hóa em-dash (ADR-0041) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-11-04 |
| `FEAT-LEG-009` | KaTeX Math Syntax & Rendering (Gate 14) | Cú pháp KaTeX đa dòng `\qquad (X)`, không lỗi đỏ (ADR-0038) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-11-04 |
| `FEAT-LEG-010` | OKF Provenance & Algorithm Version Attestation (Gate 15) | Kiểm định SHA-256 nguồn gốc và phiên bản thuật toán OKF v2.4 | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode full` | `stable` | 2026-11-04 |
| `FEAT-LEG-011` | Spoke Unit & 5-Ring Ontology Test Suite | `tests/unit/` (126 unit tests: ontology, KaTeX, visual parity) | `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode unit` | `stable` | 2026-11-04 |

---

## 2. Trụ Cột 2: Động Cơ Truy Xuất & Trí Tuệ Pháp Lý (`ccba-verify-legal-intel`)

| Mã Tính Năng | Tên Tính Năng `/ccba-legal-intel` | Endpoint / CLI / Deep Seam | Kịch Bản Kiểm Định (Verification Harness) | Trạng Thái | Last Verified |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `FEAT-INT-001` | Registry Search & Lifecycle Warning | `ccba_legal query` / `LegalKnowledgeEngine.search` | `.agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py --mode smoke` | `stable` | 2026-11-04 |
| `FEAT-INT-002` | Tier-Aware Clause Slicing & CWE-22 Guard | `ccba_legal get-clause` / `LegalKnowledgeEngine.get_clause` | `.agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py --mode smoke` | `stable` | 2026-11-04 |
| `FEAT-INT-003` | 2D Table Matrix Extraction | `ccba_legal get-table` / `LegalKnowledgeEngine.get_table` | `.agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py --mode smoke` | `stable` | 2026-11-04 |
| `FEAT-INT-004` | Canonical Lexicon & QD 1812/QD-BXD ID Parser | `ccba_legal.lexicon.parse_national_construction_id` | `.agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py --mode smoke` | `stable` | 2026-11-04 |
| `FEAT-INT-005` | Legal-to-PPTX & Spoke Sync Seams | `ccba_legal pptx`, `ccba_legal sync` | `.agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py --mode unit` | `stable` | 2026-11-04 |

---

## 3. Trụ Cột 3: Chu Trình Nạp, Hợp Nhất VBHN & Tư Vấn Pháp Lý (`ccba-verify-legal-ingest`)

| Mã Tính Năng | Tên Tính Năng Chu Trình Ingest / VBHN / Advisor | Kỹ Năng & Deep Seam Bảo Vệ | Kịch Bản Kiểm Định (Verification Harness) | Trạng Thái | Last Verified |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `FEAT-ING-001` | TVPL VIP Acquisition & Session Mutex | `/ccba-tvpl-vip-crawler`, `TVPLSessionMutex`, `CookieVault` | `.agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py --mode smoke` | `stable` | 2026-11-04 |
| `FEAT-ING-002` | Canonical OpenXML Sanitizer & OKF v2.4 Packager | `/ccba-legal-ingest`, `DocxCanonicalSanitizer`, `OKFBundlePackager` | `.agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py --mode smoke` | `stable` | 2026-11-04 |
| `FEAT-ING-003` | Multimodal 2D Table Grid, KaTeX & Visual Parity | `/ccba-legal-ingest`, `TableMatrixBuilder`, `VisualParityAuditor` | `.agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py --mode unit` | `stable` | 2026-11-04 |
| `FEAT-ING-004` | Legislative AST Consolidation & VBHN Matrix | `/ccba-legal-document-tracker`, `LegislativeConsolidator`, `VBHNEngine` | `.agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py --mode unit` | `stable` | 2026-11-04 |
| `FEAT-ING-005` | 5-Ring Legal Graph Routing & Hard-Floor Currency | `/ccba-legal-advisor`, `spoke_cli.py graph`, `DynamicStatutoryResolver` | `.agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py --mode graph` | `stable` | 2026-11-04 |

---

## 4. Quy Trình Vận Hành & Khắc Phục Lệch Hợp Đồng (COND-01)

1. **Kiểm định Kho Tri thức Pháp lý:** `python .agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode smoke`
2. **Kiểm định Động cơ Truy xuất `/ccba-legal-intel`:** `python .agents/skills/ccba-verify-legal-intel/harness/verify_legal_intel_harness.py --mode full`
3. **Kiểm định Chu trình Nạp/Hợp nhất/Tư vấn `/ccba-legal-ingest`:** `python .agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py --mode full`
4. **Khi bài kiểm định thất bại:** Thực hiện **Pre-Remediation Provenance Check** theo `maintain_drift_guide.md`:
   - Phân loại vào 1 trong 4 trạng thái chuẩn: `in_sync`, `updated`, `bug`, `blocked`.
   - Nếu là **Lệch Hợp Đồng (Contract Drift — `updated`)**: cập nhật harness tương ứng và thực hiện **Semantic Mutation Proof** (`COND-01`, `COND-02`) trước khi nâng `sync_commit`.
   - Nếu là **Lỗi Hồi Quy (Regression — `bug`)**: **CẤM SỬA HARNESS**, giữ nguyên `sync_commit` và sửa mã nguồn hoặc dữ liệu gốc.
