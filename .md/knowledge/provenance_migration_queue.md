# Hàng Đợi Di Trú & Kiểm Toán Nguồn Gốc Tri Thức (OKF v2.4 Universal Provenance Queue)

> [!IMPORTANT]
> **Tài liệu kiểm toán nguồn gốc độc lập của CCBA Legal Spoke (Gate 15 ADR 0036 - ADR 0042).**
> Tuyệt đối không chạy script đóng dấu khống (False Attestation). Mọi việc cấp tem `okf_spec: v2.4 Universal`
> bắt buộc phải tuân theo Chiến lược Di trú Phân tầng (Tiered Migration Protocol).

- **Thời điểm quét:** `2026-11-05 10:34:16 UTC`
- **Tiêu chuẩn chuẩn hóa:** `v2.4 Universal` (Converter: `0.4.0`)
- **Quy mô kho tài liệu:** **106 văn bản** (103 gói tri thức chính quy + 3 ma trận đối chiếu)
- **Tiến độ cấp tem bảo chứng:** **103 / 103** (100.0%)

---

## 1. Ma Trận Phân Hạng Chiến Lược Di Trú (Strategy Matrix)

| Nhóm Phân Loại | Số Lượng | Bản Chất Dữ Liệu | Chiến Lược Di Trú Đề Xuất | Mức Độ Rủi Ro |
| :--- | :---: | :--- | :--- | :---: |
| **🟢 Nhóm A (Clean Passthrough)** | **37** | Luật, Nghị định, Thông tư thuần túy; bảng biểu mẫu phẳng | Chạy kiểm toán Gate 1-11, cấp tem Attestation có bảo chứng | 🟢 Rất Thấp |
| **🔶 Nhóm B (Compartment Refresh)** | **59** | QCVN/TCVN kỹ thuật dày đặc bảng số liệu 2D, KaTeX, đồ họa | Phẫu thuật cục bộ ngăn kéo `tables/` và `figures/cards/` | 🟡 Trung Bình |
| **🔷 Nhóm C (Consolidated Shield)** | **7** | Văn bản Hợp nhất VBHN có `bang_so_sanh_thay_doi.md` | Snapshot bảo vệ -> Chạy VBHN Engine tái hợp nhất | 🔴 Cần Cẩn Trọng |
| **🛡️ Phụ Lục Nội Bộ** | **3** | Ma trận đối chiếu VBHN nội bộ CCBA | Bảo tồn nguyên trạng (Internal Document) | 🟢 Không Áp Dụng |

---

## 2. Danh Sách Chi Tiết Hàng Đợi 106 Văn Bản

| STT | Số Hiệu / ID | Thể Loại | Nhóm Di Trú | Trạng Thái Gate 15 | Đặc Tính (Math / Table / Fig) | Hành Động Đề Xuất |
| :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| 1 | `10/2021/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 2 | `14/VBHN-BGDĐT` | Văn bản hợp nhất | 🔷 Nhóm C (Consolidated Shield) | ✅ VERIFIED | 4 CSV/4 JSON | Bảo vệ Snapshot -> Tái hợp nhất qua VBHN Engine |
| 3 | `83/VBHN-TT-BXD` | Văn bản hợp nhất | 🔷 Nhóm C (Consolidated Shield) | ✅ VERIFIED | 3 CSV/3 JSON | Bảo vệ Snapshot -> Tái hợp nhất qua VBHN Engine |
| 4 | `57/2024/QH15` | Luật | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 7 CSV/7 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 5 | `90/2025/QH15` | Luật | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 2 CSV/2 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 6 | `31/2024/QH15` | Luật | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 2 CSV/2 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 7 | `22/2023/QH15` | Luật | 🔷 Nhóm C (Consolidated Shield) | ✅ VERIFIED | Văn bản thuần túy | Bảo vệ Snapshot -> Tái hợp nhất qua VBHN Engine |
| 8 | `40/2019/QH14` | Luật | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 9 | `27/2023/QH15` | Luật | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 1 CSV/1 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 10 | `55/2024/QH15` | Luật | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 11 | `47/2024/QH15` | Luật | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 12 | `135/2025/QH15` | Luật | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 13 | `105/2025/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 14 | `115/2024/NĐ-CP` | Nghị định | 🔷 Nhóm C (Consolidated Shield) | ✅ VERIFIED | Văn bản thuần túy | Bảo vệ Snapshot -> Tái hợp nhất qua VBHN Engine |
| 15 | `17/2025/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 16 | `193/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 5 CSV/5 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 17 | `206/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 18 | `207/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 3 CSV/3 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 19 | `209/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 20 | `210/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 21 | `212/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 3 CSV/3 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 22 | `214/2025/NĐ-CP` | Nghị định | 🔷 Nhóm C (Consolidated Shield) | ✅ VERIFIED | Văn bản thuần túy | Bảo vệ Snapshot -> Tái hợp nhất qua VBHN Engine |
| 23 | `217/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 1 CSV/1 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 24 | `225/2025/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 25 | `23/2024/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 26 | `24/2024/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 27 | `339/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 28 | `349/2026/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 29 | `85/2020/NĐ-CP` | Nghị định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 30 | `1812/QĐ-BXD` | Quyết định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 1 CSV/1 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 31 | `02/2024/TT-BKHĐT` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 4 CSV/4 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 32 | `03/2020/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 2 CSV/2 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 33 | `03/2024/TT-BKHĐT` | Thông tư | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 44 CSV/44 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 34 | `05/2024/TT-BKHĐT` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 4 CSV/4 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 35 | `06/2021/TT-BXD` | Thông tư | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 6 CSV/6 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 36 | `07/2024/TT-BKHĐT` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 1 CSV/1 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 37 | `08/2021/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 4 CSV/4 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 38 | `101/2026/TT-BQP` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 39 | `105/2025/TT-BTC` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 40 | `32/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 1 CSV/1 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 41 | `33/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 42 | `34/2026/TT-BXD` | Thông tư | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 6 CSV/6 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 43 | `36/2026/TT-BXD` | Thông tư | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 51 CSV/51 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 44 | `37/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 2 CSV/2 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 45 | `38/2026/TT-BXD` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | 3 CSV/3 JSON | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 46 | `39/2026/TT-BXD` | Thông tư | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 8 CSV/8 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 47 | `40/2026/TT-BXD` | Thông tư | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 11 CSV/11 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 48 | `41/2026/TT-BXD` | Thông tư | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 6 CSV/6 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 49 | `73/2026/TT-BTC` | Thông tư | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 20 CSV/20 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 50 | `79/2025/TT-BTC` | Thông tư | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 8 CSV/8 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 51 | `79/2026/TT-BTC` | Thông tư | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 23 CSV/23 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 52 | `98/2025/TT-BTC` | Thông tư | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 53 | `38/2026/QĐ-UBND` | Quyết định | 🟢 Nhóm A (Clean Passthrough) | ✅ VERIFIED | Văn bản thuần túy | Attestation hợp chuẩn sau khi đối soát Gate 1-11 |
| 54 | `QCVN 01:2020/BCT` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 6 CSV/6 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 55 | `QCVN 01:2021/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 32 CSV/32 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 56 | `QCVN 02:2020/BCA` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 6 CSV/6 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 57 | `QCVN 02:2022/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 49 CSV/49 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 58 | `QCVN 03:2022/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 3 CSV/3 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 59 | `QCVN 03:2023/BCA` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 7 CSV/7 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 60 | `QCVN 04:2021/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔷 Nhóm C (Consolidated Shield) | ✅ VERIFIED | Văn bản thuần túy | Bảo vệ Snapshot -> Tái hợp nhất qua VBHN Engine |
| 61 | `QCVN 06:2022/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔷 Nhóm C (Consolidated Shield) | ✅ VERIFIED | 64 CSV/64 JSON | Bảo vệ Snapshot -> Tái hợp nhất qua VBHN Engine |
| 62 | `QCVN 07:2023/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 1 KaTeX, 25 CSV/25 JSON, 2 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 63 | `QCVN 09:2017/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 9 CSV/9 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 64 | `QCVN 10:2024/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 2 CSV/2 JSON, 25 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 65 | `QCVN 10:2025/BCA` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 19 CSV/19 JSON, 2 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 66 | `QCVN 12:2014/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 6 KaTeX, 17 CSV/17 JSON, 14 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 67 | `QCVN 13:2018/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 9 CSV/9 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 68 | `QCVN 16:2023/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 24 CSV/24 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 69 | `QCVN 18:2021/BXD` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 2 CSV/2 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 70 | `QCVN 26:2025/BNNMT` | Quy chuẩn kỹ thuật quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 6 CSV/6 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 71 | `TCCS 39:2022/TCĐBVN` | Tiêu chuẩn cơ sở | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 13 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 72 | `TCCS 41:2022/TCĐBVN` | Tiêu chuẩn cơ sở | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 22 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 73 | `TCVN 10304:2014` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 54 KaTeX, 26 CSV/26 JSON, 5 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 74 | `TCVN 13456:2022` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 1 CSV/1 JSON, 8 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 75 | `TCVN 13967:2024` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 1 KaTeX, 20 CSV/20 JSON, 31 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 76 | `TCVN 14176-2:2024` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 1 CSV/1 JSON, 4 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 77 | `TCVN 2737:2023` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 29 KaTeX, 37 CSV/37 JSON, 44 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 78 | `TCVN 3890:2023` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 11 CSV/11 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 79 | `TCVN 3981:1985` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 22 CSV/22 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 80 | `TCVN 4470:2012` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 39 CSV/39 JSON, 34 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 81 | `TCVN 4474:1987` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 9 KaTeX, 11 CSV/11 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 82 | `TCVN 4513:1988` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 9 KaTeX, 21 CSV/21 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 83 | `TCVN 4601:2012` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 10 CSV/10 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 84 | `TCVN 5065:1990` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 3 CSV/3 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 85 | `TCVN 5574:2018` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 230 KaTeX, 32 CSV/32 JSON, 40 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 86 | `TCVN 5575:2024` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 261 KaTeX, 107 CSV/107 JSON, 48 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 87 | `TCVN 5687:2024` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 3 KaTeX, 17 CSV/17 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 88 | `TCVN 5738:2021` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 5 CSV/5 JSON, 3 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 89 | `TCVN 6379:2024` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 2 CSV/2 JSON, 5 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 90 | `TCVN 7114-1:2008` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | Văn bản thuần túy | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 91 | `TCVN 7161-1:2022` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 33 KaTeX, 18 CSV/18 JSON, 14 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 92 | `TCVN 7336:2021` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 10 CSV/10 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 93 | `TCVN 7568-14:2025` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 2 CSV/2 JSON, 10 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 94 | `TCVN 8793:2011` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 3 CSV/3 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 95 | `TCVN 9361:2012` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 4 KaTeX, 32 CSV/32 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 96 | `TCVN 9362:2012` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 39 KaTeX, 38 CSV/38 JSON, 7 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 97 | `TCVN 9377-1:2012` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 4 CSV/4 JSON | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 98 | `TCVN 9381:2012` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 11 KaTeX, 6 CSV/6 JSON, 7 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 99 | `TCVN 9385:2012` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 14 KaTeX, 25 CSV/25 JSON, 60 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 100 | `TCVN 9386:2025` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 158 KaTeX, 27 CSV/27 JSON, 45 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 101 | `TCVN 9411:2012` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 3 CSV/3 JSON, 7 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 102 | `TCVN ISO 19650-1:2021` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 1 CSV/1 JSON, 14 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 103 | `TCVN ISO 19650-2:2021` | Tiêu chuẩn quốc gia | 🔶 Nhóm B (Compartment Refresh) | ✅ VERIFIED | 2 CSV/2 JSON, 12 Cards | Phẫu thuật cục bộ ngăn kéo tables/ và figures/ |
| 104 | `APPENDIX-XD-2025-2014` | Phụ lục đối chiếu | 🛡️ Phụ Lục Nội Bộ | 🛡️ INTERNAL | Văn bản thuần túy | Bảo tồn nguyên vẹn (Internal Comparison Matrix) |
| 105 | `APPENDIX-SD-2023-QCVN-06` | Phụ lục đối chiếu | 🛡️ Phụ Lục Nội Bộ | 🛡️ INTERNAL | Văn bản thuần túy | Bảo tồn nguyên vẹn (Internal Comparison Matrix) |
| 106 | `APPENDIX-SD-2026-QCVN-04` | Phụ lục đối chiếu | 🛡️ Phụ Lục Nội Bộ | 🛡️ INTERNAL | Văn bản thuần túy | Bảo tồn nguyên vẹn (Internal Comparison Matrix) |

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
