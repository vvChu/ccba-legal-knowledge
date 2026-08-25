"""CCBA Catalog Query Gate — ADR 0032.

Cưỡng chế Reuse-First bằng cơ chế verify-based 2 lớp:
- Planning Gate  (--layer planning):  xác nhận intent, không block.
- Pre-execution Gate (--layer pre_exec): block nếu Hub tool đã có.

Usage:
    python scripts/query_hub_catalog.py --intent "fetch document from TVPL"
    python scripts/query_hub_catalog.py --intent "formula extraction" --layer pre_exec
    python scripts/query_hub_catalog.py --intent "..." --layer pre_exec \\
        --bypass --bypass-reason "Hub tool chưa cover edge case X"
    python scripts/query_hub_catalog.py --intent "..." --catalog path/to/catalog.yaml

Exit codes:
    0 — PASS, BYPASS, NO_MATCH
    1 — BLOCK
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

import yaml

# ── Encoding fix for Windows PowerShell ──────────────────────────────────────
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ── Project paths (relative to this script's location) ───────────────────────
_ROOT = Path(__file__).parent.parent
_DEFAULT_CATALOG = _ROOT / ".agents" / "skills" / "platform-loader" / "catalog.yaml"
_AUDIT_LOG = _ROOT / ".md" / "logs" / "catalog_gate_audit.jsonl"

# ── Capability keywords grouped by Hub capability (ADR 0032) ──────────────────
CAPABILITY_KEYWORDS: dict[str, list[str]] = {
    "fetch_group":    ["fetch", "crawl", "download", "requests", "urllib", "tvpl"],
    "convert_group":  ["convert", "extract", "parse", "docx", "ooxml", "document.xml"],
    "formula_group":  ["formula", "harvest", "vision", "ocr", "vml", "imagedata", "katex", "latex"],
    "registry_group": ["legal_registry", "registry", "update_registry"],
    "rag_group":      ["embed", "rag", "vector", "chunk", "retrieval", "embedding"],
}

# ── Capability group → human-readable Hub recommendation ─────────────────────
_GROUP_RECOMMENDATION: dict[str, str] = {
    "fetch_group":    "python -m ccba_legal fetch <tvpl_url>",
    "convert_group":  "python -m ccba_legal convert <docx_path> <output_dir>",
    "formula_group":  "from ccba_legal.formula_harvester import harvest_docx_formula_images",
    "registry_group": "python -m ccba_legal update-registry",
    "rag_group":      "Hybrid RAG Search skill (.agents/skills/hybrid-rag-search/SKILL.md)",
}


class Match(NamedTuple):
    """A Hub tool that matched the query intent."""

    skill_name: str
    skill_path: str
    triggers_matched: list[str]
    capability_group: str | None  # None nếu match từ catalog triggers


class GateResult(NamedTuple):
    """Kết quả của Gate evaluation."""

    action: str          # PASS | BLOCK | BYPASS | NO_MATCH
    matches: list[Match]
    recommendation: str
    exit_code: int       # 0 hoặc 1


# ── Core functions ────────────────────────────────────────────────────────────

def load_catalog(catalog_path: Path) -> list[dict]:
    """Nạp catalog.yaml và trả về danh sách skills.

    Args:
        catalog_path: Đường dẫn tới catalog.yaml.

    Returns:
        Danh sách skill entries từ catalog.
    """
    if not catalog_path.exists():
        print(
            json.dumps({"error": f"Catalog không tìm thấy: {catalog_path}"}),
            file=sys.stderr,
        )
        sys.exit(2)
    with catalog_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("skills", [])


def _tokenize(text: str) -> set[str]:
    """Tách text thành tập token chữ thường."""
    import re
    return set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text.lower()))


def match_intent(intent: str, catalog: list[dict]) -> list[Match]:
    """So khớp intent với catalog triggers và capability keywords.

    Args:
        intent: Mô tả tác vụ agent chuẩn bị thực hiện.
        catalog: Danh sách skills từ catalog.yaml.

    Returns:
        Danh sách Match tìm thấy (có thể rỗng).
    """
    tokens = _tokenize(intent)
    matches: list[Match] = []

    # Lớp 1: so khớp với triggers của từng skill trong catalog
    for skill in catalog:
        skill_triggers = [t.lower() for t in skill.get("triggers", [])]
        hit = [t for t in skill_triggers if t in tokens or any(t in tok for tok in tokens)]
        if hit:
            matches.append(Match(
                skill_name=skill.get("name", ""),
                skill_path=skill.get("skill_path", ""),
                triggers_matched=hit,
                capability_group=None,
            ))

    # Lớp 2: so khớp với capability keywords (ADR 0032)
    matched_groups = {m.capability_group for m in matches}
    for group, keywords in CAPABILITY_KEYWORDS.items():
        if group in matched_groups:
            continue  # đã có match từ catalog
        if tokens & set(keywords):
            # Không có skill cụ thể — dùng recommendation từ group
            matched_kws = list(tokens & set(keywords))
            matches.append(Match(
                skill_name=f"[capability: {group}]",
                skill_path=_GROUP_RECOMMENDATION.get(group, ""),
                triggers_matched=matched_kws,
                capability_group=group,
            ))

    return matches


def determine_action(
    matches: list[Match],
    layer: str,
    bypass: bool,
) -> GateResult:
    """Xác định hành động của Gate dựa trên kết quả matching.

    Args:
        matches: Danh sách Hub tools tìm thấy.
        layer:   "planning" hoặc "pre_exec".
        bypass:  Agent có khai báo BYPASS không.

    Returns:
        GateResult với action và exit_code.
    """
    if not matches:
        return GateResult(
            action="NO_MATCH",
            matches=[],
            recommendation="Capability này chưa có trong Hub — agent được phép viết mới.",
            exit_code=0,
        )

    rec_lines = []
    for m in matches:
        if m.capability_group:
            rec_lines.append(f"  [{m.capability_group}] {m.skill_path}")
        else:
            rec_lines.append(f"  Skill: {m.skill_name} ({m.skill_path})")
    recommendation = "Hub tools phù hợp:\n" + "\n".join(rec_lines)

    if bypass:
        return GateResult(action="BYPASS", matches=matches, recommendation=recommendation, exit_code=0)

    if layer == "pre_exec":
        return GateResult(action="BLOCK", matches=matches, recommendation=recommendation, exit_code=1)

    # planning layer → PASS (informational)
    return GateResult(action="PASS", matches=matches, recommendation=recommendation, exit_code=0)


def append_audit_log(
    log_path: Path,
    intent: str,
    layer: str,
    result: GateResult,
    bypass_reason: str,
) -> None:
    """Ghi một dòng JSON vào audit log (pure append, thread-safe).

    Args:
        log_path:      Đường dẫn tới catalog_gate_audit.jsonl.
        intent:        Intent string của agent.
        layer:         "planning" hoặc "pre_exec".
        result:        GateResult để log.
        bypass_reason: Lý do BYPASS (chuỗi rỗng nếu không BYPASS).
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(tz=timezone.utc).astimezone().isoformat(),
        "layer": layer,
        "intent": intent,
        "action": result.action,
        "matched_tools": [m.skill_name for m in result.matches],
        "triggers_matched": [t for m in result.matches for t in m.triggers_matched],
    }
    if bypass_reason:
        entry["bypass_reason"] = bypass_reason

    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── CLI ───────────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="CCBA Catalog Query Gate (ADR 0032) — Reuse-First enforcement."
    )
    p.add_argument("--intent", required=True, help="Mô tả tác vụ agent chuẩn bị thực hiện.")
    p.add_argument(
        "--layer",
        choices=["planning", "pre_exec"],
        default="planning",
        help="Lớp Gate: 'planning' (không block) hoặc 'pre_exec' (block nếu match).",
    )
    p.add_argument("--bypass", action="store_true", help="Khai báo BYPASS có chủ ý.")
    p.add_argument("--bypass-reason", default="", help="Lý do BYPASS (bắt buộc khi --bypass).")
    p.add_argument(
        "--catalog",
        type=Path,
        default=_DEFAULT_CATALOG,
        help=f"Đường dẫn catalog.yaml (mặc định: {_DEFAULT_CATALOG}).",
    )
    p.add_argument("--no-log", action="store_true", help="Bỏ qua ghi audit log (dùng khi test).")
    return p


def main() -> int:
    """CLI entrypoint.

    Returns:
        Exit code: 0 (PASS/BYPASS/NO_MATCH) hoặc 1 (BLOCK).
    """
    args = _build_parser().parse_args()

    if args.bypass and not args.bypass_reason:
        print(
            json.dumps({"error": "--bypass-reason bắt buộc khi dùng --bypass"}),
            file=sys.stderr,
        )
        return 2

    catalog = load_catalog(args.catalog)
    matches = match_intent(args.intent, catalog)
    result = determine_action(matches, args.layer, args.bypass)

    # Ghi log (trừ NO_MATCH và khi --no-log)
    if result.action != "NO_MATCH" and not args.no_log:
        append_audit_log(_AUDIT_LOG, args.intent, args.layer, result, args.bypass_reason)

    output = {
        "status": result.action,
        "intent": args.intent,
        "layer": args.layer,
        "matches": [
            {
                "tool": m.skill_name,
                "skill_path": m.skill_path,
                "triggers_matched": m.triggers_matched,
            }
            for m in result.matches
        ],
        "recommendation": result.recommendation,
        "audit_logged": result.action != "NO_MATCH" and not args.no_log,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
