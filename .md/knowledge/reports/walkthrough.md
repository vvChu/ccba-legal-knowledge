# Walkthrough: Hoàn Thành Chu Kỳ `/ccba-create-pr` & Giải Quyết Copilot Review (PR #6)

> **Mục tiêu:** 
> 1. Triển khai lệnh `/ccba-create-pr` trên Spoke repository `ccba-legal-knowledge`.
> 2. Tuân thủ Main Branch Guard: Tạo retroactive feature branch `feat/priority-standards-and-governance-hardening`, bảo toàn 10 commits chưa push, đưa `main` về đồng bộ với `origin/main`.
> 3. Mở Pull Request [**PR #6**](https://github.com/vvChu/ccba-legal-knowledge/pull/6) trên GitHub.
> 4. Đồng hành qua vòng lặp Dual-Gate CI & Copilot Review Self-Healing:
>    - Giải quyết lỗi Linux CI runner (ADR 0043/0044 broken references và case-sensitivity 50 table filenames).
>    - Tiếp nhận và xử lý triệt để 5 phản biện chất lượng cao từ Copilot Code Review.
> 
> **Thời điểm hoàn thành:** 2026-09-16 16:48:00 +07:00  
> **Trạng thái:** ✅ **HOÀN TẤT & ĐÃ COMMIT TOÀN DIỆN 100% (Commit: `f5ef5d3`)**

---

## 1. Thông Tin Nhận Diện Copilot Code Review

- **Review ID:** `PRR_kwDOT56haM8AAAABNy9n_A` (State: `COMMENTED`, Author: `copilot-pull-request-reviewer`)
- **Review Summary:** Lite code review covering changed files, raising 5 actionable inline comments.
- **Tình trạng:** Đã giải quyết 5/5 nhận xét phản biện tại commit `f5ef5d3`, 15/15 Master CI Gates passed, GitHub Actions CI passed.

---

## 2. Chi Tiết 5 Phản Biện Của Copilot & Giải Pháp Khắc Phục Nguyên Văn

### 2.1. QCVN 07:2023/BXD - Bảng 4
- **Comment ID:** `4024429597`
- **File:** `legal_docs/02_qcvn/qcvn_07_2023_bxd/tables/csv/bang_04.csv`
- **Nội dung:** "The stopping-distance value for the speed row “50” is missing (empty second column). For a numeric lookup table like this, an empty cell is likely an extraction error and will cause incorrect downstream computations/answers; please re-extract this table from the authoritative source so the missing value is populated."
- **Giải pháp:** Đối chiếu DOCX và Chú thích 2 quy chuẩn: *"Trường hợp tốc độ thiết kế dưới 50 km/h, lấy SD = 50 m"*, cập nhật chuẩn xác `50,50` đồng bộ trên `bang_04.csv`, `bang_04.json` và `qcvn_07_2023_bxd.md`.

### 2.2. TCVN 5575:2024 - Bảng 7 & Hình 4
- **Comment ID:** `4024429649`
- **File:** `legal_docs/03_tcvn/tcvn_5575_2024/tables/csv/bang_07.csv`
- **Nội dung:** "This cell contains a generic conversion diagnostic sentence instead of the table’s actual content for the “Hình dạng” column. This is non-verbatim data and will pollute downstream retrieval; please regenerate/re-extract this row from the source so it contains the intended symbol/figure description. This issue also appears on line 4 of the same file."
- **Giải pháp:** Khôi phục mô tả tiết diện kỹ thuật chuẩn xác theo tiêu chuẩn:
  * Hàng a: `Tiết diện ống tròn và ống hộp cán nóng`
  * Hàng b: `Tiết diện thép hình cán và tổ hợp hàn`
  * Hàng c: `Tiết diện chữ T; chữ U; thép góc đơn và tổ hợp hàn`
  * Đồng thời làm sạch bảng layout chứa câu xin lỗi của vision model phía trên Hình 4 tại dòng 1030 trong `tcvn_5575_2024.md`.

### 2.3. TCVN 5575:2024 - Bảng 14
- **Comment ID:** `4024429693`
- **File:** `legal_docs/03_tcvn/tcvn_5575_2024/tables/csv/bang_14.csv`
- **Nội dung:** "Cells in this table contain a conversion/explanation artifact (\"$` delimiters... Therefore, the LaTeX code is simply `\infty`.$") instead of the actual table value. This is non-verbatim content and will break consumers expecting a numeric/symbolic β value; please regenerate the table from sources so the cell contains only the intended value (e.g., the symbol itself), not the conversion narrative."
- **Giải pháp:** Khôi phục ký hiệu vô cực nguyên bản `$\infty$` trong `bang_14.csv`, `$\\infty$` trong `bang_14.json` và `$\infty$` trong `tcvn_5575_2024.md`.

### 2.4. TCVN 5575:2024 - Bảng F.2
- **Comment ID:** `4024429725`
- **File:** `legal_docs/03_tcvn/tcvn_5575_2024/tables/csv/bang_f_2.csv`
- **Nội dung:** "This CSV row contains an assistant-style apology/diagnostic sentence rather than the table’s normative content, which will contaminate downstream indexing/QA and likely fails the repository’s verbatim data invariants. The table extraction should be regenerated from the original sources so this cell contains the real value (or a deterministic placeholder produced by the pipeline)."
- **Giải pháp:** Khôi phục đúng loại tải trọng là `$q$`, giá trị $\Psi$ tại cả 2 dải $\alpha$ (`gridSpan=2`) là `$1,42\sqrt{\alpha}$` trong `bang_f_2.csv`, `bang_f_2.json` và Phụ lục F (`phu_luc_f_he_so_on_dinh_khi_uon_b.md`).

### 2.5. Tooling - Import Error Handling
- **Comment ID:** `4024429759`
- **File:** `scripts/sync_notebooklm_knowledge.py`
- **Nội dung:** "This ImportError handler becomes more likely to trigger on API mismatches now that the import path changed. The error message currently implies the entire ccba_notebooklm package is missing, but from ccba_notebooklm import get_client also raises ImportError when the package exists but get_client is not exported (version mismatch), which is misleading for debugging."
- **Giải pháp:** Bắt `except ImportError as exc:` và hiển thị đầy đủ chi tiết lỗi import (`f"Lỗi import ccba_notebooklm (hoặc thiếu get_client): {exc}"`).

---

## 3. Kết Quả Kiểm Định 15-Gate Master CI (Local Shift-Left & Pre-Commit)

Toàn bộ 15 Cổng kiểm định chất lượng chạy tự động qua pre-commit hook và lệnh `python scripts/validate_legal_spoke.py`:

```text
=================================================================
       CCBA LEGAL SPOKE MASTER INTEGRITY & SCHEMA VALIDATOR      
=================================================================
Target Workspace: D:\GitHubProjects\ccba-legal-knowledge

ℹ️ Living Expansion Roadmap is up to date (no substantive changes).
-> Gate 1: Registry Check completed.
-> Gate 2: OKF Bundles Structure Check completed.
-> Gate 3: Table Attachments Check completed.
-> Gate 4: Fake Data Gate Check completed.
-> Gate 5: PDF Metadata & AST Jurisdiction Gate Check completed.
-> Gate 6: Pure Normative Body & Scoped Noise Gate Check completed.
-> Gate 7: Spoke Cleanliness & Zero-Wrapper Gate completed.
-> Gate 8: Template & Table Structural Integrity Gate completed.
-> Gate 9: Visual Parity & Formatting Clutter Gate completed.
-> Gate 10: ADR Living Traceability & Self-Healing Sync completed.
-> Gate 11: DOCX-to-Markdown Verbatim Normative Parity Gate completed.
-> Gate 12: Multimodal Decoupled Asset & SVG/Cards Integrity Gate (ADR 0040) completed.
-> Gate 13: Table Knowledge Extraction & 2D Matrix Regularity Gate (ADR 0041) completed.
-> Gate 14: KaTeX Math Syntax & Rendering Integrity Gate (ADR 0038) completed.
-> Gate 15: OKF Provenance & Algorithm Version Attestation Gate completed.

-----------------------------------------------------------------
SUMMARY REPORT: Errors: 0 | Warnings: 0
-----------------------------------------------------------------

✅ PASSED: All legal knowledge gates validated successfully!
✅ PRE-COMMIT PASSED: Repository is 100% clean and verified.
```

---

## 4. Trạng Thái GitHub Actions CI & Pull Request #6

- **Repository:** `vvChu/ccba-legal-knowledge`
- **Branch:** `feat/priority-standards-and-governance-hardening`
- **Head Commit:** `f5ef5d3` (`fix(verbatim): resolve Copilot review comments on table values and import error handling`)
- **PR Link:** [https://github.com/vvChu/ccba-legal-knowledge/pull/6](https://github.com/vvChu/ccba-legal-knowledge/pull/6)
- **CI Workflow:** `Deterministic Parity & Schema Audit` -> **PASS in 20s (EXIT CODE 0)**
