# Ticket 01: Đồng bộ Sổ bộ Khối `decrees:` & Mở rộng Sub-Gate 5.3

- **Type:** Task (AFK / Code Implementation)
- **Priority:** P0 (Khẩn cấp)
- **Status:** closed (completed — 106/106 bundles synced & Sub-Gate 5.3 active on decrees)
- **Assignee:** Antigravity AI
- **Target Seams & Files:**
  - [spoke_cli.py](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L85-L115) (`get_spoke_stats`) & [spoke_cli.py](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L880-L1025) (`ingest`)
  - [validate_legal_spoke.py](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py#L615) (`_validate_legal_validity_and_in_force` — Sub-Gate 5.3)
  - [verify_all_docs_against_pdf.py](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/verify_all_docs_against_pdf.py#L253)
  - [legal_registry.yaml](file:///home/vvc/ccba/ccba-legal-knowledge/legal_registry.yaml#L4-L10) (`registry_summary`)
- **Reference:** [Wayfinder Map: Gia Cố Toàn Trình Pipeline `/ccba-legal-ingest`](../map.md), Grok Audit `C1`, `C2`, `C3`, `C8`

---

## ❓ Câu Hỏi / Vấn Đề Cốt Lõi Cần Giải Quyết
Làm thế nào để đưa toàn bộ **19 văn bản** trong khóa `decrees:` của [legal_registry.yaml](file:///home/vvc/ccba/ccba-legal-knowledge/legal_registry.yaml) vào luồng đếm (`get_spoke_stats`), cập nhật tại chỗ bảo toàn hiệu lực (`spoke_cli.py:ingest`) và lưới kiểm định hiệu lực pháp lý Sub-Gate 5.3 ([`validate_legal_spoke.py`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py#L615)), đồng thời cập nhật đúng khóa `registry_summary` (`total_documents: 106` và đếm 4 phân khu theo `bundle_path`)?

---

## 🎯 Mục Tiêu Thực Thi (KISS Implementation Scope — Tuân thủ Grok `C1`–`C3`, `C8`)
1. **Cập nhật đúng khóa `registry_summary` và đếm phân khu theo `bundle_path` (`C1`):**
   - Trong [`spoke_cli.py:ingest`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L1011-L1020) và [legal_registry.yaml](file:///home/vvc/ccba/ccba-legal-knowledge/legal_registry.yaml#L4-L10): Ghi đè đúng khóa `registry_summary` (tuyệt đối không tạo khóa `summary` mới).
   - Tính `total_documents = len(laws_list) + len(decrees_list) + len(standards_list)` (`51 + 19 + 36 = 106`).
   - Đếm lại cả 4 phân khu (`01_vbpl`, `02_qcvn`, `03_tcvn`, `04_appendices`) trên mỗi lần chạy `ingest` bằng cách kiểm tra `f"/{cat}/" in item.get("bundle_path", "")` trên tổng hợp `laws_list + decrees_list + standards_list` (`01_vbpl: 53`, `02_qcvn: 17`, `03_tcvn: 33`, `04_appendices: 3`). Tuyệt đối cấm gán `01_vbpl = len(laws) + len(decrees)` (`= 70`).
   - *Lưu ý (`C8`):* [`sync_expansion_roadmap.py:153`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/sync_expansion_roadmap.py#L153) đã đọc trực tiếp `registry_summary.total_documents`, không cần cộng thêm bộ đếm list thứ hai tại đó.
2. **Mở rộng `get_spoke_stats` và tìm kiếm trên cả 3 danh sách khi `ingest` (`C1`, `C2`, `C3`):**
   - Trong [`spoke_cli.py:get_spoke_stats`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L90-L103): Nạp đủ `laws`, `decrees`, `standards` để trả về `doc_count = 106`. (Không chạm vào `audit_provenance` vì hàm đó đã quét đĩa qua `scan_all_bundles_provenance`).
   - Trong [`spoke_cli.py:ingest`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py#L886-L1009): Tìm kiếm bản ghi hiện hữu trên cả 3 danh sách `("laws", "decrees", "standards")` và cập nhật ngay tại danh sách đang chứa nó (`matched_section_key[existing_idx]`). Chỉ khi là văn bản hoàn toàn mới mới append vào `section_key` mặc định.
   - **Bảo toàn trường hiệu lực khi re-ingest (`C3`):** Khi cập nhật `existing_entry`, bắt buộc bảo toàn `status`, `expiration_date`, `relations`, `issued_date`, `effective_date`, `published_date`, `pdf_origin`, `raw_scan_pdf` nếu payload đầu vào (`raw_meta`) không cung cấp tường minh hoặc chỉ có giá trị mặc định (ngăn chặn việc ghi đè `status: expired` của `10/2021/NĐ-CP` thành `active`).
3. **Mở rộng Sub-Gate 5.3 và `verify_all_docs_against_pdf.py` (`C3`):**
   - Chạy kiểm tra trước trên 19 mục `decrees:` (cả 19 mục đều đang `status: active` hợp lệ, cấm tự ý sửa `status` để làm xanh cổng).
   - Cập nhật vòng lặp tại [`validate_legal_spoke.py:615`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py#L615) từ `for sec in ["laws", "standards"]:` thành `for sec in ["laws", "decrees", "standards"]:`.
   - Cập nhật [`verify_all_docs_against_pdf.py:253`](file:///home/vvc/ccba/ccba-legal-knowledge/scripts/verify_all_docs_against_pdf.py#L253) thành `reg.get("laws", []) + reg.get("decrees", []) + reg.get("standards", [])`.

---

## 🧪 Tiêu Chí Hoàn Thành (Acceptance Criteria)
- [x] `python scripts/spoke_cli.py stats` hiển thị `Total Legal Documents : 106` (`get_spoke_stats` trả về `doc_count == 106` — theo Grok `N2`).
- [x] Khóa `registry_summary` trong `legal_registry.yaml` đạt `total_documents: 106` và `categories: {01_vbpl: 53, 02_qcvn: 17, 03_tcvn: 33, 04_appendices: 3}`.
- [x] Sub-Gate 5.3 trong `python scripts/validate_legal_spoke.py --skip-pdf-vault` kiểm định đủ 106 văn bản (`laws`, `decrees`, `standards`) và đạt `0 Errors`.
- [x] Khi chạy cập nhật một văn bản đã có (thuộc `decrees:` hoặc văn bản `expired` như `10/2021/NĐ-CP`), `spoke_cli.py ingest` cập nhật đúng tại danh sách chứa nó và bảo toàn nguyên vẹn `status`, `expiration_date`, `relations`, `pdf_origin`, `raw_scan_pdf`.
- [x] `python .agents/skills/ccba-verify-legal-ingest/harness/verify_legal_ingest_harness.py` đạt 100% PASS.
