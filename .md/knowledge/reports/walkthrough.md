# Walkthrough: Phát Hành Tính Năng PR #37 (Mạng Tri Thức Pháp Lý 5 Vành Đai Luật Xây Dựng 2025 & Suy Diễn Ngược Hai Chiều Trên RAM)

> **Mục tiêu:** Thiết lập Mạng Tri thức Pháp lý 5 Vành đai (5-Ring Legal Knowledge Graph) cho Luật Xây dựng 2025 (`135/2025/QH15`); triển khai động cơ suy diễn quan hệ 2 chiều động trong bộ nhớ RAM (`build_bidirectional_legal_graph`) tuân thủ nghiêm ngặt nguyên lý Single Source of Truth và KISS v2.0 (ADR-0061); xây dựng Sub-Gate 5.4 Referential Integrity và Sub-Gate 2.1 Orphan Bundle Lock trong `validate_legal_spoke.py`; nâng cấp Two-Stage Semantic Routing cho Agent Skills (`ccba-legal-advisor`, `ccba-hybrid-rag-search`); đạt chứng nhận thẩm định đối kháng song phương từ Grok (xAI) với mức rủi ro tối thiểu (Risk 1.0/10).
> **Trạng thái:** ✅ **MERGED VÀO MAIN**
> - **PR #37:** [vvChu/ccba-legal-knowledge#37](https://github.com/vvChu/ccba-legal-knowledge/pull/37)
> - **Merge Commit:** `80cefd9` (Squash and merge)
> - **CI Gate:** 100% Green (6/6 Checks Passed, 0 Errors, 0 Blocker Warnings, 100% Referential & Parity Integrity)

---

## 1. Chi Tiết Các Thay Đổi & Thành Quả Phát Hành (PR #37)

### A. Thiết Lập Mạng Tri Thức Pháp Lý 5 Vành Đai cho Luật Xây Dựng 2025
- **Ontology đa vành đai toàn diện**:
  1. **Vành đai 1 — Khung Thi hành Trực tiếp (`enacted_by`):** Kết nối 7 Nghị định trụ cột thi hành Luật 135/2025/QH15 (`193/2026/NĐ-CP`, `206/2026/NĐ-CP`, `207/2026/NĐ-CP`, `209/2026/NĐ-CP`, `210/2026/NĐ-CP`, `212/2026/NĐ-CP`, `217/2026/NĐ-CP`).
  2. **Vành đai 2 — Chế tài Xử phạt VPHC (`sanctioned_by`):** Kết nối Nghị định `339/2026/NĐ-CP` (thay thế Nghị định 16/2022/NĐ-CP).
  3. **Vành đai 3 — Thủ tục Liên thông 1 Cửa & Pháp luật Chuyên ngành (`interlocks_with` & `related_statutes`):** Kết nối Luật PCCC & CNCH 2024 (`55/2024/QH15`), Nghị định `105/2025/NĐ-CP`, Luật Quy hoạch Đô thị & Nông thôn (`47/2024/QH15`), Luật Đấu thầu (`22/2023/QH15` & `90/2025/QH15`), Luật Đất đai 2024 (`31/2024/QH15`), Luật Nhà ở 2023 (`27/2023/QH15`), Luật Kiến trúc (`40/2019/QH14`).
  4. **Vành đai 4 — Quy chuẩn Kỹ thuật Bắt buộc (`mandatory_codes`):** Kết nối 6 quy chuẩn cốt lõi (`QCVN 06:2022/BXD`, `QCVN 04:2021/BXD`, `QCVN 18:2021/BXD`, `QCVN 16:2023/BXD`, `QCVN 03:2022/BXD`, `QCVN 01:2021/BXD`).
  5. **Vành đai 5 — Phân cấp Địa phương (`local_delegations`):** Kết nối Quyết định `38/2026/QĐ-UBND` (Hà Nội) về phân cấp thẩm quyền quản lý quy hoạch - kiến trúc và cấp phép xây dựng.

### B. Động Cơ Suy Diễn Ngược Hai Chiều Trên RAM (In-Memory Graph Inversion — ADR-0061)
- **Bảo toàn Single Source of Truth trên đĩa:**
  - Dữ liệu lưu trữ tĩnh tại `legal_registry.yaml` và `metadata.yaml` chỉ lưu quan hệ một chiều trực tiếp từ gốc văn bản.
  - Hàm `build_bidirectional_legal_graph` trong `scripts/spoke_cli.py` tự động hoán vị ma trận kề (transpose adjacency list) trên bộ nhớ RAM khi truy vấn, tổng hợp tức thì các quan hệ nghịch đảo:
    - `enacted_by` $\longleftrightarrow$ `enacts`
    - `guided_by` $\longleftrightarrow$ `guides`
    - `sanctioned_by` $\longleftrightarrow$ `sanctions`
    - `interlocks_with` $\longleftrightarrow$ `interlocks_with`
    - `related_statutes` $\longleftrightarrow$ `related_statutes`
    - `mandatory_codes` $\longleftrightarrow$ `governs`
    - `local_delegations` $\longleftrightarrow$ `delegated_from`
    - `replaces` $\longleftrightarrow$ `replaced_by`
    - `amends` $\longleftrightarrow$ `amended_by`
- **Giao diện CLI trực quan:** Cung cấp lệnh CLI phong phú:
  ```bash
  python scripts/spoke_cli.py graph --doc <id|so_van_ban|slug> [--json]
  ```
  Hiển thị trực tiếp cây hệ sinh thái pháp lý với các khối `QUAN HỆ HƯỚNG TÂM` và `QUAN HỆ SUY DIỄN NGƯỢC`.

### C. Hai Tầng Kiểm Định Toàn Vẹn Mới (Sub-Gate 5.4 & Sub-Gate 2.1)
- **Sub-Gate 5.4 (Semantic Relations Referential Integrity):** Tự động đối soát chéo toàn bộ 6 trường quan hệ mở rộng trên cả `legal_registry.yaml` và `metadata.yaml`, chặn đứng 100% các liên kết đứt gãy (dangling references) hoặc trỏ tới văn bản chưa đăng ký.
- **Sub-Gate 2.1 (Orphan Bundle Lock):** Quét toàn bộ thư mục `legal_docs/01_vbpl`, `02_qcvn`, `03_tcvn`, ngăn chặn tuyệt đối tình trạng các bundle được commit / tracked trong git nhưng chưa đăng ký vào `legal_registry.yaml` (giải quyết triệt để lỗ hổng lách kiểm định).

### D. Tối Ưu Hóa Chuẩn Mực Code Quality & KISS v2.0
- Refactor toàn bộ các hàm xử lý đồ thị và validator thành các module nhỏ $\le 50$ dòng theo đúng `<RULE[user_global]>` Mục 5.
- Tự động chuẩn hóa đường dẫn `source_file` từ `.md/extracted_docs/...` về đúng ngăn kéo chuẩn `sources/` của từng bundle (ADR 0036).

---

## 2. Ma Trận Nghiệm Thu Kiểm Định (Verification Matrix)

| Cổng Kiểm Định | Loại Kiểm Tra | Lệnh Thực Thi / Workflow | Kết Quả | Trạng Thái |
| :--- | :--- | :--- | :--- | :---: |
| **Maskara Secret Gate** | Bảo mật mã nguồn | `python -m ccba_maskara.cli scan --staged` / CI | **0 secret leaks** | ✅ **PASSED** |
| **Cleanliness & Budget** | Vệ sinh Spoke | `python scripts/check_spoke_cleanliness.py` | **15/15 scripts budget, Clean** | ✅ **PASSED** |
| **Skills Governance** | Metadata Governance | Inline Python AST (ADR-0066/ADR-0057) | **100% Valid, GPI $\ge$ 12.0** | ✅ **PASSED** |
| **Pstack Verification** | Harness Smoke Test | `verify_legal_harness.py --smoke` | **All tests passed** | ✅ **PASSED** |
| **Master Legal CI Gates**| 15 Cổng Tri thức | `python scripts/validate_legal_spoke.py` | **15/15 Gates Passed (0 Errors)** | ✅ **PASSED** |
| **Master Aggregator Gate**| Ruleset #23696513 | `Deterministic Parity & Schema Audit` | **Aggregated 5/5 sub-gates (3s)** | ✅ **PASSED** |

---

## 3. Lịch Sử Phát Hành Tiền Nhiệm

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
