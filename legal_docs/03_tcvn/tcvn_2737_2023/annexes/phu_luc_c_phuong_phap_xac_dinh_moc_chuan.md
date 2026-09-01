<a id="phu-luc-c"></a>
## PHỤ LỤC C  (Quy định)  PHƯƠNG PHÁP XÁC ĐỊNH MỐC CHUẨN


<a id="muc-c-1"></a>
**C.1**  Khi xác định hệ số $k(z_e)$ theo công thức (12), nếu mặt đất xung quanh nhà và công trình không bằng phẳng thì độ cao tương đương $z_e$ được xác định thông qua độ cao $z$ (xem [10.2.4](../tcvn_2737_2023.md#muc-10-2-4)) và $z$ được xác định như sau:

a) Trường hợp mặt đất có độ dốc nhỏ so với phương nằm ngang $i \le 0{,}3$, độ cao $z$ được tính từ mặt đất (mốc chuẩn) đặt nhà và công trình tới điểm cần xét.

b) Trường hợp mặt đất có độ dốc $0{,}3 < i < 2$, độ cao $z$ được tính từ mặt cao độ công trình quy ước $z_0$ (mốc chuẩn) (xem [Hình C.1a](#hinh-c_1a)) thấp hơn so với mặt đất thực tới điểm cần xét.

c) Trường hợp mặt đất có độ dốc lớn $i \ge 2$, mặt cao độ công trình quy ước $z_0$ (mốc chuẩn) để tính độ cao $z$ thấp hơn mặt đất thực được xác định theo [Hình C.1b](#hinh-c_1b).


<a id="hinh-c_1"></a><a id="hinh-c_1a"></a>

<p align="center">

![Hình C.1a](../figures/images/hinh_c_1a.png)

</p>

_CHÚ THÍCH:_ Bên trái điểm A: $z_0 = z_1$; Trên đoạn BC: $z_0 = \frac{H(2 - i)}{1{,}7}$; Bên phải điểm D: $z_0 = z_2$; Trên đoạn AB và CD: $z_0$ được xác định bằng nội suy tuyến tính.

<p align="center"><strong>a) Khi mặt đất có độ dốc 0,3 &lt; i &lt; 2</strong></p>


<a id="hinh-c_1b"></a>

<p align="center">

![Hình C.1b](../figures/images/hinh_c_1b.png)

</p>

_CHÚ THÍCH:_ Bên trái điểm C: $z_0 = z_1$; Bên phải điểm D: $z_0 = z_2$; Trên đoạn CD: $z_0$ được xác định bằng nội suy tuyến tính.

<p align="center"><strong>b) Khi mặt đất có độ dốc i &ge; 2</strong></p>

<p align="center"><strong>Hình C.1 — Mặt cao độ công trình quy ước $z_0$ (mốc chuẩn)</strong></p>

> [!NOTE]
> **Đặc tả Hình học & Phương pháp Xác định Mốc chuẩn Khí động ($z_0$):**
> \- **Phạm vi áp dụng:** Xác định mặt cao độ công trình quy ước $z_0$ (mốc chuẩn) khi địa hình xung quanh nhà/công trình không bằng phẳng (đồi, dốc, vách đứng) để tính độ cao tương đương $z_e$ theo công thức (12).
> \- **Tham chiếu Visual Card:** [`fig_c_1_benchmark_datum.json`](../figures/cards/fig_c_1_benchmark_datum.json)
> \- **Bộ giải tính toán (Python Solver):** `calc_topography_datum_z0` trong `formulas/wind_load_tcvn2737.py`.

