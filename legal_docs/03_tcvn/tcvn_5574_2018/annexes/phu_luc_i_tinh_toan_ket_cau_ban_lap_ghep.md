
<a id="phu-luc-i"></a>
## PHỤ LỤC I  (Tham khảo)  TÍNH TOÁN KẾT CẤU BÁN LẮP GHÉP


<a id="muc-i-1"></a>
### I.1  Kết cấu bán lắp ghép bao gồm các cấu kiện bê tông cốt thép lắp ghép, bê tông liền khối đổ tại chỗ, và cốt thép.

Để sử dụng làm các cấu kiện lắp ghép thường sử dụng các cấu kiện bê tông cốt thép không ứng suất trước hoặc ứng suất trước của các kết cấu lắp ghép được thiết kế riêng hoặc thiết kế điển hình.


<a id="muc-i-2"></a>
### I.2  Kết cấu bê tông cốt thép bán lắp ghép cần phải thỏa mãn các yêu cầu tính toán về khả năng chịu lực (các trạng thái giới hạn thứ nhất) và về khả năng sử dụng bình thường (các trạng thái giới hạn thứ hai).

Kết cấu bán lắp ghép cần được tính toán về độ bền, sự hình thành và mở rộng vết nứt và về biến dạng đối với các giai đoạn làm việc sau đây của kết cấu:

&nbsp;&nbsp;\- Trước khi bê tông đổ tại chỗ (bê tông đổ bù) đạt cường độ định trước - chịu tác dụng của khối lượng bê tông này và các tải trọng khác tác dụng trong giai đoạn thi công này của kết cấu

&nbsp;&nbsp;\- Sau khi bê tông đổ tại chỗ (bê tông đổ bù) đạt cường độ định trước - chịu các tải trọng tác dụng trong quá trình thi công và khi sử dụng kết cấu.

Tính toán kết cấu bản lắp ghép sau khi bê tông đổ bù đạt cường độ định trước phải được tiến hành có kể đến ứng suất và biến dạng ban đầu xuất hiện trong các cấu kiện lắp ghép trước khi bê tông đổ bù đạt cường độ định trước.


<a id="muc-i-3"></a>
### I.3  Việc liên kết chắc chắn giữa bê tông đổ bù và bê tông của các cấu kiện lắp ghép nén được thực hiện bằng cốt thép chờ từ các cấu kiện lắp ghép, bằng cách bố trí các chốt bê tông hoặc tạo bề mặt nhám, bố trí các cốt thép dọc chờ, hoặc bằng các biện pháp tin cậy khác đã được kiểm chứng.

Tính toán độ bền các mối nối tiếp xúc do tác dụng của các lực trượt, kéo, nén giữa cấu kiện lắp ghép và bê tông liền khối được tiến hành theo I.4 đến I.8.


<a id="muc-i-4"></a>
### I.4  Tính toán chịu kéo cho các mối nối tiếp xúc không cốt thép nên được tiến hành theo điều kiện:


$$N_j \le \gamma_{bt,j} R_{bt} A_{b,j} \tag{I.1}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_I_1" -->

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $\gamma_{bt,j}$  là hệ số, lấy bằng 0,25 đối với các mối nối được gia công và bằng 0 đối với các mối nối không được gia công.

Tính toán chịu kéo cho các mối nối tiếp xúc có cốt thép nên được tiến hành theo điều kiện:


<a id="formula-i_2"></a>
$$N_{j} \le R_{s}A_{s,j} \tag{I.2}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_I_2" -->


<a id="muc-i-5"></a>
### I.5  Tính toán chống trượt cho các mối nối tiếp xúc không cốt thép nên được tiến hành theo điều kiện:


<a id="formula-i_3"></a>
$$Q_{j} \le _{b,sh,j}R_{bt}A_{b,j} \tag{I.3}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_I_3" -->

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $\gamma_{b,sh,j}$ là hệ số, lấy bằng 0,5 đối với các mối nối không được gia công và bằng 1,0 đối với các mối nối được gia công.

Tính toán chống trượt cho các mối nối tiếp xúc có cốt thép nén được tiến hành theo điều kiện:


$$Q_j \le \gamma_{b,sh,j} R_{bt} A_{b,j} \left(1 + \gamma_{sb,sh,j} R_{s,j} \mu_{s,j}\right) \tag{I.4}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_I_4" -->

nhưng không lớn hơn $\gamma_{b,sh,lim}R_{bt}A_{b,j}$ ,

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $\gamma_{b,sh,j}$  là hệ số, lấy như trong điều kiện (I.3);

&nbsp;&nbsp;&nbsp;&nbsp;\- $\gamma_{sb,sh,j}$ là hệ số, lấy bằng 1,0, tính bằng một trên megapascan ($MPa^{-1}$);

&nbsp;&nbsp;&nbsp;&nbsp;\- $\gamma_{b,sh,lim}$ là hệ số, lấy bằng 2,0;

&nbsp;&nbsp;&nbsp;&nbsp;\- µ$_{s,j}$ là hàm lượng cốt thép trong mối nối tiếp xúc, $\mu_{s,j}$=$\frac{h_{i,j}}{h_{b,j}}$ .


<a id="muc-i-6"></a>
### I.6  Tính toán mối nối tiếp xúc chịu tác dụng đồng thời của các lực trượt và lực kéo được tiến hành theo điều kiện:


<a id="formula-i_5"></a>
$$\frac{Q_j}{Q_{j,0}} + \frac{N_j}{N_{j,0}} \le 1 \tag{I.5}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_I_5" -->

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $N_{j,0}$  lấy bằng vế phải của các điều kiện (I.1) vá (I.2);

&nbsp;&nbsp;&nbsp;&nbsp;\- $Q_{j,0}$  lấy bằng vế phải của các điều kiện (I.3) và (I.4).


<a id="muc-i-7"></a>
### I.7  Tính toán chịu nén cho các mối nối tiếp xúc không cốt thép được tiến hành theo điều kiện:


<a id="formula-i_6"></a>
$$N_{j} \le R_{b}A_{b,j} \tag{I.6}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_I_6" -->

Tính toán chịu nén cho các mối nối tiếp xúc có cốt thép nên được tiến hành theo điều kiện:


<a id="formula-i_7"></a>
$$N_{j} \le R_{b}A_{b,j} + R_{sc}A_{s,j} \tag{I.7}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_I_7" -->


<a id="muc-i-8"></a>
### I.8  Tính toán mối nối tiếp xúc chịu tác dụng đồng thời của các lực trượt và lực nén được tiến hành theo các điều kiện:


$$Khi 0 \le \frac{N_j}{N_{j,0}} \le 0,4 :
Q_j \le Q_{b,j,0} + \gamma_{jn} N_j \tag{I.8}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_I_8" -->


$$Khi 0,4 < \frac{N_j}{N_{j,0}} < 0,6 :
Q_j \le Q_{b,j,0} + 0,4 \gamma_{jw} N_{j,0} \tag{I.9}
Khi 0,6 \le \frac{N_j}{N_{j,0}} \le 1,0 :
Q_j \le Q_{b,j,0} + \gamma_{jw}\left(N_{j,0} - N_j\right) \tag{I.10}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_I_9" -->

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $N_{j,0}$  lấy bằng vế phải của các điều kiện (I.6) và (I.7);

&nbsp;&nbsp;&nbsp;&nbsp;\- $Q_{b,j,0}$  lấy bằng vế phải của các điều kiện (I.3) và (I.4);

&nbsp;&nbsp;&nbsp;&nbsp;\- $\gamma_{jw}$  lấy bằng 1,0, còn đối với các trường hợp đặc biệt mà yêu cầu phải có thực nghiệm thì lấy trực tiếp theo số liệu nghiên cứu thực nghiệm.

