# ADR 0011: Atomic Clause RAG Chunking Strategy for Clause-Based Standards

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-19
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0001: Dual-Track VBHN](0001-vbhn-dual-track-provenance.md), [ADR 0005: Semantic Legal URI](0005-semantic-legal-uri-scheme.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Trong các quy chuẩn kỹ thuật xây dựng dạng điều khoản định mức (như QCVN 04:2021/BXD về Nhà chung cư, các chương điều khoản của QCVN 06:2022/BXD, Luật Xây dựng 2025):
- Cấu trúc văn bản thường được tổ chức theo mô hình **Danh mục lồng đa tầng (Nested Lists)**:
  * *Cấp 1:* Mục quy định lớn (ví dụ: `2.10.2.1 Yêu cầu kỹ thuật`).
  * *Cấp 2:* Điểm cụ thể (ví dụ: `b) Phân vùng riêng biệt và khoảng cách an toàn:`).
  * *Cấp 3:* Các quy định phân vùng chung (`+ Khu vực sạc xe điện được bố trí... Số lượng chỗ sạc trong mỗi phân vùng:`).
  * *Cấp 4:* Các định mức con phụ thuộc (`  - Khi bố trí trong tầng bán hầm/tầng hầm ≤ 25 chỗ sạc...`).

Nếu áp dụng phương pháp cắt nhỏ văn bản truyền thống (Micro-Chunking theo từng đoạn hoặc gạch đầu dòng):
- AI/RAG Agent sẽ làm đứt lìa câu quy định con khỏi câu dẫn điều kiện tiên quyết của cấp cha.
- Hậu quả: Dẫn đến lỗi suy diễn tai hại trong thẩm tra PCCC (ví dụ: hiểu nhầm là toàn bộ chung cư chỉ có tối đa 25 chỗ sạc thay vì hiểu là cho 1 phân vùng riêng biệt).

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định áp dụng tiêu chuẩn **Đóng gói Nguyên tử Cả Điều Khoản (Atomic Clause Chunking)** làm chiến lược RAG Chunking mặc định cho toàn bộ các quy chuẩn dạng điều khoản định mức trên Spoke `ccba-legal-knowledge`:

1. **Ranh Giới Chunking Nguyên Tử (Atomic Chunk Boundary):**
   - Đơn vị Document Chunk cơ sở trong Vector Database và AST Index (`clauses.json`) được xác định ở cấp **Mục lớn có đánh số quy định kỹ thuật** (H3/H4 như `2.10.2.1`, `2.11.2`, `1.4.x`).
   - Toàn bộ các điểm con (`a`, `b`, `c`...), các gạch đầu dòng `+` và các ý thụt lề `  -` bên trong mục đó bắt buộc phải nằm chung trong 1 Chunk duy nhất.

2. **Cưỡng Chế Thụt Lề Chuẩn CommonMark (Indentation Rule):**
   - Mọi danh sách lồng con bên trong Chunk nguyên tử phải sử dụng thụt lề đúng **2 spaces** (`  -`) để các mô hình Embedding/LLM nhận biết chính xác cấu trúc Cây cú pháp DOM.

3. **Cấu Trúc Hóa AST JSON Đồng Bộ:**
   - Trong `clauses.json`, trường `content` chứa toàn bộ văn bản Markdown chuẩn hóa của cả điều khoản, bảo đảm khi Agent truy xuất theo `ground_truth_id` sẽ nhận được 100% ngữ cảnh kỹ thuật.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Triệt tiêu hoàn toàn rủi ro mất ngữ cảnh điều kiện:** LLM luôn đọc được câu dẫn cha kèm theo định mức con, không bao giờ trích dẫn sai lệch quy chuẩn.
- **Tối ưu cho Audit Quy Chuẩn Toàn Diện:** Khi thẩm tra một hạng mục (như thiết kế khu vực sạc xe điện), Agent nhận trọn bộ từ yêu cầu khoảng cách, ngăn khoang cháy, hệ thống hút khói, cảnh báo khí CO/HF đến nút ngắt điện khẩn cấp trong 1 lượt truy vấn duy nhất.

### Đánh đổi:
- Kích thước payload của mỗi chunk lớn hơn (~500 - 1000 tokens), đòi hỏi mô hình Embedding hỗ trợ context window $\ge 1024$ tokens và LLM có khả năng tiếp nhận context phong phú.
