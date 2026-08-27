"""
CCBA Legal Knowledge — Deterministic Planning Solvers for QCVN 01:2021/BXD.
Triển khai các bộ giải toán quy hoạch xây dựng xác định (ADR 0020 & ADR 0034).
Bao gồm:
1. Mật độ xây dựng thuần tối đa (Bảng 2.8 & Bảng 2.9).
2. Khoảng lùi công trình tối thiểu theo lộ giới và chiều cao (Bảng 2.7).
3. Khoảng cách an toàn môi trường ATMT (Bảng 2.10).
"""

from __future__ import annotations

from typing import Any
from formulas.models import CalculationResult, CalculationStep, FormulaMetadata


# -----------------------------------------------------------------------------
# 1. BẢNG 2.8: MẬT ĐỘ XÂY DỰNG THUẦN TỐI ĐA CHO NHÀ Ở RIÊNG LẺ
# -----------------------------------------------------------------------------
TABLE_2_8_POINTS = [
    (50.0, 100.0),
    (75.0, 90.0),
    (100.0, 80.0),
    (200.0, 70.0),
    (300.0, 60.0),
    (500.0, 50.0),
    (1000.0, 40.0),
]


def _interp_table_2_8(area: float) -> float:
    """Nội suy tuyến tính mật độ xây dựng nhà ở riêng lẻ theo Bảng 2.8."""
    if area <= TABLE_2_8_POINTS[0][0]:
        return TABLE_2_8_POINTS[0][1]
    if area >= TABLE_2_8_POINTS[-1][0]:
        return TABLE_2_8_POINTS[-1][1]

    for i in range(len(TABLE_2_8_POINTS) - 1):
        s1, d1 = TABLE_2_8_POINTS[i]
        s2, d2 = TABLE_2_8_POINTS[i + 1]
        if s1 <= area <= s2:
            return d1 - ((d1 - d2) / (s2 - s1)) * (area - s1)
    return 40.0


# -----------------------------------------------------------------------------
# 2. BẢNG 2.9: MẬT ĐỘ XÂY DỰNG THUẦN TỐI ĐA CHO CHUNG CƯ & DỊCH VỤ ĐÔ THỊ
# -----------------------------------------------------------------------------
# Height thresholds in ascending order: (h_max, density_at_3000, density_at_10000)
TABLE_2_9_TIERS = [
    (16.0, 75.0, 60.0),
    (19.0, 75.0, 50.0),
    (22.0, 65.0, 45.0),
    (25.0, 60.0, 41.0),
    (28.0, 55.0, 38.0),
    (31.0, 50.0, 36.0),
    (34.0, 48.0, 35.0),
    (37.0, 45.0, 33.0),
    (40.0, 43.0, 31.0),
    (46.0, 40.0, 28.0),
    (float("inf"), 40.0, 25.0),
]


def _get_table_2_9_density_at_limits(height_m: float) -> tuple[float, float, str]:
    """Lấy mật độ tại mốc S<=3000 và S>=10000 theo chiều cao công trình."""
    for h_max, d_3000, d_10000 in TABLE_2_9_TIERS:
        if height_m <= h_max:
            tier_desc = f"≤ {h_max}m" if h_max != float("inf") else "> 46m"
            return d_3000, d_10000, tier_desc
    return 40.0, 25.0, "> 46m"


def calc_max_net_building_density(
    land_area_m2: float,
    building_height_m: float = 0.0,
    building_type: str = "residential_apartment",
    proposed_density_percent: float | None = None,
) -> CalculationResult:
    """Tính toán mật độ xây dựng thuần tối đa theo QCVN 01:2021/BXD (Bảng 2.8 & 2.9).

    Args:
        land_area_m2: Diện tích lô đất (m2).
        building_height_m: Chiều cao công trình (m).
        building_type: Loại công trình ('detached_house' hoặc 'residential_apartment'/'service_public').
        proposed_density_percent: Mật độ đề xuất thiết kế để kiểm tra tuân thủ (%).

    Returns:
        CalculationResult chứa giá trị mật độ tối đa cho phép và thuyết minh thế số.
    """
    inputs: dict[str, Any] = {
        "land_area_m2": land_area_m2,
        "building_height_m": building_height_m,
        "building_type": building_type,
    }
    if proposed_density_percent is not None:
        inputs["proposed_density_percent"] = proposed_density_percent

    steps: list[CalculationStep] = []
    notes: list[str] = []

    if building_type in ("detached_house", "nha_o_rieng_le", "biet_thu", "lien_ke"):
        max_density = _interp_table_2_8(land_area_m2)
        ref_table = "Bảng 2.8 QCVN 01:2021/BXD"
        steps.append(
            CalculationStep(
                step_number=1,
                description="Tra cứu và nội suy mật độ xây dựng thuần cho nhà ở riêng lẻ theo diện tích lô đất",
                formula_latex=r"MĐXD(S) = MĐXD(S_1) - \frac{MĐXD(S_1) - MĐXD(S_2)}{S_2 - S_1} \cdot (S - S_1)",
                substitution=f"Diện tích lô đất S = {land_area_m2} m2",
                result_text=f"Mật độ xây dựng thuần tối đa cho phép = {max_density:.2f}%",
            )
        )
        notes.append("Lô đất xây dựng nhà ở riêng lẻ có diện tích <= 50m2 được phép xây dựng tối đa 100%.")
        notes.append("Khoảng lùi nhà ở riêng lẻ tuân thủ theo quy hoạch chi tiết hoặc thiết kế đô thị được duyệt.")
    else:
        d_3000, d_10000, tier_desc = _get_table_2_9_density_at_limits(building_height_m)
        ref_table = "Bảng 2.9 QCVN 01:2021/BXD"

        if land_area_m2 <= 3000.0:
            max_density = d_3000
            interp_sub = f"S = {land_area_m2} m2 <= 3000 m2 -> Lấy cận trên = {d_3000}%"
        elif land_area_m2 >= 10000.0:
            max_density = d_10000
            interp_sub = f"S = {land_area_m2} m2 >= 10000 m2 -> Lấy cận dưới = {d_10000}%"
        else:
            max_density = d_3000 - ((d_3000 - d_10000) / (10000.0 - 3000.0)) * (land_area_m2 - 3000.0)
            interp_sub = f"{d_3000} - (({d_3000} - {d_10000}) / 7000) * ({land_area_m2} - 3000) = {max_density:.2f}%"

        steps.append(
            CalculationStep(
                step_number=1,
                description=f"Xác định ngưỡng mật độ theo chiều cao công trình h = {building_height_m}m (Khoảng {tier_desc})",
                formula_latex=r"\text{Tra cứu Bảng 2.9 tại } S \le 3000\text{ m}^2 \text{ và } S \ge 10000\text{ m}^2",
                substitution=f"Chiều cao h = {building_height_m}m -> MĐXD(3000m2) = {d_3000}%, MĐXD(10000m2) = {d_10000}%",
                result_text=f"Cận dưới: {d_10000}%, Cận trên: {d_3000}%",
            )
        )
        steps.append(
            CalculationStep(
                step_number=2,
                description="Nội suy tuyến tính mật độ xây dựng thuần theo diện tích lô đất",
                formula_latex=r"MĐXD(S) = MĐXD(3000) - \frac{MĐXD(3000) - MĐXD(10000)}{10000 - 3000} \cdot (S - 3000)",
                substitution=interp_sub,
                result_text=f"Mật độ xây dựng thuần tối đa cho phép = {max_density:.2f}%",
            )
        )
        notes.append("Mật độ xây dựng thuần của khối đế áp dụng theo Bảng 2.9 tương ứng với chiều cao khối đế.")
        notes.append("Trường hợp công trình là tổ hợp nhiều khối tháp có chiều cao khác nhau, mật độ khối tháp tính theo chiều cao trung bình hoặc chiều cao khống chế.")

    is_compliant = True
    comp_msg = f"Mật độ tối đa cho phép là {max_density:.2f}%."
    if proposed_density_percent is not None:
        if proposed_density_percent <= max_density + 1e-3:
            is_compliant = True
            comp_msg = f"ĐẠT: Mật độ đề xuất {proposed_density_percent:.2f}% ≤ Ngưỡng tối đa cho phép {max_density:.2f}%."
        else:
            is_compliant = False
            comp_msg = f"KHÔNG ĐẠT: Mật độ đề xuất {proposed_density_percent:.2f}% VƯỢT QUÁ ngưỡng tối đa cho phép {max_density:.2f}% (vượt {proposed_density_percent - max_density:.2f}%)."

    return CalculationResult(
        formula_id="F_PLANNING_QCVN01_NET_DENSITY",
        formula_name="Tính toán Mật độ Xây dựng Thuần Tối đa (QCVN 01:2021/BXD)",
        standard_reference=f"{ref_table} (Mục 2.6.3 QCVN 01:2021/BXD)",
        inputs=inputs,
        outputs={
            "max_net_density_percent": round(max_density, 2),
            "is_compliant": is_compliant,
        },
        unit="%",
        primary_value=round(max_density, 2),
        steps=steps,
        notes=notes,
        is_compliant=is_compliant,
        compliance_message=comp_msg,
    )


# -----------------------------------------------------------------------------
# 3. BẢNG 2.7: KHOẢNG LÙI TỐI THIỂU CỦA CÔNG TRÌNH
# -----------------------------------------------------------------------------
def calc_min_setback_distance(
    road_width_m: float,
    building_height_m: float,
    proposed_setback_m: float | None = None,
) -> CalculationResult:
    """Tra cứu và xác định khoảng lùi tối thiểu (m) theo Bảng 2.7 QCVN 01:2021/BXD.

    Args:
        road_width_m: Bề rộng lộ giới đường tiếp giáp (m).
        building_height_m: Chiều cao xây dựng công trình (m).
        proposed_setback_m: Khoảng lùi đề xuất thiết kế (m).

    Returns:
        CalculationResult chứa khoảng lùi tối thiểu và đánh giá tuân thủ.
    """
    inputs: dict[str, Any] = {
        "road_width_m": road_width_m,
        "building_height_m": building_height_m,
    }
    if proposed_setback_m is not None:
        inputs["proposed_setback_m"] = proposed_setback_m

    # Bảng 2.7 logic
    if road_width_m < 19.0:
        road_tier = "< 19m"
        if building_height_m <= 19.0:
            min_setback = 0.0
            height_tier = "≤ 19m"
        elif building_height_m <= 22.0:
            min_setback = 3.0
            height_tier = "> 19m đến 22m"
        elif building_height_m <= 25.0:
            min_setback = 4.0
            height_tier = "> 22m đến 25m"
        elif building_height_m <= 28.0:
            min_setback = 6.0
            height_tier = "> 25m đến 28m"
        else:
            min_setback = 6.0
            height_tier = "> 28m"
    elif road_width_m <= 22.0:
        road_tier = "19m đến 22m"
        if building_height_m <= 22.0:
            min_setback = 0.0
            height_tier = "≤ 22m"
        elif building_height_m <= 25.0:
            min_setback = 3.0
            height_tier = "> 22m đến 25m"
        elif building_height_m <= 28.0:
            min_setback = 6.0
            height_tier = "> 25m đến 28m"
        else:
            min_setback = 6.0
            height_tier = "> 28m"
    else:
        road_tier = "> 22m"
        if building_height_m <= 25.0:
            min_setback = 0.0
            height_tier = "≤ 25m"
        elif building_height_m <= 28.0:
            min_setback = 3.0
            height_tier = "> 25m đến 28m"
        else:
            min_setback = 6.0
            height_tier = "> 28m"

    steps = [
        CalculationStep(
            step_number=1,
            description="Phân loại bề rộng lộ giới đường tiếp giáp và chiều cao công trình theo Bảng 2.7",
            formula_latex=r"\text{Tra cứu Bảng 2.7: Khoảng lùi } = f(\text{Lộ giới, Chiều cao})",
            substitution=f"Lộ giới đường = {road_width_m}m (Nhóm {road_tier}), Chiều cao công trình = {building_height_m}m (Nhóm {height_tier})",
            result_text=f"Khoảng lùi tối thiểu quy định = {min_setback:.1f} m",
        )
    ]

    notes = [
        "Khoảng lùi của công trình so với lộ giới đường được xác định theo quy chuẩn hoặc quy hoạch chi tiết xây dựng/thiết kế đô thị.",
        "Đối với tổ hợp công trình bao gồm phần đế và tháp cao phía trên, khoảng lùi của phần đế tuân thủ theo chiều cao phần đế, khoảng lùi của khối tháp tuân thủ theo chiều cao toàn bộ công trình.",
    ]

    is_compliant = True
    comp_msg = f"Khoảng lùi tối thiểu quy định là {min_setback:.1f} m."
    if proposed_setback_m is not None:
        if proposed_setback_m >= min_setback - 1e-3:
            is_compliant = True
            comp_msg = f"ĐẠT: Khoảng lùi thiết kế {proposed_setback_m:.2f}m ≥ Khoảng lùi tối thiểu quy định {min_setback:.1f}m."
        else:
            is_compliant = False
            comp_msg = f"KHÔNG ĐẠT: Khoảng lùi thiết kế {proposed_setback_m:.2f}m NHỎ HƠN khoảng lùi tối thiểu quy định {min_setback:.1f}m (thiếu {min_setback - proposed_setback_m:.2f}m)."

    return CalculationResult(
        formula_id="F_PLANNING_QCVN01_SETBACK",
        formula_name="Xác định Khoảng lùi Tối thiểu của Công trình (QCVN 01:2021/BXD)",
        standard_reference="Bảng 2.7 (Mục 2.6.2 QCVN 01:2021/BXD)",
        inputs=inputs,
        outputs={
            "min_setback_m": min_setback,
            "road_tier": road_tier,
            "height_tier": height_tier,
            "is_compliant": is_compliant,
        },
        unit="m",
        primary_value=min_setback,
        steps=steps,
        notes=notes,
        is_compliant=is_compliant,
        compliance_message=comp_msg,
    )


# -----------------------------------------------------------------------------
# 4. BẢNG 2.10: KHOẢNG CÁCH AN TOÀN MÔI TRƯỜNG (ATMT)
# -----------------------------------------------------------------------------
ATMT_FACILITIES: dict[str, dict[str, Any]] = {
    "solid_waste_transfer_closed": {
        "name": "Trạm trung chuyển chất thải rắn sinh hoạt kiểu kín",
        "min_dist_m": 20.0,
        "note": "Phải có hệ thống hút lọc mùi và xử lý nước rỉ rác.",
    },
    "solid_waste_transfer_open": {
        "name": "Trạm trung chuyển chất thải rắn sinh hoạt kiểu hở",
        "min_dist_m": 50.0,
        "note": "Chỉ áp dụng tại khu vực ngoại thành hoặc khu cách ly.",
    },
    "solid_waste_treatment_plant_closed": {
        "name": "Nhà máy xử lý chất thải rắn (đốt có phát điện, chế biến phân vi sinh) kiểu kín",
        "min_dist_m": 100.0,
        "note": "Công nghệ hiện đại khép kín.",
    },
    "solid_waste_landfill_sanitary": {
        "name": "Bãi chôn lấp chất thải rắn sinh hoạt hợp vệ sinh",
        "min_dist_m": 500.0,
        "note": "Có hệ thống thu gom khí và xử lý nước rác triệt để.",
    },
    "solid_waste_landfill_inorganic": {
        "name": "Bãi chôn lấp chất thải rắn vô cơ, xỉ than",
        "min_dist_m": 100.0,
        "note": "Đất trơ hoặc chất thải xây dựng.",
    },
    "cemetery_burial_primary": {
        "name": "Nghĩa trang hung táng, chôn cất một lần (khu vực đồng bằng)",
        "min_dist_m": 500.0,
        "note": "Đến ranh giới khu dân cư gần nhất.",
    },
    "cemetery_burial_secondary": {
        "name": "Nghĩa trang cát táng, lưu tro cốt",
        "min_dist_m": 100.0,
        "note": "Đến ranh giới khu dân cư gần nhất.",
    },
    "crematorium": {
        "name": "Nhà hỏa táng / Đài hỏa táng",
        "min_dist_m": 100.0,
        "note": "Sử dụng công nghệ đốt hiện đại không phát tán khói mùi.",
    },
}


def calc_min_environmental_safety_distance(
    facility_type: str,
    scale_capacity: float | None = None,
    actual_distance_m: float | None = None,
) -> CalculationResult:
    """Tra cứu khoảng cách an toàn môi trường (ATMT) theo Bảng 2.10 QCVN 01:2021/BXD.

    Args:
        facility_type: Mã cơ sở kỹ thuật/hạ tầng.
        scale_capacity: Công suất hoặc quy mô (nếu có).
        actual_distance_m: Khoảng cách thực tế đo từ ranh giới cơ sở đến khu dân dụng (m).

    Returns:
        CalculationResult chứa khoảng cách an toàn tối thiểu và đánh giá tuân thủ.
    """
    facility_info = ATMT_FACILITIES.get(
        facility_type,
        {
            "name": f"Cơ sở hạ tầng ({facility_type})",
            "min_dist_m": 100.0,
            "note": "Khoảng cách an toàn môi trường mặc định.",
        },
    )

    min_dist = float(facility_info["min_dist_m"])
    name = str(facility_info["name"])
    note = str(facility_info["note"])

    inputs: dict[str, Any] = {
        "facility_type": facility_type,
        "facility_name": name,
    }
    if scale_capacity is not None:
        inputs["scale_capacity"] = scale_capacity
    if actual_distance_m is not None:
        inputs["actual_distance_m"] = actual_distance_m

    steps = [
        CalculationStep(
            step_number=1,
            description=f"Tra cứu khoảng cách ATMT tối thiểu cho loại cơ sở: {name}",
            formula_latex=r"D_{\text{ATMT}} \ge D_{\text{min}} \text{ (Bảng 2.10 QCVN 01:2021/BXD)}",
            substitution=f"Loại cơ sở = {name}",
            result_text=f"Khoảng cách ATMT tối thiểu = {min_dist} m",
        )
    ]

    notes = [
        note,
        "Trong vùng ATMT phải bố trí dải cây xanh cách ly tối thiểu 10m - 20m kết hợp đường giao thông.",
        "Không được xây dựng công trình nhà ở, trường học, bệnh viện trong phạm vi vùng ATMT.",
    ]

    is_compliant = True
    comp_msg = f"Khoảng cách ATMT tối thiểu quy định là {min_dist} m."
    if actual_distance_m is not None:
        if actual_distance_m >= min_dist - 1e-3:
            is_compliant = True
            comp_msg = f"ĐẠT: Khoảng cách thực tế {actual_distance_m:.1f}m ≥ Khoảng cách ATMT tối thiểu quy định {min_dist:.1f}m."
        else:
            is_compliant = False
            comp_msg = f"KHÔNG ĐẠT: Khoảng cách thực tế {actual_distance_m:.1f}m VI PHẠM khoảng cách ATMT tối thiểu quy định {min_dist:.1f}m (thiếu {min_dist - actual_distance_m:.1f}m)."

    return CalculationResult(
        formula_id="F_PLANNING_QCVN01_ATMT",
        formula_name="Tra cứu Khoảng cách An toàn Môi trường ATMT (QCVN 01:2021/BXD)",
        standard_reference="Bảng 2.10 (Mục 2.11 QCVN 01:2021/BXD)",
        inputs=inputs,
        outputs={
            "min_atmt_distance_m": min_dist,
            "facility_name": name,
            "is_compliant": is_compliant,
        },
        unit="m",
        primary_value=min_dist,
        steps=steps,
        notes=notes,
        is_compliant=is_compliant,
        compliance_message=comp_msg,
    )
