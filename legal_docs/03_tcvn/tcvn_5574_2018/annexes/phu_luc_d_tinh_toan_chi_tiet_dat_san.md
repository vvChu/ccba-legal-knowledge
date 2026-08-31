
<a id="phu-luc-d"></a>
## PHỤ LỤC D  (Tham khảo)  TÍNH TOÁN CHI TIẾT ĐẶT SẴN


<a id="muc-d-1"></a>
### D.1  Các thanh neo hàn thẳng góc vào các bản thép phẳng của chi tiết đặt sẵn, chịu tác dụng của mô men uốn, lực thẳng góc với chúng và lực trượt do tải trọng tĩnh nằm trong mặt phẳng đối xứng của chi tiết đặt sẵn (Hình D.1) cần được tính toán theo điều kiện:


<a id="hinh-d_1"></a>

<p align="center">

![Hình D.1](../figures/images/hinh_d_1.png)

</p>

<p align="center"><strong>Hình D.1 — Sơ đồ nội lực tác dụng lên chi tiết đặt sẵn</strong></p>


$$\frac{Q_{an,j}}{Q_{an,j,0}} + \frac{N_{an,j}}{N_{an,j,0}} \le 1 \tag{D.1}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_D_1" -->

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $N_{an,j}$  là lực kéo lớn nhất trong một hàng thanh neo, bằng:


$$N_{\text{an}, j} = \frac{M}{z} + \frac{N}{n_{\text{an}}}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_D_2" -->

&nbsp;&nbsp;&nbsp;&nbsp;\- $Q_{an,j}$  là lực trượt lớn nhất trong một hàng thanh neo, bằng:


$$Q_{\text{an},j} = \frac{Q - 0,3N'_{\text{an}}}{n_{\text{an}}}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_D_3" -->

&nbsp;&nbsp;&nbsp;&nbsp;\- $N'_{\text{an}}$  là lực nén lớn nhất trong một hàng thanh neo, được xác định theo công thức:


$$N'_{\text{an}} = \frac{M}{z} - \frac{N}{n_{\text{an}}}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_D_4" -->

&nbsp;&nbsp;&nbsp;&nbsp;\- $Q_{an,j,0}$  là lực trượt chịu bởi tất cả các thanh neo, được xác định theo công thức:


$$Q_{an,j,0} = \gamma_{s,sh} A_{an,j} \sqrt{R_b R_s}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_D_5" -->

&nbsp;&nbsp;&nbsp;&nbsp;\- trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $\gamma_{s,sh}$  là hệ số, lấy bằng 1,65;

&nbsp;&nbsp;&nbsp;&nbsp;\- $N_{an,j,0}$  là lực kéo giới hạn chịu bởi một hàng thanh neo, được xác định theo công thức:


<a id="formula-d_6"></a>
$$N_{an,j,0} = R_{s}A_{an,j} \tag{D.6}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_D_6" -->

Trong các công thức từ (D.1) đến (D.6):

M, N, Q  lần lượt là mô men uốn, lực dọc và lực trượt tác dụng lên chi tiết đặt sẵn; mô men uốn được xác định đối với trục nằm trên mặt phẳng chứa mép ngoài của bản và đi qua trọng tâm của tất cả các thanh neo;

$n_{an}$  là số hàng thanh neo dọc theo hướng lực trượt; nếu không đảm bảo truyền lực trượt Q đều lên tất cả các thanh neo thì khi xác định lực trượt $ Q_{an}$ chỉ kể đến không quá 4 hàng neo;

z  là khoảng cách giữa các hàng thanh neo ngoài cùng;

$A_{an,j}$  là tổng diện tích tiết diện ngang của các thanh neo trong hàng neo chịu lực lớn nhất;

Diện tích tiết diện các thanh neo của các hàng neo còn lại lấy bằng diện tích tiết diện các thanh neo của hàng neo chịu lực lớn nhất.

Trong các công thức (D.2) và (D.4), lực thẳng góc N được coi là dương nếu nó hướng từ chi tiết đặt sẵn ra ngoài (Hình D.1) và là âm nếu nó hướng vào chi tiết đặt sẵn. Trong trường hợp, nếu lực N có giá trị âm thì trong công thức (D.3) lấy $N'_{\text{an}}$ = N.

Khi bố trí các chi tiết đặt sẵn ở mặt trên (khi đổ bê tông) của cấu kiện thì lấy $N'_{\text{an}}$ = 0.


<a id="muc-d-2"></a>
### D.2  Trong các chi tiết đặt sẵn có các thanh neo được hàn xiên với một góc từ 15 ° đến 30 ° thì các thanh neo xiên này được tính chịu lực trượt (khi Q > N, với N là lực giật đứt) theo công thức:


$$A_{an,inc} = \frac{Q - 0,3 N'_{an}}{R_s}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_D_7" -->

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $A_{an,inc}$  là tổng diện tích tiết diện của các thanh neo xiên;

&nbsp;&nbsp;&nbsp;&nbsp;\- $N'_{\text{an}}$ - xem 8.1.2.1.1.

Khi đó cần bố trí thêm các thanh neo thẳng góc. Các thanh neo này được tính theo công thức (D.1) và với giá trị $Q_{an}$ lấy bằng 0,1 lần giá trị lực trượt được xác định theo công thức (D.3).


<a id="muc-d-3"></a>
### D.3  Cấu tạo của các chi tiết đặt sẵn bằng thép với các chi tiết hàn vào chúng để truyền tải trọng lên các chi tiết đặt sẵn cần đảm bảo cho các thanh neo làm việc theo sơ đồ tính toán đã lựa chọn. Các chi tiết bên ngoài của các chi tiết đặt sẵn và các liên kết hàn của chúng được tính theo TCVN 5575:2012.

Khi tính toán các bản táp và bản mã chịu lực giật thì coi như chúng liên kết khớp với các thanh neo thẳng góc. Ngoài ra, chiều dày bản của chi tiết đặt sẵn được hàn với các thanh neo thẳng góc.

Ngoài ra, chiều dày bản táp t của chi tiết đặt sẵn được hàn táp với các thanh neo cần được kiểm tra theo điều kiện:


<a id="formula-d_8"></a>
$$t \ge 0,25 d_{an} \frac{R_s}{f_v} \tag{D.8}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_D_8" -->

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $d_{an}$  là đường kính yêu cầu của thanh neo theo tính toán;

&nbsp;&nbsp;&nbsp;&nbsp;\- $f_{v}$  là cường độ chịu cắt tính toán của bản thép, lấy theo TCVN 5575:2012.

&nbsp;&nbsp;&nbsp;&nbsp;\- Trong trường hợp sử dụng các kiểu liên kết hàn để tăng vùng làm việc của bản táp khi các thanh neo bị kéo giật ra khỏi bản và khi có luận chứng thích hợp thì có thể điều chỉnh điều kiện (D.8) với mục đích giảm chiều dày của bản táp.

&nbsp;&nbsp;&nbsp;&nbsp;\- Chiều dày bản táp cũng cần thoả mãn các yêu cầu về công nghệ hàn.

