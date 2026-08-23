"""Table Extractor Engine forwarding wrapper."""
import sys
from pathlib import Path

# Add archive path to sys.path if needed
archive_path = Path(__file__).resolve().parent.parent / ".md" / "archive" / "legacy_scripts"
if str(archive_path) not in sys.path:
    sys.path.insert(0, str(archive_path))

from table_extractor import (
    extract_table_from_text_block,
    make_descriptive_table_slug,
    parse_and_extract_all_tables,
    vietnamese_to_ascii,
)
