# 🧠 CCBA Legal Knowledge Spoke — Session Learnings & Knowledge Base

> **Mục đích:** Tài liệu lưu trữ các bài học kinh nghiệm (*Learnings*), mẫu hình kiến trúc (*Architectural Patterns*), giải pháp xử lý dữ liệu và tiêu chuẩn vàng (*Gold Standards*) được đúc kết qua các phiên làm việc với AI Agent trên Spoke `ccba-legal-knowledge`.

---

## 1. Mẫu Hình Xử Lý Bảng Biểu Kỹ Thuật (Table Grid & Footnote Patterns)

### A. Chuẩn Hóa Lưới Bảng 2D GFM (2D Pipe Table Normalization)
- **Vấn đề:** Khi bóc tách từ Word/DOCX chứa các ô merge hoặc header nhiều tầng, nếu xuất thành plain text dễ bị dính chuỗi `||` trên một dòng hoặc nhân bản chữ.
- **Giải pháp chuẩn hóa:**
  1. Mỗi hàng của bảng bắt buộc phải kết thúc bằng ký tự xuống dòng `\n`.
  2. Phải có dòng trống `\n\n` phía trước và phía sau bảng để trình render Markdown (như VS Code Preview, GitHub) nhận diện đúng cú pháp bảng HTML 2D.
  3. Tách toàn bộ các Chú thích chân bảng ra khỏi thân lưới bảng, đưa xuống dưới dạng văn bản độc lập.

### B. Xử Lý Chỉ Số Phụ Tham Chiếu (Superscript Footnote References)
- **Vấn đề:** Các số chỉ số phụ trong Word (như $100^{1)}$, $85^{1)}$, $1400^{2),3)}$) khi chuyển sang plain text bị dính liền thành `1001)`, `851)`, `14002),3)` $\rightarrow$ Con người và AI dễ đọc nhầm thành con số $1.001\text{ mm}$ (sai gấp 10 lần!).
- **Giải pháp chuẩn hóa:**
  1. Chuyển đổi thành thẻ HTML chuẩn: `100 <sup>1)</sup>`, `85 <sup>1)</sup>`, `thạch cao <sup>1)</sup>`.
  2. Trong AST JSON (`tables/json/*.json`): Phân tách mảng nguyên tử `numeric_value: 100`, `unit: "mm"`, `superscript_refs: [1]` theo **ADR 0004**.

### C. Phân Loại Cấu Trúc Chú Thích Chân Bảng (Footnote Taxonomy)
- Tách rạch ròi 2 nhóm:
  - `_CHÚ THÍCH:_` (Quy định chung cho toàn bảng).
  - `_GHI CHÚ CHỈ SỐ PHỤ:_` (Ghi chú giải nghĩa điều kiện riêng cho từng ô `1)`, `2)`...).

---

## 2. Mẫu Hình Định Dạng Thân Điều Khoản & Thẻ Neo Canonical

### A. Inlined Semantic Anchors
- **Vấn đề:** Đặt thẻ neo `<a id="..."></a>` trên dòng riêng biệt trước tiêu đề khiến trình xem Markdown tính toán sai tọa độ cuộn (bị che khuất phía trên).
- **Giải pháp chuẩn hóa:**
  Nhúng trực tiếp thẻ neo vào dòng tiêu đề Markdown:
  ```markdown
  ### <a id="muc-1-1-2" name="muc-1-1-2"></a>1.1.2  Quy chuẩn này áp dụng đối với các nhà và công trình sau:
  ```

### B. Chú Thích Đơn Lẻ Trong Điều Khoản (Single Clause Notes)
- Khi điều khoản chỉ có 1 chú thích đơn lẻ $\rightarrow$ Trình bày thành một đoạn văn in nghiêng duy nhất:
  ```markdown
  _CHÚ THÍCH: Trường hợp chuyển đổi nhà ở riêng lẻ sang mục đích khác thì phải tuân thủ..._
  ```
  *(Tuyệt đối không sinh thêm dòng tiêu đề `_CHÚ THÍCH:_` và gạch đầu dòng `- **CHÚ THÍCH:**` gây lặp từ).*

### C. Mục Lục Đầu Trang (Clean Table of Contents)
- Phần Mục lục ở đầu tài liệu phải là danh sách liên kết Markdown `[Tên Chương / Phụ lục](#anchor)` nằm dưới `## MỤC LỤC`, không sử dụng các thẻ tiêu đề giả (`## PHỤ LỤC...`) làm cướp thẻ neo của nội dung thực tế.

---

## 3. Hệ Thống 9 Quyết Định Kiến Trúc Đã Xác Lập (ADR Index)

1. **ADR 0001:** Dual-Track VBHN Provenance (Bản gốc 2022 + Sửa đổi 1:2023 + VBHN 2023 có nhúng Callout).
2. **ADR 0002:** Structured Table Footnote Binding Matrix.
3. **ADR 0003:** Annex Normative Guardrails (Mandatory vs Informative).
4. **ADR 0004:** Structured Array Pointer Binding cho Chỉ số phụ Đa tầng.
5. **ADR 0005:** Semantic Legal URI Scheme (`legal://[doc_id]#[clause_id]`) & Registry URL Router.
6. **ADR 0006:** Legal Precedence Hierarchy (`Luật > NĐ 217/2026 > QCVN > TCVN`) & Phân loại Defect.
7. **ADR 0007:** Dual-Layer CI Verification Gate (Pre-commit Hook + GitHub Actions).
8. **ADR 0008:** Temporal Legal Query Engine & Point-in-Time Auditing (Time-Travel RAG).
9. **ADR 0009:** Phân phối SDK dùng chung `ccba-legal-sdk` trên Hub.
10. **ADR 0010:** 4-Layer Precision TVPL VIP Crawler & Three-Tier Fallback.
11. **ADR 0011:** Atomic Clause RAG Chunking Strategy (~800 tokens preserving complete clause AST hierarchy).
12. **ADR 0012:** Clean Unified NotebookLM Ingestion Strategy (32 clean whitelist sources; isolate obsolete base/amendments).
13. **ADR 0013:** Dynamic Grace Period Compliance Gate (6-month transition warning window to 2027-06-15 for existing apartments).
14. **ADR 0014:** Split Jurisdiction PCCC Audit Routing (CQXD vs CONG_AN vs CDT_SELF_AUDIT per Law 55/2024 & ND 105/2025).
15. **ADR 0015:** Unresolved Normative Reference Fallback (`legal://` router to Metadata Stub Card + 1-Click PDF opener).
16. **ADR 0016:** Dual-Track Hybrid Extraction & PDF Anchor of Trust (DOCX for AST parsing, official gazette PDF with stamp as legal anchor).
17. **ADR 0017:** AST Structural Patching via Semantic Action Tokens for Legislative Consolidation.
18. **ADR 0018:** Git-Ratchet Multi-Platform Knowledge Sync & Dual-Store Topology (NotebookLM + Local Spark Vector DB).
19. **ADR 0019:** Tiered Audit Persona & Client Self-Audit Affidavit Engine (Automated PCCC Affidavit per ND 105/2025).
20. **ADR 0020:** Hybrid Symbolic Formula Solver Engine (LLM parameter extractor + deterministic Python formula solvers in `formulas/`).
21. **ADR 0021:** OKF v2.2 Pure Normative Body & Atomic Form Templates (Shallow path, 100% clean normative body, modular templates/ and tables/).
22. **ADR 0022:** OKF v2.2 QCVN Modular Annexes Architecture.
23. **ADR 0023:** Full Comprehensive NotebookLM Ingestion Strategy for Ultra Tier (500-600 sources quota, 100% full unified coverage).
24. **ADR 0024:** Dual-Track Provenance with Footnote Anchor for Consolidated Legal Norms.
25. **ADR 0025:** Strict Zero-Tolerance Provenance Enactment Gate for Legal Ingestion (Mandatory genuine binary source DOCX/PDF SHA-256).
26. **ADR 0026:** Package-Based Downstream Legal Knowledge Distribution via `ccba-legal-intel` SDK.

---

## 4. Mẫu Hình & Bài Học Đột Phá Đúc Kết (Core Evidence-Backed Learnings)

### A. Rào Chắn Nguồn Gốc Nhị Phân (Strict Binary Provenance vs Synthetic Data)
- **Anti-Pattern (AP-01):** Khi thiếu file Word gốc, Agent tự ý cào HTML từ web hoặc viết code tự sinh file DOCX nhân tạo (Synthetic DOCX) dẫn đến việc lọt mã JavaScript/quảng cáo rác hoặc đứt gãy paragraph.
- **Core Pattern (P-01):** Bắt buộc 100% tài liệu phải được tải trực tiếp từ máy chủ TVPL VIP hoặc Cổng Dữ liệu Quốc gia qua Deep Seam `TVPLCrawler` (Chrome CDP + Cloudflare Solver) và lưu vào `.md/extracted_docs/<slug>/` trước khi bóc tách.

### B. Thân Văn Bản Thuần Khiết (Pure Normative Body & Scoped Noise Stripping)
- **Core Pattern (P-02):** Loại bỏ 100% rác layout hành chính (Quốc hiệu, Tiêu ngữ, Nơi nhận, Chữ ký Chủ tịch Quốc hội / Bộ trưởng, mã JS/HTML) khỏi thân Markdown chính.
- Tách toàn bộ hơn 90 biểu mẫu hành chính thành Module Biểu mẫu Nguyên tử (`templates/`) và hơn 100 bảng số liệu thành (`tables/`).

### C. Kích Hoạt Tự Động Workflow Theo Ngữ Cảnh (Contextual Auto-Triggering)
- **Core Pattern (P-03):** Đặt `disable-model-invocation: false` trong YAML frontmatter và mở rộng mô tả ngữ cảnh song ngữ (tiếng Việt / tiếng Anh) cho các workflow trọng yếu (`ccba-legal-intel`, `ccba-tvpl-vip-crawler`, `ccba-convert-markdown`, `ccba-update-legal-registry`, `ccba-eval-gate`, `ccba-ai-qc-pccc-audit`) để Agent tự động nhận diện và kích hoạt đúng quy trình không cần người dùng gõ lệnh thủ công.

---

## 5. Rào Chắn Kiểm Toán Tự Động 5 Cổng CI Gates (Zero-Tolerance Quality Gates)

Mọi đóng góp dữ liệu mới vào Spoke bắt buộc phải chạy và vượt qua toàn bộ 5 script kiểm toán với `0 Errors, 0 Warnings, 100% Valid Links, 100% PDF SHA-256 Match, 100% Visual Parity`:
```bash
python scripts/validate_legal_spoke.py
python scripts/test_converter_regression.py
python scripts/audit_visual_parity.py
python scripts/verify_cross_links.py
python scripts/verify_all_docs_against_pdf.py
```

---

## 5. Mẫu Hình Quy Chuẩn Định Mức Theo Điều Khoản (Clause-based Standards)

### A. Đặc thù Quy chuẩn không có Bảng số riêng (như QCVN 04:2021/BXD)
- Nhiều quy chuẩn xây dựng (ví dụ QCVN 04 về Nhà chung cư) không tổ chức bảng số 2D rời rạc như QCVN 06, mà phân bổ định mức kỹ thuật trực tiếp vào cấu trúc điều khoản danh mục (Mục 2.2.4 diện tích căn hộ, Mục 2.2.17 định mức chỗ để xe, Mục 2.4 số lượng thang máy).
- Khi xử lý loại quy chuẩn này:
  1. Phân cấp Heading rõ ràng: H1 (Tiêu đề QCVN), H2 (Mục lục, Lời nói đầu), H3 (Chương & Mục lớn), H4 (Tiểu mục & Định nghĩa từ ngữ 1.4.x).
  2. Bóc tách triệt để nội dung câu văn quy định ra khỏi dòng Heading.
  3. Ghi nhận `table_structure: clause_based_standards` trong `metadata.yaml`.

### B. Dual-Track Sửa đổi Bổ sung (Amended Standards)
- Với các quy chuẩn có bản Sửa đổi (như Sửa đổi 01:2026 QCVN 04 theo Thông tư 31/2026/TT-BXD):
  1. Giữ nguyên tệp Bản Gốc (`qcvn_04_2021_bxd.md`).
  2. Tạo tệp Bản Sửa Đổi (`sua_doi_01_2026_qcvn_04_2021_bxd.md`) với cross-links 2 chiều trỏ về Bản Gốc (`qcvn_04_2021_bxd.md#muc-xxx`).
  3. Tạo tệp Bản Hợp Nhất (`qcvn_04_2021_bxd_hop_nhat_2026.md`) tích hợp đầy đủ nội dung mới và ghi chú xuất xứ.
  4. Lập Bảng ma trận đối chiếu kỹ thuật (`legal_docs/04_appendices/bang_so_sanh_sua_doi_2026/bang_so_sanh_sua_doi_2026.md`) phân loại mức độ lỗi kiểm toán (Critical Defect vs Warning Notice) theo ADR 0006.

---

## 6. Mẫu Hình Kết Nối Hub-Spoke Package & Trích Xuất Văn Bản 4 Lớp (ADR 0044)

### A. Chuẩn Hóa Cài Đặt Package Hub (Editable Install Protocol)
- **Vấn đề:** Tránh anti-pattern `sys.path.insert(0, str(HUB_SRC))` làm hỏng IDE typing, phân mảnh bảo trì và vi phạm ranh giới kiến trúc.
- **Giải pháp:**
  1. Spoke khai báo danh sách packages trong `.md/workspace_context.yaml` tại trường `hub_packages: [ccba-legal-intel]`.
  2. Cài đặt editable qua `pip install -e` từ thư mục `packages/` của Hub.
  3. Mọi script import trực tiếp: `from ccba_legal.crawler import ChromeCDP, get_tvpl_metadata, download_three_tier`.
  4. File `requirements-hub.txt` được tự động sinh và bắt buộc thêm vào `.gitignore`.

### B. Quy Trình Trích Xuất & Kiểm Tra Độ Chính Xác 4 Lớp (4-Layer Precision Gate)
- Khi trích xuất và tải văn bản từ Thư Viện Pháp Luật (TVPL), script `scripts/fetch_tvpl_doc.py` cưỡng chế 4 lớp kiểm tra:
  1. **Lớp 1 (Khóa Định Danh Kép):** Lấy URL chứa TVPL Unique ID từ `legal_registry.yaml`.
  2. **Lớp 2 (Đối Soát Metadata):** Đọc Bảng Thuộc Tính từ Tab Lược đồ TVPL để đối soát Số hiệu, Cơ quan, Thể loại và Ngày hiệu lực trước khi tải.
  3. **Lớp 3 (Quét Trạng Thái Hiệu Lực & Cây Quan Hệ):** Kiểm tra nhãn trạng thái (Còn hiệu lực / Chưa có hiệu lực / Hết hiệu lực) và bóc tách các văn bản hướng dẫn/sửa đổi con.
  4. **Lớp 4 (Tải 3 Tầng & Checksum):** Tải file `.docx`/`.doc` gốc qua `download_three_tier` (Cache $\rightarrow$ Cloud $\rightarrow$ Live CDP), tính SHA-256 và tự động cập nhật vào `legal_registry.yaml`.

---

## 7. Mẫu Hình Phòng Thủ & Chống Lỗi Kiểm Định Ảo (Anti-Patterns & Quality Defenses)

### A. Anti-Pattern: Báo Xanh Ảo (False Green CI Gates)
- **Triệu chứng:** CI Gates báo `PASSED 100%` nhưng thực chất chỉ đang kiểm tra các tiêu chí cú pháp cũ (Markdown header, thẻ neo cơ bản) mà không kiểm tra sự tồn tại của file PDF gốc, mã băm hay các trường AST nghiệp vụ mới (`jurisdiction`, `grace_period_end`).
- **Giải pháp triệt tiêu:** Mở rộng `scripts/validate_legal_spoke.py` với hàm `validate_pdf_metadata_and_ast_enrichment()` cưỡng chế $100\%$ điều khoản phải có `jurisdiction` hợp lệ và `cong_bao_number`.

### B. Mẫu Hình: Danh Mục Lồng Đa Tầng Chuẩn CommonMark (CommonMark Nested Lists)
- **Triệu chứng:** Danh mục phân cấp con (`  -`) bị dồn hàng thành bullet cấp 1 do thiếu thụt dòng 2 spaces hoặc bị ngắt bởi dòng trống không thụt lề.
- **Giải pháp triệt tiêu:** Sử dụng cú pháp thụt dòng chuẩn CommonMark 2 spaces (`  -`) và kiểm tra bằng ảnh chụp trang PDF Công báo gốc làm mỏ neo thị giác (*Visual Ground Truth*).

