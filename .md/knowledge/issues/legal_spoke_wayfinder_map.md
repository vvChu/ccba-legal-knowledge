# Bản Đồ Định Hướng Tri Thức Pháp Lý CCBA (Wayfinder Map)

- **Mã Bản Đồ:** `WAYFINDER-LEGAL-KNOWLEDGE-V2`
- **Phiên bản:** 2.0.0 (Xem Bản đồ Nâng cấp v3.0 tại [.md/wayfinder/ground-truth-parity/map.md](../wayfinder/ground-truth-parity/map.md))
- **Ngày khởi tạo:** 2026-08-19 (Cập nhật chiến dịch v3.0: 2026-09-19)
- **Người lập:** CCBA Legal Intelligence Architecture Team
- **Trạng thái:** Active (Đang vận hành)

> [!TIP]
> **Chiến Dịch Nâng Hạng Đối Soát 1-1 Xác Định 55 Gói Tri Thức (v3.0):** Bản đồ chi tiết giải quyết 26 vé lỗi tiềm ẩn từ đợt kiểm định toàn kho được quản lý tại [**`WAYFINDER-GROUND-TRUTH-PARITY-100`**](../wayfinder/ground-truth-parity/map.md).

---

## 1. Điểm Đích (Destination)

Xây dựng và vận hành thành công **Kho Tri thức Pháp lý Xây dựng & PCCC Việt Nam Chính quy (CCBA Legal Knowledge Spoke)** đạt chuẩn **OKF v2.0 Native-First**, đóng vai trò là "Bộ Não Luật Định" duy nhất cho toàn bộ hệ sinh thái CCBA Agent Platform, với các tiêu chí hoàn thành đo lường được:

1. **Dữ liệu Chuẩn hóa 100%:** 29+ văn bản quy chuẩn, luật, nghị định, thông tư được bóc tách cấu trúc, hợp nhất toàn văn, gắn thẻ neo bất biến và đối soát khớp $100\%$ với bản in PDF Công báo có dấu mộc đỏ nhà nước.
2. **Cây AST Giàu Siêu Dữ Liệu (Rich AST):** 100% điều khoản trong `clauses.json` được gắn nhãn Thẩm quyền (`CQXD`, `CONG_AN`, `CHU_DAU_TU_TU_THAM_DINH`), số trang công báo (`source_pdf_page`), mốc ân hạn chuyển tiếp (`grace_period_end`) và mã công thức kỹ thuật (`formula_id`).
3. **Bộ Động Cơ Tự Động Hóa:** Vận hành trơn tru Động cơ Hợp nhất Văn bản (AST Structural Patching Engine - ADR 0017) và Động cơ Tính toán Công thức Kỹ thuật (Hybrid Formula Solver Engine - ADR 0020).
4. **Đồng Bộ Đa Nền Tảng Tự Động:** Đồng bộ song song 32 nguồn Markdown sạch lên Google NotebookLM và đẩy cây AST Vector Embeddings lên Local Spark Vector DB (:8090) qua rào chắn Git-Ratchet CI Gates.

---

## 2. Ghi Chú & Ràng Buộc Kiến Trúc (Notes & Invariants)

- **Shallow Path Invariant:** `legal_docs/` nằm tại Cấp 1 của Spoke; `legal_registry.yaml` nằm tại Root.
- **Reuse-First Gate:** Mọi công cụ bóc tách tổng quát phải đóng gói vào Hub (`ccba-agent-platform/packages/ccba-legal`), Spoke chỉ chứa dữ liệu và runner script mỏng.
- **Legal Anchor of Trust (ADR 0016):** Mọi kết luận kiểm toán phải truy vết được về số trang và tệp PDF Công báo có dấu mộc đỏ.

---

## 3. Quyết Định Đã Chốt (Decisions So Far)

*   `[ADR 0011]` [Atomic Clause RAG Chunking Strategy](../../docs/adr/0011-atomic-clause-rag-chunking-strategy.md) — Giữ nguyên khối điều/khoản lớn ~800 tokens để bảo toàn điều kiện tiên quyết.
*   `[ADR 0012]` [Clean Unified NotebookLM Ingestion Strategy](../../docs/adr/0012-clean-unified-notebooklm-ingestion-strategy.md) — Chỉ nạp 32 nguồn Markdown sạch hiện hành, cách ly toàn bộ bản gốc/bản cũ.
*   `[ADR 0013]` [Dynamic Grace Period Compliance Gate](../../docs/adr/0013-dynamic-grace-period-compliance-gate.md) — Gán nhãn Cảnh báo vàng trong hạn ân hạn 6 tháng đến 15/06/2027 cho chung cư hiện hữu sạc xe điện.
*   `[ADR 0014]` [Split Jurisdiction PCCC Audit Routing](../../docs/adr/0014-split-jurisdiction-pccc-audit-routing.md) — Phân luồng thẩm quyền Sở Xây dựng (`CQXD`) vs Cảnh sát PC07 (`CONG_AN`) theo Luật 55/2024 & NĐ 105/2025.
*   `[ADR 0015]` [Unresolved Normative Reference Metadata Fallback](../../docs/adr/0015-unresolved-reference-metadata-fallback.md) — Định tuyến giao thức `legal://` về Thẻ Siêu dữ liệu Tra cứu & nút mở file PDF gốc.
*   `[ADR 0016]` [Dual-Track Hybrid Extraction & PDF Anchor of Trust](../../docs/adr/0016-dual-track-hybrid-pdf-anchor-of-trust.md) — DOCX bóc tách cấu trúc, PDF Công báo làm mỏ neo pháp lý tối thượng.
*   `[ADR 0017]` [AST Structural Patching Engine for Legislative Consolidation](../../docs/adr/0017-ast-structural-patching-consolidation-engine.md) — Hợp nhất văn bản xác định $100\%$ qua Semantic Action Tokens.
*   `[ADR 0018]` [Git-Ratchet Multi-Platform Knowledge Sync Topology](../../docs/adr/0018-git-ratchet-multi-platform-knowledge-sync.md) — Đồng bộ tự động kép có CI Gate lên Cloud NotebookLM và Local Server Spark.
*   `[ADR 0019]` [Tiered Audit Persona & Client Self-Audit Affidavit Engine](../../docs/adr/0019-tiered-audit-persona-and-self-audit-affidavit.md) — Phân hạng hồ sơ kiểm toán và tự động xuất Biên bản Tự Thẩm định PCCC theo NĐ 105/2025.
*   `[ADR 0020]` [Hybrid Symbolic Formula Solver Engine](../../docs/adr/0020-hybrid-symbolic-formula-solver-engine.md) — Trích xuất biến số qua LLM, tính toán số học xác định qua Python pure functions trong `formulas/`.

---

## 4. Danh Sách Ticket Ở Biên Giới (Frontier Tickets)

```mermaid
flowchart TD
    T1["Ticket 1: Git Commit & Remote Sync [✅ DONE]"] --> T2["Ticket 2: Upload 29 Whitelist Sources to NotebookLM [✅ DONE]"]
    T1 --> T3["Ticket 3: Đóng gói formulas/ Engine cho QCVN 06 [✅ DONE]"]
    T1 --> T4["Ticket 4: Kiểm toán Pháp Y 29 Văn bản & PDF Anchors [✅ DONE]"]
    T2 & T3 & T4 --> T5["Ticket 5: Thử nghiệm AI QC Audit Tự Động trên Hồ sơ Bản vẽ Thực tế [Pilot / UNBLOCKED]"]
```

### 🎫 [Ticket 1: Đóng Gói Git Commit & Đồng Bộ Remote Hub](file:///d:/GitHubProjects/ccba-legal-knowledge) `[✅ DONE]`
- **Mục tiêu:** Thực hiện Commit có cấu trúc Conventional Commit cho toàn bộ 10 ADRs, bộ script CI Gates nâng cấp và dữ liệu AST `clauses.json` đã chuẩn hóa.
- **Trạng thái:** `✅ DONE` (Đã hoàn tất tại commit `2cc368b` & `254c55b` trên `main`).

### 🎫 [Ticket 2: Đồng Bộ 29 Nguồn Markdown Sạch lên Google NotebookLM](file:///d:/GitHubProjects/ccba-legal-knowledge/scripts/sync_notebooklm_knowledge.py) `[✅ DONE]`
- **Mục tiêu:** Kích hoạt `sync_notebooklm_knowledge.py` nạp 29 tệp Markdown hợp nhất (4.24 MB, 562,226 từ) vào Notebook `6dca7e4e-c407-4d1f-882a-e0d9459d1120`.
- **Trạng thái:** `✅ DONE` (Đã tải lên thành công 29/29 tệp và kiểm thử truy vấn RAG grounding chính xác 100%).

### 🎫 [Ticket 3: Xây Dựng Thư Viện Hàm Tính Toán `formulas/` cho QCVN 06](file:///d:/GitHubProjects/ccba-legal-knowledge/formulas) `[✅ DONE]`
- **Mục tiêu:** Lập trình các hàm tính toán xác định cho cấp nước chữa cháy ngoài nhà (Bảng 8), dung tích bể chứa, lưu lượng hút khói hành lang (Phụ lục D), sảnh thông tầng và bán kính Sprinkler (theo ADR 0020).
- **Trạng thái:** `✅ DONE` (Đã hoàn thành 6 module, đóng gói `SymbolicFormulaSolver` và vượt qua 12/12 unit tests).

### 🎫 [Ticket 4: Kiểm Toán Pháp Y Toàn Diện 29 Văn Bản & Quản Lý Mỏ Neo PDF (Ticket 4 Plus)](file:///d:/GitHubProjects/ccba-legal-knowledge/scripts/audit_all_vbpl_documents.py) `[✅ DONE]`
- **Mục tiêu:** Thực thi kiểm toán pháp y 100% 29 văn bản trong kho tri thức Spoke, đối soát đề mục H1-H5, thẻ neo, bảng biểu 2D, AST clauses và quản lý mỏ neo PDF Công báo (ADR 0016).
- **Trạng thái:** `✅ DONE` (Đã kiểm toán 29/29 văn bản, 69,416 dòng Markdown, 1,931 đề mục, 4,957 thẻ neo, 102 bảng 2D với **0 Lỗi & 0 Cảnh báo**).

### 🎫 [Ticket 5: Thử Nghiệm Kiểm Toán Thẩm Tra PCCC Tự Động (AI QC Pilot Test)](file:///d:/GitHubProjects/ccba-legal-knowledge) `[Pilot / UNBLOCKED]`
- **Mục tiêu:** Sử dụng một bộ hồ sơ thiết kế chung cư thực tế (có hạ tầng sạc xe điện) để chạy thử toàn trình AI QC Audit Pipeline phân luồng CQXD vs PC07 vs CDT Self-Audit.
- **Trạng thái:** `🟢 UNBLOCKED` (Sẵn sàng kích hoạt Pilot Audit).

---

## 5. Sương Mù Chiến Trận / Chưa Xác Định Rõ (Not Yet Specified)

1. **Tích hợp Ký số Điện tử Doanh nghiệp (Digital Signature HSM/USB Token):**
   - Cơ chế cắm USB Token hoặc Cloud HSM để tự động ký số lên Biên bản Tự thẩm định PCCC (.pdf) sau khi AI QC duyệt xong. Cần khảo sát API của Viettel-CA / VNPT-CA.
2. **Trình Xem PDF Tích Hợp Sẵn Tọa Độ Trang (Embedded Web PDF Viewer):**
   - Giao diện người dùng mở trực tiếp trang PDF Công báo có highlight điều khoản tương ứng trong trình duyệt Web.

---

## 6. Ngoài Phạm Vi (Out of Scope)

*   **Xây dựng Giao diện Web Frontend tổng thể:** Thuộc phạm vi của Spoke `ccba-ai-qc-frontend` hoặc Hub `ccba-agent-platform`.
*   **Số hóa Tiêu chuẩn Nước ngoài (NFPA, BS EN, IBC):** Chỉ tập trung $100\%$ cho hệ thống Văn bản Quy phạm Pháp luật và Quy chuẩn/Tiêu chuẩn chính thức của Việt Nam.
