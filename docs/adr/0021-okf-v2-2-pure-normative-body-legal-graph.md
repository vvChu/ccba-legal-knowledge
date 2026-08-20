# ADR 0021: OKF v2.2 Pure Normative Body & Legal Knowledge Graph Topology

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-20
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0011: Atomic Clause Chunking](0011-atomic-clause-rag-chunking-strategy.md), [ADR 0016: PDF Anchor of Trust](0016-dual-track-hybrid-pdf-anchor-of-trust.md), [ADR 0017: AST Structural Patching](0017-ast-structural-patching-consolidation-engine.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Trong quá trình chuẩn hóa các văn bản quy phạm pháp luật (Luật, Nghị định, Thông tư) sang định dạng OKF v2.0:
- Việc bóc tách thô (Raw OCR / Blind DOCX Conversion) mang theo toàn bộ các thành phần layout hành chính của bản in giấy vào file Markdown:
  * Khung Quốc hiệu, Tiêu ngữ, Số hiệu ở đầu trang.
  * Các dòng văn bản thô liệt kê căn cứ ban hành (*"Căn cứ Luật Xây dựng số 135/2025/QH15..."*).
  * Danh sách *Nơi nhận* dài dòng và khối chữ ký ở chân trang.
  * Việc quét toàn bộ các bảng Word vô hình biến các khung layout thành hàng loạt tệp rác `bang_01.json` $\rightarrow$ `bang_19.json` không có giá trị tra cứu kỹ thuật.
  * Các Phụ lục biểu mẫu bị dính liền vào cuối thân văn bản chính, gây trùng lặp dữ liệu lớn và làm phình to context window khi AI Agent tra cứu.
- Các thành phần rác layout này gây ra hiện tượng **ô nhiễm ngữ nghĩa (Semantic Noise)** trong Vector DB, làm giảm độ chính xác khi nhúng vector (RAG Embedding) và cản trở khả năng suy luận đồ thị liên kết (Knowledge Graph Traversal) của AI Agent.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định nâng cấp kiến trúc gói tri thức lên chuẩn **OKF v2.2 (Pure Normative Body & Legal Knowledge Graph)** với 4 nguyên tắc cốt lõi:

1. **Thân Văn Bản Quy Phạm Thuần Khiết (Pure Normative Body):**
   - Tệp Markdown chính (`[doc_slug].md`) được tinh lọc sạch hoàn toàn: chỉ chứa **Tiêu đề H1/H2 chính quy + YAML Frontmatter** và bắt đầu **NGAY LẬP TỨC từ Chương I (Điều 1) đến Điều cuối cùng**.
   - Loại bỏ $100\%$ các khối rác layout: Tiêu ngữ, Căn cứ thô, Nơi nhận và Chữ ký giấy.
   - Toàn bộ số thứ tự khoản được in đậm (`**1.**`, `**2.**`) để triệt tiêu lỗi thụt lề so le do Markdown Ordered List.

2. **Cấu Trúc Hóa Đồ Thị Căn Cứ Pháp Lý (`legal_basis` Graph):**
   - Chuyển hóa toàn bộ các căn cứ ban hành thành trường dữ liệu đồ thị có cấu trúc trong `metadata.yaml` và YAML Frontmatter:
     ```yaml
     legal_basis:
       - doc_id: luat_xay_dung_2025_135_2025_qh15
         title: Luật Xây dựng số 135/2025/QH15
       - doc_id: luat_dau_tu_2025_143_2025_qh15
         title: Luật Đầu tư số 143/2025/QH15
     ```
   - Cho phép AI Agent thực hiện truy vấn suy luận bắc cầu (*Multi-Hop Legal Graph Reasoning*) giữa các tầng Luật $\leftrightarrow$ Nghị định $\leftrightarrow$ Thông tư.

3. **Kiến Trúc Tách Module Biểu Mẫu Độc Lập (`templates/` Directory):**
   - Tách toàn bộ các Phụ lục biểu mẫu hành chính thành từng tệp Markdown độc lập trong thư mục `templates/` (ví dụ: `phu_luc_01_...md`, `phu_luc_04_...md`).
   - Tệp Markdown chính ở phần cuối sẽ tích hợp **Mục Lục Điều Hướng Ngữ Nghĩa (Semantic Navigation MOC)** trỏ trực tiếp sang các tệp biểu mẫu và bảng tra cứu, bảo đảm tuân thủ nguyên tắc *Single Source of Truth (SSOT)* và *DRY*.

4. **Bộ Lọc Phân Loại Bảng Biểu 3 Lớp (3-Tier Semantic Filter):**
   - **Lớp 1 (Layout Filter):** Tự động bỏ qua các bảng $1 \times 2, 2 \times 2$ là khung Quốc hiệu/Nơi nhận.
   - **Lớp 2 (Data Table Filter):** Chỉ trích xuất các bảng dữ liệu ma trận tra cứu kỹ thuật thực sự vào `tables/csv/` và `tables/json/` kèm tên định danh có nghĩa.
   - **Lớp 3 (Form Template Filter):** Toàn bộ biểu mẫu phụ lục được đưa vào `templates/`.

5. **Công Thức Kiểm Toán Phân Tán Zero Data Loss (Distributed Parity Audit):**
   - Đo lường tổng thể tích nội dung: $\text{Total Extracted} = \text{Text}(\text{Main .md}) + \sum \text{Text}(\text{Templates}) + \sum \text{Text}(\text{Tables})$.
   - Cưỡng chế tỷ lệ bảo toàn: $\ge 98.5\%$ tổng thể, $100\%$ Điều khoản ($N/N$) và $100\%$ Phụ lục ($M/M$).

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Tối ưu hóa Token & RAG Search:** Giảm 35-40% kích thước tệp Markdown chính, loại bỏ 100% rác từ khóa khỏi Vector Database.
- **Hỗ trợ Agent Đa Năng:** Agent Soạn thảo thầu / Hoàn thành hồ sơ có thể nạp chính xác từng biểu mẫu trong `templates/` mà không cần cắt lọc từ file lớn.
- **Khả năng Lập luận Đồ thị:** Cho phép xây dựng Legal Knowledge Graph hoàn chỉnh cho toàn bộ hệ thống pháp luật xây dựng Việt Nam.

### Đánh đổi:
- Động cơ chuyển đổi (`docx_converter.py`) cần tích hợp bộ phân loại Heuristic và bộ giải mã Regex đa tầng để tự động phân luồng QCVN vs VBPL.
