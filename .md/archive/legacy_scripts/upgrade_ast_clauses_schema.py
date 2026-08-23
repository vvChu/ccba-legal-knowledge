#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCBA AST & Registry Enrichment Tool
Upgrades legal_registry.yaml and clauses.json with:
- PDF Tracking (pdf_path, pdf_sha256, cong_bao_number, pdf_status)
- Jurisdiction Routing (jurisdiction: 'CQXD' | 'CONG_AN' | 'CHU_DAU_TU_TU_THAM_DINH')
- Transition & Grace Period (grace_period_end, compliance_severity)
- Page-Level PDF Ground Truth (source_pdf_page)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT_DIR / "legal_registry.yaml"
QCVN04_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_04_2021_bxd"
QCVN06_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"


def upgrade_registry() -> None:
    """Add rich PDF metadata schema to legal_registry.yaml."""
    print("--- 1. NÂNG CẤP SCHEMA legal_registry.yaml ---")
    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Registry file not found: {REGISTRY_FILE}")

    reg_text = REGISTRY_FILE.read_text(encoding="utf-8")
    data = yaml.safe_load(reg_text)

    # Cong Bao Mapping Table for Core Docs
    cong_bao_map = {
        "QCVN-04-2021-BXD": {"cong_bao": "373/2026 (SĐ1) / 235/2021", "pdf_slug": "qcvn_04_2021_bxd.pdf"},
        "QCVN-06-2022-BXD": {"cong_bao": "235+236/2023 (SĐ1) / 1141+1142/2022", "pdf_slug": "qcvn_06_2022_bxd.pdf"},
        "Luat-Phong-chay-chua-chay-va-cuu-nan-cuu-ho-2024-55-2024-QH15-621347": {"cong_bao": "1187+1188/2024", "pdf_slug": "luat_55_2024_qh15.pdf"},
        "Luat-Xay-dung-2025-135-2025-QH15": {"cong_bao": "1205+1206/2025", "pdf_slug": "luat_135_2025_qh15.pdf"},
        "Luat-Dau-thau-2023-22-2023-QH15": {"cong_bao": "789+790/2023", "pdf_slug": "luat_22_2023_qh15.pdf"},
    }

    laws = data.get("laws", [])
    updated_count = 0

    for item in laws:
        doc_id = item.get("id", "")
        bundle_path = item.get("bundle_path", "")
        
        # Set default PDF schema attributes if missing
        if "pdf_status" not in item:
            cb_info = cong_bao_map.get(doc_id, {})
            item["pdf_path"] = f"{bundle_path.rstrip('/')}/{cb_info.get('pdf_slug', f'{doc_id}.pdf')}" if bundle_path else ""
            item["pdf_sha256"] = ""
            item["cong_bao_number"] = cb_info.get("cong_bao", "Đang cập nhật")
            item["pdf_status"] = "pending_download"
            updated_count += 1

        # Check amendments
        rel = item.get("relations", {})
        if isinstance(rel, dict) and "amendments" in rel:
            for amd in rel.get("amendments", []):
                if isinstance(amd, dict) and "pdf_status" not in amd:
                    amd_id = amd.get("id", "")
                    amd["pdf_sha256"] = amd.get("sha256", "")
                    amd["cong_bao_number"] = "373/2026" if "SD1-2026" in amd_id else "235+236/2023"
                    amd["pdf_status"] = "pending_download"

    # Write back YAML cleanly
    REGISTRY_FILE.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )
    print(f"✅ Đã nâng cấp schema PDF metadata cho {updated_count} mục trong legal_registry.yaml")


def upgrade_qcvn04_clauses() -> None:
    """Enrich QCVN 04 clauses.json with jurisdiction, page, grace period."""
    print("\n--- 2. NÂNG CẤP AST clauses.json CHO QCVN 04:2021/BXD ---")
    clauses_file = QCVN04_DIR / "clauses.json"
    if not clauses_file.exists():
        raise FileNotFoundError(f"Missing {clauses_file}")

    clauses = json.loads(clauses_file.read_text(encoding="utf-8"))
    
    cqxd_count = 0
    congan_count = 0

    for item in clauses:
        cid = item.get("id", "")
        cnum = item.get("clause_number", "")
        title = item.get("title", "")
        content = item.get("content", "")
        full_text = f"{title} {content}".lower()

        # 1. Jurisdiction Routing
        # Water supply, fire hydrants, specific PCCC active systems -> CONG_AN
        if "cấp nước chữa cháy" in full_text or "họng nước" in full_text or "chữa cháy tự động" in full_text and "2.10.1" in cnum:
            item["jurisdiction"] = "CONG_AN"
            congan_count += 1
        else:
            # Building layout, apartment specs, parking bays, EV charging spaces, smoke exhaust, structure -> CQXD
            item["jurisdiction"] = "CQXD"
            cqxd_count += 1

        # 2. Transition & Grace Period Routing (ADR 0013)
        # Clauses amended by TT 31/2026 regarding EV charging in existing buildings
        is_ev_amendment = (
            cnum in ["1.1.3", "1.4.31", "1.4.32", "1.4.33", "1.4.34", "2.10.2.1"]
            or "xe điện" in full_text
            or "đổi pin" in full_text
            or "chung cư hiện hữu" in full_text
        )

        if is_ev_amendment:
            item["grace_period_end"] = "2027-06-15"
            item["compliance_severity"] = "WARNING_NOTICE"
            item["cong_bao_number"] = "373/2026"
            item["source_pdf_page"] = 96 if cnum == "2.10.2.1" else 95
        else:
            item["grace_period_end"] = None
            item["compliance_severity"] = "CRITICAL_DEFECT"
            item["cong_bao_number"] = "235/2021"
            item["source_pdf_page"] = None

        # Standardize anchor field
        item["clause_id"] = cid
        item["anchor"] = cid
        item["normative_status"] = "mandatory"
        item["legal_enforceability"] = True

    clauses_file.write_text(json.dumps(clauses, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Đã nâng cấp {len(clauses)} điều khoản QCVN 04:")
    print(f"   - Thẩm quyền CQXD (Sở Xây dựng) : {cqxd_count} ({cqxd_count/len(clauses)*100:.1f}%)")
    print(f"   - Thẩm quyền CÔNG AN (PC07)      : {congan_count} ({congan_count/len(clauses)*100:.1f}%)")


def upgrade_qcvn06_clauses() -> None:
    """Enrich QCVN 06 clauses.json with jurisdiction, page, grace period."""
    print("\n--- 3. NÂNG CẤP AST clauses.json CHO QCVN 06:2022/BXD ---")
    clauses_file = QCVN06_DIR / "clauses.json"
    if not clauses_file.exists():
        raise FileNotFoundError(f"Missing {clauses_file}")

    clauses = json.loads(clauses_file.read_text(encoding="utf-8"))
    
    cqxd_count = 0
    congan_count = 0

    for item in clauses:
        cid = item.get("clause_id", item.get("id", ""))
        title = item.get("title", "")
        full_text = f"{cid} {title}".lower()

        # Split Jurisdiction Routing according to Law 55/2024 & ND 105/2025:
        # - Chapter 5 (Water supply), Chapter 6 (Rescue/Fire Fighting equipment), Appendix F, G -> CONG_AN
        # - Chapter 1, 2, 3 (Escape paths/doors), Chapter 4 (Compartmentation/Smoke/Fire resistance), Appendix A, B, D, E, H -> CQXD
        is_congan = (
            cid.startswith("muc-5") 
            or cid.startswith("muc-6")
            or "phu-luc-f" in cid
            or "phu-luc-g" in cid
            or "cấp nước chữa cháy" in full_text
            or "trang bị phương tiện" in full_text
        )

        if is_congan:
            item["jurisdiction"] = "CONG_AN"
            congan_count += 1
        else:
            item["jurisdiction"] = "CQXD"
            cqxd_count += 1

        # Cong bao mapping
        # Sửa đổi 1:2023 (TT 09/2023)
        if "sửa đổi 1:2023" in full_text or "(sđ 1:2023)" in full_text:
            item["cong_bao_number"] = "235+236/2023"
            item["source_pdf_page"] = None
        else:
            item["cong_bao_number"] = "1141+1142/2022"
            item["source_pdf_page"] = None

        item["grace_period_end"] = None
        item["compliance_severity"] = "CRITICAL_DEFECT"

    clauses_file.write_text(json.dumps(clauses, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Đã nâng cấp {len(clauses)} điều khoản QCVN 06:")
    print(f"   - Thẩm quyền CQXD (Sở Xây dựng) : {cqxd_count} ({cqxd_count/len(clauses)*100:.1f}%)")
    print(f"   - Thẩm quyền CÔNG AN (PC07)      : {congan_count} ({congan_count/len(clauses)*100:.1f}%)")


def main() -> None:
    upgrade_registry()
    upgrade_qcvn04_clauses()
    upgrade_qcvn06_clauses()
    print("\n🎉 HOÀN TẤT NÂNG CẤP TOÀN BỘ AST VÀ REGISTRY METADATA!")


if __name__ == "__main__":
    main()
