"""CCBA Catalog Gate Audit Analyzer — ADR 0032.

Đọc .md/logs/catalog_gate_audit.jsonl, tính 3 chỉ số hiệu quả:
  - Hit Rate    : (PASS + BLOCK + BYPASS) / total invocations
  - Block Rate  : BLOCK / (PASS + BLOCK + BYPASS)
  - Bypass Debt : tổng số lần BYPASS tích lũy

Usage:
    python scripts/analyze_gate_audit.py
    python scripts/analyze_gate_audit.py --since "2026-08-01"
    python scripts/analyze_gate_audit.py --since "7 days ago"
    python scripts/analyze_gate_audit.py --log path/to/custom.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple

# ── Encoding fix for Windows PowerShell ──────────────────────────────────────
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_ROOT = Path(__file__).parent.parent
_DEFAULT_LOG = _ROOT / ".md" / "logs" / "catalog_gate_audit.jsonl"

# ── Thresholds (ADR 0032) ─────────────────────────────────────────────────────
_HIT_RATE_MIN = 0.80       # Alert nếu Hit Rate < 80%
_BLOCK_RATE_MAX = 0.20     # Alert nếu Block Rate > 20%
_BYPASS_DEBT_MAX = 5       # Alert nếu Bypass Debt > 5


class Metrics(NamedTuple):
    """Kết quả tổng hợp từ audit log."""

    total: int
    n_pass: int
    n_block: int
    n_bypass: int
    n_no_match: int
    hit_rate: float          # (PASS + BLOCK + BYPASS) / total
    block_rate: float        # BLOCK / (PASS + BLOCK + BYPASS) hoặc 0 nếu không có match
    bypass_debt: int
    bypass_entries: list[dict]


# ── Core functions ────────────────────────────────────────────────────────────

def parse_since(since_str: str) -> datetime | None:
    """Phân tích --since thành datetime có timezone.

    Args:
        since_str: "2026-08-01", "7 days ago", "30 days ago".

    Returns:
        datetime với tzinfo, hoặc None nếu không parse được.
    """
    s = since_str.strip().lower()

    # "N days ago"
    if s.endswith("days ago"):
        try:
            n = int(s.split()[0])
            return datetime.now(tz=timezone.utc) - timedelta(days=n)
        except ValueError:
            pass

    # "YYYY-MM-DD"
    try:
        dt = datetime.strptime(since_str.strip(), "%Y-%m-%d")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        pass

    return None


def load_entries(log_path: Path, since: datetime | None) -> list[dict]:
    """Nạp và lọc các entries từ audit log JSONL.

    Args:
        log_path: Đường dẫn tới catalog_gate_audit.jsonl.
        since:    Lọc chỉ lấy entries từ mốc thời gian này trở đi.

    Returns:
        Danh sách dict entries đã lọc.
    """
    if not log_path.exists():
        return []

    entries: list[dict] = []
    with log_path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"⚠️  Dòng {line_no} không parse được: {exc}", file=sys.stderr)
                continue

            if since is not None:
                try:
                    ts = datetime.fromisoformat(entry.get("ts", ""))
                    if ts < since:
                        continue
                except ValueError:
                    pass  # giữ entry nếu không parse được ts

            entries.append(entry)

    return entries


def compute_metrics(entries: list[dict]) -> Metrics:
    """Tính 3 chỉ số chính từ danh sách entries.

    Args:
        entries: Danh sách audit log entries.

    Returns:
        Metrics với các chỉ số tổng hợp.
    """
    n_pass = sum(1 for e in entries if e.get("action") == "PASS")
    n_block = sum(1 for e in entries if e.get("action") == "BLOCK")
    n_bypass = sum(1 for e in entries if e.get("action") == "BYPASS")
    n_no_match = sum(1 for e in entries if e.get("action") == "NO_MATCH")
    total = len(entries)

    matched = n_pass + n_block + n_bypass
    hit_rate = matched / total if total > 0 else 0.0
    block_rate = n_block / matched if matched > 0 else 0.0

    bypass_entries = [e for e in entries if e.get("action") == "BYPASS"]

    return Metrics(
        total=total,
        n_pass=n_pass,
        n_block=n_block,
        n_bypass=n_bypass,
        n_no_match=n_no_match,
        hit_rate=hit_rate,
        block_rate=block_rate,
        bypass_debt=n_bypass,
        bypass_entries=bypass_entries,
    )


def _status_icon(value: float | int, target: float | int, mode: str = "min") -> str:
    """Trả về icon ✅ hoặc ⚠️ dựa trên ngưỡng."""
    ok = value >= target if mode == "min" else value <= target
    return "✅" if ok else "⚠️ ALERT"


def print_report(metrics: Metrics, since: datetime | None, log_path: Path) -> None:
    """In report tổng hợp ra stdout.

    Args:
        metrics:  Kết quả tính toán.
        since:    Mốc thời gian lọc (None = tất cả).
        log_path: Đường dẫn log file để hiển thị.
    """
    period_str = since.strftime("%Y-%m-%d") if since else "toàn bộ"
    now_str = datetime.now().strftime("%Y-%m-%d")

    print("=" * 52)
    print("  CCBA Catalog Gate Audit Report (ADR 0032)")
    print("=" * 52)
    print(f"  Log file : {log_path}")
    print(f"  Period   : {period_str} → {now_str}")
    print(f"  Total ops: {metrics.total}  "
          f"(PASS={metrics.n_pass} BLOCK={metrics.n_block} "
          f"BYPASS={metrics.n_bypass} NO_MATCH={metrics.n_no_match})")
    print()

    if metrics.total == 0:
        print("  ℹ️  Chưa có dữ liệu trong khoảng thời gian này.")
        print("     Gate chưa được kích hoạt lần nào.")
        return

    hit_icon  = _status_icon(metrics.hit_rate,  _HIT_RATE_MIN,     mode="min")
    blk_icon  = _status_icon(metrics.block_rate, _BLOCK_RATE_MAX,   mode="max")
    byp_icon  = _status_icon(metrics.bypass_debt, _BYPASS_DEBT_MAX, mode="max")

    print(f"  Hit Rate    : {metrics.hit_rate:.1%}  {hit_icon}  (target ≥ {_HIT_RATE_MIN:.0%})")
    print(f"  Block Rate  : {metrics.block_rate:.1%}  {blk_icon}  (target ≤ {_BLOCK_RATE_MAX:.0%})")
    print(f"  Bypass Debt : {metrics.bypass_debt}        {byp_icon}  (target ≤ {_BYPASS_DEBT_MAX})")

    if metrics.bypass_entries:
        print()
        print("  BYPASS detail:")
        for e in metrics.bypass_entries:
            ts = e.get("ts", "?")[:16]
            layer = e.get("layer", "?")
            intent = e.get("intent", "")[:50]
            reason = e.get("bypass_reason", "(không có lý do)")
            print(f"    [{ts}] {layer} | {intent}")
            print(f"           → {reason}")

    # Recommendations
    alerts = []
    if metrics.hit_rate < _HIT_RATE_MIN:
        alerts.append("Hit Rate thấp → Gate có thể đang bị bỏ qua hoặc capability_keywords cần mở rộng.")
    if metrics.block_rate > _BLOCK_RATE_MAX:
        alerts.append("Block Rate cao → Agent đang thường xuyên drift khỏi Hub tools.")
    if metrics.bypass_debt > _BYPASS_DEBT_MAX:
        alerts.append(
            f"Bypass Debt = {metrics.bypass_debt} → Xem xét mở rộng Hub catalog "
            "dựa trên bypass_reason đã ghi nhận."
        )
    if alerts:
        print()
        print("  ⚠️  Recommendations:")
        for a in alerts:
            print(f"    - {a}")

    print("=" * 52)


# ── CLI ───────────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Phân tích audit log của CCBA Catalog Query Gate (ADR 0032)."
    )
    p.add_argument(
        "--since",
        default=None,
        help='Lọc từ mốc thời gian. Ví dụ: "2026-08-01" hoặc "7 days ago".',
    )
    p.add_argument(
        "--log",
        type=Path,
        default=_DEFAULT_LOG,
        help=f"Đường dẫn audit log JSONL (mặc định: {_DEFAULT_LOG}).",
    )
    return p


def main() -> int:
    """CLI entrypoint.

    Returns:
        0 nếu không có alert, 1 nếu có ít nhất 1 alert vượt ngưỡng.
    """
    args = _build_parser().parse_args()

    since: datetime | None = None
    if args.since:
        since = parse_since(args.since)
        if since is None:
            print(f"❌ Không parse được --since: '{args.since}'", file=sys.stderr)
            print("   Dùng định dạng: '2026-08-01' hoặc '7 days ago'", file=sys.stderr)
            return 2

    entries = load_entries(args.log, since)
    metrics = compute_metrics(entries)
    print_report(metrics, since, args.log)

    has_alert = (
        metrics.total > 0
        and (
            metrics.hit_rate < _HIT_RATE_MIN
            or metrics.block_rate > _BLOCK_RATE_MAX
            or metrics.bypass_debt > _BYPASS_DEBT_MAX
        )
    )
    return 1 if has_alert else 0


if __name__ == "__main__":
    sys.exit(main())
