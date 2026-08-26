"""
Unit tests for CCBA Deterministic Symbolic Formula Engine (ADR 0020).
"""

from __future__ import annotations

import pytest

from formulas import (
    SymbolicFormulaSolver,
    calc_atrium_smoke_exhaust_flow,
    calc_corridor_smoke_exhaust_flow,
    calc_f1_f4_outdoor_water_demand,
    calc_fire_water_tank_capacity,
    calc_sprinkler_density_and_spacing,
    calc_sprinkler_room_layout,
)


class TestPcccWaterDemand:
    """Kiểm tra độ chính xác tra cứu và tính toán lưu lượng nước theo QCVN 06:2022."""

    def test_apartment_mid_rise_table8(self) -> None:
        """Nhà chung cư F1.3, V = 18.000 m3, 9 tầng -> Bảng 8: 15 L/s."""
        res = calc_f1_f4_outdoor_water_demand(
            functional_group="F1.3",
            building_volume_m3=18000.0,
            floors_count=9,
        )
        assert res.primary_value == 15.0
        assert res.unit == "L/s"
        assert res.outputs["required_flow_l_per_s"] == 15.0
        assert res.outputs["required_flow_m3_per_h"] == 54.0
        assert "Bảng 8" in res.standard_reference

    def test_apartment_high_rise_large_volume_table8(self) -> None:
        """Nhà chung cư cao tầng F1.3, V = 65.000 m3, 28 tầng -> Bảng 8: 30 L/s."""
        res = calc_f1_f4_outdoor_water_demand(
            functional_group="F1.3",
            building_volume_m3=65000.0,
            floors_count=28,
        )
        assert res.primary_value == 30.0
        assert res.outputs["required_flow_m3_per_h"] == 108.0

    def test_public_building_table8(self) -> None:
        """Công trình công cộng F1.1 (bệnh viện), V = 30.000 m3, 14 tầng -> Bảng 8: 30 L/s."""
        res = calc_f1_f4_outdoor_water_demand(
            functional_group="F1.1",
            building_volume_m3=30000.0,
            floors_count=14,
        )
        assert res.primary_value == 30.0

    def test_rural_footnote_table8(self) -> None:
        """Nhà ở nông thôn <= 3 tầng, V = 800 m3 -> Ghi chú 1: 5 L/s."""
        res = calc_f1_f4_outdoor_water_demand(
            functional_group="F1.4",
            building_volume_m3=800.0,
            floors_count=2,
            is_rural=True,
        )
        assert res.primary_value == 5.0
        assert len(res.notes) > 0

    def test_fire_water_tank_capacity_calculation(self) -> None:
        """Dung tích bể nước: Ngoài 30 L/s (3h) + Trong 5 L/s (3h) + Sprinkler 30 L/s (1h)."""
        res = calc_fire_water_tank_capacity(
            outdoor_flow_l_per_s=30.0,
            duration_hours=3.0,
            indoor_flow_l_per_s=5.0,
            sprinkler_flow_l_per_s=30.0,
            sprinkler_duration_hours=1.0,
        )
        # 30 * 3.6 * 3 = 324 m3
        # 5 * 3.6 * 3 = 54 m3
        # 30 * 3.6 * 1 = 108 m3
        # Total = 486 m3
        assert res.primary_value == 486.0
        assert res.outputs["outdoor_volume_m3"] == 324.0
        assert res.outputs["indoor_volume_m3"] == 54.0
        assert res.outputs["sprinkler_volume_m3"] == 108.0
        assert len(res.steps) == 4


class TestSmokeExhaust:
    """Kiểm tra tính toán lưu lượng hút khói hành lang và sảnh thông tầng."""

    def test_corridor_smoke_exhaust(self) -> None:
        """Hành lang cửa rộng 1.2m, cao 2.2m, nhiệt độ 300°C."""
        res = calc_corridor_smoke_exhaust_flow(
            door_width_m=1.2,
            door_height_m=2.2,
            door_leaves_count=1,
            smoke_temp_celsius=300.0,
        )
        assert res.primary_value > 10000.0
        assert res.unit == "m³/h"
        assert res.outputs["smoke_density_kg_per_m3"] == pytest.approx(0.6159, rel=1e-3)
        assert len(res.steps) == 3
        # Format text report works cleanly
        report = res.format_text_report()
        assert "BÁO CÁO TÍNH TOÁN" in report

    def test_atrium_smoke_exhaust(self) -> None:
        """Sảnh thông tầng cao 18m, diện tích 400 m2."""
        res = calc_atrium_smoke_exhaust_flow(
            atrium_floor_area_m2=400.0,
            atrium_clear_height_m=18.0,
            smoke_layer_bottom_height_m=2.5,
            fire_heat_release_rate_kw=2500.0,
        )
        assert res.primary_value > 50000.0
        assert res.outputs["convective_heat_kw"] == 1750.0


class TestSprinklerSpacing:
    """Kiểm tra tính toán đầu phun Sprinkler TCVN 7336."""

    def test_sprinkler_density_ordinary_hazard_group_2(self) -> None:
        """Nhóm nguy cơ trung bình 2 -> cường độ 0.12, khoảng cách max 3.5m."""
        res = calc_sprinkler_density_and_spacing("NHOM_2_TRUNG_BINH_2")
        assert res.outputs["intensity_l_s_m2"] == 0.12
        assert res.outputs["max_head_spacing_m"] == 3.5
        assert res.outputs["max_wall_distance_m"] == 1.75
        assert res.outputs["max_coverage_area_m2"] == 9.0

    def test_sprinkler_room_layout(self) -> None:
        """Phòng 12m x 8m, nhóm 2.1 (spacing 4.0m, wall 2.0m)."""
        res = calc_sprinkler_room_layout(
            room_length_m=12.0,
            room_width_m=8.0,
            hazard_group="NHOM_2_TRUNG_BINH_1",
        )
        assert res.is_compliant is True
        assert res.outputs["total_heads"] >= 6
        assert res.outputs["area_per_head_m2"] <= 12.0


class TestSymbolicFormulaSolverFacade:
    """Kiểm tra Dispatcher và Facade của SymbolicFormulaSolver."""

    def test_list_formulas(self) -> None:
        formulas = SymbolicFormulaSolver.list_formulas()
        assert len(formulas) >= 6
        formula_ids = [f.formula_id for f in formulas]
        assert "F_QCVN06_TABLE8" in formula_ids
        assert "F_PCCC_TANK_CAPACITY" in formula_ids
        assert "F_SMOKE_EXHAUST_CORRIDOR" in formula_ids

    def test_solve_via_facade(self) -> None:
        res = SymbolicFormulaSolver.solve(
            "F_QCVN06_TABLE8",
            {
                "functional_group": "F1.3",
                "building_volume_m3": 22000.0,
                "floors_count": 10,
            },
        )
        assert res.primary_value == 15.0
        assert res.formula_id == "F_QCVN06_TABLE8"

    def test_invalid_formula_raises(self) -> None:
        with pytest.raises(KeyError):
            SymbolicFormulaSolver.solve("FORMULA_NON_EXISTENT", {})
