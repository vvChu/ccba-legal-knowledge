# ADR 0018: Git-Ratchet Multi-Platform Knowledge Sync & Dual-Store Topology

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-19
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0012: Clean Unified NotebookLM Ingestion](0012-clean-unified-notebooklm-ingestion-strategy.md), [ADR 0017: AST Structural Patching](0017-ast-structural-patching-consolidation-engine.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Hệ sinh thái tri thức pháp lý `ccba-legal-knowledge` phục vụ đồng thời cho 2 lớp đối tượng người dùng/hệ thống (*Dual Consumers*):
1. **Lớp Tương Tác Nghiên Cứu & Hội Thảo (Human-AI Interactive Layer):** Sử dụng **Google NotebookLM** để chuyên viên pháp lý và kỹ sư tra cứu ngữ cảnh lớn 2M tokens, tự động tạo tài liệu tóm tắt (Study Guides, FAQs, Audio Overview) và chuẩn bị nội dung cho các buổi seminar nội bộ CCBA.
2. **Lớp Kiểm Toán Bản Vẽ Tự Động (Machine Automated Audit Layer):** Sử dụng **AI Gateway `ccba-ai` & Vector DB (Qdrant/Chroma) trên Server Spark (:8090)** để AI QC Batch Orchestrator quét đối soát tự động hàng trăm bản vẽ kỹ thuật (Arch-KC-MEP-PCCC) với độ trễ thấp và độ chính xác nguyên tử theo từng ô bảng kỹ thuật.

Nếu quy trình đồng bộ hóa giữa 2 nền tảng này được thực hiện thủ công hoặc phân tán:
- Sẽ phát sinh rủi ro **lệch pha dữ liệu (Sync Drift)**: AI QC trên server kiểm tra theo quy chuẩn cũ trong khi kỹ sư tra cứu trên Cloud lại đọc quy chuẩn mới, hoặc ngược lại.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định thiết lập **Kiến Trúc Đồng Bộ Tri Thức Đa Nền Tảng Theo Cơ Chế Git-Ratchet (Git-Ratchet Multi-Platform Knowledge Sync Topology)**:

1. **Cơ Chế Kích Hoạt Có Cổng Kiểm Soát (Gate-Guarded CD Trigger):**
   - Mọi thay đổi dữ liệu trong `legal_docs/` hoặc `legal_registry.yaml` chỉ được đồng bộ hóa khi và chỉ khi **vượt qua $100\%$ bộ 3 CI Quality Gates** (`validate_legal_spoke.py`, `verify_knowledge_integrity.py`, `verify_cross_links.py`).
   - Ngăn chặn triệt để việc đẩy dữ liệu lỗi, vỡ bảng hoặc sai thẻ neo lên môi trường Production.

2. **Luồng Đồng Bộ Kép Tự Động (Dual-Track Automated Sync Pipeline):**
   - **Luồng 1 (Cloud Google NotebookLM Sync):** 
     - Tự động lọc danh sách **32 nguồn Markdown sạch** (theo chuẩn [ADR 0012](0012-clean-unified-notebooklm-ingestion-strategy.md)).
     - Gọi `notebooklm_helper.py` đẩy dữ liệu vào Notebook tri thức pháp lý chung (`6dca7e4e-c407-4d1f-882a-e0d9459d1120`).
   - **Luồng 2 (Local Spark Vector DB & AST Cache Sync):**
     - Đọc cây AST `clauses.json` và bảng số liệu `tables/json/` từ các gói OKF.
     - Tạo vector embeddings đa tầng (Hybrid Sparse BM25 + Dense Vectors) và upsert trực tiếp vào cơ sở dữ liệu Vector DB trên Server Spark (:8090) qua mạng nội bộ VPN Tailscale (`100.83.192.30`).

3. **Cơ Chế Khóa Phiên Bản Đồng Bộ (Sync Version Lock & Heartbeat):**
   - Mỗi lần đồng bộ thành công, pipeline ghi nhận `commit_sha` và `sync_timestamp` vào `legal_registry.yaml`.
   - AI QC Pipeline khi khởi chạy kiểm toán bản vẽ sẽ tự động kiểm tra `sync_version_lock` giữa Spark Server và Git Remote để bảo đảm $100\%$ đồng nhất.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Đồng nhất tri thức tuyệt đối ($100\%$ Parity):** Xóa bỏ hoàn toàn tình trạng lệch pha dữ liệu giữa kỹ sư tra cứu trên Cloud và AI QC quét ngầm trên Server Spark.
- **Tự động hóa hoàn toàn:** Kỹ sư chỉ cần thực hiện `git push`, toàn bộ hệ thống tri thức đa nền tảng sẽ tự động cập nhật trong vòng dưới 2 phút.

### Đánh đổi:
- Cần duy trì kết nối mạng ổn định tới Server Spark qua Tailscale VPN và quản lý token/session của Google NotebookLM.
