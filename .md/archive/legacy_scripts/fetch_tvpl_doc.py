"""Fetch and download official TVPL legal documents (.docx and .pdf) via Hub ccba-legal-intel."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from ccba_legal import (
    ChromeCDP,
    ChromeCDPError,
    download_three_tier,
    get_tvpl_credentials,
    get_tvpl_metadata,
    sleep_with_jitter,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT_DIR / "legal_registry.yaml"

# Load local environment variables (.gitignore-protected)
load_dotenv(ROOT_DIR / ".env")


def _normalize(s: str) -> str:
    """Normalize Vietnamese unicode string for fuzzy comparison."""
    if not s:
        return ""
    s = s.replace("đ", "d").replace("Đ", "D")
    nfkd = unicodedata.normalize("NFKD", s)
    no_diacritics = "".join(c for c in nfkd if not unicodedata.combining(c))
    cleaned = re.sub(r"[^\w\s]", " ", no_diacritics.lower())
    return " ".join(cleaned.split())


def compute_file_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def _extract_slug(item: dict[str, Any], default_id: str) -> str:
    bundle_path = item.get("bundle_path", "")
    if bundle_path:
        return Path(bundle_path).name
    return default_id.lower().replace("-", "_")


def find_doc_in_registry(key: str) -> tuple[str, str, dict[str, Any]]:
    """Look up document in legal_registry.yaml by number, slug, or TVPL URL."""
    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Registry not found: {REGISTRY_FILE}")

    with open(REGISTRY_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    docs_dict: dict[str, Any] = data.get("documents", {})
    laws_list: list[dict[str, Any]] = data.get("laws", [])

    all_items: list[tuple[str, dict[str, Any]]] = []
    for slug, item in docs_dict.items():
        all_items.append((slug, item))
    for law in laws_list:
        slug = _extract_slug(law, law.get("id", ""))
        all_items.append((slug, law))

    norm_key = _normalize(key)

    # 1. Exact or normalized document number / slug match
    for slug, item in all_items:
        doc_num = item.get("document_number", "")
        qcvn_code = item.get("qcvn_code", "")
        item_id = item.get("id", "")
        source_url = item.get("source_url", "")

        if key in (slug, doc_num, qcvn_code, item_id, source_url):
            return slug, source_url, item
        if norm_key in (_normalize(slug), _normalize(doc_num), _normalize(qcvn_code), _normalize(item_id)):
            return slug, source_url, item

    # 2. Check direct URL pattern (extract clean slug from URL stem)
    if "thuvienphapluat.vn" in key:
        stem = Path(key.split("?")[0].split("#")[0]).stem
        url_slug = _normalize(stem).replace(" ", "_")
        return url_slug, key, {}

    raise ValueError(f"Document identifier '{key}' not found in registry.")


def fetch_tvpl_document(
    doc_identifier: str,
    port: int = 9222,
    skip_verify: bool = False,
) -> bool:
    """Fetch and download a legal document using Hub ccba-legal-intel."""
    print(f"\n============================================================")
    print(f"  CCBA TVPL FETCHER (Hub ccba-legal-intel Engine)")
    print(f"============================================================")

    # Ensure credentials are configured
    try:
        user, _ = get_tvpl_credentials()
        print(f"[Auth] Verified TVPL VIP account configuration: '{user}'")
    except OSError as e:
        print(f"[Auth Error] {e}")
        return False

    slug, url, reg_item = find_doc_in_registry(doc_identifier)
    print(f"[Registry] Found: Slug='{slug}' | URL='{url}'")

    dest_dir = ROOT_DIR / ".md" / "extracted_docs" / slug
    dest_dir.mkdir(parents=True, exist_ok=True)

    cdp: ChromeCDP | None = None
    try:
        cdp = ChromeCDP(port=port)
        pages = cdp.get_pages()
        if not pages:
            print("[Error] No open Chrome tab found on port 9222.")
            return False

        ws_url = pages[0].get("webSocketDebuggerUrl")
        cdp.connect_tab(ws_url)

        if not skip_verify:
            print("[Step 1] Verifying metadata from TVPL...")
            meta = get_tvpl_metadata(cdp, url)
            print(f"  - Số hiệu: {meta.get('document_number')}")
            print(f"  - Tình trạng: {meta.get('status')}")

        print("[Step 2] Executing Three-Tier Download (Tier 1 -> Tier 2 -> Tier 3)...")
        success = download_three_tier(cdp, dest_dir, slug)
        if success:
            print(f"✅ [SUCCESS] Document '{slug}' downloaded to: {dest_dir}")
            return True
        else:
            print(f"❌ [FAILURE] Could not download '{slug}'.")
            return False
    except Exception as e:
        print(f"❌ [ERROR] Crawler execution failed: {e}")
        return False
    finally:
        if cdp:
            cdp.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download official legal document from TVPL with ccba-legal-intel"
    )
    parser.add_argument(
        "doc",
        help="Document Slug, Number (e.g. 217/2026/NĐ-CP), or TVPL URL",
    )
    parser.add_argument(
        "--port", "-p", help="CDP Port", default=9222, type=int
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip strict metadata comparison",
    )

    args = parser.parse_args()
    ok = fetch_tvpl_document(
        args.doc,
        port=args.port,
        skip_verify=args.skip_verify,
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
