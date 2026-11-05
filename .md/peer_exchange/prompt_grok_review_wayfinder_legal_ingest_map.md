---
request_id: "req-20261105-review-wayfinder-legal-ingest-map-001"
from_agent: "antigravity"
to_agent: "grok"
request_type: "review"
profile: "audit_plan"
subject: "Stage 1 Wayfinder Map Audit: Gia cố toàn trình Pipeline /ccba-legal-ingest & Đồng bộ Sổ bộ 106 Bundles (T-01..T-04)"
timestamp: "2026-11-05T16:58:00+07:00"
source_documents:
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/map.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/01_decrees_registry_and_subgate_53_sync.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/02_index_metadata_codegen_and_gate2_link_check.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/03_unified_ingest_dual_pdf_and_offline_meta.md
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/04_nightly_telemetry_and_provenance_queue_sync.md
output_path: ".md/peer_exchange/grok_review_wayfinder_legal_ingest_map.md"
target_files:
  - /home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/map.md
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py
  - /home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py
  - /home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py
  - /home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py
---

# 🎯 Yêu cầu Thẩm định Wayfinder Map (Stage 1 Plan Audit): Gia cố Pipeline `/ccba-legal-ingest` & Đồng bộ Sổ bộ 106 Bundles

> **Chỉ mục dòng (`line ranges`) chính xác để tiết kiệm lượt đọc (`read_file`) cho Grok**:
> 1. **Wayfinder Map & 4 Tickets:**
>    - Map chính: `/home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/map.md` (dòng `1–88`)
>    - Ticket T-01: `/home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/01_decrees_registry_and_subgate_53_sync.md` (dòng `1–54`)
>    - Ticket T-02: `/home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/02_index_metadata_codegen_and_gate2_link_check.md` (dòng `1–53`)
>    - Ticket T-03: `/home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/03_unified_ingest_dual_pdf_and_offline_meta.md` (dòng `1–50`)
>    - Ticket T-04: `/home/vvc/ccba/ccba-legal-knowledge/.md/wayfinder/legal-ingest-hardening/tickets/04_nightly_telemetry_and_provenance_queue_sync.md` (dòng `1–46`)
> 2. **Mã nguồn hiện tại liên quan tới 4 Tickets:**
>    - `/home/vvc/ccba/ccba-legal-knowledge/legal_registry.yaml`: dòng `1–15` (`summary: total_documents: 87`), dòng `1394–1420` (khối `decrees:` gồm 19 văn bản).
>    - `/home/vvc/ccba/ccba-legal-knowledge/scripts/spoke_cli.py`: dòng `85–108` (`get_spoke_stats`), dòng `180–205` & `290–305` (`audit_provenance`), dòng `770–910` & `1005–1025` (`ingest` chỉ đọc `laws` + `standards`).
>    - `/home/vvc/ccba/ccba-legal-knowledge/scripts/validate_legal_spoke.py`: dòng `310–320` (Gate 2 `index.md` check), dòng `610–650` (Sub-Gate 5.3 `_validate_legal_validity_and_in_force` chỉ lặp `for sec in ["laws", "standards"]:`).
>    - `/home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/vbpl_admin.py`: dòng `226–270` (`_write_bundle_metadata_and_index` hardcode `"Chính phủ"` tại dòng `253`, link PDF `./{Path(pdf_path).name}` tại dòng `255`, link `./templates/` tại dòng `265`).
>    - `/home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/cli.py`: dòng `858–945` (`handle_ingest` chứa logic ADR 0043 Dual-PDF `pdf_tier == 3` chưa được đưa vào `spoke_cli.py:ingest`).
>    - `/home/vvc/ccba/ccba-agent-platform/scripts/ccba_platform_cli.py`: dòng `525–555` (`execute_ingest_legal` offline mode gán cứng `"title": f"Document {slug}"` và `"status": "effective"`).
>    - `/home/vvc/ccba/ccba-legal-knowledge/.md/tools/run_nightly_telemetry.py`: dòng `150–165` (gán cứng `ci_status = "✅ PASSED (0 Errors, 0 Warnings)"`).

---

## Tóm tắt Bối cảnh & Yêu cầu Phản biện

Sau khi khảo sát đối kháng 2 vòng (Double-Pass Adversarial Review) trên lịch sử vận hành `/ccba-legal-ingest` (106 bundles thực tế trên đĩa, 53 bài học lịch sử, 43 PRs tại Spoke và >570 PRs tại Hub), chúng tôi đã lập **Wayfinder Map** chia thành 4 Tickets (`T-01` đến `T-04`) và 3 mục Sương mù (`Fog-01` đến `Fog-03`):

1. **`T-01` (P0):** Đưa khối `decrees:` (19 văn bản) vào luồng đếm/cập nhật của `spoke_cli.py`, `sync_expansion_roadmap.py`, `verify_all_docs_against_pdf.py` và lưới kiểm định hiệu lực pháp lý Sub-Gate 5.3 (`validate_legal_spoke.py`), đồng bộ `summary` từ `87` lên đúng `106` văn bản.
2. **`T-02` (P1):** Sửa `_write_bundle_metadata_and_index` trong `vbpl_admin.py` (bảo toàn `metadata.yaml`, lấy đúng `issued_by`, sửa link `./sources/<slug>.pdf`, ẩn `./templates/` khi `templates_cnt == 0`), vá 11 file `index.md` ghi nhầm `"Chính phủ"` và 27 file `index.md` đứt link trên Spoke, đồng thời bổ sung kiểm tra liên kết cục bộ `index.md` vào Gate 2 / Gate 4.
3. **`T-03` (P1):** Hợp nhất logic **ADR 0043 Dual-PDF** (`pdf_tier == 3` $\to$ `_raw_scan.pdf` + `convert_to_pdf` + `pdf_origin: docx_vector_rendered`) và `attachments` vào `spoke_cli.py:ingest`, đồng thời tự động bóc tách `doc_meta` từ DOCX khi chạy `--docx` offline trong `ccba_platform_cli.py:execute_ingest_legal`.
4. **`T-04` (P2):** Sửa `run_nightly_telemetry.py` parse đúng số `Errors`/`Warnings` thực tế và sửa tiêu đề cứng `"38 Văn Bản"` trong `spoke_cli.py:audit_provenance`, làm mới `provenance_migration_queue.md` đủ 106 văn bản.

Đề nghị Grok kiểm tra chéo với mã nguồn thực tế và cho biết:
1. Cấu trúc Wayfinder Map (`Destination`, `Decisions so far`, `Frontier Tickets`, `Not yet specified`, `Out of scope`) và sự phân rã `T-01..T-04` đã chặt chẽ, đúng chuẩn KISS & Reuse-First (ADR-0061) chưa?
2. Có rủi ro hồi quy (regression) hay edge case nào bị bỏ sót khi kích hoạt Sub-Gate 5.3 cho 19 văn bản `decrees:` (`T-01`), khi kiểm tra link `index.md` tại Gate 2 (`T-02` — lưu ý trên CI runner các tệp `.pdf` trong `sources/` được `.gitignore` theo ADR 0035), hoặc khi gọi `convert_to_pdf` trong `T-03` không?
