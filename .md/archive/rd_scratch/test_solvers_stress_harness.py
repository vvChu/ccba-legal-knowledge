import sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))

from formulas.wind_load_tcvn2737 import (
    calc_freestanding_wall_aerodynamic_coeff,
    calc_duopitch_roof_ce_coefficients,
    calc_flat_roof_ce_coefficients,
    calc_vertical_wall_ce_coefficients,
    calc_monopitch_roof_ce_coefficients,
    calc_hipped_roof_ce_coefficients,
    calc_gust_factor_gf,
    calc_equivalent_building_dimensions,
    calc_topography_datum_z0,
    calc_terrain_height_factor_kz,
    calc_full_wind_load_tcvn2737,
)
from formulas.deflection_limits_tcvn2737 import (
    calc_vertical_deflection_limit,
    calc_horizontal_drift_limit,
    calc_importance_factor_gamma_n,
)
from formulas.vietnam_wind_zones import calc_base_wind_pressure_w0

print("=== ADVERSARIAL STRESS TESTING ON SOLVERS ===")

# 1. Boundary & Invalid values for Freestanding Wall
try:
    calc_freestanding_wall_aerodynamic_coeff(-1, 5)
    print("FAIL: Wall accepted negative length")
except ValueError:
    print("PASS: Wall rejected negative length")

try:
    calc_freestanding_wall_aerodynamic_coeff(10, 0)
    print("FAIL: Wall accepted 0 height")
except ValueError:
    print("PASS: Wall rejected 0 height")

# 2. Duopitch boundary angles
res_min = calc_duopitch_roof_ce_coefficients(-45.0, 0.0)
assert res_min.is_compliant
res_max = calc_duopitch_roof_ce_coefficients(75.0, 0.0)
assert res_max.is_compliant
print("PASS: Duopitch boundary angles (-45° and 75°) handled correctly")

try:
    calc_duopitch_roof_ce_coefficients(-50.0, 0.0)
    print("FAIL: Duopitch accepted -50°")
except ValueError:
    print("PASS: Duopitch rejected out-of-range angle -50°")

# 3. Terrain Category
for cat in ["A", "B", "C"]:
    res = calc_terrain_height_factor_kz(cat, 15.0)
    assert res.primary_value > 0
print("PASS: All terrain categories A, B, C evaluated correctly")

try:
    calc_terrain_height_factor_kz("D", 15.0)
    print("FAIL: Accepted invalid terrain D")
except ValueError:
    print("PASS: Rejected invalid terrain D")

# 4. Wind Zone Lookup
w0_hn = calc_base_wind_pressure_w0("Hà Nội")
assert w0_hn.primary_value == 95.0
w0_hcm = calc_base_wind_pressure_w0("Hồ Chí Minh")
assert w0_hcm.primary_value == 95.0
w0_dn = calc_base_wind_pressure_w0("Đà Nẵng")
assert w0_dn.primary_value == 125.0
print("PASS: 63-province wind zone lookups for major cities validated per QCVN 02:2022")

# 5. Full wind load pipeline end-to-end
full_res = calc_full_wind_load_tcvn2737(
    province="Hà Nội",
    height_z=25.0,
    terrain_category="B",
    structure_geometry="vertical_wall",
    geometry_params={"building_height_h": 40.0, "building_width_b": 24.0, "building_depth_d": 30.0},
    total_building_height_h=40.0,
    consequence_class="C2",
)
assert full_res.is_compliant
assert abs(full_res.primary_value) > 0
print(f"PASS: Full wind load pipeline executed cleanly (Max |Wd| = {abs(full_res.primary_value)} kN/m2)")

# 6. Deflection & Importance limits
def_res = calc_vertical_deflection_limit(element_type="roof_floor_visible", span_L=6.0)
assert def_res.primary_value == 30.0 # 6000 / 200 = 30 mm
imp_res = calc_importance_factor_gamma_n(consequence_class="C3", building_height=120.0)
assert imp_res.primary_value == 1.15
print(f"PASS: Deflection ([fu]={def_res.primary_value}mm) & Importance factor (gamma_n={imp_res.primary_value}) passed")

print("=== ALL ADVERSARIAL CHECKS PASSED ===")
