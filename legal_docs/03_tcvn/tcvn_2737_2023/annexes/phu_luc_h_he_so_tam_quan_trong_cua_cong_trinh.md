<a id="phu-luc-h"></a>
## PHỤ LỤC H  (Quy định)  HỆ SỐ TẦM QUAN TRỌNG CỦA CÔNG TRÌNH


<a id="muc-h-1"></a>

**H.1**  Tùy thuộc vào cấp hậu quả của công trình, khi thiết kế cần sử dụng hệ số độ tin cậy về tầm quan trọng của công trình $\gamma_n$.


<a id="muc-h-2"></a>

**H.2**  Việc phân cấp hậu quả của công trình theo [QCVN 03:2022/BXD] phụ thuộc vào công năng sử dụng, cũng như hậu quả về xã hội, môi trường và kinh tế do sự hư hỏng và phá hoại của nó gây ra.


<a id="muc-h-3"></a>

**H.3**  Hệ số tầm quan trọng của công trình $\gamma_n$ được lấy theo Bảng H.1 khi tính toán theo trạng thái giới hạn thứ nhất và lấy bằng $1{,}0$ khi tính toán theo trạng thái giới hạn thứ hai.


<a id="bang-bang-h-1"></a>

**Bảng H.1 — Giá trị tối thiểu của hệ số tầm quan trọng $\gamma_n$**

| Cấp hậu quả của công trình | Mức độ quan trọng của công trình | Giá trị $\gamma_n$ |
| :---: | :--- | :---: |
| C1 | Thấp | $0{,}87$ |
| C2 | Trung bình | $1{,}00$ |
| C3 | Cao | $1{,}15$ |

_CHÚ THÍCH:_ Đối với nhà cao trên $250\text{ m}$ và mái nhịp lớn (không có trụ trung gian) với nhịp lớn hơn $120\text{ m}$ thì hệ số $\gamma_n$ lấy không nhỏ hơn $1{,}2$.

> [!NOTE]
> **Quy Chuẩn Viện Dẫn & Bộ Giải Hệ Số $\gamma_n$:**
> \- **Căn cứ phân cấp hậu quả:** QCVN 03:2022/BXD (Quy chuẩn kỹ thuật quốc gia về Phân cấp công trình phục vụ thiết kế xây dựng).
> \- **Bộ giải tính toán (Python Solver):** `calc_importance_factor_gamma_n` trong `formulas/deflection_limits_tcvn2737.py`.

### Thư mục tài liệu tham khảo

[1] QCVN 02:2022/BXD, *Quy chuẩn kỹ thuật quốc gia về Số liệu điều kiện tự nhiên dùng trong xây dựng*.

[2] QCVN 03:2022/BXD, *Quy chuẩn kỹ thuật quốc gia về Phân cấp công trình phục vụ thiết kế xây dựng*.

[3] TCVN 2737:1995, *Tải trọng và tác động - Tiêu chuẩn thiết kế*.

[4] TCVN 5574:2018, *Thiết kế kết cấu bê tông và bê tông cốt thép*.

[5] BS EN 1990, *Basis of structural design (Cơ sở thiết kế kết cấu)*.

[6] BS EN 1991, *Actions on Structures (Tác động lên kết cấu)*.

[7] ASCE/SEI 7-16, *Minimum design loads and associated criteria for buildings and other structures*.

[8] GOST 27751-2014, *Độ tin cậy của kết cấu xây dựng và nền. Yêu cầu chung*.

[9] SP 20.13330.2016, *Tải trọng và tác động (Phiên bản cập nhật SNiP 2.01.07-85\*)*.

[10] SP 267.1325800.2016, *Nhà và tổ hợp cao tầng. Nguyên tắc thiết kế*.

[11] SP 296.1325800.2017, *Nhà và công trình. Tác động đặc biệt*.
