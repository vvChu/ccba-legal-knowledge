---
okf_version: '2.2'
type: legal_comparative_matrix
title: Bảng So sánh Đối chiếu Sửa đổi 01:2026 QCVN 04:2021/BXD (Thông tư 31/2026/TT-BXD)
description: Tài liệu Phụ lục đối chiếu quy định chính quy trong hệ thống tri thức
  xây dựng CCBA.
tags:
- xay_dung
- phap_ly
timestamp: '2026-11-22T00:00:00Z'
resource: legal_docs/04_appendices/bang_so_sanh_sua_doi_2026/bang_so_sanh_sua_doi_2026.md
id: bang_so_sanh_sua_doi_2026
doc_id: bang_so_sanh_sua_doi_2026
document_number: APPENDIX-SD-2026-QCVN-04
document_type: Phụ lục đối chiếu
issued_by: CCBA Legal Research Group
signer: ''
issued_date: '2026-06-15'
effective_date: '2026-12-15'
status: pending_effective
pdf_anchor:
  path: ./bang_so_sanh_sua_doi_2026.pdf
  cong_bao_number: Đang cập nhật
relations:
- target_id: QCVN 04:2021/BXD
  relation_type: compares
- target_id: 31/2026/TT-BXD
  relation_type: compares
---

# BẢNG SO SÁNH ĐỐI CHIẾU SỬA ĐỔI 01:2026 QCVN 04:2021/BXD

*(Căn cứ Thông tư 31/2026/TT-BXD ngày 15/06/2026 của Bộ Xây dựng — Hiệu lực thi hành từ ngày 15/12/2026)*

> [!WARNING]
> **Trạng thái hiệu lực (`pending_effective`):** Thông tư 31/2026/TT-BXD và Sửa đổi 01:2026 QCVN 04:2021/BXD chỉ có hiệu lực thi hành từ ngày **`15/12/2026`**. Áp dụng Cổng Kiểm toán Ân hạn Động theo [ADR 0013](../../../docs/adr/0013-dynamic-grace-period-compliance-gate.md):
> - **Trước `2026-12-15`:** Chưa có hiệu lực $\rightarrow$ chỉ đưa ra thông báo khuyến nghị chuẩn bị (*Advisory Note*), áp dụng quy chuẩn gốc 2021.
> - **Từ `2026-12-15` đến `2027-06-15`:** Giai đoạn ân hạn **06 tháng** đối với khu vực để xe điện, sạc xe điện, đổi pin tại nhà chung cư hiện hữu theo Khoản 2 Điều 2 Thông tư 31/2026/TT-BXD (*Warning Notice*).
> - **Sau `2027-06-15`:** Hết ân hạn $\rightarrow$ bắt buộc tuân thủ toàn diện (*Critical Defect*).

---

## 1. BẢNG MA TRẬN ĐỐI CHIẾU THAY ĐỔI KỸ THUẬT

| STT | Điều Khoản | QCVN 04:2021/BXD (Bản Gốc) | Sửa Đổi 01:2026 QCVN 04:2021/BXD (TT 31/2026/TT-BXD) | Phân Loại Lỗi Kiểm Toán | Hướng Dẫn Hành Động & Thẩm Tra |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | **[Mục 1.1.3](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-1-1-3)**<br>*Phạm vi áp dụng chỗ để xe, xe điện, đổi pin* | Chỉ quy định phạm vi chung tại 1.1.1 và 1.1.2 cho xây mới, xây lại; chưa có quy định riêng cho xe điện tại chung cư hiện hữu. | **Bổ sung điểm 1.1.3:** Các quy định liên quan đến chỗ để xe, chỗ để xe điện và khu vực đổi pin áp dụng đối với **nhà chung cư xây mới và nhà chung cư hiện hữu** (Mục 3.1 và 3.2 giữ nguyên). | 🔴 **Critical Defect**<br>(Từ `15/12/2026`; chung cư hiện hữu theo lộ trình ADR-0013) | Xác định loại công trình (`new_build` hoặc `existing_building`) khi kiểm tra các hạng mục chỗ để xe, khu để xe điện, khu sạc và tủ đổi pin. |
| **2** | **[Mục 1.3](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-1-3)**<br>*Tài liệu viện dẫn* | Chưa viện dẫn QCVN 10:2025/BCA. | **Bổ sung vào cuối điểm 1.3:** Viện dẫn **QCVN 10:2025/BCA**, *Quy chuẩn kỹ thuật quốc gia về trang bị, bố trí phương tiện phòng cháy, chữa cháy, cứu nạn, cứu hộ cho nhà và công trình*. | 🟡 **Warning Notice**<br>(Cảnh Báo Tuân Thủ) | Đối soát danh mục quy chuẩn viện dẫn trong thuyết minh PCCC/MEP; áp dụng song song QCVN 06:2022/BXD (SĐ 1:2023) và QCVN 10:2025/BCA cho khu vực xe điện. |
| **3** | **[Mục 1.4.31–1.4.34](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-1-4-31)**<br>*Giải thích từ ngữ mới* | Dừng ở điểm 1.4.30 (*Tài liệu chuẩn*). | **Bổ sung 4 thuật ngữ:** `1.4.31` Nhà chung cư hiện hữu; `1.4.32` Khu vực sạc xe điện; `1.4.33` Chỗ sạc; `1.4.34` Khu vực đổi pin (dành cho xe mô tô điện, xe gắn máy điện, xe đạp điện). | 🔵 **Informative**<br>(Định Nghĩa Pháp Lý) | Phân biệt rõ "khu vực để xe điện" (`2.10.1`), "khu vực sạc xe điện" (`2.10.2`) và "khu vực đổi pin" (`2.11`) trước khi áp ngưỡng khoang cháy và PCCC. |
| **4** | **[Mục 2.2.17](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-2-2-17)**<br>*Chỗ để xe* | Điểm 2.2.17 ghi: *"Chỗ để xe (bao gồm xe ô tô, xe máy (kể cả xe máy điện), xe đạp)."* Các điểm 2.2.17.1–2.2.17.3 quy định định mức diện tích. | **Sửa đổi điểm 2.2.17 thành:** *"2.2.17 Chỗ để xe"*. Các điểm `2.2.17.1`, `2.2.17.2`, `2.2.17.3` giữ nguyên; toàn bộ quy định kỹ thuật cho xe điện chuyển sang Mục 2.10. | 🟡 **Warning Notice**<br>(Cảnh Báo Tham Chiếu) | Không gộp lẫn yêu cầu PCCC/phân vùng xe điện vào 2.2.17.1–2.2.17.3; kiểm tra định mức diện tích theo 2.2.17 và yêu cầu kỹ thuật xe điện theo 2.10. |
| **5** | **[Mục 2.10](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-2-10) & [Mục 2.11](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-2-11)**<br>*Chỗ để xe điện, khu vực sạc & khu vực đổi pin* | Chưa có Mục 2.10 và Mục 2.11. | **Bổ sung mới Mục 2.10 & 2.11:**<br>1. **Ưu tiên bố trí:** ngoài trời $\to$ mặt đất $\to$ bán hầm $\to$ hầm 1 (tầng hầm phải có giải pháp giải phóng hoặc cô lập xe/tủ pin cháy).<br>2. **Phân vùng (`2.10.1`, `2.10.2`):** tách ô tô điện với xe 2 bánh điện; cách $\ge 2\text{ m}$ hoặc tường/vách không cháy cao $\ge 2\text{ m}$. Phân vùng sạc tối đa `25` ô tô / `50` xe máy điện tại hầm; `30` ô tô / `80` xe máy điện tại tầng nổi.<br>3. **Khoang cháy & PCCC khu sạc:** bố trí thành khoang cháy riêng (`1.500/1.200 m2` cho ô tô hoặc hỗn hợp; `500/300 m2` cho xe máy điện; ngăn bằng tường ngăn cháy loại 1, khoảng trống $\ge 6\text{ m}$ hoặc màn nước drencher 2 dải $\ge 1\text{ l/s}\cdot\text{m}$ duy trì $\ge 1\text{ giờ}$); bắt buộc báo cháy tự động, chữa cháy tự động, camera 24/24, cảnh báo khí **CO** & **HF**, hút khói theo Phụ lục D QCVN 06.<br>4. **Điện & trụ sạc:** cấp điện tách biệt, tự ngắt theo báo cháy/chữa cháy và **ngắt điện khẩn cấp (EPO)**, trụ sạc tầng hầm $\le 22\text{ kW}$, chống va chạm & ngập nước.<br>5. **Khu vực đổi pin (`2.11`):** cách $\ge 3\text{ m}$ (ngoài trời) / $\ge 6\text{ m}$ (trong nhà tới cầu thang/sảnh/lối thoát nạn, giảm $\ge 1\text{ m}$ nếu vách `EI 60`), hút xả khói cưỡng bức, camera 24/24, tổng dung lượng $\le 100\text{ kWh}$ (ngoài nhà hoặc tổng phân tán trong nhà), $\le 35\text{ kWh}$/phân vùng tầng nổi, $\le 18\text{ kWh}$/phân vùng bán hầm hoặc hầm 1. | 🔴 **Critical Defect**<br>(Lỗi Đỏ khi có hiệu lực) | Thẩm tra đồng bộ kiến trúc (phân vùng, khoang cháy, khoảng cách `2 m` / `6 m` / `10 m`), MEP (cấp điện riêng, EPO, trụ $\le 22\text{ kW}$, cảm biến CO/HF, hút khói) và PCCC (chữa cháy tự động, drencher, giải pháp cô lập/giải phóng xe cháy ở hầm). |
| **6** | **[Mục 3.3](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-3-3), [3.4](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-3-4), [3.5](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-3-5)**<br>*Quy định chuyển tiếp & quản lý vận hành* | Mục 3.1 (xây mới), 3.2 (khuyến khích khi cải tạo chung cư cũ), 3.3 (chuyển tiếp chung cho dự án phê duyệt trước ngày QCVN có hiệu lực). | **Giữ nguyên 3.1 và 3.2.** Bổ sung cuối `3.3` về chuyển tiếp PCCC khu vực xe điện/sạc/đổi pin (đã thẩm định/thẩm duyệt có khu vực xe điện trước hiệu lực thì tiếp tục thực hiện; chưa có phải rà soát tuân thủ; sau hiệu lực phải tuân thủ). Bổ sung `3.4` (trách nhiệm CĐT/chủ sở hữu/BQT/đơn vị vận hành) và `3.5` (giám sát 24/24 giờ). Thời hạn rà soát **06 tháng** cho chung cư hiện hữu đến `15/06/2027` quy định tại **Khoản 2 Điều 2 Thông tư 31/2026/TT-BXD**. | 🔴 **Critical Defect**<br>(Theo mốc ADR-0013) | Kiểm tra hồ sơ thẩm định/thẩm duyệt PCCC theo 3 trường hợp tại `3.3`, phương án giám sát 24/24 tại `3.5` và áp dụng thời hạn ân hạn đến `15/06/2027` cho chung cư hiện hữu. |
| **7** | **[Mục 4.1a](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-4-1a), [4.1b](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-4-1b), [4.3](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd.md#muc-4-3)**<br>*Trách nhiệm của tổ chức, cá nhân* | Mục 4.1, 4.2, 4.3 (vướng mắc gửi về Vụ KHCN&MT - Bộ Xây dựng). | **Bổ sung `4.1a`** (tổ chức/cá nhân lắp đặt, quản lý, vận hành khu để/sạc/đổi pin phải tuân thủ QCVN); **bổ sung `4.1b`** (cơ quan PCCC có thẩm quyền kiểm tra tuân thủ); **sửa `4.3`** (mọi ý kiến vướng mắc gửi về **Bộ Xây dựng**). | 🔵 **Informative**<br>(Phân Định Trách Nhiệm) | Gắn đúng thẩm quyền kiểm tra cho cơ quan PCCC (`4.1b`) và đầu mối hướng dẫn là Bộ Xây dựng (`4.3`). |

---

## 2. QUY TRÌNH KIỂM TOÁN TỰ ĐỘNG CHO AGENT QC

1. **Cổng Thời Gian Hiệu Lực (ADR-0013 Gate):**
   - Kiểm tra `audit_date`: nếu `audit_date < 2026-12-15` $\rightarrow$ phát hành *Advisory Note* (`pending_effective`), chưa áp lỗi bắt buộc theo TT 31/2026/TT-BXD.
   - Nếu `2026-12-15 <= audit_date <= 2027-06-15` và `building_status == 'existing'` $\rightarrow$ phát hành *Warning Notice* kèm hạn chót rà soát `2027-06-15` theo Khoản 2 Điều 2 Thông tư 31/2026/TT-BXD.
   - Nếu `audit_date >= 2026-12-15` (công trình xây mới hoặc hồ sơ thẩm định sau ngày hiệu lực) hoặc `audit_date > 2027-06-15` $\rightarrow$ áp dụng cưỡng chế *Critical Defect*.
2. **Kiểm toán Khu Vực Để Xe Điện & Khu Vực Sạc (`Mục 2.10`):**
   - Đối soát kiến trúc: vị trí ưu tiên, tách phân vùng ô tô điện / xe máy điện, khoảng cách $\ge 2\text{ m}$ (hoặc vách không cháy $\ge 2\text{ m}$), số chỗ sạc/phân vùng ($\le 25/50$ hầm, $\le 30/80$ nổi) và diện tích khoang cháy ($1.500/1.200/500/300\text{ m}^2$).
   - Đối soát MEP & PCCC: báo cháy + chữa cháy tự động, camera 24/24, cảm biến **CO/HF**, nút ngắt điện khẩn cấp (**EPO**), trụ sạc tầng hầm $\le 22\text{ kW}$, giải pháp cô lập/giải phóng xe cháy và hút khói theo Phụ lục D QCVN 06.
3. **Kiểm toán Khu Vực Đổi Pin (`Mục 2.11`) & Quản Lý Vận Hành (`Mục 3.3–3.5`):**
   - Kiểm tra khoảng cách an toàn ($3\text{ m}$ ngoài trời / $6\text{ m}$ trong nhà hoặc vách `EI 60` $\ge 1\text{ m}$), hút xả khói cưỡng bức và giới hạn dung lượng ($100 / 35 / 18\text{ kWh}$).
   - Đối soát hồ sơ PCCC đã thẩm định/thẩm duyệt theo 3 nhánh chuyển tiếp tại `Mục 3.3` và xác nhận quy trình giám sát `24/24 giờ` tại `Mục 3.5`.
