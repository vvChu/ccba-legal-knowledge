"""
CCBA Legal Knowledge Spoke — Sync Extracted Docs & Compute Checksums to Registry.
Đồng bộ toàn bộ file nguồn đã lưu trong .md/extracted_docs/ và tính toán mã băm SHA-256 chuẩn hóa vào legal_registry.yaml.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT_DIR / "legal_registry.yaml"
EXTRACTED_DIR = ROOT_DIR / ".md" / "extracted_docs"


def compute_sha256(file_path: Path) -> str:
    """Tính mã băm SHA-256 của file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def sync_registry_checksums() -> None:
    """Quét .md/extracted_docs/ và cập nhật toàn bộ sha256 vào legal_registry.yaml."""
    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Không tìm thấy {REGISTRY_FILE}")

    reg_data = yaml.safe_load(REGISTRY_FILE.read_text(encoding="utf-8"))
    laws = reg_data.get("laws", [])

    print("=================================================================")
    print("      CCBA EXTRACTED DOCS & SHA-256 REGISTRY SYNCHRONIZER        ")
    print("=================================================================")

    matched_count = 0
    for idx, doc in enumerate(laws, 1):
        doc_id = doc.get("id", "")
        doc_num = doc.get("document_number", "")
        bundle_path_str = doc.get("bundle_path", "")
        slug = Path(bundle_path_str).name if bundle_path_str else doc_id

        # Tìm file nguồn trong extracted_docs
        doc_extracted_dir = EXTRACTED_DIR / slug
        source_file: Path | None = None

        if doc_extracted_dir.exists():
            # Ưu tiên .docx, .pdf, .doc
            for ext in [".docx", ".pdf", ".doc"]:
                candidates = list(doc_extracted_dir.glob(f"*{ext}"))
                # Loại bỏ file tạm Word ~$
                candidates = [c for c in candidates if not c.name.startswith("~$")]
                if candidates:
                    source_file = candidates[0]
                    break

        if source_file and source_file.exists():
            sha256_hash = compute_sha256(source_file)
            size_kb = source_file.stat().st_size / 1024
            doc["sha256"] = sha256_hash
            doc["source_file"] = str(source_file.relative_to(ROOT_DIR))
            doc["source_file_size_kb"] = round(size_kb, 1)
            matched_count += 1
            print(
                f"{idx:02d}. [✅ MATCH] {doc_num:<20} | {source_file.name:<35} | "
                f"{size_kb:>7.1f} KB | SHA: {sha256_hash[:16]}..."
            )
        else:
            # Nếu có tệp markdown chính trong bundle, băm sha256 của markdown chính
            md_candidate = ROOT_DIR / bundle_path_str / f"{slug}.md"
            if md_candidate.exists():
                sha256_hash = compute_sha256(md_candidate)
                doc["sha256"] = sha256_hash
                matched_count += 1
                print(
                    f"{idx:02d}. [📄 MD   ] {doc_num:<20} | {md_candidate.name:<35} | "
                    f"{md_candidate.stat().st_size/1024:>7.1f} KB | SHA: {sha256_hash[:16]}..."
                )
            else:
                print(f"{idx:02d}. [⚠️ MISS ] {doc_num:<20} | Không tìm thấy file nguồn")

    REGISTRY_FILE.write_text(
        yaml.dump(reg_data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print("\n=================================================================")
    print(f"🎉 ĐÃ ĐỒNG BỘ {matched_count}/{len(laws)} MÃ BĂM SHA-256 VÀO REGISTRY!")
    print("=================================================================\n")


if __name__ == "__main__":
    sync_registry_checksums()
