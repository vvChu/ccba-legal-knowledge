"""
CCBA Legal Knowledge — Smoke Exhaust System Calculation Formulas.
Tính toán lưu lượng hút khói hành lang và sảnh thông tầng theo Phụ lục D QCVN 06:2022/BXD.
"""

from __future__ import annotations

import math

from formulas.models import CalculationResult, CalculationStep


def calc_corridor_smoke_exhaust_flow(
    door_width_m: float,
    door_height_m: float,
    door_leaves_count: int = 1,
    door_opening_factor: float = 1.0,
    smoke_temp_celsius: float = 300.0,
    safety_margin_factor: float = 1.1,
) -> CalculationResult:
    """Tính toán lưu lượng khối lượng và lưu lượng thể tích hút khói hành lang khi có cháy.
    
    Căn cứ: Phụ lục D QCVN 06:2022/BXD (Hệ thống bảo vệ chống khói) & Tiêu chuẩn tính toán kỹ thuật PCCC.

    Formula:
        G = 3420 * B * n * (H_d ^ 1.5) * K_d  (kg/h)
        rho_smoke = 353 / (273 + T_smoke)     (kg/m3)
        L_design = (G / rho_smoke) * safety_margin (m3/h)

    Args:
        door_width_m: Chiều rộng cánh cửa thoát nạn từ hành lang vào buồng thang (m).
        door_height_m: Chiều cao cửa thoát nạn (m).
        door_leaves_count: Số cánh cửa (thường là 1 hoặc 2).
        door_opening_factor: Hệ số mở cửa khi sơ tán n (thường là 1.0 với cửa mở trực tiếp).
        smoke_temp_celsius: Nhiệt độ khói tính toán (°C, mặc định 300°C theo Phụ lục D.9).
        safety_margin_factor: Hệ số an toàn rò rỉ đường ống (mặc định 1.1).
    """
    kd = 1.0  # Hệ số phụ thuộc loại cửa
    total_door_width = door_width_m * door_leaves_count
    h_pow_1_5 = math.pow(door_height_m, 1.5)

    # 1. Tính lưu lượng khối lượng G (kg/h)
    g_mass_kg_per_h = 3420.0 * total_door_width * door_opening_factor * h_pow_1_5 * kd

    # 2. Tính khối lượng riêng của khói ở nhiệt độ T_smoke
    t_kelvin = 273.15 + smoke_temp_celsius
    rho_smoke = 353.0 / t_kelvin

    # 3. Tính lưu lượng thể tích L (m3/h)
    l_volumetric_m3_per_h = (g_mass_kg_per_h / rho_smoke) * safety_margin_factor
    l_flow_m3_per_s = l_volumetric_m3_per_h / 3600.0

    steps = [
        CalculationStep(
            step_number=1,
            description="Tính lưu lượng khối lượng khói cần hút qua cửa thoát nạn của hành lang",
            formula_latex="G = 3420 \\times B \\times n \\times H_d^{1.5} \\times K_d",
            substitution=f"G = 3420 \\times {total_door_width:g} \\times {door_opening_factor:g} \\times ({door_height_m:g})^{{1.5}} \\times {kd:g}",
            result_text=f"{g_mass_kg_per_h:.2f} kg/h",
        ),
        CalculationStep(
            step_number=2,
            description=f"Tính khối lượng riêng của khói ở nhiệt độ tính toán T = {smoke_temp_celsius:g}°C",
            formula_latex="\\rho_{khói} = \\frac{353}{273.15 + T_{khói}}",
            substitution=f"\\rho_{{khói}} = 353 / (273.15 + {smoke_temp_celsius:g}) = 353 / {t_kelvin:.2f}",
            result_text=f"{rho_smoke:.4f} kg/m³",
        ),
        CalculationStep(
            step_number=3,
            description=f"Tính lưu lượng thể tích quạt hút khói (kèm hệ số an toàn {safety_margin_factor:g})",
            formula_latex="L = \\frac{G}{\\rho_{khói}} \\times k_{an\\_toàn}",
            substitution=f"L = ({g_mass_kg_per_h:.2f} / {rho_smoke:.4f}) \\times {safety_margin_factor:g}",
            result_text=f"{l_volumetric_m3_per_h:.2f} m³/h ({l_flow_m3_per_s:.2f} m³/s)",
        ),
    ]

    notes = [
        f"Nhiệt độ khói tính toán: {smoke_temp_celsius:g}°C. Khối lượng riêng tương ứng: {rho_smoke:.3f} kg/m³.",
        "Quy định Phụ lục D.9: Quạt hút khói hành lang phải đảm bảo giới hạn chịu lửa tối thiểu 0,5 giờ ở 300°C hoặc 1 giờ ở 400°C.",
        "Đường ống dẫn khói trong hành lang phải có giới hạn chịu lửa tối thiểu EI 30.",
    ]

    return CalculationResult(
        formula_id="F_SMOKE_EXHAUST_CORRIDOR",
        formula_name="Lưu lượng hút khói hành lang khi có cháy",
        standard_reference="Phụ lục D (Mục D.3, D.8, D.9) QCVN 06:2022/BXD",
        inputs={
            "door_width_m": door_width_m,
            "door_height_m": door_height_m,
            "door_leaves_count": door_leaves_count,
            "door_opening_factor": door_opening_factor,
            "smoke_temp_celsius": smoke_temp_celsius,
            "safety_margin_factor": safety_margin_factor,
        },
        outputs={
            "mass_flow_kg_per_h": round(g_mass_kg_per_h, 2),
            "smoke_density_kg_per_m3": round(rho_smoke, 4),
            "volumetric_flow_m3_per_h": round(l_volumetric_m3_per_h, 2),
            "volumetric_flow_m3_per_s": round(l_flow_m3_per_s, 2),
        },
        unit="m³/h",
        primary_value=round(l_volumetric_m3_per_h, 2),
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message=f"Lưu lượng quạt hút khói hành lang thiết kế tối thiểu: {l_volumetric_m3_per_h:,.0f} m³/h.",
    )


def calc_atrium_smoke_exhaust_flow(
    atrium_floor_area_m2: float,
    atrium_clear_height_m: float,
    smoke_layer_bottom_height_m: float = 2.5,
    fire_heat_release_rate_kw: float = 2500.0,
) -> CalculationResult:
    """Tính toán lưu lượng hút khói cho sảnh thông tầng (Atrium).
    
    Căn cứ: Phụ lục D QCVN 06:2022/BXD & Phương pháp cột khói màng Plume (NFPA 92B).
    """
    z_clear = max(atrium_clear_height_m - smoke_layer_bottom_height_m, 1.0)
    # Mass flow rate of plume at height z
    # M = 0.071 * Qc^(1/3) * z^(5/3) + 0.0018 * Qc  (kg/s)
    # With convective heat release rate Qc = 0.7 * Q_total
    q_c = 0.7 * fire_heat_release_rate_kw
    q_c_cube_root = math.pow(q_c, 1.0 / 3.0)
    z_pow_5_3 = math.pow(z_clear, 5.0 / 3.0)

    mass_flow_kg_per_s = 0.071 * q_c_cube_root * z_pow_5_3 + 0.0018 * q_c
    rho_atrium = 0.7  # Khối lượng riêng khói trung bình sảnh lớn
    volumetric_flow_m3_per_s = mass_flow_kg_per_s / rho_atrium
    volumetric_flow_m3_per_h = volumetric_flow_m3_per_s * 3600.0

    steps = [
        CalculationStep(
            step_number=1,
            description="Xác định công suất tỏa nhiệt đối lưu của đám cháy thiết kế",
            formula_latex="Q_c = 0.7 \\times Q_{cháy}",
            substitution=f"Q_c = 0.7 \\times {fire_heat_release_rate_kw:g}",
            result_text=f"{q_c:.1f} kW",
        ),
        CalculationStep(
            step_number=2,
            description="Xác định chiều cao tự do của cột khói dưới đáy lớp khói",
            formula_latex="Z = H_{thông\\_tầng} - H_{đáy\\_khói}",
            substitution=f"Z = {atrium_clear_height_m:g} - {smoke_layer_bottom_height_m:g}",
            result_text=f"{z_clear:.2f} m",
        ),
        CalculationStep(
            step_number=3,
            description="Tính lưu lượng khối lượng khói sinh ra trong cột khói (Plume model)",
            formula_latex="M = 0.071 \\times Q_c^{1/3} \\times Z^{5/3} + 0.0018 \\times Q_c",
            substitution=f"M = 0.071 \\times ({q_c:.1f})^{{1/3}} \\times ({z_clear:.2f})^{{5/3}} + 0.0018 \\times {q_c:.1f}",
            result_text=f"{mass_flow_kg_per_s:.2f} kg/s",
        ),
        CalculationStep(
            step_number=4,
            description="Tính lưu lượng thể tích cần hút cho sảnh thông tầng",
            formula_latex="L = \\frac{M}{\\rho} \\times 3600",
            substitution=f"L = ({mass_flow_kg_per_s:.2f} / {rho_atrium:g}) \\times 3600",
            result_text=f"{volumetric_flow_m3_per_h:.2f} m³/h",
        ),
    ]

    return CalculationResult(
        formula_id="F_SMOKE_EXHAUST_ATRIUM",
        formula_name="Lưu lượng hút khói sảnh thông tầng (Atrium)",
        standard_reference="Phụ lục D (Mục D.4) QCVN 06:2022/BXD",
        inputs={
            "atrium_floor_area_m2": atrium_floor_area_m2,
            "atrium_clear_height_m": atrium_clear_height_m,
            "smoke_layer_bottom_height_m": smoke_layer_bottom_height_m,
            "fire_heat_release_rate_kw": fire_heat_release_rate_kw,
        },
        outputs={
            "convective_heat_kw": round(q_c, 2),
            "smoke_mass_flow_kg_per_s": round(mass_flow_kg_per_s, 2),
            "volumetric_flow_m3_per_h": round(volumetric_flow_m3_per_h, 2),
        },
        unit="m³/h",
        primary_value=round(volumetric_flow_m3_per_h, 2),
        steps=steps,
        notes=[
            f"Cao độ đáy lớp khói bảo đảm tối thiểu {smoke_layer_bottom_height_m:g} m để an toàn cho người thoát nạn.",
            "Cần bố trí miệng hút khói phân bố đều trên đỉnh sảnh để tránh hiện tượng quẩn gió (plugholing).",
        ],
        is_compliant=True,
        compliance_message=f"Lưu lượng quạt hút khói sảnh thông tầng yêu cầu: {volumetric_flow_m3_per_h:,.0f} m³/h.",
    )
