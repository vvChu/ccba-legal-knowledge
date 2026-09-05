"""sync_expansion_roadmap.py — Autonomous Living Document Engine for Legal Knowledge Expansion Roadmap.

Reads:
- legal_registry.yaml (SSOT of currently ingested bundles)
- .md/knowledge/expansion_candidates.yaml (Target catalog of legal candidates)
- legal_docs/**/*.md (Dynamic citation scanner across 7,181 clauses)

Outputs:
- .md/knowledge/expansion_roadmap.md (Living Document with auto-updated progress & tiers)
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
import yaml

# Ensure UTF-8 output on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(line_buffering=True, encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT_DIR / "legal_registry.yaml"
CANDIDATES_FILE = ROOT_DIR / ".md" / "knowledge" / "expansion_candidates.yaml"
ROADMAP_OUTPUT_FILE = ROOT_DIR / ".md" / "knowledge" / "expansion_roadmap.md"
LEGAL_DOCS_DIR = ROOT_DIR / "legal_docs"


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def scan_citations_across_corpus(candidate_doc_nums: list[str]) -> dict[str, int]:
    """Scans all markdown files in legal_docs/ for mentions of candidate document numbers.
    Excludes constituent drafts in 'sources/' to avoid duplicate counting.
    """
    counts = {num: 0 for num in candidate_doc_nums}

    # Pre-compile normalized regex for each doc num
    regexes = {}
    for num in candidate_doc_nums:
        clean_num = num.strip()
        if clean_num.upper().startswith(("QCVN", "TCVN")):
            base_num = clean_num.split("/")[0].strip()  # 'QCVN 10:2024' or 'TCVN 5575:2024'
            pattern = re.escape(base_num).replace(r"\ ", r"\s*")
        elif "/" in clean_num:
            # Handle administrative documents (e.g. 10/2024/TT-BXD) without cutting at first slash
            parts = clean_num.split("/")
            if len(parts) >= 2 and parts[1].isdigit():
                pattern = rf"\b{re.escape(parts[0])}/{re.escape(parts[1])}(?:/{re.escape(parts[2])})?\b" if len(parts) >= 3 else rf"\b{re.escape(clean_num)}\b"
            else:
                pattern = rf"\b{re.escape(clean_num)}\b"
        else:
            pattern = rf"\b{re.escape(clean_num)}\b"
        regexes[num] = re.compile(pattern, re.IGNORECASE)

    for md_file in LEGAL_DOCS_DIR.rglob("*.md"):
        # Exclude sources/ to prevent duplicate counting of raw constituent drafts
        if "sources" in md_file.parts:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            for num, reg in regexes.items():
                matches = len(reg.findall(content))
                if matches > 0:
                    counts[num] += matches
        except Exception:
            continue

    return counts


def get_ingested_document_numbers() -> set[str]:
    """Retrieves all document numbers currently registered in legal_registry.yaml."""
    reg = load_yaml(REGISTRY_FILE)
    ingested = set()
    
    for k, v in reg.items():
        if isinstance(v, list):
            for doc in v:
                doc_num = doc.get("document_number")
                if doc_num:
                    ingested.add(doc_num.strip().upper())
                doc_id = doc.get("id")
                if doc_id:
                    ingested.add(doc_id.strip().upper())
                    
    # Also scan bundle directories in legal_docs/
    for b_dir in LEGAL_DOCS_DIR.glob("*/*"):
        if b_dir.is_dir():
            meta = load_yaml(b_dir / "metadata.yaml")
            if meta.get("document_number"):
                ingested.add(meta["document_number"].strip().upper())
            ingested.add(b_dir.name.upper())

    return ingested


def sync_roadmap() -> dict[str, Any]:
    """Main execution engine to compile and refresh the Living Roadmap."""
    candidates_data = load_yaml(CANDIDATES_FILE)
    candidates: list[dict[str, Any]] = candidates_data.get("candidates", [])
    
    ingested_set = get_ingested_document_numbers()
    doc_nums = [c["document_number"] for c in candidates]
    citations_map = scan_citations_across_corpus(doc_nums)
    
    tier_groups: dict[int, list[dict[str, Any]]] = {1: [], 2: [], 3: [], 4: []}
    ingested_candidates: list[dict[str, Any]] = []
    
    for c in candidates:
        num = c["document_number"]
        norm_num = num.strip().upper()
        c_id = c.get("id", "").strip().upper()
        
        # Check if already ingested
        is_ingested = norm_num in ingested_set or c_id in ingested_set
        citations = citations_map.get(num, 0)
        c["citations"] = citations
        
        # Compute dynamic score
        base_score = float(c.get("base_impact_score", 7.0))
        bonus = min(0.5, citations * 0.05)
        final_score = round(base_score + bonus, 1)
        c["final_score"] = final_score
        
        tier = c.get("tier_override", 1)
        if is_ingested:
            c["status"] = "INGESTED"
            ingested_candidates.append(c)
        else:
            c["status"] = "PENDING"
            tier_groups[tier].append(c)
            
    # Sort tiers by final_score descending
    for t in tier_groups:
        tier_groups[t].sort(key=lambda x: x["final_score"], reverse=True)
    pending_count = sum(len(v) for v in tier_groups.values())

    # Dynamic document count from legal_registry.yaml or valid bundle directories
    reg = load_yaml(REGISTRY_FILE)
    reg_summary = reg.get("registry_summary", {})
    if "total_documents" in reg_summary and isinstance(reg_summary["total_documents"], int) and reg_summary["total_documents"] > 0:
        current_registry_total = reg_summary["total_documents"]
    else:
        current_registry_total = len([
            b for b in LEGAL_DOCS_DIR.glob("*/*")
            if b.is_dir() and (b / "metadata.yaml").exists()
        ])
    total_projected = current_registry_total + pending_count

    # Render Markdown Document
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md_content = f"""# 🗺️ Bản Đồ Chiến Lược & Lộ Trình Mở Rộng Kho Tri Thức Pháp Lý CCBA
## (Living Knowledge Expansion Roadmap — OKF v2.4 Universal)

> [!NOTE]
> **Đây là Tài Liệu Sống (Living Document) tự động cập nhật.**  
> Được đồng bộ tự động bởi `scripts/sync_expansion_roadmap.py` mỗi khi có văn bản mới được nạp vào Spoke hoặc khi chạy Master CI Gate.  
> **Lần cập nhật cuối:** `{now_str}` | **Tiêu chuẩn:** OKF v2.4 Universal (ADRs 0021–0041)

---

## 📊 I. Bảng Đồng Hồ Tiến Độ Số Hóa (Live Ingestion KPI)

| Chỉ số theo dõi | Số lượng | Tỷ lệ hoàn thành | Trạng thái hệ thống |
|:---|:---:|:---:|:---:|
| **Hiện có trong Spoke (Active Bundles)** | **{current_registry_total}** | **{current_registry_total/total_projected*100:.1f}%** | 🟢 Sẵn sàng phục vụ Agent |
| **Ứng viên Đang Chờ Nạp (Pending Target)** | **{pending_count}** | **{pending_count/total_projected*100:.1f}%** | 🟡 Trong lộ trình ưu tiên |
| **Tổng quy mô mục tiêu giai đoạn 1** | **{total_projected}** | **100.0%** | 🚀 Bao phủ toàn diện 4 bộ môn |

---

## 🧭 II. Bản Đồ Phân Tầng Trực Quan (Live Tiering Radar)

```mermaid
graph TD
    subgraph T1["🔴 TIER 1: QUY CHUẨN KỸ THUẬT BẮT BUỘC & PCCC ({len(tier_groups[1])} Văn bản)"]
"""
    for idx, c in enumerate(tier_groups[1], 1):
        md_content += f'        T1_{idx}["{c["document_number"]}<br/>({c["discipline"]} - Điểm: {c["final_score"]})"]\n'
    md_content += """    end

    subgraph T2["🟠 TIER 2: TIÊU CHUẨN THIẾT KẾ CỐT LÕI ĐA BỘ MÔN (""" + f"{len(tier_groups[2])}" + """ Văn bản)"]\n"""
    for idx, c in enumerate(tier_groups[2], 1):
        md_content += f'        T2_{idx}["{c["document_number"]}<br/>({c["discipline"]} - Điểm: {c["final_score"]})"]\n'
    md_content += """    end

    subgraph T3["🟡 TIER 3: HẠ TẦNG KỸ THUẬT & ĐỊA KỸ THUẬT (""" + f"{len(tier_groups[3])}" + """ Văn bản)"]\n"""
    for idx, c in enumerate(tier_groups[3], 1):
        md_content += f'        T3_{idx}["{c["document_number"]}<br/>({c["discipline"]} - Điểm: {c["final_score"]})"]\n'
    md_content += """    end

    subgraph T4["🔵 TIER 4: THỂ LOẠI CÔNG TRÌNH & BIM ISO (""" + f"{len(tier_groups[4])}" + """ Văn bản)"]\n"""
    for idx, c in enumerate(tier_groups[4], 1):
        md_content += f'        T4_{idx}["{c["document_number"]}<br/>({c["discipline"]} - Điểm: {c["final_score"]})"]\n'
    md_content += """    end

    T1 --> T2
    T2 --> T3
    T3 --> T4
```

---

## 📋 III. Chi Tiết Các Tầng Ưu Tiên & Mã Lệnh Nạp Tự Động

"""
    tier_titles = {
        1: "🔴 TIER 1: Quy Chuẩn Kỹ Thuật Quốc Gia Bắt Buộc & An Toàn PCCC",
        2: "🟠 TIER 2: Tiêu Chuẩn Thiết Kế Cơ Sở Đa Bộ Môn (Kết Cấu, MEP)",
        3: "🟡 TIER 3: Hạ Tầng Kỹ Thuật Đô Thị & Địa Kỹ Thuật Nền Móng",
        4: "🔵 TIER 4: Chuẩn Hóa Thể Loại Công Trình & Quản Trị BIM ISO",
    }
    
    for t_idx in [1, 2, 3, 4]:
        t_list = tier_groups[t_idx]
        md_content += f"### {tier_titles[t_idx]}\n\n"
        if not t_list:
            md_content += "*✅ Đã hoàn thành 100% các văn bản trong tầng này!*\n\n"
            continue
            
        md_content += "| STT | Ký hiệu văn bản | Tên quy chuẩn / tiêu chuẩn | Bộ môn | Viện dẫn | Điểm | Lệnh nạp 1-Command (Universal Ingest) |\n"
        md_content += "|:---:|:---|:---|:---:|:---:|:---:|:---|\n"
        for s_idx, c in enumerate(t_list, 1):
            target = c.get('search_query', c['document_number'])
            cmd = f"`python -m ccba_legal ingest \"{target}\" --category {c['category']} --upload-drive`"
            md_content += f"| {s_idx} | **[{c['document_number']}]({c['tvpl_url']})** | {c['title']} | {c['discipline']} | {c['citations']} | **{c['final_score']}** | {cmd} |\n"
        md_content += "\n"

    # Completed Section
    if ingested_candidates:
        md_content += "## ✅ IV. Danh Mục Ứng Viên Đã Được Nạp Hoàn Tất\n\n"
        md_content += "| Ký hiệu | Tên văn bản | Bộ môn | Ngày có hiệu lực | Trạng thái |\n"
        md_content += "|:---|:---|:---:|:---:|:---:|\n"
        for c in ingested_candidates:
            md_content += f"| **{c['document_number']}** | {c['title']} | {c['discipline']} | {c.get('effective_date', 'N/A')} | 🟢 `INGESTED` |\n"
        md_content += "\n"

    md_content += """---

## 🛠️ V. Giao Thức Tự Đồng Bộ & Tự Lành (Self-Healing Protocol)

Living Document này được bảo vệ và cập nhật tự động qua các cơ chế:
1. **Sau mỗi lệnh nạp mới (`ingest`)**: Engine tự động kiểm tra `legal_registry.yaml`, nhận diện văn bản mới và chuyển trạng thái từ `PENDING` $\\rightarrow$ `INGESTED`.
2. **Khi chạy Master CI Validator (`scripts/validate_legal_spoke.py`)**: Gate 10 tự động gọi `sync_expansion_roadmap.py` để tính toán lại điểm trích dẫn và đồng bộ thứ tự ưu tiên.
"""

    ROADMAP_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if ROADMAP_OUTPUT_FILE.exists():
        existing_text = ROADMAP_OUTPUT_FILE.read_text(encoding="utf-8")
        existing_substantive = re.sub(r">\s*\*\*Lần cập nhật cuối:\*\*.*", "", existing_text).strip()
        new_substantive = re.sub(r">\s*\*\*Lần cập nhật cuối:\*\*.*", "", md_content).strip()
        if existing_substantive == new_substantive:
            print(f"ℹ️ Living Expansion Roadmap is up to date (no substantive changes).")
            return {
                "status": "up_to_date",
                "current_total": current_registry_total,
                "pending_count": pending_count,
                "total_projected": total_projected,
                "output_file": str(ROADMAP_OUTPUT_FILE),
            }

    ROADMAP_OUTPUT_FILE.write_text(md_content, encoding="utf-8")
    print(f"✅ Successfully compiled Living Expansion Roadmap at: {ROADMAP_OUTPUT_FILE}")
    print(f"   - Current Spoke Total : {current_registry_total}")
    print(f"   - Pending Candidates  : {pending_count}")
    print(f"   - Total Projected     : {total_projected}")
    
    return {
        "status": "success",
        "current_total": current_registry_total,
        "pending_count": pending_count,
        "total_projected": total_projected,
        "output_file": str(ROADMAP_OUTPUT_FILE),
    }


if __name__ == "__main__":
    sync_roadmap()
