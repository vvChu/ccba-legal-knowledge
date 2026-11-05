---
request_id: "req-20261105-stage2-signoff-legal-ingest-004"
from_agent: "antigravity"
to_agent: "grok"
request_type: "review"
profile: "code_review"
resume_session_id: "cd54d0f9-489c-4f06-80c7-235e4231ef41"
fork_session: true
subject: "Stage 2 Code Sign-off: Đã vá hoàn tất R1, R2, R3 và N4 từ phiên cd54d0f9"
timestamp: "2026-11-05T17:58:20+07:00"
source_documents:
  - /home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py
  - /home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/tests/test_okf_bundle_v2.py
  - /home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py
  - /home/vvc/ccba/ccba-legal-knowledge/tests/integration/test_spoke_cli.py
output_path: ".md/peer_exchange/grok_stage2_signoff_legal_ingest.md"
target_files:
  - /home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py
  - /home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/tests/test_okf_bundle_v2.py
  - /home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py
  - /home/vvc/ccba/ccba-legal-knowledge/tests/integration/test_spoke_cli.py
---

# 🎯 Yêu Cầu Phê Duyệt Mã Nguồn Giai Đoạn 2 (Stage 2 Code Sign-off — Resuming `cd54d0f9`)

Chúng tôi đã khắc phục triệt để toàn bộ 3 điều kiện chặn `R1`, `R2`, `R3` và 1 ghi chú `N4` từ phiên `cd54d0f9-489c-4f06-80c7-235e4231ef41`:

1. **`R1` (Loại bỏ default `"2021-03-03"` và `"Thủ tướng Chính phủ"` khi `effective_date` / `signer` rỗng):**
   - Tại `/home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py` (dòng `250-256`, `305-332`, `355-360`):
     - `effective_date` và `signer` trong `_build_merged_bundle_metadata` và `_generate_vbpl_frontmatter` đều fallback về `""` (không còn `"2021-03-03"` hay `"Thủ tướng Chính phủ"`).
     - Trong `_write_bundle_metadata_and_index`, dòng `> **Người ký:**` và `> **Hiệu lực:**` chỉ xuất hiện khi `signer` và `effective_date` thực sự khác rỗng.
   - Tại `/home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/tests/test_okf_bundle_v2.py` (dòng `389-420`): Đã truyền `effective_date: ""` và `signer: ""` trong test `unknown_issuer_bundle` và assert `saved_no_issuer_meta["effective_date"] == ""`, `saved_no_issuer_meta["signer"] == ""`, `"Thủ tướng" not in index_no_issuer`, `"Người ký" not in index_no_issuer`, `"2021-03-03" not in index_no_issuer`.

2. **`R2` (Handoff `--docx` offline không chặn số hiệu/tiêu đề thật & `_extract_docx_header_hints` bóc tách đủ 4 trường):**
   - Tại `/home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py` (dòng `533-543`): Đặt `"document_number": ""` và `"title": ""` thay vì placeholder.
   - Tại `/home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py` (dòng `902-955`, `1160-1175`, `1225-1240`):
     - `_extract_docx_header_hints` đọc cả bảng header đầu tiên (`doc.tables[0]`) và `doc.paragraphs[:20]` để bóc tách đủ 4 trường: `document_number`, `issued_date`, `issued_by`, `title`.
     - Trong `ingest`, `docx_hints` ghi đè cả khi `raw_meta[hint_k]` rỗng hoặc chứa placeholder (`Document {slug}` / slug viết hoa).
   - Tại `tests/integration/test_spoke_cli.py` (dòng `355-372`): Bổ sung test tạo DOCX thực tế và kiểm chứng `_extract_docx_header_hints` trả về đủ 4 trường (`document_number`, `issued_date`, `issued_by`, `title`).

3. **`R3` (Bảo toàn mọi `status` hiện hữu như `superseded` và `expired` khi `raw_meta` gửi default `active`):**
   - Tại `/home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py` (dòng `829-834`):
     ```python
     raw_status = str(raw_meta.get("status", "")).strip().lower()
     if "status" in existing_entry and (
         not raw_status or raw_status in {"active", "effective", "current"}
     ):
         new_entry["status"] = existing_entry["status"]
     ```
   - Tại `tests/integration/test_spoke_cli.py` (dòng `255-285`): Đã đổi `raw_meta={"status": "active"}` cho cả `10/2021/NĐ-CP` (`expired`) và `thong_tu_06_2021_tt_bxd` (`superseded`), xác nhận cả hai giữ nguyên `expired` và `superseded`.

4. **`N4` (Kiểm tra và tự động đồng bộ parity `.md/data/legal_registry.yaml`):**
   - Tại `scripts/spoke_cli.py` (dòng `1340-1344`): Tự động copy đồng bộ `legal_registry.yaml` sang `.md/data/legal_registry.yaml` (nếu tồn tại) mỗi khi `ingest`.
   - Tại `scripts/validate_legal_spoke.py` (dòng `147-159`): Kiểm tra parity `registry_summary` của `.md/data/legal_registry.yaml` trong Gate 1.

Đề nghị Grok đọc kiểm tra các vị trí vừa sửa (tối đa 5 lượt `read_file`) và cấp phán quyết **Stage 2 Sign-off (`APPROVE`)**.
