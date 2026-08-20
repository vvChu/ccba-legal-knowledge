# BẢNG SO SÁNH ĐỐI CHIẾU SỬA ĐỔI 01:2026 QCVN 04:2021/BXD

*(Căn cứ Thông tư 31/2026/TT-BXD ngày 15/06/2026 của Bộ Xây dựng — Hiệu lực thi hành từ ngày 15/12/2026)*

---

## 1. BẢNG MA TRẬN ĐỐI CHIẾU THAY ĐỔI KỸ THUẬT

| STT | Điều Khoản | QCVN 04:2021/BXD (Bản Gốc) | Sửa Đổi 01:2026 QCVN 04:2021/BXD (TT 31/2026) | Phân Loại Lỗi Kiểm Toán | Hướng Dẫn Hành Động & Thẩm Tra |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | **[Mục 2.2.17](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd_hop_nhat_2026.md#muc-2-2-17)**<br>*Chỗ để xe & Trạm sạc xe điện* | Chỉ quy định chung chỗ để xe ô tô, xe máy, xe đạp; chưa quy định khu vực xe điện, trạm sạc và trạm đổi pin. | Bổ sung quy định bắt buộc:<br>1. Tách biệt khu vực xe điện.<br>2. Phân vùng PCCC riêng biệt theo **QCVN 10:2025/BCA**.<br>3. Bố trí ngắt điện khẩn cấp và chữa cháy chuyên dụng pin Lithium-ion. | 🔴 **Critical Defect**<br>(Lỗi Đỏ) | Bản vẽ MEP và PCCC bắt buộc phải thể hiện sơ đồ ngắt điện tự động khẩn cấp và hệ thống dập lửa chuyên dụng khu sạc xe điện tại tầng hầm/gara. |
| **2** | **[Mục 2.3.1](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd_hop_nhat_2026.md#muc-2-3-1)**<br>*Tải trọng kết cấu khu vực sạc/gara* | Chỉ yêu cầu tính toán an toàn chịu lực tổng quát theo tiêu chuẩn tải trọng truyền thống. | Bổ sung điểm d): Bắt buộc tính toán tải trọng tĩnh và tải trọng động bổ sung của phương tiện giao thông điện và cụm trạm sạc tập trung. | 🔴 **Critical Defect**<br>(Lỗi Đỏ) | Thuyết minh kết cấu phải có bảng tính tải trọng tập trung của xe điện và thiết bị trạm đổi pin tại vị trí đặt thiết bị. |
| **3** | **[Mục 2.5.3](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd_hop_nhat_2026.md#muc-2-5-3)**<br>*Viện dẫn quy chuẩn PCCC* | Viện dẫn QCVN 06:2021/BXD cũ. | Cập nhật viện dẫn trực tiếp quy chuẩn an toàn cháy mới nhất và **QCVN 10:2025/BCA** về trang bị phương tiện PCCC và CNCH. | 🟡 **Warning Notice**<br>(Cảnh Báo Tuân Thủ) | Rà soát danh mục tiêu chuẩn viện dẫn trong hồ sơ thuyết minh thiết kế kỹ thuật, cập nhật QCVN 10:2025/BCA. |
| **4** | **[Mục 3.1](../../02_qcvn/qcvn_04_2021_bxd/qcvn_04_2021_bxd_hop_nhat_2026.md#muc-3-1)**<br>*Phạm vi áp dụng công trình* | Chỉ bắt buộc áp dụng khi xây dựng mới, xây dựng lại; khuyến khích áp dụng khi cải tạo chung cư cũ. | Bắt buộc áp dụng đối với cả **công trình cải tạo, sửa chữa** có ảnh hưởng đến công năng, kết cấu hoặc an toàn PCCC. | 🔴 **Critical Defect**<br>(Lỗi Đỏ) | Các dự án cải tạo chuyển đổi công năng tầng đế/hầm bắt buộc phải thẩm duyệt lại PCCC theo quy chuẩn sửa đổi. |

---

## 2. QUY TRÌNH KIỂM TOÁN TỰ ĐỘNG CHO AGENT QC

1. **Kiểm toán Chỗ để xe điện (Mục 2.2.17):**
   - Quét bản vẽ Mặt bằng Kiến trúc Tầng hầm $\rightarrow$ Xác định vị trí phân vùng khu đỗ xe máy điện/ô tô điện.
   - Đối soát bản vẽ Cấp điện $\rightarrow$ Kiểm tra nút ngắt nguồn khẩn cấp (Emergency Power Off - EPO) tại phòng trực điều khiển và ngoài lối vào khu sạc.
   - Đối soát bản vẽ PCCC $\rightarrow$ Kiểm tra đầu phun sprinkler / bình bọt chữa cháy chuyên dụng cho pin Lithium.

2. **Kiểm toán Hồ sơ Cải tạo (Mục 3.1):**
   - Nếu `project_type == 'renovation'` và có thay đổi công năng tầng hầm $\rightarrow$ Kích hoạt Gate cưỡng chế tuân thủ Sửa đổi 01:2026.