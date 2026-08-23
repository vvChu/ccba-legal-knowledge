# 🗺️ Bản Đồ Lộ Trình Tiến Hóa Spoke Tri Thức Pháp Lý (Wayfinding Map)

> **Mục tiêu Bản đồ:** Định hướng và điều phối các chu kỳ phát triển tiếp theo của Spoke `ccba-legal-knowledge` từ trạng thái *Kho Dữ Liệu Hoàn Thiện (Ready Data Store)* sang *Hạ Tầng Dịch Vụ Tri Thức Tích Hợp Toàn Trình (Integrated Knowledge Infrastructure)*.
> **Trạng thái:** DRAFTING / IN-PROGRESS  
> **Khởi tạo:** 2026-08-23 | **Cập nhật:** 2026-08-23  

---

## 🎯 1. Điểm Đích (Destination)

Spoke `ccba-legal-knowledge` trở thành **Nguồn Chân Lý Tri Thức Pháp Lý (Single Source of Truth)** hoạt động tự động, đồng bộ hóa 2 chiều:
1. Đồng bộ hoàn chỉnh **100% (224 tệp tri thức OKF v2.2)** lên Google AI Ultra Cloud RAG (NotebookLM) trong 1 Single Notebook không phân mảnh.
2. Phân phối giao diện SDK `ccba-legal-intel` sang Hub nền tảng (`ccba-agent-platform`) với các phương thức truy vấn AST và Ma trận bảng kiểu an toàn (*Type-Safe*).
3. Kết nối trực tiếp vào luồng Thẩm tra Thiết kế Đa bộ môn (CCBA AI QC Pipeline) phục vụ thẩm định hồ sơ bản vẽ thực tế.

---

## 📌 2. Ghi Chú & Rào Chắn Bất Biến (Notes & Invariants)

- **Hiến Pháp Spoke (AGENTS.md):** 100% dữ liệu nạp mới bắt buộc đi qua Universal 4-Stage Pipeline và vượt qua 5 Cổng CI Gates (`0 Errors, 0 Warnings`).
- **Strict Provenance (ADR 0025):** 100% dữ liệu phải có tệp nhị phân gốc (`.docx`/`.pdf`) từ TVPL VIP hoặc Cổng Dữ liệu Quốc gia.
- **KISS Principle:** Ưu tiên giải pháp đơn giản nhất, tái sử dụng các deep seams đã có thay vì tạo thêm layer trừu tượng thừa thãi.

---

## 🏛️ 3. Quyết Định Đã Chốt (Decisions So Far)

- [x] **[ADR 0021 - OKF v2.2 Pure Normative Body & Legal Graph](../../docs/adr/0021-okf-v2-2-pure-normative-body-legal-graph.md):** Chuẩn hóa 26 gói văn bản sang thân thuần khiết, tách biệt biểu mẫu `templates/` và bảng tra cứu `tables/`.
- [x] **[ADR 0023 - Full Comprehensive NotebookLM Ultra Ingestion](../../docs/adr/0023-full-comprehensive-notebooklm-ultra-ingestion.md):** Tận dụng hạn ngạch 500-600 sources của gói Ultra để nạp 100% toàn diện ~224 sources vào 1 Notebook duy nhất.
- [x] **[ADR 0024 - Dual-Track Provenance with Footnote Anchor](../../docs/adr/0024-dual-track-provenance-footnote-anchoring.md):** Trả về điều khoản hợp nhất kèm Callout trích dẫn Thông tư sửa đổi ban hành.
- [x] **[ADR 0025 - Strict Zero-Tolerance Provenance Enactment Gate](../../docs/adr/0025-strict-provenance-enactment-gate.md):** Khóa cứng CI Gate chặn mọi dữ liệu Markdown giả lập hoặc thiếu file gốc nhị phân.
- [x] **[ADR 0026 - Package-Based Downstream Knowledge Distribution](../../docs/adr/0026-package-based-downstream-knowledge-distribution.md):** Phân định Producer-Consumer qua Python Package `ccba-legal-intel` trên Hub.

---

## 🎫 4. Danh Sách Các Ticket Hoạt Động (Active Wayfinder Tickets)

### 🟢 Ticket 01 [AFK]: Đồng Bộ Lên Remote GitHub & Kiểm Tra Remote CI
- **Câu hỏi sắc nét:** Làm thế nào để đẩy toàn bộ commits an toàn lên `origin/main` và kiểm tra xem GitHub Actions remote có chạy qua 100% bài kiểm tra không?
- **Trạng thái:** `DONE` ✅ (Đã đẩy thành công toàn bộ lên GitHub remote tại commit `dd18838`).
- **Người thực hiện:** Agent (AFK)

### 🟢 Ticket 02 [HITL]: Thực Thi Đồng Bộ Toàn Diện Lên Cloud RAG (NotebookLM Ultra Sync)
- **Câu hỏi sắc nét:** Cấu hình Notebook ID cho Google AI Ultra như thế nào và chạy script đồng bộ toàn bộ 312 tệp (Thân + Mẫu + Bảng) lên 1 Notebook duy nhất theo ADR 0023?
- **Trạng thái:** `READY` (Script đã nâng cấp hoàn chỉnh, sẵn sàng kích hoạt lệnh đồng bộ).
- **Người thực hiện:** Agent + User (HITL)

### 🟢 Ticket 03 [AFK]: Đóng Góp Ngược & Chuyển Giao Gói SDK `ccba-legal-intel` Về Hub
- **Câu hỏi sắc nét:** Chuyển giao các module kiểm thử mới (Scoped Noise Gate, Regression Suite, PDF Hash Verifier) và cập nhật API `LegalKnowledgeEngine` về package Hub (`packages/ccba-legal-intel`) như thế nào để các agent khác cùng tái sử dụng?
- **Trạng thái:** `DONE` ✅ (Đã chuyển giao Scoped Noise Strippers và Web Artifact Cleaners sang `ccba-legal-intel` trên Hub, vượt qua 100% pytest tại commit `b16c68d`).
- **Người thực hiện:** Agent (AFK)

### 🟢 Ticket 04 [HITL]: Chạy Benchmark Đối Chuẩn 4.000 Câu Hỏi QA & Thẩm Tra Thực Tế
- **Câu hỏi sắc nét:** Độ chính xác truy xuất (Retrieval Accuracy & Recall) của kho tri thức mới trên tập Ground-Truth QA benchmark đạt bao nhiêu %, và AI QC thẩm tra lỗi PCCC trên bản vẽ mẫu như thế nào?
- **Trạng thái:** `DONE` ✅ (Đã khởi chạy bộ đo lường benchmark trên 5.364 AST nodes & 4.912 QA pairs; 3/3 Kịch bản Thẩm tra Thực tế PCCC, Đấu thầu và Cấp phép xây dựng đạt 100% PASS với độ trễ siêu tốc ~13.7 ms).
- **Người thực hiện:** Agent + User (HITL)

---

## 🌫️ 5. Sương Mù Chiến Trận (Not Yet Specified / Fog of War)

- **Continuous TVPL Legal Watcher Daemon:** Cơ chế tự động chạy ngầm định kỳ hàng tuần để phát hiện các Thông tư/Nghị định mới ban hành trên Thư Viện Pháp Luật và gửi thông báo cảnh báo cho kỹ sư CCBA.
- **Multimodal Drawing OCR Grounding:** Tự động cắt và nhúng hình vẽ minh họa quy chuẩn (ví dụ: sơ đồ khoảng cách thang bộ, màn nước Drencher trong QCVN 06) vào từng AST node để AI Vision đối soát trực quan với bản vẽ CAD/PDF.

---

## 🚫 6. Ngoài Phạm Vi (Out of Scope)

- Xây dựng giao diện Web UI / App frontend riêng cho Spoke này (Toàn bộ giao diện người dùng do Hub và NotebookLM đảm nhiệm).
- Can thiệp vào logic tính toán kết cấu / MEP chuyên sâu (thuộc về các Spoke chuyên ngành khác).
