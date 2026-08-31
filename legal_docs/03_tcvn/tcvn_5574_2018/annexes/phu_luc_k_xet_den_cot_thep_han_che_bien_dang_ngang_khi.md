
<a id="phu-luc-k"></a>
## PHỤ LỤC K  (Tham khảo)  XÉT ĐẾN CỐT THÉP HẠN CHẾ BIẾN DẠNG NGANG KHI TÍNH TOÁN CÁC CẤU KIỆN CHỊU NÉN LỆCH TÂM THEO MÔ HÌNH BIẾN DẠNG PHI TUYẾN


<a id="muc-k-1"></a>
### K.1  Tính toán chịu nén lệch tâm cho các cấu kiện dạng thanh làm từ bê tông nặng hoặc bê tông hạt nhỏ với cốt thép hạn chế biến dạng ngang theo mô hình biến dạng phi tuyến cần được tiến hành theo các chỉ dẫn trong 8.1.2.7.1 đến 8.1.2.7.11 và các chỉ dẫn bổ sung trong K.2 đến K.4.


<a id="muc-k-2"></a>
### K.2  Các đặc trưng độ cứng $D_{ij}$ (i, j = 1, 2, 3) trong các phương trình từ (72) đến (74) để xác định biến dạng của bê tông và cốt thép trong tiết diện thẳng góc của các cấu kiện có cốt thép hạn chế biến dạng ngang cần được xác định theo các công thức:


$$D_{11} = \sum_i A_{bi} Z_{bni}^2 E_b v_{bi} + \sum_j A_{bj} Z_{snj}^2 E_{sj} v_{sj} + \sum_k A_{bk} Z_{bnk}^2 E_b v_{bk} \tag{K.1}
D_{22} = \sum_i A_{bi} Z_{byi}^2 E_b v_{bi} + \sum_j A_{bj} Z_{syj}^2 E_{sj} v_{sj} + \sum_k A_{bk} Z_{byk}^2 E_b v_{bk} \tag{K.2}
D_{12} = \sum_i A_{bi} Z_{bni} Z_{byi} E_b v_{bi} + \sum_j A_{bj} Z_{snj} Z_{syj} E_{sj} v_{sj} + \sum_k A_{bk} Z_{bnk} Z_{byk} E_b v_{bk} \tag{K.3}
D_{13} = \sum_i A_{bi} Z_{bni} E_b v_{bi} + \sum_j A_{bj} Z_{snj} E_{sj} v_{sj} + \sum_k A_{bk} Z_{bnk} E_b v_{bk} \tag{K.4}
D_{23} = \sum_i A_{bi} Z_{byi} E_b v_{bi} + \sum_j A_{bj} Z_{syj} E_{sj} v_{sj} + \sum_k A_{bk} Z_{byk} E_b v_{bk} \tag{K.5}
D_{33} = \sum_i A_{bi} E_b v_{bi} + \sum_j A_{bj} E_{sj} v_{sj} + \sum_k A_{bk} E_b v_{bk} \tag{K.6}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_K_1" -->

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $A_{bk}$, $Z_{bxk}$, $Z_{byk}$  lần lượt là diện tích, các tọa độ trọng tâm vùng bê tông chịu nén thứ k có cốt thép hạn chế biến dạng ngang;

&nbsp;&nbsp;&nbsp;&nbsp;\- $v_{bk}$  là hệ số đàn hồi của bê tông vùng thứ k có cốt thép hạn chế biến dạng ngang;

&nbsp;&nbsp;&nbsp;&nbsp;\- Các ký hiệu khác xem trong 8.1.2.7.4.

Trong các công thức từ (K.1) đến (K.6) cho phép lấy $A_{bi}$ = 0.


<a id="muc-k-3"></a>
### K.3  Giá trị hệ số $v_{bk}$ lấy theo biểu đồ biến dạng khi nén dọc trục của bê tông có cốt thép hạn chế biến dạng ngang.

Khi sử dụng biểu đồ hai đoạn thẳng hoặc ba đoạn thẳng thì giá trị hệ số $v_{bk}$  được xác định bằng cách sử dụng các quan hệ từ (9) đến (13) mà trong đó thay vì các đặc trưng của bê tông $R_{b}$, $\epsilon_{b0}$ và $\epsilon_{b2}$ cần sử dụng các đặc trưng của bê tông có cốt thép hạn chế biến dạng ngang $R_{b,red}$, $\epsilon_{b0,red}$ và $\epsilon_{b2,red}$:


$$R_{b,red} = R_b + \varphi \mu_{xy}R_{s,xy} \tag{K.7}
\varepsilon_{b0,red} = \varepsilon_{b0} + 0,02 \alpha_{red} \tag{K.8}
\varepsilon_{b2,red} = \varepsilon_{b2}\frac{\varepsilon_{b0,red}}{\varepsilon_{b0}} \tag{K.9}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_K_7" -->

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $R_{s,xy}$ là cường độ tính toán của cốt thép lưới gia cường;


$$\mu_{s,xy} = \frac{n_x A_{sx} L_x + n_y A_{sy} L_y}{A_{ef} s} \tag{K.10}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_K_10" -->

trong đó:

&nbsp;&nbsp;&nbsp;&nbsp;\- $n_{x}$, $A_{sx}$, $L_{x}$  lần lượt là số thanh thép, diện tích tiết diện ngang và chiều dài lưới thép (đo theo trục các thanh ngoài cùng) theo một phương;

&nbsp;&nbsp;&nbsp;&nbsp;\- $n_{x}$, $A_{sy}$, $L_{y}$  lần lượt là số thanh thép, diện tích tiết diện ngang và chiều dài lưới thép (đo theo trục các thanh ngoài cùng) theo phương kia;


$$\varphi = \frac{1}{0,23 + \alpha_{red}} \tag{K.11}
\alpha_{red} = \frac{\mu_{xy} R_{s,xy}}{R_b + 10} \tag{K.12}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_K_11" -->

$R_{s,xy}$ và $R_{b}$ tính bằng megapascan (MPa).


<a id="muc-k-4"></a>
### K.4  Khi sử dụng biểu đồ đường cong biến dạng thì giá trị hệ số $v_{bk}$ cần được xác định bằng cách sử dụng các quan hệ từ (K.2) đến (K.8) mà trong đó thay vì các đặc trưng của bê tông $\hat{\sigma}_b \text{ và } \hat{\varepsilon}_b$ cần sử dụng các đặc trưng của bê tông có cốt thép hạn chế biến dạng ngang $R_{b,red}$, $\epsilon_{b0,red}$ và $\epsilon_{b2,red}$, còn giá trị hệ số $v_{0}$ đối với nhánh xuống của biểu đồ nén dọc trục của bê tông lấy bằng giá trị tính được theo công thức:


<a id="formula-k_13"></a>
$$v_0 = \frac{R_b}{R_{b,red}} \tag{K.13}$$
<!-- formula_id: "F_TCVN_5574_2018_FORMULA_K_13" -->

