"""
CCBA Legal Knowledge — PCCC Outdoor Fire Water Demand Formulas.
Tính toán lưu lượng cấp nước chữa cháy ngoài nhà theo Bảng 7, Bảng 8 QCVN 06:2022/BXD.
"""

from __future__ import annotations


from formulas.models import CalculationResult, CalculationStep


def calc_f1_f4_outdoor_water_demand(
    functional_group: str,
    building_volume_m3: float,
    floors_count: int,
    is_rural: bool = False,
) -> CalculationResult:
    """Tính toán lưu lượng nước cho chữa cháy ngoài nhà của nhà nhóm F1, F2, F3, F4.
    
    Căn cứ: Mục 5.1.2.2 và Bảng 8 QCVN 06:2022/BXD (Văn bản hợp nhất năm 2023).

    Args:
        functional_group: Nhóm nguy hiểm cháy theo công năng (F1.3, F1.4, F1.1, F1.2, F2, F3, F4).
        building_volume_m3: Khối tích công trình (m3).
        floors_count: Số tầng của công trình.
        is_rural: Công trình thuộc khu vực nông thôn (làng, xã) hay không.
    """
    func_upper = functional_group.upper().strip()
    volume_k = building_volume_m3 / 1000.0  # Đổi ra 1.000 m3
    steps: list[CalculationStep] = []
    notes: list[str] = []

    steps.append(
        CalculationStep(
            step_number=1,
            description="Quy đổi khối tích công trình sang đơn vị 1.000 m³",
            formula_latex="V_k = \\frac{V}{1000}",
            substitution=f"V_k = {building_volume_m3:g} / 1000",
            result_text=f"{volume_k:.2f} (nghìn m³)",
        )
    )

    # Xác định loại nhóm công năng
    is_residential = func_upper in ("F1.3", "F1.4", "F1.3, F1.4", "CHUNG CƯ", "NHÀ Ở")
    flow_l_per_s: float = 0.0

    if is_residential:
        category_name = "Nhóm 1 (Nhà ở chung cư F1.3, nhà ở riêng lẻ F1.4)"
        if floors_count <= 3:
            if volume_k <= 1.0:
                flow_l_per_s = 5.0 if is_rural else 10.0
            elif volume_k <= 5.0:
                flow_l_per_s = 5.0 if is_rural else 10.0
            elif volume_k <= 25.0:
                flow_l_per_s = 15.0
            elif volume_k <= 50.0:
                flow_l_per_s = 15.0
            else:
                flow_l_per_s = 20.0
        elif 3 < floors_count <= 12:
            if volume_k <= 1.0:
                flow_l_per_s = 10.0
            elif volume_k <= 5.0:
                flow_l_per_s = 15.0
            elif volume_k <= 25.0:
                flow_l_per_s = 15.0
            elif volume_k <= 50.0:
                flow_l_per_s = 20.0
            else:
                flow_l_per_s = 20.0
        elif 12 < floors_count <= 16:
            if volume_k <= 5.0:
                flow_l_per_s = 20.0
            elif volume_k <= 25.0:
                flow_l_per_s = 20.0
            elif volume_k <= 50.0:
                flow_l_per_s = 25.0
            else:
                flow_l_per_s = 25.0
        else:  # floors_count > 16
            if volume_k <= 5.0:
                flow_l_per_s = 20.0
            elif volume_k <= 25.0:
                flow_l_per_s = 25.0
            elif volume_k <= 50.0:
                flow_l_per_s = 25.0
            else:
                flow_l_per_s = 30.0

    else:
        category_name = "Nhóm 2 (Nhà công cộng F1.1, F1.2, F2, F3, F4)"
        if floors_count <= 3:
            if volume_k <= 1.0:
                flow_l_per_s = 5.0 if is_rural else 10.0
            elif volume_k <= 5.0:
                flow_l_per_s = 5.0 if is_rural else 10.0
            elif volume_k <= 25.0:
                flow_l_per_s = 15.0
            elif volume_k <= 50.0:
                flow_l_per_s = 20.0
            else:
                flow_l_per_s = 25.0
        elif 3 < floors_count <= 12:
            if volume_k <= 1.0:
                flow_l_per_s = 10.0
            elif volume_k <= 5.0:
                flow_l_per_s = 15.0
            elif volume_k <= 25.0:
                flow_l_per_s = 20.0
            elif volume_k <= 50.0:
                flow_l_per_s = 25.0
            else:
                flow_l_per_s = 30.0
        elif 12 < floors_count <= 16:
            if volume_k <= 5.0:
                flow_l_per_s = 20.0
            elif volume_k <= 25.0:
                flow_l_per_s = 25.0
            elif volume_k <= 50.0:
                flow_l_per_s = 30.0
            else:
                flow_l_per_s = 35.0
        else:  # floors_count > 16
            if volume_k <= 5.0:
                flow_l_per_s = 25.0
            elif volume_k <= 25.0:
                flow_l_per_s = 30.0
            elif volume_k <= 50.0:
                flow_l_per_s = 30.0
            else:
                flow_l_per_s = 35.0

    if is_rural and floors_count <= 3 and volume_k <= 5.0:
        notes.append("Áp dụng Ghi chú 1 chân Bảng 8: Nhà thuộc khu vực làng, xã nông thôn lấy lưu lượng 5 L/s.")

    notes.append(
        "Chú thích 1 Bảng 8: Nếu mạng đường ống ngoài nhà không đủ lưu lượng hoặc mạng cụt thì phải có bồn/bể nước bảo đảm chữa cháy trong 3 giờ."
    )

    steps.append(
        CalculationStep(
            step_number=2,
            description=f"Tra cứu Bảng 8 QCVN 06:2022 theo {category_name}, Số tầng = {floors_count}, Khối tích V = {volume_k:.2f} nghìn m³",
            formula_latex="Q_{cc\\_ngoai} = \\text{Tra Bảng 8}(Nhóm, Tầng, V)",
            substitution=f"Tra cứu: Nhóm={func_upper}, Số tầng={floors_count}, V={building_volume_m3:g} m³",
            result_text=f"{flow_l_per_s:g} L/s",
        )
    )

    return CalculationResult(
        formula_id="F_QCVN06_TABLE8",
        formula_name="Lưu lượng nước chữa cháy ngoài nhà (F1-F4)",
        standard_reference="Mục 5.1.2.2 & Bảng 8 QCVN 06:2022/BXD",
        inputs={
            "functional_group": functional_group,
            "building_volume_m3": building_volume_m3,
            "floors_count": floors_count,
            "is_rural": is_rural,
        },
        outputs={
            "required_flow_l_per_s": flow_l_per_s,
            "required_flow_m3_per_h": flow_l_per_s * 3.6,
        },
        unit="L/s",
        primary_value=flow_l_per_s,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message=f"Lưu lượng cấp nước chữa cháy ngoài nhà tối thiểu theo Bảng 8 là {flow_l_per_s:g} L/s ({flow_l_per_s * 3.6:.1f} m³/h).",
    )


def calc_fire_water_tank_capacity(
    outdoor_flow_l_per_s: float,
    duration_hours: float = 3.0,
    indoor_flow_l_per_s: float = 0.0,
    sprinkler_flow_l_per_s: float = 0.0,
    sprinkler_duration_hours: float = 1.0,
) -> CalculationResult:
    """Tính toán dung tích bể nước chữa cháy ngầm dự trữ.
    
    Căn cứ: Mục 5.1.4 QCVN 06:2022/BXD và TCVN 7336:2021.
    
    Formula:
        V_tank = (Q_outdoor * 3.6 * t_outdoor) + (Q_indoor * 3.6 * t_indoor) + (Q_sprinkler * 3.6 * t_sprinkler)
    """
    v_outdoor = outdoor_flow_l_per_s * 3.6 * duration_hours
    v_indoor = indoor_flow_l_per_s * 3.6 * duration_hours
    v_sprinkler = sprinkler_flow_l_per_s * 3.6 * sprinkler_duration_hours
    total_volume_m3 = v_outdoor + v_indoor + v_sprinkler

    steps = [
        CalculationStep(
            step_number=1,
            description="Tính dung tích nước dự trữ cho chữa cháy ngoài nhà",
            formula_latex="V_{ngoai} = Q_{ngoai} \\times 3.6 \\times t_{chua\\_chay}",
            substitution=f"V_{{ngoai}} = {outdoor_flow_l_per_s:g} \\times 3.6 \\times {duration_hours:g}",
            result_text=f"{v_outdoor:.2f} m³",
        )
    ]

    if indoor_flow_l_per_s > 0:
        steps.append(
            CalculationStep(
                step_number=2,
                description="Tính dung tích nước dự trữ cho họng nước chữa cháy trong nhà",
                formula_latex="V_{trong} = Q_{trong} \\times 3.6 \\times t_{trong}",
                substitution=f"V_{{trong}} = {indoor_flow_l_per_s:g} \\times 3.6 \\times {duration_hours:g}",
                result_text=f"{v_indoor:.2f} m³",
            )
        )

    if sprinkler_flow_l_per_s > 0:
        steps.append(
            CalculationStep(
                step_number=3,
                description="Tính dung tích nước cho hệ thống chữa cháy tự động Sprinkler",
                formula_latex="V_{sprinkler} = Q_{sprinkler} \\times 3.6 \\times t_{sprinkler}",
                substitution=f"V_{{sprinkler}} = {sprinkler_flow_l_per_s:g} \\times 3.6 \\times {sprinkler_duration_hours:g}",
                result_text=f"{v_sprinkler:.2f} m³",
            )
        )

    steps.append(
        CalculationStep(
            step_number=len(steps) + 1,
            description="Tổng hợp dung tích bể chứa nước chữa cháy",
            formula_latex="V_{tong} = V_{ngoai} + V_{trong} + V_{sprinkler}",
            substitution=f"V_{{tong}} = {v_outdoor:.2f} + {v_indoor:.2f} + {v_sprinkler:.2f}",
            result_text=f"{total_volume_m3:.2f} m³",
        )
    )

    return CalculationResult(
        formula_id="F_PCCC_TANK_CAPACITY",
        formula_name="Dung tích bể chứa nước chữa cháy",
        standard_reference="Mục 5.1.4 QCVN 06:2022/BXD & TCVN 7336:2021",
        inputs={
            "outdoor_flow_l_per_s": outdoor_flow_l_per_s,
            "duration_hours": duration_hours,
            "indoor_flow_l_per_s": indoor_flow_l_per_s,
            "sprinkler_flow_l_per_s": sprinkler_flow_l_per_s,
            "sprinkler_duration_hours": sprinkler_duration_hours,
        },
        outputs={
            "outdoor_volume_m3": round(v_outdoor, 2),
            "indoor_volume_m3": round(v_indoor, 2),
            "sprinkler_volume_m3": round(v_sprinkler, 2),
            "total_tank_volume_m3": round(total_volume_m3, 2),
        },
        unit="m³",
        primary_value=round(total_volume_m3, 2),
        steps=steps,
        notes=[
            f"Thời gian chữa cháy ngoài nhà: {duration_hours:g} giờ theo quy định Mục 5.1.4 QCVN 06:2022.",
            "Bể nước chữa cháy phải được chia làm tối thiểu 2 ngăn độc lập để bảo dưỡng mà không gián đoạn cấp nước.",
        ],
        is_compliant=True,
        compliance_message=f"Dung tích bể nước chữa cháy hữu ích tối thiểu yêu cầu là {total_volume_m3:.2f} m³.",
    )
