# ADR 0017: AST Structural Patching via Semantic Action Tokens for Legislative Consolidation

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-19
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0001: Dual-Track VBHN](0001-vbhn-dual-track-provenance.md), [ADR 0011: Atomic Clause Chunking](0011-atomic-clause-rag-chunking-strategy.md), [ADR 0016: Dual-Track Hybrid PDF Anchor](0016-dual-track-hybrid-pdf-anchor-of-trust.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Trong hệ thống pháp luật xây dựng Việt Nam:
- Các Thông tư, Nghị định và Quy chuẩn kỹ thuật quốc gia thường xuyên được sửa đổi, bổ sung hoặc bãi bỏ từng phần bằng các văn bản sửa đổi chuyên ngành (ví dụ: Thông tư 31/2026/TT-BXD sửa đổi QCVN 04:2021/BXD; Thông tư 09/2023/TT-BXD sửa đổi QCVN 06:2022/BXD).
- Việc tạo ra văn bản hợp nhất toàn văn (`*_hop_nhat_*.md`) và ma trận đối chiếu thay đổi (`bang_so_sanh_*.md`) nếu thực hiện thủ công sẽ tốn nhiều nhân lực và dễ sai sót.
- Ngược lại, nếu sử dụng LLM thuần túy (Prompt-based Rewrite), có nguy cơ cao xảy ra hiện tượng **ảo giác (hallucination)**, thay đổi ngoài ý muốn các câu chữ gốc tại các điều khoản không bị sửa đổi, phá vỡ tính bất biến và độ tin cậy tuyệt đối của tri thức pháp lý.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định thiết lập **Động cơ Hợp nhất Văn bản Pháp luật theo Cơ chế Vá Cấu Trúc Cây Cú Pháp Nguyên Tử (AST Structural Patching Engine)**:

1. **Ngữ pháp Thao tác Lập quy (Semantic Action Tokens Grammar):**
   Động cơ phân tích cú pháp văn bản sửa đổi thành tập hợp các Action Token xác định:
   - `REPLACE_CLAUSE(target_anchor, new_content)`: Thay thế toàn bộ nội dung một điều/khoản/mục cũ bằng nội dung mới.
   - `INSERT_CLAUSE(parent_anchor, insert_position, new_clause)`: Bổ sung một điều khoản mới vào vị trí xác định trong cây phân cấp.
   - `AMEND_SUBCLAUSE(parent_anchor, subclause_id, new_content)`: Sửa đổi một điểm hoặc gạch đầu dòng con mà không ảnh hưởng đến các điểm anh em.
   - `REPEAL_CLAUSE(target_anchor)`: Đánh dấu bãi bỏ điều khoản kèm ghi chú pháp lý gạch ngang hoặc ẩn.
   - `SUBSTITUTE_PHRASE(target_anchor, old_phrase, new_phrase)`: Thay thế chính xác cụm từ kỹ thuật trong điều khoản chỉ định.

2. **Quy trình Thực thi Xác định (Deterministic Execution Pipeline):**
   - **Bước 1 (Parse Source AST):** Tải cây AST `clauses.json` của văn bản gốc.
   - **Bước 2 (Apply Action Tokens):** Áp dụng tuần tự các bản vá (*AST Patches*) vào đúng vị trí nút cây tương ứng.
   - **Bước 3 (Inject Canonical Provenance Callouts):** Tự động bao bọc nội dung sửa đổi/bổ sung trong các khối Callout chuẩn:
     ```markdown
     > [!IMPORTANT]
     > *(Bổ sung/Sửa đổi bởi Điều X Thông tư Y/Z)*
     ```
   - **Bước 4 (Render Outputs):** Kết xuất đồng thời:
     - Văn bản hợp nhất toàn văn: `*_hop_nhat_*.md`.
     - Cây dữ liệu AST hợp nhất: `clauses.json` với đầy đủ siêu dữ liệu `jurisdiction`, `grace_period_end`, `source_pdf_page`.
     - Bảng đối chiếu so sánh: `bang_so_sanh_*.md` phân loại mức độ sai phạm kiểm toán.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Độ chính xác tuyệt đối ($100\%$ Deterministic):** Không có rủi ro ảo giác LLM; các điều khoản không sửa đổi được giữ nguyên vẹn $100\%$ ký tự.
- **Tự động hóa hoàn toàn & Có thể Kiểm thử (Testable & CI-Verified):** Các bản vá AST có thể chạy kiểm thử đơn vị (*Unit Tests*) và đối soát thẻ neo tự động qua `verify_cross_links.py`.
- **Khả năng mở rộng:** Module có thể tái sử dụng trên Hub để hợp nhất mọi loại hình văn bản pháp luật (Luật, Nghị định, Thông tư, QCVN, TCVN).

### Đánh đổi:
- Cần duy trì và cập nhật bộ parser regex/NLP cho các biến thể câu chữ trong thể thức lập quy của các cơ quan ban hành khác nhau.
