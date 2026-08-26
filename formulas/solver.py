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
from formulas.wind_load_tcvn2737 import (
    calc_duopitch_roof_ce_coefficients,
    calc_freestanding_wall_aerodynamic_coeff,
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
