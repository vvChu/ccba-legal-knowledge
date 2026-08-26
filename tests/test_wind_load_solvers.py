"""
Unit tests for Wind Load Deterministic Solvers and Visual Card Engine (TCVN 2737:2023 - Phụ lục F).
Kiểm chứng tính đúng đắn 100% số học và hình học (ADR 0020 & ADR 0030).
"""

from __future__ import annotations

import pytest

from formulas import (
    SymbolicFormulaSolver,
    VisualCardEngine,
    calc_duopitch_roof_ce_coefficients,
    calc_freestanding_wall_aerodynamic_coeff,
)


class TestFreestandingWallSolvers:
    """Kiểm tra tra cứu và nội suy hệ số c_x cho tường phẳng (Bảng F.1 & Hình F.1)."""

    def test_straight_wall_L_over_h_5(self) -> None:
        """Test Case 1: Tường phẳng L=20m, h=4m (L/h=5, phi=1.0) -> A=2.9, B=1.8, C=1.4, D=1.2."""
        res = calc_freestanding_wall_aerodynamic_coeff(
            length_L=20.0,
            height_h=4.0,
            solidity_ratio_phi=1.0,
            has_return_corner=False,
        )
        assert res.zone_values["Vùng A"] == 2.9
        assert res.zone_values["Vùng B"] == 1.8
        assert res.zone_values["Vùng C"] == 1.4
        assert res.zone_values["Vùng D"] == 1.2
        assert res.is_compliant is True

    def test_straight_wall_L_over_h_3(self) -> None:
        """Tường phẳng L=12m, h=4m (L/h=3, phi=1.0) -> A=2.3, B=1.4, C=1.2, D=1.2."""
        res = calc_freestanding_wall_aerodynamic_coeff(
            length_L=12.0,
            height_h=4.0,
            solidity_ratio_phi=1.0,
        )
        assert res.zone_values["Vùng A"] == 2.3
        assert res.zone_values["Vùng B"] == 1.4
        assert res.zone_values["Vùng C"] == 1.2
        assert res.zone_values["Vùng D"] == 1.2

    def test_straight_wall_L_over_h_12(self) -> None:
        """Tường phẳng L=48m, h=4m (L/h=12 >= 10, phi=1.0) -> A=3.4, B=2.1, C=1.7, D=1.2."""
        res = calc_freestanding_wall_aerodynamic_coeff(
            length_L=48.0,
            height_h=4.0,
            solidity_ratio_phi=1.0,
        )
        assert res.zone_values["Vùng A"] == 3.4
        assert res.zone_values["Vùng B"] == 2.1
        assert res.zone_values["Vùng C"] == 1.7
        assert res.zone_values["Vùng D"] == 1.2

    def test_straight_wall_interpolated_L_over_h_4(self) -> None:
        """Tường phẳng L=16m, h=4m (L/h=4.0 nằm giữa 3 và 5) -> Nội suy A=2.6, B=1.6, C=1.3, D=1.2."""
        res = calc_freestanding_wall_aerodynamic_coeff(
            length_L=16.0,
            height_h=4.0,
            solidity_ratio_phi=1.0,
        )
        assert res.zone_values["Vùng A"] == 2.6
        assert res.zone_values["Vùng B"] == 1.6
        assert res.zone_values["Vùng C"] == 1.3
        assert res.zone_values["Vùng D"] == 1.2

    def test_return_corner_wall(self) -> None:
        """Test Case 2: Tường có bẻ góc l_ret = 4m >= h = 4m, phi=1.0 -> A=2.1, B=1.8, C=1.4, D=1.2."""
        res = calc_freestanding_wall_aerodynamic_coeff(
            length_L=20.0,
            height_h=4.0,
            solidity_ratio_phi=1.0,
            has_return_corner=True,
            return_corner_length=4.0,
        )
        assert res.zone_values["Vùng A"] == 2.1
        assert res.zone_values["Vùng B"] == 1.8
        assert res.zone_values["Vùng C"] == 1.4
        assert res.zone_values["Vùng D"] == 1.2

    def test_permeable_wall_phi_0_8(self) -> None:
        """Tường rỗng / hàng rào phi = 0.8 -> A=1.2, B=1.2, C=1.2, D=1.2."""
        res = calc_freestanding_wall_aerodynamic_coeff(
            length_L=20.0,
            height_h=4.0,
            solidity_ratio_phi=0.8,
        )
        assert res.zone_values["Vùng A"] == 1.2
        assert res.zone_values["Vùng B"] == 1.2
        assert res.zone_values["Vùng C"] == 1.2
        assert res.zone_values["Vùng D"] == 1.2


class TestDuopitchRoofSolvers:
    """Kiểm tra tra cứu và phân tách kịch bản c_e cho mái dốc 2 phía (Bảng F.5a, F.5b & Hình F.6)."""

    def test_duopitch_alpha_15_theta_0(self) -> None:
        """Test Case 3: Mái dốc alpha = 15°, theta = 0° -> 2 kịch bản Hút và Đẩy."""
        res = calc_duopitch_roof_ce_coefficients(
            pitch_angle_alpha=15.0,
            wind_angle_theta=0.0,
            building_width_b=30.0,
            building_height_h=8.0,
        )
        assert "Trường hợp 1 (Áp lực âm / Hút)" in res.scenarios
        assert "Trường hợp 2 (Áp lực dương / Đẩy)" in res.scenarios

        case_suction = res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]
        assert case_suction["Vùng F"] == -0.9
        assert case_suction["Vùng G"] == -0.8
        assert case_suction["Vùng H"] == -0.3
        assert case_suction["Vùng I"] == -0.4
        assert case_suction["Vùng J"] == -1.0

        case_pressure = res.scenarios["Trường hợp 2 (Áp lực dương / Đẩy)"]
        assert case_pressure["Vùng F"] == 0.2
        assert case_pressure["Vùng G"] == 0.2
        assert case_pressure["Vùng H"] == 0.2
        assert case_pressure["Vùng I"] == -0.4
        assert case_pressure["Vùng J"] == -1.0

    def test_duopitch_interpolated_alpha_20_theta_0(self) -> None:
        """Test Case 4: Nội suy tuyến tính tại alpha = 20° giữa 15° và 30°."""
        res = calc_duopitch_roof_ce_coefficients(
            pitch_angle_alpha=20.0,
            wind_angle_theta=0.0,
        )
        case_suction = res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]
        case_pressure = res.scenarios["Trường hợp 2 (Áp lực dương / Đẩy)"]

        # Vùng F âm: -0.9 + (5/15)*(-0.5 - (-0.9)) = -0.767
        assert abs(case_suction["Vùng F"] - (-0.767)) < 0.01
        # Vùng F dương: +0.2 + (5/15)*(0.7 - 0.2) = +0.367
        assert abs(case_pressure["Vùng F"] - 0.367) < 0.01

    def test_duopitch_alpha_15_theta_90(self) -> None:
        """Hướng gió theta = 90° (Bảng F.5b) tại alpha = 15° -> F=-1.3, G=-1.3, H=-0.6, I=-0.5."""
        res = calc_duopitch_roof_ce_coefficients(
            pitch_angle_alpha=15.0,
            wind_angle_theta=90.0,
        )
        assert res.zone_values["Vùng F"] == -1.3
        assert res.zone_values["Vùng G"] == -1.3
        assert res.zone_values["Vùng H"] == -0.6
        assert res.zone_values["Vùng I"] == -0.5

    def test_duopitch_alpha_60_theta_0(self) -> None:
        """Mái dốc đứng alpha = 60° -> Chỉ có giá trị dương cho mặt đón gió (+0.7)."""
        res = calc_duopitch_roof_ce_coefficients(
            pitch_angle_alpha=60.0,
            wind_angle_theta=0.0,
        )
        assert res.zone_values["Vùng F"] == 0.7
        assert res.zone_values["Vùng G"] == 0.7
        assert res.zone_values["Vùng H"] == 0.7
        assert res.zone_values["Vùng I"] == -0.2
        assert res.zone_values["Vùng J"] == -0.3


class TestVisualCardEngine:
    """Kiểm tra nạp và đánh giá hình học từ Visual Cards JSON."""

    def test_list_cards(self) -> None:
        cards = VisualCardEngine.list_cards()
        assert len(cards) >= 2
        card_ids = [c["card_id"] for c in cards]
        assert "FIG_TCVN2737_F1" in card_ids
        assert "FIG_TCVN2737_F6" in card_ids

    def test_evaluate_wall_f1(self) -> None:
        eval_res = VisualCardEngine.evaluate_wall_f1(length_L=20.0, height_h=4.0)
        assert eval_res.matched_case_id == "CASE_LONG_WALL"
        assert eval_res.zones["Zone_A"].dimension_m["length_m"] == 1.2
        assert eval_res.zones["Zone_B"].dimension_m["length_m"] == 6.8
        assert eval_res.zones["Zone_C"].dimension_m["length_m"] == 8.0
        assert eval_res.zones["Zone_D"].dimension_m["length_m"] == 4.0

    def test_evaluate_duopitch_f6(self) -> None:
        eval_res = VisualCardEngine.evaluate_duopitch_f6(
            pitch_angle_alpha=15.0,
            wind_angle_theta=0.0,
            building_width_b=30.0,
            building_height_h=8.0,
            building_depth_d=50.0,
        )
        # e = min(30, 2*8) = 16 m
        assert eval_res.calculated_parameters["e_dimension"] == 16.0
        assert eval_res.calculated_parameters["e_over_10"] == 1.6
        assert eval_res.calculated_parameters["e_over_4"] == 4.0


class TestSolverFacade:
    """Kiểm tra đăng ký và gọi facade giải toán qua SymbolicFormulaSolver."""

    def test_solve_wall(self) -> None:
        res = SymbolicFormulaSolver.solve(
            "F_WIND_TCVN2737_F1_WALL",
            {"length_L": 20.0, "height_h": 4.0, "solidity_ratio_phi": 1.0},
        )
        assert res.formula_id == "F_WIND_TCVN2737_F1_WALL"
        assert res.zone_values["Vùng A"] == 2.9
        report = res.format_text_report()
        assert "BÁO CÁO TÍNH TOÁN" in report
        assert "Vùng A" in report

    def test_solve_duopitch(self) -> None:
        res = SymbolicFormulaSolver.solve(
            "F_WIND_TCVN2737_F6_DUOPITCH",
            {"pitch_angle_alpha": 15.0, "wind_angle_theta": 0.0},
        )
        assert res.formula_id == "F_WIND_TCVN2737_F6_DUOPITCH"
        assert "Trường hợp 1 (Áp lực âm / Hút)" in res.scenarios
        report = res.format_text_report()
        assert "Trường hợp 1 (Áp lực âm / Hút)" in report
