"""Generate a customized PowerPoint presentation (.pptx) tailored specifically for FPT HN03 Project Workshop: Part 1 Overview of Construction Law 2025, Part 2 Application to HN03 Project."""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_fpt_hn03_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5) # 16:9 Widescreen

    # Color Palette: FPT Corporate Orange & Navy Theme
    DARK_BG = RGBColor(15, 23, 42)        # Slate 900
    NAVY_PRIMARY = RGBColor(30, 58, 138)   # Blue 900
    CARD_BG = RGBColor(30, 41, 59)        # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)    # Slate 700
    TEXT_WHITE = RGBColor(248, 250, 252)
    TEXT_MUTED = RGBColor(148, 163, 184)
    ACCENT_ORANGE = RGBColor(249, 115, 22) # FPT Orange (Amber/Orange 500)
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
        p.font.size = Pt(23)
        p.font.bold = True
        p.font.color.rgb = ACCENT_ORANGE

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
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = accent_color

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.name = 'Segoe UI'
            p.font.size = Pt(12.5)
            p.font.color.rgb = TEXT_WHITE
            p.space_before = Pt(7)

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide (FPT HN03 Workshop - 2 Parts)
    # -------------------------------------------------------------------------
    s1 = add_blank_slide()
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1))
    hero.fill.solid()
    hero.fill.fore_color.rgb = NAVY_PRIMARY
    hero.line.color.rgb = ACCENT_ORANGE
    hero.line.width = Pt(2)

    txBox = s1.shapes.add_textbox(Inches(1.5), Inches(1.6), Inches(10.333), Inches(4.2))
    tf = txBox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "WORKSHOP CHUYÊN ĐỀ: LUẬT XÂY DỰNG 2025 & TÁC ĐỘNG ĐẾN DỰ ÁN FPT HN03"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE

    p2 = tf.add_paragraph()
    p2.text = "PHẦN 1: TỔNG QUAN LUẬT XÂY DỰNG 2025 & NGHỊ ĐỊNH HƯỚNG DẪN MỚI\nPHẦN 2: ÁP DỤNG THỰC TIỄN CHO DỰ ÁN DCHN03 (KCN TLIP III, PHÚ THỌ)"
    p2.font.name = 'Segoe UI'
    p2.font.size = Pt(21)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "CĐT: FPT Thăng Long BDA — TVTK: Liên danh IBST (Viện KHCN Xây dựng) - First Green (FGE)"
    p3.font.name = 'Segoe UI'
    p3.font.size = Pt(14)
    p3.font.color.rgb = ACCENT_BLUE
    p3.space_before = Pt(14)

    p4 = tf.add_paragraph()
    p4.text = "Địa điểm: Lô E9 (27.206m²), KCN Thăng Long Vĩnh Phúc, Tỉnh Phú Thọ | Đơn vị thẩm định: Sở Xây dựng / BQL KCN Phú Thọ"
    p4.font.name = 'Segoe UI'
    p4.font.size = Pt(12.5)
    p4.font.color.rgb = TEXT_MUTED
    p4.space_before = Pt(20)

    # -------------------------------------------------------------------------
    # SLIDE 2: PHẦN 1 - Tổng quan Những Điểm Mới Cốt lõi của Luật Xây dựng 2025
    # -------------------------------------------------------------------------
    s2 = add_blank_slide()
    add_header(s2, "PHẦN 1: 1. Tổng quan Những Điểm Mới Cốt lõi của Luật Xây dựng 2025 (135/2025/QH15)", "Định hướng đổi mới quản lý đầu tư xây dựng — Có hiệu lực thi hành từ 01/07/2026")
    add_card(s2, 0.8, 1.8, 5.6, 5.0, "🏛️ Định hướng Thay đổi Cốt lõi", [
        "Luật Xây dựng số 135/2025/QH15 (Thay thế Luật 2014 & Luật sửa đổi 2020).",
        "Chuyển dịch mạnh mẽ từ Tiền kiểm sang Hậu kiểm & Phân cấp về địa phương.",
        "Tối giản thủ tục hành chính, giao quyền tự quyết định cho Chủ đầu tư.",
        "Đẩy mạnh Chuyển đổi số & Bắt buộc áp dụng BIM (TCVN ISO 19650)."
    ], accent_color=ACCENT_ORANGE)
    add_card(s2, 6.9, 1.8, 5.6, 5.0, "🎯 Phân định Thẩm quyền Rạch ròi", [
        "Cơ quan Nhà nước: Thẩm định quy hoạch, kết cấu an toàn, an toàn PCCC & QCVN.",
        "Chủ đầu tư: Toàn quyền phê duyệt Thiết kế thi công (TKBVTC) & Chi tiết kỹ thuật.",
        "Tích hợp dữ liệu công khai trên CSDL Quốc gia về Hoạt động Xây dựng.",
        "Xác định rõ danh mục công trình thuộc diện Miễn Giấy phép Xây dựng."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 3: PHẦN 1 - Hệ thống Nghị định & Thông tư Hướng dẫn Thi hành
    # -------------------------------------------------------------------------
    s3 = add_blank_slide()
    add_header(s3, "PHẦN 1: 2. Khung Văn bản Hướng dẫn Thi hành Cốt lõi (Nghị định & Thông tư 2026)", "Hệ thống văn bản đồng bộ ban hành tháng 06/2026, có hiệu lực đồng thời từ 01/07/2026")
    add_card(s3, 0.8, 1.8, 5.6, 5.0, "📋 Các Nghị định Hướng dẫn Chính", [
        "Nghị định 217/2026/NĐ-CP: Quản lý dự án & Thẩm định BCNCKT / TKCS.",
        "Nghị định 207/2026/NĐ-CP: Quản lý chất lượng, thi công & bảo trì công trình.",
        "Nghị định 212/2026/NĐ-CP: Điều kiện năng lực hoạt động xây dựng & CSDL Quốc gia.",
        "Nghị định 206/2026/NĐ-CP & NĐ 210/2026/NĐ-CP: Quản lý chi phí & Hợp đồng."
    ], accent_color=ACCENT_ORANGE)
    add_card(s3, 6.9, 1.8, 5.6, 5.0, "⚖️ Quy định Phân cấp & PCCC Mới", [
        "Thông tư 34/2026/TT-BXD: Quy định chi tiết về Phân cấp công trình xây dựng.",
        "Luật PCCC & CNCH 55/2024 & Nghị định 105/2025/NĐ-CP: Phân định ranh giới PCCC.",
        "Phân công 2 cổng: Cơ quan chuyên môn Xây dựng (QCVN 06) vs PC07 (PCCC chuyên ngành).",
        "Đơn giản hóa quy trình thẩm duyệt và liên thông 1 cửa."
    ], accent_color=ACCENT_GREEN)

    # -------------------------------------------------------------------------
    # SLIDE 4: PHẦN 1 - Phân định Phạm vi TKCS & Ranh giới PCCC 2 Cổng
    # -------------------------------------------------------------------------
    s4 = add_blank_slide()
    add_header(s4, "PHẦN 1: 3. Quy định Pháp định về Phạm vi TKCS & Cơ chế Thẩm định PCCC 2 Cổng", "Phân định nguyên tắc pháp lý trước khi áp dụng cho dự án cụ thể (Điều 17 NĐ 217/2026)")
    add_card(s4, 0.8, 1.8, 5.6, 5.0, "📋 Phạm vi TKCS Pháp định (Điều 17 NĐ 217)", [
        "Thuyết minh TKCS: Tổng quan kiến trúc, kết cấu, nguyên lý MEP chính, PCCC.",
        "Bản vẽ TKCS: Mặt bằng tổng thể, sơ đồ nguyên lý MEP, mặt cắt kết cấu chịu lực.",
        "Phục vụ Cơ quan Nhà nước thẩm định BCNCKT để cấp phép / phê duyệt dự án.",
        "Mô hình 3D/Combine, bản vẽ thi công chi tiết KHÔNG thuộc phạm vi thẩm định."
    ], accent_color=ACCENT_BLUE)
    add_card(s4, 6.9, 1.8, 5.6, 5.0, "🔥 Cơ chế Thẩm định PCCC 2 Cổng", [
        "Cơ quan Chuyên môn Xây dựng: Thẩm định An toàn cháy cho nhà theo QCVN 06:2022.",
        "Cảnh sát PCCC (PC07): Thẩm duyệt PCCC chuyên ngành (báo cháy, chữa cháy tự động).",
        "Loại bỏ trùng lặp nội dung kiểm tra giữa 2 cơ quan chuyên môn.",
        "Tạo cơ sở pháp lý minh bạch cho việc nộp và giải trình hồ sơ."
    ], accent_color=ACCENT_ORANGE)

    # -------------------------------------------------------------------------
    # SLIDE 5: PHẦN 2 - Thông số Quy mô & Phân cấp Dự án FPT DCHN03
    # -------------------------------------------------------------------------
    s5 = add_blank_slide()
    add_header(s5, "PHẦN 2: 1. Áp dụng Cụ thể: Thông số Quy mô & Phân cấp Dự án FPT DCHN03", "Rà soát thông số kỹ thuật chuẩn từ Thuyết minh QHTMB & TKCS chính thức dự án HN03")
    add_card(s5, 0.8, 1.8, 5.6, 5.0, "📐 Thông số Quy mô Kỹ thuật (Lô E9)", [
        "Diện tích khu đất (Lô E9): 27.206 m² (2,72 ha), KCN TLIP III, Phú Thọ.",
        "Diện tích xây dựng (Mật độ 45%): 12.243 m².",
        "Tổng diện tích sàn (Hệ số 1,4): 36.728 m².",
        "Quy mô: 3 tầng (chiều cao h <= 22m), gồm 3 khối DC + 1 khối MFB."
    ], accent_color=ACCENT_ORANGE)
    add_card(s5, 6.9, 1.8, 5.6, 5.0, "🏛️ Phân loại, Phân cấp & PCCC", [
        "Cấp công trình chính: CÔNG TRÌNH CẤP II (TT 34/2026/TT-BXD, niên hạn >= 50 năm).",
        "Phân nhóm dự án: DỰ ÁN NHÓM A (Hạ tầng CNTT & dữ liệu công suất lớn).",
        "Phân loại PCCC (QCVN 06:2022): Nhóm F4.3, Bậc chịu lửa Bậc II.",
        "Nguồn điện: 22kV đường S3 KCN, MBA 2500kVA (N+1) & 1000kVA."
    ], accent_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 6: PHẦN 2 - Thẩm quyền Thẩm định BCNCKT & PCCC tại Tỉnh Phú Thọ
    # -------------------------------------------------------------------------
    s6 = add_blank_slide()
    add_header(s6, "PHẦN 2: 2. Thẩm quyền Thẩm định BCNCKT & PCCC Dự án HN03 tại Tỉnh Phú Thọ", "Cơ chế phân công giải quyết hồ sơ Dự án Nhóm A / Công trình Cấp II tại địa phương")
    add_card(s6, 0.8, 1.8, 5.6, 5.0, "🏢 Sở Xây dựng / BQL KCN tỉnh Phú Thọ", [
        "Thẩm định BCNCKT / TKCS thuộc thẩm quyền Nhà nước cho Dự án Nhóm A / Cấp II.",
        "Thẩm định tuân thủ Quy hoạch 1/500 KCN Thăng Long Vĩnh Phúc (TLIP III).",
        "Kiểm tra kết cấu chịu lực Cấp II, an toàn PCCC tổng thể & đấu nối hạ tầng S3.",
        "Tích hợp kết quả thẩm định vào Thông báo BCNCKT."
    ], accent_color=ACCENT_ORANGE)
    add_card(s6, 6.9, 1.8, 5.6, 5.0, "🔥 Phòng Cảnh sát PCCC & CNCH (PC07 Công an Tỉnh Phú Thọ)", [
        "Thẩm duyệt thiết kế PCCC chuyên ngành theo QCVN 10, TCVN 7568, TCVN 3890.",
        "Thẩm duyệt hệ thống báo cháy tự động, chữa cháy khí/nước, cấp nước 30 l/s.",
        "Kiểm tra giải pháp xe chữa cháy tiếp cận công trình từ đường S3 KCN TLIP III.",
        "Nộp song song hồ sơ PCCC chuyên ngành để tối ưu thời gian."
    ], accent_color=ACCENT_GREEN)

    # -------------------------------------------------------------------------
    # SLIDE 7: PHẦN 2 - Đánh giá Thực trạng Hồ sơ & Lộ trình Trình nộp 3 Bước
    # -------------------------------------------------------------------------
    s7 = add_blank_slide()
    add_header(s7, "PHẦN 2: 3. Đánh giá Thực trạng Hồ sơ & Lộ trình Trình nộp 3 Bước với CĐT FPT", "Bảo đảm quy trình pháp lý chuẩn mực, đúng thẩm quyền và tối ưu thời gian cho CĐT FPT")
    add_card(s7, 0.8, 1.8, 5.6, 5.0, "📌 3 Bước Thực hiện Pháp lý Chuẩn", [
        "Bước 1: Khóa bộ Hồ sơ TKCS chuẩn Cấp II theo Nghị định 217/2026/NĐ-CP.",
        "Bước 2: Nộp BCNCKT / TKCS lên Sở Xây dựng / BQL KCN Phú Thọ & PCCC lên PC07 Phú Thọ.",
        "Bước 3: CĐT FPT phê duyệt BCNCKT và chuyển tiếp phát hành TKBVTC."
    ], accent_color=ACCENT_ORANGE)
    add_card(s7, 6.9, 1.8, 5.6, 5.0, "✅ Kết luận & Kiến nghị của TVTK", [
        "Mức độ thể hiện hiện tại (~80% TKBVTC) vượt xa yêu cầu pháp định của TKCS.",
        "Sử dụng đúng hồ sơ TKCS chuẩn để trình nộp cơ quan chuyên môn tỉnh Phú Thọ.",
        "Chuyển các nội dung nâng cao chi tiết sang giai đoạn Thiết kế triển khai sau TKCS.",
        "Liên danh IBST - FGE cam kết phối hợp chặt chẽ bảo vệ hồ sơ tại Phú Thọ."
    ], accent_color=ACCENT_GREEN)

    output_dir = Path(r"D:\GitHubProjects\ccba-legal-knowledge\.md\seminars\2026")
    output_dir.mkdir(parents=True, exist_ok=True)
    pptx_path = output_dir / "FPT_HN03_WORKSHOP_Luat_Xay_Dung_135_Structure_2Parts.pptx"
    prs.save(str(pptx_path))
    print(f"✅ SUCCESSFULLY GENERATED FPT HN03 WORKSHOP PPTX AT: {pptx_path}")

if __name__ == "__main__":
    create_fpt_hn03_presentation()
