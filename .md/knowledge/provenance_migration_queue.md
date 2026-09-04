# Hàng Đợi Di Trú & Kiểm Toán Nguồn Gốc Tri Thức (OKF v2.4 Universal Provenance Queue)

> [!IMPORTANT]
> **Tài liệu kiểm toán nguồn gốc độc lập của CCBA Legal Spoke (Gate 15 ADR 0036 - ADR 0041).**
> Tuyệt đối không chạy script đóng dấu khống (False Attestation). Mọi việc cấp tem `okf_spec: v2.4 Universal`
> bắt buộc phải tuân theo Chiến lược Di trú Phân tầng (Tiered Migration Protocol).

- **Thời điểm quét:** `2026-09-04 23:03:35 UTC`
- **Tiêu chuẩn chuẩn hóa:** `v2.4 Universal` (Converter: `0.4.0`)
- **Quy mô kho tài liệu:** **38 văn bản** (35 gói tri thức chính quy + 3 ma trận đối chiếu)
- **Tiến độ cấp tem bảo chứng:** **1 / 35** (2.9%)

---

## 1. Ma Trận Phân Hạng Chiến Lược Di Trú (Strategy Matrix)

| Nhóm Phân Loại | Số Lượng | Bản Chất Dữ Liệu | Chiến Lược Di Trú Đề Xuất | Mức Độ Rủi Ro |
| :--- | :---: | :--- | :--- | :---: |
| **🟢 Nhóm A (Clean Passthrough)** | **24** | Luật, Nghị định, Thông tư thuần túy; bảng biểu mẫu phẳng | Chạy kiểm toán Gate 1-11, cấp tem Attestation có bảo chứng | 🟢 Rất Thấp |
| **🔶 Nhóm B (Compartment Refresh)** | **9** | QCVN/TCVN kỹ thuật dày đặc bảng số liệu 2D, KaTeX, đồ họa | Phẫu thuật cục bộ ngăn kéo `tables/` và `figures/cards/` | 🟡 Trung Bình |
| **🔷 Nhóm C (Consolidated Shield)** | **2** | Văn bản Hợp nhất VBHN có `bang_so_sanh_thay_doi.md` | Snapshot bảo vệ -> Chạy VBHN Engine tái hợp nhất | 🔴 Cần Cẩn Trọng |
| **🛡️ Phụ Lục Nội Bộ** | **3** | Ma trận đối chiếu VBHN nội bộ CCBA | Bảo tồn nguyên trạng (Internal Document) | 🟢 Không Áp Dụng |

---

## 2. Danh Sách Chi Tiết Hàng Đợi 38 Văn Bản

| STT | Số Hiệu / ID | Thể Loại | Nhóm Di Trú | Trạng Thái Gate 15 | Đặc Tính (Math / Table / Fig) | Hành Động Đề Xuất |
| :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| 1 | `22/2023/QH15` | Luật | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 2 | `55/2024/QH15` | Luật | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 3 | `135/2025/QH15` | Luật | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 4 | `105/2025/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 5 | `193/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 6 | `206/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 7 | `207/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | 3 CSV/3 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 8 | `209/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 9 | `210/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 10 | `212/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 11 | `217/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | 1 CSV/1 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 12 | `24/2024/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 13 | `101/2026/TT-BQP` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 14 | `32/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 15 | `33/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 16 | `34/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 17 | `36/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 18 | `37/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | 2 CSV/2 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 19 | `38/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | 3 CSV/3 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 20 | `39/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 21 | `40/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 22 | `41/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 23 | `73/2026/TT-BTC` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 24 | `79/2026/TT-BTC` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 25 | `QCVN 01:2021/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ⏳ CHƯA CẤP DẤU | 32 CSV/32 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 26 | `QCVN 02:2022/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ⏳ CHƯA CẤP DẤU | 49 CSV/49 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 27 | `QCVN 03:2022/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 3 CSV/3 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 28 | `QCVN 04:2021/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔷 Nhóm C (Consolidated Shield) | ⏳ CHƯA CẤP DẤU | Văn bản thuần túy | Bảo vệ Snapshot -> Tái hợp nhất qua VBHN Engine |
| 29 | `QCVN 06:2022/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔷 Nhóm C (Consolidated Shield) | ⏳ CHƯA CẤP DẤU | 64 CSV/64 JSON | Bảo vệ Snapshot -> Tái hợp nhất qua VBHN Engine |
| 30 | `QCVN 09:2017/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ⏳ CHƯA CẤP DẤU | 9 CSV/9 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 31 | `TCVN 2737:2023` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ⏳ CHƯA CẤP DẤU | 29 KaTeX, 37 CSV/37 JSON, 44 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 32 | `TCVN 3890:2023` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ⏳ CHƯA CẤP DẤU | 11 CSV/11 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 33 | `TCVN 5574:2018` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ⏳ CHƯA CẤP DẤU | 230 KaTeX, 32 CSV/32 JSON, 40 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 34 | `TCVN 5738:2021` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ⏳ CHƯA CẤP DẤU | 5 CSV/5 JSON, 3 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 35 | `TCVN 7336:2021` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ⏳ CHƯA CẤP DẤU | 10 CSV/10 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 36 | `APPENDIX-XD-2025-2014` | Phụ lục đối chiếu | 🛡️ Phụ Lục Nội Bộ | 🛡️ INTERNAL | Văn bản thuần túy | Bảo tồn nguyên vẹn (Internal Comparison Matrix) |
| 37 | `APPENDIX-SD-2023-QCVN-06` | Phụ lục đối chiếu | 🛡️ Phụ Lục Nội Bộ | 🛡️ INTERNAL | Văn bản thuần túy | Bảo tồn nguyên vẹn (Internal Comparison Matrix) |
| 38 | `APPENDIX-SD-2026-QCVN-04` | Phụ lục đối chiếu | 🛡️ Phụ Lục Nội Bộ | 🛡️ INTERNAL | Văn bản thuần túy | Bảo tồn nguyên vẹn (Internal Comparison Matrix) |

---

## 3. Quy Trình Vận Hành Di Trú (Operational SOP)

```mermaid
flowchart LR
    Queue[Hàng Đợi Di Trú] --> TierA[Nhóm A: Clean Passthrough]
    Queue --> TierB[Nhóm B: Compartment Refresh]
    Queue --> TierC[Nhóm C: Consolidated Shield]

    TierA --> AuditA[Đối soát Gate 1-11] --> StampA[Attest okf_spec: v2.4 Universal]
    TierB --> SurgB[Phẫu thuật tables/ & figures/] --> AuditB[Gate 12-14] --> StampB[Cấp tem sau nghiệm thu]
    TierC --> SnapC[Snapshot Shield .bak/] --> EngineC[VBHN Consolidate] --> DiffC[Verify Parity] --> StampC[Cấp tem an toàn]
```

### 3.1 Hướng Dẫn Di Trú Từng Nhóm
- **Xử lý Nhóm A (Văn bản thuần túy):**
  1. Chạy lệnh: `python scripts/spoke_cli.py validate` để chắc chắn 15 gates xanh.
  2. Cấp dấu Provenance chính thức vào `metadata.yaml` ghi nhận đúng phiên bản bóc tách.
- **Xử lý Nhóm B (Quy chuẩn/Tiêu chuẩn kỹ thuật):**
  1. Không ghi đè toàn bộ bundle.
  2. Tái tạo `tables/` bằng `TableKnowledgeExtractor` (ADR 0041).
  3. Đồng bộ `figures/cards/` bằng `FigureExtractor` (ADR 0040).
  4. Xác nhận Gate 12, Gate 13, Gate 14 đạt $100\%$ trước khi cấp dấu.
- **Xử lý Nhóm C (Văn bản Hợp nhất VBHN):**
  1. Sao lưu dự phòng `bang_so_sanh_thay_doi.md` và `patch_manifest.yaml`.
  2. Thực thi VBHN Engine tái hợp nhất từ `sources/*_goc.md` và `sources/sua_doi_*.md`.
  3. Đối chiếu diff bảo toàn toàn diện trước khi cấp dấu.
