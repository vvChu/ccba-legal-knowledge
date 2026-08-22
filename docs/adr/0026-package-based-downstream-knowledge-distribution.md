# ADR 0026: Package-Based Downstream Legal Knowledge Distribution via ccba-legal-intel SDK

- **Trạng thái:** ACCEPTED
- **Ngày quyết định:** 2026-08-22
- **Người đề xuất:** CCBA Legal Intelligence Team
- **Phạm vi:** Hub-Spoke Interface, SDK Distribution, Downstream Agent Interoperability

---

## 1. Bối cảnh & Vấn đề (Context & Problem Statement)

Spoke `ccba-legal-knowledge` quản trị toàn bộ 26 gói tri thức pháp lý chuẩn hóa theo định dạng **OKF v2.2** (Thân văn bản thuần khiết, Biểu mẫu nguyên tử, Bảng tra cứu ma trận 2D và Cây cú pháp AST phẳng).

Để các dịch vụ downstream trên toàn hệ sinh thái CCBA (như `ccba-ai-qc` thẩm tra thiết kế, `completion-checklist` tạo hồ sơ hoàn công, `ccba-contract-audit` rà soát hợp đồng xây dựng) có thể khai thác kho tri thức này một cách an toàn và bền vững, hệ thống cần một cơ chế giao tiếp độc lập với cấu trúc thư mục vật lý cục bộ. Việc đọc tệp trực tiếp bằng đường dẫn tuyệt đối (Hardcoded Path) gây ra rủi ro đứt gãy hệ thống khi chuyển đổi môi trường hoặc refactor cấu trúc dữ liệu.

---

## 2. Quyết định Thiết kế (Decision)

1. **Phân Định Trách Nhiệm Hub - Spoke (Producer - Consumer Architecture):**
   * **Spoke `ccba-legal-knowledge` (Data Producer):** Tập trung $100\%$ vào việc số hóa, đóng gói OKF v2.2, quản trị mã băm SHA-256 đối soát PDF và duy trì 5 Cổng CI Gates nghiệm thu chất lượng dữ liệu.
   * **Hub `ccba-agent-platform` / `packages/ccba-legal-intel` (SDK Consumer & Gateway):** Đóng gói thành Python Package chính quy, cung cấp Giao diện lập trình kiểu an toàn (*Type-Safe API*) cho toàn bộ các Agent bộ môn downstream.

2. **Giao Diện Lập Trình Chuẩn Hóa (`LegalKnowledgeEngine` Interface):**
   * Toàn bộ các tương tác tri thức phải thông qua interface chính thức:
     ```python
     from ccba_legal_intel import LegalKnowledgeEngine

     engine = LegalKnowledgeEngine()
     # Tra cứu điều khoản theo AST O(1)
     clause = engine.get_clause(doc_number="22/2023/QH15", clause_id="dieu-2-khoan-1")
     # Truy xuất ma trận ràng buộc bảng kỹ thuật
     table_matrix = engine.get_table_matrix(doc_id="qcvn_06_2022_bxd", table_id="bang_06")
     # Trích xuất biểu mẫu nguyên tử
     template = engine.get_form_template(doc_number="36/2026/TT-BXD", template_id="mau_01")
     ```

3. **Cấm Tuyệt Đối Đọc File Trực Tiếp ở Tầng Ứng Dụng Downstream:**
   * Mọi Agent downstream (QC, Checklist, Contract) không được mở tệp Markdown/JSON thô bằng `open()` trực tiếp mà bắt buộc phải gọi qua `ccba-legal-intel`.

---

## 3. Hệ quả & Đánh đổi (Consequences)

### Tích cực:
* ✅ Bảo vệ cấu trúc Spoke: Thay đổi vị trí file nội bộ tại Spoke không làm sập các dịch vụ downstream.
* ✅ Type-Safety & IntelliSense: Hỗ trợ kiểm tra kiểu tĩnh (Mypy) và tự động hoàn thành mã nguồn cho lập trình viên CCBA.
* ✅ Khả năng mở rộng cao: Hoạt động đồng nhất trên máy phát triển cá nhân, Docker Container, CI/CD Pipeline và Cloud Server Spark.

---

## 4. Tham chiếu (References)
- [ADR 0009: CCBA Legal SDK Package Distribution](./0009-ccba-legal-sdk-package-distribution.md)
- [ADR 0021: OKF v2.2 Pure Normative Body & Legal Graph](./0021-okf-v2-2-pure-normative-body-legal-graph.md)
- [ADR 0023: Full Comprehensive NotebookLM Ingestion](./0023-full-comprehensive-notebooklm-ultra-ingestion.md)
- [ADR 0024: Dual-Track Provenance with Footnote Anchor](./0024-dual-track-provenance-footnote-anchoring.md)
- [ADR 0025: Strict Provenance Enactment Gate](./0025-strict-provenance-enactment-gate.md)
