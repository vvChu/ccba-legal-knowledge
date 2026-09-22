# Ticket 01: Core Package & Path Resilience Engine

- **Type:** Task (AFK / Code Implementation)
- **Status:** closed (completed on Hub — Commit 30a2d6c0)
- **Assignee:** Antigravity AI
- **Target Seams:**
  - `packages/ccba-legal-intel/pyproject.toml`
  - `scripts/spoke/spoke_adopter.py`
  - `scripts/adopt_spoke.py`
  - `scripts/ccba_platform_cli.py`
  - `scripts/spoke/sync/discovery.py`
  - `scripts/spoke/spoke_bootstrap.py`
  - `scripts/sync_hub_adr_matrix.py`
- **Reference:** HUB-ADR-0044, HUB-ADR-0045, [learning_proposal.md](file:///home/vvc/.gemini/antigravity/brain/bbe6a22c-2adb-4dc2-a026-1c5cab5eb69d/learning_proposal.md)

---

## 🎯 Mục Tiêu
1. **Khử blocker dependency:** Bổ sung `"pymupdf>=1.23.0"` vào `dependencies` của `packages/ccba-legal-intel/pyproject.toml` để đảm bảo `pip install -e` không bao giờ gặp lỗi thiếu thư viện `fitz`.
2. **Hard Fail-Safe Gate cho `adopt`:**
   - Mở rộng phương thức `adopt(self, dry_run=False, force=False)` và `adopt_project(..., force=False)`.
   - Chặn đứng thực thi khi `report.has_workspace_context and not force`, in hướng dẫn rõ ràng chuyển sang `bootstrap-spoke`.
   - Bổ sung flag `--force` và `--dry-run` vào CLI parser của `scripts/adopt_spoke.py` và `scripts/ccba_platform_cli.py`.
3. **Chuẩn hóa đường dẫn tương đối (POSIX Sibling):**
   - `spoke_adopter.py`: Tính `os.path.relpath(hub_path, spoke_base)` dạng POSIX (`../ccba-agent-platform`) khi lưu `workspace_context.yaml`. Xử lý an toàn khi khác ổ đĩa Windows (`ValueError` fallback thành `None`).
   - `discovery.py`: Cấm auto-save bẩn Git khi tìm thấy Hub qua `CCBA_HUB_PATH`; thêm `sort_keys=False` khi lưu YAML.
   - `spoke_bootstrap.py` & `sync_hub_adr_matrix.py`: Chuẩn hóa resolve relative path dựa trên thư mục gốc Spoke (`self.spoke_root` / `root_dir`) và hỗ trợ cấu trúc `dict` đa OS an toàn.

---

## 🧪 Tiêu Chí Hoàn Thành (Acceptance Criteria)
- [x] `packages/ccba-legal-intel/pyproject.toml` có `pymupdf>=1.23.0`.
- [x] Chạy `python scripts/adopt_spoke.py --spoke <registered_spoke>` mà không có `--force` sẽ lập tức exit với code 1 và in hướng dẫn bảo vệ.
- [x] Chạy với `--force` cho phép tiếp tục ghi đè nếu người dùng thực sự muốn.
- [x] Không có đường dẫn tuyệt đối Windows `D:\...` hay POSIX `/home/...` nào được ghi vào `workspace_context.yaml`.
- [x] Toàn bộ unit tests liên quan tại `tests/test_spoke_adopter.py` (bao gồm test cross-drive `ValueError`) và `tests/test_delivery_spoke_setup.py` đạt 100% PASS (11/11).
