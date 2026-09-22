# 🗺️ Wayfinder Map: Cơ Chế Điều Phối Động 5 Bối Cảnh & Bảo Vệ Spoke Đa Máy (Context-Aware Dynamic Dispatch & Multi-Device Resilience)

> **Trạng thái:** 🟢 **COMPLETED & ARCHIVED**  
> **Thời điểm hoàn tất:** `2026-09-22T21:35:00+07:00`  
> **Hub PR liên kết:** [#328 (Đã Squash & Merge vào main)](https://github.com/vvChu/ccba-agent-platform/pull/328) | **Issue:** [#326 (Đã đóng)](https://github.com/vvChu/ccba-agent-platform/issues/326)  
> **Spoke Đồng Bộ:** `ccba-legal-knowledge` (15/15 Gates PASS, Cleanliness Audit PASS)  
> **Backlog Tách Ra:** Đề xuất RFC Issue trên Hub: `rfc(cli): deterministic init-spoke command to eliminate LLM non-determinism`

---

## 🎯 Điểm Đích (Destination)
Xây dựng và tích hợp trọn vẹn cơ chế **Điều Phối Động 5 Bối Cảnh (Context-Aware Dynamic Dispatch)** cho [/ccba-platform](file:///home/vvc/ccba/ccba-legal-knowledge/.agents/skills/ccba-platform/SKILL.md) cùng hệ thống phòng thủ 2 lớp (**2-Layer Defense**):
1. **Lớp 1 (UI Dynamic Filtering):** Tự động phân luồng 5 bối cảnh (Hub, Greenfield, Brownfield, Multi-Device Cloned, Healthy Ready), lọc bỏ 100% các lệnh nguy hiểm như `/ccba-init-spoke` và `/ccba-spoke-adopter` trên Spoke đã onboard.
2. **Lớp 2 (Hard Fail-Safe Gate):** Khóa cứng codebase tại `spoke_adopter.py` và `ccba-init-spoke` từ chối thực thi khi phát hiện `.md/workspace_context.yaml` đã tồn tại (hỗ trợ cờ `--force` giải cứu).
3. **Hub Packages & Path Resilience:** Khai báo `pymupdf>=1.23.0` trong `ccba-legal-intel`, hỗ trợ đường dẫn tương đối chuẩn POSIX `../ccba-agent-platform` xuyên suốt bộ công cụ (`spoke_adopter.py`, `discovery.py`, `spoke_bootstrap.py`, `sync_hub_adr_matrix.py`).
4. **Hiến Pháp Nền Tảng & Smart Merge:** Upstream 2 điều khoản bất biến (`Single-User Multi-Device` & `Remote Mutation Idempotency`) lên Hub canonical `AGENTS.md` và triển khai bộ parser gom cụm đa dòng (Multiline Bullet Parser) trong `coordinator.py` nhằm bảo tồn tuyệt đối các quy tắc riêng của Spoke khi chạy `sync_spoke.py`.

---

## 📝 Ghi Chú (Notes)
- **GitHub RFC Issue trên Hub:** [#326 (vvChu/ccba-agent-platform)](https://github.com/vvChu/ccba-agent-platform/issues/326)
- **Tài liệu đối soát bắt buộc:**
  - [learning_proposal.md](file:///home/vvc/.gemini/antigravity/brain/bbe6a22c-2adb-4dc2-a026-1c5cab5eb69d/learning_proposal.md) (Bản tổng hợp đề xuất & kết quả phản biện đối kháng)
  - `HUB-ADR-0041`: Hub-Spoke Ecosystem Taxonomy and Archetypes
  - `HUB-ADR-0044`: Spoke Bootstrap Engine & Editable Link Protocol
  - `HUB-ADR-0045`: Spoke Leakage Guard & Cleanliness Gate
  - `HUB-ADR-0058`: Hard Completion Lock (`python -m ccba_harness verify-patch`)
- **Nguyên tắc vận hành:** Plan, don't do. Mỗi ticket giải quyết trọn vẹn một quyết định và gói công việc độc lập.

---

## ⚖️ Quyết Định Đã Chốt (Decisions so far)
- [x] **[D-01] Mô hình 2 lớp bảo vệ (2-Layer Defense):** Kết hợp phân luồng UI menu động (Lớp 1) và khóa cứng fail-safe chặn thực thi trong code (Lớp 2).
- [x] **[D-02] Ma trận 5 bối cảnh (5 Contexts Topology):** (1) Hub Monorepo, (2) Greenfield Spoke, (3) Brownfield Spoke, (4) Multi-Device Cloned Spoke, (5) Healthy Ready Spoke.
- [x] **[D-03] Tiêu chuẩn đường dẫn tương đối (Relative POSIX Sibling Invariant):** Chuẩn hóa `hub_path` thành `../ccba-agent-platform` thay vì hardcode drive letter, fallback qua `CCBA_HUB_PATH` khi khác ổ đĩa.
- [x] **[D-04] Đồng bộ Hiến pháp cấp hạt nhân (Multiline Bullet Merge):** Không ghi đè section thô bạo, hợp nhất theo key bullet `**Invariant Name**:` để bảo tồn các điều khoản Spoke.
- [x] **[D-05] Cross-Drive Resilient Fallback:** Khi `os.path.relpath` gặp `ValueError` (Windows C: vs D:), tự động fallback `hub_path` về `None`, loại trừ hoàn toàn nguy cơ đóng cứng ký tự ổ đĩa máy đơn vào cấu hình.

---

## 🎫 Danh Sách Ticket Tại Biên Giới (Frontier Tickets)
- [x] **[T-01: Core Package & Path Resilience Engine](tickets/01_core_package_and_path_resilience.md)** `[Task - AFK]` *(DONE on Hub — Commit 30a2d6c0)*
- [x] **[T-02: Constitution Upstream & Smart Multiline Merge](tickets/02_constitution_upstream_and_multiline_merge.md)** `[Task - AFK]` *(DONE on Hub — Commit 30a2d6c0)*
- [x] **[T-03: Dynamic Dispatch Matrix & Skill Fail-Safe Gates](tickets/03_dynamic_dispatch_and_skill_gates.md)** `[Task - AFK]` *(DONE on Hub — Commit 30a2d6c0, 6d1c7b4f)*

---

## 🌫️ Sương Mù Chiến Trận / Chưa Xác Định Rõ (Not yet specified)
- **[Fog-01] Đóng gói CLI `init-spoke` tất định:** Hiện tại `/ccba-init-spoke` hoàn toàn dựa vào AI Agent tự tạo file Markdown. Đã chuyển giao và mở Issue RFC chính thức trên Hub: [#329 (vvChu/ccba-agent-platform)](https://github.com/vvChu/ccba-agent-platform/issues/329).
- ~~**[Fog-02] Kiểm thử Cross-Drive trên Windows Native:**~~ **[ĐÃ GIẢI TỎA]** Đã hoàn thiện qua unit test mô phỏng `test_additive_merge_handles_cross_drive_value_error` tại `tests/test_spoke_adopter.py`, xác nhận tự động gán `rel_hub_str = None` an toàn khi ném `ValueError`.

---

## 🚀 Kế Hoạch Đồng Bộ Về Spoke (Downstream Sync Milestone)
Sau khi Pull Request của Issue #326 được hợp nhất vào nhánh `main` trên Hub:
1. [x] **Thực thi đồng bộ Hiến pháp & Kỹ năng (Non-Destructive Merge):** Đã chạy `sync_spoke.py --apply --force`, bảo tồn toàn bộ custom sections.
2. [x] **Kiểm tra độ sạch môi trường:** `check_spoke_cleanliness.py` đạt chuẩn 0 rò rỉ máy, 15/15 scripts ngân sách.
3. [x] **Nghiệm thu vận hành:** 15/15 cổng pháp điển `validate_legal_spoke.py` đạt **PASSED 100%**.

---

## 🚫 Ngoài Phạm Vi (Out of scope)
- **Tái cấu trúc bộ mã hóa RSA 2048 Registry:** Giữ nguyên cơ chế bảo mật của `decrypt_spoke_registry.py` và `spoke_registry.yaml`.
- **Thay đổi định dạng schema của `workspace_context.yaml`:** Giữ nguyên các trường hiện hữu (`project`, `hub_packages`, `must_read`) để bảo toàn tính tương thích ngược 100%.
