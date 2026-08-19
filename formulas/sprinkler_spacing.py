"""
CCBA Legal Knowledge — Automatic Sprinkler Spacing & Layout Formulas.
Tính toán khoảng cách, diện tích bảo vệ và số lượng đầu phun Sprinkler theo TCVN 7336:2021 & QCVN 06:2022/BXD.
"""

from __future__ import annotations

import math
from typing import Any

from formulas.models import CalculationResult, CalculationStep


def calc_sprinkler_density_and_spacing(
    hazard_group: str,
    sprinkler_k_factor: float = 80.0,
    min_pressure_bar: float = 1.0,
) -> CalculationResult:
    """Xác định cường độ phun, khoảng cách tối đa và diện tích bảo vệ của 1 đầu phun Sprinkler.
    
    Căn cứ: Bảng 1 và Bảng 2 TCVN 7336:2021 (Hệ thống chữa cháy tự động bằng nước Sprinkler).

    Args:
        hazard_group: Nhóm nguy cơ cháy (NHOM_1_THAP, NHOM_2_TRUNG_BINH_1, NHOM_2_TRUNG_BINH_2, NHOM_3_CAO).
        sprinkler_k_factor: Hệ số lưu lượng K của đầu phun (mặc định K = 80 L/(min·bar^0.5)).
        min_pressure_bar: Áp suất tối thiểu tại đầu phun (bar, mặc định 1.0 bar).
    """
    hg_norm = hazard_group.upper().strip()

    if "THAP" in hg_norm or "1" in hg_norm and "CAO" not in hg_norm and "2" not in hg_norm:
        group_name = "Nhóm 1 (Nguy cơ cháy thấp - Văn phòng, nhà ở, trường học, khách sạn)"
        intensity_l_s_m2 = 0.08
        max_area_m2 = 12.0
        max_spacing_m = 4.0
        design_area_m2 = 120.0
        duration_min = 30.0
    elif "TRUNG_BINH_2" in hg_norm or "TB2" in hg_norm:
        group_name = "Nhóm 2.2 (Nguy cơ cháy trung bình 2 - Trung tâm thương mại, gara ô tô, xưởng may)"
        intensity_l_s_m2 = 0.12
        max_area_m2 = 9.0
        max_spacing_m = 3.5
        design_area_m2 = 180.0
        duration_min = 60.0
    elif "CAO" in hg_norm or "3" in hg_norm or "4" in hg_norm:
        group_name = "Nhóm 3/4 (Nguy cơ cháy cao - Kho hàng chứa vật liệu dễ cháy, xưởng sơn)"
        intensity_l_s_m2 = 0.24
        max_area_m2 = 9.0
        max_spacing_m = 3.0
        design_area_m2 = 240.0
        duration_min = 90.0
    else:  # Mặc định Nhóm 2.1
        group_name = "Nhóm 2.1 (Nguy cơ cháy trung bình 1 - Bệnh viện, nhà hàng, thư viện)"
        intensity_l_s_m2 = 0.08
        max_area_m2 = 12.0
        max_spacing_m = 4.0
        design_area_m2 = 180.0
        duration_min = 60.0

    max_wall_distance_m = max_spacing_m / 2.0
    # Q_head = K * sqrt(P) (L/min) -> L/s
    q_head_l_per_min = sprinkler_k_factor * math.sqrt(min_pressure_bar)
    q_head_l_per_s = q_head_l_per_min / 60.0

    # System flow for design area
    total_system_flow_l_per_s = intensity_l_s_m2 * design_area_m2

    steps = [
        CalculationStep(
            step_number=1,
            description=f"Tra cứu thông số thiết kế theo {group_name}",
            formula_latex="i = \\text{Tra Bảng 1 TCVN 7336}, A_{max} = \\text{Tra Bảng 2}",
            substitution=f"Nhóm: {group_name}",
            result_text=f"Cường độ i = {intensity_l_s_m2:g} L/(s·m²), Diện tích bảo vệ A_max = {max_area_m2:g} m²",
        ),
        CalculationStep(
            step_number=2,
            description="Xác định khoảng cách tối đa giữa các đầu phun và khoảng cách tới tường",
            formula_latex="L_{max} = \\text{Quy chuẩn}, L_{tường} \\le \\frac{L_{max}}{2}",
            substitution=f"L_{{max}} = {max_spacing_m:g} m, L_{{tường}} \\le {max_spacing_m:g} / 2",
            result_text=f"Khoảng cách giữa các đầu phun ≤ {max_spacing_m:g} m, Cách tường ≤ {max_wall_distance_m:g} m",
        ),
        CalculationStep(
            step_number=3,
            description="Tính lưu lượng nước phun của 1 đầu phun ở áp suất thiết kế tối thiểu",
            formula_latex="q_{đầu\\_phun} = \\frac{K \\times \\sqrt{P}}{60}",
            substitution=f"q = ({sprinkler_k_factor:g} \\times \\sqrt{{{min_pressure_bar:g}}}) / 60",
            result_text=f"{q_head_l_per_s:.2f} L/s ({q_head_l_per_min:.1f} L/phút)",
        ),
        CalculationStep(
            step_number=4,
            description=f"Tính lưu lượng tổng hệ thống Sprinkler cho diện tích tính toán {design_area_m2:g} m²",
            formula_latex="Q_{sprinkler} = i \\times S_{tính\\_toán}",
            substitution=f"Q = {intensity_l_s_m2:g} \\times {design_area_m2:g}",
            result_text=f"{total_system_flow_l_per_s:.2f} L/s",
        ),
    ]

    return CalculationResult(
        formula_id="F_SPRINKLER_SPACING_TCVN7336",
        formula_name="Khoảng cách & Lưu lượng đầu phun Sprinkler",
        standard_reference="Bảng 1, Bảng 2 TCVN 7336:2021",
        inputs={
            "hazard_group": hazard_group,
            "sprinkler_k_factor": sprinkler_k_factor,
            "min_pressure_bar": min_pressure_bar,
        },
        outputs={
            "intensity_l_s_m2": intensity_l_s_m2,
            "max_coverage_area_m2": max_area_m2,
            "max_head_spacing_m": max_spacing_m,
            "max_wall_distance_m": max_wall_distance_m,
            "head_flow_l_per_s": round(q_head_l_per_s, 2),
            "design_area_m2": design_area_m2,
            "total_system_flow_l_per_s": round(total_system_flow_l_per_s, 2),
            "duration_minutes": duration_min,
        },
        unit="m",
        primary_value=max_spacing_m,
        steps=steps,
        notes=[
            f"Thời gian hoạt động yêu cầu của hệ thống Sprinkler: {duration_min:g} phút.",
            f"Khoảng cách từ đầu phun tới trần: 0,08 m đến 0,40 m.",
            "Khoảng cách tối thiểu giữa 2 đầu phun cạnh nhau không nhỏ hơn 1,5 m để tránh phun ướt làm nguội đầu phun kế bên.",
        ],
        is_compliant=True,
        compliance_message=f"Khoảng cách đầu phun tối đa: {max_spacing_m:g} m (Diện tích bảo vệ: {max_area_m2:g} m²/đầu). Lưu lượng trạm bơm Sprinkler: {total_system_flow_l_per_s:.1f} L/s.",
    )


def calc_sprinkler_room_layout(
    room_length_m: float,
    room_width_m: float,
    hazard_group: str = "NHOM_2_TRUNG_BINH_1",
) -> CalculationResult:
    """Tính toán bố trí lưới đầu phun Sprinkler tối ưu cho một gian phòng hoặc tầng.
    
    Căn cứ: TCVN 7336:2021.
    """
    density_res = calc_sprinkler_density_and_spacing(hazard_group)
    max_spacing_m = density_res.outputs["max_head_spacing_m"]
    max_wall_m = density_res.outputs["max_wall_distance_m"]
    max_area_m2 = density_res.outputs["max_coverage_area_m2"]

    room_area_m2 = room_length_m * room_width_m

    # Tính số hàng và số đầu phun mỗi hàng ban đầu theo khoảng cách
    n_length = max(1, math.ceil((room_length_m - 2 * max_wall_m) / max_spacing_m) + 1)
    n_width = max(1, math.ceil((room_width_m - 2 * max_wall_m) / max_spacing_m) + 1)

    # Đảm bảo tổng số đầu phun thỏa mãn diện tích bảo vệ tối đa A_max
    while (room_area_m2 / (n_length * n_width)) > max_area_m2:
        # Tăng dần số đầu phun ở chiều có khoảng cách thực tế lớn hơn
        if (room_length_m / n_length) >= (room_width_m / n_width):
            n_length += 1
        else:
            n_width += 1

    # Actual spacing
    actual_spacing_length = room_length_m / n_length
    actual_spacing_width = room_width_m / n_width
    actual_wall_length = actual_spacing_length / 2.0
    actual_wall_width = actual_spacing_width / 2.0

    total_heads = n_length * n_width
    area_per_head = room_area_m2 / total_heads

    steps = [
        CalculationStep(
            step_number=1,
            description="Tính diện tích gian phòng",
            formula_latex="S_{phòng} = L \\times W",
            substitution=f"S = {room_length_m:g} \\times {room_width_m:g}",
            result_text=f"{room_area_m2:.2f} m²",
        ),
        CalculationStep(
            step_number=2,
            description="Xác định số lượng dãy đầu phun theo chiều dài và chiều rộng",
            formula_latex="N_L = \\lceil \\frac{L - 2L_{tường}}{L_{max}} \\rceil + 1, \\quad N_W = \\lceil \\frac{W - 2L_{tường}}{L_{max}} \\rceil + 1",
            substitution=f"N_L = {n_length}, N_W = {n_width}",
            result_text=f"{n_length} đầu theo chiều dài × {n_width} đầu theo chiều rộng",
        ),
        CalculationStep(
            step_number=3,
            description="Tính tổng số lượng đầu phun và diện tích bảo vệ thực tế trên mỗi đầu",
            formula_latex="N_{tổng} = N_L \\times N_W, \\quad A_{thực\\_tế} = \\frac{S_{phòng}}{N_{tổng}}",
            substitution=f"N_{{tổng}} = {n_length} \\times {n_width} = {total_heads}, \\quad A = {room_area_m2:.2f} / {total_heads}",
            result_text=f"Tổng số: {total_heads} đầu phun (Diện tích bảo vệ: {area_per_head:.2f} m²/đầu ≤ {max_area_m2:g} m²)",
        ),
    ]

    is_compliant = (
        actual_spacing_length <= max_spacing_m
        and actual_spacing_width <= max_spacing_m
        and area_per_head <= max_area_m2
    )

    return CalculationResult(
        formula_id="F_SPRINKLER_ROOM_LAYOUT",
        formula_name="Bố trí mạng lưới đầu phun Sprinkler cho gian phòng",
        standard_reference="TCVN 7336:2021",
        inputs={
            "room_length_m": room_length_m,
            "room_width_m": room_width_m,
            "room_area_m2": room_area_m2,
            "hazard_group": hazard_group,
        },
        outputs={
            "total_heads": total_heads,
            "heads_along_length": n_length,
            "heads_along_width": n_width,
            "spacing_length_m": round(actual_spacing_length, 2),
            "spacing_width_m": round(actual_spacing_width, 2),
            "wall_distance_length_m": round(actual_wall_length, 2),
            "wall_distance_width_m": round(actual_wall_width, 2),
            "area_per_head_m2": round(area_per_head, 2),
        },
        unit="đầu phun",
        primary_value=float(total_heads),
        steps=steps,
        notes=[
            f"Lưới bố trí: {n_length} × {n_width} = {total_heads} đầu phun.",
            f"Khoảng cách thực tế: {actual_spacing_length:.2f} m × {actual_spacing_width:.2f} m (Cách tường: {actual_wall_length:.2f} m / {actual_wall_width:.2f} m).",
        ],
        is_compliant=is_compliant,
        compliance_message=f"Bố trí {total_heads} đầu phun Sprinkler bảo đảm tuân thủ khoảng cách và diện tích bảo vệ quy chuẩn."
        if is_compliant
        else "Lưới bố trí chưa đạt yêu cầu quy chuẩn!",
    )
