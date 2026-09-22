# Ticket 02: Constitution Upstream & Smart Multiline Merge

- **Type:** Task (AFK / Code Implementation)
- **Status:** closed (completed on Hub — Commit 30a2d6c0)
- **Assignee:** Antigravity AI
- **Target Seams:**
  - `AGENTS.md` (Hub root)
  - `.agents/AGENTS.md` (Hub core)
  - `scripts/spoke/sync/coordinator.py`
  - `scripts/tests/test_spoke_synchronizer.py`
  - `tests/test_spoke_synchronizer.py`
- **Reference:** HUB-ADR-0044, [learning_proposal.md](file:///home/vvc/.gemini/antigravity/brain/bbe6a22c-2adb-4dc2-a026-1c5cab5eb69d/learning_proposal.md)

---

## 🎯 Mục Tiêu
1. **Upstream 2 điều khoản Hiến pháp:**
   Bổ sung 2 nguyên tắc bất biến vào mục `## Core Invariants` của cả `AGENTS.md` và `.agents/AGENTS.md` trên Hub:
   - `Single-User Multi-Device & Machine-State Decoupling`
   - `Remote Mutation Idempotency & State Inspection Gate`
2. **Nâng cấp bộ hợp nhất Hiến pháp thông minh (Smart Multiline Merge):**
   - Refactor hàm `merge_agents_constitution()` trong `scripts/spoke/sync/coordinator.py`.
   - Sử dụng Universal Regex `r"^[ \t]*(?:[-*]|\d+\.)[ \t]+\*\*([^*:]+)(?::\*\*|\*\*:)[\t ]*(.*)"` nhận diện mọi dạng bullet, numbered list và dấu hai chấm.
   - Thuật toán hợp nhất:
     1. Kế thừa 100% Invariants từ Hub (Hub là SSoT cho Layer 1).
     2. Giữ lại và nối tiếp các Invariants cục bộ độc thù của Spoke (nếu Spoke có các bullet keys mà Hub chưa có).
     3. Giữ nguyên các custom sections `## ` khác ở cuối file.
     4. Bảo đảm tính lũy kế (idempotency): `merge(hub, merge(hub, spoke)) == merge(hub, spoke)`.

---

## 🧪 Tiêu Chí Hoàn Thành (Acceptance Criteria)
- [x] Cả 2 file `AGENTS.md` trên Hub đều có đủ 2 điều khoản mới.
- [x] Khi chạy `python scripts/sync_spoke.py --spoke <spoke> --apply`, Spoke không bao giờ bị mất các điều khoản riêng dưới mục `## Core Invariants`.
- [x] Các nested bullet points hoặc mô tả nhiều dòng trong Invariant không bị cắt xén hay định dạng sai.
- [x] Toàn bộ 20 tests trong `tests/test_spoke_synchronizer.py` và `scripts/tests/test_spoke_synchronizer.py` đạt 100% PASS.
