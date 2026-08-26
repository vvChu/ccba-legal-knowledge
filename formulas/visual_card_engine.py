"""
CCBA Legal Knowledge — Parametric Visual Card Engine.
Mô-đun tải, kiểm tra và tính toán hình học phân vùng khí động từ Visual Cards JSON (ADR 0030).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class GeometricZoneResult:
    """Kết quả tính toán kích thước hình học của một vùng khí động."""
    zone_name: str
    extent_description: str
    dimension_m: dict[str, float] = field(default_factory=dict)
    description: str = ""


@dataclass
class VisualCardEvaluation:
    """Kết quả đánh giá tham số hóa hoàn chỉnh của một Visual Card."""
    card_id: str
    figure_number: str
    title: str
    matched_case_id: str
    matched_case_description: str
    calculated_parameters: dict[str, float]
    zones: dict[str, GeometricZoneResult] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)


class VisualCardEngine:
    """Engine quản lý và thực thi logic hình học từ các Visual Cards."""

    _DEFAULT_CARDS_DIR = Path(__file__).resolve().parent.parent / "legal_docs" / "03_tcvn" / "tcvn_2737_2023" / "figures" / "cards"

    @classmethod
    def load_card(cls, card_id_or_filename: str, custom_dir: Path | None = None) -> dict[str, Any]:
        """Tải nội dung tệp JSON của Visual Card."""
        cards_dir = custom_dir or cls._DEFAULT_CARDS_DIR
        if not cards_dir.exists():
            raise FileNotFoundError(f"Không tìm thấy thư mục Visual Cards: {cards_dir}")

        filename = card_id_or_filename if card_id_or_filename.endswith(".json") else f"{card_id_or_filename}.json"
        target_path = cards_dir / filename
        
        # Nếu chưa tìm thấy, duyệt tìm theo card_id
        if not target_path.exists():
            for p in cards_dir.glob("*.json"):
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                    if data.get("card_id") == card_id_or_filename or data.get("figure_number") == card_id_or_filename:
                        return data
                except Exception:
                    continue
            raise FileNotFoundError(f"Không tìm thấy Visual Card '{card_id_or_filename}' trong {cards_dir}")

        return json.loads(target_path.read_text(encoding="utf-8"))

    @classmethod
    def list_cards(cls, custom_dir: Path | None = None) -> list[dict[str, Any]]:
        """Liệt kê toàn bộ các Visual Cards khả dụng."""
        cards_dir = custom_dir or cls._DEFAULT_CARDS_DIR
        if not cards_dir.exists():
            return []
        cards = []
        for p in sorted(cards_dir.glob("*.json")):
            try:
                cards.append(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                continue
        return cards

    @classmethod
    def evaluate_wall_f1(
        cls,
        length_L: float,
        height_h: float,
        solidity_ratio_phi: float = 1.0,
        return_corner_length: float = 0.0,
    ) -> VisualCardEvaluation:
        """Tính toán phân vùng hình học cho tường phẳng / hàng rào theo Hình F.1."""
        card = cls.load_card("fig_f_1_freestanding_wall.json")
        ratio = length_L / height_h if height_h > 0 else 0.0
        calc_params = {
            "length_L": length_L,
            "height_h": height_h,
            "aspect_ratio_L_h": ratio,
            "solidity_ratio_phi": solidity_ratio_phi,
            "return_corner_length": return_corner_length,
        }

        zones: dict[str, GeometricZoneResult] = {}
        matched_case = "CASE_UNKNOWN"
        matched_desc = ""
        constraints = []

        if return_corner_length >= height_h:
            constraints.append(f"Tường có bẻ góc với l_ret = {return_corner_length:g} m >= h = {height_h:g} m: Áp dụng hệ số giảm c_x theo Bảng F.1.")

        if ratio > 4.0:
            matched_case = "CASE_LONG_WALL"
            matched_desc = "Khi L > 4h (Tường dài)"
            zones["Zone_A"] = GeometricZoneResult("Zone_A", "0.0 đến 0.3h", {"length_m": round(0.3 * height_h, 3)}, "Mép đón gió tự do")
            zones["Zone_B"] = GeometricZoneResult("Zone_B", "0.3h đến 2.0h", {"length_m": round(1.7 * height_h, 3)}, "Dải chuyển tiếp")
            zones["Zone_C"] = GeometricZoneResult("Zone_C", "2.0h đến 4.0h", {"length_m": round(2.0 * height_h, 3)}, "Dải giữa")
            zones["Zone_D"] = GeometricZoneResult("Zone_D", "4.0h đến L", {"length_m": round(length_L - 4.0 * height_h, 3)}, "Phần còn lại của tường")
        elif ratio > 2.0:
            matched_case = "CASE_MEDIUM_WALL"
            matched_desc = "Khi 2h < L <= 4h (Tường trung bình)"
            zones["Zone_A"] = GeometricZoneResult("Zone_A", "0.0 đến 0.3h", {"length_m": round(0.3 * height_h, 3)}, "Mép đón gió")
            zones["Zone_B"] = GeometricZoneResult("Zone_B", "0.3h đến 2.0h", {"length_m": round(1.7 * height_h, 3)}, "Dải giữa")
            zones["Zone_C"] = GeometricZoneResult("Zone_C", "2.0h đến L", {"length_m": round(length_L - 2.0 * height_h, 3)}, "Dải cuối")
        else:
            matched_case = "CASE_SHORT_WALL"
            matched_desc = "Khi L <= 2h (Tường ngắn)"
            zones["Zone_A"] = GeometricZoneResult("Zone_A", "0.0 đến 0.3h", {"length_m": round(0.3 * height_h, 3)}, "Mép đón gió")
            zones["Zone_B"] = GeometricZoneResult("Zone_B", "0.3h đến L", {"length_m": round(length_L - 0.3 * height_h, 3)}, "Phần còn lại của tường")

        return VisualCardEvaluation(
            card_id=card.get("card_id", "FIG_TCVN2737_F1"),
            figure_number="F.1",
            title=card.get("title", ""),
            matched_case_id=matched_case,
            matched_case_description=matched_desc,
            calculated_parameters=calc_params,
            zones=zones,
            constraints=constraints,
        )

    @classmethod
    def evaluate_duopitch_f6(
        cls,
        pitch_angle_alpha: float,
        wind_angle_theta: float,
        building_width_b: float,
        building_height_h: float,
        building_depth_d: float,
    ) -> VisualCardEvaluation:
        """Tính toán phân vùng hình học cho mái dốc 2 phía theo Hình F.6."""
        card = cls.load_card("fig_f_6_duopitch_roof.json")
        e_dim = min(building_width_b, 2.0 * building_height_h)
        calc_params = {
            "pitch_angle_alpha": pitch_angle_alpha,
            "wind_angle_theta": wind_angle_theta,
            "building_width_b": building_width_b,
            "building_height_h": building_height_h,
            "building_depth_d": building_depth_d,
            "e_dimension": e_dim,
            "e_over_10": round(e_dim / 10.0, 3),
            "e_over_4": round(e_dim / 4.0, 3),
            "e_over_2": round(e_dim / 2.0, 3),
        }

        zones: dict[str, GeometricZoneResult] = {}
        constraints = []

        if wind_angle_theta == 0.0 and -5.0 <= pitch_angle_alpha <= 45.0:
            constraints.append("Áp lực thay đổi nhanh giữa âm và dương: Bắt buộc xét 2 trường hợp tải trọng độc lập (Toàn bộ Hút hoặc Toàn bộ Đẩy).")

        if wind_angle_theta == 0.0:
            matched_case = "CASE_THETA_0"
            matched_desc = "Góc hướng gió theta = 0 độ (Gió thổi vuông góc đường nóc)"
            zones["Zone_F"] = GeometricZoneResult("Zone_F", "e/4 x e/10", {"width_m": e_dim / 4.0, "depth_m": e_dim / 10.0}, "Góc mép đón gió")
            zones["Zone_G"] = GeometricZoneResult("Zone_G", "e/10 x (b - e/2)", {"width_m": building_width_b - e_dim / 2.0, "depth_m": e_dim / 10.0}, "Dải mép đón gió giữa hai vùng F")
            zones["Zone_H"] = GeometricZoneResult("Zone_H", "Phần còn lại nửa mái đón gió", {}, "Diện tích giữa mái đón gió")
            zones["Zone_I"] = GeometricZoneResult("Zone_I", "Diện tích chính nửa mái khuất gió", {}, "Diện tích chính mái khuất gió")
            zones["Zone_J"] = GeometricZoneResult("Zone_J", "e/10 x b dọc nóc mái khuất gió", {"width_m": building_width_b, "depth_m": e_dim / 10.0}, "Dải mép nóc mái khuất gió")
        else:
            matched_case = "CASE_THETA_90"
            matched_desc = "Góc hướng gió theta = 90 độ (Gió thổi song song đường nóc)"
            zones["Zone_F"] = GeometricZoneResult("Zone_F", "e/4 x e/10", {"width_m": e_dim / 10.0, "depth_m": e_dim / 4.0}, "Góc mép đón gió bên")
            zones["Zone_G"] = GeometricZoneResult("Zone_G", "e/10 rộng", {"depth_m": e_dim / 10.0}, "Dải mép đón gió bên")
            zones["Zone_H"] = GeometricZoneResult("Zone_H", "e/2 x (b - e/5)", {"depth_m": e_dim / 2.0}, "Dải tiếp theo dọc sườn")
            zones["Zone_I"] = GeometricZoneResult("Zone_I", "Phần diện tích còn lại", {}, "Toàn bộ diện tích còn lại của mái")

        return VisualCardEvaluation(
            card_id=card.get("card_id", "FIG_TCVN2737_F6"),
            figure_number="F.6",
            title=card.get("title", ""),
            matched_case_id=matched_case,
            matched_case_description=matched_desc,
            calculated_parameters=calc_params,
            zones=zones,
            constraints=constraints,
        )
