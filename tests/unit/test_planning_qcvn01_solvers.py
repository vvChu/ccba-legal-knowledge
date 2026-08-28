"""
Unit tests for QCVN 01:2021/BXD Planning Solvers (ADR 0020 & ADR 0034).
"""

from __future__ import annotations

import pytest
from formulas.planning_qcvn01 import (
    calc_max_net_building_density,
    calc_min_environmental_safety_distance,
    calc_min_setback_distance,
)
from formulas.solver import SymbolicFormulaSolver


def test_calc_max_net_building_density_detached_house():
    # <= 50m2 -> 100%
    res50 = calc_max_net_building_density(land_area_m2=45.0, building_type="detached_house")
    assert res50.primary_value == 100.0

    # 75m2 -> 90%
    res75 = calc_max_net_building_density(land_area_m2=75.0, building_type="detached_house")
    assert res75.primary_value == 90.0

    # Midpoint between 75m2 (90%) and 100m2 (80%) = 87.5m2 -> 85%
    res87_5 = calc_max_net_building_density(land_area_m2=87.5, building_type="detached_house")
    assert pytest.approx(res87_5.primary_value, 0.01) == 85.0

    # 100m2 -> 80%
    res100 = calc_max_net_building_density(land_area_m2=100.0, building_type="detached_house")
    assert res100.primary_value == 80.0

    # 200m2 -> 70%
    res200 = calc_max_net_building_density(land_area_m2=200.0, building_type="detached_house")
    assert res200.primary_value == 70.0

    # >= 1000m2 -> 40%
    res1200 = calc_max_net_building_density(land_area_m2=1200.0, building_type="detached_house")
    assert res1200.primary_value == 40.0


def test_calc_max_net_building_density_apartment():
    # Height 15m (<= 16m), Area 2000m2 (<= 3000m2) -> 75%
    res_low_small = calc_max_net_building_density(
        land_area_m2=2000.0, building_height_m=15.0, building_type="residential_apartment"
    )
    assert res_low_small.primary_value == 75.0

    # Height 15m (<= 16m), Area 12000m2 (>= 10000m2) -> 60%
    res_low_large = calc_max_net_building_density(
        land_area_m2=12000.0, building_height_m=15.0, building_type="residential_apartment"
    )
    assert res_low_large.primary_value == 60.0

    # Height 15m, Area 6500m2 (midpoint 3000-10000) -> 75 - (15/7000)*3500 = 67.5%
    res_low_mid = calc_max_net_building_density(
        land_area_m2=6500.0, building_height_m=15.0, building_type="residential_apartment"
    )
    assert pytest.approx(res_low_mid.primary_value, 0.01) == 67.5

    # Height 50m (> 46m), Area 3000m2 -> 40%
    res_high_small = calc_max_net_building_density(
        land_area_m2=3000.0, building_height_m=50.0, building_type="residential_apartment"
    )
    assert res_high_small.primary_value == 40.0

    # Height 50m (> 46m), Area 10000m2 -> 25%
    res_high_large = calc_max_net_building_density(
        land_area_m2=10000.0, building_height_m=50.0, building_type="residential_apartment"
    )
    assert res_high_large.primary_value == 25.0

    # Compliance check
    res_pass = calc_max_net_building_density(
        land_area_m2=3000.0,
        building_height_m=50.0,
        building_type="residential_apartment",
        proposed_density_percent=38.0,
    )
    assert res_pass.is_compliant is True
    assert "ĐẠT" in res_pass.compliance_message

    res_fail = calc_max_net_building_density(
        land_area_m2=3000.0,
        building_height_m=50.0,
        building_type="residential_apartment",
        proposed_density_percent=45.0,
    )
    assert res_fail.is_compliant is False
    assert "KHÔNG ĐẠT" in res_fail.compliance_message


def test_calc_min_setback_distance():
    # Road < 19m
    assert calc_min_setback_distance(road_width_m=15.0, building_height_m=18.0).primary_value == 0.0
    assert calc_min_setback_distance(road_width_m=15.0, building_height_m=21.0).primary_value == 3.0
    assert calc_min_setback_distance(road_width_m=15.0, building_height_m=24.0).primary_value == 4.0
    assert calc_min_setback_distance(road_width_m=15.0, building_height_m=30.0).primary_value == 6.0

    # Road 19m - 22m
    assert calc_min_setback_distance(road_width_m=20.0, building_height_m=22.0).primary_value == 0.0
    assert calc_min_setback_distance(road_width_m=20.0, building_height_m=24.0).primary_value == 3.0
    assert calc_min_setback_distance(road_width_m=20.0, building_height_m=35.0).primary_value == 6.0

    # Road > 22m
    assert calc_min_setback_distance(road_width_m=25.0, building_height_m=25.0).primary_value == 0.0
    assert calc_min_setback_distance(road_width_m=25.0, building_height_m=27.0).primary_value == 3.0
    assert calc_min_setback_distance(road_width_m=25.0, building_height_m=30.0).primary_value == 6.0

    # Compliance test
    comp_ok = calc_min_setback_distance(road_width_m=15.0, building_height_m=30.0, proposed_setback_m=6.5)
    assert comp_ok.is_compliant is True

    comp_bad = calc_min_setback_distance(road_width_m=15.0, building_height_m=30.0, proposed_setback_m=5.0)
    assert comp_bad.is_compliant is False


def test_calc_min_environmental_safety_distance():
    res_transfer = calc_min_environmental_safety_distance("solid_waste_transfer_closed")
    assert res_transfer.primary_value == 20.0

    res_landfill = calc_min_environmental_safety_distance("solid_waste_landfill_sanitary")
    assert res_landfill.primary_value == 500.0

    res_crematorium = calc_min_environmental_safety_distance("crematorium")
    assert res_crematorium.primary_value == 100.0

    # Distance check
    dist_ok = calc_min_environmental_safety_distance("crematorium", actual_distance_m=150.0)
    assert dist_ok.is_compliant is True

    dist_violation = calc_min_environmental_safety_distance("crematorium", actual_distance_m=80.0)
    assert dist_violation.is_compliant is False


def test_symbolic_formula_solver_facade_planning_registration():
    meta_density = SymbolicFormulaSolver.get_metadata("F_PLANNING_QCVN01_NET_DENSITY")
    assert meta_density is not None
    assert "Mật độ" in meta_density.name

    meta_setback = SymbolicFormulaSolver.get_metadata("F_PLANNING_QCVN01_SETBACK")
    assert meta_setback is not None
    assert "Khoảng lùi" in meta_setback.name

    meta_atmt = SymbolicFormulaSolver.get_metadata("F_PLANNING_QCVN01_ATMT")
    assert meta_atmt is not None
    assert "Môi trường" in meta_atmt.name or "ATMT" in meta_atmt.name

    meta_parking = SymbolicFormulaSolver.get_metadata("F_PLANNING_QCVN01_PARKING")
    assert meta_parking is not None
    assert "Đỗ Xe" in meta_parking.name

    meta_chamfer = SymbolicFormulaSolver.get_metadata("F_PLANNING_QCVN01_CORNER_CHAMFER")
    assert meta_chamfer is not None
    assert "Vát góc" in meta_chamfer.name

    meta_greenery = SymbolicFormulaSolver.get_metadata("F_PLANNING_QCVN01_GREENERY")
    assert meta_greenery is not None
    assert "Cây xanh" in meta_greenery.name


def test_calc_min_parking_spaces():
    from formulas.planning_qcvn01 import calc_min_parking_spaces

    # 1. Commercial apartment: 100 units -> 100 cars, 200 motorbikes
    res_apt = calc_min_parking_spaces(
        building_type="apartment_commercial",
        num_apartments=100,
        proposed_car_spaces=110,
        proposed_motorbike_spaces=220,
    )
    assert res_apt.outputs["min_car_spaces"] == 100
    assert res_apt.outputs["min_motorbike_spaces"] == 200
    assert res_apt.is_compliant is True

    # 2. Social apartment: 100 units -> 50 cars, 200 motorbikes
    res_soc = calc_min_parking_spaces(
        building_type="apartment_social",
        num_apartments=100,
        proposed_car_spaces=40,
        proposed_motorbike_spaces=200,
    )
    assert res_soc.outputs["min_car_spaces"] == 50
    assert res_soc.is_compliant is False
    assert "THIẾU" in res_soc.compliance_message

    # 3. Office: 2500m2 floor area -> 25 cars, 83 motorbikes
    res_off = calc_min_parking_spaces(
        building_type="office",
        floor_area_m2=2500.0,
    )
    assert res_off.outputs["min_car_spaces"] == 25
    assert res_off.outputs["min_motorbike_spaces"] == 83

    # 4. Shopping center: 5000m2 -> 50 cars, 250 motorbikes
    res_mall = calc_min_parking_spaces(
        building_type="commercial",
        floor_area_m2=5000.0,
    )
    assert res_mall.outputs["min_car_spaces"] == 50
    assert res_mall.outputs["min_motorbike_spaces"] == 250

    # 5. Hotel 5 stars: 200 rooms -> 50 cars, 20 motorbikes
    res_hotel = calc_min_parking_spaces(
        building_type="hotel",
        num_hotel_rooms=200,
        hotel_stars=5,
    )
    assert res_hotel.outputs["min_car_spaces"] == 50
    assert res_hotel.outputs["min_motorbike_spaces"] == 20


def test_calc_corner_chamfer_dimensions():
    from formulas.planning_qcvn01 import calc_corner_chamfer_dimensions

    # 1. Acute angle: 45 deg, Road widths: 20m & 15m -> 6m
    res_acute = calc_corner_chamfer_dimensions(
        intersection_angle_deg=45.0,
        road_width_1_m=20.0,
        road_width_2_m=15.0,
    )
    assert res_acute.outputs["min_chamfer_m"] == 6.0
    assert res_acute.outputs["triangle_area_m2"] > 0

    # 2. Right angle: 90 deg, Road widths: 20m & 20m -> 5m
    res_right_wide = calc_corner_chamfer_dimensions(
        intersection_angle_deg=90.0,
        road_width_1_m=20.0,
        road_width_2_m=20.0,
    )
    assert res_right_wide.outputs["min_chamfer_m"] == 5.0
    assert res_right_wide.outputs["triangle_area_m2"] == 12.5

    # 3. Right angle: 90 deg, Road widths: 8m & 8m -> 3m
    res_right_narrow = calc_corner_chamfer_dimensions(
        intersection_angle_deg=90.0,
        road_width_1_m=8.0,
        road_width_2_m=8.0,
    )
    assert res_right_narrow.outputs["min_chamfer_m"] == 3.0

    # 4. Obtuse angle: 120 deg -> 3m
    res_obtuse = calc_corner_chamfer_dimensions(
        intersection_angle_deg=120.0,
        road_width_1_m=15.0,
        road_width_2_m=15.0,
    )
    assert res_obtuse.outputs["min_chamfer_m"] == 3.0

    # 5. Very obtuse angle: 150 deg -> 0m
    res_flat = calc_corner_chamfer_dimensions(
        intersection_angle_deg=150.0,
        road_width_1_m=15.0,
        road_width_2_m=15.0,
    )
    assert res_flat.outputs["min_chamfer_m"] == 0.0


def test_calc_urban_greenery_requirement():
    from formulas.planning_qcvn01 import calc_urban_greenery_requirement

    # Grade 1 urban area: 100,000 population -> 700,000 m2 (70 ha)
    res_g1 = calc_urban_greenery_requirement(
        urban_grade="grade_1",
        population=100000,
        proposed_greenery_area_m2=750000.0,
    )
    assert res_g1.outputs["min_total_greenery_m2"] == 700000.0
    assert res_g1.outputs["min_residential_greenery_m2"] == 500000.0
    assert res_g1.is_compliant is True

    # Grade 4 urban area: 50,000 population -> 300,000 m2 (30 ha)
    res_g4 = calc_urban_greenery_requirement(
        urban_grade="grade_4",
        population=50000,
        proposed_greenery_area_m2=250000.0,
    )
    assert res_g4.outputs["min_total_greenery_m2"] == 300000.0
    assert res_g4.is_compliant is False
    assert "KHÔNG ĐẠT" in res_g4.compliance_message

