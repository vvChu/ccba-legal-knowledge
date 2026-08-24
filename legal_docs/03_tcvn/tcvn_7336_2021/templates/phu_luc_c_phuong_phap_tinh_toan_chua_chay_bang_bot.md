---
title: "Phụ lục C (Tham khảo): Phương pháp tính toán các thông số của hệ thống chữa cháy bằng bọt bội số nở cao"
document: "TCVN 7336:2021"
appendix: "Phụ lục C"
type: "calculation_method"
usage: "Phương pháp tính toán các thông số của hệ thống chữa cháy bằng bọt bội số nở cao"
---

# Phụ lục C
### (Tham khảo)
## Phương pháp tính toán các thông số của hệ thống chữa cháy bằng bọt bội số nở cao

> [!NOTE]
> **Tiêu chuẩn viện dẫn:** Tiêu chuẩn Quốc gia TCVN 7336:2021.  
> **Mỏ neo PDF (PDF Anchor):** [`tcvn_7336_2021.pdf`](../tcvn_7336_2021.pdf).

---

### C.1 Thể tích tính toán của không gian bảo vệ ($V$)
Phải xác định thể tích tính toán $V\text{ (m}^3\text{)}$ của không gian được bảo vệ hoặc thể tích chữa cháy cục bộ. Thể tích tính toán của gian phòng được xác định bởi diện tích sàn và chiều cao của gian phòng khi chứa đầy bọt, ngoại trừ thể tích của các cấu kiện chống cháy (không thấm nước) của nhà (cột, dầm, móng, v.v.).

### C.2 Hiệu suất thiết bị tạo bọt ($q$)
Với chủng loại và nhãn hiệu của thiết bị tạo bọt bội số nở cao đã lựa chọn, hiệu suất của chúng được xác định dựa trên đặc tính dung dịch chất tạo bọt $q\text{ (l/min)}$.

### C.3 Số lượng thiết bị tạo bọt bội số nở cao ($N$)
Số lượng thiết bị tạo bọt bội số nở cao được tính theo công thức:
$$N = \frac{V \cdot a}{q \cdot K \cdot \tau}$$

Trong đó:
- $V$: Thể tích tính toán của không gian được bảo vệ $(\text{m}^3)$;
- $K$: Bội số nở của bọt (lấy theo thông số kỹ thuật của thiết bị tạo bọt);
- $\tau$: Thời gian tối đa để lấp đầy không gian được bảo vệ bằng bọt (min, $\tau \le 10\text{ min}$);
- $a$: Hệ số phá hủy bọt do tác động nhiệt và môi trường.

Giá trị của hệ số $a$ được tính theo công thức:
$$a = a_1 \cdot a_2 \cdot a_3$$

Trong đó:
- $a_1$: Hệ số độ co của bọt, lấy bằng $1,2$ với chiều cao phòng lên tới $4\text{ m}$ và $1,5$ với chiều cao phòng lên tới $10\text{ m}$; với chiều cao phòng trên $10\text{ m}$ được xác định bằng thử nghiệm;
- $a_2$: Hệ số tính đến rò rỉ bọt, trong trường hợp không có lỗ mở lấy bằng $1,2$, khi có các lỗ mở được xác định bằng thực nghiệm;
- $a_3$: Hệ số tính đến ảnh hưởng của khói, khí cháy đến sự phá hủy bọt; đối với sản phẩm cháy của chất lỏng hydrocarbon lấy bằng $1,5$, đối với các loại chất cháy khác được xác định bằng thực nghiệm.

> [!IMPORTANT]
> Thời gian tối đa để lấp đầy thể tích của không gian được bảo vệ bằng bọt không được vượt quá $10\text{ min}$.

### C.4 Lưu lượng dung dịch chất tạo bọt cần thiết ($Q_b$)
Xác định lưu lượng dung dịch chất tạo bọt cần thiết của toàn hệ thống $(\text{m}^3/\text{s})$:
$$Q_b = \frac{N \cdot q}{60 \cdot 1000}$$

### C.5 Nồng độ thể tích của dung dịch chất tạo bọt ($c$)
Nồng độ thể tích của dung dịch chất tạo bọt lấy theo tài liệu kỹ thuật của nhà sản xuất $c\text{ (\%)}$.

### C.6 Lượng chất tạo bọt cô đặc tính toán ($V_{ctb}$)
Lượng chất tạo bọt cô đặc tính toán được xác định $(\text{m}^3)$:
$$V_{ctb} = V_{dd} \cdot \frac{c}{100}$$
Trong đó:
- $V_{dd}$: Tổng lượng dung dịch chất tạo bọt cần thiết cho thời gian chữa cháy $(\text{m}^3)$;
- $c$: Nồng độ chất tạo bọt $(\%)$.
