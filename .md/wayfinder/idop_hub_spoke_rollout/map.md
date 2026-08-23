# 🗺️ Wayfinding Map: Triển Khai & Vận Hành Mạng Lưới Hub-Spoke Theo Nền Tảng IDOP CCBA

> **Trạng thái:** ACTIVE  
> **Khởi tạo:** 2026-08-22T14:37:28+07:00  
> **Mục tiêu:** Định hướng và giải mã toàn bộ lộ trình đưa mô hình Hub-Spoke vào vận hành thực tế tại CCBA.

---

## 🎯 1. Điểm Đích (Destination)

Thiết lập một **Khung Vận Hành Toàn Trình (Actionable Operational Framework)** chuẩn mực, cho phép:
1. Mọi kỹ sư CCBA có thể tự thiết lập **Personal Workspace Spoke** trên máy tính cá nhân trong 2 phút để tận dụng AI Gateway.
2. Mọi **Dự án Mới** có thể khởi tạo **Project Delivery Spoke** kết nối trơn tru với CDE Master OneDrive 5TB và 58 SharePoint Lists.
3. Ranh giới dữ liệu và dòng tiền được tự động hóa 100% qua cơ chế IDOPBridge và Tiered AI Pre-Submission Gate mà không gặp sự cố gián đoạn (Zero-Downtime).

---

## 📌 2. Ghi Chú & Kỹ Năng Bổ Trợ (Notes)
- **Kỹ năng liên quan:** `wayfinder`, `handoff`, `grilling`, `spoke-adopter`, `platform-loader`.
- **Hiến pháp tham chiếu:** [ADR 0041](file:///D:/GitHubProjects/ccba-agent-platform/docs/adr/0041-hub-spoke-ecosystem-taxonomy-and-archetypes.md), [ADR 0042](file:///D:/GitHubProjects/ccba-agent-platform/docs/adr/0042-tiered-ai-pre-submission-gate-and-tri-repo-sync.md), [ADR 0043](file:///D:/GitHubProjects/ccba-agent-platform/docs/adr/0043-idop-active-dev-resilience-and-fallback.md), [ADR 0044](file:///D:/GitHubProjects/ccba-agent-platform/docs/adr/0044-spoke-hub-package-bootstrap-standard.md).

---

## ⚖️ 3. Quyết Định Đã Chốt (Decisions So Far)

| STT | Quyết Định / Tiêu Chuẩn | Nội Dung Chi Tiết |
| :---: | :--- | :--- |
| **D1** | **Phân loại 4 Core Archetypes** | Hub (`platform_hub`), Quy chế (`enterprise_governance`), Pháp lý (`knowledge_corpus`), Dự án (`project_delivery`). *(Theo ADR 0041)* |
| **D2** | **Cơ chế Đồng bộ Tri-Repo Sync** | Đồng bộ tuần tự lúc 00:00: `ccba-legal-knowledge` $\rightarrow$ `IDOP-CCBA-WAY` $\rightarrow$ `ccba-agent-platform`. *(Theo ADR 0042)* |
| **D3** | **Cầu nối IDOPBridge & Local Queue** | Đệm dữ liệu tại `.md/idop_staged/` khi offline, tự động đẩy bù (Idempotent Replay) khi có mạng. *(Theo ADR 0043)* |
| **D4** | **Bootstrap Package qua Editable Link** | Cài đặt qua `pip install -e "[hub_path]/packages/..."` vào `.venv`, cô lập bằng Pre-commit hook. *(Theo ADR 0044)* |
| **D5** | **Chính sách Spoke Cá nhân (Personal Spoke)** | Khuyến khích tạo cục bộ trên máy để nháp/nghiên cứu; **Không push** lên Hub Remote Registry. |
| **D6** | **Chính sách Phòng ban Hành chính** | KHKT, TCKT, TCHC không tạo Spoke Git riêng $\rightarrow$ Vận hành tập trung trên 58 SharePoint Lists. |

---

## 🎫 4. Các Vé Công Việc Ở Biên Giới (Frontier Tickets)

### 🟢 Ticket 1: [HITL - Grilling] [Xác Lập Quy Trình Chuyển Giao Dữ Liệu Từ Personal Spoke Sang Spoke Dự Án & 58 Lists](ticket_01_personal_to_project_flow.md)
* **Loại:** `Grilling [HITL]`
* **Mục tiêu:** Làm rõ cơ chế kiểm duyệt và thao tác của kỹ sư khi chuyển kết quả làm việc nháp từ máy cá nhân vào hồ sơ nghiệm thu chính thức của dự án.
* **Trạng thái:** OPEN (Unblocked)

### 🟢 Ticket 2: [AFK - Template] [Bộ Mẫu Cấu Hình `workspace_context.yaml` Chuẩn Cho Từng Archetype](ticket_02_workspace_context_templates.md)
* **Loại:** `Research / Template [AFK]`
* **Mục tiêu:** Tạo sẵn 4 bộ mẫu `workspace_context.yaml` tương ứng với 4 Archetypes để kỹ sư chỉ việc copy dùng ngay.
* **Trạng thái:** OPEN (Unblocked)

### 🟢 Ticket 3: [AFK - Task] [Soạn Thảo Sổ Tay Hướng Dẫn Kỹ Sư Mới (1-Page Onboarding Quickstart)](ticket_03_onboarding_cheatsheet.md)
* **Loại:** `Task [AFK]`
* **Mục tiêu:** Viết tài liệu tóm gọn 1 trang hướng dẫn kỹ sư mới cài đặt môi trường trong 5 phút.
* **Trạng thái:** OPEN (Unblocked)

---

## 🌫️ 5. Sương Mù Chiến Trận / Chưa Xác Định Rõ (Not Yet Specified)
- *Cơ chế cấp phát & Quản lý hạn mức Virtual Key AI Gateway cho từng kỹ sư / dự án.*
- *Quy trình tự động hóa nhân bản (scaffold) cấu trúc 58 SharePoint Lists khi mở một dự án mới.*
- *Mô hình kiểm định chéo giữa các Spoke Dự án khác nhau (Cross-Spoke Audit).*

---

## 🚫 6. Ngoài Phạm Vi (Out of Scope)
- Sửa đổi cấu trúc core của Microsoft 365 / SharePoint Tenant.
- Tự ý thay đổi nội dung các văn bản pháp luật gốc trong `ccba-legal-knowledge`.
