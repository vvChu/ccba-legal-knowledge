# Walkthrough: Phát Hành Tính Năng PR #47 (Khắc Phục Toàn Trình Codebase Review, Gia Cố Pstack Verification Harnesses & Đồng Bộ 100% E2E Suite OKF v2.4)

> **Mục tiêu:** Giải quyết toàn bộ 20 phát hiện chặn từ đợt kiểm tra chéo song song `/ccba-code-review` (`Standards` + `Spec`) và 5 điều kiện nghiệm thu từ Grok 4.7; gia cố 2 bộ kiểm tra vệ sinh Spoke (`check_spoke_cleanliness.py`, `check_hub_import_depth.py`), 3 Pstack Verification Harnesses (bảo vệ tiến trình con bằng `Popen(..., start_new_session=True)` + `os.killpg` chống treo pipe), các cổng kiểm định OKF v2.4 (`validate_legal_spoke.py`, `verify_cross_links.py`), và đồng bộ 100% bộ kiểm thử `tests/e2e/` (`428 passed, 4 skipped, 0 failed`).
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **Spoke PR #47:** [vvChu/ccba-legal-knowledge#47](https://github.com/vvChu/ccba-legal-knowledge/pull/47) — Merge Commit: `b5b832d` (Squash and merge, 6/6 CI Checks Passed)
> - **Biên bản Thẩm định Grok 4.7:** Round 1 (`APPROVE_WITH_CONDITIONS`, Session `7b7b9a49-b881-4134-9ef2-d4884d782213`) & Round 2 (`FINAL_ACCEPT`, Risk: 1/5, 0 Blocking Conditions, Session `6e2ea3db-d153-4502-b98d-4f92501976d7`).

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (Spoke PR #47)

### A. Gia Cố Spoke Guardrails & Pstack Verification Harnesses
- Cập nhật `scripts/_guardrails/check_spoke_cleanliness.py` (mẫu Regex `MACHINE_PATH_RE` theo ADR-0061, sắp xếp tất định `sorted()` trên mọi phép duyệt thư mục) và `scripts/_guardrails/check_hub_import_depth.py` (quét toàn bộ dải dòng AST `[lineno..end_lineno]` để nhận diện `# ccba:quarantine` và `# ccba:allow-deep-import` trên câu lệnh import nhiều dòng).
- Chuyển đổi `run_cmd` trong 3 Pstack Verification Harnesses (`verify_legal_harness.py`, `verify_legal_intel_harness.py`, `verify_legal_ingest_harness.py`) từ `subprocess.run` sang `subprocess.Popen(..., start_new_session=True)` kèm `os.killpg(..., signal.SIGKILL)` khi `TimeoutExpired`, khử triệt để lỗi treo pipe khi tiến trình con sinh tiến trình cháu giữ mở `stdout`/`stderr`.

### B. Chuẩn Hóa Tất Định & Cổng Kiểm Định OKF v2.4 (`scripts/` & `.md/tools/`)
- Áp dụng **Filesystem Inode Ordering Invariance** (`sorted(...)`) và **Multi-Key Deterministic Sorting** (`-round(score, 4)`) cùng xử lý ngoại lệ tường minh (không dùng bare `except Exception: pass`) trên 14 kịch bản kiểm định trong `scripts/` và `.md/tools/verify_ground_truth_parity.py`.
- Nâng cấp `scripts/validate_legal_spoke.py` (Gate 2 bắt lỗi liên kết hỏng tới tài liệu cấu thành, Gate 8 quét đệ quy `rglob("*.md")`, Gate 12 kiểm tra đồng bộ $1:1$ thẻ thị giác `figures/cards/*.md` và cấm tệp `.wmf`/`.emf` đóng kín) và `scripts/verify_cross_links.py` (bóc tách đầy đủ cú pháp `[label](href)` kèm `urllib.parse.unquote`).

### C. Đồng Bộ 100% Bộ Kiểm Thử `tests/` Với Kiến Trúc OKF v2.4
- Cập nhật `tests/conftest.py` và 4 tệp kiểm thử trong `tests/e2e/` (`test_tier1_feature_coverage.py`, `test_tier2_boundaries.py`, `test_tier3_cross_features.py`, `test_tier4_real_world.py`) để phản ánh cấu trúc VBHN hợp nhất của `qcvn_06_2022_bxd`, phụ lục tách rời `annexes/*.md` (ADR 0036) và bảng dữ liệu 2D tách chú thích (ADR 0041), nâng tỷ lệ vượt qua toàn bộ pytest suite lên **100% (`428 passed, 4 skipped, 0 failed`)**.

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Loại Kiểm Tra | Lệnh Thực Thi / Workflow | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :--- | :---: |
| **Maskara Secret Gate** | Bảo mật mã nguồn | `python -m ccba_maskara.cli scan --staged` / CI | **0 secret leaks** | ✅ **PASSED** |
| **Cleanliness & Budget** | Vệ sinh Spoke | `python scripts/_guardrails/check_spoke_cleanliness.py` | **15/15 scripts, 0 leaks** | ✅ **PASSED** |
| **Hub Import Depth** | Kiến trúc Seam | `python scripts/_guardrails/check_hub_import_depth.py` | **44 files scanned, 0 violations** | ✅ **PASSED** |
| **Full Pytest Suite** | Unit + Integration + E2E | `python -m pytest tests/unit/ tests/integration/ tests/e2e/ -q` | **428 passed, 4 skipped, 0 failed** | ✅ **PASSED** |
| **Master Legal CI Gates**| 15 Cổng Tri thức | `python scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors)** | ✅ **PASSED** |
| **Spoke GitHub Actions CI**| 6 Jobs trên GitHub | `gh pr checks 47` | **6/6 Checks Passed** | ✅ **PASSED** |
| **Copilot / Bugbot Audit**| AI Review Gate | `python ../ccba-agent-platform/scripts/validation/audit_pr_comments.py --pr 47` | **0 unresolved comments (Clean)** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

<details>
<summary>Nhấn để xem chi tiết PR #44 & Hub PR #607 (Phát hành ngày 2026-11-05)</summary>

### PR #44 & Hub PR #607: Gia Cố Toàn Trình Pipeline `/ccba-legal-ingest`, Đồng Bộ Sổ Bộ 106 Bundles & Khóa Cổng Liên Kết Gate 2
- **T-01:** Đồng bộ khối `decrees:` (19 văn bản) và mở rộng Sub-Gate 5.3 lên **106/106 bundles**.
- **T-02:** Chuẩn hóa sinh `index.md` / `metadata.yaml` và bổ sung `_validate_index_md_links` trong Gate 2.
- **T-03:** Hợp nhất điểm vào ingest một cửa, hỗ trợ ADR 0043 Dual-PDF fallback và trích xuất DOCX header hints offline.
- **T-04:** Chuẩn hóa Nightly Telemetry và làm mới hàng đợi Provenance 106 bundles.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #40 (Phát hành ngày 2026-10-21)</summary>

### PR #40: Nạp Quyết Định 1812/QĐ-BXD 2026 Từ Điển Dữ Liệu Quốc Gia Về Hoạt Động Xây Dựng v1.0 & Đồng Bộ Spoke Guardrails
- **Tài liệu nguồn xác thực SHA-256 (`sources/`)**:
  - `quyet_dinh_1812_qd_bxd_2026.docx`: `35,186 bytes` (`d6e7c7d3fdd25a187fe66eeddfaf843741dc8054e575b0a0718652ed1f6a2e19`)
  - `quyet_dinh_1812_qd_bxd_2026.pdf`: `921,231 bytes`, 38 trang (`db769ac3c9f7795152aa7f8989b71974e9e2e18ef5afe0a87b8737a77627942e`)
- **Cấu trúc Bundle `legal_docs/01_vbpl/quyet_dinh_1812_qd_bxd_2026/`**:
  - Văn bản quy phạm nguyên văn `quyet_dinh_1812_qd_bxd_2026.md` (2,875 dòng, Verbatim Parity 100%).
  - Bảng từ điển dữ liệu 2D `tables/csv/bang_01.csv` & `tables/json/bang_01.json` (176 hàng dữ liệu x 9 cột, Zero Ragged Rows).
  - Cây điều khoản `clauses.json`, `qa_benchmark.json`, `metadata.yaml` và đăng ký vào `legal_registry.yaml` (liên kết `guided_by`: `nghi_dinh_212_2026_nd_cp`, `thong_tu_39_2026_tt_bxd`).
- **Đồng Bộ Layer-1 Constitution & Hiện Đại Hóa CI Matrix**:
  - Đồng bộ `.agents/AGENTS.md` từ Hub `ccba-agent-platform` và di chuyển bộ kiểm chuẩn về `scripts/_guardrails/`.
  - Cập nhật `scripts/spoke_cli.py` loại bỏ các trường sandbox tạm thời (`docx_path`, `pdf_path`, `attachments`, `links`) khi nạp `metadata_handoff.json`.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #37 (Phát hành ngày 2026-10-12)</summary>

### PR #37: Mạng Tri Thức Pháp Lý 5 Vành Đai Luật Xây Dựng 2025 & Suy Diễn Ngược Hai Chiều Trên RAM
- **Ontology 5 vành đai** kết nối Luật Xây dựng 2025 (`135/2025/QH15`) với 7 Nghị định thi hành, Nghị định xử phạt `339/2026/NĐ-CP`, 6 QCVN cốt lõi và phân cấp địa phương.
- **Động cơ suy diễn ngược 2 chiều trên RAM** (`build_bidirectional_legal_graph`) và Sub-Gate 5.4 / Sub-Gate 2.1.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #32 (Phát hành ngày 2026-10-06)</summary>

### PR #32: Triển Khai Pstack Verification Harness, Features Map & Hiện Đại Hóa Ma Trận 6 CI Gates
- **Kiến trúc Pstack 5 khối độc lập**: Clean-Slate Pre-flight, Dual-Mode Lifecycle, Deterministic Health Barrier, Evidence-Capture Suite, Guaranteed Cleanup ($300.0\text{ s}$ timeout).
- **Lập Bản Đồ 9 Tính Năng Quy Phạm**: Trong `features/INDEX.md` kèm quy tắc COND-01 chống gian lận dữ liệu.
- **Tái cấu trúc Ma trận CI 6 cổng song song**: Phân rã 1 job nguyên khối thành 5 cổng song song kèm Master Aggregator Gate khớp $1:1$ GitHub Ruleset `#23696513`.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #30 (Phát hành ngày 2026-10-05)</summary>

### PR #30: Số Hóa 6 Tiêu Chuẩn PCCC & Đường Đất Yếu, Cài Đặt Maskara Guardrail, Spoke Đạt 96 Bundles
- **Số hóa toàn diện 6 tiêu chuẩn**: `QCVN 02:2020/BCA`, `TCVN 13456:2022`, `TCVN 6379:2024`, `TCVN 7568-14:2025`, `TCCS 41:2022/TCĐBVN`, `TCCS 39:2022/TCĐBVN`.
- **Cài đặt Client-Side Guardrail**: Cài đặt `.githooks/pre-commit` kích hoạt `ccba-maskara` trước mỗi commit.
- **Đồng bộ Tri-Tier Cloud Vault**: 18 tệp nhị phân nguồn lên Google Drive Vault `gdrive:CCBA_Legal_Vault`.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #21 (Phát hành ngày 2026-10-03)</summary>

### PR #21: Đồng Bộ Cloud RAG NotebookLM & Ưu Tiên 6 Văn Bản Đấu Thầu 2024–2026 Vào Living Roadmap
- **Khắc phục lỗi xác thực Playwright (`notebooklm-py`)**: Truy vết và hotfix lỗi race condition / premature commit tại `browser_capture.py`.
- **Thực thi đồng bộ 65 nguồn văn bản quy phạm**: Tải mới 37 nguồn tri thức vào sổ tay `CCBA_Legal_Knowledge_Base_2026`.
- **Nghiên cứu thể chế & bổ sung 6 văn bản đấu thầu**: NĐ 349/2026, Luật 57/2024, NĐ 225/2025, TT 05/2024, TT 105/2025, TT 03/2024.

</details>

<details>
<summary>Nhấn để xem chi tiết PR #19 (Phát hành ngày 2026-10-03)</summary>

### PR #19: Nạp 2 Văn Bản Luật Tier 1 (Luật Nhà Ở 2023 & Luật Đất Đai 2024)
- **Luật Nhà ở 2023 (`27/2023/QH15`)**: 978 AST clauses, 1 bảng dữ liệu, 978 QA pairs.
- **Luật Đất đai 2024 (`31/2024/QH15`)**: 1,500 AST clauses, 2 bảng dữ liệu, 1,500 QA pairs.
- **Sổ bộ Pháp lý (`legal_registry.yaml`)**: Nâng từ 70 lên 72 văn bản pháp quy.
- **Google Drive Vault (`CCBA_Legal_Vault`)**: Tải lên và xác thực 100% SHA-256 cho 4 tệp DOCX/PDF gốc.

</details>
