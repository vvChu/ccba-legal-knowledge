# ADR 0005: Semantic Legal URI Scheme & Registry Resolver Cho Viện Dẫn Đa Văn Bản

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-18
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0001: Dual-Track VBHN](0001-vbhn-dual-track-provenance.md), [CONTEXT.md](../../CONTEXT.md), `legal_registry.yaml`

---

## 1. Bối Cảnh (Context)
Trong các quy chuẩn và tiêu chuẩn kỹ thuật xây dựng (như QCVN 06:2022/BXD), có hàng trăm mối quan hệ viện dẫn chéo sang các văn bản pháp quy khác (ví dụ: TCVN 7336, TCVN 3890, QCVN 04:2021/BXD, Nghị định 175/2024/NĐ-CP).

Nếu sử dụng đường dẫn tệp tin tương đối cố định (`../../03_tcvn/...`):
1. **Dễ gãy vỡ liên kết (Fragile Links):** Khi thay đổi cấu trúc thư mục, đổi tên tệp tin hoặc di chuyển vị trí, hàng loạt liên kết sẽ bị hỏng (*Broken Links*).
2. **Lỗi 404 khi tài liệu đích chưa bóc tách:** Trong quá trình phát triển Spoke, các tài liệu đích có thể chưa sẵn sàng ở dạng Markdown, dẫn đến việc liên kết bị lỗi khi người dùng hoặc Agent bấm xem.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định chuẩn hóa toàn bộ các viện dẫn đa văn bản trong Spoke và Hub theo giao thức **Semantic Legal URI Scheme (`legal://`)**:

1. **Cấu trúc Định danh URI Pháp lý:**
   ```
   legal://[doc_id]#[clause_id]
   ```
   *Ví dụ:*
   - `[TCVN 7336:2021](legal://tcvn_7336_2021#muc-5-2)`
   - `[QCVN 04:2021/BXD](legal://qcvn_04_2021_bxd#muc-2-1-3)`
   - `[Nghị định 175/2024/NĐ-CP](legal://nd_175_2024_ndcp#dieu-12)`

2. **Cơ chế Phân giải qua Sổ đăng ký (`Registry URL Router`):**
   - Bộ điều hướng trung tâm đọc tệp `legal_registry.yaml` để ánh xạ `doc_id` sang đường dẫn thực tế trên đĩa (`legal_docs/...`).
   - **Trạng thái Trì hoãn Liên kết (Pending Fallback):** Nếu tài liệu đích có trạng thái `status: pending` hoặc chưa bóc tách sang Markdown, resolver sẽ trỏ an toàn về thẻ thông tin metadata trong Registry hoặc bản tóm tắt, tuyệt đối không để xảy ra lỗi 404.

3. **Tương thích Markdown Preview:**
   - Trong quá trình xuất bản hoặc hiển thị Markdown tĩnh, một build hook đơn giản sẽ chuyển đổi `legal://` sang đường dẫn tương đối nội bộ hoặc liên kết Web Portal của CCBA.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Kháng gãy vỡ $100\%$:** Đường dẫn vật lý có thể tự do tái cấu trúc mà không ảnh hưởng đến hàng nghìn liên kết trong nội dung văn bản.
- **Tương thích Đa nền tảng:** Hoạt động liền mạch giữa Spoke Tri thức, Spoke Dự án và Hub CCBA.
- **Hỗ trợ Agent Routing:** AI Agent chỉ cần đọc URI `legal://[doc_id]` là biết chính xác cần nạp bundle nào từ Hub mà không phải dò tìm tên file.

### Đánh đổi:
- Cần duy trì mã định danh `doc_id` thống nhất trong `legal_registry.yaml`.
