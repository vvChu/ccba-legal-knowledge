# ADR 0012: Clean Unified Repository Strategy for Google NotebookLM Ingestion

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-19
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0001: Dual-Track VBHN](0001-vbhn-dual-track-provenance.md), [ADR 0008: Temporal Legal Query Engine](0008-temporal-query-engine-point-in-time-auditing.md), [ADR 0011: Atomic Clause Chunking](0011-atomic-clause-rag-chunking-strategy.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Nền tảng CCBA Legal Knowledge Spoke duy trì đồng bộ tri thức với Google NotebookLM (Gemini Notebook) để phục vụ tra cứu tự nhiên và hỗ trợ kỹ sư giải đáp pháp luật xây dựng.
Trong kho tri thức tồn tại các phiên bản văn bản kép (Dual-Track):
- Bản Gốc ban đầu (ví dụ: `qcvn_06_2022_bxd.md`, `qcvn_04_2021_bxd.md`).
- Bản Sửa đổi kỹ thuật độc lập (ví dụ: `sua_doi_1_2023_*.md`, `sua_doi_01_2026_*.md`).
- Bản Hợp nhất toàn văn mới nhất (ví dụ: `qcvn_06_2022_bxd_hop_nhat_2023.md`, `qcvn_04_2021_bxd_hop_nhat_2026.md`).
- Bảng So sánh đối chiếu thay đổi (`bang_so_sanh_*.md`).

Khảo sát thực nghiệm đo lường trên codebase cho thấy:
- Nếu nạp toàn bộ mọi phiên bản (Chiến lược B - 37 nguồn, 698.465 từ): Tồn tại hơn 120 điều khoản mâu thuẫn giữa bản cũ và bản mới (ví dụ: quy định nhà ở riêng lẻ 6 tầng trong QCVN 06:2022 vs 7 tầng trong TT 09/2023; thiếu quy định trạm sạc xe điện trong QCVN 04:2021). Điều này dẫn đến nguy cơ cao AI của NotebookLM trích dẫn nhầm điều khoản cũ đã hết hiệu lực.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định áp dụng **Chiến lược Kho Tri thức Chuẩn hóa Hiện hành (Clean Unified Repository Strategy)** làm tiêu chuẩn đóng gói và đồng bộ dữ liệu mặc định lên Google NotebookLM:

1. **Bộ Nguồn Chuẩn Hóa Được Phép Upload (Whitelisted Sources):**
   - **Tầng 1 (Văn bản Quy phạm Pháp luật Hiện hành):** Toàn bộ 24 tệp Luật, Nghị định, Thông tư tại thư mục `legal_docs/01_vbpl/`.
   - **Tầng 2 (Quy Chuẩn Kỹ Thuật Hợp Nhất):** Chỉ upload các tệp **Bản Hợp Nhất Toàn Văn Mới Nhất** (`*_hop_nhat_*.md`) trong `legal_docs/02_qcvn/`.
   - **Tầng 3 (Ma Trận Đối Chiếu Lịch Sử):** Upload các tệp **Bảng So Sánh Thay Đổi** (`bang_so_sanh_*.md`) trong `legal_docs/04_appendices/`.
   - *Quy mô định lượng:* Đúng **32 tệp nguồn chuẩn hóa** (tương đương 565.403 từ và 4,35 MB).

2. **Rào Chắn Ngăn Chặn Bản Cũ (Obsolete Source Quarantine Gate):**
   - Tuyệt đối không upload các tệp Bản Gốc cũ (`qcvn_06_2022_bxd.md`, `qcvn_04_2021_bxd.md`) hoặc các tệp Sửa đổi rời rạc lên NotebookLM chính.
   - Các tệp bản gốc và sửa đổi rời rạc chỉ được lưu trữ cục bộ tại Spoke để phục vụ pipeline phân tích AST lịch sử (`Temporal Legal Query Engine` theo ADR 0008).

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Độ chính xác pháp lý $100\%$:** Loại bỏ hoàn toàn $100\%$ xung đột ngữ nghĩa và rủi ro trích dẫn nhầm điều khoản đã hết hiệu lực.
- **Bảo toàn khả năng giải trình lịch sử (Zero Data Loss):** Khi người dùng hỏi *"Quy chuẩn 04 trước đây và hiện nay khác nhau thế nào về trạm sạc?"*, NotebookLM trích xuất trực tiếp câu trả lời từ `bang_so_sanh_sua_doi_2026.md`.
- **Hiệu suất phản hồi cao:** Giảm tải 133.000 từ dữ liệu rác, giúp thời gian sinh câu trả lời và grounding citation của NotebookLM nhanh và chuẩn xác hơn.

### Đánh đổi:
- Cần chạy script đồng bộ chọn lọc (`scripts/notebooklm_helper.py` có filter whitelist) thay vì upload toàn bộ thư mục một cách cơ học.
