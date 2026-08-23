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
