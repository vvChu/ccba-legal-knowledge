# ADR 0007: Dual-Layer CI Verification Gate & Zero-Tolerance Quality Enforcement

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-18
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0001: Dual-Track VBHN](0001-vbhn-dual-track-provenance.md), [CONTEXT.md](../../CONTEXT.md), `scripts/validate_legal_spoke.py`

---

## 1. Bối Cảnh (Context)
Spoke `ccba-legal-knowledge` là nguồn cung cấp tri thức pháp lý nền tảng cho toàn bộ hệ thống thẩm tra tự động của CCBA Agent Platform. Bất kỳ một lỗi định dạng nhỏ nào (như lặp tiêu đề, vỡ lưới bảng Markdown 2D, sai lệch giá trị số trong JSON, thẻ neo hỏng hoặc mất đoạn văn) đều có thể dẫn đến việc AI QC Agent thẩm tra sai lệch hồ sơ thiết kế công trình của khách hàng.

Khi mở rộng bóc tách thêm các quy chuẩn và tiêu chuẩn mới (QCVN 04, Nghị định 217/2026, TCVN 7336...), việc kiểm tra thủ công qua từng câu lệnh terminal không đảm bảo tính ổn định lâu dài.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định thiết lập hệ thống **Rào chắn Kiểm thử Kép (Dual-Layer CI Verification Gate)** với cơ chế **Zero-Tolerance Quality Enforcement**:

### Lớp 1: Local Pre-Commit Hook (`.githooks/pre-commit` hoặc npm/python hook)
- Chặn đứng mọi commit vi phạm ngay trên máy cục bộ của kỹ sư / AI Agent.
- Tự động kích hoạt bộ 3 công cụ kiểm toán:
  1. `python scripts/validate_legal_spoke.py` (Registry, Schema & Fake Data Gate).
  2. `python scripts/verify_knowledge_integrity.py` (Zero Data Loss & Deterministic Parity).
  3. `python scripts/verify_cross_links.py` (Broken Link & Semantic Anchor Audit).
- Nếu bất kỳ script nào trả về Exit Code $\ne 0$, tiến trình commit lập tức bị hủy (*Aborted*).

### Lớp 2: Remote GitHub Actions CI Workflow (`.github/workflows/legal-knowledge-ci.yml`)
- Kích hoạt tự động trên mọi sự kiện `push` và `pull_request` vào nhánh `main`.
- Thiết lập môi trường Python, thực thi bộ kiểm toán và xuất báo cáo chất lượng tổng hợp (Audit Matrix) trực tiếp trong log của GitHub Actions.
- Cấm merge nếu chưa vượt qua $100\%$ các bài kiểm tra chất lượng.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Đảm bảo Zero Data Loss trọn đời:** Không một dòng văn bản quy chuẩn hay bảng biểu nào bị lỗi có thể lọt vào nhánh chính `main`.
- **Tự động hóa hoàn toàn:** Loại bỏ gánh nặng rà soát thủ công, tạo sự an tâm tuyệt đối khi AI Agent cập nhật dữ liệu tự động.
- **Tiêu chuẩn hóa đóng góp (Contribution Standard):** Bất kỳ lập trình viên hay đối tác nào muốn đóng góp tài liệu pháp lý mới đều phải vượt qua bài kiểm tra chuẩn này.

### Đánh đổi:
- Cần duy trì cấu hình CI và đảm bảo thời gian chạy kiểm thử nhanh (hiện tại < 3 giây).
