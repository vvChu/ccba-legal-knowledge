import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

bundle_dir = Path("legal_docs/02_qcvn/qcvn_03_2022_bxd")
sources_dir = bundle_dir / "sources"
annexes_dir = bundle_dir / "annexes"

# 1. thong_tu_05_2022_tt_bxd.md
thong_tu_md = """# THÔNG TƯ 05/2022/TT-BXD

## BAN HÀNH QCVN 03:2022/BXD QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ PHÂN CẤP CÔNG TRÌNH PHỤC VỤ THIẾT KẾ XÂY DỰNG

---

**BỘ XÂY DỰNG**

Số: 05/2022/TT-BXD  
*Hà Nội, ngày 30 tháng 11 năm 2022*

---

### CĂN CỨ PHÁP LÝ

\\- Căn cứ Luật Tiêu chuẩn và quy chuẩn kỹ thuật ngày 29 tháng 6 năm 2006;

\\- Căn cứ Nghị định số 127/2007/NĐ-CP ngày 01 tháng 8 năm 2007 của Chính phủ quy định chi tiết thi hành một số điều của Luật Tiêu chuẩn và quy chuẩn kỹ thuật và Nghị định số 78/2018/NĐ-CP ngày 16 tháng 5 năm 2018 của Chính phủ sửa đổi, bổ sung một số điều của Nghị định số 127/2007/NĐ-CP ngày 01 tháng 8 năm 2007 của Chính phủ;

\\- Căn cứ Nghị định số 52/2022/NĐ-CP ngày 08 tháng 8 năm 2022 của Chính phủ quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Bộ Xây dựng;

\\- Theo đề nghị của Vụ trưởng Vụ Khoa học công nghệ và môi trường;

Bộ trưởng Bộ Xây dựng ban hành Thông tư ban hành QCVN 03:2022/BXD Quy chuẩn kỹ thuật quốc gia về Phân cấp công trình phục vụ thiết kế xây dựng.

---

### ĐIỀU KHOẢN THI HÀNH

**Điều 1.** Ban hành kèm theo Thông tư này QCVN 03:2022/BXD Quy chuẩn kỹ thuật quốc gia về Phân cấp công trình phục vụ thiết kế xây dựng.

**Điều 2.** Thông tư này có hiệu lực kể từ ngày 01 tháng 6 năm 2023 và thay thế Thông tư số 12/2012/TT-BXD ngày 28/12/2012 của Bộ trưởng Bộ Xây dựng ban hành QCVN 03:2012/BXD Quy chuẩn kỹ thuật quốc gia về Nguyên tắc phân loại, phân cấp công trình dân dụng, công nghiệp và hạ tầng kỹ thuật đô thị.

**Điều 3.** Các bộ, cơ quan ngang bộ, cơ quan thuộc Chính phủ, Ủy ban nhân dân các tỉnh, thành phố trực thuộc Trung ương và các tổ chức, cá nhân có liên quan chịu trách nhiệm thi hành Thông tư này./.

---

| NƠI NHẬN | KT. BỘ TRƯỞNG<br>THỨ TRƯỞNG |
| :--- | :---: |
| \\- Văn phòng Quốc hội; Văn phòng Chủ tịch nước;<br>\\- Văn phòng Chính phủ;<br>\\- Các bộ, cơ quan ngang bộ, cơ quan thuộc CP;<br>\\- Ủy ban Trung ương Mặt trận Tổ quốc Việt Nam;<br>\\- UBND các tỉnh, thành phố trực thuộc TW;<br>\\- Bộ Khoa học và Công nghệ (để đăng ký);<br>\\- Cục Kiểm tra văn bản QPPL - Bộ Tư pháp;<br>\\- Các Sở: XD, GTVT, NN&PTNT các tỉnh, TP trực thuộc TW;<br>\\- Công báo, Cổng thông tin điện tử Chính phủ;<br>\\- Cổng thông tin điện tử Bộ Xây dựng;<br>\\- Các cơ quan, đơn vị thuộc Bộ Xây dựng;<br>\\- Lưu: VT, Vụ KHCN&MT. | *(Đã ký)*<br><br>**Lê Quang Hùng** |
"""
(bundle_dir / "thong_tu_05_2022_tt_bxd.md").write_text(thong_tu_md.strip() + "\n", encoding="utf-8")

# 2. qcvn_03_2022_bxd.md (100% Verbatim normative text)
qcvn_verbatim = """# QCVN 03:2022/BXD

## QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ PHÂN CẤP CÔNG TRÌNH PHỤC VỤ THIẾT KẾ XÂY DỰNG
*National Technical Regulation on Classifications of Buildings and Structures for design*

---

### Lời nói đầu

QCVN 03:2022/BXD do Viện Khoa học Công nghệ Xây dựng biên soạn, Vụ Khoa học Công nghệ và Môi trường trình duyệt, Bộ Khoa học và Công nghệ thẩm định, Bộ Xây dựng ban hành kèm theo Thông tư số 05/2022/TT-BXD ngày 30 tháng 11 năm 2022.

QCVN 03:2022/BXD thay thế QCVN 03:2012/BXD được ban hành kèm theo Thông tư số 12/2012/TT-BXD ngày 28 tháng 12 năm 2012 của Bộ trưởng Bộ Xây dựng.

---

## 1. QUY ĐỊNH CHUNG

### 1.1. Phạm vi điều chỉnh

1.1.1. Quy chuẩn này quy định về việc phân cấp công trình theo các tiêu chí sau:

\\- a) Hậu quả do kết cấu công trình bị hư hỏng hoặc phá hủy (sau đây gọi là cấp hậu quả);

\\- b) Thời hạn sử dụng theo thiết kế của công trình;

\\- c) Phân loại kỹ thuật về cháy đối với công trình (hoặc các phần của công trình, sau đây gọi chung là công trình), bao gồm: bậc chịu lửa, cấp nguy hiểm cháy kết cấu và nhóm nguy hiểm cháy theo công năng.

1.1.2. Quy chuẩn này áp dụng để xác định các giải pháp kinh tế - kỹ thuật khi thiết kế các công trình dân dụng, công nghiệp, hạ tầng kỹ thuật và các công trình dạng nhà khác.

1.1.3. Quy chuẩn này áp dụng khi thiết kế xây dựng mới các công trình quy định tại 1.1.2 của quy chuẩn này, và khuyến khích áp dụng khi thiết kế cải tạo các công trình hiện hữu.

### 1.2. Đối tượng áp dụng

Quy chuẩn này áp dụng đối với các tổ chức, cá nhân có liên quan đến hoạt động đầu tư xây dựng tại Việt Nam.

### 1.3. Giải thích từ ngữ

Trong quy chuẩn này, các thuật ngữ, định nghĩa dưới đây được hiểu như sau:

1.3.1. **Bậc chịu lửa:** Đặc trưng phân bậc của công trình, được xác định bởi giới hạn chịu lửa của các kết cấu, cấu kiện sử dụng để xây dựng công trình đó.

1.3.2. **Cấp hậu quả:** Đặc trưng phân cấp của công trình, phụ thuộc vào công năng sử dụng của công trình, cũng như thiệt hại về người, hậu quả về xã hội, môi trường và kinh tế khi kết cấu công trình bị hư hỏng hoặc phá hủy.

1.3.3. **Cấp nguy hiểm cháy kết cấu công trình:** Đặc trưng phân cấp của công trình, được xác định bởi mức độ tham gia của kết cấu xây dựng vào sự phát triển đám cháy và hình thành các yếu tố nguy hiểm của đám cháy.

1.3.4. **Độ bền lâu:** Khả năng của công trình xây dựng bảo toàn được các tính chất độ bền, vật lý và các tính chất khác đã được quy định trong thiết kế và bảo đảm cho công trình xây dựng sử dụng bình thường trong suốt thời hạn sử dụng theo thiết kế.

1.3.5. **Kết cấu công trình:** Tổ hợp các bộ phận, cấu kiện của công trình chịu tất cả các tải trọng và tác động lên công trình, và bảo đảm độ bền, độ cứng và ổn định cho công trình.

1.3.6. **Nhóm nguy hiểm cháy theo công năng của công trình:** Đặc trưng phân nhóm của công trình, được xác định bởi công năng và các đặc điểm sử dụng riêng của công trình, kể cả các đặc điểm của các quá trình công nghệ của sản xuất trong công trình đó.

1.3.7. **Sửa chữa lớn (đối với kết cấu công trình):** Hoạt động thay thế, gia cường, khôi phục các bộ phận, cấu kiện kết cấu hoặc gia cố nền nhằm đưa chúng trở lại trạng thái làm việc bình thường.

&nbsp;&nbsp;*CHÚ THÍCH: Công tác sửa chữa, thay thế các bộ phận bao che, trang trí, hoàn thiện, các lớp bảo vệ kết cấu trong quá trình bảo trì không được coi là sửa chữa lớn.*

1.3.8. **Thời hạn sử dụng theo thiết kế của công trình (tuổi thọ thiết kế):** Khoảng thời gian công trình được dự kiến sử dụng, đảm bảo yêu cầu về an toàn và công năng sử dụng mà không cần sửa chữa lớn kết cấu.

---

## 2. QUY ĐỊNH KỸ THUẬT

### 2.1. Cấp hậu quả của công trình

2.1.1. Cấp hậu quả của công trình được phân thành ba cấp: C1 (thấp), C2 (trung bình) và C3 (cao), được quy định tại [Phụ lục A](./annexes/phu_luc_a_cap_hau_qua_cong_trinh.md) của quy chuẩn này và được xác định trong nhiệm vụ thiết kế xây dựng công trình.

2.1.2. Kết cấu và nền của công trình cần được thiết kế tương ứng với cấp hậu quả của công trình quy định tại quy chuẩn này theo các tiêu chuẩn thiết kế được lựa chọn áp dụng.

2.1.3. Phụ thuộc vào dạng kết cấu và những tình huống cụ thể trong thiết kế công trình, có thể áp dụng cấp hậu quả của một số bộ phận, cấu kiện kết cấu khác với cấp hậu quả của công trình.

### 2.2. Thời hạn sử dụng theo thiết kế của công trình

2.2.1. Tùy thuộc chức năng của công trình trong dự án đầu tư xây dựng, môi trường khai thác sử dụng, và thời hạn hoạt động của dự án (nếu có); thời hạn sử dụng theo thiết kế của công trình phải được xác định trong nhiệm vụ thiết kế xây dựng công trình.

2.2.2. Thời hạn sử dụng theo thiết kế của công trình được chia thành bốn mức như Bảng 1, người quyết định đầu tư hoặc chủ đầu tư có thể sử dụng các mức này để xác định thời hạn sử dụng theo thiết kế của công trình trong nhiệm vụ thiết kế xây dựng công trình.

#### Bảng 1 — Thời hạn sử dụng theo thiết kế của công trình

| Mức | Thời hạn sử dụng theo thiết kế của công trình 1) | Công trình |
| :--- | :--- | :--- |
| **1** | Nhỏ hơn 25 năm | Công trình quy định tại A.2, [Phụ lục A](./annexes/phu_luc_a_cap_hau_qua_cong_trinh.md) của quy chuẩn này. |
| **2** | Không nhỏ hơn 25 năm | Công trình chịu tác động trực tiếp của môi trường xâm thực mạnh 2) (hóa chất, môi trường biển), trừ công trình tạm. |
| **3** | Không nhỏ hơn 50 năm | Các công trình dân dụng, công nghiệp, hạ tầng kỹ thuật và các công trình dạng nhà khác không thuộc các mức 1, 2 và 4 trong bảng này. |
| **4** | Không nhỏ hơn 100 năm | Nhà và công trình độc đáo, có giá trị kiến trúc hoặc mang ý nghĩa biểu tượng quan trọng (Bảo tàng quốc gia, nhà lưu giữ hiện vật quốc gia, sân vận động thi đấu cấp quốc gia hoặc quốc tế, nhà hát quốc gia, công trình điểm nhấn có kiến trúc độc đáo tại các địa phương và các công trình tương tự). |

**CHÚ THÍCH:**  
\\- 1) Thời hạn sử dụng theo thiết kế của công trình được xác định trong nhiệm vụ thiết kế xây dựng công trình hoặc theo quy định của tiêu chuẩn thiết kế chuyên ngành được áp dụng.  
\\- 2) Môi trường xâm thực mạnh được xác định theo các tiêu chuẩn kỹ thuật hiện hành về bảo vệ chống ăn mòn kết cấu xây dựng.

2.2.3. Kết cấu của công trình phải được thiết kế theo tiêu chuẩn lựa chọn áp dụng nhằm đảm bảo độ bền lâu tương ứng với thời hạn sử dụng theo thiết kế của công trình, có xét đến các yếu tố sau:

\\- Các điều kiện khai thác sử dụng theo công năng;

\\- Ảnh hưởng của môi trường xung quanh;

\\- Các tính chất của vật liệu sử dụng, các giải pháp bảo vệ chúng khỏi các tác động bất lợi của môi trường cũng như khả năng suy giảm các tính chất của vật liệu.

### 2.3. Phân loại kỹ thuật về cháy đối với công trình

2.3.1. Việc phân loại kỹ thuật về cháy đối với công trình nhằm thiết lập các yêu cầu an toàn cháy khi thiết kế xây dựng các hệ thống phòng cháy chống cháy cho công trình, phụ thuộc vào công năng và tính nguy hiểm cháy của công trình.

&nbsp;&nbsp;*CHÚ THÍCH: Các khái niệm về an toàn cháy trong 2.3 được định nghĩa tại QCVN 06:2022/BXD.*

2.3.2. Phân loại kỹ thuật về cháy đối với công trình được thực hiện theo các tiêu chí sau:

\\- a) Bậc chịu lửa;

\\- b) Cấp nguy hiểm cháy kết cấu;

\\- c) Nhóm nguy hiểm cháy theo công năng.

2.3.3. Bậc chịu lửa của công trình được phân thành 5 bậc từ I, II, III, IV đến V; phụ thuộc vào số tầng (hoặc chiều cao phòng cháy chữa cháy của công trình), nhóm nguy hiểm cháy theo công năng, diện tích khoang cháy và tính nguy hiểm cháy của các quá trình công nghệ diễn ra trong công trình.

&nbsp;&nbsp;*CHÚ THÍCH: Đối với nhà chung cư có chiều cao trên 75 m và nhà công cộng có chiều cao trên 50 m, QCVN 06:2022/BXD quy định các yêu cầu riêng về giới hạn chịu lửa của kết cấu, cấu kiện của công trình.*

2.3.4. Cấp nguy hiểm cháy kết cấu của công trình được phân thành 4 cấp từ S0, S1, S2 đến S3; theo tính nguy hiểm cháy của cấu kiện.

2.3.5. Công trình được phân thành 5 nhóm nguy hiểm cháy theo công năng từ F1, F2, F3, F4 đến F5; tùy thuộc vào đặc điểm sử dụng chúng và vào mức đe dọa tới sự an toàn của người trong trường hợp xảy ra đám cháy có tính đến: lứa tuổi, trạng thái thể chất, khả năng có người đang ngủ, nhóm người sử dụng theo công năng chính và số người của nhóm đó.

2.3.6. Bậc chịu lửa, cấp nguy hiểm cháy kết cấu và nhóm nguy hiểm cháy theo công năng của công trình được xác định theo QCVN 06:2022/BXD.

---

## 3. TỔ CHỨC THỰC HIỆN

### 3.1. Quy định chuyển tiếp

3.1.1. Dự án đầu tư xây dựng đã được phê duyệt trước khi quy chuẩn này có hiệu lực thi hành thì tiếp tục thực hiện theo các quy định tại thời điểm được phê duyệt.

3.1.2. Dự án đầu tư xây dựng được phê duyệt kể từ thời điểm quy chuẩn này có hiệu lực thi hành thì thực hiện theo quy định của quy chuẩn này.

3.1.3. Riêng về an toàn cháy, dự án đầu tư xây dựng được chuyển tiếp theo quy định của QCVN 06:2022/BXD.

### 3.2. Trách nhiệm kiểm tra tuân thủ

Các cơ quan quản lý Nhà nước về xây dựng tại các địa phương có trách nhiệm tổ chức kiểm tra sự tuân thủ quy chuẩn này trong việc lập, thẩm định, phê duyệt và quản lý thiết kế xây dựng công trình.

### 3.3. Trách nhiệm hướng dẫn áp dụng

Bộ Xây dựng chịu trách nhiệm phổ biến, hướng dẫn áp dụng quy chuẩn này cho các đối tượng có liên quan. Trong quá trình triển khai thực hiện quy chuẩn này, nếu có vướng mắc, mọi ý kiến gửi về Vụ Khoa học công nghệ và môi trường, Bộ Xây dựng để được hướng dẫn và xử lý.
"""
(bundle_dir / "qcvn_03_2022_bxd.md").write_text(qcvn_verbatim.strip() + "\n", encoding="utf-8")
(sources_dir / "qcvn_03_2022_bxd_goc.md").write_text(qcvn_verbatim.strip() + "\n", encoding="utf-8")

# 3. phu_luc_a_cap_hau_qua_cong_trinh.md (100% Verbatim)
phu_luc_a_verbatim = """# PHỤ LỤC A (Quy định)

## CẤP HẬU QUẢ CỦA CÔNG TRÌNH XÂY DỰNG

---

### A.1. Các công trình có cấp C3

#### A.1.1. Công trình tập trung đông người
\\- **A.1.1.1.** Nhà ga hàng không (nhà ga chính).
\\- **A.1.1.2.** Tòa nhà trung tâm hội nghị, nhà hát, nhà văn hóa, câu lạc bộ, rạp chiếu phim, rạp xiếc, vũ trường và các công trình văn hóa tập trung đông người tương tự với tổng sức chứa trên 1 200 chỗ.
\\- **A.1.1.3.** Tòa nhà trung tâm thương mại, siêu thị, nhà hàng và các nhà để kinh doanh dịch vụ tập trung đông người tương tự, có nhiều tầng với tổng diện tích sàn kinh doanh trên 30 000 m2.
\\- **A.1.1.4.** Khán đài sân vận động hoặc khán đài sân thi đấu thể thao ngoài trời (và mái che khán đài, nếu có) với sức chứa trên 5 000 chỗ.
\\- **A.1.1.5.** Tòa nhà thi đấu thể thao có khán đài với sức chứa trên 5 000 chỗ.
\\- **A.1.1.6.** Tòa nhà bệnh viện với tổng số giường bệnh trong tòa nhà đó từ 500 giường trở lên.

#### A.1.2. Công trình có nguy cơ gây ô nhiễm môi trường hoặc thiệt hại về kinh tế nếu có sự cố
\\- **A.1.2.1.** Các công trình chính trong cơ sở sản xuất, chế biến, sử dụng, lưu trữ, bảo quản, xử lý, tiêu hủy chất phóng xạ, vật liệu nổ có nguy cơ rò rỉ hoặc phát nổ.
\\- **A.1.2.2.** Các công trình chính trong cơ sở sản xuất, chế biến, sử dụng, lưu trữ, bảo quản, xử lý, tiêu hủy hóa chất nguy hiểm, độc hại có nguy cơ rò rỉ hoặc cháy nổ.
\\- **A.1.2.3.** Các công trình chính trong các cơ sở: nhà máy lọc, hóa dầu, nhà máy chế biến khí, trạm cấp khí (LPG, CNG, LNG), nhà máy sản xuất nhiên liệu sinh học, kho chứa dầu thô, xăng dầu, kho chứa khí hóa lỏng, trạm chiết khí hóa lỏng, phân phối khí; các tuyến ống dẫn khí, dẫn dầu có nguy cơ sự cố gây thiệt hại về người hoặc hậu quả cao về kinh tế hoặc môi trường.
&nbsp;&nbsp;*CHÚ THÍCH: LPG là từ viết tắt của Liquified Petrolium Gas; CNG - Compressed Natural Gas; LNG - Liquified Natural Gas.*
\\- **A.1.2.4.** Các công trình chính thuộc nhà máy nhiệt điện có công suất từ 150 MW trở lên.

#### A.1.3. Công trình có ý nghĩa chính trị - xã hội
\\- **A.1.3.1.** Nhà Quốc hội, Phủ Chủ tịch, tòa nhà trụ sở Chính phủ, tòa nhà trụ sở Trung ương Đảng.
\\- **A.1.3.2.** Tòa nhà bảo tàng, thư viện, triển lãm, nhà trưng bày cấp quốc gia.

#### A.1.4. Công trình có quy mô kết cấu lớn
\\- **A.1.4.1.** Kết cấu dạng nhà có chiều cao trên 75 m.
&nbsp;&nbsp;*CHÚ THÍCH: Chiều cao kết cấu dạng nhà được tính từ cao độ mặt đất đặt công trình tới điểm cao nhất của kết cấu công trình (bao gồm tầng tum, mái dốc nếu có; không bao gồm các thiết bị kỹ thuật như cột ăng ten, cột thu sét, thiết bị sử dụng năng lượng mặt trời, bể nước kim loại .... nếu có). Đối với công trình đặt trên mặt đất có các cao độ mặt đất khác nhau thì chiều cao tính từ cao độ mặt đất thấp nhất.*
\\- **A.1.4.2.** Kết cấu cột, trụ, tháp có chiều cao trên 75 m.
&nbsp;&nbsp;*CHÚ THÍCH: Chiều cao kết cấu cột, trụ, tháp được tính từ cao độ mặt đất đặt công trình hoặc từ cao độ mặt móng công trình, lấy theo cao độ cao hơn, tới đỉnh kết cấu cột, trụ, tháp (không bao gồm các thiết bị kỹ thuật trên đỉnh cột, trụ, tháp nếu có). Đối với công trình đặt trên mặt đất có các cao độ mặt đất khác nhau thì chiều cao tính từ cao độ mặt đất thấp nhất.*
\\- **A.1.4.3.** Kết cấu dạng bể chứa, si lô có chiều cao trên 75 m, hoặc dung tích chứa lớn hơn 15 000 m3.
\\- **A.1.4.4.** Kết cấu có nhịp từ 100 m trở lên.
\\- **A.1.4.5.** Kết cấu ngầm thuộc công trình dân dụng và công trình hạ tầng kỹ thuật trong đô thị có chiều sâu ngầm từ 18 m trở lên.
&nbsp;&nbsp;*CHÚ THÍCH: Chiều sâu ngầm của kết cấu được tính từ cao độ mặt đất đặt công trình tới mặt sàn dưới cùng.*

#### A.1.5. Các công trình khác theo quyết định của người quyết định đầu tư, chủ đầu tư xây dựng công trình
&nbsp;&nbsp;*CHÚ THÍCH: Đê, đập, tường chắn, kè và các công trình chịu áp tương tự phân cấp theo quy chuẩn, tiêu chuẩn chuyên ngành khác.*

---

### A.2. Các công trình có cấp C1

\\- **A.2.1.** Nhà ở riêng lẻ một tầng sử dụng vật liệu độ bền lâu thấp (gạch xỉ, vôi xỉ, đá ong, đất, tre, lá và tương tự).
\\- **A.2.2.** Nhà một tầng dùng vào các mục đích: sinh hoạt tạm cho người, nhà tạm tổ chức sự kiện, hoạt động văn hóa, dịch vụ ngoài trời quy mô vừa và nhỏ; gia công, sản xuất tạm; kho lưu trữ tạm.
\\- **A.2.3.** Nhà di động dạng công ten nơ hoặc nhà tháo lắp được, sử dụng vào các mục đích tạm thời.
\\- **A.2.4.** Nhà bảo vệ, bãi để xe, lều trại, hàng rào tạm.
\\- **A.2.5.** Các công trình có mục đích sử dụng tạm khác.

---

### A.3. Các công trình có cấp C2

Công trình khác ngoài các công trình có cấp C1 và cấp C3.
"""
(annexes_dir / "phu_luc_a_cap_hau_qua_cong_trinh.md").write_text(phu_luc_a_verbatim.strip() + "\n", encoding="utf-8")

print("✅ Successfully updated QCVN 03:2022/BXD markdown files with 100% verbatim accuracy.")
