"""
Unit tests for Deflection and Drift Deterministic Solvers (TCVN 2737:2023 - Phụ lục G & H).
Kiểm chứng tính đúng đắn 100% số học và điều kiện an toàn f <= [fu] (ADR 0020 & ADR 0034).
"""

from __future__ import annotations

import pytest

from formulas import (
    SymbolicFormulaSolver,
    calc_horizontal_drift_limit,
    calc_importance_factor_gamma_n,
    calc_vertical_deflection_limit,
    check_deflection_and_drift_limits,
)


class TestVerticalDeflectionLimits:
    """Kiểm tra độ võng đứng giới hạn [fu] theo Bảng G.1, Bảng G.4 và Mục G.2.5.4."""

    def test_roof_floor_span_6m(self) -> None:
        """Dầm/sàn nhìn thấy nhịp L=6m -> [fu] = 6/200 = 30mm."""
        res = calc_vertical_deflection_limit(element_type="roof_floor_visible", span_L=6.0)
        assert res.primary_value == 30.0
        assert res.outputs["fu_limit_mm"] == 30.0

    def test_roof_floor_span_3m(self) -> None:
        """Dầm/sàn nhìn thấy nhịp L=3m -> [fu] = 3/150 = 20mm."""
        res = calc_vertical_deflection_limit(element_type="roof_floor_visible", span_L=3.0)
        assert res.primary_value == 20.0

    def test_roof_floor_span_1m(self) -> None:
        """Dầm/sàn nhìn thấy nhịp L=1m -> [fu] = 1/120 = 8.33mm."""
        res = calc_vertical_deflection_limit(element_type="roof_floor_visible", span_L=1.0)
        assert res.primary_value == 8.33

    def test_roof_floor_span_12m_low_room(self) -> None:
        """Nhịp L=12m trong phòng cao <= 6m -> [fu] = 12/250 = 48mm."""
        res = calc_vertical_deflection_limit(element_type="roof_floor_visible", span_L=12.0, room_height=4.0)
        assert res.primary_value == 48.0

    def test_roof_floor_span_24m_low_room(self) -> None:
        """Nhịp L=24m trong phòng cao <= 6m -> [fu] = 24/300 = 80mm."""
        res = calc_vertical_deflection_limit(element_type="roof_floor_visible", span_L=24.0, room_height=4.0)
        assert res.primary_value == 80.0

    def test_cantilever_beam_2m(self) -> None:
        """Công xôn L=2m -> L_eff = 4m -> nội suy 3m-6m -> [fu] ≈ 24.0mm."""
        res = calc_vertical_deflection_limit(element_type="roof_floor_visible", span_L=2.0, is_cantilever=True)
        assert res.outputs["L_effective_m"] == 4.0
        assert 23.9 <= res.primary_value <= 24.1

    def test_crane_girder_cabin_a1_a6(self) -> None:
        """Dầm cầu trục cabin A1-A6 nhịp L=6m -> [fu] = 6/400 = 15mm."""
        res = calc_vertical_deflection_limit(element_type="crane_girder", span_L=6.0, crane_control="cabin", crane_group="A1_A6")
        assert res.primary_value == 15.0

    def test_crane_girder_cabin_a7(self) -> None:
        """Dầm cầu trục cabin A7 nhịp L=6m -> [fu] = 6/500 = 12mm."""
        res = calc_vertical_deflection_limit(element_type="crane_girder", span_L=6.0, crane_control="cabin", crane_group="A7")
        assert res.primary_value == 12.0

    def test_crane_girder_cabin_a8(self) -> None:
        """Dầm cầu trục cabin A8 nhịp L=6m -> [fu] = 6/600 = 10mm."""
        res = calc_vertical_deflection_limit(element_type="crane_girder", span_L=6.0, crane_control="cabin", crane_group="A8")
        assert res.primary_value == 10.0

    def test_crane_girder_floor(self) -> None:
        """Dầm cầu trục điều khiển từ nền nhịp L=6m -> [fu] = 6/250 = 24mm."""
        res = calc_vertical_deflection_limit(element_type="crane_girder", span_L=6.0, crane_control="floor")
        assert res.primary_value == 24.0

    def test_moving_load_wide_rail(self) -> None:
        """Sàn tải trọng ray khổ rộng L=10m -> [fu] = 10/500 = 20mm."""
        res = calc_vertical_deflection_limit(element_type="floor_moving_load", span_L=10.0, rail_type="wide")
        assert res.primary_value == 20.0

    def test_parking_floor_span_12m(self) -> None:
        """Sàn bãi đỗ xe L=12m -> [fu] = 12/250 = 48mm."""
        res = calc_vertical_deflection_limit(element_type="parking_floor", span_L=12.0)
        assert res.primary_value == 48.0

    def test_lintel_wall_span_3m(self) -> None:
        """Lanh tô L=3m -> [fu] = 3/200 = 15mm."""
        res = calc_vertical_deflection_limit(element_type="lintel_wall", span_L=3.0)
        assert res.primary_value == 15.0

    def test_prestress_camber_span_3m(self) -> None:
        """Độ vồng L=3m -> [fu] = 15mm."""
        res = calc_vertical_deflection_limit(element_type="prestress_camber", span_L=3.0)
        assert res.primary_value == 15.0

    def test_prestress_camber_span_12m(self) -> None:
        """Độ vồng L=12m -> [fu] = 40mm."""
        res = calc_vertical_deflection_limit(element_type="prestress_camber", span_L=12.0)
        assert res.primary_value == 40.0

    def test_prestress_camber_span_7_5m(self) -> None:
        """Độ vồng L=7.5m -> nội suy = 15 + 4.5 * 25 / 9 = 27.5mm."""
        res = calc_vertical_deflection_limit(element_type="prestress_camber", span_L=7.5)
        assert res.primary_value == 27.5

    def test_invalid_span(self) -> None:
        with pytest.raises(ValueError, match="span_L phải > 0"):
            calc_vertical_deflection_limit(span_L=-2.0)


class TestHorizontalDriftLimits:
    """Kiểm tra chuyển vị ngang giới hạn [fu] theo Bảng G.3, Bảng G.5 và Mục G.2.4.2."""

    def test_multistory_building_overall_h_50m(self) -> None:
        """Toàn bộ nhà nhiều tầng h=50m -> [fu] = 50/500 = 100mm."""
        res = calc_horizontal_drift_limit(structure_type="multistory_building_overall", total_height_h=50.0)
        assert res.primary_value == 100.0

    def test_multistory_single_story_rigid_brick_hs_3_6m(self) -> None:
        """Một tầng nhà nhiều tầng tường gạch liên kết cứng hs=3.6m -> [fu] = 3.6/500 = 7.2mm."""
        res = calc_horizontal_drift_limit(
            structure_type="multistory_single_story",
            story_height_hs=3.6,
            partition_material="brick_concrete_gypsum",
            connection_type="rigid",
        )
        assert res.primary_value == 7.2

    def test_multistory_single_story_rigid_ceramic_hs_3_6m(self) -> None:
        """Một tầng nhà nhiều tầng tường ceramic liên kết cứng hs=3.6m -> [fu] = 3.6/700 = 5.14mm."""
        res = calc_horizontal_drift_limit(
            structure_type="multistory_single_story",
            story_height_hs=3.6,
            partition_material="natural_stone_ceramic",
            connection_type="rigid",
        )
        assert res.primary_value == 5.14

    def test_multistory_single_story_flexible_hs_3_6m(self) -> None:
        """Một tầng nhà nhiều tầng liên kết mềm hs=3.6m -> [fu] = 3.6/300 = 12.0mm."""
        res = calc_horizontal_drift_limit(
            structure_type="multistory_single_story",
            story_height_hs=3.6,
            connection_type="flexible",
        )
        assert res.primary_value == 12.0

    def test_single_story_building_hs_6m(self) -> None:
        """Nhà một tầng hs=6m -> [fu] = 6/300 = 20.0mm."""
        res = calc_horizontal_drift_limit(structure_type="single_story_building", story_height_hs=6.0)
        assert res.primary_value == 20.0

    def test_crane_column_a1_a3_h_10m(self) -> None:
        """Cột cầu trục A1-A3 h=10m -> [fu] = max(10000/500=20, 6) = 20.0mm."""
        res = calc_horizontal_drift_limit(structure_type="crane_column", story_height_hs=10.0, crane_group="A1_A3")
        assert res.primary_value == 20.0

    def test_crane_column_a7_a8_h_6m(self) -> None:
        """Cột cầu trục A7-A8 h=6m -> [fu] = max(6000/2000=3, 6) = 6.0mm (ngưỡng min 6mm)."""
        res = calc_horizontal_drift_limit(structure_type="crane_column", story_height_hs=6.0, crane_group="A7_A8")
        assert res.primary_value == 6.0

    def test_temperature_settlement_column_hs_3m(self) -> None:
        """Cột do nhiệt/lún tường gạch hs=3m -> [fu] = 3/150 = 20.0mm."""
        res = calc_horizontal_drift_limit(
            structure_type="temperature_settlement_column",
            story_height_hs=3.0,
            partition_material="brick",
        )
        assert res.primary_value == 20.0


class TestImportanceFactorGammaN:
    """Kiểm tra hệ số tầm quan trọng gamma_n theo Phụ lục H."""

    def test_gamma_n_uls_c1(self) -> None:
        """Cấp C1 (Thấp) TTGH1 -> gamma_n = 0.87."""
        res = calc_importance_factor_gamma_n(consequence_class="C1", limit_state="ULS")
        assert res.primary_value == 0.87

    def test_gamma_n_uls_c2(self) -> None:
        """Cấp C2 (Trung bình) TTGH1 -> gamma_n = 1.00."""
        res = calc_importance_factor_gamma_n(consequence_class="C2", limit_state="ULS")
        assert res.primary_value == 1.00

    def test_gamma_n_uls_c3(self) -> None:
        """Cấp C3 (Cao) TTGH1 -> gamma_n = 1.15."""
        res = calc_importance_factor_gamma_n(consequence_class="C3", limit_state="ULS")
        assert res.primary_value == 1.15

    def test_gamma_n_sls(self) -> None:
        """Mọi cấp khi tính theo TTGH2 (SLS) -> gamma_n = 1.00."""
        res = calc_importance_factor_gamma_n(consequence_class="C3", limit_state="SLS")
        assert res.primary_value == 1.00

    def test_gamma_n_super_tall_building(self) -> None:
        """Nhà cao h=280m > 250m -> gamma_n >= 1.20."""
        res = calc_importance_factor_gamma_n(consequence_class="C2", limit_state="ULS", building_height=280.0)
        assert res.primary_value == 1.20

    def test_gamma_n_large_span(self) -> None:
        """Mái nhịp lớn L=130m > 120m -> gamma_n >= 1.20."""
        res = calc_importance_factor_gamma_n(consequence_class="C2", limit_state="ULS", span_length=130.0)
        assert res.primary_value == 1.20


class TestDeflectionAndDriftComplianceFacade:
    """Kiểm tra đánh giá điều kiện tuân thủ f <= [fu] qua Master Facade."""

    def test_compliance_ok(self) -> None:
        """Thực tế 20mm <= Giới hạn 30mm (Dầm L=6m) -> ĐẠT, tỷ lệ 66.7%."""
        res = check_deflection_and_drift_limits(
            actual_value_mm=20.0,
            check_type="vertical_deflection",
            params={"element_type": "roof_floor_visible", "span_L": 6.0},
        )
        assert res.is_compliant is True
        assert res.outputs["utilization_ratio"] == 0.667
        assert res.outputs["safety_margin_percent"] == 33.3

    def test_compliance_exceeded(self) -> None:
        """Thực tế 35mm > Giới hạn 30mm (Dầm L=6m) -> VƯỢT GIỚI HẠN."""
        res = check_deflection_and_drift_limits(
            actual_value_mm=35.0,
            check_type="vertical_deflection",
            params={"element_type": "roof_floor_visible", "span_L": 6.0},
        )
        assert res.is_compliant is False
        assert res.outputs["utilization_ratio"] == 1.167
        assert res.outputs["safety_margin_percent"] == -16.7

    def test_master_solver_facade_all_registered(self) -> None:
        """Kiểm tra gọi cả 4 solvers mới qua SymbolicFormulaSolver."""
        res_v = SymbolicFormulaSolver.solve("F_DEFLECTION_TCVN2737_G_VERT", {"span_L": 6.0})
        assert res_v.primary_value == 30.0

        res_h = SymbolicFormulaSolver.solve("F_DRIFT_TCVN2737_G_HORIZ", {"total_height_h": 50.0})
        assert res_h.primary_value == 100.0

        res_g = SymbolicFormulaSolver.solve("F_IMPORTANCE_TCVN2737_H_GAMMA_N", {"consequence_class": "C3"})
        assert res_g.primary_value == 1.15

        res_chk = SymbolicFormulaSolver.solve(
            "F_CHECK_DEFLECTION_DRIFT_COMPLIANCE",
            {"actual_value_mm": 20.0, "check_type": "vertical_deflection", "params": {"span_L": 6.0}},
        )
        assert res_chk.is_compliant is True
