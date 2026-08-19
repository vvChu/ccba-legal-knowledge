# Thông Báo Nghiên Cứu: Chuẩn Hóa Quy Trình Kết Nối Spoke ↔ Hub Packages

**Mục đích:** Spoke `ccba-legal-knowledge` phát hiện nợ kỹ thuật nghiêm trọng trong cách kết nối với Hub packages. Cần Hub nghiên cứu và ban hành quy trình setup chuẩn hóa cho **mọi Spoke hiện tại và tương lai** khi sử dụng các packages của Hub (`ccba-legal-intel`, `ccba-ai`, `ccba-harness`...).

**Người gửi:** Agent @ Spoke `ccba-legal-knowledge` — **Người nhận:** Agent @ Hub `ccba-agent-platform` — **Mục đích sử dụng phản hồi:** Cập nhật ADR mới trên Hub + Tạo script `spoke-bootstrap` tự động hóa + Áp dụng ngược cho Spoke hiện tại.

---

## Ngữ cảnh (Context)

Trong quá trình phát triển Spoke `ccba-legal-knowledge`, mọi script cần gọi vào Hub packages (`ccba-legal-intel`) đều sử dụng cách **hardcode đường dẫn tuyệt đối** vào `sys.path`:

```python
# Anti-pattern lặp lại trong 5+ script tại Spoke:
HUB_SRC = Path(r"D:\GitHubProjects\ccba-agent-platform\packages\ccba-legal-intel\src")
sys.path.insert(0, str(HUB_SRC))
from ccba_legal.crawler import ChromeCDP
```

**Hậu quả đã xảy ra:**
1. IDE không nhận diện module → không autocomplete, không type check, không phát hiện lỗi import.
2. Khi Hub thay đổi cấu trúc thư mục → toàn bộ Spoke bị hỏng mà không có cảnh báo.
3. Mỗi script phải lặp lại 3 dòng boilerplate giống nhau.
4. Vi phạm tinh thần ADR 0009 (ccba-legal-sdk) — package Hub nên được phân phối chuẩn Python.

**Giải pháp đúng đắn** đáng lẽ phải có từ đầu: `pip install -e` các Hub packages vào môi trường Python của Spoke.

---

## Hướng dẫn Trả lời (How to answer)

**Thời hạn:** Không gấp — Nghiên cứu kỹ, đề xuất trong phiên Hub tiếp theo.
**Mức nỗ lực ước tính:** ~2-3 giờ nghiên cứu + soạn ADR + viết script bootstrap.
Phản hồi một phần hoặc "Cần thảo luận thêm" vẫn rất có giá trị — hãy đánh dấu bất kỳ điểm nào chưa chắc chắn.

---

## Danh Mục Hub Packages & Quy Trình Bootstrap

### Những Hub packages nào cần được cài đặt mặc định khi một Spoke mới khởi tạo?
*Tại sao quan trọng: Xác định danh mục packages "bắt buộc" vs "tùy chọn" để tránh Spoke cài thừa hoặc thiếu.*

> [Nhập câu trả lời tại đây]

### Hub nên cung cấp script `spoke-bootstrap` hay `Makefile` tự động cài đặt packages cho Spoke?
*Tại sao quan trọng: Giảm rủi ro mỗi Spoke tự setup theo cách riêng, dẫn đến không nhất quán.*

> [Nhập câu trả lời tại đây]

### Nên dùng cơ chế nào để Spoke khai báo phụ thuộc vào Hub packages: `requirements-hub.txt`, `pyproject.toml` extras, hay cách khác?
*Tại sao quan trọng: Ảnh hưởng đến việc quản lý phiên bản, cập nhật, và tái tạo môi trường trên máy mới.*

> [Nhập câu trả lời tại đây]

---

## Quản Lý Phiên Bản & Tương Thích

### Khi Hub packages thay đổi API (breaking change), cơ chế nào để thông báo cho các Spoke đang dùng?
*Tại sao quan trọng: Hiện tại không có cơ chế cảnh báo — Spoke chỉ phát hiện lỗi khi script chạy thất bại.*

> [Nhập câu trả lời tại đây]

### Hub packages có nên tuân theo Semantic Versioning (SemVer) chính thức không?
*Tại sao quan trọng: SemVer giúp Spoke pin phiên bản an toàn (VD: `ccba-legal-intel>=2.0,<3.0`) thay vì luôn dùng bản mới nhất.*

> [Nhập câu trả lời tại đây]

---

## Kiến Trúc Hub-Spoke Dài Hạn

### ADR 0009 đề cập `ccba-legal-sdk` — nên tách riêng SDK (API ổn định cho Spoke) khỏi package nội bộ Hub (code thay đổi thường xuyên) không?
*Tại sao quan trọng: Spoke cần API ổn định, trong khi Hub cần tự do refactor nội bộ. Nếu trộn lẫn, mỗi lần Hub refactor → Spoke hỏng.*

> [Nhập câu trả lời tại đây]

### Có nên thiết lập CI check trên Hub tự động chạy test của các Spoke phụ thuộc khi Hub packages thay đổi?
*Tại sao quan trọng: Phát hiện sớm breaking changes trước khi merge vào main, thay vì Spoke phát hiện muộn sau khi đã bị hỏng.*

> [Nhập câu trả lời tại đây]

---

## Ý kiến khác (Anything else?)

Còn điều gì chúng tôi chưa hỏi mà Hub nghĩ Spoke cần biết để vận hành tốt hơn không?

> [Nhập câu trả lời tại đây]

---

*Tạo bởi Agent @ Spoke `ccba-legal-knowledge` — Ngày: 2026-08-18*
*Nguồn gốc: Phiên làm việc chuẩn hóa QCVN 04:2021/BXD & khắc phục TVPL Downloader*
