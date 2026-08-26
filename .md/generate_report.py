import os
import docx
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = docx.Document()
    
    # Page setup (A4, standard margins: Top 2cm, Bottom 2cm, Left 2.5cm, Right 2cm)
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.0)
        
    def set_cell_border_none(cell):
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            '<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:top w:val="none"/>'
            '<w:left w:val="none"/>'
            '<w:bottom w:val="none"/>'
            '<w:right w:val="none"/>'
            '</w:tcBorders>'
        )
        tcPr.append(tcBorders)

    def set_cell_padding(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    # Style default
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.line_spacing = 1.2
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.space_before = Pt(0)

    # 1. Header Table (Quốc hiệu, Tên đơn vị)
    head_table = doc.add_table(rows=1, cols=2)
    head_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    head_table.autofit = False
    
    cell_l, cell_r = head_table.rows[0].cells
    cell_l.width = Cm(8.0)
    cell_r.width = Cm(8.5)
    set_cell_border_none(cell_l)
    set_cell_border_none(cell_r)
    
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.line_spacing = 1.15
    p_l.paragraph_format.space_after = Pt(2)
    r = p_l.add_run('VIỆN KHCN XÂY DỰNG\n')
    r.font.bold = True
    r.font.size = Pt(11.5)
    r = p_l.add_run('TRUNG TÂM TƯ VẤN VÀ\nỨNG DỤNG BIM TRONG XÂY DỰNG\n')
    r.font.bold = True
    r.font.size = Pt(11)
    r = p_l.add_run('Số: 16/2026/VKH-BIM/BCHT')
    r.font.italic = True
    r.font.size = Pt(12)
    
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.line_spacing = 1.15
    p_r.paragraph_format.space_after = Pt(2)
    r = p_r.add_run('CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n')
    r.font.bold = True
    r.font.size = Pt(12)
    r = p_r.add_run('Độc lập - Tự do - Hạnh phúc\n')
    r.font.bold = True
    r.font.size = Pt(13)
    r = p_r.add_run('----------o0o----------\n')
    r.font.size = Pt(9)
    r = p_r.add_run('Hà Nội, ngày 25 tháng 08 năm 2026')
    r.font.italic = True
    r.font.size = Pt(12.5)

    doc.add_paragraph() # Spacing

    # 2. Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    r = p_title.add_run('BÁO CÁO\n')
    r.font.bold = True
    r.font.size = Pt(15)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    r = p_sub.add_run('HOÀN THÀNH CÔNG TÁC GIÁM SÁT THI CÔNG XÂY DỰNG\nGIAI ĐOẠN PHẦN THÔ\n')
    r.font.bold = True
    r.font.size = Pt(13.5)
    r = p_sub.add_run('(Kèm theo Nghị định số 207/2026/NĐ-CP và Nghị định số 06/2021/NĐ-CP của Chính phủ)')
    r.font.italic = True
    r.font.size = Pt(11)

    # 3. Kính gửi
    p_kg = doc.add_paragraph()
    p_kg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_kg.paragraph_format.space_after = Pt(10)
    r = p_kg.add_run('Kính gửi: ')
    r.font.bold = True
    r = p_kg.add_run('Văn phòng Ban Cơ yếu Chính phủ (Chủ đầu tư)')
    r.font.bold = True

    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.first_line_indent = Cm(1.0)
    p_intro.paragraph_format.space_after = Pt(6)
    p_intro.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_intro.add_run('Viện Khoa học Công nghệ Xây dựng (Trung tâm Tư vấn và Ứng dụng BIM trong Xây dựng) báo cáo về công tác giám sát thi công xây dựng công trình ')
    r = p_intro.add_run('“Nhà điều hành, tác nghiệp của Ban Cơ yếu Chính phủ”')
    r.font.bold = True
    p_intro.add_run(' – Giai đoạn Phần thô (kết cấu bê tông cốt thép, tường xây bao che) như sau:')

    # 4. Căn cứ pháp lý
    p_cc_header = doc.add_paragraph()
    r = p_cc_header.add_run('I. CÁC CĂN CỨ PHÁP LÝ VÀ HỒ SƠ DỰ ÁN:')
    r.font.bold = True
    r.font.size = Pt(13)

    cancus = [
        'Luật Xây dựng số 50/2014/QH13 ngày 18/06/2014; Luật số 62/2020/QH14 ngày 17/06/2020 sửa đổi, bổ sung một số điều của Luật Xây dựng và Luật Xây dựng số 135/2025/QH15;',
        'Nghị định số 06/2021/NĐ-CP ngày 26/01/2021 của Chính phủ quy định chi tiết một số nội dung về quản lý chất lượng, thi công xây dựng và bảo trì công trình xây dựng; Nghị định số 207/2026/NĐ-CP ngày 15/06/2026 của Chính phủ;',
        'Nghị định số 175/2024/NĐ-CP ngày 30/12/2024 của Chính phủ quy định chi tiết một số điều và biện pháp thi hành Luật Xây dựng về quản lý hoạt động xây dựng;',
        'Thông tư số 10/2021/TT-BXD ngày 25/08/2021 và Thông tư số 32/2026/TT-BXD ngày 30/06/2026 của Bộ Xây dựng quy định chi tiết về quản lý chất lượng thi công xây dựng;',
        'Hệ thống Quy chuẩn kỹ thuật quốc gia (QCVN 06:2022/BXD, QCVN 02:2022/BXD...) và các Tiêu chuẩn kỹ thuật áp dụng cho dự án (TCVN 4453:1995, TCVN 5574:2018, TCVN 9340:2012, TCVN 8163:2009...);',
        'Hợp đồng kinh tế thực hiện công tác Tư vấn giám sát ký kết giữa Văn phòng Ban Cơ yếu Chính phủ và Viện Khoa học Công nghệ Xây dựng;',
        'Đề cương công tác Tư vấn giám sát đã được Chủ đầu tư phê duyệt;',
        'Hồ sơ thiết kế bản vẽ thi công phần kết cấu đã được Chủ đầu tư phê duyệt kèm Quyết định phê duyệt và đóng dấu “Bản vẽ thi công đã phê duyệt” theo quy định;',
        'Hồ sơ mời thầu, Hồ sơ dự thầu và Hợp đồng thi công xây dựng ký giữa Chủ đầu tư và các Nhà thầu thi công xây lắp;',
        'Các biên bản kiểm tra, nghiệm thu công việc xây dựng, kết quả thí nghiệm kiểm định và nhật ký thi công trên công trường.'
    ]
    for cc in cancus:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0.8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run('• ')
        r.font.bold = True
        r = p.add_run(cc)
        r.font.italic = True

    # 5. Thông tin chung
    p_info_header = doc.add_paragraph()
    p_info_header.paragraph_format.space_before = Pt(6)
    r = p_info_header.add_run('II. THÔNG TIN CHUNG DỰ ÁN VÀ CÁC CHỦ THỂ THAM GIA:')
    r.font.bold = True
    r.font.size = Pt(13)

    info_table = doc.add_table(rows=7, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ('1. Tên dự án / Công trình:', 'Xây dựng Nhà điều hành, tác nghiệp của Ban Cơ yếu Chính phủ'),
        ('2. Địa điểm xây dựng:', 'Số 107 Nguyễn Chí Thanh, phường Láng Thượng, quận Đống Đa, TP. Hà Nội'),
        ('3. Chủ đầu tư:', 'Văn phòng / Ban Cơ yếu Chính phủ'),
        ('4. Nhà thầu Thiết kế:', 'Công ty Tư vấn Thiết kế và Đầu tư Xây dựng – BQP'),
        ('5. Nhà thầu Thẩm tra thiết kế:', 'Viện Kỹ thuật Công trình Đặc biệt'),
        ('6. Nhà thầu Tư vấn Giám sát:', 'Viện Khoa học Công nghệ Xây dựng (Trung tâm TV & UD BIM trong XD)'),
        ('7. Các Nhà thầu Thi công:', 
         '• Gói thầu XL-01 (Xây dựng công trình & HTKT): Tổng công ty Thành An\n'
         '• Gói thầu XL-02 (PCCC): Công ty Cổ phần ZME\n'
         '• Gói thầu XL-03 (Hệ thống M&E): Công ty TNHH Cơ điện Miền Bắc Việt Nam\n'
         '• Gói thầu XL-04 (Máy phát điện & Trạm biến áp): Liên danh Letuv Việt Nam & Invico\n'
         '• Gói thầu XL-05 (Trạm xử lý nước thải): Công ty Cổ phần Công nghệ Farich Việt Nam')
    ]
    for idx, (label, val) in enumerate(info_data):
        row = info_table.rows[idx]
        cell_0, cell_1 = row.cells
        cell_0.width = Cm(4.5)
        cell_1.width = Cm(12.0)
        
        tcPr0 = cell_0._tc.get_or_add_tcPr()
        tcPr1 = cell_1._tc.get_or_add_tcPr()
        borders = parse_xml(
            '<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            '<w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            '<w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            '</w:tcBorders>'
        )
        tcPr0.append(parse_xml('<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/></w:tcBorders>'))
        tcPr1.append(parse_xml('<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/></w:tcBorders>'))
        set_cell_padding(cell_0, 80, 80, 100, 100)
        set_cell_padding(cell_1, 80, 80, 100, 100)
        
        p0 = cell_0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(12)
        
        p1 = cell_1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.size = Pt(12)

    # 6. Nội dung báo cáo 12 mục
    p_body_header = doc.add_paragraph()
    p_body_header.paragraph_format.space_before = Pt(12)
    r = p_body_header.add_run('III. NỘI DUNG BÁO CÁO CHI TIẾT (Theo Phụ lục IVb – Nghị định 207/2026/NĐ-CP):')
    r.font.bold = True
    r.font.size = Pt(13)

    sections = [
        ('1. Quy mô công trình và hạng mục giai đoạn phần thô:', [
            ('a) Mô tả quy mô và công năng:', 
             '• Khối Nhà làm việc cơ quan: Xây dựng mới 08 tầng nổi, tổng diện tích sàn khoảng 28.895 m².\n'
             '• Khối Hội trường và Nhà ăn: Xây dựng mới 02 tầng nổi, quy mô Hội trường 500 chỗ và khu vực Nhà ăn, tổng diện tích sàn khoảng 3.138 m².\n'
             '• Tầng hầm: Bố trí 01 tầng hầm dùng chung kết nối các khối công trình, tổng diện tích sàn khoảng 7.090 m².\n'
             '• Các hạng mục phụ trợ: Nhà trực ban, Nhà để xe, Cổng chính & Nhà bảo vệ, Cổng phụ, Nhà điều hành trạm xử lý nước thải và Nhà thu gom rác (tổng diện tích khoảng 262 m²).\n'
             '• Công trình cải tạo: Cải tạo Nhà để máy phát điện hiện hữu, tổng diện tích sàn khoảng 270 m².\n'
             '• Hạ tầng kỹ thuật & Thiết bị: Đầu tư đồng bộ hệ thống cấp điện, cấp thoát nước ngoài nhà, PCCC, chống sét, thang máy, trạm biến áp, máy phát điện, điều hòa không khí, thông gió và hạ tầng cảnh quan sân đường nội bộ.'),
            ('b) Đánh giá sự phù hợp về quy mô, công năng phần thô:',
             'Quy mô hình học, kết cấu chịu lực (cột, dầm, sàn, vách bê tông cốt thép, tường xây bao che) hoàn thành thi công hoàn toàn phù hợp với Giấy phép xây dựng, Quyết định phê duyệt dự án, Hồ sơ thiết kế bản vẽ thi công được duyệt, Chỉ dẫn kỹ thuật và các Quy chuẩn, Tiêu chuẩn xây dựng hiện hành.')
        ]),
        ('2. Đánh giá sự phù hợp về năng lực của các nhà thầu thi công xây dựng so với HSDT và hợp đồng:', [
            ('a) Nhân lực của Nhà thầu thi công:',
             'Nhà thầu (Tổng công ty Thành An và các nhà thầu chuyên ngành) đã bố trí đầy đủ sơ đồ tổ chức Ban chỉ huy công trường, danh sách nhân sự chủ chốt. Các vị trí Chỉ huy trưởng, kỹ sư phụ trách kết cấu và cán bộ an toàn (HSE) đều có chứng chỉ hành nghề phù hợp, đủ năng lực quản lý. Số lượng công nhân kỹ thuật, thợ cốp pha, cốt thép, thợ nề cơ bản đáp ứng yêu cầu thi công; tuy nhiên tại một số thời điểm cao điểm, việc huy động nhân lực có lúc chưa thực sự bám sát biểu đồ tiến độ.'),
            ('b) Thiết bị thi công trên công trường:',
             'Nhà thầu đã huy động đầy đủ máy móc, thiết bị chính phục vụ thi công phần thô (Cần trục tháp, vận thăng lồng, máy bơm bê tông tĩnh/cần, máy đầm cóc, đầm dùi, máy hàn, cốp pha định hình...). Toàn bộ thiết bị có yêu cầu nghiêm ngặt về an toàn đều có hồ sơ kiểm định kỹ thuật còn hiệu lực và được bảo dưỡng định kỳ.'),
            ('c) Phòng thí nghiệm chuyên ngành xây dựng (LAS-XD):',
             'Nhà thầu liên kết với phòng thí nghiệm chuyên ngành xây dựng hợp chuẩn, được Bộ Xây dựng cấp phép, có đầy đủ năng lực thực hiện các phép thử cơ lý vật liệu (thép xây dựng, bê tông thương phẩm, xi măng, cát, đá, gạch xây, vữa xây trát...).'),
            ('d) Hệ thống quản lý chất lượng của Nhà thầu:',
             'Nhà thầu đã thiết lập hệ thống quản lý chất lượng (QA/QC), quy trình kiểm soát nội bộ và kế hoạch kiểm tra chất lượng. Công tác lập và lưu trữ hồ sơ nghiệm thu cơ bản đáp ứng yêu cầu, TVGS đã thường xuyên đôn đốc cập nhật hồ sơ kịp thời.')
        ]),
        ('3. Đánh giá về khối lượng, tiến độ hoàn thành, tổ chức thi công và an toàn lao động:', [
            ('a) Đánh giá khối lượng công việc hoàn thành:',
             'TVGS đã kiểm tra, đối soát và xác nhận khối lượng hoàn thành thực tế giai đoạn phần thô theo đúng hồ sơ thiết kế và hợp đồng. Toàn bộ các cấu kiện chịu lực bê tông cốt thép ngầm và phần thân, tường xây đã được kiểm tra hình học, cao độ, tim trục, không có sai lệch kỹ thuật.'),
            ('b) Đánh giá về tiến độ thi công:',
             'Tiến độ thực hiện gói thầu XL-01 của Nhà thầu Tổng công ty Thành An hiện chậm khoảng 90 ngày so với tiến độ tổng thể ban đầu được phê duyệt. Nguyên nhân chủ yếu do năng lực tổ chức thực hiện, điều phối cung ứng vật tư, thiết bị và duy trì lực lượng nhân công tại một số giai đoạn chưa đạt yêu cầu kế hoạch đề ra. TVGS đã phát hành văn bản cảnh báo và yêu cầu Nhà thầu lập biện pháp thi công bù tiến độ ở các giai đoạn tiếp theo.'),
            ('c) Đánh giá công tác tổ chức thi công:',
             'Mặt bằng thi công được tổ chức cơ bản hợp lý, tuân thủ biện pháp tổ chức thi công được phê duyệt. Công tác phối hợp thi công giữa các nhà thầu kết cấu và nhà thầu cơ điện (chờ lỗ mở, đặt ống kỹ thuật MEP) được giám sát chặt chẽ.'),
            ('d) Công tác an toàn lao động, vệ sinh môi trường (HSE):',
             'Nhà thầu đã duy trì các biện pháp an toàn lao động trên công trường: Trang bị đầy đủ bảo hộ lao động (PPE), lắp dựng lưới chống rơi chu vi công trình, rào chắn lan can an toàn tại các lỗ mở sàn, giếng thang máy, cầu thang bộ. Đội ngũ an toàn viên thường xuyên kiểm tra công tác hàn cắt, an toàn điện tạm. Trong suốt giai đoạn thi công phần thô không xảy ra sự cố hay tai nạn lao động.')
        ]),
        ('4. Đánh giá công tác thí nghiệm, kiểm tra vật liệu, cấu kiện và thiết bị lắp đặt:', [
            ('Nội dung kiểm soát:',
             '• Kiểm tra nguồn gốc xuất xứ (CO/CQ): 100% vật tư đầu vào (cốt thép Hòa Phát/Việt Đức, xi măng, cát, đá, phụ gia bê tông, gạch xây không nung/gạch đất sét nung...) đều có đầy đủ chứng chỉ xuất xưởng, nguồn gốc rõ ràng trước khi đưa vào công trường.\n'
             '• Công tác lấy mẫu và thí nghiệm: Toàn bộ công tác lấy mẫu tại hiện trường đều có sự chứng kiến và ký biên bản lấy mẫu của Kỹ sư TVGS. Các tổ mẫu bê tông (R7, R28), mẫu kéo uốn cốt thép, mối nối cốt thép, mẫu vữa xây đều được thí nghiệm tại phòng LAS-XD hợp chuẩn. 100% kết quả thí nghiệm đạt yêu cầu cường độ thiết kế và tiêu chuẩn áp dụng.')
        ]),
        ('5. Đánh giá về công tác kiểm định, quan trắc và thí nghiệm đối chứng:', [
            ('Nội dung thực hiện:',
             'Công trình không thuộc trường hợp phải thực hiện quan trắc lún, nghiêng đặc biệt theo yêu cầu của hồ sơ thiết kế và quy định kỹ thuật hiện hành đối với giai đoạn này. Các số liệu đo trắc địa định vị tim trục, cao độ kết cấu dầm sàn từng tầng do Nhà thầu thực hiện đều được TVGS kiểm tra đo đạc đối chứng bằng máy toàn đạc điện tử và thủy bình đạt độ chính xác cho phép.')
        ]),
        ('6. Đánh giá công tác tổ chức nghiệm thu công việc xây dựng và nghiệm thu giai đoạn:', [
            ('Nội dung thực hiện:',
             '• Quy trình nghiệm thu: Thực hiện nghiêm ngặt quy trình nghiệm thu 2 bước (Nhà thầu nghiệm thu nội bộ đạt yêu cầu mới gửi phiếu yêu cầu nghiệm thu cho TVGS).\n'
             '• Nghiệm thu công tác khuất: Các công tác cốt thép móng, dầm sàn, cột, vách trước khi đổ bê tông đều được TVGS kiểm tra tỉ mỉ về đường kính, khoảng cách đai, số lượng thanh thép, chiều dày lớp bê tông bảo vệ và vệ sinh trước khi ký chấp thuận đổ bê tông.\n'
             '• Biên bản nghiệm thu: Lập đầy đủ theo mẫu chuẩn, có chữ ký xác nhận của các kỹ sư giám sát và chỉ huy kỹ thuật trực tiếp.\n'
             '• Bản vẽ hoàn công giai đoạn phần thô: Nhà thầu đã lập bản vẽ hoàn công kết cấu đúng kích thước hình học thực tế, được TVGS kiểm tra ký xác nhận.')
        ]),
        ('7. Các thay đổi thiết kế và việc thẩm định, phê duyệt thiết kế điều chỉnh (nếu có):', [
            ('Nội dung xử lý:',
             'Trong quá trình thi công phần thô, một số điều chỉnh chi tiết cấu tạo cục bộ nhằm xử lý giao cắt kỹ thuật và tăng tính thuận tiện thi công đã được xử lý qua phiếu yêu cầu làm rõ (RFI). Các thay đổi này không làm thay đổi tải trọng thiết kế, giải pháp kết cấu chịu lực chính của công trình và đều được Nhà thầu Thiết kế, TVGS và Chủ đầu tư thống nhất chấp thuận.')
        ]),
        ('8. Những tồn tại, khiếm khuyết về chất lượng, sự cố công trình và kết quả khắc phục:', [
            ('Nội dung đánh giá:',
             'Trong suốt quá trình thi công giai đoạn phần thô, TVGS thực hiện giám sát liên tục tại hiện trường, kiểm soát chặt chẽ quy trình đổ và đầm bê tông, bảo dưỡng bê tông ẩm đúng quy định. Không ghi nhận sự cố công trình hay khiếm khuyết lớn về an toàn chịu lực. Một số hiện tượng rỗ bề mặt hoặc nứt co ngót bề mặt nhỏ cục bộ đã được TVGS lập phiếu yêu cầu (NCR) và Nhà thầu đã xử lý dứt điểm bằng vữa sửa chữa chuyên dụng (Sika Grout), được TVGS nghiệm thu đạt 100%.')
        ]),
        ('9. Đánh giá sự phù hợp của hồ sơ quản lý chất lượng:', [
            ('Nội dung hồ sơ:',
             'Hồ sơ quản lý chất lượng giai đoạn phần thô được Nhà thầu lập đầy đủ, sắp xếp khoa học theo đúng quy định tại Nghị định số 06/2021/NĐ-CP (và Nghị định 207/2026/NĐ-CP), Thông tư 10/2021/TT-BXD, bao gồm: Nhật ký thi công công trình, Biên bản nghiệm thu công việc xây dựng, Phiếu kết quả thí nghiệm vật liệu, Chứng chỉ xuất xưởng, Bản vẽ hoàn công phần kết cấu. Hồ sơ phản ánh trung thực quá trình thi công và đủ điều kiện lưu trữ theo quy định.')
        ]),
        ('10. Đánh giá về an toàn PCCC, bảo vệ môi trường và pháp luật liên quan:', [
            ('Nội dung tuân thủ:',
             '• An toàn PCCC: Công trường đã thành lập Đội PCCC cơ sở, trang bị bình chữa cháy bột/CO2 tại các khu vực gia công cốt thép, trạm điện tạm, kho vật tư. Đảm bảo kích thước và giải pháp kết cấu bảo vệ cấu kiện chịu lực theo bậc chịu lửa thiết kế PCCC.\n'
             '• Bảo vệ môi trường: Bụi và tiếng ồn trong quá trình đổ bê tông và xây tường được kiểm soát; nước rửa bồn bê tông được lắng lọc; phế thải xây dựng (cốp pha vụn, bao bì, đầu mẩu thép) được thu gom và vận chuyển xử lý theo đúng quy định.')
        ]),
        ('11. Đánh giá về sự phù hợp của quy trình vận hành, bảo trì công trình:', [
            ('Nội dung thực hiện:',
             'Quy trình bảo trì kết cấu công trình đã được Nhà thầu thiết kế lập trong hồ sơ thiết kế bản vẽ thi công được duyệt, bảo đảm tính khả thi và tuân thủ các quy định hiện hành.')
        ]),
        ('12. Đánh giá về các điều kiện nghiệm thu hoàn thành giai đoạn phần thô:', [
            ('Đánh giá tổng hợp và kết luận:',
             '• Toàn bộ các công việc xây dựng thuộc giai đoạn phần thô (kết cấu bê tông cốt thép, tường xây bao che) của khối Nhà làm việc cơ quan 8 tầng, khối Hội trường 2 tầng, tầng hầm và các công trình phụ trợ đã được thi công hoàn thành theo đúng hồ sơ thiết kế được duyệt và chỉ dẫn kỹ thuật.\n'
             '• Chất lượng thi công bảo đảm an toàn chịu lực, độ bền vững, mỹ quan kỹ thuật và đáp ứng đầy đủ các tiêu chuẩn hiện hành.\n'
             '• Hồ sơ nghiệm thu chất lượng, kết quả thí nghiệm vật liệu và bản vẽ hoàn công giai đoạn phần thô đã được hoàn thành đầy đủ, hợp lệ.\n'
             '• KẾT LUẬN: ĐỦ ĐIỀU KIỆN ĐỂ TỔ CHỨC NGHIỆM THU HOÀN THÀNH GIAI ĐOẠN PHẦN THÔ VÀ CHUYỂN BƯỚC SANG THI CÔNG GIAI ĐOẠN HOÀN THIỆN VÀ LẮP ĐẶT HỆ THỐNG CƠ ĐIỆN (MEP).')
        ])
    ]

    for title, subs in sections:
        p_sec = doc.add_paragraph()
        p_sec.paragraph_format.space_before = Pt(8)
        p_sec.paragraph_format.space_after = Pt(2)
        r = p_sec.add_run(title)
        r.font.bold = True
        r.font.size = Pt(12.5)
        
        for sub_title, sub_content in subs:
            if len(subs) > 1:
                p_sub_t = doc.add_paragraph()
                p_sub_t.paragraph_format.first_line_indent = Cm(0.5)
                p_sub_t.paragraph_format.space_after = Pt(2)
                r_st = p_sub_t.add_run(sub_title)
                r_st.font.bold = True
                r_st.font.size = Pt(12)
                
            p_sub_c = doc.add_paragraph()
            p_sub_c.paragraph_format.first_line_indent = Cm(0.8)
            p_sub_c.paragraph_format.space_after = Pt(4)
            p_sub_c.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r_sc = p_sub_c.add_run(sub_content)
            r_sc.font.size = Pt(12.5)

    # 7. Kiến nghị
    p_rec = doc.add_paragraph()
    p_rec.paragraph_format.space_before = Pt(8)
    r = p_rec.add_run('IV. KIẾN NGHỊ VỚI CHỦ ĐẦU TƯ:')
    r.font.bold = True
    r.font.size = Pt(13)

    p_rec_c = doc.add_paragraph()
    p_rec_c.paragraph_format.first_line_indent = Cm(0.8)
    p_rec_c.paragraph_format.space_after = Pt(6)
    p_rec_c.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_rec_c.add_run('1. Kính đề nghị Văn phòng Ban Cơ yếu Chính phủ (Chủ đầu tư) chủ trì tổ chức cuộc họp và tiến hành ký ')
    r = p_rec_c.add_run('Biên bản nghiệm thu hoàn thành giai đoạn phần thô')
    r.font.bold = True
    p_rec_c.add_run(' công trình để làm cơ sở cho các Nhà thầu triển khai thi công giai đoạn hoàn thiện và cơ điện (MEP).\n'
                    '2. Đề nghị Chủ đầu tư tiếp tục đôn đốc Nhà thầu Tổng công ty Thành An tập trung tối đa nguồn lực nhân sự, vật tư thiết bị để đẩy nhanh tiến độ thi công bù vào khoảng thời gian đã bị chậm trễ.')

    p_thanks = doc.add_paragraph()
    p_thanks.paragraph_format.first_line_indent = Cm(0.8)
    p_thanks.paragraph_format.space_after = Pt(14)
    r = p_thanks.add_run('Trân trọng cảm ơn!./.')
    r.font.italic = True

    # 8. Chữ ký Table
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False
    
    cell_sl, cell_sr = sig_table.rows[0].cells
    cell_sl.width = Cm(8.0)
    cell_sr.width = Cm(8.5)
    set_cell_border_none(cell_sl)
    set_cell_border_none(cell_sr)

    p_sl = cell_sl.paragraphs[0]
    p_sl.paragraph_format.line_spacing = 1.15
    p_sl.paragraph_format.space_after = Pt(2)
    r = p_sl.add_run('Nơi nhận:\n')
    r.font.bold = True
    r.font.size = Pt(11)
    r = p_sl.add_run('• Như kính gửi;\n• Ban Giám đốc Viện (để b/c);\n• Phòng Kế hoạch – Quản lý KT;\n• Lưu: VP, TVGS-BIM.\n\n')
    r.font.italic = True
    r.font.size = Pt(10)
    r = p_sl.add_run('GIÁM SÁT TRƯỞNG\n\n\n\n\n')
    r.font.bold = True
    r.font.size = Pt(12.5)
    r = p_sl.add_run('Hà Thanh Tùng')
    r.font.bold = True
    r.font.size = Pt(13)

    p_sr = cell_sr.paragraphs[0]
    p_sr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sr.paragraph_format.line_spacing = 1.15
    p_sr.paragraph_format.space_after = Pt(2)
    r = p_sr.add_run('TRUNG TÂM TƯ VẤN VÀ ỨNG DỤNG\nBIM TRONG XÂY DỰNG\n')
    r.font.bold = True
    r.font.size = Pt(12)
    r = p_sr.add_run('GIÁM ĐỐC\n\n\n\n\n')
    r.font.bold = True
    r.font.size = Pt(12.5)
    r = p_sr.add_run('Vũ Văn Chủ')
    r.font.bold = True
    r.font.size = Pt(13)

    # Save paths
    out_dir_reports = os.path.abspath(r'd:\GitHubProjects\ccba-legal-knowledge\.md\reports')
    os.makedirs(out_dir_reports, exist_ok=True)
    out_docx_repo = os.path.join(out_dir_reports, '20260824_BC_hoan_thanh_giam_sat_GD_Phan_Tho_Ban_Co_Yeu.docx')
    
    out_downloads = os.path.abspath(r'C:\Users\chuvu\Downloads\20260824_BC_hoan_thanh_giam_sat_GD_Phan_Tho_Ban_Co_Yeu.docx')
    
    doc.save(out_docx_repo)
    try:
        doc.save(out_downloads)
    except Exception as e:
        print('Could not save to downloads:', e)
        
    print('SUCCESS: Generated DOCX at:', out_docx_repo)
    print('SUCCESS: Generated DOCX at:', out_downloads)

if __name__ == '__main__':
    create_report()
