# Ticket 04: Chuẩn hóa Báo cáo Nightly Telemetry & Hàng đợi Provenance 106 Bundles

- **Type:** Task (AFK / Code Implementation)
- **Priority:** P2 (Trung bình)
- **Status:** closed
- **Assignee:** Antigravity AI
- **Target Seams & Files:**
  - [run_nightly_telemetry.py](file:///home/vvc/ccba/ccba-legal-knowledge/.md/tools/run_nightly_telemetry.py#L150-L168)
  - [spoke_cli.py](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L297) (`audit_provenance`)
  - [provenance_migration_queue.md](file:///home/vvc/ccba/ccba-legal-knowledge/.md/knowledge/provenance_migration_queue.md)
  - [legal_registry.yaml](file:///home/vvc/ccba/ccba-legal-knowledge/.md/data/legal_registry.yaml)
- **Reference:** [Wayfinder Map: Gia Cố Toàn Trình Pipeline `/ccba-legal-ingest`](../map.md), Grok Audit `C2`, `C7`, `C8`

---

## ❓ Câu Hỏi / Vấn Đề Cốt Lõi Cần Giải Quyết
Làm thế nào để [`run_nightly_telemetry.py`](file:///home/vvc/ccba/ccba-legal-knowledge/.md/tools/run_nightly_telemetry.py#L157) trích xuất đúng số `Errors` / `Warnings` thực tế trên cả `exit 0` và `exit != 0` (giữ nguyên Tầng 1 Golden Cohort 11 bundles, Tầng 2 đọc `registry_summary` 106 bundles) và [`spoke_cli.py:audit_provenance`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L297) xuất báo cáo [`provenance_migration_queue.md`](file:///home/vvc/ccba/ccba-legal-knowledge/.md/knowledge/provenance_migration_queue.md) chuẩn xác trên toàn bộ **106 bundles** sau khi [T-01: Đồng bộ Sổ bộ Khối decrees & Mở rộng Sub-Gate 5.3](01_decrees_registry_and_subgate_53_sync.md) hoàn tất?

---

## 🎯 Mục Tiêu Thực Thi (KISS Implementation Scope — Tuân thủ Grok `C2`, `C7`, `C8`)
1. **Parse trung thực `Errors` và `Warnings` trên cả `exit 0` và `exit != 0` trong [`run_nightly_telemetry.py`](file:///home/vvc/ccba/ccba-legal-knowledge/.md/tools/run_nightly_telemetry.py#L150-L168) (`C7`):**
   - Dùng Regex `r"SUMMARY REPORT:\s*Errors:\s*(\d+)\s*\|\s*Warnings:\s*(\d+)"` trên `out_ci` (đã gộp `stdout + stderr`, khớp với [`validate_legal_spoke.py:2019`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py#L2019)) cho **cả hai nhánh** `code_ci == 0` (`✅ PASSED ({errs} Errors, {warns} Warnings)`) và `code_ci != 0` (`❌ FAILED (Exit {code_ci}: {errs} Errors, {warns} Warnings)`).
   - **Bảo toàn ngữ nghĩa 2 tầng (`C7`):** Giữ nguyên Tầng 1 (`verify_ground_truth_parity.py`) kiểm định trên tập Golden Cohort mặc định (11 bundles), trong khi Tầng 2 hiển thị tổng quy mô Spoke `106 bundles` đọc từ `registry_summary.total_documents` sau khi `T-01` hoàn tất.
2. **Sửa tiêu đề cứng và làm mới Hàng đợi Provenance trong [`spoke_cli.py:audit_provenance`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L297) (`C2`, `C7`, `C8`):**
   - Thay chuỗi cứng `"## 2. Danh Sách Chi Tiết Hàng Đợi 38 Văn Bản"` tại `spoke_cli.py:297` bằng f-string động `f"## 2. Danh Sách Chi Tiết Hàng Đợi {len(records)} Văn Bản"`.
   - Chạy lệnh `python scripts/spoke_cli.py audit-provenance` (**tuyệt đối không** kèm cờ `--attest-group-a` theo `C7`) để cập nhật [provenance_migration_queue.md](file:///home/vvc/ccba/ccba-legal-knowledge/.md/knowledge/provenance_migration_queue.md) lên đúng **106 văn bản**.
   - Đồng bộ bản sao `.md/data/legal_registry.yaml` (nếu tồn tại cục bộ) khớp 100% với `legal_registry.yaml` gốc và bổ sung kiểm tra parity khi tồn tại tệp bản sao này (`C8`).

---

## 🧪 Tiêu Chí Hoàn Thành (Acceptance Criteria)
- [x] `run_nightly_telemetry.py` hiển thị chính xác số lượng `Errors` và `Warnings` từ `SUMMARY REPORT` trên cả trường hợp `exit 0` lẫn `exit != 0`; Tầng 1 giữ nguyên Golden Cohort (11 bundles) và Tầng 2 hiển thị đúng `106 bundles`.
- [x] [provenance_migration_queue.md](file:///home/vvc/ccba/ccba-legal-knowledge/.md/knowledge/provenance_migration_queue.md) được làm mới qua `python scripts/spoke_cli.py audit-provenance` (không có `--attest-group-a`), hiển thị đúng 106 văn bản và không còn tiêu đề cứng `"38 Văn Bản"`.
- [x] `python scripts/validate_legal_spoke.py --skip-pdf-vault` đạt 100% PASS.
