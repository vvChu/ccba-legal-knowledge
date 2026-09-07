"""sync_adr_matrix.py - ADR Compiler, Traceability Matrix & Skill Impact Radar."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

# Ensure UTF-8 output on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(line_buffering=True, encoding="utf-8")

# Define Pillar Classification Mapping
PILLAR_MAPPING: dict[str, list[int]] = {
    "Trụ Cột 1: Tiêu Chuẩn Định Dạng Tri Thức OKF v2.4 Universal & Biểu Mẫu": [
        1, 2, 3, 4, 5, 21, 22, 27, 28, 29, 30, 34, 36, 37, 38, 39, 40, 41, 42
    ],
    "Trụ Cột 2: PDF Mỏ Neo Pháp Lý & Tri-Tier Cloud Vault (Acquisition, Anchoring & Vault)": [
        10, 16, 24, 25, 31, 35
    ],
    "Trụ Cột 3: Bộ Cổng Kiểm Định CI & Vận Hành Spoke (CI Gates & Operations)": [
        6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19, 20, 23, 26, 32, 33
    ],
}


def parse_adr_file(adr_path: Path) -> dict[str, Any]:
    """Extract metadata from an ADR markdown file with self-describing frontmatter support."""
    content = adr_path.read_text(encoding="utf-8")

    # Extract ID and Title from H1 (supporting En-dash \u2013 and Em-dash \u2014)
    h1_match = re.search(r"^#\s*ADR\s*0*([0-9]+)[:\s\u2013\u2014-]+(.*)$", content, re.MULTILINE | re.IGNORECASE)
    if h1_match:
        adr_num = int(h1_match.group(1))
        adr_title = h1_match.group(2).strip(" :—–-")
    else:
        # Fallback to filename
        fname_match = re.match(r"^0*([0-9]+)-(.*)\.md$", adr_path.name)
        if fname_match:
            adr_num = int(fname_match.group(1))
            adr_title = fname_match.group(2).replace("-", " ").title()
        else:
            adr_num = 0
            adr_title = adr_path.stem

    # Extract Status (supporting bullet or raw bold)
    status = "ACCEPTED"
    status_match = re.search(r"##\s*1\.\s*Trạng Thái\s*\(Status\)\s*\n\s*(?:-\s*)?\*\*([A-Z_]+)", content, re.IGNORECASE)
    if status_match:
        status = status_match.group(1).upper()
    elif "DEPRECATED" in content[:400]:
        status = "DEPRECATED"
    elif "SUPERSEDED" in content[:400]:
        status = "SUPERSEDED"

    # Extract Date
    date_str = ""
    date_match = re.search(r"\b(202[0-9]-[0-1][0-9]-[0-3][0-9])\b", content)
    if date_match:
        date_str = date_match.group(1)

    # Extract Pillar if specified in YAML frontmatter or content for self-evolution
    pillar: int | str | None = None
    fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        p_match = re.search(r"^pillar:\s*([^\n\r]+)", fm_match.group(1), re.MULTILINE | re.IGNORECASE)
        if p_match:
            raw_p = p_match.group(1).strip().strip("\"'")
            pillar = int(raw_p) if raw_p.isdigit() else raw_p

    return {
        "num": adr_num,
        "num_str": f"{adr_num:04d}",
        "title": adr_title,
        "filename": adr_path.name,
        "status": status,
        "date": date_str,
        "pillar": pillar,
        "path": adr_path,
        "content": content,
    }


def compile_adr_readme(adr_list: list[dict[str, Any]], target_file: Path) -> str:
    """Generate docs/adr/README.md from list of ADRs with dynamic self-describing pillar support."""
    adr_by_num = {a["num"]: a for a in adr_list}
    all_assigned_nums: set[int] = set()

    # Dynamic pillar assignment for self-evolving ADRs
    pillar_keys = list(PILLAR_MAPPING.keys())
    dynamic_mapping: dict[str, list[int]] = {k: list(v) for k, v in PILLAR_MAPPING.items()}
    for adr in adr_list:
        p_val = adr.get("pillar")
        num = adr["num"]
        if p_val and not any(num in nums for nums in dynamic_mapping.values()):
            if isinstance(p_val, int) and 1 <= p_val <= len(pillar_keys):
                dynamic_mapping[pillar_keys[p_val - 1]].append(num)
            elif isinstance(p_val, str):
                for p_key in pillar_keys:
                    if p_val.lower() in p_key.lower():
                        dynamic_mapping[p_key].append(num)
                        break

    lines = [
        "# 🏛️ CCBA Legal Knowledge Spoke — Architectural Decision Records (ADRs)",
        "",
        "Tài liệu này lưu trữ toàn bộ các Quyết định Kiến trúc (ADRs) định hình tiêu chuẩn đóng gói tri thức pháp lý **OKF v2.4 Universal Agent-Centric**, mỏ neo PDF Công báo gốc và hệ thống cổng kiểm định chất lượng tự động hóa.",
        "",
        "*(Tệp này được biên dịch tự động bởi `scripts/sync_adr_matrix.py` — Không chỉnh sửa thủ công)*",
        "",
        "---",
        "",
        f"## 📑 Danh Mục Quyết Định Kiến Trúc ({adr_list[0]['num_str']} — {adr_list[-1]['num_str']})",
        "",
    ]

    for pillar_title, num_list in dynamic_mapping.items():
        lines.append(f"### {pillar_title}")
        lines.append("| Mã ADR | Tiêu đề | Trạng thái | Ngày ban hành |")
        lines.append("| :--- | :--- | :---: | :---: |")
        sorted_nums = sorted(set(num_list))
        for num in sorted_nums:
            if num in adr_by_num:
                adr = adr_by_num[num]
                all_assigned_nums.add(num)
                status_icon = "✅ ACCEPTED" if adr["status"] == "ACCEPTED" else f"⚠️ {adr['status']}"
                date_display = adr["date"] or "N/A"
                lines.append(
                    f"| [ADR {adr['num_str']}]({adr['filename']}) | {adr['title']} | {status_icon} | {date_display} |"
                )
        lines.append("")
        lines.append("---")
        lines.append("")

    # Any unassigned ADRs
    unassigned = [a for a in adr_list if a["num"] not in all_assigned_nums]
    if unassigned:
        lines.append("### 📌 Các Quyết Định Khác (Unassigned)")
        lines.append("| Mã ADR | Tiêu đề | Trạng thái | Ngày ban hành |")
        lines.append("| :--- | :--- | :---: | :---: |")
        for adr in unassigned:
            status_icon = "✅ ACCEPTED" if adr["status"] == "ACCEPTED" else f"⚠️ {adr['status']}"
            date_display = adr["date"] or "N/A"
            lines.append(
                f"| [ADR {adr['num_str']}]({adr['filename']}) | {adr['title']} | {status_icon} | {date_display} |"
            )
        lines.append("")

    new_content = "\n".join(lines).strip() + "\n"
    target_file.write_text(new_content, encoding="utf-8")
    return new_content


def scan_skill_radar(adr_list: list[dict[str, Any]], root_dir: Path) -> dict[str, list[dict[str, str]]]:
    """Scan all SKILL.md, AGENTS.md, registry, and core CI scripts across Spoke and Hub to detect ADR references."""
    matrix: dict[str, list[dict[str, str]]] = {a["num_str"]: [] for a in adr_list}

    target_paths: list[Path] = []
    # Search skills
    skills_dir = root_dir / ".agents" / "skills"
    if skills_dir.exists():
        target_paths.extend(skills_dir.glob("*/SKILL.md"))

    # Core files and constitutional CI scripts (Whitelisted Targets to avoid noise)
    core_candidates = [
        "AGENTS.md",
        ".agents/AGENTS.md",
        "CONTEXT.md",
        "legal_registry.yaml",
        ".md/knowledge/session_learnings.md",
        "scripts/validate_legal_spoke.py",
        "scripts/lint_visual_parity.py",
        "scripts/spoke_cli.py",
    ]
    for core_f in core_candidates:
        p = root_dir / core_f
        if p.exists() and p not in target_paths:
            target_paths.append(p)

    target_paths.sort()

    for doc_path in target_paths:
        text = doc_path.read_text(encoding="utf-8")
        rel_path = str(doc_path.relative_to(root_dir)).replace("\\", "/")

        # Regex to find ADR references
        matches = re.findall(r"\bADR[-\s]*0*([0-9]+)\b", text, re.IGNORECASE)
        for m in matches:
            num = int(m)
            num_str = f"{num:04d}"
            if num_str in matrix:
                if rel_path not in [item["file"] for item in matrix[num_str]]:
                    matrix[num_str].append({"file": rel_path})

    return matrix


def compile_traceability_matrix(
    adr_list: list[dict[str, Any]],
    matrix: dict[str, list[dict[str, str]]],
    target_file: Path,
) -> str:
    """Generate docs/adr/TRACEABILITY_MATRIX.md with deterministic sorting (idempotent output)."""
    lines = [
        "# 🗺️ Living Architecture Traceability Matrix & Skill Radar",
        "",
        "> **Mục tiêu:** Ma trận tự động theo dõi mối quan hệ giữa các **Quyết định Kiến trúc (ADR)** và các **Kỹ năng (Skills) / Hiến pháp Vận hành**.",
        "",
        "*(Tệp này được biên dịch tự động bởi `scripts/sync_adr_matrix.py` — Không chỉnh sửa thủ công)*",
        "",
        "---",
        "",
        "| Mã ADR | Tiêu đề Quyết Định | Trạng thái | Tài Liệu & Skills Đang Tuân Thủ / Viện Dẫn |",
        "| :--- | :--- | :---: | :--- |",
    ]

    for adr in adr_list:
        num_str = adr["num_str"]
        refs = sorted(matrix.get(num_str, []), key=lambda r: r["file"])
        status_icon = "✅ ACCEPTED" if adr["status"] == "ACCEPTED" else f"⚠️ {adr['status']}"
        if refs:
            ref_links = "<br>".join([f"`{r['file']}`" for r in refs])
        else:
            ref_links = "*Chưa có liên kết trực tiếp*"

        lines.append(
            f"| [ADR {num_str}]({adr['filename']}) | **{adr['title']}** | {status_icon} | {ref_links} |"
        )

    lines.append("")
    new_content = "\n".join(lines).strip() + "\n"
    target_file.write_text(new_content, encoding="utf-8")
    return new_content


def main() -> None:
    root_dir = Path.cwd()
    adr_dir = root_dir / "docs" / "adr"
    if not adr_dir.exists():
        print(f"[ERROR] ADR directory not found at: {adr_dir}")
        sys.exit(1)

    # 1. Load all ADR files
    adr_files = sorted(
        [f for f in adr_dir.glob("*.md") if f.name not in ("README.md", "TRACEABILITY_MATRIX.md")]
    )
    adr_list = [parse_adr_file(f) for f in adr_files]
    adr_list.sort(key=lambda x: x["num"])

    print(f"[sync_adr_matrix] Found {len(adr_list)} ADRs in {adr_dir.relative_to(root_dir)}")

    # 2. Compile README.md
    readme_path = adr_dir / "README.md"
    compile_adr_readme(adr_list, readme_path)
    print(f"[sync_adr_matrix] Successfully compiled: {readme_path.relative_to(root_dir)}")

    # 3. Scan Skill Radar & Compile Traceability Matrix
    matrix = scan_skill_radar(adr_list, root_dir)
    trace_path = adr_dir / "TRACEABILITY_MATRIX.md"
    compile_traceability_matrix(adr_list, matrix, trace_path)
    print(f"[sync_adr_matrix] Successfully compiled: {trace_path.relative_to(root_dir)}")

    # Print summary
    total_refs = sum(len(refs) for refs in matrix.values())
    print(f"[sync_adr_matrix] Total active cross-references tracked: {total_refs}")


if __name__ == "__main__":
    main()
