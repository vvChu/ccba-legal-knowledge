"""
CCBA Legal Knowledge — Master Symbolic Formula Solver Engine.
Động cơ điều phối và giải toán kỹ thuật xác định (ADR 0020).
"""

from __future__ import annotations

from typing import Any, Callable

from formulas.models import CalculationResult, FormulaMetadata
from formulas.pccc_water_demand import (
    calc_f1_f4_outdoor_water_demand,
    calc_fire_water_tank_capacity,
)
from formulas.smoke_exhaust import (
    calc_atrium_smoke_exhaust_flow,
    calc_corridor_smoke_exhaust_flow,
)
from formulas.sprinkler_spacing import (
    calc_sprinkler_density_and_spacing,
    calc_sprinkler_room_layout,
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
from formulas.planning_qcvn01 import (
    calc_corner_chamfer_dimensions,
    calc_max_net_building_density,
    calc_min_environmental_safety_distance,
    calc_min_parking_spaces,
    calc_min_setback_distance,
    calc_urban_greenery_requirement,
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


class SymbolicFormulaSolver:
    """Master Solver Facade điều phối các hàm tính toán kỹ thuật theo chuẩn quy định."""

    _REGISTRY: dict[str, tuple[Callable[..., CalculationResult], FormulaMetadata]] = {}

    @classmethod
    def register(cls, metadata: FormulaMetadata, func: Callable[..., CalculationResult]) -> None:
        """Đăng ký công thức mới vào hệ thống."""
        cls._REGISTRY[metadata.formula_id] = (func, metadata)

    @classmethod
    def get_metadata(cls, formula_id: str) -> FormulaMetadata | None:
        """Lấy siêu dữ liệu công thức."""
        entry = cls._REGISTRY.get(formula_id)
        return entry[1] if entry else None

    @classmethod
    def list_formulas(cls) -> list[FormulaMetadata]:
        """Liệt kê toàn bộ các công thức hiện có trong hệ thống."""
        return [entry[1] for entry in cls._REGISTRY.values()]

    @classmethod
    def solve(cls, formula_id: str, params: dict[str, Any]) -> CalculationResult:
        """Thực thi tính toán xác định cho một công thức cụ thể."""
        if formula_id not in cls._REGISTRY:
            available = ", ".join(cls._REGISTRY.keys())
            raise KeyError(
                f"Không tìm thấy công thức '{formula_id}'. Các công thức sẵn có: {available}"
            )

        func, _ = cls._REGISTRY[formula_id]
        try:
            return func(**params)
        except TypeError as e:
            raise ValueError(
                f"Lỗi tham số khi gọi công thức '{formula_id}': {e}. Vui lòng kiểm tra lại tham số đầu vào."
            ) from e


# ---------------------------------------------------------------------------
# Đăng ký các công thức mặc định
# ---------------------------------------------------------------------------

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_QCVN06_TABLE8",
        name="Lưu lượng nước chữa cháy ngoài nhà (F1-F4)",
        category="PCCC_WATER",
        standard_reference="Mục 5.1.2.2 & Bảng 8 QCVN 06:2022/BXD",
        description="Tra cứu và tính toán lưu lượng nước cấp ngoài nhà cho công trình nhóm F1 đến F4.",
        parameters={
            "functional_group": "Nhóm công năng (F1.3, F1.4, F1.1, F1.2, F2, F3, F4)",
            "building_volume_m3": "Khối tích công trình (m³)",
            "floors_count": "Số tầng công trình",
            "is_rural": "bool: Nông thôn làng/xã (mặc định False)",
        },
    ),
    calc_f1_f4_outdoor_water_demand,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_PCCC_TANK_CAPACITY",
        name="Dung tích bể chứa nước chữa cháy",
        category="PCCC_WATER",
        standard_reference="Mục 5.1.4 QCVN 06:2022/BXD & TCVN 7336:2021",
        description="Tính toán dung tích bể nước chữa cháy ngầm dự trữ cho hệ thống ngoài nhà, trong nhà và Sprinkler.",
        parameters={
            "outdoor_flow_l_per_s": "Lưu lượng chữa cháy ngoài nhà (L/s)",
            "duration_hours": "Thời gian chữa cháy ngoài nhà (giờ, mặc định 3.0)",
            "indoor_flow_l_per_s": "Lưu lượng họng nước trong nhà (L/s, mặc định 0.0)",
            "sprinkler_flow_l_per_s": "Lưu lượng Sprinkler (L/s, mặc định 0.0)",
            "sprinkler_duration_hours": "Thời gian Sprinkler (giờ, mặc định 1.0)",
        },
    ),
    calc_fire_water_tank_capacity,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_SMOKE_EXHAUST_CORRIDOR",
        name="Lưu lượng hút khói hành lang khi có cháy",
        category="SMOKE_EXHAUST",
        standard_reference="Phụ lục D (Mục D.3, D.8, D.9) QCVN 06:2022/BXD",
        description="Tính toán lưu lượng quạt hút khói bảo vệ hành lang thoát nạn.",
        parameters={
            "door_width_m": "Chiều rộng cánh cửa thoát nạn (m)",
            "door_height_m": "Chiều cao cửa thoát nạn (m)",
            "door_leaves_count": "Số cánh cửa (mặc định 1)",
            "door_opening_factor": "Hệ số mở cửa (mặc định 1.0)",
            "smoke_temp_celsius": "Nhiệt độ khói tính toán (°C, mặc định 300)",
            "safety_margin_factor": "Hệ số an toàn (mặc định 1.1)",
        },
    ),
    calc_corridor_smoke_exhaust_flow,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_SMOKE_EXHAUST_ATRIUM",
        name="Lưu lượng hút khói sảnh thông tầng (Atrium)",
        category="SMOKE_EXHAUST",
        standard_reference="Phụ lục D (Mục D.4) QCVN 06:2022/BXD",
        description="Tính toán lưu lượng hút khói cho không gian sảnh thông tầng lớn.",
        parameters={
            "atrium_floor_area_m2": "Diện tích sàn sảnh (m²)",
            "atrium_clear_height_m": "Chiều cao thông tầng (m)",
            "smoke_layer_bottom_height_m": "Cao độ đáy lớp khói an toàn (m, mặc định 2.5)",
            "fire_heat_release_rate_kw": "Công suất nhiệt đám cháy thiết kế (kW, mặc định 2500)",
        },
    ),
    calc_atrium_smoke_exhaust_flow,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_SPRINKLER_SPACING_TCVN7336",
        name="Khoảng cách & Lưu lượng đầu phun Sprinkler",
        category="SPRINKLER",
        standard_reference="Bảng 1, Bảng 2 TCVN 7336:2021",
        description="Tra cứu cường độ phun, khoảng cách và diện tích bảo vệ của đầu phun Sprinkler.",
        parameters={
            "hazard_group": "Nhóm nguy cơ cháy (NHOM_1_THAP, NHOM_2_TRUNG_BINH_1, NHOM_2_TRUNG_BINH_2, NHOM_3_CAO)",
            "sprinkler_k_factor": "Hệ số K của đầu phun (mặc định 80.0)",
            "min_pressure_bar": "Áp suất tối thiểu (bar, mặc định 1.0)",
        },
    ),
    calc_sprinkler_density_and_spacing,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_SPRINKLER_ROOM_LAYOUT",
        name="Bố trí mạng lưới đầu phun Sprinkler cho gian phòng",
        category="SPRINKLER",
        standard_reference="TCVN 7336:2021",
        description="Tính toán số lượng và khoảng cách bố trí lưới đầu phun Sprinkler cho gian phòng.",
        parameters={
            "room_length_m": "Chiều dài phòng (m)",
            "room_width_m": "Chiều rộng phòng (m)",
            "hazard_group": "Nhóm nguy cơ cháy (mặc định NHOM_2_TRUNG_BINH_1)",
        },
    ),
    calc_sprinkler_room_layout,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_F1_WALL",
        name="Hệ số khí động c_x cho tường phẳng độc lập và hàng rào",
        category="WIND_LOAD",
        standard_reference="Mục F.1.1, Hình F.1 & Bảng F.1 Phụ lục F TCVN 2737:2023",
        description="Tra cứu và nội suy hệ số cản c_x cho các vùng A, B, C, D trên tường phẳng độc lập.",
        parameters={
            "length_L": "Chiều dài tường L (m)",
            "height_h": "Chiều cao tường h (m)",
            "solidity_ratio_phi": "Hệ số đặc phi (mặc định 1.0)",
            "has_return_corner": "bool: Có bẻ góc (mặc định False)",
            "return_corner_length": "Chiều dài bẻ góc l_ret (m, mặc định 0.0)",
        },
    ),
    calc_freestanding_wall_aerodynamic_coeff,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_F6_DUOPITCH",
        name="Hệ số khí động c_e cho mái dốc hai phía",
        category="WIND_LOAD",
        standard_reference="Mục F.4.2, Hình F.6, Bảng F.5a & Bảng F.5b TCVN 2737:2023",
        description="Tính toán hệ số c_e cho các vùng F, G, H, I, J và phân tách kịch bản áp lực hút/đẩy.",
        parameters={
            "pitch_angle_alpha": "Góc dốc mái alpha (-45 đến 75 độ)",
            "wind_angle_theta": "Góc hướng gió theta (0 hoặc 90 độ, mặc định 0)",
            "building_width_b": "Chiều rộng đón gió b (m, tùy chọn)",
            "building_height_h": "Chiều cao đỉnh mái h (m, tùy chọn)",
            "building_depth_d": "Chiều sâu dọc gió d (m, tùy chọn)",
        },
    ),
    calc_duopitch_roof_ce_coefficients,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_F3_FLAT",
        name="Hệ số khí động c_e cho mái bằng",
        category="WIND_LOAD",
        standard_reference="Mục F.2, Hình F.3 & Bảng F.2 TCVN 2737:2023",
        description="Tính toán hệ số c_e cho mái bằng có cạnh sắc, tường chắn mái hoặc bo tròn.",
        parameters={
            "eaves_type": "Loại mép mái ('CANH_SAC', 'TUONG_CHAN_MAI', 'BO_TRON', 'VAT_GOC')",
            "parapet_height_hp": "Chiều cao tường chắn mái hp (m, tùy chọn)",
            "radius_r": "Bán kính bo tròn r (m, tùy chọn)",
            "building_height_h": "Chiều cao công trình h (m)",
            "building_width_b": "Chiều rộng đón gió b (m, tùy chọn)",
        },
    ),
    calc_flat_roof_ce_coefficients,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_F4_MONOPITCH",
        name="Hệ số khí động c_e cho mái dốc một phía",
        category="WIND_LOAD",
        standard_reference="Mục F.3, Hình F.4, Bảng F.3a & Bảng F.3b TCVN 2737:2023",
        description="Tính toán hệ số c_e cho mái dốc 1 phía khi gió thổi 0°, 90° hoặc 180°.",
        parameters={
            "pitch_angle_alpha": "Góc dốc mái alpha (5 đến 75 độ)",
            "wind_angle_theta": "Góc hướng gió theta (0, 90 hoặc 180 độ, mặc định 0)",
            "building_width_b": "Chiều rộng đón gió b (m, tùy chọn)",
            "building_height_h": "Chiều cao đỉnh mái h (m, tùy chọn)",
            "building_depth_d": "Chiều sâu dọc gió d (m, tùy chọn)",
        },
    ),
    calc_monopitch_roof_ce_coefficients,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_F5A_WALLS",
        name="Hệ số khí động c_e cho tường thẳng đứng của nhà chữ nhật",
        category="WIND_LOAD",
        standard_reference="Mục F.4.1, Hình F.5a & Bảng F.4 TCVN 2737:2023",
        description="Tính toán hệ số c_e cho các vùng A, B, C (tường bên), D (đón gió), E (hút gió).",
        parameters={
            "building_height_h": "Chiều cao công trình h (m)",
            "building_depth_d": "Chiều sâu dọc hướng gió d (m)",
            "building_width_b": "Chiều rộng đón gió b (m, tùy chọn)",
        },
    ),
    calc_vertical_wall_ce_coefficients,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_F7_HIPPED",
        name="Hệ số khí động c_e cho mái dốc bốn phía",
        category="WIND_LOAD",
        standard_reference="Mục F.5, Hình F.7 & Bảng F.6 TCVN 2737:2023",
        description="Tính toán hệ số c_e cho 9 vùng F đến N trên mái dốc bốn phía (mái hông).",
        parameters={
            "pitch_angle_alpha": "Góc dốc mái alpha (5 đến 75 độ)",
            "wind_angle_theta": "Góc hướng gió theta (0 hoặc 90 độ, mặc định 0)",
            "building_width_b": "Chiều rộng đón gió b (m, tùy chọn)",
            "building_height_h": "Chiều cao đỉnh mái h (m, tùy chọn)",
            "building_depth_d": "Chiều sâu dọc gió d (m, tùy chọn)",
        },
    ),
    calc_hipped_roof_ce_coefficients,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_E_GUST_FACTOR",
        name="Hệ số hiệu ứng giật G_f theo công thức đơn giản",
        category="WIND_LOAD",
        standard_reference="Mục E.1, Công thức E.1 & E.2 Phụ lục E TCVN 2737:2023",
        description="Tính toán hệ số hiệu ứng giật G_f cho nhà cao tầng BTCT (E.1) và nhà thép (E.2) có h <= 150m, T1 > 1s.",
        parameters={
            "structure_type": "Loại kết cấu ('concrete' / 'be_tong_cot_thep' hoặc 'steel' / 'thep')",
            "height_h": "Chiều cao công trình h (m)",
            "period_T1": "Chu kỳ dao động riêng thứ nhất T1 (s, mặc định 1.2s)",
        },
    ),
    calc_gust_factor_gf,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_E_EQUIV_DIM",
        name="Kích thước tương đương cho mặt bằng phức tạp",
        category="WIND_LOAD",
        standard_reference="Mục E.2, Hình E.1 Phụ lục E TCVN 2737:2023",
        description="Quy đổi kích thước tương đương (d, b) cho mặt bằng chữ U, X, Y đôi, Y đơn, L, Z.",
        parameters={
            "shape": "Dạng mặt bằng ('U', 'X', 'Y_DOUBLE', 'Y_SINGLE', 'L', 'Z')",
            "b": "Bề rộng đón gió tổng thể của hình chữ nhật ngoại tiếp (m)",
            "d": "Chiều sâu tổng thể dọc hướng gió cho dạng U, X (m, mặc định 0.0)",
            "d1": "Chiều sâu nhánh 1 cho dạng L, Z (m, mặc định 0.0)",
            "d2": "Chiều sâu nhánh 2 cho dạng L, Z (m, mặc định 0.0)",
        },
    ),
    calc_equivalent_building_dimensions,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_C_DATUM",
        name="Mặt cao độ quy ước z0 (mốc chuẩn khí động học)",
        category="WIND_LOAD",
        standard_reference="Mục C.1, Hình C.1 Phụ lục C TCVN 2737:2023",
        description="Xác định mốc chuẩn quy ước z0 theo độ dốc địa hình i (i <= 0.3, 0.3 < i < 2, i >= 2).",
        parameters={
            "slope_i": "Độ dốc địa hình i (i = tan theta hoặc H/L)",
            "height_H": "Chiều cao chênh lệch địa hình H (m, mặc định 10.0)",
            "zone": "Vị trí xét ('left_A', 'AB', 'BC', 'CD', 'right_D', mặc định 'BC')",
            "x_pos": "Vị trí tương đối trên đoạn nội suy (m, mặc định 0.0)",
            "z1": "Cao độ đỉnh dốc (m, mặc định 0.0)",
            "z2": "Cao độ chân dốc (m, mặc định 0.0)",
        },
    ),
    calc_topography_datum_z0,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_D_KZ",
        name="Hệ số độ cao k(z) theo dạng địa hình",
        category="WIND_LOAD",
        standard_reference="Mục 10.2.4, Bảng 8 & Bảng 9 TCVN 2737:2023",
        description="Tính toán hệ số k(z) theo độ cao z cho 3 dạng địa hình A, B, C.",
        parameters={
            "terrain_category": "Dạng địa hình ('A', 'B' hoặc 'C')",
            "height_z": "Chiều cao điểm tính toán so với mốc chuẩn (m)",
        },
    ),
    calc_terrain_height_factor_kz,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_QCVN02_W0_LOOKUP",
        name="Tra cứu áp lực gió cơ sở W0 theo địa danh hành chính",
        category="WIND_LOAD",
        standard_reference="Bảng 5.1 QCVN 02:2022/BXD & Bảng 7 TCVN 2737:2023",
        description="Tra cứu phân vùng áp lực gió W0, V3s,50, V10m,50 cho 63 tỉnh/thành phố và quận/huyện/xã.",
        parameters={
            "province": "Tên tỉnh hoặc thành phố (ví dụ: 'Hà Nội', 'Hồ Chí Minh')",
            "district": "Tên quận, huyện, thị xã (tùy chọn)",
            "commune": "Tên xã, phường, thị trấn (tùy chọn)",
        },
    ),
    calc_base_wind_pressure_w0,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_DEFLECTION_TCVN2737_G_VERT",
        name="Độ võng đứng giới hạn [fu] cho dầm, sàn, giàn",
        category="DEFLECTION_AND_DRIFT",
        standard_reference="Bảng G.1, Bảng G.4 & Mục G.2.5.4 Phụ lục G TCVN 2737:2023",
        description="Tính toán độ võng đứng giới hạn [fu] theo yêu cầu thẩm mỹ, tâm sinh lý và công nghệ.",
        parameters={
            "element_type": "Loại cấu kiện ('roof_floor_visible', 'crane_girder', 'floor_moving_load', 'parking_floor', 'lintel_wall', 'prestress_camber')",
            "span_L": "Nhịp tính toán L (m)",
            "is_cantilever": "True nếu là dầm/bản công xôn (mặc định False)",
            "room_height": "Chiều cao thông thủy phòng (m, mặc định 4.0)",
            "crane_control": "'cabin' hoặc 'floor' (mặc định 'cabin')",
            "crane_group": "Chế độ làm việc cầu trục ('A1_A6', 'A7', 'A8')",
            "rail_type": "Loại đường ray ('narrow', 'wide', 'none')",
        },
    ),
    calc_vertical_deflection_limit,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_DRIFT_TCVN2737_G_HORIZ",
        name="Chuyển vị ngang giới hạn [fu] cho nhà và cột",
        category="DEFLECTION_AND_DRIFT",
        standard_reference="Bảng G.3, Bảng G.5 & Mục G.2.4.2 Phụ lục G TCVN 2737:2023",
        description="Tính toán chuyển vị ngang giới hạn [fu] cho nhà nhiều tầng, một tầng, cột cầu trục.",
        parameters={
            "structure_type": "'multistory_building_overall', 'multistory_single_story', 'single_story_building', 'crane_column', 'temperature_settlement_column'",
            "total_height_h": "Chiều cao toàn nhà h (m, mặc định 30.0)",
            "story_height_hs": "Chiều cao tầng hs (m, mặc định 3.6)",
            "partition_material": "'brick_concrete_gypsum', 'natural_stone_ceramic', 'glass_curtain'",
            "connection_type": "'rigid' hoặc 'flexible'",
            "crane_group": "'A1_A3', 'A4_A6', 'A7_A8'",
        },
    ),
    calc_horizontal_drift_limit,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_IMPORTANCE_TCVN2737_H_GAMMA_N",
        name="Hệ số tầm quan trọng gamma_n",
        category="IMPORTANCE_FACTOR",
        standard_reference="Bảng H.1 & Mục H.3 Phụ lục H TCVN 2737:2023",
        description="Xác định hệ số độ tin cậy về tầm quan trọng gamma_n theo cấp hậu quả C1, C2, C3.",
        parameters={
            "consequence_class": "Cấp hậu quả ('C1', 'C2', 'C3')",
            "limit_state": "Trạng thái giới hạn ('ULS' hoặc 'SLS')",
            "building_height": "Chiều cao công trình (m, mặc định 0.0)",
            "span_length": "Nhịp lớn không trụ trung gian (m, mặc định 0.0)",
        },
    ),
    calc_importance_factor_gamma_n,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_PHYSIOLOGICAL_DEFLECTION_G1",
        name="Độ võng giới hạn theo yêu cầu tâm sinh lý [fu] (Công thức G.1)",
        category="DEFLECTION_AND_DRIFT",
        standard_reference="Mục G.2.2 & Bảng G.2 Phụ lục G TCVN 2737:2023",
        description="Tính toán độ võng giới hạn theo yêu cầu tâm sinh lý phụ thuộc vào tải trọng người dao động và thông số hình học sàn.",
        parameters={
            "occupancy_group": "Nhóm công năng ('A_B' hoặc 'C_D')",
            "p": "Tải trọng con người dao động p (kN/m2, tùy chọn)",
            "p1": "Tải trọng giảm lên sàn p1 (kN/m2, mặc định 0.5)",
            "q": "Tải trọng bản thân kết cấu q (kN/m2, mặc định 3.0)",
            "n": "Tần số gia tải n (Hz, mặc định 1.5)",
            "a_m": "Bước dầm hoặc chiều rộng bản sàn a (m, mặc định 3.0)",
            "span_L_m": "Nhịp tính toán L (m, mặc định 6.0)",
            "beam_scheme": "'beam' (dầm, alpha=1.0) hoặc 'slab_3_4_edges' (bản sàn, alpha=0.6)",
            "Q_person_kN": "Trọng lượng một người Q (kN, mặc định 0.8)",
            "g_m_s2": "Gia tốc trọng trường g (m/s2, mặc định 9.81)",
        },
    ),
    calc_physiological_deflection_limit_fu,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_CHECK_DEFLECTION_DRIFT_COMPLIANCE",
        name="Kiểm tra điều kiện an toàn chuyển vị f <= [fu]",
        category="DEFLECTION_AND_DRIFT",
        standard_reference="Phụ lục G & H TCVN 2737:2023",
        description="Kiểm tra tuân thủ điều kiện an toàn độ võng/chuyển vị thực tế so với giới hạn tiêu chuẩn.",
        parameters={
            "actual_value_mm": "Giá trị độ võng/chuyển vị tính toán thực tế f (mm)",
            "check_type": "'vertical_deflection' hoặc 'horizontal_drift'",
            "params": "Dict các tham số truyền cho bộ giải giới hạn tương ứng",
        },
    ),
    check_deflection_and_drift_limits,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_WIND_TCVN2737_FULL_PIPELINE",
        name="Tải trọng gió toàn trình theo Chương 10 TCVN 2737:2023",
        category="WIND_LOAD",
        standard_reference="Chương 10, Phụ lục C, D, E, F, H TCVN 2737:2023",
        description="Bộ giải tích hợp toàn trình tính áp lực gió tiêu chuẩn Wk và tính toán Wd theo từng vùng khí động học.",
        parameters={
            "province": "Tên tỉnh/thành phố (mặc định 'Hà Nội')",
            "district": "Tên quận/huyện (tùy chọn)",
            "commune": "Tên xã/phường (tùy chọn)",
            "height_z": "Chiều cao điểm tính toán z (m, mặc định 10.0)",
            "terrain_category": "Dạng địa hình ('A', 'B', 'C', mặc định 'B')",
            "slope_i": "Độ dốc địa hình xung quanh (mặc định 0.0)",
            "structure_geometry": "'vertical_wall', 'duopitch_roof', 'flat_roof', 'monopitch_roof', 'hipped_roof', 'freestanding_wall'",
            "geometry_params": "Dict tham số hình học chi tiết",
            "structure_type": "'concrete' hoặc 'steel'",
            "total_building_height_h": "Chiều cao tổng thể toàn nhà h (m, mặc định 30.0)",
            "period_T1": "Chu kỳ dao động T1 (s, mặc định 1.0)",
            "consequence_class": "Cấp hậu quả ('C1', 'C2', 'C3', mặc định 'C2')",
            "gamma_f": "Hệ số độ tin cậy tải trọng gió (mặc định 2.1)",
        },
    ),
    calc_full_wind_load_tcvn2737,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_PLANNING_QCVN01_NET_DENSITY",
        name="Tính toán Mật độ Xây dựng Thuần Tối đa",
        category="PLANNING_DENSITY",
        standard_reference="Bảng 2.8 & Bảng 2.9 (Mục 2.6.3 QCVN 01:2021/BXD)",
        description="Tính toán mật độ xây dựng thuần tối đa cho nhà ở riêng lẻ, chung cư và dịch vụ công cộng theo diện tích lô đất và chiều cao công trình.",
        parameters={
            "land_area_m2": "Diện tích lô đất xây dựng (m2)",
            "building_height_m": "Chiều cao công trình (m, mặc định 0.0)",
            "building_type": "Loại công trình ('detached_house', 'residential_apartment', 'service_public')",
            "proposed_density_percent": "Mật độ đề xuất thiết kế để kiểm tra tuân thủ (%, tùy chọn)",
        },
    ),
    calc_max_net_building_density,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_PLANNING_QCVN01_SETBACK",
        name="Xác định Khoảng lùi Tối thiểu của Công trình",
        category="PLANNING_SETBACK",
        standard_reference="Bảng 2.7 (Mục 2.6.2 QCVN 01:2021/BXD)",
        description="Tra cứu khoảng lùi tối thiểu (m) của công trình theo bề rộng lộ giới đường tiếp giáp và chiều cao xây dựng.",
        parameters={
            "road_width_m": "Bề rộng lộ giới đường tiếp giáp (m)",
            "building_height_m": "Chiều cao xây dựng công trình (m)",
            "proposed_setback_m": "Khoảng lùi đề xuất thiết kế (m, tùy chọn)",
        },
    ),
    calc_min_setback_distance,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_PLANNING_QCVN01_ATMT",
        name="Tra cứu Khoảng cách An toàn Môi trường (ATMT)",
        category="PLANNING_ENVIRONMENTAL_SAFETY",
        standard_reference="Bảng 2.10 (Mục 2.11 QCVN 01:2021/BXD)",
        description="Tra cứu khoảng cách an toàn môi trường tối thiểu đối với trạm trung chuyển CTR, bãi chôn lấp, nhà máy xử lý rác, nghĩa trang, nhà tang lễ.",
        parameters={
            "facility_type": "Mã loại cơ sở ('solid_waste_transfer_closed', 'solid_waste_transfer_open', 'solid_waste_treatment_plant_closed', 'solid_waste_landfill_sanitary', 'cemetery_burial_primary', 'cemetery_burial_secondary', 'crematorium')",
            "scale_capacity": "Quy mô/công suất (tùy chọn)",
            "actual_distance_m": "Khoảng cách thực tế đến khu dân cư (m, tùy chọn)",
        },
    ),
    calc_min_environmental_safety_distance,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_PLANNING_QCVN01_PARKING",
        name="Tính toán Chỉ tiêu Chỗ Đỗ Xe Tối thiểu",
        category="PLANNING_PARKING",
        standard_reference="Bảng 2.19 (Mục 2.9 QCVN 01:2021/BXD)",
        description="Tính toán số lượng chỗ đỗ ô tô và xe máy tối thiểu cho chung cư thương mại, nhà ở xã hội, văn phòng, TTTM và khách sạn.",
        parameters={
            "building_type": "Loại công trình ('apartment_commercial', 'apartment_social', 'office', 'commercial', 'hotel')",
            "floor_area_m2": "Diện tích sàn sử dụng (m2, mặc định 0.0)",
            "num_apartments": "Số căn hộ (mặc định 0)",
            "num_hotel_rooms": "Số phòng khách sạn (mặc định 0)",
            "hotel_stars": "Số sao khách sạn (mặc định 3)",
            "proposed_car_spaces": "Số chỗ ô tô thiết kế (tùy chọn)",
            "proposed_motorbike_spaces": "Số chỗ xe máy thiết kế (tùy chọn)",
        },
    ),
    calc_min_parking_spaces,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_PLANNING_QCVN01_CORNER_CHAMFER",
        name="Tính toán Kích thước Vát góc Lộ giới tại Nút giao",
        category="PLANNING_ROAD_NETWORK",
        standard_reference="Mục 2.6.2 (QCVN 01:2021/BXD)",
        description="Tính toán kích thước cạnh vát góc tam giác tối thiểu và diện tích vát góc tại nút giao lộ theo góc giao và cấp đường.",
        parameters={
            "intersection_angle_deg": "Góc giao nhau giữa 2 đường (độ)",
            "road_width_1_m": "Bề rộng lộ giới đường 1 (m)",
            "road_width_2_m": "Bề rộng lộ giới đường 2 (m)",
            "proposed_chamfer_m": "Cạnh vát đề xuất (m, tùy chọn)",
        },
    ),
    calc_corner_chamfer_dimensions,
)

SymbolicFormulaSolver.register(
    FormulaMetadata(
        formula_id="F_PLANNING_QCVN01_GREENERY",
        name="Tính toán Chỉ tiêu Đất Cây xanh Đô thị",
        category="PLANNING_GREENERY",
        standard_reference="Bảng 2.1 & Bảng 2.2 (Mục 2.2 QCVN 01:2021/BXD)",
        description="Tính toán diện tích đất cây xanh công cộng tối thiểu toàn đô thị và trong khu ở theo loại đô thị và quy mô dân số.",
        parameters={
            "urban_grade": "Cấp đô thị ('special', 'grade_1', 'grade_2', 'grade_3', 'grade_4', 'grade_5')",
            "population": "Quy mô dân số (người)",
            "proposed_greenery_area_m2": "Diện tích cây xanh đề xuất (m2, tùy chọn)",
        },
    ),
    calc_urban_greenery_requirement,
)

