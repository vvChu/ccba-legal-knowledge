"""Generate a professional 15-slide PowerPoint presentation (.pptx) for CCBA Seminar."""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5) # 16:9 Widescreen

    # Color Palette
    DARK_BG = RGBColor(15, 23, 42)      # Slate 900
    NAVY_PRIMARY = RGBColor(30, 58, 138) # Blue 900
    CARD_BG = RGBColor(30, 41, 59)      # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)  # Slate 700
    TEXT_WHITE = RGBColor(248, 250, 252)
    TEXT_MUTED = RGBColor(148, 163, 184)
    ACCENT_BLUE = RGBColor(56, 189, 248) # Sky 400
    ACCENT_GOLD = RGBColor(250, 204, 21) # Amber 400
    ACCENT_GREEN = RGBColor(74, 222, 128)# Emerald 400

    def add_blank_slide():
        blank_layout = prs.slide_layouts[6]
        slide = prs.slides.add_slide(blank_layout)
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()
        return slide

    def add_header(slide, title_text, subtitle_text=""):
        # Header banner
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.0))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = 'Segoe UI'
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.name = 'Segoe UI'
            p2.font.size = Pt(13)
            p2.font.color.rgb = TEXT_MUTED
            p2.space_before = Pt(4)

    def add_card(slide, left, top, width, height, title, items, badge="", accent_color=ACCENT_BLUE):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = CARD_BORDER
        shape.line.width = Pt(1)

        txBox = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.4))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = 'Segoe UI'
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = accent_color

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.name = 'Segoe UI'
            p.font.size = Pt(13)
            p.font.color.rgb = TEXT_WHITE
            p.space_before = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------------------
    s1 = add_blank_slide()
    # Hero container
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1))
    hero.fill.solid()
    hero.fill.fore_color.rgb = NAVY_PRIMARY
    hero.line.color.rgb = ACCENT_BLUE
    hero.line.width = Pt(2)

    txBox = s1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.333), Inches(4.0))
    tf = txBox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "BÁO CÁO CHUYÊN ĐỀ SEMINAR CCBA"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD

    p2 = tf.add_paragraph()
    p2.text = "LUẬT XÂY DỰNG SỐ 135/2025/QH15 &\nHỆ THỐNG VĂN BẢN HƯỚNG DẪN THI HÀNH"
    p2.font.name = 'Segoe UI'
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(12)

    p3 = tf.add_paragraph()
    p3.text = "Phân tích Tác động Kỹ thuật từ Bộ 7 Nghị định & 12 Thông tư Cốt lõi (Hiệu lực 01/07/2026)"
    p3.font.name = 'Segoe UI'
    p3.font.size = Pt(15)
    p3.font.color.rgb = ACCENT_BLUE
    p3.space_before = Pt(16)

    p4 = tf.add_paragraph()
    p4.text = "Đơn vị thực hiện: Trung tâm Tư vấn và Ứng dụng BIM trong Xây dựng (CCBA) | Tháng 08/2026"
    p4.font.name = 'Segoe UI'
    p4.font.size = Pt(13)
    p4.font.color.rgb = TEXT_MUTED
    p4.space_before = Pt(24)

    # -------------------------------------------------------------------------
    # SLIDE 2: Bối cảnh & Cấu trúc Văn bản
    # -------------------------------------------------------------------------
    s2 = add_blank_slide()
    add_header(s2, "1. Bối cảnh Ban hành & Khung Pháp lý Xây dựng 2026", "Hệ thống văn bản pháp luật mới có hiệu lực thi hành từ ngày 01/07/2026")
    add_card(s2, 0.8, 1.8, 5.6, 5.0, "🏛️ Luật Xây dựng số 135/2025/QH15", [
        "Được Quốc hội khóa XV thông qua ngày 10/12/2025.",
        "Thay thế Luật Xây dựng 2014 & Luật sửa đổi 2020.",
        "Mục tiêu: Chuyển đổi mô hình quản lý từ Tiền kiểm sang Hậu kiểm, phân cấp triệt để.",
        "Hiệu lực thi hành: Từ ngày 01/07/2026 (Một số điều khoản miễn GPXD hiệu lực từ 01/01/2026)."
    ], accent_color=ACCENT_GOLD)

    add_card(s2, 6.9, 1.8, 5.6, 5.0, "📜 Hệ thống Văn bản Hướng dẫn Đồng bộ", [
        "Bộ 7 Nghị định Chính phủ (NĐ 217, 207, 212, 206, 210, 209, 193/2026/NĐ-CP).",
        "Bộ 12 Thông tư Chuyên ngành (Bộ Xây dựng, Bộ Tài chính, Bộ Quốc phòng).",
        "Dung lượng kho tri thức: > 3.31 MB Markdown với 3,198 AST Clauses.",
        "Thiết lập đồ thị liên kết 2 chiều (guided_by) trong legal_registry.yaml."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 3: Ma trận 9 Điểm mới Đột phá
    # -------------------------------------------------------------------------
    s3 = add_blank_slide()
    add_header(s3, "2. Ma trận 9 Điểm mới Đột phá (Luật 2025 vs Luật 2014)", "Những thay đổi căn bản tác động trực tiếp lên quy trình thẩm định & thi công")
    add_card(s3, 0.8, 1.8, 3.6, 5.0, "🔄 Mô hình Quản lý", [
        "Tiền kiểm -> Hậu kiểm mạnh mẽ.",
        "Giảm can thiệp trực tiếp của cơ quan nhà nước vào thiết kế sau TKCS.",
        "Tăng trách nhiệm tự thẩm tra của Chủ đầu tư."
    ], accent_color=ACCENT_GOLD)
    add_card(s3, 4.8, 1.8, 3.6, 5.0, "🚒 Tích hợp PCCC & GPXD", [
        "Liên thông 1 cửa: Tích hợp ý kiến PCCC vào thẩm định thiết kế.",
        "Mở rộng tối đa các trường hợp miễn Giấy phép xây dựng.",
        "Chỉ cần nộp Thông báo khởi công."
    ], accent_color=ACCENT_BLUE)
    add_card(s3, 8.8, 1.8, 3.7, 5.0, "💻 Số hóa BIM & CSDL", [
        "Bắt buộc BIM cho công trình cấp II trở lên (TCVN ISO 19650).",
        "Mã định danh duy nhất (Unique Construction ID) quản lý công trình.",
        "Nhật ký thi công điện tử & Hồ sơ hoàn công số."
    ], accent_color=ACCENT_GREEN)

    # -------------------------------------------------------------------------
    # SLIDE 4: Điểm mới 1 - Tích hợp Thẩm duyệt PCCC
    # -------------------------------------------------------------------------
    s4 = add_blank_slide()
    add_header(s4, "3. Điểm mới 1 — Tích hợp Thủ tục PCCC Liên thông 1 Cửa", "Giải quyết triệt để tình trạng chồng chéo hồ sơ giữa Bộ Xây dựng & Bộ Công an")
    add_card(s4, 0.8, 1.8, 5.6, 5.0, "❌ Quy trình Cũ (Luật 2014 & Luật PCCC 2001)", [
        "Thực hiện 2 thủ tục độc lập, song song tại 2 cơ quan.",
        "Chủ đầu tư phải nộp hồ sơ thẩm duyệt PCCC riêng tại Công an PCCC.",
        "Gây kéo dài thời gian từ 45-60 ngày và nguy cơ mâu thuẫn bản vẽ."
    ], accent_color=ACCENT_GOLD)
    add_card(s4, 6.9, 1.8, 5.6, 5.0, "✅ Quy trình Mới (Luật 135/2025 & NĐ 217/2026)", [
        "Cơ chế 1 cửa liên thông: Cơ quan chuyên môn về xây dựng làm đầu mối.",
        "Ý kiến PCCC được tích hợp trực tiếp vào Thông báo kết quả thẩm định.",
        "Cắt giảm 30-40% thời gian lấy ý kiến chuyên ngành.",
        "Đồng bộ chuẩn quy chuẩn QCVN 06:2022 & QCVN 10:2025/BCA."
    ], accent_color=ACCENT_GREEN)

    # -------------------------------------------------------------------------
    # SLIDE 5: Điểm mới 2 - Mở rộng Miễn Giấy phép Xây dựng
    # -------------------------------------------------------------------------
    s5 = add_blank_slide()
    add_header(s5, "4. Điểm mới 2 — Mở rộng Diện Miễn Giấy phép Xây dựng (GPXD)", "Chuyển từ quản lý bằng Giấy phép sang quản lý bằng Quy hoạch & Thiết kế")
    add_card(s5, 0.8, 1.8, 5.6, 5.0, "📋 Các Đối tượng được Miễn GPXD Mới", [
        "Dự án đã được cơ quan chuyên môn thông báo kết quả thẩm định thiết kế đủ điều kiện phê duyệt.",
        "Nhà ở riêng lẻ quy mô dưới 5 tầng thuộc dự án đô thị/nông thôn đã có Quy hoạch chi tiết 1/500.",
        "Công trình hạ tầng viễn thông, trạm sạc xe điện, công trình khẩn cấp."
    ], accent_color=ACCENT_BLUE)
    add_card(s5, 6.9, 1.8, 5.6, 5.0, "⚙️ Nghĩa vụ Quản lý của Chủ đầu tư", [
        "Nộp Thông báo khởi công kèm hồ sơ thiết kế đã thẩm định trước 07 ngày.",
        "Công khai nội dung thiết kế/Giấy phép tại địa điểm thi công.",
        "Chịu trách nhiệm toàn diện trước pháp luật nếu thi công sai quy hoạch."
    ], accent_color=ACCENT_GOLD)

    # -------------------------------------------------------------------------
    # SLIDE 6: Điểm mới 3 - Cưỡng chế Số hóa BIM & Unique ID
    # -------------------------------------------------------------------------
    s6 = add_blank_slide()
    add_header(s6, "5. Điểm mới 3 — Bắt buộc Số hóa BIM & Mã Định danh Duy nhất", "Chuẩn hóa dữ liệu mô hình IFC/BIM theo TCVN ISO 19650 và CSDL Quốc gia")
    add_card(s6, 0.8, 1.8, 5.6, 5.0, "📐 Áp dụng Mô hình Thông tin Công trình (BIM)", [
        "Bắt buộc áp dụng BIM đối với công trình xây dựng cấp II trở lên (NĐ 217).",
        "Áp dụng từ giai đoạn lập Báo cáo NCKT hoặc Báo cáo KT-KT.",
        "Lập Kế hoạch thực hiện BIM (BEP) tuân thủ TCVN ISO 19650-1/2.",
        "Khuyến khích áp dụng cho công trình cấp III, IV và vốn tư nhân."
    ], accent_color=ACCENT_GREEN)
    add_card(s6, 6.9, 1.8, 5.6, 5.0, "🆔 Mã Định danh Duy nhất (Unique Construction ID)", [
        "Mỗi dự án/công trình được cấp 1 Mã định danh duy nhất trên CSDL Quốc gia (NĐ 212).",
        "Quản lý dữ liệu xuyên suốt vòng đời: Thiết kế -> Cấp phép -> Thi công -> Bảo trì.",
        "Kết nối chia sẻ dữ liệu với CSDL Quốc gia về dân cư & đất đai."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 7: Phân tích NĐ 217/2026/NĐ-CP (Quản lý dự án)
    # -------------------------------------------------------------------------
    s7 = add_blank_slide()
    add_header(s7, "6. Nghị định 217/2026/NĐ-CP — Quản lý Dự án & Thẩm định Thiết kế", "Văn bản xương sống điều chỉnh quy trình lập, thẩm định & phê duyệt dự án (422 KB, 907 Clauses)")
    add_card(s7, 0.8, 1.8, 5.6, 5.0, "🔑 Nội dung Cốt lõi", [
        "Quy định chi tiết Báo cáo NCKT, Báo cáo KT-KT (ngưỡng 40 tỷ đồng).",
        "Phân cấp mạnh cho UBND cấp tỉnh/Sở Xây dựng thẩm định công trình cấp I.",
        "Cơ chế tự tổ chức thẩm tra thiết kế của Chủ đầu tư.",
        "Quy định 4 hình thức tổ chức quản lý dự án."
    ], accent_color=ACCENT_GOLD)
    add_card(s7, 6.9, 1.8, 5.6, 5.0, "⚖️ Quy định Chuyển tiếp (Điều 73 & 74)", [
        "Hồ sơ nộp thẩm định trước ngày 01/07/2026 tiếp tục thực hiện theo Luật 2014.",
        "Cho phép Chủ đầu tư đăng ký chuyển sang áp dụng quy trình Hậu kiểm của Luật 2025.",
        "Đảm bảo tính liên tục của dự án, tránh ách tắc pháp lý."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 8: Phân tích NĐ 207/2026/NĐ-CP (Quản lý chất lượng)
    # -------------------------------------------------------------------------
    s8 = add_blank_slide()
    add_header(s8, "7. Nghị định 207/2026/NĐ-CP — Quản lý Chất lượng & Thi công", "Hướng dẫn kiểm tra nghiệm thu theo rủi ro & an toàn công trình hiện hữu (282 KB, 503 Clauses)")
    add_card(s8, 0.8, 1.8, 5.6, 5.0, "🛡️ Kiểm tra Nghiệm thu Dựa trên Rủi ro", [
        "Áp dụng cơ chế đánh giá rủi ro (risk-based inspection) và kiểm tra đột xuất.",
        "Bắt buộc Nhật ký thi công điện tử & Hồ sơ hoàn công số.",
        "Phân định rõ trách nhiệm kiểm tra giữa Chủ đầu tư & Cơ quan chuyên môn."
    ], accent_color=ACCENT_GREEN)
    add_card(s8, 6.9, 1.8, 5.6, 5.0, "🔍 An toàn Công trình Hiện hữu Khai thác", [
        "Bắt buộc đánh giá an toàn chịu lực & an toàn PCCC định kỳ cho công trình cũ.",
        "Đặc biệt áp dụng đối với nhà chung cư cũ, nhà ở kết hợp kinh doanh.",
        "Phát sinh nghĩa vụ bảo trì & nâng cấp giải pháp an toàn."
    ], accent_color=ACCENT_GOLD)

    # -------------------------------------------------------------------------
    # SLIDE 9: Phân tích NĐ 212/2026/NĐ-CP (Năng lực & CSDL)
    # -------------------------------------------------------------------------
    s9 = add_blank_slide()
    add_header(s9, "8. Nghị định 212/2026/NĐ-CP — Năng lực Hoạt động & CSDL Quốc gia", "Chuẩn hóa điều kiện năng lực tổ chức/cá nhân & Hệ thống CSDL (484 KB, 356 Clauses)")
    add_card(s9, 0.8, 1.8, 5.6, 5.0, "🆔 Quản lý CSDL Quốc gia Xây dựng", [
        "Bộ Xây dựng thống nhất quản lý CSDL tập trung toàn quốc.",
        "Cấp Mã định danh duy nhất cho từng dự án & công trình.",
        "Công khai kết quả thẩm định, giấy phép và năng lực tổ chức tư vấn."
    ], accent_color=ACCENT_BLUE)
    add_card(s9, 6.9, 1.8, 5.6, 5.0, "📜 Chứng chỉ Hành nghề & Năng lực", [
        "Phân hạng Chứng chỉ hành nghề cá nhân: Hạng I, Hạng II, Hạng III (hiệu lực 5 năm).",
        "Quy định điều kiện năng lực chặt chẽ đối với tổ chức Thẩm tra thiết kế.",
        "Sát hạch & cấp chứng chỉ qua Cổng dịch vụ công trực tuyến."
    ], accent_color=ACCENT_GOLD)

    # -------------------------------------------------------------------------
    # SLIDE 10: Bộ 4 Nghị định Chi phí, Hợp đồng, VLXD, Quyết toán
    # -------------------------------------------------------------------------
    s10 = add_blank_slide()
    add_header(s10, "9. Bộ 4 Nghị định: Chi phí, Hợp đồng, VLXD & Quyết toán (NĐ 206, 210, 209, 193)", "Hoàn thiện các công cụ kinh tế, tài chính & hợp đồng trong hoạt động xây dựng")
    add_card(s10, 0.8, 1.8, 2.7, 5.0, "💰 NĐ 206/2026\n(Quản lý Chi phí)", [
        "Quản lý TMĐTV & dự toán.",
        "Tích hợp định mức chi phí vào BIM.",
        "Phương pháp chỉ số giá."
    ], accent_color=ACCENT_GOLD)
    add_card(s10, 3.8, 1.8, 2.7, 5.0, "📝 NĐ 210/2026\n(Hợp đồng Xây dựng)", [
        "Hợp đồng EPC, Turnkey.",
        "Đơn giá cố định & điều chỉnh.",
        "Xử lý tranh chấp thi công."
    ], accent_color=ACCENT_BLUE)
    add_card(s10, 6.8, 1.8, 2.7, 5.0, "🧱 NĐ 209/2026\n(Vật liệu Xây dựng)", [
        "Chất lượng VLXD đầu vào.",
        "Vật liệu xanh & tiết kiệm năng lượng.",
        "Hợp chuẩn/hợp quy."
    ], accent_color=ACCENT_GREEN)
    add_card(s10, 9.8, 1.8, 2.7, 5.0, "📊 NĐ 193/2026\n(Quyết toán Vốn)", [
        "Quyết toán dự án hoàn thành.",
        "Kiểm toán độc lập vốn công.",
        "Công khai chi phí đầu tư."
    ], accent_color=ACCENT_GOLD)

    # -------------------------------------------------------------------------
    # SLIDE 11: Bộ 10 Thông tư của Bộ Xây dựng (TT 32 - 41)
    # -------------------------------------------------------------------------
    s11 = add_blank_slide()
    add_header(s11, "10. Bộ 10 Thông tư của Bộ Xây dựng (TT 32/2026 đến TT 41/2026/TT-BXD)", "Quy định kỹ thuật chi tiết, định mức kinh tế kỹ thuật & CSDL quốc gia (> 1.5 MB Markdown)")
    add_card(s11, 0.8, 1.8, 5.6, 5.0, "📐 Phân cấp & Định mức Kinh tế Kỹ thuật", [
        "TT 34/2026/TT-BXD: Phân cấp công trình xây dựng phục vụ quản lý.",
        "TT 36/2026/TT-BXD: Hướng dẫn xác định và quản lý chi phí đầu tư.",
        "TT 37/2026/TT-BXD: Phương pháp xác định định mức dự toán (585 KB).",
        "TT 38/2026/TT-BXD: Ban hành hệ thống Định mức xây dựng quốc gia."
    ], accent_color=ACCENT_BLUE)
    add_card(s11, 6.9, 1.8, 5.6, 5.0, "🏢 Chất lượng, CSDL & Bảo trì Công trình", [
        "TT 32, 33/2026/TT-BXD: Quản lý chất lượng & Đánh giá an toàn công trình.",
        "TT 39/2026/TT-BXD: Chuẩn hóa dữ liệu CSDL Quốc gia Xây dựng.",
        "TT 40/2026/TT-BXD: Phương pháp xác định Chi phí bảo trì công trình.",
        "TT 41/2026/TT-BXD: Quản lý chất lượng sản phẩm, hàng hóa VLXD."
    ], accent_color=ACCENT_GOLD)

    # -------------------------------------------------------------------------
    # SLIDE 12: Thông tư Bộ Tài chính & Bộ Quốc phòng
    # -------------------------------------------------------------------------
    s12 = add_blank_slide()
    add_header(s12, "11. Thông tư Bộ Tài chính (TT 73, 79/2026/TT-BTC) & Bộ Quốc phòng (TT 101)", "Quy định tài chính dự án công & công trình đặc thù an ninh quốc phòng")
    add_card(s12, 0.8, 1.8, 5.6, 5.0, "💵 Thông tư Bộ Tài chính (TT 73 & TT 79)", [
        "TT 73/2026/TT-BTC: Quy định hệ thống Mẫu biểu quyết toán vốn đầu tư dự án.",
        "TT 79/2026/TT-BTC: Quy định thu, chi của Chủ đầu tư & Ban QLDA sử dụng vốn NSNN.",
        "Tối ưu hóa quy trình giải ngân & kiểm soát chi ngân sách."
    ], accent_color=ACCENT_GREEN)
    add_card(s12, 6.9, 1.8, 5.6, 5.0, "🛡️ Thông tư Bộ Quốc phòng (TT 101/2026/TT-BQP)", [
        "Quy định đặc thù quản lý đầu tư xây dựng công trình quốc phòng, an ninh.",
        "Quy trình bảo vệ bí mật nhà nước trong khảo sát, thiết kế & thi công.",
        "Áp dụng trình tự thủ tục rút gọn đối với công trình khẩn cấp."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 13: Tác động Kỹ thuật lên Thẩm tra CCBA
    # -------------------------------------------------------------------------
    s13 = add_blank_slide()
    add_header(s13, "12. Tác động Kỹ thuật lên Quy trình Thẩm tra Thiết kế CCBA", "Chuẩn hóa ma trận kiểm soát chất lượng 4 bộ môn (Arch - KC - MEP - PCCC)")
    add_card(s13, 0.8, 1.8, 5.6, 5.0, "🎯 Nâng cấp Quy trình Thẩm tra 4 Bộ môn", [
        "Tích hợp ma trận đối soát quy chuẩn PCCC (QCVN 06:2022 & QCVN 10:2025/BCA).",
        "Kiểm tra tính an toàn chịu lực & tuân thủ quy chuẩn kỹ thuật theo NĐ 217.",
        "Rà soát tính khả thi thi công & giải pháp an toàn công trình."
    ], accent_color=ACCENT_GOLD)
    add_card(s13, 6.9, 1.8, 5.6, 5.0, "🤖 Ứng dụng AI Agent & OKF v0.2 Graph", [
        "Nạp 21 gói tri thức OKF v0.2 vào Tác nhân AI QC (Discovery, Audit, Reporter).",
        "Kiểm tra đối chiếu 3,198 AST Clauses & 578 Q&A Benchmark tự động.",
        "Đối soát mô hình BIM IFC theo TCVN ISO 19650."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 14: Kế hoạch Hành động CCBA
    # -------------------------------------------------------------------------
    s14 = add_blank_slide()
    add_header(s14, "13. Kế hoạch Hành động (Action Items) cho Đội ngũ Chuyên gia CCBA", "Chuẩn bị nguồn lực & quy trình sẵn sàng cho mốc hiệu lực 01/07/2026")
    add_card(s14, 0.8, 1.8, 5.6, 5.0, "📚 Đào tạo Nội bộ & Chuẩn hóa Mẫu biểu", [
        "Tổ chức các buổi tập huấn chuyên sâu cho Kỹ sư Thẩm tra trưởng.",
        "Cập nhật bộ Mẫu biểu Tờ trình & Thông báo thẩm định theo NĐ 217.",
        "Xây dựng Hướng dẫn thẩm tra mô hình BIM cho công trình cấp II trở lên."
    ], accent_color=ACCENT_GREEN)
    add_card(s14, 6.9, 1.8, 5.6, 5.0, "🔄 Đồng bộ RAG Cloud & Công cụ QC", [
        "Đồng bộ kho tri thức 3.31 MB lên Google NotebookLM Cloud RAG.",
        "Triển khai hệ thống Thẩm tra đa bộ môn Semantic Map-Reduce.",
        "Sẵn sàng tư vấn & hỗ trợ Chủ đầu tư thích ứng Luật mới."
    ], accent_color=ACCENT_GOLD)

    # -------------------------------------------------------------------------
    # SLIDE 15: Conclusion & Q&A
    # -------------------------------------------------------------------------
    s15 = add_blank_slide()
    # Hero container
    hero15 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1))
    hero15.fill.solid()
    hero15.fill.fore_color.rgb = NAVY_PRIMARY
    hero15.line.color.rgb = ACCENT_GOLD
    hero15.line.width = Pt(2)

    txBox = s15.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.333), Inches(4.0))
    tf = txBox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "TỔNG KẾT & PHẦN THẢO LUẬN Q&A"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD

    p2 = tf.add_paragraph()
    p2.text = "3 Thông điệp Cốt lõi: Phân cấp Hậu kiểm • Tích hợp PCCC • Bắt buộc Số hóa BIM"
    p2.font.name = 'Segoe UI'
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(16)

    p3 = tf.add_paragraph()
    p3.text = "Kho tri thức 21 văn bản pháp luật OKF v0.2 đã sẵn sàng tại Spoke ccba-legal-knowledge.\nXin chân thành cảm ơn Quý đồng nghiệp & Chuyên gia đã tham dự!"
    p3.font.name = 'Segoe UI'
    p3.font.size = Pt(14)
    p3.font.color.rgb = ACCENT_BLUE
    p3.space_before = Pt(20)

    # Save presentation
    output_dir = Path(__file__).resolve().parent.parent / ".md" / "seminars" / "2026"
    output_dir.mkdir(parents=True, exist_ok=True)
    pptx_path = output_dir / "CCBA_RD_SEMINAR_001_Rev01-10.08.26-Luat_Xay_Dung_135_Va_Van_Ban_Huong_Dan.pptx"
    prs.save(str(pptx_path))
    print(f"✅ SUCCESSFULLY GENERATED PPTX PRESENTATION AT: {pptx_path}")

if __name__ == "__main__":
    create_presentation()
