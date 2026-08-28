"""
Unit tests for Wind Load Deterministic Solvers and Visual Card Engine (TCVN 2737:2023 - Phụ lục F).
Kiểm chứng tính đúng đắn 100% số học và hình học (ADR 0020 & ADR 0030).
"""

from __future__ import annotations

import pytest

from formulas import (
    SymbolicFormulaSolver,
    VisualCardEngine,
    calc_base_wind_pressure_w0,
    calc_duopitch_roof_ce_coefficients,
    calc_equivalent_building_dimensions,
    calc_flat_roof_ce_coefficients,
    calc_freestanding_wall_aerodynamic_coeff,
    calc_gust_factor_gf,
    calc_hipped_roof_ce_coefficients,
    calc_monopitch_roof_ce_coefficients,
    calc_terrain_height_factor_kz,
    calc_topography_datum_z0,
    calc_vertical_wall_ce_coefficients,
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


class TestFlatRoofSolvers:
    """Kiểm tra tra cứu hệ số c_e cho mái bằng (Bảng F.2 & Hình F.3)."""

    def test_sharp_eaves(self) -> None:
        """Mái bằng có cạnh sắc -> F=-1.8, G=-1.2, H=-0.7, I=±0.2."""
        res = calc_flat_roof_ce_coefficients(eaves_type="CANH_SAC", building_height_h=10.0, building_width_b=30.0)
        assert res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]["Vùng F"] == -1.8
        assert res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]["Vùng G"] == -1.2
        assert res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]["Vùng H"] == -0.7
        assert res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]["Vùng I"] == -0.2
        assert res.scenarios["Trường hợp 2 (Áp lực dương / Đẩy)"]["Vùng I"] == 0.2

    def test_parapet_0_05(self) -> None:
        """Mái bằng có tường chắn mái hp/h = 0.05 -> F=-1.4, G=-0.9."""
        res = calc_flat_roof_ce_coefficients(
            eaves_type="TUONG_CHAN_MAI",
            parapet_height_hp=0.5,
            building_height_h=10.0,
        )
        assert res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]["Vùng F"] == -1.4
        assert res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]["Vùng G"] == -0.9

    def test_rounded_0_10(self) -> None:
        """Mái bằng có cạnh bo tròn r/h = 0.10 -> F=-0.7, G=-0.7, H=-0.7."""
        res = calc_flat_roof_ce_coefficients(
            eaves_type="BO_TRON",
            radius_r=1.0,
            building_height_h=10.0,
        )
        assert res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]["Vùng F"] == -0.7
        assert res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]["Vùng G"] == -0.7
        assert res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]["Vùng H"] == -0.7


class TestVerticalWallSolvers:
    """Kiểm tra tra cứu hệ số c_e cho tường thẳng đứng (Bảng F.4 & Hình F.5a)."""

    def test_h_over_d_5(self) -> None:
        """h/d = 5.0 -> A=-1.2, B=-0.8, C=-0.5, D=+0.8, E=-0.7."""
        res = calc_vertical_wall_ce_coefficients(building_height_h=50.0, building_depth_d=10.0)
        assert res.zone_values["Vùng A (Tường bên mép đón)"] == -1.2
        assert res.zone_values["Vùng B (Tường bên dải giữa)"] == -0.8
        assert res.zone_values["Vùng C (Tường bên dải cuối)"] == -0.5
        assert res.zone_values["Vùng D (Tường đón gió)"] == 0.8
        assert res.zone_values["Vùng E (Tường hút gió)"] == -0.7

    def test_h_over_d_1(self) -> None:
        """h/d = 1.0 -> A=-1.2, B=-0.8, C=-0.5, D=+0.8, E=-0.5."""
        res = calc_vertical_wall_ce_coefficients(building_height_h=20.0, building_depth_d=20.0)
        assert res.zone_values["Vùng D (Tường đón gió)"] == 0.8
        assert res.zone_values["Vùng E (Tường hút gió)"] == -0.5

    def test_h_over_d_0_25(self) -> None:
        """h/d = 0.25 -> A=-1.2, B=-0.8, C=-0.5, D=+0.7, E=-0.3."""
        res = calc_vertical_wall_ce_coefficients(building_height_h=5.0, building_depth_d=20.0)
        assert res.zone_values["Vùng D (Tường đón gió)"] == 0.7
        assert res.zone_values["Vùng E (Tường hút gió)"] == -0.3


class TestMonopitchRoofSolvers:
    """Kiểm tra tra cứu hệ số c_e cho mái dốc một phía (Bảng F.3a, F.3b)."""

    def test_alpha_15_theta_0(self) -> None:
        """alpha = 15°, theta = 0° -> Dual: Hút (F=-0.9, G=-0.8, H=-0.3), Đẩy (F=+0.2, G=+0.2, H=+0.2)."""
        res = calc_monopitch_roof_ce_coefficients(pitch_angle_alpha=15.0, wind_angle_theta=0.0)
        assert res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]["Vùng F"] == -0.9
        assert res.scenarios["Trường hợp 2 (Áp lực dương / Đẩy)"]["Vùng F"] == 0.2

    def test_alpha_15_theta_180(self) -> None:
        """alpha = 15°, theta = 180° -> F=-2.5, G=-1.3, H=-0.9."""
        res = calc_monopitch_roof_ce_coefficients(pitch_angle_alpha=15.0, wind_angle_theta=180.0)
        assert res.zone_values["Vùng F"] == -2.5
        assert res.zone_values["Vùng G"] == -1.3
        assert res.zone_values["Vùng H"] == -0.9

    def test_alpha_15_theta_90(self) -> None:
        """alpha = 15°, theta = 90° -> F_up=-2.4, F_low=-1.6, G=-1.9, H=-0.8, I=-0.7."""
        res = calc_monopitch_roof_ce_coefficients(pitch_angle_alpha=15.0, wind_angle_theta=90.0)
        assert res.zone_values["Vùng F_up"] == -2.4
        assert res.zone_values["Vùng F_low"] == -1.6
        assert res.zone_values["Vùng G"] == -1.9
        assert res.zone_values["Vùng H"] == -0.8
        assert res.zone_values["Vùng I"] == -0.7


class TestHippedRoofSolvers:
    """Kiểm tra tra cứu hệ số c_e cho mái dốc bốn phía (Bảng F.6)."""

    def test_alpha_15_theta_0(self) -> None:
        """alpha = 15°, theta = 0° -> Dual F, G, H và các vùng I, J, K, L, M, N."""
        res = calc_hipped_roof_ce_coefficients(pitch_angle_alpha=15.0, wind_angle_theta=0.0)
        case_suction = res.scenarios["Trường hợp 1 (Áp lực âm / Hút)"]
        assert case_suction["Vùng F"] == -0.9
        assert case_suction["Vùng G"] == -0.8
        assert case_suction["Vùng H"] == -0.3
        assert case_suction["Vùng I"] == -0.5
        assert case_suction["Vùng J"] == -1.0
        assert case_suction["Vùng K"] == -1.2
        assert case_suction["Vùng L"] == -1.4
        assert case_suction["Vùng M"] == -0.6
        assert case_suction["Vùng N"] == -0.3


class TestExtendedVisualCards:
    """Kiểm tra nạp toàn bộ các Visual Cards."""

    def test_all_cards_present(self) -> None:
        cards = VisualCardEngine.list_cards()
        assert len(cards) >= 9
        expected_ids = {
            "FIG_TCVN2737_C1",
            "FIG_TCVN2737_D1",
            "FIG_TCVN2737_E1",
            "FIG_TCVN2737_F1",
            "FIG_TCVN2737_F3",
            "FIG_TCVN2737_F4",
            "FIG_TCVN2737_F5A",
            "FIG_TCVN2737_F6",
            "FIG_TCVN2737_F7",
        }
        found_ids = {c["card_id"] for c in cards}
        assert expected_ids.issubset(found_ids)


class TestGustFactorSolvers:
    """Kiểm tra tính toán hệ số hiệu ứng giật G_f theo Phụ lục E.1 TCVN 2737:2023."""

    def test_concrete_building_h_60m(self) -> None:
        """Nhà BTCT h=60m, T1=1.2s -> Gf = 0.8 + 60/1200 = 0.85."""
        res = calc_gust_factor_gf(structure_type="concrete", height_h=60.0, period_T1=1.2)
        assert res.primary_value == 0.85
        assert res.outputs["gust_factor_Gf"] == 0.85
        assert res.is_compliant is True

    def test_concrete_building_h_120m(self) -> None:
        """Nhà BTCT h=120m -> Gf = 0.8 + 120/1200 = 0.90."""
        res = calc_gust_factor_gf(structure_type="be_tong_cot_thep", height_h=120.0)
        assert res.primary_value == 0.90

    def test_steel_building_h_80m(self) -> None:
        """Nhà thép h=80m -> Gf = 0.85 + 80/800 = 0.95."""
        res = calc_gust_factor_gf(structure_type="steel", height_h=80.0)
        assert res.primary_value == 0.95

    def test_steel_building_h_40m(self) -> None:
        """Nhà thép h=40m -> Gf = 0.85 + 40/800 = 0.90."""
        res = calc_gust_factor_gf(structure_type="thep", height_h=40.0)
        assert res.primary_value == 0.90

    def test_gust_factor_height_warning_above_150m(self) -> None:
        """Nhà cao h=180m vượt quá 150m -> cảnh báo trong notes."""
        res = calc_gust_factor_gf(structure_type="concrete", height_h=180.0)
        assert any("150m" in n for n in res.notes)

    def test_gust_factor_invalid_inputs(self) -> None:
        """Kiểm tra bắt lỗi đầu vào không hợp lệ."""
        with pytest.raises(ValueError, match="h phải > 0"):
            calc_gust_factor_gf(structure_type="concrete", height_h=-10.0)

        with pytest.raises(ValueError, match="không hợp lệ"):
            calc_gust_factor_gf(structure_type="wood", height_h=50.0)


class TestEquivalentDimensionsSolvers:
    """Kiểm tra quy đổi kích thước tương đương cho mặt bằng phức tạp (Phụ lục E.2 / Hình E.1)."""

    def test_shape_u_and_x(self) -> None:
        """Mặt bằng chữ U: b=30m, d=40m -> d_equiv=40m, b_equiv=30m."""
        res = calc_equivalent_building_dimensions(shape="U", b=30.0, d=40.0)
        assert res.outputs["b_equiv"] == 30.0
        assert res.outputs["d_equiv"] == 40.0

    def test_shape_y_single(self) -> None:
        """Mặt bằng chữ Y đơn: b=36m -> d_equiv = 36 / 1.8 = 20.0m."""
        res = calc_equivalent_building_dimensions(shape="Y_SINGLE", b=36.0)
        assert res.outputs["d_equiv"] == 20.0
        assert res.outputs["b_equiv"] == 36.0

    def test_shape_l(self) -> None:
        """Mặt bằng chữ L: b=50m, d1=20m, d2=40m -> d_equiv = (20 + 40)/2 = 30.0m."""
        res = calc_equivalent_building_dimensions(shape="L", b=50.0, d1=20.0, d2=40.0)
        assert res.outputs["d_equiv"] == 30.0
        assert res.outputs["b_equiv"] == 50.0

    def test_shape_z(self) -> None:
        """Mặt bằng chữ Z: b=40m, d1=15m, d2=25m -> d_equiv = (15 + 25)/2 = 20.0m."""
        res = calc_equivalent_building_dimensions(shape="Z", b=40.0, d1=15.0, d2=25.0)
        assert res.outputs["d_equiv"] == 20.0
        assert res.outputs["b_equiv"] == 40.0

    def test_solver_facade_integration(self) -> None:
        """Kiểm tra gọi qua Master Solver Facade."""
        res_gf = SymbolicFormulaSolver.solve("F_WIND_TCVN2737_E_GUST_FACTOR", {"structure_type": "concrete", "height_h": 60.0})
        assert res_gf.primary_value == 0.85

        res_dim = SymbolicFormulaSolver.solve("F_WIND_TCVN2737_E_EQUIV_DIM", {"shape": "Y", "b": 36.0})
        assert res_dim.outputs["d_equiv"] == 20.0


class TestTopographyDatumSolvers:
    """Kiểm tra xác định mốc chuẩn quy ước z0 theo Phụ lục C TCVN 2737:2023."""

    def test_gentle_slope(self) -> None:
        """Độ dốc i = 0.2 <= 0.3 -> z0 = 0.0."""
        res = calc_topography_datum_z0(slope_i=0.2)
        assert res.primary_value == 0.0
        assert res.outputs["datum_z0"] == 0.0

    def test_moderate_slope_bc(self) -> None:
        """Độ dốc i = 1.0, H = 17.0m -> z0 = 17 * (2 - 1) / 1.7 = 10.0m."""
        res = calc_topography_datum_z0(slope_i=1.0, height_H=17.0)
        assert res.primary_value == 10.0

    def test_moderate_slope_i_0_5(self) -> None:
        """Độ dốc i = 0.5, H = 10.0m -> z0 = 10 * 1.5 / 1.7 = 8.824m."""
        res = calc_topography_datum_z0(slope_i=0.5, height_H=10.0)
        assert res.primary_value == 8.824

    def test_steep_cliff(self) -> None:
        """Độ dốc i = 2.5 >= 2.0, z1 = 5.0m -> z0 = 5.0m."""
        res = calc_topography_datum_z0(slope_i=2.5, z1=5.0)
        assert res.primary_value == 5.0

    def test_invalid_inputs(self) -> None:
        with pytest.raises(ValueError, match="i phải >= 0"):
            calc_topography_datum_z0(slope_i=-0.5)


class TestTerrainHeightFactorSolvers:
    """Kiểm tra tính toán hệ số độ cao k(z) theo Mục 10.2.4, Bảng 8 & Bảng 9 và Phụ lục D."""

    def test_terrain_a_z_10m(self) -> None:
        """Dạng A ở z=10m -> k(10) = 0.86."""
        res = calc_terrain_height_factor_kz(terrain_category="A", height_z=10.0)
        assert res.primary_value == 0.86

    def test_terrain_a_z_20m(self) -> None:
        """Dạng A ở z=20m -> k(20) = 0.86 * 2^0.22 ≈ 1.002."""
        res = calc_terrain_height_factor_kz(terrain_category="A", height_z=20.0)
        assert res.primary_value == 1.002

    def test_terrain_b_z_10m(self) -> None:
        """Dạng B ở z=10m -> k(10) = 1.00."""
        res = calc_terrain_height_factor_kz(terrain_category="B", height_z=10.0)
        assert res.primary_value == 1.0

    def test_terrain_b_z_20m(self) -> None:
        """Dạng B ở z=20m -> k(20) = 2^0.30 ≈ 1.231."""
        res = calc_terrain_height_factor_kz(terrain_category="B", height_z=20.0)
        assert res.primary_value == 1.231

    def test_terrain_b_z_below_min(self) -> None:
        """Dạng B ở z=2m < zmin=3m -> lấy k(3) = 0.697."""
        res = calc_terrain_height_factor_kz(terrain_category="B", height_z=2.0)
        assert res.primary_value == 0.697
        assert any("zmin" in n for n in res.notes)

    def test_terrain_c_z_10m(self) -> None:
        """Dạng C ở z=10m -> k(10) = 1.0."""
        res = calc_terrain_height_factor_kz(terrain_category="C", height_z=10.0)
        assert res.primary_value == 1.0

    def test_terrain_c_z_5m(self) -> None:
        """Dạng C ở z=5m < zmin=10m -> lấy k(10) = 1.0."""
        res = calc_terrain_height_factor_kz(terrain_category="C", height_z=5.0)
        assert res.primary_value == 1.0


class TestVietnamWindZonesLookup:
    """Kiểm tra tra cứu áp lực gió W0 cho 63 tỉnh thành (Bảng 5.1 QCVN 02:2022 & Bảng 7 TCVN 2737:2023)."""

    def test_hanoi_general(self) -> None:
        """Hà Nội chung -> Vùng II, W0 = 95 daN/m2."""
        res = calc_base_wind_pressure_w0(province="Hà Nội")
        assert res.outputs["wind_zone"] == "II"
        assert res.primary_value == 95.0

    def test_hanoi_my_duc_huong_son(self) -> None:
        """Hà Nội, Mỹ Đức, Hương Sơn -> Vùng III, W0 = 125 daN/m2."""
        res = calc_base_wind_pressure_w0(province="Hà Nội", district="Mỹ Đức", commune="Hương Sơn")
        assert res.outputs["wind_zone"] == "III"
        assert res.primary_value == 125.0

    def test_hcm_cu_chi(self) -> None:
        """TP.HCM, Củ Chi -> Vùng I, W0 = 65 daN/m2."""
        res = calc_base_wind_pressure_w0(province="Hồ Chí Minh", district="Củ Chi")
        assert res.outputs["wind_zone"] == "I"
        assert res.primary_value == 65.0

    def test_hcm_general(self) -> None:
        """TP.HCM chung -> Vùng II, W0 = 95 daN/m2."""
        res = calc_base_wind_pressure_w0(province="Thành phố Hồ Chí Minh")
        assert res.outputs["wind_zone"] == "II"
        assert res.primary_value == 95.0

    def test_hai_phong_bach_long_vi(self) -> None:
        """Hải Phòng, Bạch Long Vĩ -> Vùng V, W0 = 185 daN/m2."""
        res = calc_base_wind_pressure_w0(province="Hải Phòng", district="Bạch Long Vĩ")
        assert res.outputs["wind_zone"] == "V"
        assert res.primary_value == 185.0

    def test_da_nang_hoang_sa(self) -> None:
        """Đà Nẵng, Hoàng Sa -> Vùng V, W0 = 185 daN/m2."""
        res = calc_base_wind_pressure_w0(province="Đà Nẵng", district="Hoàng Sa")
        assert res.outputs["wind_zone"] == "V"
        assert res.primary_value == 185.0

    def test_ba_ria_vung_tau_con_dao(self) -> None:
        """Bà Rịa - Vũng Tàu, Côn Đảo -> Vùng III, W0 = 125 daN/m2."""
        res = calc_base_wind_pressure_w0(province="Bà Rịa - Vũng Tàu", district="Côn Đảo")
        assert res.outputs["wind_zone"] == "III"
        assert res.primary_value == 125.0

    def test_can_tho(self) -> None:
        """Cần Thơ -> Vùng II, W0 = 95 daN/m2."""
        res = calc_base_wind_pressure_w0(province="Cần Thơ")
        assert res.outputs["wind_zone"] == "II"
        assert res.primary_value == 95.0

    def test_solver_facade_w0_kz_datum(self) -> None:
        """Kiểm tra gọi qua Master Solver Facade."""
        res_w0 = SymbolicFormulaSolver.solve("F_WIND_QCVN02_W0_LOOKUP", {"province": "Hà Nội"})
        assert res_w0.primary_value == 95.0

        res_kz = SymbolicFormulaSolver.solve("F_WIND_TCVN2737_D_KZ", {"terrain_category": "B", "height_z": 20.0})
        assert res_kz.primary_value == 1.231

        res_datum = SymbolicFormulaSolver.solve("F_WIND_TCVN2737_C_DATUM", {"slope_i": 1.0, "height_H": 17.0})
        assert res_datum.primary_value == 10.0


