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
