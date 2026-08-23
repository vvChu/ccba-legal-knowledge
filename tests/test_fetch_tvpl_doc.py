import hashlib
import re
import tempfile
import unicodedata
from pathlib import Path
from typing import Any
import pytest
import yaml
from ccba_legal.crawler import MockChromeCDP, get_tvpl_metadata


def _normalize(text: str) -> str:
    """Normalize string by removing diacritics, punctuation, and lowering."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "D")
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def compute_file_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def find_doc_in_registry(
    key: str, registry_file: Path | None = None
) -> tuple[str | None, str | None, dict[str, Any] | None]:
    """Find a document in legal_registry.yaml by number, title, id, or URL."""
    reg_path = registry_file or (Path(__file__).resolve().parent.parent / "legal_registry.yaml")
    if not reg_path.exists():
        return None, None, None

    with open(reg_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    all_items: list[dict[str, Any]] = []
    for section in ["laws", "decrees", "circulars", "standards"]:
        all_items.extend(data.get(section, []))

    norm_key = _normalize(key)

    # 1. Exact match on URL
    if key.startswith("http://") or key.startswith("https://"):
        for item in all_items:
            if item.get("source_url") == key or item.get("tvpl_url") == key:
                return item.get("id"), key, item
        slug = re.sub(r"[^\w\d]+", "_", Path(key).stem.lower()).strip("_")
        return slug, key, None

    # 2. Match on document_number or id
    for item in all_items:
        doc_num = item.get("document_number", "")
        doc_id = item.get("id", "")
        if key == doc_num or key == doc_id or norm_key == _normalize(doc_num) or norm_key == _normalize(doc_id):
            url = item.get("tvpl_url") or item.get("source_url")
            slug = item.get("id", "").lower().replace("-", "_")
            return slug, url, item

    return None, None, None


def test_normalize_vietnamese_strings() -> None:
    """Test unicode and diacritic normalization for legal identifiers."""
    assert _normalize("QCVN 04:2021/BXD") == "qcvn 04 2021 bxd"
    assert _normalize("Nghị định 217/2026/NĐ-CP") == "nghi dinh 217 2026 nd cp"
    assert _normalize("Định mức") == "dinh muc"


def test_find_doc_in_registry_by_various_keys() -> None:
    """Test finding document slugs and URLs using various identifier formats."""
    # 1. Exact document number
    slug, url, item = find_doc_in_registry("217/2026/NĐ-CP")
    assert slug == "nghi_dinh_217_2026_nd_cp"
    assert "217-2026-ND-CP" in url

    # 2. QCVN Code
    slug, url, item = find_doc_in_registry("QCVN 04:2021/BXD")
    assert slug == "qcvn_04_2021_bxd"
    assert "474758.aspx" in url

    # 3. Direct URL
    direct_url = "https://thuvienphapluat.vn/van-ban/Xay-dung-Nha-o/Thong-tu-06-2022-TT-BXD-545609.aspx"
    slug, url, item = find_doc_in_registry(direct_url)
    assert slug == "thong_tu_06_2022_tt_bxd_545609"
    assert url == direct_url


def test_compute_file_sha256(tmp_path: Path) -> None:
    """Test SHA-256 calculation on a test file."""
    test_file = tmp_path / "test.docx"
    test_file.write_bytes(b"CCBA Legal Knowledge Platform 2026")
    sha = compute_file_sha256(test_file)
    assert len(sha) == 64
    assert isinstance(sha, str)


def test_mock_cdp_4_layer_precision_check(tmp_path: Path) -> None:
    """Test the complete 4-Layer Precision Check flow with MockChromeCDP."""
    mock_cdp = MockChromeCDP()
    pages = mock_cdp.get_pages()
    mock_cdp.connect_tab(pages[0]["webSocketDebuggerUrl"])

    test_meta = {
        "document_number": "217/2026/NĐ-CP",
        "type": "Nghị định",
        "issued_by": "Chính phủ",
        "signer": "Phạm Minh Chính",
        "issued_date": "25/06/2026",
        "effective_date": "01/07/2026",
        "status": "Còn hiệu lực",
        "relations": {
            "guiding_docs": [
                {
                    "title": "Thông tư 36/2026/TT-BXD",
                    "url": "https://thuvienphapluat.vn/van-ban/thong_tu_36_2026_tt_bxd.aspx",
                }
            ]
        },
    }
    mock_cdp.set_mock_metadata(test_meta)

    # Layer 1: Registry Lookup
    slug, url, reg_item = find_doc_in_registry("217/2026/NĐ-CP")
    assert slug == "nghi_dinh_217_2026_nd_cp"

    # Layer 2: Metadata Extraction
    metadata = get_tvpl_metadata(mock_cdp, url)
    assert metadata["document_number"] == "217/2026/NĐ-CP"
    assert metadata["type"] == "Nghị định"
    assert metadata["issued_by"] == "Chính phủ"
    assert metadata["issued_date"] == "2026-06-25"
    assert metadata["effective_date"] == "2026-07-01"

    # Layer 3: Status & Relations Check
    assert "Còn hiệu lực" in metadata["status"]
    assert "guiding_docs" in metadata["relations"]
    assert len(metadata["relations"]["guiding_docs"]) == 1

    # Layer 4: Three-tier Check
    doc_dir = tmp_path / slug
    doc_dir.mkdir(parents=True, exist_ok=True)
    doc_file = doc_dir / f"{slug}.docx"
    doc_file.write_bytes(b"Mock docx binary content")

    sha256 = compute_file_sha256(doc_file)
    assert len(sha256) == 64
