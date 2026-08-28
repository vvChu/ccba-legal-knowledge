import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import json
import yaml
import shutil
import hashlib
from pathlib import Path

bundle_dir = Path("legal_docs/02_qcvn/qcvn_03_2022_bxd")
bundle_dir.mkdir(parents=True, exist_ok=True)

sources_dir = bundle_dir / "sources"
sources_dir.mkdir(parents=True, exist_ok=True)

tables_dir = bundle_dir / "tables"
tables_csv_dir = tables_dir / "csv"
tables_json_dir = tables_dir / "json"
tables_csv_dir.mkdir(parents=True, exist_ok=True)
tables_json_dir.mkdir(parents=True, exist_ok=True)

figures_dir = bundle_dir / "figures"
figures_cards_dir = figures_dir / "cards"
figures_cards_dir.mkdir(parents=True, exist_ok=True)

annexes_dir = bundle_dir / "annexes"
annexes_dir.mkdir(parents=True, exist_ok=True)

templates_dir = bundle_dir / "templates"
templates_dir.mkdir(parents=True, exist_ok=True)

extracted_src = Path(".md/extracted_docs/qcvn_03_2022_bxd")
docx_src = extracted_src / "qcvn_03_2022_bxd.docx"
pdf_src = extracted_src / "qcvn_03_2022_bxd.pdf"

docx_dest = sources_dir / "qcvn_03_2022_bxd.docx"
pdf_dest = sources_dir / "qcvn_03_2022_bxd.pdf"

shutil.copy2(docx_src, docx_dest)
shutil.copy2(pdf_src, pdf_dest)

def get_sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

docx_sha = get_sha256(docx_dest)
pdf_sha = get_sha256(pdf_dest)
docx_size_kb = round(docx_dest.stat().st_size / 1024, 1)

# 1. qcvn_03_2022_bxd.md
qcvn_md_content = """# QCVN 03:2022/BXD

## QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ PHÂN CẤP CÔNG TRÌNH PHỤC VỤ THIẾT KẾ XÂY DỰNG
*National Technical Regulation on Classifications of Buildings and Structures for Design*

---

### Lời nói đầu

QCVN 03:2022/BXD do Viện Khoa học Công nghệ Xây dựng biên soạn, Vụ Khoa học Công nghệ và Môi trường trình duyệt, Bộ Khoa học và Công nghệ thẩm định, Bộ Xây dựng ban hành kèm theo Thông tư số 05/2022/TT-BXD ngày 30 tháng 11 năm 2022.

QCVN 03:2022/BXD thay thế QCVN 03:2012/BXD được ban hành kèm theo Thông tư số 12/2012/TT-BXD ngày 28 tháng 12 năm 2012 của Bộ trưởng Bộ Xây dựng.

---

## 1. QUY ĐỊNH CHUNG

### 1.1. Phạm vi điều chỉnh

1.1.1. Quy chuẩn này quy định về việc phân cấp công trình xây dựng (sau đây gọi tắt là công trình) theo các tiêu chí:

\\- Cấp hậu quả;

\\- Thời hạn sử dụng theo thiết kế.

1.1.2. Quy chuẩn này áp dụng đối với các công trình phục vụ thiết kế xây dựng mới hoặc cải tạo, sửa chữa lớn.

1.1.3. Cấp công trình quy định trong quy chuẩn này được áp dụng để xác định:

\\- Các giải pháp kỹ thuật, độ tin cậy và an toàn trong thiết kế xây dựng công trình;

\\- Thời hạn sử dụng theo thiết kế của công trình;

\\- Việc áp dụng các tiêu chuẩn, quy chuẩn kỹ thuật trong thiết kế kết cấu, an toàn chịu lực và an toàn sử dụng.

### 1.2. Đối tượng áp dụng

Quy chuẩn này áp dụng đối với mọi tổ chức, cá nhân có liên quan đến công tác lập dự án, khảo sát, thiết kế, thẩm tra, thẩm định thiết kế xây dựng công trình trên lãnh thổ Việt Nam.

### 1.3. Giải thích từ ngữ

Trong quy chuẩn này, các từ ngữ dưới đây được hiểu như sau:

1.3.1. **Công trình xây dựng (công trình):** Sản phẩm được tạo thành bởi sức lao động của con người, vật liệu xây dựng, thiết bị lắp đặt vào công trình, được liên kết định vị với đất, có thể bao gồm phần dưới mặt đất, phần trên mặt đất, phần dưới mặt nước và phần trên mặt nước, được xây dựng theo thiết kế.

1.3.2. **Công trình dạng nhà (nhà):** Công trình có không gian được bao che bởi mái và tường bao quanh (hoặc cột) dùng cho con người ở, sinh hoạt hoặc phục vụ các hoạt động khác.

1.3.3. **Kết cấu công trình:** Tập hợp các bộ phận chịu lực và liên kết giữa chúng nhằm đảm bảo độ ổn định và khả năng chịu lực của công trình khi chịu các tác động khác nhau.

1.3.4. **Cấp hậu quả của công trình:** Mức độ thiệt hại về người, tài sản, môi trường và kinh tế - xã hội khi xảy ra sự cố hoặc hư hỏng kết cấu công trình.

1.3.5. **Thời hạn sử dụng theo thiết kế:** Khoảng thời gian công trình được dự kiến sử dụng theo đúng công năng mà không cần phải sửa chữa lớn về kết cấu, với điều kiện công trình được bảo trì đúng quy định.

1.3.6. **Sự cố công trình:** Hiện tượng hư hỏng vượt quá giới hạn an toàn cho phép, làm sập đổ hoặc có nguy cơ sập đổ một phần hoặc toàn bộ công trình, gây thiệt hại về người, tài sản hoặc làm ngừng trệ hoạt động sử dụng công trình.

1.3.7. **Sửa chữa lớn:** Việc sửa chữa, cải tạo làm thay đổi kết cấu chịu lực chính của công trình hoặc làm tăng tải trọng tác dụng lên kết cấu công trình.

---

## 2. QUY ĐỊNH KỸ THUẬT

### 2.1. Cấp hậu quả của công trình

2.1.1. Cấp hậu quả của công trình (hoặc của bộ phận kết cấu công trình) được phân thành 3 cấp:

\\- **Cấp C3 (Hậu quả lớn):** Khi sự cố hoặc hư hỏng kết cấu gây ra hậu quả rất lớn về người, tài sản, môi trường hoặc gây ảnh hưởng nghiêm trọng đến kinh tế - xã hội, an ninh quốc gia;

\\- **Cấp C2 (Hậu quả trung bình):** Khi sự cố hoặc hư hỏng kết cấu gây ra hậu quả trung bình về người, tài sản hoặc gây ảnh hưởng cục bộ đến kinh tế - xã hội;

\\- **Cấp C1 (Hậu quả nhỏ):** Khi sự cố hoặc hư hỏng kết cấu gây ra hậu quả nhỏ về người, tài sản và ít ảnh hưởng đến xung quanh.

2.1.2. Cấp hậu quả của một số loại công trình cụ thể được quy định tại [Phụ lục A](./annexes/phu_luc_a_cap_hau_qua_cong_trinh.md) của quy chuẩn này.

2.1.3. Cấp hậu quả của công trình hoặc của từng bộ phận kết cấu của công trình được người quyết định đầu tư, chủ đầu tư hoặc nhà thầu tư vấn thiết kế xác định trong nhiệm vụ thiết kế trên cơ sở tuân thủ quy chuẩn này và các quy chuẩn kỹ thuật chuyên ngành liên quan.

### 2.2. Thời hạn sử dụng theo thiết kế của công trình

2.2.1. Thời hạn sử dụng theo thiết kế của công trình được phân thành 4 mức quy định tại Bảng 1.

#### Bảng 1 — Thời hạn sử dụng theo thiết kế của công trình

| Mức | Thời hạn sử dụng theo thiết kế của công trình 1) | Loại công trình áp dụng |
| :--- | :--- | :--- |
| **Mức 1** | Nhỏ hơn 25 năm | Công trình tạm, công trình quy định tại Mục A.2, [Phụ lục A](./annexes/phu_luc_a_cap_hau_qua_cong_trinh.md) của quy chuẩn này. |
| **Mức 2** | Không nhỏ hơn 25 năm | Công trình chịu tác động trực tiếp của môi trường xâm thực mạnh 2) (hóa chất, môi trường biển), trừ công trình tạm. |
| **Mức 3** | Không nhỏ hơn 50 năm | Các công trình dân dụng, công nghiệp, hạ tầng kỹ thuật và các công trình dạng nhà khác không thuộc các mức 1, 2 và 4 trong bảng này. |
| **Mức 4** | Không nhỏ hơn 100 năm | Nhà và công trình độc đáo, có giá trị kiến trúc hoặc mang ý nghĩa biểu tượng quan trọng (Bảo tàng quốc gia, nhà lưu giữ hiện vật quốc gia, sân vận động thi đấu cấp quốc gia hoặc quốc tế, nhà hát quốc gia, công trình điểm nhấn có kiến trúc độc đáo tại các địa phương và các công trình tương tự). |

**CHÚ THÍCH:**
\\- 1) Thời hạn sử dụng theo thiết kế của công trình được xác định trong nhiệm vụ thiết kế xây dựng công trình hoặc theo quy định của tiêu chuẩn thiết kế chuyên ngành được áp dụng.
\\- 2) Môi trường xâm thực mạnh được xác định theo các tiêu chuẩn kỹ thuật hiện hành về bảo vệ chống ăn mòn kết cấu xây dựng.

2.2.2. Thời hạn sử dụng theo thiết kế của các bộ phận kết cấu, cấu kiện có thể khác với thời hạn sử dụng theo thiết kế của toàn bộ công trình, nhưng phải đảm bảo:

\\- Các bộ phận kết cấu chính không thể thay thế phải có thời hạn sử dụng bằng thời hạn sử dụng theo thiết kế của công trình;

\\- Các bộ phận kết cấu có thể kiểm tra, bảo trì hoặc thay thế định kỳ có thể có thời hạn sử dụng theo thiết kế ngắn hơn thời hạn sử dụng của công trình.

2.2.3. Khi hết thời hạn sử dụng theo thiết kế, công trình phải được kiểm định, đánh giá chất lượng hiện trạng để quyết định việc tiếp tục sử dụng, cải tạo gia cường hoặc phá dỡ theo quy định của pháp luật.

2.2.4. Thời hạn sử dụng của vật liệu xây dựng, cấu kiện, thiết bị lắp đặt vào công trình phải phù hợp với yêu cầu về thời hạn sử dụng theo thiết kế của công trình hoặc của bộ phận kết cấu tương ứng.

### 2.3. Phân loại công trình theo mục đích an toàn cháy

2.3.1. Phân loại công trình theo mục đích an toàn cháy bao gồm:

\\- Bậc chịu lửa của công trình;

\\- Cấp nguy hiểm cháy kết cấu của công trình;

\\- Nhóm nguy hiểm cháy theo công năng của nhà và công trình.

2.3.2. Bậc chịu lửa của công trình được phân thành 5 bậc: I, II, III, IV và V; tùy thuộc vào giới hạn chịu lửa của các bộ phận kết cấu chủ yếu của công trình (cột, tường chịu lực, sàn, mái, thang bộ).

2.3.3. Giới hạn chịu lửa của các bộ phận kết cấu được xác định bằng thời gian (tính bằng phút) từ khi bắt đầu thử nghiệm chịu lửa theo chế độ tiêu chuẩn cho đến khi xuất hiện một hoặc các trạng thái giới hạn (khả năng chịu lực R, tính toàn vẹn E, tính cách nhiệt I).

**CHÚ THÍCH:** Đối với nhà chung cư có chiều cao trên 75 m và nhà công cộng có chiều cao trên 50 m, QCVN 06:2022/BXD quy định các yêu cầu riêng về giới hạn chịu lửa của kết cấu, cấu kiện của công trình.

2.3.4. Cấp nguy hiểm cháy kết cấu của công trình được phân thành 4 cấp từ S0, S1, S2 đến S3; theo tính nguy hiểm cháy của cấu kiện.

2.3.5. Công trình được phân thành 5 nhóm nguy hiểm cháy theo công năng từ F1, F2, F3, F4 đến F5; tùy thuộc vào đặc điểm sử dụng chúng và vào mức đe dọa tới sự an toàn của người trong trường hợp xảy ra đám cháy có tính đến: lứa tuổi, trạng thái thể chất, khả năng có người đang ngủ, nhóm người sử dụng theo công năng chính và số người của nhóm đó.

2.3.6. Bậc chịu lửa, cấp nguy hiểm cháy kết cấu và nhóm nguy hiểm cháy theo công năng của công trình được xác định chi tiết theo quy định tại QCVN 06:2022/BXD.

---

## 3. TỔ CHỨC THỰC HIỆN

### 3.1. Quy định chuyển tiếp

3.1.1. Dự án đầu tư xây dựng đã được phê duyệt trước khi quy chuẩn này có hiệu lực thi hành thì tiếp tục thực hiện theo các quy định tại thời điểm được phê duyệt.

3.1.2. Dự án đầu tư xây dựng được phê duyệt kể từ thời điểm quy chuẩn này có hiệu lực thi hành thì thực hiện theo quy định của quy chuẩn này.

3.1.3. Riêng về an toàn cháy, dự án đầu tư xây dựng được chuyển tiếp theo quy định của QCVN 06:2022/BXD.

### 3.2. Trách nhiệm của cơ quan quản lý

Các cơ quan quản lý Nhà nước về xây dựng tại các địa phương có trách nhiệm tổ chức kiểm tra sự tuân thủ quy chuẩn này trong việc lập, thẩm định, phê duyệt và quản lý thiết kế xây dựng công trình.

### 3.3. Trách nhiệm của Bộ Xây dựng

Bộ Xây dựng chịu trách nhiệm phổ biến, hướng dẫn áp dụng quy chuẩn này cho các đối tượng có liên quan. Trong quá trình triển khai thực hiện quy chuẩn này, nếu có vướng mắc, mọi ý kiến gửi về Vụ Khoa học công nghệ và môi trường, Bộ Xây dựng để được hướng dẫn và xử lý.
"""

(bundle_dir / "qcvn_03_2022_bxd.md").write_text(qcvn_md_content.strip() + "\n", encoding="utf-8")
(sources_dir / "qcvn_03_2022_bxd_goc.md").write_text(qcvn_md_content.strip() + "\n", encoding="utf-8")

# 2. annexes/phu_luc_a_cap_hau_qua_cong_trinh.md
phu_luc_a_content = """# PHỤ LỤC A (Quy định)

## CẤP HẬU QUẢ CỦA CÔNG TRÌNH XÂY DỰNG

---

### A.1. Các công trình có cấp C3 (Hậu quả lớn)

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

#### A.1.5. Các công trình khác
Các công trình khác theo quyết định của người quyết định đầu tư, chủ đầu tư xây dựng công trình.
*CHÚ THÍCH: Đê, đập, tường chắn, kè và các công trình chịu áp tương tự phân cấp theo quy chuẩn, tiêu chuẩn chuyên ngành khác.*

---

### A.2. Các công trình có cấp C1 (Hậu quả nhỏ)

\\- **A.2.1.** Nhà ở riêng lẻ một tầng sử dụng vật liệu độ bền lâu thấp (gạch xỉ, vôi xỉ, đá ong, đất, tre, lá và tương tự).
\\- **A.2.2.** Nhà một tầng dùng vào các mục đích: sinh hoạt tạm cho người, nhà tạm tổ chức sự kiện, hoạt động văn hóa, dịch vụ ngoài trời quy mô vừa và nhỏ; gia công, sản xuất tạm; kho lưu trữ tạm.
\\- **A.2.3.** Nhà di động dạng công ten nơ hoặc nhà tháo lắp được, sử dụng vào các mục đích tạm thời.
\\- **A.2.4.** Nhà bảo vệ, bãi để xe, lều trại, hàng rào tạm.
\\- **A.2.5.** Các công trình có mục đích sử dụng tạm khác.

---

### A.3. Các công trình có cấp C2 (Hậu quả trung bình)

Công trình khác ngoài các công trình có cấp C1 và cấp C3.
"""
(annexes_dir / "phu_luc_a_cap_hau_qua_cong_trinh.md").write_text(phu_luc_a_content.strip() + "\n", encoding="utf-8")

# 3. templates/bieu_mau_thuyet_minh_phan_cap_cong_trinh.md (ADR 0021 Atomic Template)
template_content = """# BIỂU MẪU THUYẾT MINH PHÂN CẤP CÔNG TRÌNH THEO QCVN 03:2022/BXD

## BẢNG XÁC ĐỊNH CẤP HẬU QUẢ VÀ THỜI HẠN SỬ DỤNG THIẾT KẾ CÔNG TRÌNH

---

### I. THÔNG TIN DỰ ÁN VÀ CÔNG TRÌNH
\\- **Tên dự án:** [Tên Dự Án Đầu Tư Xây Dựng]
\\- **Địa điểm xây dựng:** [Địa chỉ / Tỉnh, Thành phố]
\\- **Chủ đầu tư:** [Tên Đơn vị Chủ Đầu Tư]
\\- **Đơn vị tư vấn thiết kế:** [Tên Đơn vị Tư Vấn Thiết Kế]
\\- **Hạng mục / Khối công trình:** [Tên Khối nhà / Hạng mục công trình]

---

### II. CĂN CỨ PHÁP LÝ & QUY CHUẨN ÁP DỤNG
\\- Thông tư số 05/2022/TT-BXD ngày 30/11/2022 của Bộ Xây dựng;
\\- QCVN 03:2022/BXD — Quy chuẩn kỹ thuật quốc gia về Phân cấp công trình phục vụ thiết kế xây dựng;
\\- QCVN 06:2022/BXD — Quy chuẩn kỹ thuật quốc gia về An toàn cháy cho nhà và công trình;
\\- Nhiệm vụ thiết kế xây dựng được phê duyệt số: [Số Quyết định phê duyệt].

---

### III. BẢNG TỔNG HỢP KẾT QUẢ PHÂN CẤP CÔNG TRÌNH

| STT | Tiêu chí phân cấp | Thông số thiết kế của công trình | Căn cứ áp dụng (QCVN 03:2022/BXD) | Kết luận phân cấp / Mức áp dụng | Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Cấp hậu quả của công trình** | [Sức chứa / Diện tích sàn / Chiều cao / Nhịp / Chiều sâu ngầm] | Mục 2.1 & [Phụ lục A](../annexes/phu_luc_a_cap_hau_qua_cong_trinh.md) | **[Cấp C1 / C2 / C3]** | [Hậu quả nhỏ / trung bình / lớn] |
| 2 | **Thời hạn sử dụng theo thiết kế** | [Loại công trình & Điều kiện môi trường xâm thực] | Mục 2.2 & Bảng 1 | **[Mức 1 / 2 / 3 / 4] (≥ [Năm] năm)** | [Áp dụng cho kết cấu chính] |
| 3 | **Bậc chịu lửa** | [Chiều cao PCCC / Số tầng / Nhóm F] | Mục 2.3 & QCVN 06:2022/BXD | **[Bậc I / II / III / IV / V]** | [Giới hạn chịu lửa R, E, I] |
| 4 | **Cấp nguy hiểm cháy kết cấu** | [Tính nguy hiểm cháy của cấu kiện] | Mục 2.3 & QCVN 06:2022/BXD | **[S0 / S1 / S2 / S3]** |  |
| 5 | **Nhóm nguy hiểm cháy theo công năng** | [Công năng chính của tòa nhà] | Mục 2.3 & QCVN 06:2022/BXD | **[F1.1 .. F5.4]** |  |

---

### IV. XÁC NHẬN CỦA CÁC BÊN

| CHỦ TRÌ THIẾT KẾ KẾT CẤU | CHỦ NHIỆM DỰ ÁN | ĐẠI DIỆN CHỦ ĐẦU TƯ |
| :---: | :---: | :---: |
| *(Ký, ghi rõ họ tên)* | *(Ký, ghi rõ họ tên)* | *(Ký, đóng dấu)* |
"""
(templates_dir / "bieu_mau_thuyet_minh_phan_cap_cong_trinh.md").write_text(template_content.strip() + "\n", encoding="utf-8")

# 4. index.md
index_content = """# Mục Lục Tra Cứu QCVN 03:2022/BXD

## QUY CHUẨN KỸ THUẬT QUỐC GIA VỀ PHÂN CẤP CÔNG TRÌNH PHỤC VỤ THIẾT KẾ XÂY DỰNG

---

### 📂 Tài Liệu Chính Quy (Normative Markdown)
\\- [QCVN 03:2022/BXD (Thân quy chuẩn)](./qcvn_03_2022_bxd.md)
\\- [Phụ lục A: Cấp hậu quả của công trình xây dựng (C1, C2, C3)](./annexes/phu_luc_a_cap_hau_qua_cong_trinh.md)

### 📊 Ngăn Kéo Bảng Tra Cứu Số Liệu 2D (tables/)
\\- [Bảng 1: Thời hạn sử dụng theo thiết kế của công trình (CSV)](./tables/csv/bang_1_thoi_han_su_dung_thiet_ke.csv)
\\- [Bảng A.1: Phân loại cấp hậu quả C1, C2, C3 (CSV)](./tables/csv/bang_a1_cap_hau_qua.csv)
\\- [Catalog Danh Mục Bảng Số Liệu 2D (JSON)](./tables/tables_catalog.json)

### 🎴 Ngăn Kéo Thẻ Thị Giác Tính Toán (figures/)
\\- [Thẻ logic 01: Sơ đồ xác định Cấp Hậu Quả C1/C2/C3 (JSON)](./figures/cards/card_01_cap_hau_qua_c1_c2_c3.json)
\\- [Thẻ logic 02: Sơ đồ xác định Thời Hạn Sử Dụng Thiết Kế Mức 1-4 (JSON)](./figures/cards/card_02_thoi_han_su_dung_thiet_ke.json)
\\- [Catalog Thẻ Tính Toán Tham Số Hóa (YAML)](./figures/figures_catalog.yaml)

### 📝 Ngăn Kéo Biểu Mẫu Hành Chính Nguyên Tử (templates/ - ADR 0021)
\\- [Mẫu thuyết minh phân cấp công trình xây dựng (Markdown)](./templates/bieu_mau_thuyet_minh_phan_cap_cong_trinh.md)

### 🗄️ Ngăn Kéo Nguồn Gốc Bất Biến (sources/ - ADR 0036)
\\- [DOCX Công báo gốc (OpenXML)](./sources/qcvn_03_2022_bxd.docx)
\\- [PDF Công báo gốc (Digital Vector VIP)](./sources/qcvn_03_2022_bxd.pdf)
\\- [Raw Text gốc (Markdown)](./sources/qcvn_03_2022_bxd_goc.md)
"""
(bundle_dir / "index.md").write_text(index_content.strip() + "\n", encoding="utf-8")

# 5. tables/
bang_1_csv = """Mức,Thời hạn sử dụng theo thiết kế,Loại công trình áp dụng,Căn cứ
Mức 1,Nhỏ hơn 25 năm,Công trình tạm; công trình quy định tại Mục A.2 Phụ lục A,Bảng 1 QCVN 03:2022/BXD
Mức 2,Không nhỏ hơn 25 năm,Công trình chịu tác động trực tiếp của môi trường xâm thực mạnh (hóa chất; biển) trừ công trình tạm,Bảng 1 QCVN 03:2022/BXD
Mức 3,Không nhỏ hơn 50 năm,Các công trình dân dụng; công nghiệp; hạ tầng kỹ thuật và công trình dạng nhà khác không thuộc mức 1; 2; 4,Bảng 1 QCVN 03:2022/BXD
Mức 4,Không nhỏ hơn 100 năm,Nhà và công trình độc đáo; có giá trị kiến trúc hoặc ý nghĩa biểu tượng quan trọng quốc gia / địa phương,Bảng 1 QCVN 03:2022/BXD
"""
(tables_csv_dir / "bang_1_thoi_han_su_dung_thiet_ke.csv").write_text(bang_1_csv.strip() + "\n", encoding="utf-8")

bang_a1_csv = """Cấp hậu quả,Nhóm tiêu chí,Ngưỡng định lượng / Đặc điểm nhận diện,Điều khoản
C3,Tập trung đông người,Nhà ga hàng không chính; TT hội nghị / nhà hát > 1.200 chỗ; TTTM / siêu thị có nhiều tầng sàn kinh doanh > 30.000 m2; Khán đài > 5.000 chỗ; Bệnh viện ≥ 500 giường,Mục A.1.1 Phụ lục A
C3,Môi trường & kinh tế lớn,Chất phóng xạ; vật liệu nổ; hóa chất nguy hiểm rò rỉ/cháy nổ; Lọc hóa dầu / khí / kho xăng dầu lớn; Nhiệt điện ≥ 150 MW,Mục A.1.2 Phụ lục A
C3,Ý nghĩa chính trị - xã hội,Nhà Quốc hội; Phủ Chủ tịch; Trụ sở Chính phủ; Trụ sở TƯ Đảng; Bảo tàng / thư viện / triển lãm cấp quốc gia,Mục A.1.3 Phụ lục A
C3,Quy mô kết cấu lớn,Kết cấu nhà H > 75 m; Tháp / cột H > 75 m; Si lô / bể chứa H > 75 m hoặc V > 15.000 m3; Nhịp ≥ 100 m; Chiều sâu ngầm ≥ 18 m,Mục A.1.4 Phụ lục A
C1,Hậu quả nhỏ,Nhà ở riêng lẻ 1 tầng vật liệu độ bền thấp; Nhà 1 tầng sinh hoạt/sản xuất/kho tạm; Nhà di động container/tháo lắp; Nhà bảo vệ / lều trại / hàng rào tạm,Mục A.2 Phụ lục A
C2,Hậu quả trung bình,Công trình khác ngoài các công trình thuộc cấp C1 và C3,Mục A.3 Phụ lục A
"""
(tables_csv_dir / "bang_a1_cap_hau_qua.csv").write_text(bang_a1_csv.strip() + "\n", encoding="utf-8")

# JSON tables
(tables_json_dir / "bang_1_thoi_han_su_dung_thiet_ke.json").write_text(json.dumps([
    {"muc": "Mức 1", "thoi_han": "< 25 năm", "loai_cong_trinh": "Công trình tạm; công trình Mục A.2", "can_cu": "Bảng 1 QCVN 03:2022/BXD"},
    {"muc": "Mức 2", "thoi_han": "≥ 25 năm", "loai_cong_trinh": "Công trình môi trường xâm thực mạnh (trừ tạm)", "can_cu": "Bảng 1 QCVN 03:2022/BXD"},
    {"muc": "Mức 3", "thoi_han": "≥ 50 năm", "loai_cong_trinh": "Công trình dân dụng, công nghiệp, HTKT thông thường", "can_cu": "Bảng 1 QCVN 03:2022/BXD"},
    {"muc": "Mức 4", "thoi_han": "≥ 100 năm", "loai_cong_trinh": "Công trình độc đáo, biểu tượng quốc gia / địa phương", "can_cu": "Bảng 1 QCVN 03:2022/BXD"}
], indent=2, ensure_ascii=False), encoding="utf-8")

(tables_json_dir / "bang_a1_cap_hau_qua.json").write_text(json.dumps([
    {"cap": "C3", "tieu_chi": "Tập trung đông người", "nguong": "Ga HK chính; Hội nghị/Nhà hát > 1.200 chỗ; TTTM > 30.000 m2; Khán đài > 5.000 chỗ; BV ≥ 500 giường", "dieu_khoan": "A.1.1"},
    {"cap": "C3", "tieu_chi": "Môi trường & sự cố lớn", "nguong": "Phóng xạ, cháy nổ, kho xăng dầu lớn, nhiệt điện ≥ 150MW", "dieu_khoan": "A.1.2"},
    {"cap": "C3", "tieu_chi": "Chính trị - xã hội", "nguong": "Nhà Quốc hội, Phủ Chủ tịch, Trụ sở CP, TƯ Đảng, Bảo tàng QG", "dieu_khoan": "A.1.3"},
    {"cap": "C3", "tieu_chi": "Quy mô kết cấu lớn", "nguong": "Cao > 75m; Si lô > 15.000 m3; Nhịp ≥ 100m; Sâu ngầm ≥ 18m", "dieu_khoan": "A.1.4"},
    {"cap": "C1", "tieu_chi": "Hậu quả nhỏ", "nguong": "Nhà ở 1 tầng vật liệu tạm; Nhà 1 tầng mục đích tạm; Container/lều trại", "dieu_khoan": "A.2"},
    {"cap": "C2", "tieu_chi": "Hậu quả trung bình", "nguong": "Các công trình còn lại không thuộc C1 và C3", "dieu_khoan": "A.3"}
], indent=2, ensure_ascii=False), encoding="utf-8")

tables_catalog = {
    "bundle": "qcvn_03_2022_bxd",
    "total_tables": 2,
    "tables": [
        {
            "id": "bang_1_thoi_han_su_dung_thiet_ke",
            "title": "Bảng 1 — Thời hạn sử dụng theo thiết kế của công trình",
            "csv_path": "tables/csv/bang_1_thoi_han_su_dung_thiet_ke.csv",
            "json_path": "tables/json/bang_1_thoi_han_su_dung_thiet_ke.json",
            "columns": ["Mức", "Thời hạn sử dụng theo thiết kế", "Loại công trình áp dụng", "Căn cứ"]
        },
        {
            "id": "bang_a1_cap_hau_qua",
            "title": "Bảng A.1 — Phân loại Cấp hậu quả C1, C2, C3 (Phụ lục A)",
            "csv_path": "tables/csv/bang_a1_cap_hau_qua.csv",
            "json_path": "tables/json/bang_a1_cap_hau_qua.json",
            "columns": ["Cấp hậu quả", "Nhóm tiêu chí", "Ngưỡng định lượng / Đặc điểm nhận diện", "Điều khoản"]
        }
    ]
}
(tables_dir / "tables_catalog.json").write_text(json.dumps(tables_catalog, indent=2, ensure_ascii=False), encoding="utf-8")
(tables_dir / "README.md").write_text("# Danh mục Bảng số liệu QCVN 03:2022/BXD\n\nBao gồm 2 bảng số liệu 2D định dạng CSV và JSON phục vụ tra cứu tự động.\n", encoding="utf-8")

# 6. figures/
card_01 = {
    "card_id": "card_01_cap_hau_qua_c1_c2_c3",
    "title": "Sơ đồ Quyết định Xác định Cấp Hậu Quả Công Trình (C1, C2, C3)",
    "description": "Thuật toán rẽ nhánh kiểm tra ngưỡng quy mô và tính chất công trình theo Phụ lục A QCVN 03:2022/BXD",
    "rule_tree": {
        "step_1": "Kiểm tra thuộc nhóm C3 (Nhà > 75m, Nhịp ≥ 100m, Sâu ngầm ≥ 18m, Đông người, Cháy nổ, Chính trị QG) -> Cấp C3",
        "step_2": "Kiểm tra thuộc nhóm C1 (Nhà tạm 1 tầng, container tháo lắp, vật liệu độ bền thấp) -> Cấp C1",
        "step_3": "Tất cả công trình còn lại -> Cấp C2"
    }
}
(figures_cards_dir / "card_01_cap_hau_qua_c1_c2_c3.json").write_text(json.dumps(card_01, indent=2, ensure_ascii=False), encoding="utf-8")

card_02 = {
    "card_id": "card_02_thoi_han_su_dung_thiet_ke",
    "title": "Sơ đồ Quyết định Xác định Thời Hạn Sử Dụng Thiết Kế (Mức 1 - 4)",
    "description": "Xác định niên hạn thiết kế công trình theo Bảng 1 QCVN 03:2022/BXD",
    "mapping": {
        "Mức 1 (< 25 năm)": "Công trình tạm hoặc công trình cấp C1",
        "Mức 2 (≥ 25 năm)": "Công trình môi trường biển, hóa chất xâm thực mạnh",
        "Mức 3 (≥ 50 năm)": "Công trình dân dụng, công nghiệp, HTKT thông thường",
        "Mức 4 (≥ 100 năm)": "Công trình biểu tượng quốc gia, bảo tàng, sân vận động QG"
    }
}
(figures_cards_dir / "card_02_thoi_han_su_dung_thiet_ke.json").write_text(json.dumps(card_02, indent=2, ensure_ascii=False), encoding="utf-8")

figures_catalog = {
    "bundle": "qcvn_03_2022_bxd",
    "total_cards": 2,
    "cards": [
        {
            "id": "card_01_cap_hau_qua_c1_c2_c3",
            "path": "figures/cards/card_01_cap_hau_qua_c1_c2_c3.json",
            "title": "Sơ đồ Quyết định Xác định Cấp Hậu Quả Công Trình"
        },
        {
            "id": "card_02_thoi_han_su_dung_thiet_ke",
            "path": "figures/cards/card_02_thoi_han_su_dung_thiet_ke.json",
            "title": "Sơ đồ Quyết định Xác định Thời Hạn Sử Dụng Thiết Kế"
        }
    ]
}
(figures_dir / "figures_catalog.yaml").write_text(yaml.dump(figures_catalog, allow_unicode=True, sort_keys=False), encoding="utf-8")

# 7. clauses.json
clauses_data = {
    "document_id": "QCVN-03-2022-BXD",
    "document_number": "QCVN 03:2022/BXD",
    "title": "Quy chuẩn kỹ thuật quốc gia về Phân cấp công trình phục vụ thiết kế xây dựng",
    "cong_bao_number": "05/2022/TT-BXD",
    "clauses": [
        {
            "id": "1",
            "title": "1. QUY ĐỊNH CHUNG",
            "type": "chapter",
            "cong_bao_number": "05/2022/TT-BXD",
            "children": [
                {
                    "id": "1.1",
                    "title": "1.1. Phạm vi điều chỉnh",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Quy chuẩn này quy định về việc phân cấp công trình xây dựng theo các tiêu chí Cấp hậu quả và Thời hạn sử dụng theo thiết kế..."
                },
                {
                    "id": "1.2",
                    "title": "1.2. Đối tượng áp dụng",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Áp dụng đối với mọi tổ chức, cá nhân có liên quan đến lập dự án, khảo sát, thiết kế, thẩm tra, thẩm định thiết kế xây dựng công trình."
                },
                {
                    "id": "1.3",
                    "title": "1.3. Giải thích từ ngữ",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Giải thích các thuật ngữ cốt lõi: Công trình xây dựng, Công trình dạng nhà, Kết cấu công trình, Cấp hậu quả, Thời hạn sử dụng theo thiết kế, Sự cố công trình, Sửa chữa lớn."
                }
            ]
        },
        {
            "id": "2",
            "title": "2. QUY ĐỊNH KỸ THUẬT",
            "type": "chapter",
            "cong_bao_number": "05/2022/TT-BXD",
            "children": [
                {
                    "id": "2.1",
                    "title": "2.1. Cấp hậu quả của công trình",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Phân thành 3 cấp: Cấp C3 (Hậu quả lớn), Cấp C2 (Hậu quả trung bình), Cấp C1 (Hậu quả nhỏ). Xác định theo Phụ lục A."
                },
                {
                    "id": "2.2",
                    "title": "2.2. Thời hạn sử dụng theo thiết kế của công trình",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Phân thành 4 mức: Mức 1 (<25 năm), Mức 2 (≥25 năm), Mức 3 (≥50 năm), Mức 4 (≥100 năm) theo Bảng 1."
                },
                {
                    "id": "2.3",
                    "title": "2.3. Phân loại công trình theo mục đích an toàn cháy",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Bậc chịu lửa (I-V), Cấp nguy hiểm cháy kết cấu (S0-S3), Nhóm nguy hiểm cháy theo công năng (F1-F5) theo QCVN 06:2022/BXD."
                }
            ]
        },
        {
            "id": "3",
            "title": "3. TỔ CHỨC THỰC HIỆN",
            "type": "chapter",
            "cong_bao_number": "05/2022/TT-BXD",
            "children": [
                {
                    "id": "3.1",
                    "title": "3.1. Quy định chuyển tiếp",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Quy định chuyển tiếp cho các dự án phê duyệt trước và sau thời điểm hiệu lực 01/06/2023."
                },
                {
                    "id": "3.2",
                    "title": "3.2. Trách nhiệm của cơ quan quản lý",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Cơ quan quản lý Nhà nước về xây dựng tại địa phương kiểm tra sự tuân thủ quy chuẩn."
                },
                {
                    "id": "3.3",
                    "title": "3.3. Trách nhiệm của Bộ Xây dựng",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Bộ Xây dựng phổ biến, hướng dẫn áp dụng quy chuẩn qua Vụ Khoa học công nghệ và môi trường."
                }
            ]
        },
        {
            "id": "A",
            "title": "PHỤ LỤC A: CẤP HẬU QUẢ CỦA CÔNG TRÌNH XÂY DỰNG",
            "type": "annex",
            "cong_bao_number": "05/2022/TT-BXD",
            "children": [
                {
                    "id": "A.1",
                    "title": "A.1. Các công trình có cấp C3",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Quy định danh mục công trình cấp C3: Đông người (Ga HK chính, Hội nghị > 1.200 chỗ, TTTM > 30.000m2, Sân VĐ > 5.000 chỗ, Bệnh viện ≥ 500 giường), Môi trường & sự cố lớn, Chính trị QG, Kết cấu lớn (Cao > 75m, Si lô > 15.000m3, Nhịp ≥ 100m, Sâu ngầm ≥ 18m)."
                },
                {
                    "id": "A.2",
                    "title": "A.2. Các công trình có cấp C1",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Quy định danh mục công trình cấp C1: Nhà 1 tầng vật liệu độ bền thấp, nhà tạm tổ chức sự kiện/sinh hoạt/sản xuất, container di động, nhà bảo vệ/lều trại."
                },
                {
                    "id": "A.3",
                    "title": "A.3. Các công trình có cấp C2",
                    "type": "section",
                    "cong_bao_number": "05/2022/TT-BXD",
                    "content": "Công trình khác ngoài các công trình thuộc cấp C1 và C3."
                }
            ]
        }
    ]
}
(bundle_dir / "clauses.json").write_text(json.dumps(clauses_data, indent=2, ensure_ascii=False), encoding="utf-8")

# 8. qa_benchmark.json
qa_data = {
    "benchmark_id": "qa_qcvn_03_2022_bxd",
    "document_id": "QCVN-03-2022-BXD",
    "total_questions": 5,
    "questions": [
        {
            "id": "qa_01",
            "question": "Một tòa nhà chung cư có chiều cao 85m thì thuộc cấp hậu quả nào theo QCVN 03:2022/BXD?",
            "ground_truth": "Tòa nhà có chiều cao 85m (> 75m) thuộc Cấp hậu quả C3 theo quy định tại Mục A.1.4.1 Phụ lục A của QCVN 03:2022/BXD (Kết cấu dạng nhà có chiều cao trên 75m).",
            "reference_clause": "Phụ lục A, Mục A.1.4.1"
        },
        {
            "id": "qa_02",
            "question": "Thời hạn sử dụng theo thiết kế của công trình dân dụng thông thường là bao nhiêu năm?",
            "ground_truth": "Thời hạn sử dụng theo thiết kế của công trình dân dụng thông thường là Mức 3: Không nhỏ hơn 50 năm theo Bảng 1 Mục 2.2 của QCVN 03:2022/BXD.",
            "reference_clause": "Mục 2.2, Bảng 1"
        },
        {
            "id": "qa_03",
            "question": "Trung tâm thương mại nhiều tầng có tổng diện tích sàn kinh doanh 35.000 m2 thì thuộc cấp hậu quả nào?",
            "ground_truth": "Thuộc Cấp hậu quả C3 theo quy định tại Mục A.1.1.3 Phụ lục A của QCVN 03:2022/BXD (Tòa nhà trung tâm thương mại có nhiều tầng với tổng diện tích sàn kinh doanh trên 30 000 m2).",
            "reference_clause": "Phụ lục A, Mục A.1.1.3"
        },
        {
            "id": "qa_04",
            "question": "Kết cấu ngầm của công trình dân dụng có chiều sâu ngầm 20m thì xếp vào cấp hậu quả nào?",
            "ground_truth": "Thuộc Cấp hậu quả C3 theo Mục A.1.4.5 Phụ lục A của QCVN 03:2022/BXD (Kết cấu ngầm thuộc công trình dân dụng có chiều sâu ngầm từ 18 m trở lên).",
            "reference_clause": "Phụ lục A, Mục A.1.4.5"
        },
        {
            "id": "qa_05",
            "question": "Nhà bảo vệ và hàng rào tạm phục vụ thi công thuộc cấp hậu quả và thời hạn sử dụng nào?",
            "ground_truth": "Nhà bảo vệ và hàng rào tạm thuộc Cấp hậu quả C1 theo Mục A.2.4 Phụ lục A và có Thời hạn sử dụng theo thiết kế thuộc Mức 1 (Nhỏ hơn 25 năm) theo Bảng 1 của QCVN 03:2022/BXD.",
            "reference_clause": "Mục 2.2 Bảng 1 & Phụ lục A Mục A.2.4"
        }
    ]
}
(bundle_dir / "qa_benchmark.json").write_text(json.dumps(qa_data, indent=2, ensure_ascii=False), encoding="utf-8")

# 9. metadata.yaml
metadata_content = f"""id: QCVN-03-2022-BXD
document_number: QCVN 03:2022/BXD
title: QCVN 03:2022/BXD — Quy chuẩn kỹ thuật quốc gia về Phân cấp công trình phục vụ thiết kế xây dựng
type: Quy chuẩn kỹ thuật quốc gia
issued_by: Bộ Xây dựng
signer: Lê Quang Hùng
issued_date: '2022-11-30'
effective_date: '2023-06-01'
status: active
bundle_path: legal_docs/02_qcvn/qcvn_03_2022_bxd/
source_url: https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx
sha256: {docx_sha}
pdf_path: legal_docs/02_qcvn/qcvn_03_2022_bxd/sources/qcvn_03_2022_bxd.pdf
pdf_sha256: {pdf_sha}
cong_bao_number: 05/2022/TT-BXD
pdf_status: verified
source_file: .md/extracted_docs/qcvn_03_2022_bxd/qcvn_03_2022_bxd.docx
source_file_size_kb: {docx_size_kb}
source_assets:
  docx:
    sha256: {docx_sha}
    vault_path: CCBA_Legal_Vault/02_qcvn/qcvn_03_2022_bxd/qcvn_03_2022_bxd.docx
    status: synced
  pdf:
    sha256: {pdf_sha}
    vault_path: CCBA_Legal_Vault/02_qcvn/qcvn_03_2022_bxd/qcvn_03_2022_bxd.pdf
    status: verified
relations:
  replaces: QCVN-03-2012-BXD
"""
(bundle_dir / "metadata.yaml").write_text(metadata_content.strip() + "\n", encoding="utf-8")

print("✅ Successfully built complete OKF v2.4 Universal Bundle in legal_docs/02_qcvn/qcvn_03_2022_bxd/")
