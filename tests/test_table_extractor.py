"""Unit tests for Table Extractor Engine."""

from pathlib import Path
from scripts.table_extractor import (
    extract_table_from_text_block,
    make_descriptive_table_slug,
    parse_and_extract_all_tables,
)

SAMPLE_HTML_TABLE = """
### Bảng 4 - Sự phù hợp giữa bậc chịu lửa của nhà và khoang cháy
| Bậc chịu lửa | Tường chịu lực | Tường ngoài | Sàn tầng |
| --- | --- | --- | --- |
| Bậc I | REI 150 | E 30 | REI 60 |
| Bậc II | REI 120 | E 15 | REI 45 |
"""

def test_make_descriptive_table_slug():
    assert make_descriptive_table_slug("1", "Bảng 1 - Giới hạn chịu lửa") == "bang_01_gioi_han_chiu_lua"
    assert make_descriptive_table_slug("4.1", "Bảng 4.1 - Sự phù hợp") == "bang_4_1_su_phu_hop"

def test_extract_table_from_text_block():
    lines = [
        "| Bậc chịu lửa | Tường chịu lực | Tường ngoài | Sàn tầng |",
        "| --- | --- | --- | --- |",
        "| Bậc I | REI 150 | E 30 | REI 60 |",
    ]
    res = extract_table_from_text_block("Bảng 4 - Sự phù hợp", lines)
    assert res is not None
    assert res["table_id"].startswith("bang_04")
    assert res["total_rows"] == 1

def test_parse_and_extract_all_tables(tmp_path: Path):
    bundle_dir = tmp_path / "test_qcvn"
    bundle_dir.mkdir()

    cleaned_md, generated_files = parse_and_extract_all_tables(bundle_dir, SAMPLE_HTML_TABLE)
    assert len(generated_files) == 2  # 1 JSON + 1 CSV

    json_files = list((bundle_dir / "tables" / "json").glob("bang_04*.json"))
    assert len(json_files) == 1
    assert json_files[0].exists()
