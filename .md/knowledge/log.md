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

## [2026-09-05] [feat] | QCVN 10:2024/BXD 100% Verbatim Ingestion, Horizontal Layout Table Figure Stitching & Unit Normalization
- **Phạm vi:** `legal_docs/02_qcvn/qcvn_10_2024_bxd/`, `packages/ccba-legal-intel/`, `scripts/validate_legal_spoke.py`, `.md/knowledge/`.
- **Nội dung:**
  - **Nạp QCVN 10:2024/BXD:** Đóng gói chuẩn OKF v2.4 Universal với 100% Verbatim Parity (276 đoạn văn bản đối soát khớp 1:1, 0 đoạn thiếu), 2 bảng tra số liệu 2D (`tables/`), 2 Phụ lục quy phạm (`annexes/`), 25 thẻ thị giác (`figures/cards/`), AST `clauses.json` và bộ câu hỏi `qa_benchmark.json`.
  - **Động cơ Ghép ảnh Ngang Bảng Layout (Horizontal Dynamic Canvas Stitching):** Khắc phục lỗi The "Inline Paragraph" Fallacy và Decoupled Pipeline Silos trong `figure_extractor.py`, tự động quét bảng không viền $\le 3$ hàng, bóc tách và ghép nối 2 sơ đồ con song song kèm nhãn $a), b)$ căn giữa (Hình 1 bãi xe, Hình 14 tay vịn vệ sinh, Hình 18 khoảng cách trồng cây).
  - **Chuẩn hóa Nhãn Đơn vị Đo lường (Unit Normalization):** Sửa lỗi FSM nuốt chửng text trong `heading_handler.py`, xuất trực tiếp `<p align="right"><em>Đơn vị tính: mm</em></p>` vào Markdown stream.
  - **Đúc kết Bài học Kinh nghiệm Mục 42 & Khảo sát 5 Bẫy ngầm:** Ghi nhận vào `session_learnings.md` và phân tích sâu các rủi ro Floating Text Box, Ghost Media, Slug Collision, EMU Scaling và Symbol PUA Font.
  - **Nghiệm thu Master CI 15 Gates:** Đạt $100\%$ tỷ lệ đạt chuẩn trên toàn bộ 39 văn bản của Spoke. Đẩy thành công 92 commits lên GitHub Remote `origin/main`.

## [2026-09-05] [feat] | QCVN 10:2025/BCA 100% Verbatim Ingestion, Pure AST Tree & Zero Ragged Rows 2D Matrix Regularity
- **Phạm vi:** `legal_docs/02_qcvn/qcvn_10_2025_bca/`, `legal_registry.yaml`, `.md/knowledge/expansion_roadmap.md`, `.md/knowledge/log.md`.
- **Nội dung:**
  - **Nạp QCVN 10:2025/BCA:** Đóng gói chuẩn OKF v2.4 Universal với 100% Verbatim Parity (548 đoạn DOCX đối soát khớp 1:1, 0 đoạn thiếu), ban hành kèm Thông tư 103/2025/TT-BCA của Bộ Công an, có hiệu lực 30/12/2025 (Thay thế phần bắt buộc của TCVN 3890:2023).
  - **Cấu trúc Dữ liệu Đa tầng:** 13 bảng tra cứu số liệu 2D chuẩn chữ nhật (Zero Ragged Rows, footnotes decoupled vào metadata), 8 Phụ lục kỹ thuật quy phạm (A đến H), cây AST `clauses.json` (105 điều khoản phân quyền `CONG_AN`), bộ câu hỏi `qa_benchmark.json` (110 test cases), và các thẻ thuyết minh `figures/`, `templates/`.
  - **Chẩn đoán & Xử lý Triệt để Lỗi Visual Parity:** Khắc phục lỗi `MISSING_NOTE_1` do chuyển đổi nhầm các dòng tham số (`24 h`, `36 h`, `72 h`, `20 L/s`, `48 h`) thành tiêu đề Markdown giả, khôi phục cấu trúc phân cấp danh sách chuẩn quy chuẩn cho Điều H.1.3.4 và CHÚ THÍCH 1 - 2.
  - **Nghiệm thu Master CI 15 Gates:** Vượt qua 100% toàn bộ 15 Cổng kiểm định chất lượng nghiêm ngặt của Spoke (`scripts/validate_legal_spoke.py`), nâng tổng số văn bản tri thức chuẩn hóa lên **40 văn bản**.



## [2026-09-05] [refactor] | QCVN 10:2025/BCA Complete Remediation: Decoupled Annexes, 19 Tables, and 10 Visual Parity Error Patterns
- **Phạm vi:** `legal_docs/02_qcvn/qcvn_10_2025_bca/`, `legal_registry.yaml`, `.md/knowledge/`.
- **Nội dung:**
  - **Bóc tách 8 Module Phụ lục kỹ thuật quy phạm (`annexes/`):** Tách rời hoàn toàn Phụ lục A đến H ra khỏi thân văn bản chính, trả lại Pure Normative Body cho `qcvn_10_2025_bca.md`, tạo liên kết 2 chiều đồng bộ giữa `index.md` và `annexes/README.md`.
  - **Số hóa toàn diện 19 Bảng số liệu tra cứu 2D (`tables/`):** Bổ sung đầy đủ 19 cặp CSV + JSON (thêm Bảng A.3, B.1, C.1, D.1, G.1), khử 100% rò rỉ chú thích ở Bảng H.2 và H.7, khôi phục nguyên văn chú thích (1)–(5) của Bảng A.3 và định mức xe chữa cháy Bảng D.1.
  - **Trích xuất Đồ họa nét cao (`figures/`):** Bóc tách raster $\ge 300\text{ DPI}$ từ PDF gốc cho `hinh_h_1.png` và `hinh_h_2.png`, lập 2 Visual Cards và `figures_catalog.yaml`.
  - **Xử lý triệt để 10 hình mẫu lỗi vi mô:** Khắc phục lỗi đảo phả hệ chú thích (Dual-Zone), rơi rụng dấu trừ do ngắt trang, phẳng hóa ô gộp ngang (`gridSpan`), mất chỉ số trên `<sup>`, vỡ thụt lề `&nbsp;&nbsp;\- `, lẫn lộn chú thích với điều khoản, và bảo toàn token trích dẫn gốc `QCVN 06:/BXD`.
  - **Nghiệm thu Master CI 15 Gates:** Vượt qua 100% 15 Cổng Master CI Gate với 0 Errors và 0 Visual Parity Errors trên toàn bộ kho tri thức.

## [2026-09-06] [feat] | 4-Layer Defense-in-Depth: Enforced Annex Leakage Gate, Rating Superscripts & Dual-Zone Footnote Linter
- **Phạm vi:** `scripts/validate_legal_spoke.py`, Hub `packages/ccba-legal-intel/src/ccba_legal/visual_parity.py`, `.md/knowledge/`.
- **Nội dung:**
  - **Khóa chặt Gate 6 (Pure Normative Body Gate):** Thêm kiểm tra **Annex Leakage Hard Gate** (`_check_annex_leakage`), báo lỗi Exit 1 ngay lập tức nếu phát hiện heading Phụ lục `## PHỤ LỤC [A-Z0-9]` nằm trong thân văn bản chính của quy chuẩn (`02_qcvn`, `03_tcvn`), bảo đảm tuân thủ triệt để ADR 0036.
  - **Nâng cấp Linter Gate 9 (Visual Parity Gate):** Bổ sung 2 quy tắc bắt lỗi vi mô tự động:
    1. `RAW_TABLE_SUPERSCRIPT`: Phát hiện ký hiệu mỏ neo trần như `+(1)`, `++(1)`, `+++(1)` trong ô bảng để cưỡng chế định dạng `<sup>(1)</sup>`.
    2. `INVERTED_FOOTNOTE_HIERARCHY`: Bắt lỗi đảo phả hệ chú thích khi `**CHÚ THÍCH:**` đặt đè lên các chú thích ô `(1)`, `(2)` khi có kèm theo các dòng giải nghĩa dấu `Dấu “+++”` (Dual-Zone Decoupling Engine theo Session Learning 44).
  - **Nghiệm thu Master CI 15 Gates:** Vượt qua 100% 15 Cổng Master CI Gate với 0 Errors và 0 Visual Parity Errors trên toàn bộ 402 files Markdown của Spoke.

## [2026-09-19] [feat] | 100% Ground Truth Parity Campaign: Phase 1 Completion (50/55 Pass Rate, 87 Tables Extracted & Nightly Telemetry Integration)
- **Phạm vi:** Spoke `legal_docs/`, Hub `packages/ccba-legal-intel/`, `scripts/cron/run_nightly_tuner.sh`, `.md/tools/run_nightly_telemetry.py`, `.md/knowledge/`.
- **Nội dung:**
  - **Triển khai Động cơ Đối soát Xác định 1-1 (Deterministic Ground Truth Parity Engine v2.0):** Phát triển thuật toán Greedy Multi-Span Coverage ($\ge 70\%$ từ vựng trên span $\ge 4$ từ) và đối soát 5 trục (Verbatim, 2D Grid, KaTeX Math, Multimodal Asset, Structural AST), loại bỏ hoàn toàn các lỗi False Pass (cửa sổ 6 từ) và False Drop (KaTeX macro, inline MathType VML/OLE).
  - **Hoàn tất Pha 0 & Pha 1 Chiến dịch Parity:** Trích xuất 87 bảng dữ liệu quan hệ chuẩn 2D (Zero Ragged Rows, footnotes decoupled) cho 10 bundle (`TT 12/2025`, `TT 13/2025`, `TT 14/2025`, `TT 34/2025`, `TT 36/2025`, `TT 79/2026`, `TT 07/2024`, `TT 08/2024`, `QCVN 01:2021`, `QCVN 09:2025`). Nâng tỷ lệ đạt chuẩn toàn Spoke từ **34/55 (61.8%)** lên **50/55 (90.9%)**.
  - **Lọc bỏ Căn cứ Hành chính & Layout Heuristics:** Cập nhật `compute_docx_to_markdown_parity` và Gate 11 để bỏ qua phần mở đầu hành chính không mang tính quy phạm; siết chặt nhận diện bảng chữ ký hành chính ("đơn vị tính", `nơi nhận:` + `lưu: vt`/`kt.`).
  - **Tích hợp Tự động Ban Đêm trên Server Spark (:8090):** Nâng cấp `run_nightly_telemetry.py` và `run_nightly_tuner.sh` hỗ trợ `--cohorts all`, quét toàn bộ 55 văn bản trong ~22s, tự động ghi nhận 5 diagnostic tickets còn lại và commit báo cáo định kỳ lúc 00:00 AM với zero token cost.
  - **Nghiệm thu Master CI 15 Gates:** Vượt qua 100% 15 Cổng Master CI Gate với `0 Errors, 0 Warnings` trên toàn bộ 58 bundles.



