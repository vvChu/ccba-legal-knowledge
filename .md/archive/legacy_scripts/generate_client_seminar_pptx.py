"""Generate a client-focused 15-slide PowerPoint presentation (.pptx) for Project Owners/Investors."""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_client_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5) # 16:9 Widescreen

    # Client Theme Color Palette
    DARK_BG = RGBColor(15, 23, 42)        # Slate 900
    NAVY_PRIMARY = RGBColor(30, 58, 138)   # Blue 900
    CARD_BG = RGBColor(30, 41, 59)        # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)    # Slate 700
    TEXT_WHITE = RGBColor(248, 250, 252)
    TEXT_MUTED = RGBColor(148, 163, 184)
    ACCENT_GOLD = RGBColor(245, 158, 11)   # Amber 500
    ACCENT_BLUE = RGBColor(56, 189, 248)   # Sky 400
    ACCENT_GREEN = RGBColor(52, 211, 153)  # Emerald 400

    def add_blank_slide():
        blank_layout = prs.slide_layouts[6]
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()
        return slide

    def add_header(slide, title_text, subtitle_text=""):
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.0))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = 'Segoe UI'
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GOLD

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.name = 'Segoe UI'
            p2.font.size = Pt(13)
            p2.font.color.rgb = TEXT_MUTED
            p2.space_before = Pt(4)

    def add_card(slide, left, top, width, height, title, items, accent_color=ACCENT_BLUE):
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
    # SLIDE 1: Title Slide (Client Focus)
    # -------------------------------------------------------------------------
    s1 = add_blank_slide()
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1))
    hero.fill.solid()
    hero.fill.fore_color.rgb = NAVY_PRIMARY
    hero.line.color.rgb = ACCENT_GOLD
    hero.line.width = Pt(2)

    txBox = s1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.333), Inches(4.0))
    tf = txBox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "BÁO CÁO TƯ VẤN CHUYÊN ĐỀ DÀNH CHO CHỦ ĐẦU TƯ & KHÁCH HÀNG"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD

    p2 = tf.add_paragraph()
    p2.text = "TỐI ƯU HÓA DỰ ÁN DƯỚI GÓC NHÌN LUẬT XÂY DỰNG 135/2025/QH15\n& 19 VĂN BẢN HƯỚNG DẪN THI HÀNH 2026"
    p2.font.name = 'Segoe UI'
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(12)

    p3 = tf.add_paragraph()
    p3.text = "Cơ hội Cắt giảm Thủ tục • Tích hợp PCCC 1 cửa • Lộ trình Số hóa BIM & Giải pháp Đồng hành từ CCBA"
    p3.font.name = 'Segoe UI'
    p3.font.size = Pt(14)
    p3.font.color.rgb = ACCENT_BLUE
    p3.space_before = Pt(16)

    p4 = tf.add_paragraph()
    p4.text = "Đơn vị tư vấn: Trung tâm Tư vấn và Ứng dụng BIM trong Xây dựng (CCBA) | Hiệu lực thi hành: 01/07/2026"
    p4.font.name = 'Segoe UI'
    p4.font.size = Pt(13)
    p4.font.color.rgb = TEXT_MUTED
    p4.space_before = Pt(24)

    # -------------------------------------------------------------------------
    # SLIDE 2: Bối cảnh 2026 & Thông điệp cho Chủ Đầu tư
    # -------------------------------------------------------------------------
    s2 = add_blank_slide()
    add_header(s2, "1. Bối cảnh Khung Pháp lý 2026 — Bước ngoặt Cắt giảm Thủ tục", "Luật Xây dựng số 135/2025/QH15 và hệ thống 19 văn bản hướng dẫn có hiệu lực từ 01/07/2026")
    add_card(s2, 0.8, 1.8, 5.6, 5.0, "🎯 Chuyển dịch Cơ chế Quản lý Nhà nước", [
        "Chuyển mạnh từ 'Tiền kiểm' sang 'Hậu kiểm'.",
        "Giảm can thiệp trực tiếp vào thiết kế triển khai sau thiết kế cơ sở.",
        "Trao quyền tự quyết & nâng cao trách nhiệm của Chủ đầu tư.",
        "Phân cấp triệt để cho UBND cấp tỉnh & Sở Xây dựng địa phương."
    ], accent_color=ACCENT_GOLD)
    add_card(s2, 6.9, 1.8, 5.6, 5.0, "📜 Hệ thống Văn bản Đồng bộ 2026", [
        "1 Luật Xây dựng số 135/2025/QH15 (Thay thế Luật 2014).",
        "7 Nghị định Chính phủ (NĐ 217, 207, 212, 206, 210, 209, 193).",
        "12 Thông tư Bộ chuyên ngành (BXD, BTC, BQP).",
        "Bộ dữ liệu pháp lý 100% full-text chính quy (> 3.31 MB)."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 3: 5 Lợi ích Trực tiếp cho Chủ Đầu tư
    # -------------------------------------------------------------------------
    s3 = add_blank_slide()
    add_header(s3, "2. Top 5 Lợi ích Trực tiếp cho Chủ Đầu tư từ Khung Pháp lý Mới", "Tối ưu hóa tiến độ, giảm thiểu rủi ro pháp lý & tiết kiệm chi phí triển khai dự án")
    add_card(s3, 0.8, 1.8, 3.6, 5.0, "⚡ 1. Tiết kiệm Thời gian", [
        "Rút ngắn 3-4 tuần lấy ý kiến PCCC nhờ cơ chế 1 cửa liên thông.",
        "Phân cấp địa phương giúp giải quyết hồ sơ thẩm định nhanh hơn."
    ], accent_color=ACCENT_GREEN)
    add_card(s3, 4.8, 1.8, 3.6, 5.0, "🔓 2. Tối đa Miễn GPXD", [
        "Công trình đã thẩm định thiết kế đủ điều kiện miễn cấp phép.",
        "Nhà ở dưới 5 tầng trong quy hoạch 1/500 chỉ cần Thông báo khởi công."
    ], accent_color=ACCENT_GOLD)
    add_card(s3, 8.8, 1.8, 3.7, 5.0, "💎 3. Minh bạch Chi phí & BIM", [
        "BIM (ISO 19650) giúp kiểm soát bóc tách khối lượng minh bạch.",
        "Giảm thiểu phát sinh vượt Tổng mức đầu tư dự án."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 4: Tích hợp PCCC 1 cửa
    # -------------------------------------------------------------------------
    s4 = add_blank_slide()
    add_header(s4, "3. Tích hợp Thủ tục PCCC 1 Cửa — Tiết kiệm 30-40% Thời gian Hồ sơ", "Giải quyết tình trạng xin ý kiến 2 nơi (Bộ Xây dựng & Công an PCCC)")
    add_card(s4, 0.8, 1.8, 5.6, 5.0, "❌ Khó khăn của Chủ Đầu tư Trước đây", [
        "Nộp hồ sơ 2 lần độc lập tại Sở Xây dựng & Cảnh sát PCCC.",
        "Thời gian kéo dài 45-60 ngày làm chậm tiến độ khởi công.",
        "Nguy cơ xung đột giải pháp giữa bản vẽ Kiến trúc và bản vẽ PCCC."
    ], accent_color=ACCENT_GOLD)
    add_card(s4, 6.9, 1.8, 5.6, 5.0, "✅ Đột phá từ Luật 135 & NĐ 217/2026", [
        "Một đầu mối duy nhất: Cơ quan chuyên môn về xây dựng chủ trì.",
        "Ý kiến PCCC được tích hợp trực tiếp vào Thông báo kết quả thẩm định.",
        "Loại bỏ hồ sơ trùng lặp, đảm bảo tính đồng bộ kỹ thuật 100%.",
        "Tiết kiệm chi phí hành chính và đưa dự án vào vận hành sớm hơn."
    ], accent_color=ACCENT_GREEN)

    # -------------------------------------------------------------------------
    # SLIDE 5: Miễn GPXD
    # -------------------------------------------------------------------------
    s5 = add_blank_slide()
    add_header(s5, "4. Dự án của Bạn có thuộc Diện được MIỄN Giấy phép Xây dựng?", "Nghị định 217/2026/NĐ-CP mở rộng tối đa quyền khởi công cho Chủ đầu tư")
    add_card(s5, 0.8, 1.8, 5.6, 5.0, "📋 Các Trường hợp được Miễn GPXD Mới", [
        "Công trình đã được cơ quan chuyên môn thông báo kết quả thẩm định thiết kế triển khai sau TKCS đủ điều kiện phê duyệt.",
        "Nhà ở riêng lẻ quy mô dưới 5 tầng thuộc dự án đô thị/nông thôn đã có Quy hoạch chi tiết 1/500.",
        "Công trình hạ tầng viễn thông, trạm sạc xe điện, công trình khẩn cấp."
    ], accent_color=ACCENT_BLUE)
    add_card(s5, 6.9, 1.8, 5.6, 5.0, "⚙️ Quy trình Khởi công 2 Bước Đơn giản", [
        "Bước 1: Nộp Thông báo khởi công kèm bản vẽ thiết kế trước 07 ngày.",
        "Bước 2: Công khai thông tin dự án tại công trình và tiến hành thi công.",
        "Chủ đầu tư hoàn toàn chủ động tiến độ không phải chờ cấp phép."
    ], accent_color=ACCENT_GOLD)

    # -------------------------------------------------------------------------
    # SLIDE 6: Phân cấp Thẩm định Thiết kế
    # -------------------------------------------------------------------------
    s6 = add_blank_slide()
    add_header(s6, "5. Phân cấp Thẩm định Thiết kế — Thủ tục Nhanh hơn, Gần hơn", "UBND cấp tỉnh & Sở Xây dựng giải quyết hầu hết các dự án công trình cấp I trên địa bàn")
    add_card(s6, 0.8, 1.8, 5.6, 5.0, "🏛️ Phân định Thẩm quyền Thẩm định Mới", [
        "Bộ Xây dựng/Bộ quản lý chuyên ngành: Chỉ thẩm định công trình cấp đặc biệt, dự án quan trọng quốc gia.",
        "Sở Xây dựng địa phương: Thẩm định toàn bộ công trình cấp I, II, III trên địa bàn tỉnh/thành phố.",
        "Chủ đầu tư tự thẩm định: Đối với công trình cấp III, IV hoặc công trình sử dụng vốn tư nhân."
    ], accent_color=ACCENT_GOLD)
    add_card(s6, 6.9, 1.8, 5.6, 5.0, "💡 Giá trị Mang lại cho Chủ Đầu tư", [
        "Không cần đi lại nộp hồ sơ ra Trung ương/Hà Nội.",
        "Rút ngắn 15-20 ngày thẩm định nhờ cơ chế địa phương linh hoạt.",
        "Dễ dàng trao đổi và xử lý vướng mắc quy hoạch tại địa bàn."
    ], accent_color=ACCENT_GREEN)

    # -------------------------------------------------------------------------
    # SLIDE 7: Cưỡng chế Số hóa BIM (ISO 19650)
    # -------------------------------------------------------------------------
    s7 = add_blank_slide()
    add_header(s7, "6. Lộ trình Áp dụng BIM (TCVN ISO 19650) — Thách thức & Cơ hội", "Nghị định 217/2026/NĐ-CP bắt buộc áp dụng BIM đối với công trình cấp II trở lên từ 01/07/2026")
    add_card(s7, 0.8, 1.8, 5.6, 5.0, "⚠️ Yêu cầu Tuân thủ Bắt buộc", [
        "Công trình cấp II trở lên bắt buộc lập mô hình BIM từ Báo cáo NCKT.",
        "Phải xây dựng Kế hoạch thực hiện BIM (BEP) theo TCVN ISO 19650.",
        "Giao nộp dữ liệu mô hình định dạng mở (IFC) lên hệ thống thẩm định."
    ], accent_color=ACCENT_GOLD)
    add_card(s7, 6.9, 1.8, 5.6, 5.0, "💎 Lợi ích Kinh tế cho Chủ Đầu tư", [
        "Phát hiện & xử lý 100% mâu thuẫn va chạm (Clash Detection) trước khi thi công.",
        "Bóc tách khối lượng & dự toán chính xác, giảm 5-10% chi phí lãng phí.",
        "Tạo dựng tài sản dữ liệu số phục vụ vận hành & bảo trì (FM) dài hạn."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 8: Quản lý Chi phí & Dự toán (NĐ 206)
    # -------------------------------------------------------------------------
    s8 = add_blank_slide()
    add_header(s8, "7. Quản lý Chi phí & Dự toán Dự án theo Nghị định 206/2026/NĐ-CP", "Tích hợp chỉ tiêu kinh tế kỹ thuật & định mức xây dựng quốc gia vào mô hình BIM")
    add_card(s8, 0.8, 1.8, 5.6, 5.0, "📊 Chuẩn hóa Phương pháp Tính TMĐTV & Dự toán", [
        "Áp dụng hệ thống Định mức xây dựng mới (Thông tư 38/2026/TT-BXD).",
        "Phương pháp xác định chi phí dự phòng & chỉ số giá xây dựng chính xác hơn.",
        "Tích hợp tự động dữ liệu giá từ CSDL Quốc gia về hoạt động xây dựng."
    ], accent_color=ACCENT_BLUE)
    add_card(s8, 6.9, 1.8, 5.6, 5.0, "🛡️ Rào chắn Tránh Vượt Tổng mức Đầu tư", [
        "Kiểm soát chi phí theo từng giai đoạn thiết kế (TKCS -> TK Triển khai).",
        "Tránh nguy cơ điều chỉnh dự án do trượt giá hoặc bóc tách thiếu khối lượng.",
        "Minh bạch chi phí bảo trì công trình theo Thông tư 40/2026/TT-BXD."
    ], accent_color=ACCENT_GREEN)

    # -------------------------------------------------------------------------
    # SLIDE 9: Quản lý Hợp đồng Thi công (NĐ 210)
    # -------------------------------------------------------------------------
    s9 = add_blank_slide()
    add_header(s9, "8. Bảo vệ Quyền lợi Chủ Đầu tư trong Hợp đồng Xây dựng (NĐ 210/2026)", "Quy định chi tiết mẫu hợp đồng EPC, Turnkey, Đơn giá cố định & Điều chỉnh giá")
    add_card(s9, 0.8, 1.8, 5.6, 5.0, "📝 Chuẩn hóa Các Dạng Hợp đồng Cốt lõi", [
        "Hợp đồng Trọn gói & Đơn giá cố định: Hạn chế tối đa nguy cơ phát sinh.",
        "Hợp đồng EPC / Thiết kế - Thi công: Phân định rõ trách nhiệm của Tổng thầu.",
        "Quy định công bằng về tạm ứng, thanh toán và giữ tiền bảo hành."
    ], accent_color=ACCENT_GOLD)
    add_card(s9, 6.9, 1.8, 5.6, 5.0, "⚖️ Cơ chế Giải quyết Tranh chấp & Biến động Giá", [
        "Quy trình điều chỉnh hợp đồng minh bạch khi giá vật liệu xây dựng biến động.",
        "Cơ chế xử lý thưởng/phạt tiến độ thi công rõ ràng.",
        "Bảo vệ Chủ đầu tư trước các khiếu nại không hợp lý từ nhà thầu."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 10: Nghiệm thu & Nhật ký Số (NĐ 207)
    # -------------------------------------------------------------------------
    s10 = add_blank_slide()
    add_header(s10, "9. Quản lý Chất lượng & Nghiệm thu Công trình (NĐ 207/2026/NĐ-CP)", "Áp dụng kiểm tra theo đánh giá rủi ro, Nhật ký thi công điện tử & Hoàn công số")
    add_card(s10, 0.8, 1.8, 5.6, 5.0, "📲 Chuyển đổi Số trong Quản lý Thi công", [
        "Bắt buộc áp dụng Nhật ký thi công điện tử (truy xuất nguồn gốc thời gian thực).",
        "Hồ sơ hoàn công số hóa gắn liền với Mã định danh duy nhất của công trình.",
        "Giảm 70% khối lượng giấy tờ nghiệm thu tại công trường."
    ], accent_color=ACCENT_GREEN)
    add_card(s10, 6.9, 1.8, 5.6, 5.0, "🔍 Kiểm tra Nghiệm thu Dựa trên Rủi ro", [
        "Cơ quan chuyên môn kiểm tra công tác nghiệm thu theo tiêu chí đánh giá rủi ro.",
        "Tập trung kiểm tra các công trình có quy mô lớn, ảnh hưởng an toàn cộng đồng.",
        "Đánh giá an toàn định kỳ trong suốt quá trình khai thác vận hành."
    ], accent_color=ACCENT_GOLD)

    # -------------------------------------------------------------------------
    # SLIDE 11: CSDL Quốc gia & Mã Định danh Duy nhất
    # -------------------------------------------------------------------------
    s11 = add_blank_slide()
    add_header(s11, "10. Mã Định danh Duy nhất & CSDL Quốc gia Xây dựng (NĐ 212 & TT 39)", "Gia tăng tính minh bạch pháp lý & giá trị thương mại cho Bất động sản")
    add_card(s11, 0.8, 1.8, 5.6, 5.0, "🆔 Mã Định danh Duy nhất (Unique Construction ID)", [
        "Mỗi dự án/công trình được cấp 1 Mã số công trình duy nhất khi thẩm định.",
        "Tích hợp toàn bộ lịch sử pháp lý: Quy hoạch -> Thẩm định -> Cấp phép -> Bảo trì.",
        "Dễ dàng xác thực tính pháp lý chính danh của dự án đối với ngân hàng & khách hàng."
    ], accent_color=ACCENT_BLUE)
    add_card(s11, 6.9, 1.8, 5.6, 5.0, "🌐 Kết nối CSDL Quốc gia Tập trung", [
        "Công khai thông tin năng lực nhà thầu & kết quả thẩm định.",
        "Tăng tính thanh khoản & niềm tin thương hiệu dự án trên thị trường.",
        "Rút ngắn thời gian thẩm định điều chỉnh dự án về sau."
    ], accent_color=ACCENT_GREEN)

    # -------------------------------------------------------------------------
    # SLIDE 12: Xử lý Chuyển tiếp Dự án Dở dang
    # -------------------------------------------------------------------------
    s12 = add_blank_slide()
    add_header(s12, "11. Xử lý Chuyển tiếp cho các Dự án Dở dang (NĐ 217 - Điều 73, 74)", "Giải pháp tránh ách tắc pháp lý cho các dự án chuẩn bị nộp hoặc đang triển khai")
    add_card(s12, 0.8, 1.8, 5.6, 5.0, "📁 Dự án Nộp Thẩm định Trước 01/07/2026", [
        "Tiếp tục thực hiện thẩm định & cấp phép theo quy định cũ của Luật 2014.",
        "Không bắt buộc phải lập lại hồ sơ theo quy định mới của Luật 135/2025.",
        "Bảo đảm quyền lợi đã hình thành hợp pháp của Chủ đầu tư."
    ], accent_color=ACCENT_GOLD)
    add_card(s12, 6.9, 1.8, 5.6, 5.0, "🔄 Đăng ký Chuyển đổi Cơ chế Mới", [
        "Chủ đầu tư có quyền đăng ký chuyển sang áp dụng quy trình Hậu kiểm của Luật 2025.",
        "Tận dụng cơ chế Miễn GPXD & Tích hợp PCCC 1 cửa để tăng tốc tiến độ.",
        "CCBA tư vấn kịch bản chuyển đổi tối ưu nhất cho từng dự án."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 13: Dịch vụ Đồng hành của CCBA cho Chủ Đầu tư
    # -------------------------------------------------------------------------
    s13 = add_blank_slide()
    add_header(s13, "12. Giải pháp Đồng hành Toàn diện từ CCBA cho Chủ Đầu tư", "Trung tâm Tư vấn & Ứng dụng BIM trong Xây dựng (CCBA) — Đối tác Kỹ thuật Pháp lý Tin cậy")
    add_card(s13, 0.8, 1.8, 3.6, 5.0, "⚖️ Tư vấn Pháp lý Dự án", [
        "Rà soát quy hoạch & điều kiện pháp lý.",
        "Lập kịch bản xin phép/thẩm định 1 cửa.",
        "Tư vấn thủ tục miễn GPXD."
    ], accent_color=ACCENT_GOLD)
    add_card(s13, 4.8, 1.8, 3.6, 5.0, "🔍 Thẩm tra Thiết kế QC", [
        "Thẩm tra 4 bộ môn Arch-KC-MEP-PCCC.",
        "Tích hợp chuẩn PCCC QCVN 06:2022.",
        "Cam kết chất lượng hồ sơ thẩm định."
    ], accent_color=ACCENT_BLUE)
    add_card(s13, 8.8, 1.8, 3.7, 5.0, "💻 Tư vấn & Quản lý BIM", [
        "Xây dựng Kế hoạch BEP chuẩn ISO 19650.",
        "Kiểm soát va chạm & bóc tách khối lượng.",
        "Bàn giao mô hình IFC & CSDL hoàn công."
    ], accent_color=ACCENT_GREEN)

    # -------------------------------------------------------------------------
    # SLIDE 14: Quy trình 4 Bước CCBA Hỗ trợ Dự án
    # -------------------------------------------------------------------------
    s14 = add_blank_slide()
    add_header(s14, "13. Quy trình 4 Bước CCBA Đồng hành Cùng Dự án của Bạn", "Đảm bảo tiến độ nhanh nhất, 100% tuân thủ quy chuẩn & tối ưu chi phí đầu tư")
    add_card(s14, 0.8, 1.8, 2.7, 5.0, "Bước 1: Rà soát", [
        "Đánh giá phân cấp công trình.",
        "Xác định diện miễn GPXD.",
        "Lập lộ trình thủ tục."
    ], accent_color=ACCENT_BLUE)
    add_card(s14, 3.8, 1.8, 2.7, 5.0, "Bước 2: Tối ưu", [
        "Thẩm tra QC 4 bộ môn.",
        "Xử lý mâu thuẫn PCCC & BIM.",
        "Hoàn thiện hồ sơ 1 cửa."
    ], accent_color=ACCENT_GOLD)
    add_card(s14, 6.8, 1.8, 2.7, 5.0, "Bước 3: Thẩm định", [
        "Hỗ trợ nộp hồ sơ 1 cửa.",
        "Giải trình cơ quan chuyên môn.",
        "Lấy Thông báo kết quả."
    ], accent_color=ACCENT_GREEN)
    add_card(s14, 9.8, 1.8, 2.7, 5.0, "Bước 4: Nghiệm thu", [
        "Giám sát thi công số.",
        "Hồ sơ hoàn công BIM.",
        "Quyết toán vốn đầu tư."
    ], accent_color=ACCENT_GOLD)

    # -------------------------------------------------------------------------
    # SLIDE 15: Conclusion & Contact Slide
    # -------------------------------------------------------------------------
    s15 = add_blank_slide()
    hero15 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1))
    hero15.fill.solid()
    hero15.fill.fore_color.rgb = NAVY_PRIMARY
    hero15.line.color.rgb = ACCENT_GOLD
    hero15.line.width = Pt(2)

    txBox = s15.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.333), Inches(4.0))
    tf = txBox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "CCBA — CAM KẾT ĐỒNG HÀNH CÙNG CHỦ ĐẦU TƯ"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD

    p2 = tf.add_paragraph()
    p2.text = "Rút ngắn 20-30% Thời gian Thủ tục • Đảm bảo 100% Tuân thủ Quy chuẩn • Tối ưu Chi phí Đầu tư"
    p2.font.name = 'Segoe UI'
    p2.font.size = Pt(17)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(16)

    p3 = tf.add_paragraph()
    p3.text = "Liên hệ Tư vấn & Đánh giá Hồ sơ Dự án Miễn phí:\n• Trung tâm Tư vấn và Ứng dụng BIM trong Xây dựng (CCBA)\n• Email: contact@ccba.vn | Hotline: 0988.xxx.xxx\n• Địa chỉ: Tháp CCBA, TP. Hà Nội"
    p3.font.name = 'Segoe UI'
    p3.font.size = Pt(14)
    p3.font.color.rgb = ACCENT_BLUE
    p3.space_before = Pt(20)

    output_dir = Path(__file__).resolve().parent.parent / ".md" / "seminars" / "2026"
    output_dir.mkdir(parents=True, exist_ok=True)
    pptx_path = output_dir / "CCBA_CLIENT_PRESENTATION_Luat_Xay_Dung_135_Va_Van_Ban_Huong_Dan.pptx"
    prs.save(str(pptx_path))
    print(f"✅ SUCCESSFULLY GENERATED CLIENT PRESENTATION PPTX AT: {pptx_path}")

if __name__ == "__main__":
    create_client_presentation()
