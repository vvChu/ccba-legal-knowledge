"""
CCBA Legal Knowledge — Deflection & Drift Limits Deterministic Solvers (TCVN 2737:2023 Phụ lục G & H).
Bộ giải xác định kiểm tra độ võng đứng giới hạn [fu], chuyển vị ngang [fu] và hệ số tầm quan trọng gamma_n (ADR 0020 & ADR 0034).
"""

from __future__ import annotations

from typing import Any

from formulas.models import CalculationResult, CalculationStep


def calc_vertical_deflection_limit(
    element_type: str = "roof_floor_visible",
    span_L: float = 6.0,
    is_cantilever: bool = False,
    room_height: float = 4.0,
    crane_control: str = "cabin",
    crane_group: str = "A1_A6",
    rail_type: str = "none",
) -> CalculationResult:
    """Tính toán độ võng đứng giới hạn [fu] cho dầm, sàn, giàn, xà gồ, dầm cầu trục theo Phụ lục G TCVN 2737:2023.

    Căn cứ: Bảng G.1, Bảng G.4 và Mục G.2.5.4 TCVN 2737:2023.

    Args:
        element_type: Loại cấu kiện ('roof_floor_visible', 'crane_girder', 'floor_moving_load', 'parking_floor', 'lintel_wall', 'prestress_camber').
        span_L: Nhịp tính toán L (m).
        is_cantilever: True nếu là dầm/bản công xôn (khi đó L_eff = 2 * L_cantilever).
        room_height: Chiều cao thông thủy phòng (m, dùng để xét ngưỡng nhịp phòng <= 6m).
        crane_control: 'cabin' (điều khiển từ cabin) hoặc 'floor' (từ nền).
        crane_group: Chế độ làm việc cầu trục ('A1_A6', 'A7', 'A8').
        rail_type: Loại đường ray ('narrow', 'wide', 'none').
    """
    if span_L <= 0:
        raise ValueError("Nhịp tính toán span_L phải > 0")

    L_eff = 2.0 * span_L if is_cantilever else span_L
    steps: list[CalculationStep] = []
    notes: list[str] = []

    if is_cantilever:
        notes.append(f"Cấu kiện công xôn: Chiều dài vươn L={span_L:g}m -> Nhịp tương đương L_eff = 2*L = {L_eff:g}m (CHÚ THÍCH 1 Bảng G.1).")

    el_norm = element_type.strip().lower()

    if el_norm in ("roof_floor_visible", "dam_san_nhin_thay"):
        desc = "Dầm, giàn, xà, bản mái và sàn tầng nhìn thấy được (Bảng G.1 mục 2a - Thẩm mỹ & tâm lý)"
        is_low_room = room_height <= 6.0
        if is_low_room:
            notes.append(f"Chiều cao phòng h={room_height:g}m <= 6m: Áp dụng ngưỡng nhịp rút gọn trong ngoặc đơn (CHÚ THÍCH 3).")
            # Thresholds: L<=1: 120, L=3: 150, L=6: 200, L=12: 250, L>=24: 300
            pts = [(1.0, 120.0), (3.0, 150.0), (6.0, 200.0), (12.0, 250.0), (24.0, 300.0)]
        else:
            # Thresholds: L<=1: 120, L=3: 150, L=6: 200, L=24: 250, L>=36: 300
            pts = [(1.0, 120.0), (3.0, 150.0), (6.0, 200.0), (24.0, 250.0), (36.0, 300.0)]

        if L_eff <= pts[0][0]:
            denom = pts[0][1]
        elif L_eff >= pts[-1][0]:
            denom = pts[-1][1]
        else:
            denom = pts[0][1]
            for i in range(len(pts) - 1):
                x1, y1 = pts[i]
                x2, y2 = pts[i + 1]
                if x1 <= L_eff <= x2:
                    denom = y1 + (L_eff - x1) * (y2 - y1) / (x2 - x1)
                    break

        denom_rounded = round(denom, 1)
        fu_m = L_eff / denom_rounded
        fu_mm = round(fu_m * 1000.0, 2)
        formula_latex = rf"[f_u] = \frac{{L}}{{{denom_rounded:g}}}"
        subst = f"[fu] = {L_eff:g} / {denom_rounded:g} = {fu_m:.4f} m = {fu_mm:g} mm"

    elif el_norm in ("crane_girder", "dam_cau_truc"):
        desc = "Dầm đỡ cần trục kiểu cầu / cần trục treo (Bảng G.1 mục 1 & Bảng G.4 mục 1)"
        if crane_control.lower() == "floor":
            denom = 250.0
            formula_latex = r"[f_u] = \frac{L}{250}"
            notes.append("Điều khiển từ dưới nền: [fu] = L / 250 (Bảng G.4 mục 1a).")
        else:
            grp_norm = crane_group.upper().replace("-", "_")
            if "A8" in grp_norm:
                denom = 600.0
            elif "A7" in grp_norm:
                denom = 500.0
            else:
                denom = 400.0
            formula_latex = rf"[f_u] = \frac{{L}}{{{int(denom)}}}"
            notes.append(f"Điều khiển từ cabin chế độ {crane_group}: [fu] = L / {int(denom)}.")

        fu_m = L_eff / denom
        fu_mm = round(fu_m * 1000.0, 2)
        subst = f"[fu] = {L_eff:g} / {denom:g} = {fu_m:.4f} m = {fu_mm:g} mm"

    elif el_norm in ("floor_moving_load", "san_tai_trong_di_dong"):
        desc = "Sàn tầng chịu tải trọng di chuyển (Bảng G.1 mục 2c / G.4 mục 2c)"
        r_norm = rail_type.lower()
        if "narrow" in r_norm or "hep" in r_norm:
            denom = 400.0
            notes.append("Tải trọng di chuyển trên ray khổ hẹp: [fu] = L / 400.")
        elif "wide" in r_norm or "rong" in r_norm:
            denom = 500.0
            notes.append("Tải trọng di chuyển trên ray khổ rộng: [fu] = L / 500.")
        else:
            denom = 350.0
            notes.append("Tải trọng di chuyển trên nền không ray: [fu] = L / 350.")

        formula_latex = rf"[f_u] = \frac{{L}}{{{int(denom)}}}"
        fu_m = L_eff / denom
        fu_mm = round(fu_m * 1000.0, 2)
        subst = f"[fu] = {L_eff:g} / {denom:g} = {fu_m:.4f} m = {fu_mm:g} mm"

    elif el_norm in ("parking_floor", "san_bai_do_xe"):
        desc = "Mái và sàn tầng bãi đỗ xe trong nhà (Bảng G.1 mục 2d / Bảng G.4 mục 2d)"
        pts = [(6.0, 200.0), (12.0, 250.0), (24.0, 300.0)]
        if L_eff <= pts[0][0]:
            denom = pts[0][1]
        elif L_eff >= pts[-1][0]:
            denom = pts[-1][1]
        else:
            denom = pts[0][1]
            for i in range(len(pts) - 1):
                x1, y1 = pts[i]
                x2, y2 = pts[i + 1]
                if x1 <= L_eff <= x2:
                    denom = y1 + (L_eff - x1) * (y2 - y1) / (x2 - x1)
                    break

        denom_rounded = round(denom, 1)
        fu_m = L_eff / denom_rounded
        fu_mm = round(fu_m * 1000.0, 2)
        formula_latex = rf"[f_u] = \frac{{L}}{{{denom_rounded:g}}}"
        subst = f"[fu] = {L_eff:g} / {denom_rounded:g} = {fu_m:.4f} m = {fu_mm:g} mm"

    elif el_norm in ("lintel_wall", "lanh_to_tuong_treo"):
        desc = "Lanh tô, tấm tường treo phía trên lỗ cửa (Bảng G.4 mục 3)"
        denom = 200.0
        formula_latex = r"[f_u] = \frac{L}{200}"
        fu_m = L_eff / denom
        fu_mm = round(fu_m * 1000.0, 2)
        subst = f"[fu] = {L_eff:g} / 200 = {fu_m:.4f} m = {fu_mm:g} mm"

    elif el_norm in ("prestress_camber", "do_vong_ung_suat_truoc"):
        desc = "Độ vồng giới hạn do lực nén trước (Mục G.2.5.4)"
        if L_eff <= 3.0:
            fu_mm = 15.0
        elif L_eff >= 12.0:
            fu_mm = 40.0
        else:
            fu_mm = 15.0 + (L_eff - 3.0) * (40.0 - 15.0) / (12.0 - 3.0)
            fu_mm = round(fu_mm, 2)
        fu_m = round(fu_mm / 1000.0, 4)
        formula_latex = r"[f_u]\text{ nội suy 15 mm đến 40 mm}"
        subst = f"L = {L_eff:g} m -> [fu] = {fu_mm:g} mm"
        notes.append("Căn cứ Mục G.2.5.4: L <= 3m: 15mm; L >= 12m: 40mm; nội suy tuyến tính.")

    else:
        raise ValueError(
            f"Loại cấu kiện '{element_type}' không được hỗ trợ. "
            "Chọn 'roof_floor_visible', 'crane_girder', 'floor_moving_load', 'parking_floor', 'lintel_wall', 'prestress_camber'."
        )

    steps.append(
        CalculationStep(
            step_number=1,
            description=f"Xác định độ võng đứng giới hạn cho {desc}",
            formula_latex=formula_latex,
            substitution=subst,
            result_text=f"[fu] = {fu_mm:g} mm ({fu_m:g} m)",
        )
    )

    return CalculationResult(
        formula_id="F_DEFLECTION_TCVN2737_G_VERT",
        formula_name=f"Độ võng đứng giới hạn [fu] ({desc})",
        standard_reference="Bảng G.1, Bảng G.4 & Mục G.2.5.4 Phụ lục G TCVN 2737:2023",
        inputs={
            "element_type": element_type,
            "span_L": span_L,
            "is_cantilever": is_cantilever,
            "room_height": room_height,
            "crane_control": crane_control,
            "crane_group": crane_group,
            "rail_type": rail_type,
        },
        outputs={
            "fu_limit_mm": fu_mm,
            "fu_limit_m": fu_m,
            "L_effective_m": L_eff,
        },
        unit="mm",
        primary_value=fu_mm,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message=f"Đã xác định độ võng đứng giới hạn [fu] = {fu_mm:g} mm cho {desc}.",
    )


def calc_horizontal_drift_limit(
    structure_type: str = "multistory_building_overall",
    total_height_h: float = 30.0,
    story_height_hs: float = 3.6,
    partition_material: str = "brick_concrete_gypsum",
    connection_type: str = "rigid",
    crane_group: str = "A1_A3",
) -> CalculationResult:
    """Tính toán chuyển vị ngang giới hạn [fu] theo Phụ lục G TCVN 2737:2023.

    Căn cứ: Bảng G.3, Bảng G.5 & Mục G.2.4.2 TCVN 2737:2023.

    Args:
        structure_type: 'multistory_building_overall', 'multistory_single_story', 'single_story_building', 'crane_column', 'temperature_settlement_column'.
        total_height_h: Chiều cao toàn nhà h (m).
        story_height_hs: Chiều cao tầng hs (m).
        partition_material: Vật liệu tường/vách ('brick_concrete_gypsum', 'natural_stone_ceramic', 'glass_curtain').
        connection_type: Loại liên kết khung - tường ('rigid' / 'cung', 'flexible' / 'mem').
        crane_group: Nhóm chế độ làm việc cầu trục ('A1_A3', 'A4_A6', 'A7_A8').
    """
    steps: list[CalculationStep] = []
    notes: list[str] = []
    st_norm = structure_type.strip().lower()

    if st_norm in ("multistory_building_overall", "nha_nhieu_tang_tong_the"):
        if total_height_h <= 0:
            raise ValueError("Chiều cao toàn nhà total_height_h phải > 0")
        desc = "Toàn bộ nhà nhiều tầng (Bảng G.5 mục 1)"
        denom = 500.0
        formula_latex = r"[f_u] = \frac{h}{500}"
        fu_m = total_height_h / denom
        fu_mm = round(fu_m * 1000.0, 2)
        subst = f"[fu] = {total_height_h:g} / 500 = {fu_m:.4f} m = {fu_mm:g} mm"
        notes.append("Chuyển vị đỉnh toàn nhà nhiều tầng theo yêu cầu cấu tạo: [fu] = h / 500.")

    elif st_norm in ("multistory_single_story", "mot_tang_nha_nhieu_tang"):
        if story_height_hs <= 0:
            raise ValueError("Chiều cao tầng story_height_hs phải > 0")
        desc = "Một tầng của nhà nhiều tầng (Bảng G.5 mục 2)"
        is_rigid = connection_type.strip().lower() in ("rigid", "cung")
        mat_norm = partition_material.strip().lower()

        if is_rigid:
            if "stone" in mat_norm or "ceramic" in mat_norm or "da" in mat_norm:
                denom = 700.0
                desc_detail = "Tường ốp đá tự nhiên / gạch ceramic liên kết cứng (Bảng G.5 mục 2b)"
            else:
                denom = 500.0
                desc_detail = "Tường gạch / BTCT / thạch cao liên kết cứng (Bảng G.5 mục 2a)"
        else:
            denom = 300.0
            desc_detail = "Tường và tường ngăn liên kết mềm (Bảng G.5 mục 2c)"

        formula_latex = rf"[f_u] = \frac{{h_s}}{{{int(denom)}}}"
        fu_m = story_height_hs / denom
        fu_mm = round(fu_m * 1000.0, 2)
        subst = f"[fu] = {story_height_hs:g} / {denom:g} = {fu_m:.4f} m = {fu_mm:g} mm"
        notes.append(desc_detail)

    elif st_norm in ("single_story_building", "nha_mot_tang"):
        if story_height_hs <= 0:
            raise ValueError("Chiều cao tầng story_height_hs phải > 0")
        desc = "Nhà một tầng tường tự chịu lực (Bảng G.5 mục 3)"
        denom = 300.0
        formula_latex = r"[f_u] = \frac{h_s}{300}"
        fu_m = story_height_hs / denom
        fu_mm = round(fu_m * 1000.0, 2)
        subst = f"[fu] = {story_height_hs:g} / 300 = {fu_m:.4f} m = {fu_mm:g} mm"
        notes.append("Nhà một tầng liên kết mềm: [fu] = hs / 300 (CHÚ THÍCH 3: có thể tăng 30% nếu là tường treo, tối đa hs/150).")

    elif st_norm in ("crane_column", "cot_cau_truc"):
        if story_height_hs <= 0:
            raise ValueError("Chiều cao h từ móng đến đỉnh ray phải > 0")
        desc = "Cột nhà có cầu trục do lực hãm ngang (Bảng G.3)"
        grp_norm = crane_group.upper().replace("-", "_")
        if "A7" in grp_norm or "A8" in grp_norm:
            denom = 2000.0
        elif "A4" in grp_norm or "A5" in grp_norm or "A6" in grp_norm:
            denom = 1000.0
        else:
            denom = 500.0

        formula_latex = rf"[f_u] = \max\left(\frac{{h}}{{{int(denom)}}}, 6\text{{ mm}}\right)"
        fu_calc_mm = (story_height_hs / denom) * 1000.0
        fu_mm = round(max(fu_calc_mm, 6.0), 2)
        fu_m = round(fu_mm / 1000.0, 4)
        subst = f"[fu] = max({story_height_hs:g} * 1000 / {denom:g} = {fu_calc_mm:g} mm, 6 mm) = {fu_mm:g} mm"
        notes.append(f"Cột nhà có cầu trục chế độ {crane_group}: [fu] = h / {int(denom)} nhưng không nhỏ hơn 6mm (Bảng G.3).")

    elif st_norm in ("temperature_settlement_column", "cot_nhiet_lun"):
        if story_height_hs <= 0:
            raise ValueError("Chiều cao tầng story_height_hs phải > 0")
        desc = "Cột nhà khung do tác động nhiệt khí hậu & lún (Mục G.2.4.2)"
        mat_norm = partition_material.strip().lower()
        if "stone" in mat_norm or "ceramic" in mat_norm or "glass" in mat_norm:
            denom = 200.0
            notes.append("Tường ốp đá tự nhiên / gạch ceramic / vách kính: [fu] = hs / 200.")
        else:
            denom = 150.0
            notes.append("Tường gạch / bê tông / thạch cao / panel treo: [fu] = hs / 150.")

        formula_latex = rf"[f_u] = \frac{{h_s}}{{{int(denom)}}}"
        fu_m = story_height_hs / denom
        fu_mm = round(fu_m * 1000.0, 2)
        subst = f"[fu] = {story_height_hs:g} / {denom:g} = {fu_m:.4f} m = {fu_mm:g} mm"

    else:
        raise ValueError(
            f"Loại kết cấu '{structure_type}' không được hỗ trợ. "
            "Chọn 'multistory_building_overall', 'multistory_single_story', 'single_story_building', 'crane_column', 'temperature_settlement_column'."
        )

    steps.append(
        CalculationStep(
            step_number=1,
            description=f"Xác định chuyển vị ngang giới hạn cho {desc}",
            formula_latex=formula_latex,
            substitution=subst,
            result_text=f"[fu] = {fu_mm:g} mm ({fu_m:g} m)",
        )
    )

    return CalculationResult(
        formula_id="F_DRIFT_TCVN2737_G_HORIZ",
        formula_name=f"Chuyển vị ngang giới hạn [fu] ({desc})",
        standard_reference="Bảng G.3, Bảng G.5 & Mục G.2.4.2 Phụ lục G TCVN 2737:2023",
        inputs={
            "structure_type": structure_type,
            "total_height_h": total_height_h,
            "story_height_hs": story_height_hs,
            "partition_material": partition_material,
            "connection_type": connection_type,
            "crane_group": crane_group,
        },
        outputs={
            "fu_limit_mm": fu_mm,
            "fu_limit_m": fu_m,
        },
        unit="mm",
        primary_value=fu_mm,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message=f"Đã xác định chuyển vị ngang giới hạn [fu] = {fu_mm:g} mm cho {desc}.",
    )


def calc_importance_factor_gamma_n(
    consequence_class: str = "C2",
    limit_state: str = "ULS",
    building_height: float = 0.0,
    span_length: float = 0.0,
) -> CalculationResult:
    """Xác định hệ số tầm quan trọng gamma_n theo Phụ lục H TCVN 2737:2023.

    Căn cứ: Bảng H.1 và Mục H.1 - H.3 Phụ lục H TCVN 2737:2023.

    Args:
        consequence_class: Cấp hậu quả công trình ('C1', 'C2', 'C3' theo QCVN 03:2022/BXD).
        limit_state: Trạng thái giới hạn ('ULS' / 'TTGH1' hoặc 'SLS' / 'TTGH2').
        building_height: Chiều cao công trình (m, nếu > 250m -> gamma_n >= 1.2).
        span_length: Nhịp kết cấu lớn nhất không có trụ trung gian (m, nếu > 120m -> gamma_n >= 1.2).
    """
    steps: list[CalculationStep] = []
    notes: list[str] = []

    cc_norm = consequence_class.strip().upper()
    ls_norm = limit_state.strip().upper()

    if ls_norm in ("SLS", "TTGH2", "TRANG_THAI_GIOI_HAN_2"):
        gamma_n = 1.0
        formula_latex = r"\gamma_n = 1{,}0\text{ (Trạng thái giới hạn thứ hai)}"
        subst = "Mục H.3: Tính toán theo TTGH2 lấy gamma_n = 1.0."
        desc = "Trạng thái giới hạn thứ hai (SLS)"
        notes.append("Mục H.3: Lấy gamma_n = 1.0 đối với mọi cấp công trình khi tính theo TTGH2.")
    else:
        desc = f"Cấp hậu quả {cc_norm} (Trạng thái giới hạn thứ nhất - ULS)"
        if cc_norm == "C1":
            base_gamma = 0.87
        elif cc_norm == "C3":
            base_gamma = 1.15
        elif cc_norm == "C2":
            base_gamma = 1.00
        else:
            raise ValueError(f"Cấp hậu quả '{consequence_class}' không hợp lệ. Chọn 'C1', 'C2' hoặc 'C3'.")

        gamma_n = base_gamma
        formula_latex = rf"\gamma_n = {base_gamma:g}"
        subst = f"Bảng H.1: Cấp hậu quả {cc_norm} -> gamma_n = {base_gamma:g}."

        if building_height > 250.0 or span_length > 120.0:
            gamma_n = max(gamma_n, 1.20)
            formula_latex = r"\gamma_n \ge 1{,}20\text{ (Công trình siêu cao hoặc nhịp lớn)}"
            reason = []
            if building_height > 250.0:
                reason.append(f"Chiều cao h={building_height:g}m > 250m")
            if span_length > 120.0:
                reason.append(f"Nhịp L={span_length:g}m > 120m")
            subst += f" [CHÚ THÍCH Bảng H.1: {', '.join(reason)} -> lấy gamma_n = 1.20]"
            notes.append(f"Áp dụng CHÚ THÍCH Bảng H.1: {', '.join(reason)} -> gamma_n = 1.20.")

    steps.append(
        CalculationStep(
            step_number=1,
            description=f"Xác định hệ số tầm quan trọng gamma_n cho {desc}",
            formula_latex=formula_latex,
            substitution=subst,
            result_text=f"gamma_n = {gamma_n:g}",
        )
    )

    return CalculationResult(
        formula_id="F_IMPORTANCE_TCVN2737_H_GAMMA_N",
        formula_name=f"Hệ số tầm quan trọng gamma_n ({desc})",
        standard_reference="Bảng H.1 & Mục H.3 Phụ lục H TCVN 2737:2023",
        inputs={
            "consequence_class": consequence_class,
            "limit_state": limit_state,
            "building_height": building_height,
            "span_length": span_length,
        },
        outputs={"gamma_n": gamma_n},
        unit="",
        primary_value=gamma_n,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message=f"Đã xác định hệ số tầm quan trọng gamma_n = {gamma_n:g} cho {desc}.",
    )


def check_deflection_and_drift_limits(
    actual_value_mm: float,
    check_type: str = "vertical_deflection",
    params: dict[str, Any] | None = None,
) -> CalculationResult:
    """Master Facade kiểm tra điều kiện an toàn độ võng/chuyển vị f <= [fu] (Phụ lục G & H TCVN 2737:2023).

    Args:
        actual_value_mm: Giá trị độ võng/chuyển vị tính toán thực tế f (mm).
        check_type: 'vertical_deflection' (độ võng đứng) hoặc 'horizontal_drift' (chuyển vị ngang).
        params: Dict các tham số truyền cho bộ giải giới hạn tương ứng.
    """
    if actual_value_mm < 0:
        raise ValueError("Giá trị chuyển vị thực tế actual_value_mm phải >= 0")

    p = params or {}
    chk_norm = check_type.strip().lower()

    if "vert" in chk_norm or "vong" in chk_norm:
        limit_res = calc_vertical_deflection_limit(**p)
        check_title = "Kiểm tra Độ Võng Đứng Kết Cấu"
    elif "horiz" in chk_norm or "drift" in chk_norm or "chuyen_vi" in chk_norm:
        limit_res = calc_horizontal_drift_limit(**p)
        check_title = "Kiểm tra Chuyển Vị Ngang Kết Cấu"
    else:
        raise ValueError(f"Loại kiểm tra '{check_type}' không hợp lệ. Chọn 'vertical_deflection' hoặc 'horizontal_drift'.")

    limit_val_mm = limit_res.primary_value
    ratio = round(actual_value_mm / limit_val_mm, 3) if limit_val_mm > 0 else 0.0
    is_ok = actual_value_mm <= limit_val_mm
    margin_pct = round((1.0 - ratio) * 100.0, 1)

    steps: list[CalculationStep] = list(limit_res.steps)

    status_str = "THỎA MÃN (ĐẠT)" if is_ok else "KHÔNG THỎA MÃN (VƯỢT GIỚI HẠN)"
    steps.append(
        CalculationStep(
            step_number=len(steps) + 1,
            description="Đánh giá điều kiện an toàn chuyển vị f <= [fu]",
            formula_latex=r"\text{Điều kiện: } f \le [f_u]",
            substitution=f"f = {actual_value_mm:g} mm {'<=' if is_ok else '>'} [fu] = {limit_val_mm:g} mm (Tỷ số f/[fu] = {ratio:g})",
            result_text=f"Kết luận: {status_str} (Dư biên an toàn: {margin_pct:g}%)",
        )
    )

    notes = list(limit_res.notes)
    notes.append(f"Giá trị thực tế kiểm tra: f = {actual_value_mm:g} mm.")
    notes.append(f"Tỷ số sử dụng: f/[fu] = {ratio:.1%} ({status_str}).")

    msg = (
        f"KẾT QUẢ: {status_str}. Giá trị f = {actual_value_mm:g}mm so với giới hạn [fu] = {limit_val_mm:g}mm "
        f"(Tỷ lệ: {ratio:.1%}, Dư biên an toàn: {margin_pct:g}%)."
    )

    return CalculationResult(
        formula_id="F_CHECK_DEFLECTION_DRIFT_COMPLIANCE",
        formula_name=f"{check_title} (f <= [fu])",
        standard_reference="Phụ lục G & H TCVN 2737:2023",
        inputs={
            "actual_value_mm": actual_value_mm,
            "check_type": check_type,
            "params": p,
        },
        outputs={
            "actual_value_mm": actual_value_mm,
            "limit_value_mm": limit_val_mm,
            "utilization_ratio": ratio,
            "safety_margin_percent": margin_pct,
            "is_compliant": is_ok,
        },
        unit="mm",
        primary_value=ratio,
        steps=steps,
        notes=notes,
        is_compliant=is_ok,
        compliance_message=msg,
    )
