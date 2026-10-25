
<a id="phu-luc-d"></a>
## PHỤ LỤC D (Tham khảo) — Ví dụ tính toán

Trên cơ sở số liệu khảo sát của một công trình với các số liệu dưới đây, xác định mức độ nguy hiểm của công trình.

Xác định số cấu kiện nguy hiểm trong tổng số cấu kiện theo kết quả khảo sát:

Tổng số móng: 34Số móng nguy hiểm: 12

Tổng số cột: 180Số cột nguy hiểm: 36

Tổng số dầm chính: 60Số dầm chính nguy hiểm: 12

Tổng số dầm phụ: 80Số dầm phụ nguy hiểm: 16

Tổng số đoạn tường: 80Số dầm phụ nguy hiểm: 16

Tổng số bản sàn: 50Số dầm phụ nguy hiểm: 10

Xác định tỷ số phần trăm nguy hiểm nhất của các bộ phận nhà theo các công thức (1), (2) và (3):

Tỷ số phần trăm cấu kiện nguy hiểm trong nền móng là:


$$r_{fdm} = \frac{12}{34}x100\% = 35\%$$
<!-- formula_id: "F_TCVN_9381_2012_RID102" -->

Tỷ số phần trăm cấu kiện nguy hiểm trong kết cấu chịu lực là:


$$r_{sdm} = \frac{(2,4x36 + 2,4x16 + 1,9x12 + 1,4x16 + 10)}{(2,4x180 + 2,4x80 + 1,9x60 + 1,4x80 + 50)}x100\% = 20\%$$
<!-- formula_id: "F_TCVN_9381_2012_RID104" -->

Tỷ số phần trăm cấu kiện nguy hiểm trong kết cấu bao che:


$$r_{esdm} = \frac{20}{80}x100\% = 25\%$$
<!-- formula_id: "F_TCVN_9381_2012_RID106" -->

Xác định hàm phụ thuộc của các bộ phận nhà theo các cấp a, b, c, d theo các công thức tổng quát (4), (5), (6) và (7). Đối với từng bộ phận nhà cụ thể: móng, kết cấu chịu lực, kết cấu bao che là $_{af}$, $_{as}$, $_{aes}$... (ký hiệu xem các công thức từ (8) đến (11).

Cấp a: $_{af}$ = 0; $_{as}$ = 0; $_{aes}$ = 0

Cấp b: $_{bf}$ = 0; $_{bs}$ = (30 - 20)/25 = 0,4; $_{bes}$ = (30 - 25)/25 = 0,2

Cấp c: $_{cf}$ = (100 - 35)/70 = 0,93; $_{cs}$ = (20 - 5)/25 = 0,6; $_{ces}$ = (25-5)/25 = 0,8

Cấp d: $_{df}$ = (35-30)/70 = 0,07; $_{ds}$ = 0; $_{des}$ = 0

Hàm phụ thuộc của nhà theo các cấp A, B, C, D xác định theo các công thức (8), (9), (10) và (11):

$m_{A}$ = max[min(0,3;0) min(0,6;0) min(0,1;0)] = max(0;0;0) = 0

$m_{B}$ = max[min(0,3;0) min(0,6;0,4) min(0,1;0,2)] = max(0;0,4;0,1) = 0,4

$m_{C}$ = max[min(0,3;0,93) min(0,6;0,6) min(0,1;0,8)] = max(0,3;0,6;0,1) = 0,6

$m_{D}$ = max[min(0,3;0,07) min(0,6;0) min(0,1;0)] = max(0,07;0;0) = 0,07

Đánh giá mức độ nguy hiểm của toàn nhà.

max[$m_{A}$, $m_{B}$, $m_{C}$, $m_{D}$] = max(0; 0,4; 0,6; 0,07) = 0,6 = $m_{C}$

Kết luận: Nhà có bộ phận nguy hiểm.

MỤC LỤC


<a id="phu-luc-d-muc-1"></a>
## 1  PHẠM VI ÁP DỤNG


<a id="phu-luc-d-muc-2"></a>
## 2  TÀI LIỆU VIỆN DẪN


<a id="phu-luc-d-muc-3"></a>
## 3  KÝ HIỆU


<a id="phu-luc-d-muc-4"></a>
## 4  TRÌNH TỰ ĐÁNH GIÁ MỨC ĐỘ NGUY HIỂM CỦA NHÀ


<a id="muc-4-1"></a>
### 4.1  Nội dung và phạm vi đánh giá


<a id="muc-4-2"></a>
### 4.2  Khảo sát sơ bộ


<a id="muc-4-3"></a>
### 4.3  Khảo sát chi tiết


<a id="muc-4-4"></a>
### 4.4  Phân tích, đánh giá


<a id="muc-4-5"></a>
### 4.5  Lập báo cáo


<a id="phu-luc-d-muc-5"></a>
## 5  PHƯƠNG PHÁP ĐÁNH GIÁ


<a id="muc-5-1"></a>
### 5.1  Nguyên tắc đánh giá tổng hợp


<a id="muc-5-2"></a>
### 5.2  Đánh giá mức độ nguy hiểm của cấu kiện


<a id="muc-5-2-1"></a>
### 5.2.1  Nguyên tắc chung


<a id="muc-5-2-2"></a>
### 5.2.2  Đáng giá nền móng


<a id="muc-5-2-3"></a>
### 5.2.3  Đánh giá cấu kiện kết cấu xây gạch


<a id="muc-5-2-4"></a>
### 5.2.4  Đánh giá cấu kiện kết cấu gỗ


<a id="muc-5-2-5"></a>
### 5.2.5  Đánh giá cấu kiện kết cấu bê tông cốt thép


<a id="muc-5-2-6"></a>
### 5.2.6  Đánh giá cấu kiện kết cấu thép


<a id="muc-5-3"></a>
### 5.3  Đánh giá mức độ nguy hiểm của nhà


<a id="muc-5-3-1"></a>
### 5.3.1  Nguyên tắc đánh giá chung


<a id="muc-5-3-2"></a>
### 5.3.2  Phân cấp nguy hiểm của nhà


<a id="muc-5-3-3"></a>
### 5.3.3  Nguyên tắc đánh giá tổng hợp


<a id="muc-5-3-4"></a>
### 5.3.4  Phương pháp đánh giá tổng hợp