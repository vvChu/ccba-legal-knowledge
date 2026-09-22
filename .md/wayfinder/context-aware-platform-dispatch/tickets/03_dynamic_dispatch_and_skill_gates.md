# Ticket 03: Dynamic Dispatch Matrix & Skill Fail-Safe Gates

- **Type:** Task (AFK / Skill & Documentation Refactor)
- **Status:** closed (completed on Hub — Commit 30a2d6c0, 6d1c7b4f)
- **Assignee:** Antigravity AI
- **Target Seams:**
  - `.agents/skills/ccba-platform/SKILL.md` (Hub & Spoke)
  - `.agents/skills/ccba-init-spoke/SKILL.md` (Hub & Spoke)
- **Reference:** [learning_proposal.md](file:///home/vvc/.gemini/antigravity/brain/bbe6a22c-2adb-4dc2-a026-1c5cab5eb69d/learning_proposal.md), [map.md](../map.md)

---

## 🎯 Mục Tiêu
1. **Phân Luồng Menu Động Theo 5 Bối Cảnh trong `/ccba-platform`:**
   - Tái cấu trúc Pha 1.3 và Bảng Ma Trận Điều Phối:
     - **Bối cảnh 1 (Hub Monorepo):** Ẩn các lệnh tạo/adopt Spoke.
     - **Bối cảnh 2 (Greenfield Spoke):** Chỉ hiển thị duy nhất `/ccba-init-spoke`.
     - **Bối cảnh 3 (Brownfield Spoke):** Chỉ hiển thị duy nhất `/ccba-spoke-adopter`.
     - **Bối cảnh 4 (Multi-Device Cloned Spoke):** Ẩn hoàn toàn `/ccba-init-spoke` và `/ccba-spoke-adopter`; hiển thị lệnh `bootstrap-spoke` làm ưu tiên hàng đầu.
     - **Bối cảnh 5 (Healthy Ready Spoke):** Ẩn các lệnh onboarding; lọc và hiển thị kỹ năng nghiệp vụ theo Archetype.
   - Sửa đổi cú pháp lệnh CLI: Không dùng `python3 scripts/ccba_platform_cli.py` khi đứng tại Spoke mà dùng `python3 "$CCBA_HUB_PATH/scripts/ccba_platform_cli.py"`.
   - Dọn sạch các tàn dư tài liệu số thứ tự cũ (`1-21`) và cấu hình hardcoded path `windows: D:\...`.
2. **Hard Refusal Gate cho `/ccba-init-spoke`:**
   - Viết lại Bước 0 trong `ccba-init-spoke/SKILL.md`: Nếu phát hiện `.md/workspace_context.yaml` đã tồn tại, Agent **BẮT BUỘC DỪNG LẠI**, tuyệt đối không gợi ý hay chuyển sang chạy `/ccba-spoke-adopter`.

---

## 🧪 Tiêu Chí Hoàn Thành (Acceptance Criteria)
- [x] Bảng Ma trận trong `ccba-platform/SKILL.md` được thay thế bằng Ma trận điều phối động 5 bối cảnh.
- [x] Không còn bất kỳ chỉ dẫn nào gợi ý chạy `init` hoặc `adopter` trên Spoke đã có `workspace_context.yaml`.
- [x] Toàn bộ hướng dẫn gọi CLI từ Spoke đều trỏ chuẩn xác qua `$CCBA_HUB_PATH`.
- [x] Biên dịch lại `catalog.yaml` (74 skills), `skills_docs` và vượt qua `scripts/validate_skills.py --enforce-gpi` (GPI 100% PASS).
