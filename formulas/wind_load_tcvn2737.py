"""
CCBA Legal Knowledge — Deterministic Wind Load Formula Solver (TCVN 2737:2023 - Phụ lục F).
Tính toán chính xác hệ số khí động cho tường phẳng độc lập và mái dốc 2 phía (ADR 0020).
"""

from __future__ import annotations

from typing import Any
from formulas.models import CalculationResult, CalculationStep


def _interp(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """Nội suy tuyến tính cơ bản."""
    if x1 == x0:
        return y0
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


# ===========================================================================
# 1. BẢNG F.1 & HÌNH F.1: TƯỜNG PHẲNG ĐỘC LẬP VÀ HÀNG RÀO
# ===========================================================================

def calc_freestanding_wall_aerodynamic_coeff(
    length_L: float,
    height_h: float,
    solidity_ratio_phi: float = 1.0,
    has_return_corner: bool = False,
    return_corner_length: float = 0.0,
) -> CalculationResult:
    """Tính toán hệ số khí động c_x cho tường phẳng độc lập và hàng rào (Bảng F.1 / Hình F.1).

    Căn cứ: Mục F.1.1, Hình F.1 và Bảng F.1 Phụ lục F TCVN 2737:2023.

    Args:
        length_L: Chiều dài tường (m).
        height_h: Chiều cao tường (m).
        solidity_ratio_phi: Hệ số đặc phi (0.8 <= phi <= 1.0, mặc định 1.0).
        has_return_corner: bool (tường có bẻ góc hay không).
        return_corner_length: Chiều dài phần bẻ góc l_ret (m, mặc định 0.0).
    """
    if height_h <= 0:
        raise ValueError("Chiều cao tường h phải > 0")
    if length_L <= 0:
        raise ValueError("Chiều dài tường L phải > 0")

    phi = max(0.8, min(1.0, solidity_ratio_phi))
    ratio_L_h = length_L / height_h
    l_ret = return_corner_length if has_return_corner or return_corner_length > 0 else 0.0
    is_return = has_return_corner or l_ret >= height_h

    steps: list[CalculationStep] = []
    notes: list[str] = []

    steps.append(
        CalculationStep(
            step_number=1,
            description="Xác định tỷ lệ hình học L/h và hệ số đặc φ",
            formula_latex=r"\lambda = \frac{L}{h}",
            substitution=rf"\lambda = {length_L:g}/{height_h:g} = {ratio_L_h:.2f}; \varphi = {phi:g}",
            result_text=f"L/h = {ratio_L_h:.2f}, φ = {phi:g}",
        )
    )

    # 1. Xác định hệ số khi phi = 1.0
    # Straight wall at phi = 1.0
    if ratio_L_h <= 3.0:
        cx_straight_1_0 = {"Vùng A": 2.3, "Vùng B": 1.4, "Vùng C": 1.2, "Vùng D": 1.2}
        interp_desc = f"L/h = {ratio_L_h:.2f} <= 3.0 (Tra trực tiếp hàng L/h <= 3)"
    elif ratio_L_h <= 5.0:
        cx_straight_1_0 = {
            "Vùng A": round(_interp(ratio_L_h, 3.0, 5.0, 2.3, 2.9), 3),
            "Vùng B": round(_interp(ratio_L_h, 3.0, 5.0, 1.4, 1.8), 3),
            "Vùng C": round(_interp(ratio_L_h, 3.0, 5.0, 1.2, 1.4), 3),
            "Vùng D": 1.2,
        }
        interp_desc = f"3.0 < L/h = {ratio_L_h:.2f} <= 5.0 (Nội suy tuyến tính giữa L/h=3 và L/h=5)"
    elif ratio_L_h < 10.0:
        cx_straight_1_0 = {
            "Vùng A": round(_interp(ratio_L_h, 5.0, 10.0, 2.9, 3.4), 3),
            "Vùng B": round(_interp(ratio_L_h, 5.0, 10.0, 1.8, 2.1), 3),
            "Vùng C": round(_interp(ratio_L_h, 5.0, 10.0, 1.4, 1.7), 3),
            "Vùng D": 1.2,
        }
        interp_desc = f"5.0 < L/h = {ratio_L_h:.2f} < 10.0 (Nội suy tuyến tính giữa L/h=5 và L/h=10)"
    else:
        cx_straight_1_0 = {"Vùng A": 3.4, "Vùng B": 2.1, "Vùng C": 1.7, "Vùng D": 1.2}
        interp_desc = f"L/h = {ratio_L_h:.2f} >= 10.0 (Tra trực tiếp hàng L/h >= 10)"

    # Return corner wall at phi = 1.0 (l_ret >= h)
    cx_return_1_0 = {"Vùng A": 2.1, "Vùng B": 1.8, "Vùng C": 1.4, "Vùng D": 1.2}

    if is_return and l_ret >= height_h:
        cx_phi_1_0 = cx_return_1_0
        steps.append(
            CalculationStep(
                step_number=2,
                description="Tra hệ số cx cho tường có bẻ góc (l_ret >= h, φ = 1.0)",
                formula_latex=r"c_x(\text{bẻ góc})",
                substitution=rf"l_{{ret}} = {l_ret:g} m \ge h = {height_h:g} m",
                result_text="Vùng A=2.1, B=1.8, C=1.4, D=1.2",
            )
        )
    elif is_return and 0 < l_ret < height_h:
        # Chú thích 1: Nội suy giữa thẳng và bẻ góc hoàn toàn
        ratio_ret = l_ret / height_h
        cx_phi_1_0 = {
            z: round(_interp(ratio_ret, 0.0, 1.0, cx_straight_1_0[z], cx_return_1_0[z]), 3)
            for z in cx_straight_1_0
        }
        steps.append(
            CalculationStep(
                step_number=2,
                description="Nội suy hệ số cx theo chiều dài bẻ góc 0 < l_ret < h (Chú thích 1)",
                formula_latex=r"c_x = c_{x,\text{thẳng}} + \frac{l_{ret}}{h} (c_{x,\text{bẻ góc}} - c_{x,\text{thẳng}})",
                substitution=f"l_{{ret}}/h = {ratio_ret:.2f}",
                result_text=f"Vùng A={cx_phi_1_0['Vùng A']}, B={cx_phi_1_0['Vùng B']}, C={cx_phi_1_0['Vùng C']}, D={cx_phi_1_0['Vùng D']}",
            )
        )
    else:
        cx_phi_1_0 = cx_straight_1_0
        steps.append(
            CalculationStep(
                step_number=2,
                description=f"Tra và nội suy hệ số cx cho tường thẳng (φ = 1.0): {interp_desc}",
                formula_latex=r"c_x(\varphi=1.0)",
                substitution=f"L/h = {ratio_L_h:.2f}",
                result_text=f"Vùng A={cx_phi_1_0['Vùng A']}, B={cx_phi_1_0['Vùng B']}, C={cx_phi_1_0['Vùng C']}, D={cx_phi_1_0['Vùng D']}",
            )
        )

    # 2. Xử lý khi phi < 1.0 (Chú thích Bảng F.1)
    cx_phi_0_8 = {"Vùng A": 1.2, "Vùng B": 1.2, "Vùng C": 1.2, "Vùng D": 1.2}
    if phi == 1.0:
        final_cx = cx_phi_1_0
    elif phi == 0.8:
        final_cx = cx_phi_0_8
        steps.append(
            CalculationStep(
                step_number=3,
                description="Hệ số đặc φ = 0.8: Tra trực tiếp hàng φ = 0.8",
                formula_latex=r"c_x(\varphi=0.8) = 1.2",
                substitution="\varphi = 0.8",
                result_text="Vùng A=1.2, B=1.2, C=1.2, D=1.2",
            )
        )
    else:
        # Nội suy giữa phi = 0.8 và phi = 1.0
        final_cx = {
            z: round(_interp(phi, 0.8, 1.0, cx_phi_0_8[z], cx_phi_1_0[z]), 3)
            for z in cx_phi_1_0
        }
        steps.append(
            CalculationStep(
                step_number=3,
                description="Nội suy tuyến tính theo hệ số đặc 0.8 < φ < 1.0 (CHÚ THÍCH Bảng F.1)",
                formula_latex=r"c_x(\varphi) = c_x(0.8) + \frac{\varphi - 0.8}{1.0 - 0.8} [c_x(1.0) - c_x(0.8)]",
                substitution=rf"\varphi = {phi:g}",
                result_text=f"Vùng A={final_cx['Vùng A']}, B={final_cx['Vùng B']}, C={final_cx['Vùng C']}, D={final_cx['Vùng D']}",
            )
        )

    notes.append(f"Độ cao tương đương lấy bằng z_e = h = {height_h:g} m (theo F.1.1.2).")
    if ratio_L_h > 4.0:
        notes.append(f"Phân vùng Hình F.1 (L > 4h): Vùng A (0 đến {0.3*height_h:.2f}m), Vùng B ({0.3*height_h:.2f} đến {2.0*height_h:.2f}m), Vùng C ({2.0*height_h:.2f} đến {4.0*height_h:.2f}m), Vùng D ({4.0*height_h:.2f} đến {length_L:.2f}m).")
    elif ratio_L_h > 2.0:
        notes.append(f"Phân vùng Hình F.1 (2h < L <= 4h): Vùng A (0 đến {0.3*height_h:.2f}m), Vùng B ({0.3*height_h:.2f} đến {2.0*height_h:.2f}m), Vùng C ({2.0*height_h:.2f} đến {length_L:.2f}m).")
    else:
        notes.append(f"Phân vùng Hình F.1 (L <= 2h): Vùng A (0 đến {0.3*height_h:.2f}m), Vùng B ({0.3*height_h:.2f} đến {length_L:.2f}m).")

    return CalculationResult(
        formula_id="F_WIND_TCVN2737_F1_WALL",
        formula_name="Hệ số khí động c_x cho tường phẳng độc lập và hàng rào",
        standard_reference="Mục F.1.1, Hình F.1 & Bảng F.1 Phụ lục F TCVN 2737:2023",
        inputs={
            "length_L_m": length_L,
            "height_h_m": height_h,
            "solidity_ratio_phi": phi,
            "has_return_corner": is_return,
            "return_corner_length_m": l_ret,
        },
        outputs={f"cx_{z}": val for z, val in final_cx.items()},
        unit="",
        primary_value=final_cx["Vùng A"],
        zone_values=final_cx,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message="Hệ số khí động c_x đã được tra cứu và nội suy chính xác 100% theo Bảng F.1 TCVN 2737:2023.",
    )


# ===========================================================================
# 2. BẢNG F.5a, F.5b & HÌNH F.6: MÁI DỐC HAI PHÍA CỦA NHÀ MẶT BẰNG CHỮ NHẬT
# ===========================================================================

# Bảng F.5a: theta = 0 độ
# Format: alpha: (F_neg, F_pos, G_neg, G_pos, H_neg, H_pos, I_neg, I_pos, J_neg, J_pos)
_RAW_F5A: dict[float, tuple[float | None, ...]] = {
    -45.0: (-0.6, None, -0.6, None, -0.8, None, -0.7, None, -1.0, None),
    -30.0: (-1.1, None, -2.0, None, -0.8, None, -0.6, None, -0.8, None),
    -15.0: (-2.5, None, -1.3, None, -0.9, None, -0.5, None, -0.7, None),
    -5.0:  (-2.3, None, -1.2, None, -0.8, None, -0.6, 0.2,  -0.6, 0.2),
    5.0:   (-1.7, 0.0,  -1.2, 0.0,  -0.6, 0.0,  -0.6, None, -0.6, 0.2),
    15.0:  (-0.9, 0.2,  -0.8, 0.2,  -0.3, 0.2,  -0.4, None, -1.0, None),
    30.0:  (-0.5, 0.7,  -0.5, 0.7,  -0.2, 0.4,  -0.4, None, -0.5, None),
    45.0:  (-0.0, 0.7,  -0.0, 0.7,  -0.0, 0.6,  -0.2, 0.0,  -0.3, 0.0),
    60.0:  (None, 0.7,  None, 0.7,  None, 0.7,  -0.2, None, -0.3, None),
    75.0:  (None, 0.8,  None, 0.8,  None, 0.8,  -0.2, None, -0.3, None),
}

# Bảng F.5b: theta = 90 độ
# Format: alpha: (F, G, H, I)
_RAW_F5B: dict[float, tuple[float, float, float, float]] = {
    -45.0: (-1.4, -1.2, -1.0, -0.9),
    -30.0: (-1.5, -1.2, -1.0, -0.9),
    -15.0: (-1.9, -1.2, -0.8, -0.8),
    -5.0:  (-1.8, -1.2, -0.7, -0.6),
    5.0:   (-1.6, -1.3, -0.7, -0.6),
    15.0:  (-1.3, -1.3, -0.6, -0.5),
    30.0:  (-1.1, -1.4, -0.8, -0.5),
    45.0:  (-1.1, -1.4, -0.9, -0.5),
    60.0:  (-1.1, -1.2, -0.8, -0.5),
    75.0:  (-1.1, -1.2, -0.8, -0.5),
}


def calc_duopitch_roof_ce_coefficients(
    pitch_angle_alpha: float,
    wind_angle_theta: float = 0.0,
    building_width_b: float = 0.0,
    building_height_h: float = 0.0,
    building_depth_d: float = 0.0,
) -> CalculationResult:
    """Tính toán hệ số khí động áp lực ngoài c_e cho mái dốc 2 phía (Bảng F.5a, F.5b / Hình F.6).

    Căn cứ: Mục F.4.2, Hình F.6, Bảng F.5a và Bảng F.5b Phụ lục F TCVN 2737:2023.

    Args:
        pitch_angle_alpha: Góc dốc mái alpha (-45 <= alpha <= 75 độ).
        wind_angle_theta: Góc hướng gió theta (0 hoặc 90 độ, mặc định 0).
        building_width_b: Chiều rộng mặt đón gió b (m, tùy chọn).
        building_height_h: Chiều cao đỉnh mái h (m, tùy chọn).
        building_depth_d: Chiều sâu dọc gió d (m, tùy chọn).
    """
    alpha = float(pitch_angle_alpha)
    if alpha < -45.0 or alpha > 75.0:
        raise ValueError(f"Góc dốc mái alpha = {alpha:g}° nằm ngoài phạm vi Bảng F.5 (-45° đến +75°)")

    theta = 90.0 if abs(wind_angle_theta - 90.0) < 45.0 else 0.0
    steps: list[CalculationStep] = []
    notes: list[str] = []

    steps.append(
        CalculationStep(
            step_number=1,
            description="Xác định góc dốc mái α và góc hướng gió θ",
            formula_latex=r"\alpha = \dots^\circ,\; \theta = \dots^\circ",
            substitution=rf"\alpha = {alpha:g}^\circ, \theta = {theta:g}^\circ",
            result_text=f"α = {alpha:g}°, θ = {theta:g}°",
        )
    )

    if building_width_b > 0 and building_height_h > 0:
        e_dim = min(building_width_b, 2.0 * building_height_h)
        notes.append(f"Kích thước e = min(b, 2h) = min({building_width_b:g}, {2.0*building_height_h:g}) = {e_dim:g} m.")
        notes.append(f"Kích thước phân vùng: e/10 = {e_dim/10.0:.2f} m, e/4 = {e_dim/4.0:.2f} m, e/2 = {e_dim/2.0:.2f} m.")

    # -----------------------------------------------------------------------
    # Hướng gió theta = 90 độ (Bảng F.5b)
    # -----------------------------------------------------------------------
    if theta == 90.0:
        angles = sorted(_RAW_F5B.keys())
        if alpha in _RAW_F5B:
            f, g, h, i = _RAW_F5B[alpha]
            steps.append(
                CalculationStep(
                    step_number=2,
                    description=f"Tra trực tiếp Bảng F.5b cho hướng gió θ = 90° tại α = {alpha:g}°",
                    formula_latex=r"c_e(\theta=90^\circ, \alpha)",
                    substitution=rf"\alpha = {alpha:g}^\circ",
                    result_text=f"Vùng F={f:g}, G={g:g}, H={h:g}, I={i:g}",
                )
            )
        else:
            # Tìm khoảng nội suy cùng dấu
            # Lưu ý Chú thích 2: không nội suy giữa -5 và +5
            if -5.0 < alpha < 5.0:
                raise ValueError("Không nội suy tuyến tính giữa alpha = -5° và +5° (Chú thích 2: dùng số liệu mái bằng trong F.2)")
            
            # Tìm idx
            idx = 0
            for k in range(len(angles) - 1):
                if angles[k] <= alpha <= angles[k+1]:
                    idx = k
                    break
            a0, a1 = angles[idx], angles[idx+1]
            f0, g0, h0, i0 = _RAW_F5B[a0]
            f1, g1, h1, i1 = _RAW_F5B[a1]
            f = round(_interp(alpha, a0, a1, f0, f1), 3)
            g = round(_interp(alpha, a0, a1, g0, g1), 3)
            h = round(_interp(alpha, a0, a1, h0, h1), 3)
            i = round(_interp(alpha, a0, a1, i0, i1), 3)
            steps.append(
                CalculationStep(
                    step_number=2,
                    description=f"Nội suy tuyến tính Bảng F.5b giữa α = {a0:g}° và α = {a1:g}°",
                    formula_latex=r"c_e = c_{e,0} + \frac{\alpha - \alpha_0}{\alpha_1 - \alpha_0} (c_{e,1} - c_{e,0})",
                    substitution=rf"\alpha = {alpha:g}^\circ \in [{a0:g}^\circ, {a1:g}^\circ]",
                    result_text=f"Vùng F={f:g}, G={g:g}, H={h:g}, I={i:g}",
                )
            )

        res_zones = {"Vùng F": f, "Vùng G": g, "Vùng H": h, "Vùng I": i}
        return CalculationResult(
            formula_id="F_WIND_TCVN2737_F6_DUOPITCH",
            formula_name="Hệ số khí động c_e cho mái dốc hai phía (θ = 90°)",
            standard_reference="Mục F.4.2, Hình F.6 & Bảng F.5b Phụ lục F TCVN 2737:2023",
            inputs={"pitch_angle_alpha": alpha, "wind_angle_theta": 90.0},
            outputs={f"ce_{z}": val for z, val in res_zones.items()},
            unit="",
            primary_value=f,
            zone_values=res_zones,
            steps=steps,
            notes=notes,
            is_compliant=True,
            compliance_message="Hệ số khí động c_e (θ = 90°) đã được tính toán chính xác theo Bảng F.5b.",
        )

    # -----------------------------------------------------------------------
    # Hướng gió theta = 0 độ (Bảng F.5a)
    # -----------------------------------------------------------------------
    angles = sorted(_RAW_F5A.keys())
    if -5.0 < alpha < 5.0:
        raise ValueError("Không nội suy tuyến tính giữa alpha = -5° và +5° (Chú thích 2: dùng số liệu mái bằng trong F.2)")

    # Tìm khoảng góc
    if alpha in _RAW_F5A:
        row = _RAW_F5A[alpha]
        f_neg, f_pos, g_neg, g_pos, h_neg, h_pos, i_neg, i_pos, j_neg, j_pos = row
        steps.append(
            CalculationStep(
                step_number=2,
                description=f"Tra trực tiếp Bảng F.5a cho hướng gió θ = 0° tại α = {alpha:g}°",
                formula_latex=r"c_e(\theta=0^\circ, \alpha)",
                substitution=rf"\alpha = {alpha:g}^\circ",
                result_text="Đã lấy giá trị trực tiếp từ Bảng F.5a",
            )
        )
    else:
        idx = 0
        for k in range(len(angles) - 1):
            if angles[k] <= alpha <= angles[k+1]:
                idx = k
                break
        a0, a1 = angles[idx], angles[idx+1]
        r0, r1 = _RAW_F5A[a0], _RAW_F5A[a1]

        def _interp_val(v0: float | None, v1: float | None) -> float | None:
            if v0 is not None and v1 is not None:
                return round(_interp(alpha, a0, a1, v0, v1), 3)
            return v0 if v0 is not None else v1

        f_neg = _interp_val(r0[0], r1[0])
        f_pos = _interp_val(r0[1], r1[1])
        g_neg = _interp_val(r0[2], r1[2])
        g_pos = _interp_val(r0[3], r1[3])
        h_neg = _interp_val(r0[4], r1[4])
        h_pos = _interp_val(r0[5], r1[5])
        i_neg = _interp_val(r0[6], r1[6])
        i_pos = _interp_val(r0[7], r1[7])
        j_neg = _interp_val(r0[8], r1[8])
        j_pos = _interp_val(r0[9], r1[9])

        steps.append(
            CalculationStep(
                step_number=2,
                description=f"Nội suy tuyến tính Bảng F.5a cho các giá trị cùng dấu giữa α = {a0:g}° và α = {a1:g}° (CHÚ THÍCH 2)",
                formula_latex=r"c_e = c_{e,0} + \frac{\alpha - \alpha_0}{\alpha_1 - \alpha_0} (c_{e,1} - c_{e,0})",
                substitution=rf"\alpha = {alpha:g}^\circ \in [{a0:g}^\circ, {a1:g}^\circ]",
                result_text="Nội suy thành công",
            )
        )

    # Kiểm tra xem có dual scenario không (khi -5 <= alpha <= 45 hoặc có cả neg/pos)
    has_dual = any(v is not None for v in [f_pos, g_pos, h_pos]) and any(v is not None for v in [f_neg, g_neg, h_neg])
    scenarios: dict[str, dict[str, float]] = {}

    if has_dual:
        # Case 1: Toàn bộ âm (Hút)
        case_suction: dict[str, float] = {}
        case_suction["Vùng F"] = f_neg if f_neg is not None else f_pos
        case_suction["Vùng G"] = g_neg if g_neg is not None else g_pos
        case_suction["Vùng H"] = h_neg if h_neg is not None else h_pos
        case_suction["Vùng I"] = i_neg if i_neg is not None else (i_pos if i_pos is not None else 0.0)
        case_suction["Vùng J"] = j_neg if j_neg is not None else (j_pos if j_pos is not None else 0.0)
        scenarios["Trường hợp 1 (Áp lực âm / Hút)"] = case_suction

        # Case 2: Toàn bộ dương (Đẩy)
        case_pressure: dict[str, float] = {}
        case_pressure["Vùng F"] = f_pos if f_pos is not None else f_neg
        case_pressure["Vùng G"] = g_pos if g_pos is not None else g_neg
        case_pressure["Vùng H"] = h_pos if h_pos is not None else h_neg
        case_pressure["Vùng I"] = i_pos if i_pos is not None else i_neg
        case_pressure["Vùng J"] = j_pos if j_pos is not None else j_neg
        scenarios["Trường hợp 2 (Áp lực dương / Đẩy)"] = case_pressure

        notes.append("CHÚ THÍCH 1 Bảng F.5a: Áp lực thay đổi nhanh giữa âm và dương. Cần xét 2 trường hợp tải trọng riêng biệt: một là tất cả giá trị dương, hai là tất cả giá trị âm. Không được xét đồng thời âm và dương trên cùng một mặt.")
        primary = case_suction["Vùng F"]
        zone_vals = case_suction
    else:
        # Single scenario
        single_case: dict[str, float] = {
            "Vùng F": f_neg if f_neg is not None else f_pos,
            "Vùng G": g_neg if g_neg is not None else g_pos,
            "Vùng H": h_neg if h_neg is not None else h_pos,
            "Vùng I": i_neg if i_neg is not None else (i_pos if i_pos is not None else 0.0),
            "Vùng J": j_neg if j_neg is not None else (j_pos if j_pos is not None else 0.0),
        }
        primary = single_case["Vùng F"]
        zone_vals = single_case

    return CalculationResult(
        formula_id="F_WIND_TCVN2737_F6_DUOPITCH",
        formula_name="Hệ số khí động c_e cho mái dốc hai phía (θ = 0°)",
        standard_reference="Mục F.4.2, Hình F.6 & Bảng F.5a Phụ lục F TCVN 2737:2023",
        inputs={"pitch_angle_alpha": alpha, "wind_angle_theta": 0.0},
        outputs=scenarios if scenarios else {f"ce_{z}": val for z, val in zone_vals.items()},
        unit="",
        primary_value=primary,
        zone_values=zone_vals if not scenarios else {},
        scenarios=scenarios,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message="Hệ số khí động c_e (θ = 0°) đã được tính toán và phân tách kịch bản chính xác 100% theo Bảng F.5a.",
    )


# ===========================================================================
# 3. BẢNG F.2 & HÌNH F.3: MÁI BẰNG (FLAT ROOFS)
# ===========================================================================

def calc_flat_roof_ce_coefficients(
    eaves_type: str = "CANH_SAC",
    parapet_height_hp: float = 0.0,
    radius_r: float = 0.0,
    building_height_h: float = 0.0,
    building_width_b: float = 0.0,
) -> CalculationResult:
    """Tính toán hệ số khí động áp lực ngoài c_e cho mái bằng (Bảng F.2 / Hình F.3).

    Căn cứ: Mục F.2, Hình F.3 và Bảng F.2 Phụ lục F TCVN 2737:2023.

    Args:
        eaves_type: Loại mép mái ('CANH_SAC', 'TUONG_CHAN_MAI', 'BO_TRON', 'VAT_GOC').
        parapet_height_hp: Chiều cao tường chắn mái hp (m, mặc định 0.0).
        radius_r: Bán kính bo tròn mép mái r (m, mặc định 0.0).
        building_height_h: Chiều cao công trình h (m).
        building_width_b: Chiều rộng đón gió b (m).
    """
    etype = eaves_type.upper().strip()
    h = max(0.1, building_height_h)
    steps: list[CalculationStep] = []
    notes: list[str] = []

    if building_width_b > 0 and building_height_h > 0:
        e_dim = min(building_width_b, 2.0 * building_height_h)
        notes.append(f"Kích thước e = min(b, 2h) = min({building_width_b:g}, {2.0*h:g}) = {e_dim:g} m.")
        notes.append(f"Phân vùng Hình F.3: Vùng F ({e_dim/4.0:.2f} x {e_dim/10.0:.2f} m), Vùng G ({e_dim/10.0:.2f} m dọc mép đón gió), Vùng H ({e_dim/2.0:.2f} m dọc sườn), Vùng I (diện tích còn lại).")

    # Mặc định Cạnh sắc
    f, g, h_val, i_val = -1.8, -1.2, -0.7, 0.2
    desc = "Mái bằng có cạnh sắc"

    if etype in ("TUONG_CHAN_MAI", "PARAPET") and parapet_height_hp > 0:
        ratio = parapet_height_hp / h
        desc = f"Mái bằng có tường chắn mái (hp/h = {ratio:.3f})"
        if ratio <= 0.025:
            f, g = -1.6, -1.1
        elif ratio <= 0.05:
            f = round(_interp(ratio, 0.025, 0.05, -1.6, -1.4), 3)
            g = round(_interp(ratio, 0.025, 0.05, -1.1, -0.9), 3)
        elif ratio < 0.10:
            f = round(_interp(ratio, 0.05, 0.10, -1.4, -1.2), 3)
            g = round(_interp(ratio, 0.05, 0.10, -0.9, -0.8), 3)
        else:
            f, g = -1.2, -0.8
        notes.append(f"Hệ số khí động áp lực cho tường chắn mái được tính theo F.1.1 (Chú thích Bảng F.2).")
    elif etype in ("BO_TRON", "ROUNDED") and radius_r > 0:
        ratio = radius_r / h
        desc = f"Mái bằng có cạnh bo tròn (r/h = {ratio:.3f})"
        if ratio <= 0.05:
            f, g, h_val = -1.0, -0.7, -0.7
        elif ratio <= 0.10:
            f = round(_interp(ratio, 0.05, 0.10, -1.0, -0.7), 3)
            g, h_val = -0.7, -0.7
        elif ratio < 0.20:
            f = round(_interp(ratio, 0.10, 0.20, -0.7, -0.5), 3)
            g = round(_interp(ratio, 0.10, 0.20, -0.7, -0.5), 3)
            h_val = round(_interp(ratio, 0.10, 0.20, -0.7, -0.5), 3)
        else:
            f, g, h_val = -0.5, -0.5, -0.5

    steps.append(
        CalculationStep(
            step_number=1,
            description=f"Tra cứu và nội suy hệ số c_e Bảng F.2 cho {desc}",
            formula_latex=r"c_e(	ext{mái bằng})",
            substitution=f"Loại mép: {etype}",
            result_text=f"Vùng F={f:g}, G={g:g}, H={h_val:g}, I=±{i_val:g}",
        )
    )

    # Vùng I có cả giá trị dương và âm (CHÚ THÍCH 3)
    scenarios = {
        "Trường hợp 1 (Áp lực âm / Hút)": {"Vùng F": f, "Vùng G": g, "Vùng H": h_val, "Vùng I": -0.2},
        "Trường hợp 2 (Áp lực dương / Đẩy)": {"Vùng F": f, "Vùng G": g, "Vùng H": h_val, "Vùng I": 0.2},
    }
    notes.append("CHÚ THÍCH 3 Bảng F.2: Trong vùng I, nơi có các giá trị dương và âm (±0.2), cần xét cả hai giá trị này.")

    return CalculationResult(
        formula_id="F_WIND_TCVN2737_F3_FLAT",
        formula_name="Hệ số khí động c_e cho mái bằng",
        standard_reference="Mục F.2, Hình F.3 & Bảng F.2 Phụ lục F TCVN 2737:2023",
        inputs={
            "eaves_type": etype,
            "parapet_height_hp_m": parapet_height_hp,
            "radius_r_m": radius_r,
            "building_height_h_m": building_height_h,
            "building_width_b_m": building_width_b,
        },
        outputs=scenarios,
        unit="",
        primary_value=f,
        scenarios=scenarios,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message="Hệ số khí động c_e cho mái bằng đã được tính toán chính xác theo Bảng F.2.",
    )


# ===========================================================================
# 4. BẢNG F.4 & HÌNH F.5a: TƯỜNG THẲNG ĐỨNG CỦA NHÀ MẶT BẰNG CHỮ NHẬT
# ===========================================================================

def calc_vertical_wall_ce_coefficients(
    building_height_h: float,
    building_depth_d: float,
    building_width_b: float = 0.0,
) -> CalculationResult:
    """Tính toán hệ số khí động c_e cho các tường thẳng đứng của nhà chữ nhật (Bảng F.4 / Hình F.5a).

    Căn cứ: Mục F.4.1, Hình F.5a và Bảng F.4 Phụ lục F TCVN 2737:2023.

    Args:
        building_height_h: Chiều cao công trình h (m).
        building_depth_d: Chiều sâu dọc hướng gió d (m).
        building_width_b: Chiều rộng mặt đón gió b (m, tùy chọn).
    """
    if building_height_h <= 0 or building_depth_d <= 0:
        raise ValueError("Chiều cao h và chiều sâu d phải > 0")

    ratio_h_d = building_height_h / building_depth_d
    steps: list[CalculationStep] = []
    notes: list[str] = []

    steps.append(
        CalculationStep(
            step_number=1,
            description="Xác định tỷ lệ kích thước h/d",
            formula_latex=r"rac{h}{d}",
            substitution=rf"rac{{{building_height_h:g}}}{{{building_depth_d:g}}} = {ratio_h_d:.2f}",
            result_text=f"h/d = {ratio_h_d:.2f}",
        )
    )

    # Tra Bảng F.4
    # h/d >= 5: A=-1.2, B=-0.8, C=-0.5, D=+0.8, E=-0.7
    # h/d = 1:  A=-1.2, B=-0.8, C=-0.5, D=+0.8, E=-0.5
    # h/d <= 0.25: A=-1.2, B=-0.8, C=-0.5, D=+0.7, E=-0.3
    if ratio_h_d >= 5.0:
        a, b_val, c_val, d_val, e_val = -1.2, -0.8, -0.5, 0.8, -0.7
        desc = "h/d >= 5.0 (Tra trực tiếp hàng h/d = 5)"
    elif ratio_h_d >= 1.0:
        a, b_val, c_val = -1.2, -0.8, -0.5
        d_val = 0.8
        e_val = round(_interp(ratio_h_d, 1.0, 5.0, -0.5, -0.7), 3)
        desc = "1.0 <= h/d < 5.0 (Nội suy tuyến tính vùng E giữa h/d=1 và h/d=5)"
    elif ratio_h_d > 0.25:
        a, b_val, c_val = -1.2, -0.8, -0.5
        d_val = round(_interp(ratio_h_d, 0.25, 1.0, 0.7, 0.8), 3)
        e_val = round(_interp(ratio_h_d, 0.25, 1.0, -0.3, -0.5), 3)
        desc = "0.25 < h/d < 1.0 (Nội suy tuyến tính vùng D và E giữa h/d=0.25 và h/d=1)"
    else:
        a, b_val, c_val, d_val, e_val = -1.2, -0.8, -0.5, 0.7, -0.3
        desc = "h/d <= 0.25 (Tra trực tiếp hàng h/d <= 0.25)"

    steps.append(
        CalculationStep(
            step_number=2,
            description=f"Tra và nội suy hệ số c_e Bảng F.4 ({desc})",
            formula_latex=r"c_e(	ext{tường đứng})",
            substitution=f"h/d = {ratio_h_d:.2f}",
            result_text=f"Vùng A={a:g}, B={b_val:g}, C={c_val:g}, D={d_val:g}, E={e_val:g}",
        )
    )

    if building_width_b > 0:
        e_dim = min(building_width_b, 2.0 * building_height_h)
        notes.append(f"Kích thước e = min(b, 2h) = min({building_width_b:g}, {2.0*building_height_h:g}) = {e_dim:g} m.")
        notes.append(f"Phân vùng tường bên Hình F.5a: Vùng A (chiều rộng e/5 = {e_dim/5.0:.2f} m), Vùng B (chiều rộng 4e/5 = {4.0*e_dim/5.0:.2f} m), Vùng C (chiều rộng d - e = {building_depth_d - e_dim:.2f} m khi d > e).")

    zones = {
        "Vùng A (Tường bên mép đón)": a,
        "Vùng B (Tường bên dải giữa)": b_val,
        "Vùng C (Tường bên dải cuối)": c_val,
        "Vùng D (Tường đón gió)": d_val,
        "Vùng E (Tường hút gió)": e_val,
    }

    return CalculationResult(
        formula_id="F_WIND_TCVN2737_F5A_WALLS",
        formula_name="Hệ số khí động c_e cho tường thẳng đứng của nhà chữ nhật",
        standard_reference="Mục F.4.1, Hình F.5a & Bảng F.4 Phụ lục F TCVN 2737:2023",
        inputs={"building_height_h_m": building_height_h, "building_depth_d_m": building_depth_d, "building_width_b_m": building_width_b},
        outputs={f"ce_{z}": val for z, val in zones.items()},
        unit="",
        primary_value=d_val,
        zone_values=zones,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message="Hệ số khí động c_e cho tường đứng đã được tính toán chính xác theo Bảng F.4.",
    )


# ===========================================================================
# 5. BẢNG F.3a, F.3b & HÌNH F.4: MÁI DỐC MỘT PHÍA (MONOPITCH ROOFS)
# ===========================================================================

# Bảng F.3a: theta = 0 và 180 độ
# Format: alpha: (F_0_neg, F_0_pos, G_0_neg, G_0_pos, H_0_neg, H_0_pos, F_180, G_180, H_180)
_RAW_F3A: dict[float, tuple[float | None, ...]] = {
    5.0:  (-1.7, 0.0, -1.2, 0.0, -0.6, 0.0, -2.3, -1.3, -0.8),
    15.0: (-0.9, 0.2, -0.8, 0.2, -0.3, 0.2, -2.5, -1.3, -0.9),
    30.0: (-0.5, 0.7, -0.5, 0.7, -0.2, 0.4, -1.1, -0.8, -0.8),
    45.0: (-0.0, 0.7, -0.0, 0.7, -0.0, 0.6, -0.6, -0.5, -0.7),
    60.0: (None, 0.7, None, 0.7, None, 0.7, -0.5, -0.5, -0.5),
    75.0: (None, 0.8, None, 0.8, None, 0.8, -0.5, -0.5, -0.5),
}

# Bảng F.3b: theta = 90 độ
# Format: alpha: (F_up, F_low, G, H, I)
_RAW_F3B: dict[float, tuple[float, float, float, float, float]] = {
    5.0:  (-2.1, -2.1, -1.8, -0.6, -0.5),
    15.0: (-2.4, -1.6, -1.9, -0.8, -0.7),
    30.0: (-2.1, -1.3, -1.5, -1.0, -0.8),
    45.0: (-1.5, -1.3, -1.4, -1.0, -0.9),
    60.0: (-1.2, -1.2, -1.2, -1.0, -0.7),
    75.0: (-1.2, -1.2, -1.2, -1.0, -0.5),
}


def calc_monopitch_roof_ce_coefficients(
    pitch_angle_alpha: float,
    wind_angle_theta: float = 0.0,
    building_width_b: float = 0.0,
    building_height_h: float = 0.0,
    building_depth_d: float = 0.0,
) -> CalculationResult:
    """Tính toán hệ số khí động áp lực ngoài c_e cho mái dốc một phía (Bảng F.3a, F.3b / Hình F.4).

    Căn cứ: Mục F.3, Hình F.4, Bảng F.3a và Bảng F.3b Phụ lục F TCVN 2737:2023.

    Args:
        pitch_angle_alpha: Góc dốc mái alpha (5 <= alpha <= 75 độ).
        wind_angle_theta: Góc hướng gió theta (0, 90 hoặc 180 độ, mặc định 0).
        building_width_b: Chiều rộng đón gió b (m, tùy chọn).
        building_height_h: Chiều cao đỉnh mái h (m, tùy chọn).
        building_depth_d: Chiều sâu dọc gió d (m, tùy chọn).
    """
    alpha = float(pitch_angle_alpha)
    if alpha < 5.0 or alpha > 75.0:
        raise ValueError(f"Góc dốc mái alpha = {alpha:g}° nằm ngoài phạm vi Bảng F.3 (5° đến 75°)")

    theta = 90.0 if abs(wind_angle_theta - 90.0) < 45.0 else (180.0 if wind_angle_theta >= 135.0 else 0.0)
    steps: list[CalculationStep] = []
    notes: list[str] = []

    steps.append(
        CalculationStep(
            step_number=1,
            description="Xác định góc dốc mái α và hướng gió θ",
            formula_latex=r"lpha = \dots^\circ,\; 	heta = \dots^\circ",
            substitution=rf"lpha = {alpha:g}^\circ, 	heta = {theta:g}^\circ",
            result_text=f"α = {alpha:g}°, θ = {theta:g}°",
        )
    )

    if building_width_b > 0 and building_height_h > 0:
        e_dim = min(building_width_b, 2.0 * building_height_h)
        notes.append(f"Kích thước e = min(b, 2h) = {e_dim:g} m.")

    # theta = 90 deg (Bảng F.3b)
    if theta == 90.0:
        angles = sorted(_RAW_F3B.keys())
        if alpha in _RAW_F3B:
            f_up, f_low, g, h_val, i_val = _RAW_F3B[alpha]
        else:
            idx = 0
            for k in range(len(angles) - 1):
                if angles[k] <= alpha <= angles[k+1]:
                    idx = k
                    break
            a0, a1 = angles[idx], angles[idx+1]
            r0, r1 = _RAW_F3B[a0], _RAW_F3B[a1]
            f_up = round(_interp(alpha, a0, a1, r0[0], r1[0]), 3)
            f_low = round(_interp(alpha, a0, a1, r0[1], r1[1]), 3)
            g = round(_interp(alpha, a0, a1, r0[2], r1[2]), 3)
            h_val = round(_interp(alpha, a0, a1, r0[3], r1[3]), 3)
            i_val = round(_interp(alpha, a0, a1, r0[4], r1[4]), 3)

        zones = {"Vùng F_up": f_up, "Vùng F_low": f_low, "Vùng G": g, "Vùng H": h_val, "Vùng I": i_val}
        return CalculationResult(
            formula_id="F_WIND_TCVN2737_F4_MONOPITCH",
            formula_name="Hệ số khí động c_e cho mái dốc 1 phía (θ = 90°)",
            standard_reference="Mục F.3, Hình F.4 & Bảng F.3b TCVN 2737:2023",
            inputs={"pitch_angle_alpha": alpha, "wind_angle_theta": 90.0},
            outputs={f"ce_{z}": val for z, val in zones.items()},
            unit="",
            primary_value=f_up,
            zone_values=zones,
            steps=steps,
            notes=notes,
            is_compliant=True,
            compliance_message="Hệ số c_e (θ = 90°) đã được tính toán chính xác theo Bảng F.3b.",
        )

    # theta = 180 deg
    if theta == 180.0:
        angles = sorted(_RAW_F3A.keys())
        if alpha in _RAW_F3A:
            r = _RAW_F3A[alpha]
            f_180, g_180, h_180 = r[6], r[7], r[8]
        else:
            idx = 0
            for k in range(len(angles) - 1):
                if angles[k] <= alpha <= angles[k+1]:
                    idx = k
                    break
            a0, a1 = angles[idx], angles[idx+1]
            r0, r1 = _RAW_F3A[a0], _RAW_F3A[a1]
            f_180 = round(_interp(alpha, a0, a1, r0[6], r1[6]), 3)
            g_180 = round(_interp(alpha, a0, a1, r0[7], r1[7]), 3)
            h_180 = round(_interp(alpha, a0, a1, r0[8], r1[8]), 3)

        zones = {"Vùng F": f_180, "Vùng G": g_180, "Vùng H": h_180}
        return CalculationResult(
            formula_id="F_WIND_TCVN2737_F4_MONOPITCH",
            formula_name="Hệ số khí động c_e cho mái dốc 1 phía (θ = 180°)",
            standard_reference="Mục F.3, Hình F.4 & Bảng F.3a TCVN 2737:2023",
            inputs={"pitch_angle_alpha": alpha, "wind_angle_theta": 180.0},
            outputs={f"ce_{z}": val for z, val in zones.items()},
            unit="",
            primary_value=f_180,
            zone_values=zones,
            steps=steps,
            notes=notes,
            is_compliant=True,
            compliance_message="Hệ số c_e (θ = 180°) đã được tính toán chính xác theo Bảng F.3a.",
        )

    # theta = 0 deg (có dual values)
    angles = sorted(_RAW_F3A.keys())
    if alpha in _RAW_F3A:
        r = _RAW_F3A[alpha]
        f_neg, f_pos, g_neg, g_pos, h_neg, h_pos = r[0], r[1], r[2], r[3], r[4], r[5]
    else:
        idx = 0
        for k in range(len(angles) - 1):
            if angles[k] <= alpha <= angles[k+1]:
                idx = k
                break
        a0, a1 = angles[idx], angles[idx+1]
        r0, r1 = _RAW_F3A[a0], _RAW_F3A[a1]

        def _interp_val(v0: float | None, v1: float | None) -> float | None:
            if v0 is not None and v1 is not None:
                return round(_interp(alpha, a0, a1, v0, v1), 3)
            return v0 if v0 is not None else v1

        f_neg = _interp_val(r0[0], r1[0])
        f_pos = _interp_val(r0[1], r1[1])
        g_neg = _interp_val(r0[2], r1[2])
        g_pos = _interp_val(r0[3], r1[3])
        h_neg = _interp_val(r0[4], r1[4])
        h_pos = _interp_val(r0[5], r1[5])

    scenarios = {}
    if f_pos is not None and f_neg is not None:
        scenarios["Trường hợp 1 (Áp lực âm / Hút)"] = {"Vùng F": f_neg, "Vùng G": g_neg, "Vùng H": h_neg}
        scenarios["Trường hợp 2 (Áp lực dương / Đẩy)"] = {"Vùng F": f_pos, "Vùng G": g_pos, "Vùng H": h_pos}
        notes.append("CHÚ THÍCH 1 Bảng F.3a: Bắt buộc xét 2 trường hợp tải trọng riêng biệt (Toàn bộ âm hoặc Toàn bộ dương).")
        primary = f_neg
        zone_vals = {}
    else:
        primary = f_pos if f_pos is not None else f_neg
        zone_vals = {"Vùng F": primary, "Vùng G": g_pos if g_pos is not None else g_neg, "Vùng H": h_pos if h_pos is not None else h_neg}

    return CalculationResult(
        formula_id="F_WIND_TCVN2737_F4_MONOPITCH",
        formula_name="Hệ số khí động c_e cho mái dốc 1 phía (θ = 0°)",
        standard_reference="Mục F.3, Hình F.4 & Bảng F.3a TCVN 2737:2023",
        inputs={"pitch_angle_alpha": alpha, "wind_angle_theta": 0.0},
        outputs=scenarios if scenarios else {f"ce_{z}": val for z, val in zone_vals.items()},
        unit="",
        primary_value=primary,
        zone_values=zone_vals,
        scenarios=scenarios,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message="Hệ số c_e (θ = 0°) đã được tính toán chính xác theo Bảng F.3a.",
    )


# ===========================================================================
# 6. BẢNG F.6 & HÌNH F.7: MÁI DỐC BỐN PHÍA (HIPPED ROOFS)
# ===========================================================================

# Bảng F.6:
# Format: alpha: (F_neg, F_pos, G_neg, G_pos, H_neg, H_pos, I, J, K, L, M, N)
_RAW_F6: dict[float, tuple[float | None, ...]] = {
    5.0:  (-1.7, 0.0, -1.2, 0.0, -0.6, 0.0, -0.3, -0.6, -0.6, -1.2, -0.4, -0.4),
    15.0: (-0.9, 0.2, -0.8, 0.2, -0.3, 0.2, -0.5, -1.0, -1.2, -1.4, -0.6, -0.3),
    30.0: (-0.5, 0.7, -0.5, 0.7, -0.2, 0.4, -0.4, -0.5, -0.5, -0.8, -0.8, -0.2),
    45.0: (-0.0, 0.7, -0.0, 0.7, -0.0, 0.6, -0.3, -0.4, -0.7, -0.8, -0.8, -0.2),
    60.0: (None, 0.7, None, 0.7, None, 0.7, -0.3, -0.4, -0.7, -0.8, -0.8, -0.2),
    75.0: (None, 0.8, None, 0.8, None, 0.8, -0.3, -0.4, -0.7, -0.8, -0.8, -0.2),
}


def calc_hipped_roof_ce_coefficients(
    pitch_angle_alpha: float,
    wind_angle_theta: float = 0.0,
    building_width_b: float = 0.0,
    building_height_h: float = 0.0,
    building_depth_d: float = 0.0,
) -> CalculationResult:
    """Tính toán hệ số khí động áp lực ngoài c_e cho mái dốc bốn phía (Bảng F.6 / Hình F.7).

    Căn cứ: Mục F.5, Hình F.7 và Bảng F.6 Phụ lục F TCVN 2737:2023.

    Args:
        pitch_angle_alpha: Góc dốc mái alpha (5 <= alpha <= 75 độ).
        wind_angle_theta: Góc hướng gió theta (0 hoặc 90 độ, mặc định 0).
        building_width_b: Chiều rộng đón gió b (m, tùy chọn).
        building_height_h: Chiều cao đỉnh mái h (m, tùy chọn).
        building_depth_d: Chiều sâu dọc gió d (m, tùy chọn).
    """
    alpha = float(pitch_angle_alpha)
    if alpha < 5.0 or alpha > 75.0:
        raise ValueError(f"Góc dốc mái alpha = {alpha:g}° nằm ngoài phạm vi Bảng F.6 (5° đến 75°)")

    theta = 90.0 if abs(wind_angle_theta - 90.0) < 45.0 else 0.0
    steps: list[CalculationStep] = []
    notes: list[str] = []

    steps.append(
        CalculationStep(
            step_number=1,
            description="Xác định góc dốc mái α và góc hướng gió θ",
            formula_latex=r"lpha = \dots^\circ,\; 	heta = \dots^\circ",
            substitution=rf"lpha = {alpha:g}^\circ, 	heta = {theta:g}^\circ",
            result_text=f"α = {alpha:g}°, θ = {theta:g}°",
        )
    )

    if building_width_b > 0 and building_height_h > 0:
        e_dim = min(building_width_b, 2.0 * building_height_h)
        notes.append(f"Kích thước e = min(b, 2h) = {e_dim:g} m.")

    angles = sorted(_RAW_F6.keys())
    if alpha in _RAW_F6:
        r = _RAW_F6[alpha]
        f_neg, f_pos, g_neg, g_pos, h_neg, h_pos = r[0], r[1], r[2], r[3], r[4], r[5]
        i_val, j_val, k_val, l_val, m_val, n_val = r[6], r[7], r[8], r[9], r[10], r[11]
    else:
        idx = 0
        for k in range(len(angles) - 1):
            if angles[k] <= alpha <= angles[k+1]:
                idx = k
                break
        a0, a1 = angles[idx], angles[idx+1]
        r0, r1 = _RAW_F6[a0], _RAW_F6[a1]

        def _interp_val(v0: float | None, v1: float | None) -> float | None:
            if v0 is not None and v1 is not None:
                return round(_interp(alpha, a0, a1, v0, v1), 3)
            return v0 if v0 is not None else v1

        f_neg = _interp_val(r0[0], r1[0])
        f_pos = _interp_val(r0[1], r1[1])
        g_neg = _interp_val(r0[2], r1[2])
        g_pos = _interp_val(r0[3], r1[3])
        h_neg = _interp_val(r0[4], r1[4])
        h_pos = _interp_val(r0[5], r1[5])
        i_val = round(_interp(alpha, a0, a1, r0[6], r1[6]), 3)
        j_val = round(_interp(alpha, a0, a1, r0[7], r1[7]), 3)
        k_val = round(_interp(alpha, a0, a1, r0[8], r1[8]), 3)
        l_val = round(_interp(alpha, a0, a1, r0[9], r1[9]), 3)
        m_val = round(_interp(alpha, a0, a1, r0[10], r1[10]), 3)
        n_val = round(_interp(alpha, a0, a1, r0[11], r1[11]), 3)

    scenarios = {}
    if f_pos is not None and f_neg is not None:
        scenarios["Trường hợp 1 (Áp lực âm / Hút)"] = {
            "Vùng F": f_neg, "Vùng G": g_neg, "Vùng H": h_neg, "Vùng I": i_val,
            "Vùng J": j_val, "Vùng K": k_val, "Vùng L": l_val, "Vùng M": m_val, "Vùng N": n_val
        }
        scenarios["Trường hợp 2 (Áp lực dương / Đẩy)"] = {
            "Vùng F": f_pos, "Vùng G": g_pos, "Vùng H": h_pos, "Vùng I": i_val,
            "Vùng J": j_val, "Vùng K": k_val, "Vùng L": l_val, "Vùng M": m_val, "Vùng N": n_val
        }
        notes.append("CHÚ THÍCH 1 Bảng F.6: Bắt buộc xét 2 trường hợp tải trọng riêng biệt (Toàn bộ âm hoặc Toàn bộ dương).")
        primary = f_neg
        zone_vals = {}
    else:
        primary = f_pos if f_pos is not None else f_neg
        zone_vals = {
            "Vùng F": primary, "Vùng G": g_pos if g_pos is not None else g_neg, "Vùng H": h_pos if h_pos is not None else h_neg,
            "Vùng I": i_val, "Vùng J": j_val, "Vùng K": k_val, "Vùng L": l_val, "Vùng M": m_val, "Vùng N": n_val
        }

    return CalculationResult(
        formula_id="F_WIND_TCVN2737_F7_HIPPED",
        formula_name="Hệ số khí động c_e cho mái dốc bốn phía",
        standard_reference="Mục F.5, Hình F.7 & Bảng F.6 TCVN 2737:2023",
        inputs={"pitch_angle_alpha": alpha, "wind_angle_theta": theta},
        outputs=scenarios if scenarios else {f"ce_{z}": val for z, val in zone_vals.items()},
        unit="",
        primary_value=primary,
        zone_values=zone_vals,
        scenarios=scenarios,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message="Hệ số c_e cho mái dốc bốn phía đã được tính toán chính xác theo Bảng F.6.",
    )


# ===========================================================================
# 7. PHỤ LỤC E: HỆ SỐ HIỆU ỨNG GIẬT G_f VÀ KÍCH THƯỚC TƯƠNG ĐƯƠNG MẶT BẰNG PHỨC TẠP
# ===========================================================================

def calc_gust_factor_gf(
    structure_type: str,
    height_h: float,
    period_T1: float = 1.2,
) -> CalculationResult:
    """Tính toán hệ số hiệu ứng giật G_f theo công thức đơn giản (Phụ lục E.1 TCVN 2737:2023).

    Áp dụng sơ bộ cho nhà cao tầng có hình dạng đều đặn theo chiều cao,
    chu kỳ dao động riêng cơ bản thứ nhất T1 > 1s và chiều cao h <= 150m.

    Args:
        structure_type: Loại kết cấu ('concrete' / 'be_tong_cot_thep' hoặc 'steel' / 'thep').
        height_h: Chiều cao công trình (m).
        period_T1: Chu kỳ dao động riêng thứ nhất T1 (s, mặc định 1.2s).
    """
    if height_h <= 0:
        raise ValueError("Chiều cao công trình h phải > 0")

    st_norm = structure_type.strip().lower()
    is_concrete = any(k in st_norm for k in ["concrete", "be_tong", "btct", "reinforced"])
    is_steel = any(k in st_norm for k in ["steel", "thep"])

    if not is_concrete and not is_steel:
        raise ValueError(f"Loại kết cấu '{structure_type}' không hợp lệ. Chọn 'concrete' (bê tông) hoặc 'steel' (thép).")

    steps: list[CalculationStep] = []
    notes: list[str] = []

    steps.append(
        CalculationStep(
            step_number=1,
            description="Kiểm tra phạm vi áp dụng công thức đơn giản Phụ lục E.1",
            formula_latex=r"T_1 > 1\text{ s}, h \le 150\text{ m}",
            substitution=f"T_1 = {period_T1:g} s, h = {height_h:g} m",
            result_text=f"T1 = {period_T1:g}s, h = {height_h:g}m",
        )
    )

    if height_h > 150.0:
        notes.append(f"CẢNH BÁO: Chiều cao h = {height_h:g}m vượt quá 150m. Phụ lục E.1 chỉ cho phép tính toán sơ bộ cho h <= 150m. Cần tính toán chi tiết theo Mục 10.2.")

    if period_T1 <= 1.0:
        notes.append(f"CHÚ Ý: Chu kỳ T1 = {period_T1:g}s <= 1.0s. Công trình thuộc dạng công trình cứng, Gf có thể lấy bằng 0.85 theo quy định chung.")

    if is_concrete:
        gf = 0.8 + height_h / 1200.0
        formula_latex = r"G_f = 0{,}8 + \frac{h}{1\,200}"
        subst = f"G_f = 0.8 + {height_h:g} / 1200 = {gf:.4f}"
        st_name = "Nhà bê tông cốt thép (Công thức E.1)"
        f_id = "F_WIND_TCVN2737_E1_CONCRETE"
    else:
        gf = 0.85 + height_h / 800.0
        formula_latex = r"G_f = 0{,}85 + \frac{h}{800}"
        subst = f"G_f = 0.85 + {height_h:g} / 800 = {gf:.4f}"
        st_name = "Nhà thép (Công thức E.2)"
        f_id = "F_WIND_TCVN2737_E2_STEEL"

    gf_rounded = round(gf, 4)

    steps.append(
        CalculationStep(
            step_number=2,
            description=f"Tính hệ số hiệu ứng giật G_f cho {st_name}",
            formula_latex=formula_latex,
            substitution=subst,
            result_text=f"G_f = {gf_rounded:.4f}",
        )
    )

    return CalculationResult(
        formula_id=f_id,
        formula_name=f"Hệ số hiệu ứng giật G_f ({st_name})",
        standard_reference="Mục E.1, Phụ lục E TCVN 2737:2023",
        inputs={"structure_type": structure_type, "height_h": height_h, "period_T1": period_T1},
        outputs={"gust_factor_Gf": gf_rounded},
        unit="",
        primary_value=gf_rounded,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message=f"Hệ số G_f = {gf_rounded:.4f} được tính toán hợp lệ theo {st_name}.",
    )


def calc_equivalent_building_dimensions(
    shape: str,
    b: float,
    d: float = 0.0,
    d1: float = 0.0,
    d2: float = 0.0,
) -> CalculationResult:
    """Xác định kích thước tương đương (d, b) cho mặt bằng phức tạp (Phụ lục E.2 / Hình E.1).

    Căn cứ: Mục E.2, Hình E.1 Phụ lục E TCVN 2737:2023.

    Args:
        shape: Dạng mặt bằng ('U', 'X', 'Y_DOUBLE', 'Y_SINGLE', 'L', 'Z').
        b: Bề rộng đón gió tổng thể của hình chữ nhật ngoại tiếp (m).
        d: Chiều sâu tổng thể dọc hướng gió cho dạng U, X (m).
        d1: Chiều sâu nhánh 1 cho dạng L, Z (m).
        d2: Chiều sâu nhánh 2 cho dạng L, Z (m).
    """
    if b <= 0:
        raise ValueError("Bề rộng đón gió b phải > 0")

    sh_norm = shape.strip().upper().replace(" ", "_")
    steps: list[CalculationStep] = []
    notes: list[str] = []

    if sh_norm in ("U", "X", "Y_DOUBLE"):
        d_equiv = d if d > 0 else b
        formula_latex = r"d = d, b = b"
        subst = f"d = {d_equiv:g} m, b = {b:g} m"
        desc = f"Mặt bằng hình chữ {sh_norm} (Hình E.1a/b/c)"
        notes.append("Kích thước tương đương lấy bằng kích thước hình chữ nhật ngoại tiếp.")
    elif sh_norm in ("Y", "Y_SINGLE", "Y_DON"):
        d_equiv = round(b / 1.8, 3)
        formula_latex = r"d = \frac{b}{1{,}8}"
        subst = f"d = {b:g} / 1.8 = {d_equiv:g} m"
        desc = "Mặt bằng hình chữ Y đơn (Hình E.1d)"
        notes.append("CHÚ THÍCH Hình E.1d: d = b / 1.8.")
    elif sh_norm in ("L", "Z"):
        if d1 <= 0 or d2 <= 0:
            raise ValueError(f"Dạng mặt bằng chữ {sh_norm} yêu cầu cung cấp d1 > 0 và d2 > 0.")
        d_equiv = round((d1 + d2) / 2.0, 3)
        formula_latex = r"d = \frac{d_1 + d_2}{2}"
        subst = f"d = ({d1:g} + {d2:g}) / 2 = {d_equiv:g} m"
        desc = f"Mặt bằng hình chữ {sh_norm} (Hình E.1e/f)"
        notes.append(f"CHÚ THÍCH Hình E.1{sh_norm.lower()}: d = (d1 + d2) / 2.")
    else:
        raise ValueError(f"Dạng mặt bằng '{shape}' không được hỗ trợ. Chọn U, X, Y_DOUBLE, Y_SINGLE, L, Z.")

    b_equiv = b

    steps.append(
        CalculationStep(
            step_number=1,
            description=f"Quy đổi kích thước tương đương cho {desc}",
            formula_latex=formula_latex,
            substitution=subst,
            result_text=f"d_equiv = {d_equiv:g} m, b_equiv = {b_equiv:g} m",
        )
    )

    return CalculationResult(
        formula_id="F_WIND_TCVN2737_E_EQUIV_DIM",
        formula_name=f"Kích thước tương đương cho {desc}",
        standard_reference="Mục E.2, Hình E.1 Phụ lục E TCVN 2737:2023",
        inputs={"shape": shape, "b": b, "d": d, "d1": d1, "d2": d2},
        outputs={"b_equiv": b_equiv, "d_equiv": d_equiv},
        unit="m",
        primary_value=d_equiv,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message=f"Đã xác định kích thước tương đương d = {d_equiv:g}m, b = {b_equiv:g}m cho mặt bằng {desc}.",
    )


# ===========================================================================
# 8. PHỤ LỤC C: MỐC CHUẨN KHÍ ĐỘNG z0 & PHỤ LỤC D: HỆ SỐ ĐỘ CAO k(z)
# ===========================================================================

def calc_topography_datum_z0(
    slope_i: float,
    height_H: float = 10.0,
    zone: str = "BC",
    x_pos: float = 0.0,
    z1: float = 0.0,
    z2: float = 0.0,
) -> CalculationResult:
    """Xác định mặt cao độ quy ước z0 (mốc chuẩn khí động) theo độ dốc địa hình (Phụ lục C TCVN 2737:2023).

    Căn cứ: Mục C.1, Hình C.1a & C.1b Phụ lục C TCVN 2737:2023.

    Args:
        slope_i: Độ dốc địa hình so với phương ngang (i = tan theta hoặc H/L).
        height_H: Chiều cao chênh lệch địa hình H (m, mặc định 10m).
        zone: Vị trí xét ('left_A', 'AB', 'BC', 'CD', 'right_D', mặc định 'BC').
        x_pos: Vị trí tương đối trên đoạn nội suy (m).
        z1: Cao độ mặt đất thực đỉnh dốc (m).
        z2: Cao độ mặt đất thực chân dốc (m).
    """
    if slope_i < 0:
        raise ValueError("Độ dốc địa hình i phải >= 0")
    if height_H <= 0:
        raise ValueError("Chiều cao chênh lệch địa hình H phải > 0")

    steps: list[CalculationStep] = []
    notes: list[str] = []

    if slope_i <= 0.3:
        z0 = 0.0
        formula_latex = r"z_0 = 0\text{ (mặt đất bằng phẳng)}"
        subst = f"i = {slope_i:g} <= 0.3 -> z0 = 0 m"
        desc = "Trường hợp 1: Độ dốc nhỏ (i <= 0.3)"
        notes.append("Độ cao z được tính trực tiếp từ mặt đất thực đặt công trình.")
    elif slope_i < 2.0:
        desc = "Trường hợp 2: Sườn dốc vừa (0.3 < i < 2, Hình C.1a)"
        z0_bc = round(height_H * (2.0 - slope_i) / 1.7, 3)
        formula_latex = r"z_0 = \frac{H(2 - i)}{1{,}7}"
        subst = f"z0 = {height_H:g} * (2 - {slope_i:g}) / 1.7 = {z0_bc:g} m"
        z0 = z0_bc
        notes.append(f"Trên đoạn BC: z0 = H*(2-i)/1.7 = {z0_bc:g}m.")
        notes.append("Bên trái A: z0 = z1; Bên phải D: z0 = z2; Trên AB và CD: nội suy tuyến tính.")
    else:
        desc = "Trường hợp 3: Vách dốc đứng (i >= 2.0, Hình C.1b)"
        z0 = z1
        formula_latex = r"z_0 = z_1\text{ hoặc nội suy theo Hình C.1b}"
        subst = f"i = {slope_i:g} >= 2.0 -> z0 = z1 = {z1:g} m (đỉnh vách)"
        notes.append("Bên trái C: z0 = z1; Bên phải D: z0 = z2; Trên CD: nội suy tuyến tính.")

    steps.append(
        CalculationStep(
            step_number=1,
            description=f"Xác định mốc chuẩn quy ước z0 cho {desc}",
            formula_latex=formula_latex,
            substitution=subst,
            result_text=f"z0 = {z0:g} m",
        )
    )

    return CalculationResult(
        formula_id="F_WIND_TCVN2737_C_DATUM",
        formula_name=f"Mốc chuẩn khí động học z0 ({desc})",
        standard_reference="Mục C.1, Phụ lục C TCVN 2737:2023",
        inputs={"slope_i": slope_i, "height_H": height_H, "zone": zone, "z1": z1, "z2": z2},
        outputs={"datum_z0": z0, "slope_i": slope_i, "height_H": height_H},
        unit="m",
        primary_value=z0,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message=f"Đã xác định mốc chuẩn quy ước z0 = {z0:g}m theo {desc}.",
    )


def calc_terrain_height_factor_kz(
    terrain_category: str,
    height_z: float,
) -> CalculationResult:
    """Tính toán hệ số k(z_e) theo độ cao z và dạng địa hình A, B, C (Bảng 8 & Bảng 9 TCVN 2737:2023).

    Căn cứ: Mục 10.2.4, Bảng 8 & Bảng 9 và Phụ lục D TCVN 2737:2023.

    Args:
        terrain_category: Dạng địa hình ('A', 'B' hoặc 'C').
        height_z: Chiều cao điểm tính toán so với mốc chuẩn (m).
    """
    if height_z <= 0:
        raise ValueError("Chiều cao tính toán z phải > 0")

    cat_norm = terrain_category.strip().upper()
    if cat_norm not in ("A", "B", "C"):
        raise ValueError(f"Dạng địa hình '{terrain_category}' không hợp lệ. Chọn 'A', 'B' hoặc 'C'.")

    steps: list[CalculationStep] = []
    notes: list[str] = []

    if cat_norm == "A":
        z_min = 1.0
        z_eff = max(height_z, z_min)
        kz = 0.86 * (z_eff / 10.0) ** 0.22
        formula_latex = r"k(z) = 0{,}86 \cdot \left(\frac{z}{10}\right)^{0{,}22}"
        desc = "Địa hình dạng A (trống trải, ít vật cản)"
        notes.append("Bảng 8: zg = 250m, zmin = 1m, alpha = 0.11.")
    elif cat_norm == "B":
        z_min = 3.0
        z_eff = max(height_z, z_min)
        kz = (z_eff / 10.0) ** 0.30
        formula_latex = r"k(z) = \left(\frac{z}{10}\right)^{0{,}30}"
        desc = "Địa hình dạng B (tương đối trống trải, có vật cản phân tán)"
        notes.append("Bảng 8: zg = 300m, zmin = 3m, alpha = 0.15.")
    else:
        z_min = 10.0
        z_eff = max(height_z, z_min)
        kz = (z_eff / 10.0) ** 0.40
        formula_latex = r"k(z) = \left(\frac{z}{10}\right)^{0{,}40}"
        desc = "Địa hình dạng C (bị che chắn mạnh, nội thành đô thị lớn)"
        notes.append("Bảng 8: zg = 400m, zmin = 10m, alpha = 0.20.")

    if height_z < z_min:
        notes.append(f"Chiều cao z = {height_z:g}m < zmin = {z_min:g}m, lấy k(z) = k(zmin) theo quy định Mục 10.2.4.")

    kz_rounded = round(kz, 3)

    steps.append(
        CalculationStep(
            step_number=1,
            description=f"Tính hệ số độ cao k(z) cho {desc}",
            formula_latex=formula_latex,
            substitution=f"k({height_z:g}) = k({z_eff:g}) = {kz_rounded:g}",
            result_text=f"k(z) = {kz_rounded:g}",
        )
    )

    return CalculationResult(
        formula_id="F_WIND_TCVN2737_D_KZ",
        formula_name=f"Hệ số k(z) độ cao ({desc})",
        standard_reference="Mục 10.2.4, Bảng 8 & Bảng 9 TCVN 2737:2023",
        inputs={"terrain_category": terrain_category, "height_z": height_z},
        outputs={"k_z": kz_rounded, "z_eff": z_eff, "z_min": z_min},
        unit="",
        primary_value=kz_rounded,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message=f"Đã tính toán thành công hệ số độ cao k(z) = {kz_rounded:g} cho địa hình dạng {cat_norm} ở độ cao z = {height_z:g}m.",
    )


