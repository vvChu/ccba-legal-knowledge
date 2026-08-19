"""
CCBA Legal Knowledge — Formula Solver Data Models.
Định nghĩa cấu trúc dữ liệu cho kết quả tính toán kỹ thuật xác định (ADR 0020).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class CalculationStep:
    """Từng bước giải trình và thế số trong bài toán kỹ thuật."""

    step_number: int
    description: str
    formula_latex: str
    substitution: str
    result_text: str


@dataclass
class CalculationResult:
    """Kết quả tính toán kỹ thuật hoàn chỉnh và minh bạch giải trình."""

    formula_id: str
    formula_name: str
    standard_reference: str
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    unit: str
    primary_value: float
    steps: list[CalculationStep] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    is_compliant: bool = True
    compliance_message: str = "Thỏa mãn yêu cầu quy chuẩn."

    def to_dict(self) -> dict[str, Any]:
        """Chuyển đổi kết quả thành dictionary cấu trúc JSON."""
        return asdict(self)

    def format_text_report(self) -> str:
        """Xuất báo cáo giải trình thế số dạng Markdown/Văn bản cho hồ sơ thẩm tra."""
        lines = [
            f"### 🧮 BÁO CÁO TÍNH TOÁN: {self.formula_name}",
            f"- **Mã công thức:** `{self.formula_id}`",
            f"- **Căn cứ pháp lý / Quy chuẩn:** {self.standard_reference}",
            f"- **Giá trị tính toán cốt lõi:** **{self.primary_value:g} {self.unit}**",
            "",
            "#### 1. Thông số đầu vào:",
        ]
        for k, v in self.inputs.items():
            lines.append(f"  • `{k}`: {v}")

        if self.steps:
            lines.append("\n#### 2. Các bước giải trình thế số:")
            for s in self.steps:
                lines.append(f"**Bước {s.step_number}: {s.description}**")
                if s.formula_latex:
                    lines.append(f"  - Công thức: ${s.formula_latex}$")
                if s.substitution:
                    lines.append(f"  - Thế số: {s.substitution}")
                lines.append(f"  - Kết quả: {s.result_text}\n")

        if self.notes:
            lines.append("#### 3. Ghi chú điều kiện biên & Chú thích quy chuẩn:")
            for n in self.notes:
                lines.append(f"  - ℹ️ {n}")

        lines.append(f"\n#### 4. Kết luận tuân thủ:\n  👉 **{self.compliance_message}**")
        return "\n".join(lines)


@dataclass
class FormulaMetadata:
    """Siêu dữ liệu mô tả công thức kỹ thuật."""

    formula_id: str
    name: str
    category: str
    standard_reference: str
    description: str
    parameters: dict[str, str]
