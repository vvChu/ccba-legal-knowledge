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
    r = p_sub.add_run('(Theo Phụ lục IVb ban hành kèm theo Nghị định số 207/2026/NĐ-CP của Chính phủ)')
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
        'Luật Xây dựng số 135/2025/QH15 ngày 10/12/2025 của Quốc hội (có hiệu lực thi hành từ ngày 01/07/2026);',
        'Nghị định số 207/2026/NĐ-CP ngày 15/06/2026 của Chính phủ về quản lý chất lượng, thi công xây dựng và bảo trì công trình xây dựng (có hiệu lực thi hành từ ngày 01/07/2026);',
        'Nghị định số 217/2026/NĐ-CP ngày 19/06/2026 của Chính phủ về quản lý dự án đầu tư xây dựng (có hiệu lực thi hành từ ngày 01/07/2026);',
        'Thông tư số 32/2026/TT-BXD ngày 30/06/2026 của Bộ Xây dựng quy định chi tiết một số điều của Nghị định số 207/2026/NĐ-CP về quản lý chất lượng thi công xây dựng (có hiệu lực thi hành từ ngày 01/07/2026);',
        'Hệ thống Quy chuẩn kỹ thuật quốc gia (QCVN 06:2022/BXD, QCVN 02:2022/BXD...) và các Tiêu chuẩn kỹ thuật thi công, nghiệm thu áp dụng cho dự án (TCVN 4453:1995, TCVN 5574:2018, TCVN 9340:2012, TCVN 8163:2009...);',
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

    # 6. Nội dung báo cáo 13 mục chuẩn mực theo Phụ lục IVb
    p_body_header = doc.add_paragraph()
    p_body_header.paragraph_format.space_before = Pt(12)
    r = p_body_header.add_run('III. NỘI DUNG BÁO CÁO CHI TIẾT (Theo Phụ lục IVb – Nghị định 207/2026/NĐ-CP):')
    r.font.bold = True
    r.font.size = Pt(13)

    sections = [
        ('1. Quy mô công trình và hạng mục giai đoạn phần thô:', [
            ('a) Mô tả quy mô và công năng của các phần hoặc hạng mục công trình:', 
             '• Khối Nhà làm việc cơ quan (Khối chính): Xây dựng mới 08 tầng nổi, kết cấu khung - vách bê tông cốt thép toàn khối, tổng diện tích sàn xây dựng khoảng 28.895 m². Bố trí các phòng làm việc lãnh đạo, khối làm việc chuyên môn nghiệp vụ cơ yếu, phòng khánh tiết, trung tâm dữ liệu kỹ thuật mật mã và các phòng kỹ thuật phụ trợ.\n'
             '• Khối Hội trường và Nhà ăn: Xây dựng mới 02 tầng nổi, tổng diện tích sàn khoảng 3.138 m². Tầng 1 bố trí khu nhà ăn tập thể phục vụ cán bộ công nhân viên; Tầng 2 bố trí Hội trường đa năng quy mô 500 chỗ ngồi với khẩu độ kết cấu vượt nhịp lớn.\n'
             '• Tầng hầm chung: Bố trí 01 tầng hầm liên thông kết nối dưới khối Nhà làm việc và khối Hội trường, tổng diện tích sàn hầm khoảng 7.090 m². Công năng chính làm bãi đỗ xe ô tô, xe máy, trạm biến áp ngầm, phòng máy bơm PCCC & cấp nước sinh hoạt, bể nước ngầm sinh hoạt và bể ngầm PCCC.\n'
             '• Các hạng mục công trình phụ trợ: Xây dựng mới Nhà trực ban, Nhà để xe, Cổng chính & Nhà bảo vệ, Cổng phụ, Nhà điều hành trạm xử lý nước thải và Nhà thu gom rác trung chuyển (tổng diện tích xây dựng khoảng 262 m²).\n'
             '• Công trình cải tạo: Cải tạo hoàn thiện Nhà để máy phát điện dự phòng hiện hữu (tổng diện tích sàn khoảng 270 m²).\n'
             '• Hạ tầng kỹ thuật & Hệ thống thiết bị phụ trợ: Hệ thống cấp điện mạng ngoài, hệ thống cấp thoát nước mạng ngoài, trạm biến áp, máy phát điện dự phòng, hệ thống điều hòa không khí và thông gió (HVAC), thang máy, hệ thống phòng cháy chữa cháy (PCCC), hệ thống xử lý nước thải công nghệ tiên tiến, tường rào bảo vệ, đường giao thông nội bộ, sân bê tông và cây xanh cảnh quan.'),
            ('b) Đánh giá sự phù hợp về quy mô, công năng phần thô:',
             'Quy mô hình học, vị trí tim trục công trình, cao độ các tầng sàn, kích thước tiết diện cấu kiện chịu lực (móng, cột, dầm, sàn, vách, bể ngầm, tường xây bao che) thi công thực tế hoàn toàn phù hợp với Giấy phép xây dựng số [...], Quyết định đầu tư, Hồ sơ thiết kế bản vẽ thi công được duyệt, Chỉ dẫn kỹ thuật dự án và các Quy chuẩn kỹ thuật quốc gia (QCVN 02:2022/BXD, QCVN 06:2022/BXD), Tiêu chuẩn thiết kế kết cấu (TCVN 5574:2018, TCVN 2737:2023).')
        ]),
        ('2. Đánh giá sự phù hợp về năng lực của các nhà thầu thi công xây dựng so với HSDT và hợp đồng:', [
            ('a) Nhân lực của các Nhà thầu thi công:',
             'Nhà thầu chính (Tổng công ty Thành An - Gói XL-01) và các Nhà thầu chuyên ngành (ZME - XL-02, Cơ điện Miền Bắc - XL-03, Liên danh Letuv & Invico - XL-04, Farich - XL-05) đã thành lập và duy trì Ban chỉ huy công trường tại hiện trường. Các nhân sự chủ chốt gồm: Chỉ huy trưởng công trình, Giám đốc dự án, Kỹ sư trưởng kết cấu, Kỹ sư trắc đạc, Kỹ sư phụ trách QA/QC, Cán bộ an toàn lao động chuyên trách (HSE) đều có đầy đủ văn bằng chuyên môn, chứng chỉ hành nghề hoạt động xây dựng phù hợp với cấp công trình và được Chủ đầu tư/TVGS chấp thuận bằng văn bản. Lực lượng công nhân kỹ thuật (thợ cốt thép, thợ cốp pha, thợ nề, thợ hàn 3G/4G, thợ điện nước) được bố trí đầy đủ về chủng loại tay nghề. Tuy nhiên, tại một số thời điểm cao điểm đẩy nhanh tiến độ đổ bê tông sàn các tầng, việc huy động quân số công nhân của Tổng công ty Thành An có lúc chưa thực sự bám sát biểu đồ nhân lực cam kết, TVGS đã kịp thời đôn đốc chấn chỉnh và bổ sung.'),
            ('b) Máy móc, thiết bị thi công trên công trường:',
             'Toàn bộ thiết bị chính phục vụ thi công giai đoạn phần thô gồm: Cần trục tháp (02 bộ), Vận thăng lồng chở người và vật liệu (02 bộ), Trạm bơm bê tông tĩnh & Xe bơm cần chuyên dụng, Máy đầm bàn, đầm dùi, Máy cắt uốn thép, Máy hàn hồ quang, Hệ thống cốp pha nhôm/cốp pha phủ phim định hình chất lượng cao, Hệ giàn giáo chịu lực Ringlock/giáo nêm hoàn chỉnh. Toàn bộ các thiết bị nâng hạ có yêu cầu nghiêm ngặt về an toàn lao động (cần trục tháp, vận thăng lồng) đều có Giấy chứng nhận kiểm định kỹ thuật an toàn của Trung tâm kiểm định được cấp phép còn thời hạn hiệu lực, nhật ký vận hành và biên bản bảo dưỡng định kỳ đầy đủ.'),
            ('c) Phòng thí nghiệm chuyên ngành xây dựng (LAS-XD):',
             'Nhà thầu đã hợp đồng và sử dụng Phòng thí nghiệm chuyên ngành xây dựng hợp chuẩn LAS-XD (được Bộ Xây dựng cấp Giấy chứng nhận đủ điều kiện hoạt động thí nghiệm chuyên ngành xây dựng). Phòng thí nghiệm có đủ trang thiết bị chuẩn, nhân lực thí nghiệm viên có chứng chỉ chuyên môn để thực hiện đầy đủ các chỉ tiêu cơ lý của vật liệu, cấu kiện cho dự án.'),
            ('d) Hệ thống quản lý chất lượng (QA/QC) của Nhà thầu:',
             'Nhà thầu đã ban hành và triển khai áp dụng Hệ thống quản lý chất lượng nội bộ, Quy trình kiểm soát chất lượng từ khâu kiểm tra vật tư đầu vào, kiểm tra cốt pha, cốt thép đến quy trình đổ, đầm, bảo dưỡng bê tông và tháo dỡ cốp pha. Đội ngũ cán bộ kiểm soát chất lượng (QC) thường xuyên có mặt tại hiện trường để phối hợp với Kỹ sư TVGS kiểm tra nội bộ trước khi gửi phiếu yêu cầu nghiệm thu chính thức.')
        ]),
        ('3. Đánh giá về khối lượng, tiến độ hoàn thành, tổ chức thi công và an toàn lao động:', [
            ('a) Đánh giá khối lượng công việc hoàn thành giai đoạn phần thô:',
             'TVGS đã tiến hành đo đạc, kiểm tra hình học và xác nhận khối lượng thực tế hoàn thành cho giai đoạn phần thô, bao gồm: Khối lượng bê tông thương phẩm móng, vách hầm, dầm, sàn, cột các tầng đã đổ; Khối lượng cốt thép các loại gia công, lắp dựng nghiệm thu; Khối lượng cốp pha lắp dựng, tháo dỡ; Khối lượng tường xây gạch bao che, tường ngăn các tầng; Khối lượng cọc khoan nhồi, tường vây ngầm (phần kết nối kết cấu ngầm) đã hoàn thành 100%. Toàn bộ khối lượng thi công thực tế đều phù hợp với hồ sơ thiết kế bản vẽ thi công được duyệt, không có khối lượng phát sinh ngoài thiết kế chưa được chấp thuận.'),
            ('b) Đánh giá về tiến độ thi công:',
             'Tiến độ thực tế thi công gói thầu XL-01 của Nhà thầu Tổng công ty Thành An tại thời điểm kết thúc giai đoạn phần thô đang chậm khoảng 90 ngày so với biểu đồ tiến độ tổng thể ban đầu được phê duyệt trong Hợp đồng. Nguyên nhân chủ yếu xuất phát từ năng lực tổ chức điều hành của Nhà thầu trong một số thời điểm (việc huy động nhân lực chưa tập trung cao độ, việc điều phối chuỗi cung ứng vật tư thép và bê tông vào ban đêm trong khu vực nội đô Hà Nội gặp khó khăn về luồng giao thông vận tải, điều kiện thời tiết mưa bão kéo dài). TVGS đã làm việc với Ban chỉ huy công trường của Thành An, phát hành văn bản đôn đốc và yêu cầu Nhà thầu lập Kế hoạch thi công chi tiết bù tiến độ cho các giai đoạn hoàn thiện và MEP tiếp theo (tăng ca, tăng kíp, bổ sung nhân lực hoàn thiện mặt ngoài và nội thất).'),
            ('c) Đánh giá công tác tổ chức thi công:',
             'Mặt bằng tổng thể công trường được bố trí khoa học: Khu vực kho bãi tập kết sắt thép, bãi gia công cốp pha, vị trí trạm biến áp thi công, vị trí cần trục tháp và vận thăng đảm bảo bán kính hoạt động an toàn và không gây cản trở giao thông đô thị xung quanh số 107 Nguyễn Chí Thanh. Công tác phối hợp thi công giữa gói thầu xây dựng (XL-01) với các gói thầu cơ điện MEP (XL-03), PCCC (XL-02) và trạm xử lý nước thải (XL-05) được điều phối nhịp nhàng; toàn bộ các vị trí chờ ống luồn, sleeve kỹ thuật, hộp chờ điện nước xuyên sàn, xuyên vách bê tông hầm đều được định vị chính xác trước khi đổ bê tông.'),
            ('d) Công tác bảo đảm an toàn lao động và vệ sinh môi trường (HSE):',
             'Công trường được che chắn toàn bộ chu vi bằng hệ lưới an toàn chống rơi; các mép sàn biên, giếng thang máy, lỗ mở kỹ thuật đều được lắp đặt lan can an toàn cao tối thiểu 1.1m có thanh chắn chân (toe-board) và biển cảnh báo nguy hiểm. 100% cán bộ, công nhân ra vào công trường đều được huấn luyện an toàn lao động, trang bị đầy đủ phương tiện bảo vệ cá nhân (mũ bảo hộ, giày mũi sắt, áo phản quang, dây an toàn 2 móc khi làm việc trên cao). Đội ngũ HSE thường xuyên kiểm tra an toàn hệ thống điện thi công (sử dụng tủ điện thi công có aptomat chống giật ELCB, dây cáp bọc cao su cách điện kép). Trong suốt quá trình thi công giai đoạn phần thô, không để xảy ra bất kỳ sự cố hay tai nạn lao động nào.')
        ]),
        ('4. Đánh giá công tác thí nghiệm, kiểm tra vật liệu, sản phẩm xây dựng, cấu kiện, thiết bị lắp đặt:', [
            ('Nội dung kiểm soát:',
             '• Kiểm soát nguồn gốc vật liệu đầu vào: 100% các chủng loại vật liệu chính đưa vào thi công phần thô (thép xây dựng Hòa Phát/Việt Đức, xi măng Nghi Sơn/Bút Sơn, cát vàng sông Lô, đá dăm nghiền Hà Nam, phụ gia bê tông Sika, gạch xây không nung/gạch đất sét nung tuynel...) đều được kiểm tra hồ sơ xuất xưởng (CO/CQ), chứng chỉ hợp chuẩn hợp quy và nghiệm thu đầu vào bởi Kỹ sư TVGS trước khi cho phép tập kết vào công trường.\n'
             '• Kế hoạch thí nghiệm và kết quả thử nghiệm: Công tác lấy mẫu thí nghiệm hiện trường được thực hiện theo đúng Kế hoạch tổ chức thí nghiệm đã được Chủ đầu tư phê duyệt, có sự chứng kiến và ký biên bản lấy mẫu của Kỹ sư TVGS. Các tổ mẫu bê tông (mỗi tổ 03 viên) tại các độ tuổi R7, R28 đều đạt và vượt cường độ thiết kế (Mác B30/C30, B35/C35). Các tổ mẫu kéo, uốn, thử mối nối ren cơ khí (coupler) và mối hàn cốt thép đều đạt giới hạn chảy, giới hạn bền và độ giãn dài tương đối theo tiêu chuẩn TCVN 1651:2018 và TCVN 8163:2009. Kết quả kiểm tra cường độ nén, uốn của gạch và vữa xây xi măng mác M75/M100 đều đáp ứng đúng yêu cầu của chỉ dẫn kỹ thuật.')
        ]),
        ('5. Đánh giá về công tác tổ chức và kết quả kiểm định, quan trắc, thí nghiệm đối chứng:', [
            ('Nội dung thực hiện:',
             '• Về quan trắc công trình: Theo hồ sơ thiết kế bản vẽ thi công và các quy chuẩn kỹ thuật hiện hành, công trình thuộc cấp II không nằm trong danh mục bắt buộc phải lập đề cương quan trắc lún dài hạn đặc biệt trong quá trình thi công phần thân.\n'
             '• Về trắc đạc hình học và đo đạc đối chứng: Công tác trắc địa định vị hệ lưới trục tọa độ, độ thẳng đứng của cột vách (kiểm tra bằng máy chiếu đứng Zenit / Laser) và cao độ sàn bê tông từng tầng (đo bằng máy thủy bình kỹ thuật số) được Nhà thầu thực hiện thường xuyên và được TVGS đo đạc đối chứng độc lập. Sai số hình học thực tế nằm trong phạm vi dung sai cho phép theo TCVN 4453:1995 (độ lệch trục cột < 10mm, độ chênh cao độ sàn < 10mm).\n'
             '• Thí nghiệm đối chứng & Kiểm định: Đã thực hiện các đợt thí nghiệm đối chứng súng bật nẩy kết hợp siêu âm bê tông (theo TCVN 9334:2012 và TCVN 9335:2012) tại một số cấu kiện chịu lực chính, kết quả đồng nhất và khẳng định độ tin cậy của kết quả nén mẫu lưu tại phòng LAS-XD.')
        ]),
        ('6. Đánh giá về công tác tổ chức nghiệm thu công việc xây dựng, nghiệm thu giai đoạn:', [
            ('Nội dung thực hiện:',
             '• Trình tự và thủ tục nghiệm thu: Nghiêm túc tuân thủ quy trình nghiệm thu 2 bước: Nhà thầu thi công tự kiểm tra, lập biên bản nghiệm thu nội bộ đạt yêu cầu mới phát hành Phiếu yêu cầu nghiệm thu gửi TVGS kèm đầy đủ hồ sơ thí nghiệm, chứng chỉ vật tư liên quan. TVGS bố trí Kỹ sư giám sát chuyên ngành kiểm tra hiện trường trong thời hạn không quá 24 giờ kể từ khi nhận được yêu cầu nghiệm thu theo đúng quy định tại Điều 22 Khoản 3 Nghị định 207/2026/NĐ-CP.\n'
             '• Nghiệm thu công tác khuất (Hidden Works): Toàn bộ công tác khuất gồm cốt thép móng, thép dầm, sàn, cột, vách, bể ngầm và các chi tiết đặt sẵn (sleeve, bản mã, bu lông neo) đều được kiểm tra kỹ lưỡng về chủng loại, đường kính, vị trí, khoảng cách đai, mối nối, chiều dày lớp bê tông bảo vệ và công tác vệ sinh xịt rửa cốp pha trước khi TVGS ký biên bản nghiệm thu chuyển bước cho phép đổ bê tông.\n'
             '• Hồ sơ biên bản nghiệm thu: Lập đầy đủ theo mẫu chuẩn quy định tại Điều 22 Nghị định 207/2026/NĐ-CP, có đầy đủ chữ ký của Kỹ sư TVGS trực tiếp và Kỹ thuật thi công của Nhà thầu.\n'
             '• Bản vẽ hoàn công giai đoạn phần thô: Nhà thầu đã lập Bản vẽ hoàn công phần kết cấu thô phản ánh đúng kích thước hình học thực tế thi công, có chữ ký của Chỉ huy trưởng nhà thầu và chữ ký xác nhận của Giám sát trưởng TVGS theo quy định tại Phụ lục II Nghị định 207/2026/NĐ-CP.')
        ]),
        ('7. Các thay đổi thiết kế và việc thẩm định, phê duyệt thiết kế điều chỉnh trong quá trình thi công:', [
            ('Nội dung xử lý:',
             'Trong quá trình thi công phần thô, một số điều chỉnh chi tiết cấu tạo cục bộ nhằm xử lý va chạm không gian giữa ống thoát nước ngầm và dầm móng hầm, điều chỉnh vị trí lỗ mở kỹ thuật hộp gen MEP đã được các bên xử lý qua Phiếu yêu cầu thông tin làm rõ (RFI số 01 đến RFI số 08). Các nội dung điều chỉnh này là điều chỉnh cục bộ, không làm thay đổi mục tiêu đầu tư, không làm thay đổi tải trọng thiết kế, giải pháp kết cấu chịu lực chính của công trình và không vượt tổng mức đầu tư. Các thay đổi đã được Nhà thầu Thiết kế (Công ty Tư vấn Thiết kế và ĐTXD - BQP) xác nhận bằng văn bản/bản vẽ sửa đổi, được TVGS thẩm tra chấp thuận và Chủ đầu tư phê duyệt trước khi thi công.')
        ]),
        ('8. Những tồn tại, khiếm khuyết về chất lượng, sự cố công trình và kết quả khắc phục:', [
            ('Nội dung đánh giá:',
             '• Về sự cố công trình: Trong suốt quá trình thi công giai đoạn phần thô, công trình không để xảy ra bất kỳ sự cố công trình xây dựng hay sự cố mất an toàn lao động nào theo quy định tại Điều 45 và Điều 49 Nghị định 207/2026/NĐ-CP.\n'
             '• Về tồn tại, khiếm khuyết chất lượng cục bộ và kết quả xử lý: Trong một số đợt đổ bê tông cột vách tầng hầm và tầng 3, xuất hiện hiện tượng rỗ bề mặt cục bộ tại chân cột do mật độ cốt thép dày và hiện tượng nứt chân chim co ngót nhiệt bề mặt sàn tầng mái khi gặp nắng gắt. TVGS đã kịp thời phát hành các Phiếu yêu cầu xử lý không phù hợp (NCR) yêu cầu Nhà thầu tạm dừng và lập biện pháp khắc phục. Nhà thầu đã đục tẩy phần bê tông rỗ, vệ sinh sạch bằng khí nén và trám vá hoàn thiện bằng vữa không co ngót cường độ cao Sika Grout 214-11, đồng thời tiến hành bơm keo Epoxy xử lý vết nứt bề mặt. TVGS đã kiểm tra nghiệm thu đóng phiếu NCR đạt 100% yêu cầu kỹ thuật và thẩm mỹ.')
        ]),
        ('9. Đánh giá sự phù hợp của hồ sơ quản lý chất lượng theo quy định:', [
            ('Nội dung hồ sơ:',
             'Toàn bộ Hồ sơ quản lý chất lượng giai đoạn phần thô đã được Nhà thầu lập và tập hợp đầy đủ theo đúng danh mục quy định tại Phụ lục VII Nghị định số 207/2026/NĐ-CP và Thông tư số 32/2026/TT-BXD, bao gồm: Hồ sơ pháp lý dự án (GPXD, Quyết định phê duyệt dự án, Hồ sơ thiết kế bản vẽ thi công được duyệt); Sổ Nhật ký thi công công trình của Nhà thầu chính và các nhà thầu phụ; Hệ thống Biên bản nghiệm thu công việc xây dựng, Biên bản nghiệm thu nội bộ; Toàn bộ Chứng chỉ xuất xưởng (CO/CQ), Chứng nhận chất lượng vật tư, vật liệu đầu vào; Các Phiếu kết quả thí nghiệm nén bê tông, kéo thép, thử mối nối của phòng LAS-XD; Bộ Bản vẽ hoàn công phần kết cấu thô (A3/A1) có dấu hoàn công và chữ ký của các bên; Hồ sơ xử lý kỹ thuật hiện trường (RFI), Biên bản xử lý khiếm khuyết (NCR). Hồ sơ được lập bằng tiếng Việt, lưu trữ khoa học, số liệu trung thực, rõ ràng và đủ điều kiện phục vụ công tác nghiệm thu giai đoạn cũng như bàn giao lưu trữ hoàn công sau này.')
        ]),
        ('10. Đánh giá công tác thi công xây dựng công trình theo thiết kế PCCC đã thẩm duyệt:', [
            ('Nội dung tuân thủ:',
             '• Bậc chịu lửa và bảo vệ kết cấu chịu lực: Công trình được thiết kế với Bậc chịu lửa Bậc I theo QCVN 06:2022/BXD. Trong giai đoạn phần thô, TVGS đã kiểm soát nghiêm ngặt chiều dày lớp bê tông bảo vệ cốt thép (cột >= 25mm, dầm >= 25mm, sàn >= 15mm, vách >= 20mm) và cấp độ bền bê tông để đảm bảo giới hạn chịu lửa của các cấu kiện chịu lực chính (Cột R120, Vách chịu lực REI120, Dầm sàn R60/REI60).\n'
             '• Buồng thang bộ thoát nạn & Ngăn cháy lan: Hệ thống vách bê tông cốt thép của các buồng thang bộ thoát nạn (thang N1/N2/N3) và giếng thang máy được thi công đặc chắc, bề mặt phẳng, kích thước hình học thông thủy của vế thang, chiếu nghỉ đúng thiết kế, đảm bảo khả năng ngăn cháy lan và khói khi vận hành.\n'
             '• Định vị các lỗ mở kỹ thuật hệ thống PCCC: Đã phối hợp chặt chẽ với Nhà thầu PCCC (Công ty Cổ phần ZME - Gói XL-02) để chừa sẵn các lỗ mở kỹ thuật xuyên sàn, xuyên vách hầm cho đường ống cấp nước chữa cháy D100/D150, hệ thống ống hút khói hành lang và tạo áp buồng thang, tuyệt đối không đục phá cắt phạm cốt thép chịu lực sau khi đổ bê tông.')
        ]),
        ('11. Đánh giá về sự tuân thủ các quy định của pháp luật về bảo vệ môi trường:', [
            ('Nội dung tuân thủ:',
             'Nhà thầu đã thực hiện nghiêm túc Kế hoạch quản lý môi trường trên công trường: Nước thải rửa xe bồn bê tông và nước thi công được dẫn qua hố lắng 3 ngăn trước khi xả vào hệ thống thoát nước đô thị; Chất thải rắn xây dựng (đầu mẩu thép vụn, cốp pha hỏng, bao bì xi măng, gạch vỡ) được thu gom phân loại tại bãi tập kết tạm và ký hợp đồng với đơn vị có chức năng vận chuyển xử lý định kỳ; Bụi và tiếng ồn được kiểm soát bằng việc tưới nước dập bụi đường nội bộ, bạt che phủ vật liệu và kiểm soát giờ đổ bê tông ban đêm không gây ảnh hưởng đến khu dân cư lân cận. Trong suốt quá trình thi công không để xảy ra ô nhiễm môi trường hay bị cơ quan quản lý môi trường địa phương xử phạt.')
        ]),
        ('12. Đánh giá về sự phù hợp của quy trình vận hành, bảo trì công trình:', [
            ('Nội dung thực hiện:',
             'Nhà thầu thiết kế đã lập Quy trình bảo trì công trình xây dựng (phần kết cấu và kiến trúc) trong tập hồ sơ thiết kế bản vẽ thi công. TVGS đã rà soát nội dung quy trình, nhận thấy các chỉ dẫn về chu kỳ kiểm tra kết cấu, quan trắc biến dạng, bảo dưỡng lớp phủ bề mặt bê tông và sửa chữa tường xây đáp ứng đúng quy định tại Điều 34 Nghị định số 207/2026/NĐ-CP và Thông tư số 32/2026/TT-BXD, bảo đảm tính khả thi cho công tác khai thác sử dụng lâu dài.')
        ]),
        ('13. Đánh giá về các điều kiện nghiệm thu hoàn thành giai đoạn phần thô:', [
            ('Đánh giá tổng hợp và kết luận:',
             'TVGS đã tiến hành rà soát, đối chiếu toàn bộ các điều kiện nghiệm thu theo quy định tại Điều 23 Nghị định số 207/2026/NĐ-CP và Hợp đồng kinh tế:\n'
             '1. Khối lượng thi công: Đã hoàn thành 100% khối lượng kết cấu khung bê tông cốt thép và tường xây bao che của tất cả các khối công trình theo đúng hồ sơ thiết kế được duyệt;\n'
             '2. Chất lượng công trình: Đảm bảo an toàn chịu lực, độ bền vững, mỹ quan kỹ thuật, phù hợp với các quy chuẩn kỹ thuật quốc gia (QCVN 06:2022/BXD, QCVN 02:2022/BXD) và tiêu chuẩn thi công nghiệm thu hiện hành (TCVN 4453:1995, TCVN 5574:2018);\n'
             '3. Kết quả thí nghiệm & Kiểm định: 100% phiếu thí nghiệm mẫu nén bê tông R28, kéo thép, mối nối cơ khí và kiểm tra kích thước hình học đều đạt yêu cầu thiết kế;\n'
             '4. Hồ sơ hoàn thành giai đoạn: Hồ sơ quản lý chất lượng, Nhật ký thi công, Bản vẽ hoàn công phần thô đã được hoàn thiện đầy đủ, hợp lệ;\n'
             '5. An toàn & Môi trường: Công trường đảm bảo an toàn tuyệt đối, không có sự cố, không tranh chấp kỹ thuật.\n'
             '--> KẾT LUẬN TỔNG THỂ: GIAI ĐOẠN PHẦN THÔ CÔNG TRÌNH “NHÀ ĐIỀU HÀNH, TÁC NGHIỆP CỦA BAN CƠ YẾU CHÍNH PHỦ” ĐỦ ĐIỀU KIỆN ĐỂ TỔ CHỨC NGHIỆM THU HOÀN THÀNH VÀ BÀN GIAO MẶT BẰNG CHUYỂN SANG GIAI ĐOẠN THI CÔNG HOÀN THIỆN VÀ LẮP ĐẶT HỆ THỐNG CƠ ĐIỆN (MEP).')
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
