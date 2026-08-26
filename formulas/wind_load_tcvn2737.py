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
