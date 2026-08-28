"""Unit tests for Modernize Annex Engine (Ticket 1 / OKF v2.3)."""

from pathlib import Path
from PIL import Image

try:
    from scripts.modernize_annex_engine import (
        FigureAutoCompositor,
        MathEquationConverter,
        TableMatrixBuilder,
    )
except ImportError:
    from modernize_annex_engine import (
        FigureAutoCompositor,
        MathEquationConverter,
        TableMatrixBuilder,
    )


def test_figure_auto_compositor_vertical(tmp_path: Path) -> None:
    img1 = tmp_path / "panel_a.png"
    img2 = tmp_path / "panel_b.png"
    out_img = tmp_path / "composite.png"

    # Create dummy panel images
    Image.new("RGB", (100, 50), color=(200, 200, 200)).save(img1)
    Image.new("RGB", (120, 60), color=(150, 150, 150)).save(img2)

    res = FigureAutoCompositor.composite_panels(
        image_paths=[img1, img2],
        output_path=out_img,
        layout="vertical",
        panel_labels=["a)", "b)"],
    )

    assert res.exists()
    comp = Image.open(res)
    assert comp.mode == "RGB"
    # Max width is 120 + 20*2 = 160
    assert comp.width >= 120
    # Height includes both images + padding + label space
    assert comp.height > 110


def test_figure_auto_compositor_horizontal(tmp_path: Path) -> None:
    img1 = tmp_path / "panel_1.png"
    img2 = tmp_path / "panel_2.png"
    out_img = tmp_path / "composite_h.png"

    Image.new("RGB", (80, 40), color=(220, 220, 220)).save(img1)
    Image.new("RGB", (80, 40), color=(180, 180, 180)).save(img2)

    res = FigureAutoCompositor.composite_panels(
        image_paths=[img1, img2],
        output_path=out_img,
        layout="horizontal",
    )

    assert res.exists()
    comp = Image.open(res)
    # Total width >= 80 + 80 + 20*3 = 220
    assert comp.width >= 160


def test_table_matrix_builder_lossless() -> None:
    raw_rows = [
        ["Góc alpha", "Vùng F", "Vùng G", "Vùng H"],
        ["5 độ", "-1.7 / +0.2", "-1.2", "-0.6"],
        ["15 độ", "-0.9 / +0.2", "-0.8 / +0.2", "-0.5"],
        ["CHÚ THÍCH: Giá trị tải trọng gió được xác định theo bảng F.3a"],
    ]

    table_md = TableMatrixBuilder.format_lossless_matrix_table(
        raw_rows=raw_rows,
        caption="Hệ số khí động mái dốc",
        table_num="Bảng F.3a",
    )

    assert "**Bảng F.3a — Hệ số khí động mái dốc**" in table_md
    assert "| Góc alpha | Vùng F | Vùng G | Vùng H |" in table_md
    assert "-1.7<br>+0.2" in table_md
    assert "-0.9<br>+0.2" in table_md
    assert "_CHÚ THÍCH:_" in table_md
    assert "Giá trị tải trọng gió được xác định theo bảng F.3a" in table_md


def test_math_equation_converter() -> None:
    raw_md = (
        "# Phụ lục F\n\n"
        "Áp lực gió tiêu chuẩn tác dụng lên bề mặt được xác định:\n"
        "W_k = W_0 * k(z_e) * c_e (F.1)\n\n"
        "Hệ số áp lực trong:\n"
        "c_i = +0.2 (F.2)\n"
    )

    clean_md = MathEquationConverter.convert_numbered_equations(raw_md)
    assert "$$" in clean_md
    assert "\\tag{F.1}" in clean_md
    assert "\\tag{F.2}" in clean_md
