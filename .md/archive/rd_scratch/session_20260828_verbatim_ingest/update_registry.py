import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import yaml
from pathlib import Path

registry_path = Path("legal_registry.yaml")

with open(registry_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# Update registry summary
data["registry_summary"]["total_documents"] = data["registry_summary"].get("total_documents", 33) + 1
data["registry_summary"]["categories"]["02_qcvn"] = data["registry_summary"]["categories"].get("02_qcvn", 4) + 1

new_entry = {
    "id": "QCVN-03-2022-BXD",
    "document_number": "QCVN 03:2022/BXD",
    "title": "QCVN 03:2022/BXD — Quy chuẩn kỹ thuật quốc gia về Phân cấp công trình phục vụ thiết kế xây dựng",
    "type": "Quy chuẩn kỹ thuật quốc gia",
    "issued_by": "Bộ Xây dựng",
    "signer": "Lê Quang Hùng",
    "issued_date": "2022-11-30",
    "effective_date": "2023-06-01",
    "status": "active",
    "bundle_path": "legal_docs/02_qcvn/qcvn_03_2022_bxd/",
    "source_url": "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Thong-tu-05-2022-TT-BXD-Quy-chuan-QCVN-03-2022-BXD-phan-cap-cong-trinh-thiet-ke-xay-dung-543956.aspx",
    "pdf_path": "legal_docs/02_qcvn/qcvn_03_2022_bxd/sources/qcvn_03_2022_bxd.pdf",
    "pdf_sha256": "f0f1a871b1a73ac209911f508ab8f64999ec39237a6538d2b71a08a5b277e380",
    "cong_bao_number": "05/2022/TT-BXD",
    "pdf_status": "verified",
    "sha256": "cfaf62f9de163aefc4bfd18f20965b9fea139a65e60cb3ae4554c6c2c881cfad",
    "source_file": ".md\\extracted_docs\\qcvn_03_2022_bxd\\qcvn_03_2022_bxd.docx",
    "source_file_size_kb": 13.4,
    "source_assets": {
        "docx": {
            "sha256": "cfaf62f9de163aefc4bfd18f20965b9fea139a65e60cb3ae4554c6c2c881cfad",
            "vault_path": "CCBA_Legal_Vault/02_qcvn/qcvn_03_2022_bxd/qcvn_03_2022_bxd.docx",
            "status": "synced"
        },
        "pdf": {
            "sha256": "f0f1a871b1a73ac209911f508ab8f64999ec39237a6538d2b71a08a5b277e380",
            "vault_path": "CCBA_Legal_Vault/02_qcvn/qcvn_03_2022_bxd/qcvn_03_2022_bxd.pdf",
            "status": "verified"
        }
    },
    "relations": {
        "replaces": "QCVN-03-2012-BXD"
    }
}

# Find insertion index in data["laws"] (after QCVN-02-2022-BXD)
insert_idx = None
for i, item in enumerate(data["laws"]):
    if item.get("id") == "QCVN-02-2022-BXD":
        insert_idx = i + 1
        break

# Filter out if already exists
data["laws"] = [item for item in data["laws"] if item.get("id") != "QCVN-03-2022-BXD"]

if insert_idx is not None:
    data["laws"].insert(insert_idx, new_entry)
else:
    data["laws"].append(new_entry)

with open(registry_path, "w", encoding="utf-8") as f:
    yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

print("✅ Updated legal_registry.yaml with QCVN-03-2022-BXD")
