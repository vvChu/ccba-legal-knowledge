# CCBA Legal Knowledge Spoke — Mutation Log

Tài liệu ghi nhận nhật ký đột biến, chuẩn hóa dữ liệu và ban hành quyết định kiến trúc tại Spoke `ccba-legal-knowledge`.

---

## [2026-08-22] [refactor] | 100% OKF v2.2 Pure Normative Body & Atomic Form Templates Across 26 Bundles
- **Phạm vi:** 24 Văn bản quy phạm pháp luật + 2 Quy chuẩn kỹ thuật quốc gia (`legal_docs/01_vbpl/`).
- **Nội dung:**
  - Tách thân văn bản thuần khiết 100% sạch rác layout, chữ ký và mã HTML.
  - Bóc tách hơn 90 Biểu mẫu nguyên tử vào `templates/` và hơn 100 Bảng kỹ thuật vào `tables/`.
  - Thiết lập cây cú pháp AST `clauses.json` và bộ câu hỏi Ground-Truth `qa_benchmark.json`.

## [2026-08-22] [feat] | TVPL VIP Genuine Binary DOCX Crawler Integration
- **Phạm vi:** `scripts/fetch_tvpl_doc.py`, `scripts/download_tvpl_docx.py`.
- **Nội dung:**
  - Tự động hóa kết nối Chrome CDP, giải Cloudflare Turnstile và đăng nhập TVPL VIP.
  - Tải và thay thế tệp Word nhị phân nguyên bản 100% cho Luật Đấu thầu số 22/2023/QH15 (`62,776 bytes`).

## [2026-08-22] [feat] | Upgraded 5 CI Verification Gates & Dynamic Regression Suite
- **Phạm vi:** `scripts/validate_legal_spoke.py`, `scripts/test_converter_regression.py`, `scripts/verify_all_docs_against_pdf.py`.
- **Nội dung:**
  - Bổ sung Scoped Noise Gate quét rác Quốc hiệu, Tiêu ngữ, Nơi nhận và chữ ký hành chính.
  - Xây dựng Dynamic Regression Suite phát hiện tự động 24 gói dữ liệu có file DOCX nguồn.
  - Kiểm toán đối soát mã băm SHA-256 trên 3,590 trang PDF Công báo gốc đạt 100% match.

## [2026-08-22] [feat] | Contextual Auto-Triggering for Core Legal Workflows
- **Phạm vi:** `.agents/workflows/` (`ccba-legal-intel`, `ccba-tvpl-vip-crawler`, `ccba-convert-markdown`, `ccba-update-legal-registry`, `ccba-eval-gate`, `ccba-ai-qc-pccc-audit`).
- **Nội dung:**
  - Thiết lập `disable-model-invocation: false`.
  - Mở rộng mô tả ngữ cảnh song ngữ phong phú để AI Agent tự động kích hoạt workflow khi người dùng yêu cầu tra cứu/nạp luật.

## [2026-08-22] [docs] | Ratified ADR 0023 — 0026 from Socrates Grilling Session
- **Phạm vi:** `docs/adr/`, `CONTEXT.md`.
- **Nội dung:**
  - **ADR 0023:** Full Comprehensive NotebookLM Ingestion Strategy for Ultra Tier (500+ sources capacity).
  - **ADR 0024:** Dual-Track Provenance with Footnote Anchor for Consolidated Legal Norms.
  - **ADR 0025:** Strict Zero-Tolerance Provenance Enactment Gate for Legal Ingestion.
  - **ADR 0026:** Package-Based Downstream Legal Knowledge Distribution via `ccba-legal-intel` SDK.

## [2026-08-26] [feat] | OKF v2.3 Dual-Engine Paradigm & TCVN 2737:2023 Annex F Full Modernization
- **Phạm vi:** `legal_docs/03_tcvn/tcvn_2737_2023/annexes/phu_luc_f_he_so_khi_dong.md`, `formulas/`, `docs/adr/`.
- **Nội dung:**
  - **Hình ảnh Composite:** Hợp nhất 11 sơ đồ hình học đa nhánh thành ảnh đơn nhất căn giữa (`hinh_f_1.png` -> `hinh_f_15.png`).
  - **Bảng tra ma trận:** Khôi phục 16 bảng tra hệ số khí động với đầy đủ các cột và giá trị tải trọng kép `<br>`.
  - **Công thức KaTeX:** Chuyển đổi 100% công thức (F.1 -> F.9) sang LaTeX khối.
  - **Kiến trúc Song Mã:** Xây dựng 6 Visual Cards JSON + 6 Deterministic Solvers Python trong `wind_load_tcvn2737.py` + 38 unit tests Ground Truth.
  - **Ban hành ADR 0034 & Spec:** Chuẩn hóa toàn diện OKF v2.3 và phân rã 5 tickets triển khai cho toàn bộ hệ thống.

## [2026-08-28] [feat] | QCVN 03:2022/BXD 100% Verbatim Ingestion, Gate 11 Parity & Multi-Attachment Ingestion
- **Phạm vi:** `legal_docs/02_qcvn/qcvn_03_2022_bxd/`, `packages/ccba-legal-intel/`, `scripts/validate_legal_spoke.py`, `AGENTS.md`.
- **Nội dung:**
  - **Nạp QCVN 03:2022/BXD:** Đóng gói chuẩn OKF v2.4 Universal (12 trang PDF, 137 đoạn DOCX nguyên văn 100%, 23 AST clauses `CQXD`, Bảng 1 Niên hạn Mức 1-4, Phụ lục A Cấp hậu quả C1/C2/C3, thẻ tính toán và biểu mẫu nguyên tử).
  - **Gate 11 Verbatim Normative Parity Gate:** Thiết lập cổng kiểm định toán học thứ 11 trong CI và Pre-commit, chặn đứng mọi hành vi tóm tắt, diễn đạt lại thân văn bản quy phạm.
  - **Vá Lỗ hổng Tài liệu & Nhận diện Công cụ:** Thêm lệnh `convert` tường minh, 3 kịch bản vận hành vào `AGENTS.md` / `SKILL.md` và đăng ký 6 CLI subcommands vào `catalog.yaml`.
  - **Nâng cấp Multi-Attachment Crawler:** Tự động phát hiện và thu thập toàn bộ các tệp phụ lục đính kèm rời (`.doc`, `.docx`, `.xlsx`, `.pdf`) tại `tab=7` về `sources/attachments/` kèm unit test `100% PASS`.
  - **Tốt nghiệp R&D:** Chuyển hóa toàn bộ thuật toán vào Hub Deep Seam `ccba_legal.provenance` và `ccba_legal.crawler.tier_downloader`, dọn sạch 100% scratch scripts.

