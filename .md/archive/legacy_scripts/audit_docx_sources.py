"""Comprehensive Audit of all DOCX source files in .md/extracted_docs/."""

import docx
from pathlib import Path
import yaml
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

root = Path(__file__).resolve().parent.parent
extracted_dir = root / ".md" / "extracted_docs"
reg_file = root / "legal_registry.yaml"

with open(reg_file, "r", encoding="utf-8") as f:
    reg_data = yaml.safe_load(f)

all_docs = []
if "laws" in reg_data:
    all_docs.extend(reg_data["laws"])
if "documents" in reg_data:
    all_docs.extend(reg_data["documents"].values())

doc_map = {d.get("bundle_path", "").strip("/").split("/")[-1]: d for d in all_docs if d.get("bundle_path")}

print("=====================================================================================================================")
print("                   CCBA COMPREHENSIVE SOURCE DOCX ASSET INTEGRITY AUDIT                                              ")
print("=====================================================================================================================")
print(f"{'Slug / Bundle':<35} | {'DOCX File':<32} | {'Size KB':<10} | {'Paras':<6} | {'Tables':<6} | {'Chars':<8} | {'Status'}")
print("-" * 117)

suspicious_count = 0
ok_count = 0

for folder in sorted(extracted_dir.iterdir()):
    if not folder.is_dir():
        continue
    docx_files = list(folder.glob("*.docx"))
    if not docx_files:
        print(f"{folder.name:<35} | {'NO DOCX':<32} | {'0':<10} | {'0':<6} | {'0':<6} | {'0':<8} | ❌ MISSING")
        suspicious_count += 1
        continue

    for df in docx_files:
        size_kb = df.stat().st_size / 1024
        try:
            doc = docx.Document(str(df))
            paras = len(doc.paragraphs)
            tables = len(doc.tables)
            total_chars = sum(len(p.text) for p in doc.paragraphs)

            status = "✅ OK"
            if size_kb < 15 and paras < 20:
                status = "⚠️ SUSPICIOUS (Too small)"
                suspicious_count += 1
            else:
                ok_count += 1

            print(f"{folder.name[:33]:<35} | {df.name[:30]:<32} | {size_kb:<10.1f} | {paras:<6} | {tables:<6} | {total_chars:<8} | {status}")
        except Exception as e:
            print(f"{folder.name[:33]:<35} | {df.name[:30]:<32} | {size_kb:<10.1f} | {'ERR':<6} | {'ERR':<6} | {'ERR':<8} | ❌ CORRUPT: {e}")
            suspicious_count += 1

print("-" * 117)
print(f"📊 SUMMARY: Total DOCX Inspected: {ok_count + suspicious_count} | Genuine & Complete: {ok_count} | Suspicious/Missing: {suspicious_count}")
print("=====================================================================================================================")
