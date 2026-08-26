"""
CCBA Legal Knowledge — Deterministic Symbolic Formula Engine.
Thư viện các công thức tính toán kỹ thuật xác định theo QCVN 06 & TCVN (ADR 0020).
"""

from formulas.models import CalculationResult, CalculationStep, FormulaMetadata
from formulas.pccc_water_demand import (
    calc_f1_f4_outdoor_water_demand,
    calc_fire_water_tank_capacity,
)
from formulas.smoke_exhaust import (
    calc_atrium_smoke_exhaust_flow,
    calc_corridor_smoke_exhaust_flow,
)
from formulas.solver import SymbolicFormulaSolver
from formulas.sprinkler_spacing import (
    calc_sprinkler_density_and_spacing,
    calc_sprinkler_room_layout,
)
from formulas.visual_card_engine import (
    GeometricZoneResult,
    VisualCardEngine,
    VisualCardEvaluation,
)
from formulas.deflection_limits_tcvn2737 import (
    calc_horizontal_drift_limit,
    calc_importance_factor_gamma_n,
    calc_physiological_deflection_limit_fu,
    calc_vertical_deflection_limit,
    check_deflection_and_drift_limits,
)
from formulas.vietnam_wind_zones import (
    calc_base_wind_pressure_w0,
)
from formulas.wind_load_tcvn2737 import (
    calc_duopitch_roof_ce_coefficients,
    calc_equivalent_building_dimensions,
    calc_flat_roof_ce_coefficients,
    calc_freestanding_wall_aerodynamic_coeff,
    calc_full_wind_load_tcvn2737,
    calc_gust_factor_gf,
    calc_hipped_roof_ce_coefficients,
    calc_monopitch_roof_ce_coefficients,
    calc_terrain_height_factor_kz,
    calc_topography_datum_z0,
    calc_vertical_wall_ce_coefficients,
)

__all__ = [
    "CalculationResult",
    "CalculationStep",
    "FormulaMetadata",
    "SymbolicFormulaSolver",
    "VisualCardEngine",
    "VisualCardEvaluation",
    "GeometricZoneResult",
    "calc_f1_f4_outdoor_water_demand",
    "calc_fire_water_tank_capacity",
    "calc_corridor_smoke_exhaust_flow",
    "calc_atrium_smoke_exhaust_flow",
    "calc_sprinkler_density_and_spacing",
    "calc_sprinkler_room_layout",
    "calc_freestanding_wall_aerodynamic_coeff",
    "calc_duopitch_roof_ce_coefficients",
    "calc_flat_roof_ce_coefficients",
    "calc_monopitch_roof_ce_coefficients",
    "calc_vertical_wall_ce_coefficients",
    "calc_hipped_roof_ce_coefficients",
    "calc_gust_factor_gf",
    "calc_equivalent_building_dimensions",
    "calc_topography_datum_z0",
    "calc_terrain_height_factor_kz",
    "calc_base_wind_pressure_w0",
    "calc_vertical_deflection_limit",
    "calc_physiological_deflection_limit_fu",
    "calc_horizontal_drift_limit",
    "calc_importance_factor_gamma_n",
    "check_deflection_and_drift_limits",
    "calc_full_wind_load_tcvn2737",
]
