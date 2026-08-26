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
from formulas.wind_load_tcvn2737 import (
    calc_duopitch_roof_ce_coefficients,
    calc_flat_roof_ce_coefficients,
    calc_freestanding_wall_aerodynamic_coeff,
    calc_hipped_roof_ce_coefficients,
    calc_monopitch_roof_ce_coefficients,
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
]
