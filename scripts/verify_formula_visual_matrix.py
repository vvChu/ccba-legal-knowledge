"""Formula Visual Verification Matrix & Anomaly Auditor (ADR 0031 & ADR 0038).

Generates a standalone, self-contained HTML verification gallery for all formulas
in a legal knowledge bundle, embedding original DOCX bitmap images alongside
KaTeX rendered formulas for 1:1 visual parity auditing.
"""

from __future__ import annotations

import argparse
import base64
import html
import io
import json
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml
from docx import Document


def generate_formula_audit_report(
    bundle_dir: Path,
    output_html_path: Path,
) -> dict[str, Any]:
    """Generate self-contained HTML formula verification report."""
    bundle_path = Path(bundle_dir)
    docx_candidates = list((bundle_path / "sources").glob("*.docx"))
    if not docx_candidates:
        docx_candidates = list(bundle_path.glob("*.docx"))
    if not docx_candidates:
        raise FileNotFoundError(f"No DOCX found in {bundle_path}")

    docx_path = docx_candidates[0]
    override_file = bundle_path / "formulas_override.yaml"
    if not override_file.exists():
        raise FileNotFoundError(f"formulas_override.yaml not found in {bundle_path}")

    formulas_override = yaml.safe_load(override_file.read_text(encoding="utf-8")) or {}

    # Open DOCX
    doc = Document(docx_path)
    rels = doc.part.rels

    # Extract all media from zip
    zip_media: dict[str, bytes] = {}
    with zipfile.ZipFile(docx_path) as z:
        for name in z.namelist():
            if name.startswith("word/media/"):
                zip_media[name.replace("word/", "")] = z.read(name)

    # Scan paragraphs to find rId mappings and context
    rid_to_context: dict[str, dict[str, Any]] = {}
    fnum_to_rids: dict[str, list[str]] = defaultdict(list)

    for p_idx, p in enumerate(doc.paragraphs):
        p_xml = p._p.xml
        p_text = p.text.strip()
        rids = re.findall(r'r:(?:id|embed)="([^"]+)"', p_xml)

        # Look for formula numbers like (135), (136), (A.1) in text or surrounding paragraphs
        f_num_match = re.search(r"\((\d+[a-z]?|[A-Z]\.\d+)\)\s*$", p_text)
        detected_fnum = f_num_match.group(1) if f_num_match else ""

        for rid in rids:
            if rid in rels:
                target = rels[rid].target_ref
                if target.startswith("media/image"):
                    prev_text = doc.paragraphs[p_idx - 1].text.strip() if p_idx > 0 else ""
                    next_text = doc.paragraphs[p_idx + 1].text.strip() if p_idx + 1 < len(doc.paragraphs) else ""

                    if not detected_fnum and prev_text:
                        prev_m = re.search(r"\((\d+[a-z]?|[A-Z]\.\d+)\)\s*$", prev_text)
                        if prev_m:
                            detected_fnum = prev_m.group(1)
                    if not detected_fnum and next_text:
                        next_m = re.search(r"\((\d+[a-z]?|[A-Z]\.\d+)\)\s*$", next_text)
                        if next_m:
                            detected_fnum = next_m.group(1)

                    rid_to_context[rid] = {
                        "p_idx": p_idx,
                        "target_media": target,
                        "p_text": p_text,
                        "prev_text": prev_text,
                        "next_text": next_text,
                        "fnum": detected_fnum,
                    }
                    if detected_fnum:
                        fnum_to_rids[detected_fnum].append(rid)

    # Build formula audit rows
    audit_rows: list[dict[str, Any]] = []
    latex_occurrences: dict[str, list[str]] = defaultdict(list)

    for key, val in formulas_override.items():
        if isinstance(val, dict):
            latex = val.get("latex", "").strip()
            fid = val.get("formula_id", "")
        else:
            latex = str(val).strip()
            fid = ""

        # Extract or resolve formula number / tag
        tag_match = re.search(r"\\tag\{([^}]+)\}", latex)
        tag_val = tag_match.group(1).strip() if tag_match else ""

        if not tag_val:
            if str(key).isdigit() or re.match(r"^[A-Z]\.\d+$", str(key)):
                tag_val = str(key)
            elif fid and "FORMULA_" in fid:
                candidate_tag = fid.split("FORMULA_")[-1].replace("_", ".")
                if candidate_tag.isdigit() or re.match(r"^[A-Z]\.\d+$", candidate_tag):
                    tag_val = candidate_tag
            elif str(key).lower().startswith("rid") and fid and "FORMULA_" in fid:
                candidate_tag = fid.split("FORMULA_")[-1].replace("_", ".")
                if candidate_tag.isdigit() or re.match(r"^[A-Z]\.\d+$", candidate_tag):
                    tag_val = candidate_tag

        # Find matching image
        img_bytes: bytes | None = None
        img_target_name = ""
        context_str = ""

        if key in rid_to_context:
            ctx = rid_to_context[key]
            img_target_name = ctx["target_media"]
            img_bytes = zip_media.get(img_target_name)
            context_str = ctx["prev_text"] or ctx["p_text"] or ctx["next_text"]
        elif tag_val and tag_val in fnum_to_rids:
            matched_rids = fnum_to_rids[tag_val]
            if matched_rids:
                ctx = rid_to_context.get(matched_rids[0], {})
                img_target_name = ctx.get("target_media", "")
                img_bytes = zip_media.get(img_target_name)
                context_str = ctx.get("prev_text") or ctx.get("p_text") or ctx.get("next_text") or ""
        elif key in fnum_to_rids:
            matched_rids = fnum_to_rids[key]
            if matched_rids:
                ctx = rid_to_context.get(matched_rids[0], {})
                img_target_name = ctx.get("target_media", "")
                img_bytes = zip_media.get(img_target_name)
                context_str = ctx.get("prev_text") or ctx.get("p_text") or ctx.get("next_text") or ""

        # Check for potential duplicates
        clean_latex = re.sub(r"\\tag\{[^}]+\}", "", latex).strip()
        if len(clean_latex) > 15:
            latex_occurrences[clean_latex].append(str(key))

        img_b64 = ""
        if img_bytes:
            img_b64 = f"data:image/png;base64,{base64.b64encode(img_bytes).decode('utf-8')}"

        audit_rows.append({
            "key": str(key),
            "formula_id": fid,
            "tag": tag_val,
            "latex": latex,
            "clean_latex": clean_latex,
            "image_name": img_target_name,
            "image_b64": img_b64,
            "context": context_str,
        })

    # Sort rows logically (Formula 1, 2, 3... 259, A.1, B.1... then unnumbered rId...)
    def _sort_key(r: dict[str, Any]) -> tuple[int, int, str]:
        t = r.get("tag", "")
        k = r.get("key", "")
        if t.isdigit():
            return (0, int(t), "")
        if re.match(r"^[A-Z]\.\d+$", t):
            l, n = t.split(".")
            return (1, int(n), l)
        if k.isdigit():
            return (0, int(k), "")
        if re.match(r"^[A-Z]\.\d+$", k):
            l, n = k.split(".")
            return (1, int(n), l)
        if k.lower().startswith("rid"):
            nums = re.findall(r"\d+", k)
            return (2, int(nums[0]) if nums else 9999, k)
        return (3, 9999, k)

    audit_rows.sort(key=_sort_key)

    # Identify anomalies
    anomalies: list[dict[str, Any]] = []
    for l_str, keys in latex_occurrences.items():
        if len(keys) > 1:
            # Check if these are truly separate formulas or just aliases
            rids = [k for k in keys if k.startswith("rId")]
            nums = [k for k in keys if not k.startswith("rId")]
            if len(rids) > 1:
                anomalies.append({
                    "type": "DUPLICATE_LATEX_ACROSS_RIDS",
                    "latex": l_str,
                    "keys": keys,
                    "message": f"Same LaTeX found across multiple rIds: {keys}",
                })

    # Render HTML
    html_content = _build_html_report(
        bundle_name=bundle_path.name,
        rows=audit_rows,
        anomalies=anomalies,
    )

    output_html_path.parent.mkdir(parents=True, exist_ok=True)
    output_html_path.write_text(html_content, encoding="utf-8")

    return {
        "total_formulas": len(audit_rows),
        "with_images": sum(1 for r in audit_rows if r["image_b64"]),
        "anomalies_count": len(anomalies),
        "html_report": str(output_html_path),
    }


def _build_html_report(
    bundle_name: str,
    rows: list[dict[str, Any]],
    anomalies: list[dict[str, Any]],
) -> str:
    """Build standalone HTML with KaTeX and interactive search."""
    rows_json = json.dumps(rows, ensure_ascii=False)
    anomalies_json = json.dumps(anomalies, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bảng Đối Soát Trực Quan Công Thức KaTeX — {bundle_name}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
    <style>
        :root {{
            --bg: #0d1117;
            --surface: #161b22;
            --border: #30363d;
            --text: #c9d1d9;
            --text-bright: #f0f6fc;
            --accent: #58a6ff;
            --success: #3fb950;
            --warning: #d29922;
            --danger: #f85149;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.5;
            padding: 24px;
        }}
        .header {{
            max-width: 1400px;
            margin: 0 auto 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .title h1 {{
            font-size: 24px;
            color: var(--text-bright);
            margin-bottom: 4px;
        }}
        .title p {{
            font-size: 14px;
            color: #8b949e;
        }}
        .stats {{
            display: flex;
            gap: 12px;
        }}
        .badge {{
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            background: var(--surface);
            border: 1px solid var(--border);
        }}
        .badge-success {{ color: var(--success); border-color: rgba(63, 185, 80, 0.4); }}
        .badge-warning {{ color: var(--warning); border-color: rgba(210, 153, 34, 0.4); }}
        .badge-info {{ color: var(--accent); border-color: rgba(88, 166, 255, 0.4); }}
        .controls {{
            max-width: 98%;
            margin: 0 auto 20px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .search-box {{
            flex: 1;
            min-width: 280px;
            padding: 10px 16px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-bright);
            font-size: 14px;
            outline: none;
        }}
        .search-box:focus {{ border-color: var(--accent); }}
        .header {{
            max-width: 98%;
            margin: 0 auto 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .container {{
            max-width: 98%;
            margin: 0 auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--surface);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        th, td {{
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
            vertical-align: middle;
        }}
        th {{
            background: #1c2128;
            color: var(--text-bright);
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        tr:hover {{ background: rgba(88, 166, 255, 0.04); }}
        .col-id {{ width: 170px; }}
        .col-img {{ width: 320px; text-align: center; }}
        .col-katex {{ min-width: 420px; }}
        .col-latex {{ width: 340px; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; color: #79c0ff; word-break: break-all; }}
        .doc-img {{
            max-width: 290px;
            max-height: 85px;
            background: #ffffff;
            padding: 4px;
            border-radius: 4px;
            border: 1px solid #484f58;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        .no-img {{
            color: #8b949e;
            font-style: italic;
            font-size: 12px;
        }}
        .katex-render-box {{
            background: #0d1117;
            padding: 12px 16px;
            border-radius: 6px;
            border: 1px solid var(--border);
            overflow-x: auto;
            color: #ffffff;
            font-size: 16px;
        }}
        .tag-pill {{
            display: inline-block;
            background: rgba(88, 166, 255, 0.2);
            color: #58a6ff;
            border: 1px solid rgba(88, 166, 255, 0.5);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 6px;
        }}
        .fid-text {{
            font-size: 11px;
            color: #8b949e;
            display: block;
        }}
        .context-tip {{
            font-size: 11px;
            color: #8b949e;
            margin-top: 4px;
            max-width: 220px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .alert-box {{
            max-width: 98%;
            margin: 0 auto 20px;
            padding: 14px 18px;
            border-radius: 6px;
            background: rgba(210, 153, 34, 0.1);
            border: 1px solid rgba(210, 153, 34, 0.4);
            color: #e3b341;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">
            <h1>📐 Bảng Đối Soát Trực Quan Công Thức KaTeX</h1>
            <p>Tài liệu: <strong>{bundle_name}</strong> | Chuẩn hóa OKF v2.4 (ADR 0031 & ADR 0038)</p>
        </div>
        <div class="stats">
            <div class="badge badge-info">Tổng số: <span id="stat-total">{len(rows)}</span> công thức</div>
            <div class="badge badge-success">Có ảnh gốc: <span id="stat-imgs">{sum(1 for r in rows if r['image_b64'])}</span></div>
            <div class="badge badge-warning">Cảnh báo trùng lặp: <span id="stat-warn">{len(anomalies)}</span></div>
        </div>
    </div>

    <div class="controls">
        <input type="text" id="search-input" class="search-box" placeholder="🔍 Tìm kiếm theo số hiệu (135, 36...), mã rId, hoặc công thức LaTeX..." oninput="filterTable()">
    </div>

    <div class="alert-box" id="anomalies-banner" style="display: {'block' if anomalies else 'none'};">
        <details>
            <summary style="cursor: pointer; font-weight: 600;">
                ⚠️ <strong>Phát Hiện {len(anomalies)} Nhóm Công Thức Có Chuỗi LaTeX Trùng Nhau (Click để xem đối chiếu):</strong>
            </summary>
            <ul style="margin-top: 10px; margin-left: 20px; font-size: 13px;">
                {''.join(f"<li style='margin-bottom: 6px;'><strong>Công thức:</strong> <code>{html.escape(a['latex'])}</code> <br><span style='color: #8b949e;'>Xuất hiện tại các khóa: {', '.join(a['keys'])}</span></li>" for a in anomalies)}
            </ul>
            <p style="margin-top: 8px; font-size: 12px; color: #8b949e;"><em>* Ghi chú: Các công thức trùng nhau như hệ số uốn dọc &eta;, tải trọng tới hạn N_cr, hoặc tỷ số mô đun đàn hồi &alpha;_s1 là sự lặp lại toán học hợp lệ ở các điều khoản khác nhau trong tiêu chuẩn TCVN 5574:2018.</em></p>
        </details>
    </div>

    <div class="container">
        <table>
            <thead>
                <tr>
                    <th class="col-id">Định Danh / Số Hiệu</th>
                    <th class="col-img">Ảnh Gốc DOCX (Bitmap)</th>
                    <th class="col-katex">Hiển Thị KaTeX (Render)</th>
                    <th class="col-latex">Mã Nguồn LaTeX</th>
                </tr>
            </thead>
            <tbody id="formula-tbody">
            </tbody>
        </table>
    </div>

    <script>
        const formulasData = {rows_json};

        function renderRows(data) {{
            const tbody = document.getElementById("formula-tbody");
            tbody.innerHTML = "";

            data.forEach((row, idx) => {{
                const tr = document.createElement("tr");
                
                // Tag & ID column
                let tagHtml = "";
                if (row.tag) {{
                    tagHtml = `<span class="tag-pill">Công thức (${{row.tag}})</span>`;
                }}
                let keyHtml = `<span class="fid-text"><strong>Key:</strong> ${{row.key}}</span>`;
                let fidHtml = row.formula_id ? `<span class="fid-text">${{row.formula_id}}</span>` : "";
                let ctxHtml = row.context ? `<div class="context-tip" title="${{escapeHtml(row.context)}}"><em>${{escapeHtml(row.context)}}</em></div>` : "";

                // Image column
                let imgHtml = row.image_b64 
                    ? `<img class="doc-img" src="${{row.image_b64}}" alt="${{row.image_name}}"><br><span class="fid-text">${{row.image_name}}</span>` 
                    : `<span class="no-img">Không có ảnh bitmap</span>`;

                // KaTeX column
                let rawLatex = row.latex || "";
                let cleanLatex = rawLatex.replace(/\\\\tag\\{{[^}}]+\\}}/g, "").trim();
                let renderLatex = cleanLatex;
                if (row.tag && !cleanLatex.includes("\\\\tag") && !cleanLatex.includes("\\\\qquad")) {{
                    let isMultiline = cleanLatex.includes("aligned") || cleanLatex.includes("cases") || cleanLatex.includes("gather");
                    if (isMultiline) {{
                        renderLatex = cleanLatex;
                    }} else {{
                        renderLatex = cleanLatex + " \\\\tag{" + row.tag + "}";
                    }}
                }}

                tr.innerHTML = `
                    <td class="col-id">
                        ${{tagHtml}}
                        ${{keyHtml}}
                        ${{fidHtml}}
                        ${{ctxHtml}}
                    </td>
                    <td class="col-img">
                        ${{imgHtml}}
                    </td>
                    <td class="col-katex">
                        <div class="katex-render-box" id="katex-${{idx}}"></div>
                    </td>
                    <td class="col-latex">
                        <code>${{escapeHtml(rawLatex)}}</code>
                    </td>
                `;
                tbody.appendChild(tr);

                // Render KaTeX
                try {{
                    const targetEl = document.getElementById(`katex-${{idx}}`);
                    katex.render(renderLatex, targetEl, {{
                        displayMode: true,
                        throwOnError: false
                    }});
                }} catch (e) {{
                    document.getElementById(`katex-${{idx}}`).innerText = renderLatex;
                }}
            }});
        }}

        function filterTable() {{
            const query = document.getElementById("search-input").value.toLowerCase().trim();
            if (!query) {{
                renderRows(formulasData);
                return;
            }}
            const filtered = formulasData.filter(r => {{
                return (r.key && r.key.toLowerCase().includes(query)) ||
                       (r.tag && r.tag.toLowerCase().includes(query)) ||
                       (r.formula_id && r.formula_id.toLowerCase().includes(query)) ||
                       (r.latex && r.latex.toLowerCase().includes(query)) ||
                       (r.context && r.context.toLowerCase().includes(query));
            }});
            renderRows(filtered);
        }}

        function escapeHtml(text) {{
            if (!text) return "";
            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}

        document.addEventListener("DOMContentLoaded", () => {{
            renderRows(formulasData);
        }});
    </script>
</body>
</html>
"""


def main() -> None:
    """CLI entrypoint for formula verification auditor."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Audit formulas against DOCX original images.")
    parser.add_argument(
        "--bundle",
        "-b",
        default="legal_docs/03_tcvn/tcvn_5574_2018",
        help="Path to legal bundle directory.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=".md/reports/formula_audit_tcvn_5574.html",
        help="Path to output HTML report.",
    )
    args = parser.parse_args()

    bundle_dir = Path(args.bundle)
    output_html = Path(args.output)

    print("=================================================================")
    print("      CCBA FORMULA VISUAL MATRIX & ANOMALY AUDITOR               ")
    print("=================================================================")
    print(f"📁 Target Bundle: {bundle_dir}")
    print(f"📊 Output Report: {output_html}")
    print("-----------------------------------------------------------------")

    res = generate_formula_audit_report(bundle_dir, output_html)

    print(f"✅ Scanned Formulas : {res['total_formulas']}")
    print(f"🖼️ With Images      : {res['with_images']}")
    print(f"⚠️ Anomalies Count  : {res['anomalies_count']}")
    print(f"📄 Report Saved To  : {res['html_report']}")
    print("=================================================================")


if __name__ == "__main__":
    main()
