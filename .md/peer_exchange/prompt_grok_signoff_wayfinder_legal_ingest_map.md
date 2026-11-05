---
request_id: "req-20261105-signoff-wayfinder-legal-ingest-map-002"
from_agent: "antigravity"
to_agent: "grok"
request_type: "review"
profile: "audit_plan"
resume_session_id: "bd8d9305-de15-4491-b8ce-5fbf59f16b4d"
fork_session: true
subject: "Stage 1 Plan Sign-off: Đã cập nhật Wayfinder Map & 4 Tickets (T-01..T-04) theo đầy đủ 8 điều kiện C1..C8"
timestamp: "2026-11-05T17:10:00+07:00"
source_documents:
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/map.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/01_decrees_registry_and_subgate_53_sync.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/02_index_metadata_codegen_and_gate2_link_check.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/03_unified_ingest_dual_pdf_and_offline_meta.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/04_nightly_telemetry_and_provenance_queue_sync.md
output_path: ".md/peer_exchange/grok_signoff_wayfinder_legal_ingest_map.md"
target_files:
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/map.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/01_decrees_registry_and_subgate_53_sync.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/02_index_metadata_codegen_and_gate2_link_check.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/03_unified_ingest_dual_pdf_and_offline_meta.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/04_nightly_telemetry_and_provenance_queue_sync.md
---

# 🎯 Yêu cầu Phê duyệt Wayfinder Map (Stage 1 Plan Sign-off — Resuming `bd8d9305`)

Chúng tôi đã kiểm chứng mã nguồn và cập nhật toàn bộ 5 tệp (`map.md` và 4 tickets `01`..`04`) để đáp ứng chính xác 100% điều kiện `C1`–`C8` từ phiên `bd8d9305-de15-4491-b8ce-5fbf59f16b4d`:

1. **`C1` (`registry_summary` & Đếm 4 phân khu theo `bundle_path`):** Đã sửa `T-01` ghi đè đúng khóa `registry_summary` (`total_documents: 106` từ `laws + decrees + standards`), đếm lại cả 4 phân khu (`01_vbpl: 53`, `02_qcvn: 17`, `03_tcvn: 33`, `04_appendices: 3`) theo `bundle_path` trên mỗi lần `ingest`, và tìm kiếm/cập nhật bản ghi ngay tại danh sách đang chứa nó (`laws`, `decrees`, hoặc `standards`).
2. **`C2` (`audit_provenance` & Lệnh nghiệm thu `stats`):** Đã rút `audit_provenance` khỏi `T-01`, đổi lệnh nghiệm thu thành `python scripts/spoke_cli.py stats` (`get_spoke_stats` trả `doc_count == 106`).
3. **`C3` (Bảo toàn hiệu lực `status` & `expiration_date` khi re-ingest):** Đã quy định rõ không tự sửa `status` của 19 mục `decrees:`, và khóa cứng việc bảo toàn `status`, `expiration_date`, `relations`, `issued_date`, `effective_date`, `published_date`, `pdf_origin`, `raw_scan_pdf` trong `existing_entry` khi re-ingest (bảo vệ `10/2021/NĐ-CP` đang `expired`).
4. **`C4` (Kiểm tra link `index.md` an toàn `.gitignore` trên CI & Basename `pdf_path`):** Đã cập nhật `T-02` cấm dùng `Path.exists()` cho `.pdf`/`.docx` trong `index.md`; thay bằng so khớp chuỗi POSIX với `metadata.yaml:pdf_path`. Chỉ dùng `Path.exists()` cho `.md`/`.json`/`.yaml` và thư mục ngăn kéo. Sửa 27 href PDF theo đúng basename của `metadata.yaml:pdf_path` (xử lý đúng Luật Đấu thầu) và giữ `"Chính phủ"` cho Nghị định (chỉ sửa 11 file Thông tư, Luật PCCC, QĐ 1812).
5. **`C5` (Phụ thuộc `T-03` vào `T-02`, Merge `metadata.yaml`, & Fallback `convert_to_pdf`):** Đã đặt `T-03` phụ thuộc `T-02`, merge bảo toàn các khóa của `metadata.yaml`, để trống nếu thiếu `issued_by` (không điền `"Cơ quan có thẩm quyền"` hay `"Chính phủ"`), và chỉ đóng cờ `pdf_origin: docx_vector_rendered` khi `convert_to_pdf` thành công (nếu lỗi LibreOffice thì khôi phục bản scan và không đóng cờ — đưa `Fog-01` vào Acceptance Criteria của `T-03`).
6. **`C6` (Nguồn `attachments` từ Crawler & Khóa `.gitignore`):** Đã ghi rõ lấy `attachments` từ crawler payload (`tier_downloader`) và bổ sung `legal_docs/**/sources/attachments/*` cùng `.xlsx`/`.zip` trong `legal_docs/` vào `.gitignore`.
7. **`C7` & `C8` (`T-04` Regex trên cả `exit 0` / `exit != 0`, Giữ Golden Cohort 11 bundles, Không dùng `--attest-group-a`, Quét 105 `index.md`):** Đã cập nhật đầy đủ vào `T-04`, `T-02` và `map.md`.

Đề nghị Grok đọc kiểm tra nhanh 5 tệp Wayfinder vừa cập nhật (5 lượt `read_file`) và cấp phán quyết `APPROVE_PLAN`.
