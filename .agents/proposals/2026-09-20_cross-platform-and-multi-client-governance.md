---
proposal_id: "2026-09-20_cross-platform-and-multi-client-governance"
type: "architecture"
name: "cross-platform-and-multi-client-governance"
status: "open"
priority: "Cao"
proposed_by_project: "ccba-legal-knowledge"
proposed_date: "2026-09-20"
hub_issue: "https://github.com/vvChu/ccba-agent-platform/issues/299"
applies_to:
  - "Core Platform"
  - "Quản trị Hub-Spoke"
  - "Bảo mật & Phân quyền"
  - "Pháp lý & Quy chuẩn"
---

# Đề Xuất Kiến Trúc: Chuẩn Hóa Đa Nền Tảng (Linux/WSL) & Cơ Chế Bảo Vệ Hub-Spoke Đa Thiết Bị / Đa Người Dùng

## 1. Tóm Tắt Đề Xuất (Executive Summary)
Đề xuất nâng cấp kiến trúc tổng thể của CCBA Agent Services Platform (`ccba-agent-platform`) nhằm:
1. **Hỗ trợ toàn diện môi trường đa hệ điều hành (Cross-Platform Linux/WSL/POSIX)** cho các Spoke clients, loại bỏ các giả định cứng về môi trường Windows.
2. **Thiết lập cơ chế bảo vệ khi CÙNG MỘT USER làm việc trên NHIỀU MÁY (Single-User, Multi-Device)**: ngăn rò rỉ cấu hình máy cục bộ, tránh xung đột khi đồng bộ Cloud/NotebookLM và ngăn chặn phân kỳ nhánh Git.
3. **Thiết lập khung tương tác an toàn khi NHIỀU USER KHÁC NHAU cùng làm việc (Multi-User Collaboration)**: phân quyền nhánh (Branch Protection), cô lập bí mật (Secret Isolation), ký danh trách nhiệm và giải quyết xung đột trên sổ bạ tri thức tập trung.

---

## 2. Các Trụ Cột Kiến Trúc Cần Cụ Thể Hóa

### Trụ Cột 1: Nhận Diện & Phân Giải Đường Dẫn Đa Nền Tảng (Linux/WSL/Windows)
- **Vấn đề:** Hardcoded `hub_path: D:\...` trong `workspace_context.yaml` khiến `Path.is_absolute()` trên Linux trả về `False`, gây lỗi âm thầm khi tìm packages của Hub.
- **Giải pháp:**
  - Hỗ trợ Multi-OS Path mapping trong cấu hình SSoT hoặc quy chuẩn đường dẫn tương đối (`../ccba-agent-platform`).
  - Ưu tiên biến môi trường `CCBA_HUB_PATH` trên toàn bộ hệ thống Hub packages.
  - Tự động chuyển đổi `wslpath` khi phát hiện môi trường WSL.

### Trụ Cột 2: Khử Phụ Thuộc Windows Word COM (ADR 0043 Headless Fallback)
- **Vấn đề:** ADR 0043 yêu cầu xuất Vector PDF qua `Word COM` (`win32com`), khiến Spoke trên Linux/CI-CD không thể xuất bản chuẩn hóa.
- **Giải pháp:**
  - Bổ sung `HeadlessFallbackEngine` với LibreOffice (`soffice --headless --convert-to pdf`).
  - Hoặc cung cấp Microservice xuất PDF tập trung trên Server Spark qua Tailscale VPN.

### Trụ Cột 3: Cơ Chế Bảo Vệ Cùng Một User Làm Việc Trên Nhiều Máy (Single-User, Multi-Device)
- **Vấn đề:** Một kỹ sư dùng máy bàn Windows ở công ty và laptop Linux ở nhà. Nguy cơ commit đường dẫn cục bộ đè lên nhau, race-condition khi đồng bộ NotebookLM, và quên rebase gây lệch SSoT.
- **Giải pháp bảo vệ:**
  1. **Tách biệt tuyệt đối trạng thái máy (Machine-State Decoupling):** Cấm commit đường dẫn tuyệt đối hoặc định danh máy. Cấu hình máy phải nằm trong `.env` (được `.gitignore`) hoặc biến môi trường hệ thống.
  2. **Pre-commit Hook `check_machine_state.py`:** Chặn commit nếu phát hiện đường dẫn chứa ổ đĩa (`C:`, `D:`) hoặc username máy (`/home/username`, `C:\Users\...`).
  3. **Khóa phân tán khi đồng bộ Cloud (Cloud Sync Soft-Locking):** Khi chạy `sync_notebooklm_knowledge.py` hoặc đẩy file lên Cloud Vault, tạo lockfile có TTL trên cloud storage để tránh 2 máy cùng sync một lúc.
  4. **Quy trình Git Rebase bắt buộc:** Tự động kiểm tra trạng thái remote trước khi chạy test/convert để cảnh báo nếu máy chưa kéo commit mới nhất về.

### Trụ Cột 4: Cơ Chế Bảo Vệ Khi Nhiều User Khác Nhau Cùng Tương Tác (Multi-User Governance)
- **Vấn đề:** Nhiều kỹ sư cùng nạp văn bản, sửa đổi quy chuẩn, hoặc đóng góp ngược lên Hub. Nguy cơ ghi đè `main`, xung đột `legal_registry.yaml`, và lộ lọt credentials.
- **Giải pháp bảo vệ:**
  1. **Branch Protection & Forking / PR Model:** Cấm tuyệt đối push trực tiếp lên `main` của Hub và `main` của Spoke. Mọi thay đổi đều phải qua Pull Request và vượt qua CI Gate (`verify-patch`, `validate_legal_spoke.py`).
  2. **Cô lập Bí mật (Zero-Secret Invariant):** Không lưu API Key AI Gateway, Service Account Drive Vault trong mã nguồn. Mọi user dùng biến môi trường cục bộ hoặc cơ chế secret vault phân quyền.
  3. **Phân mảnh Sổ bạ (Sharded Registry Strategy):** Thay vì tất cả user cùng sửa một file monolithic `legal_registry.yaml`, Hub nên hỗ trợ gom nhóm registry theo thư mục (`legal_docs/**/metadata.yaml`) và tự động compile thành registry tổng bằng CLI, triệt tiêu nguy cơ merge conflict.
  4. **Ký danh trách nhiệm (Audit Provenance):** Gắn thông tin `contributor_id`, commit SHA và kiểm định chất lượng vào metadata của gói tri thức.

### Trụ Cột 5: Nâng Cấp Kỹ Năng Điều Phối Toàn Cục `/ccba-platform`
- Bổ sung kiểm định OS Topology (Pha 1.4) để phát hiện sai lệch môi trường và hướng dẫn cấu hình tức thì.

### Trụ Cột 6: Chuẩn Hóa Cú Pháp Tài Liệu & Git Line Endings
- Cung cấp template `.gitattributes` (`* text=auto eol=lf`) ngăn lỗi `\r: command not found`.
- Chuẩn hóa cú pháp lệnh trong tài liệu sang POSIX Bash và PowerShell đa năng.
