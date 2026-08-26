"""
Unit tests for End-to-End Wind Load Pipeline Solver (Chương 10 TCVN 2737:2023).
Kiểm chứng chuỗi tính toán toàn trình tích hợp W0, k(z), c_e, G_f, gamma_n, gamma_f (ADR 0020 & ADR 0034).
"""

from __future__ import annotations

import pytest

from formulas import (
    SymbolicFormulaSolver,
    calc_full_wind_load_tcvn2737,
)


class TestFullWindLoadPipeline:
    """Kiểm tra tích hợp toàn trình tải trọng gió TCVN 2737:2023."""

    def test_hanoi_tall_building_concrete_vertical_wall(self) -> None:
        """Nhà cao tầng BTCT h=60m tại Hà Nội (Vùng II, W0=95 daN/m2), địa hình B, T1=1.5s."""
        res = calc_full_wind_load_tcvn2737(
            province="Hà Nội",
            height_z=30.0,
            terrain_category="B",
            structure_geometry="vertical_wall",
            geometry_params={"building_height_h": 60.0, "building_width_b": 20.0, "building_depth_d": 30.0},
            structure_type="concrete",
            total_building_height_h=60.0,
            period_T1=1.5,
            consequence_class="C2",
        )

        assert res.outputs["W0_daN_m2"] == 95.0
        assert res.outputs["W3s_10_daN_m2"] == 80.94
        assert res.outputs["G_f"] == 0.85
        assert res.outputs["gamma_n"] == 1.0
        assert res.outputs["gamma_f"] == 2.1
        assert 1.38 <= res.outputs["k_z"] <= 1.40

        zones = res.outputs["zones"]
        assert "Vùng D (Tường đón gió)" in zones
        assert "Vùng E (Tường hút gió)" in zones
        assert zones["Vùng D (Tường đón gió)"]["c_e"] == 0.8
        assert zones["Vùng D (Tường đón gió)"]["W_d_kNm2"] > 1.5
        assert zones["Vùng E (Tường hút gió)"]["W_d_kNm2"] < 0.0

    def test_danang_industrial_warehouse_duopitch(self) -> None:
        """Nhà xưởng công nghiệp tại Đà Nẵng (Vùng III, W0=125 daN/m2), địa hình A, mái dốc đôi alpha=15 độ."""
        res = calc_full_wind_load_tcvn2737(
            province="Đà Nẵng",
            height_z=8.0,
            terrain_category="A",
            structure_geometry="duopitch_roof",
            geometry_params={"pitch_angle_deg": 15.0, "wind_direction_deg": 0.0},
            structure_type="steel",
            total_building_height_h=10.0,
            period_T1=0.6,
            consequence_class="C2",
        )

        assert res.outputs["W0_daN_m2"] == 125.0
        assert res.outputs["W3s_10_daN_m2"] == 106.5
        assert res.outputs["G_f"] == 0.85

        zones = res.outputs["zones"]
        assert "Vùng F" in zones or any("F" in z for z in zones)
        assert "Vùng H" in zones or any("H" in z for z in zones)

    def test_haiphong_bachlongvi_island_high_consequence(self) -> None:
        """Đảo Bạch Long Vĩ (Vùng V, W0=185 daN/m2), cấp hậu quả C3 (gamma_n=1.15)."""
        res = calc_full_wind_load_tcvn2737(
            province="Hải Phòng",
            district="Bạch Long Vĩ",
            height_z=10.0,
            terrain_category="A",
            structure_geometry="custom",
            geometry_params={"c_e": 0.8},
            consequence_class="C3",
        )

        assert res.outputs["W0_daN_m2"] == 185.0
        assert res.outputs["W3s_10_daN_m2"] == 157.62
        assert res.outputs["gamma_n"] == 1.15
        assert res.outputs["k_z"] == 0.86
        assert res.outputs["primary_Wd_kNm2"] > 2.0

    def test_sloping_terrain_datum_offset(self) -> None:
        """Địa hình dốc i=1.0, H=17m -> z0=10m -> tại z=20m có z_e=10m."""
        res = calc_full_wind_load_tcvn2737(
            province="Hồ Chí Minh",
            height_z=20.0,
            terrain_category="B",
            slope_i=1.0,
            height_H_slope=17.0,
            structure_geometry="custom",
            geometry_params={"c_e": 0.8},
        )

        assert res.outputs["z_e_m"] == 10.0
        assert res.outputs["k_z"] == 1.00

    def test_master_solver_facade_integration(self) -> None:
        """Kiểm tra gọi qua Master Solver Facade."""
        res = SymbolicFormulaSolver.solve(
            "F_WIND_TCVN2737_FULL_PIPELINE",
            {
                "province": "Hà Nội",
                "height_z": 10.0,
                "terrain_category": "B",
                "structure_geometry": "custom",
                "geometry_params": {"c_e": 0.8},
            },
        )
        assert res.outputs["W0_daN_m2"] == 95.0
        assert res.primary_value > 0.0

    def test_flat_roof_parapet_building(self) -> None:
        """Mái phẳng có tường chắn mái parapet hp=1.0m."""
        res = calc_full_wind_load_tcvn2737(
            province="Hà Nội",
            height_z=20.0,
            terrain_category="B",
            structure_geometry="flat_roof",
            geometry_params={"edge_type": "parapet", "parapet_height_hp": 1.0, "building_height_h": 20.0, "building_depth_d": 30.0},
        )
        assert "zones" in res.outputs
        assert len(res.outputs["zones"]) > 0

    def test_monopitch_roof_building(self) -> None:
        """Mái dốc một phía alpha=15 độ tại Cần Thơ (Vùng II, W0=95 daN/m2)."""
        res = calc_full_wind_load_tcvn2737(
            province="Cần Thơ",
            height_z=12.0,
            terrain_category="B",
            structure_geometry="monopitch_roof",
            geometry_params={"pitch_angle_alpha": 15.0, "wind_angle_theta": 0.0},
        )
        assert res.outputs["W0_daN_m2"] == 95.0
        assert len(res.outputs["zones"]) > 0

    def test_hipped_roof_building(self) -> None:
        """Mái 4 mái (hipped roof) alpha=25 độ."""
        res = calc_full_wind_load_tcvn2737(
            province="Quảng Ninh",
            height_z=15.0,
            terrain_category="A",
            structure_geometry="hipped_roof",
            geometry_params={"pitch_angle_alpha": 25.0, "wind_angle_theta": 0.0},
        )
        assert len(res.outputs["zones"]) > 0

    def test_freestanding_wall_fence(self) -> None:
        """Tường phẳng độc lập / hàng rào dài L=30m, cao h=3m."""
        res = calc_full_wind_load_tcvn2737(
            province="Hà Nội",
            height_z=3.0,
            terrain_category="B",
            structure_geometry="freestanding_wall",
            geometry_params={"length_L": 30.0, "height_h": 3.0},
        )
        assert len(res.outputs["zones"]) > 0

    def test_supertall_building_gamma_n_trigger(self) -> None:
        """Công trình siêu cao h=280m (>250m) kích hoạt gamma_n >= 1.20."""
        res = calc_full_wind_load_tcvn2737(
            province="Hồ Chí Minh",
            height_z=280.0,
            terrain_category="B",
            structure_type="concrete",
            total_building_height_h=280.0,
            period_T1=3.5,
            consequence_class="C3",
            structure_geometry="custom",
            geometry_params={"c_e": 0.8},
        )
        assert res.outputs["gamma_n"] >= 1.20

    def test_steel_tall_building_gust_factor(self) -> None:
        """Nhà khung thép h=80m, T1=2.0s kích hoạt Phụ lục E.1 cho kết cấu thép."""
        res = calc_full_wind_load_tcvn2737(
            province="Hà Nội",
            height_z=80.0,
            terrain_category="B",
            structure_type="steel",
            total_building_height_h=80.0,
            period_T1=2.0,
            structure_geometry="custom",
            geometry_params={"c_e": 0.8},
        )
        # Steel Gf = 0.85 + 80/800 = 0.85 + 0.10 = 0.95
        assert res.outputs["G_f"] == 0.95

