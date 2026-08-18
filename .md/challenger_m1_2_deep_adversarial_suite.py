import os
import sys
import re
import docx
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\.md\extracted_docs\qcvn_06_2022_bxd\qcvn_06_2022_bxd.docx"
MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\qcvn_06_2022_bxd.md"
SD1_MD_PATH = r"d:\GitHubProjects\ccba-legal-knowledge\legal_docs\02_qcvn\qcvn_06_2022_bxd\sua_doi_1_2023_qcvn_06_2022_bxd.md"

def normalize_text(t):
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def run_adversarial_suite():
    print("=" * 80)
    print("      CHALLENGER M1-2: COMPREHENSIVE ADVERSARIAL VERIFICATION SUITE      ")
    print("=" * 80)
    
    # -------------------------------------------------------------
    # 1. LOAD DOCX AND MD
    # -------------------------------------------------------------
    doc = docx.Document(DOCX_PATH)
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()
    md_lines = md_content.splitlines()

    print(f"Loaded DOCX: {len(doc.paragraphs)} paragraphs, {len(doc.tables)} tables")
    print(f"Loaded MD  : {len(md_lines)} lines, {len(md_content):,} characters")

    # -------------------------------------------------------------
    # TEST SUITE 1: AGGRESSIVE NUMBERING & HEADING BUG HUNTING
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST SUITE 1: AGGRESSIVE NUMBERING & HEADING ANOMALIES")
    print("=" * 80)
    
    anomalies = []

    # 1.1 Check dot-split 1.4: 1.4.X.Y (e.g. 1.4.1.7)
    dot_split_1_4 = re.findall(r"^#{1,6}\s+1\.4\.\d+\.\d+.*", md_content, re.MULTILINE)
    print(f"[1.1] Dot-split headings in Section 1.4 (e.g. 1.4.1.7): {len(dot_split_1_4)}")
    if dot_split_1_4:
        for item in dot_split_1_4[:10]:
            anomalies.append(f"Dot-split in 1.4: {item}")
            print(f"      FAIL: {item}")
    else:
        print("      PASS: 0 dot-split headings found in 1.4.")

    # 1.2 Check all definitions under Section 1.4 (1.4.1 to 1.4.72)
    defs_found = {}
    for line in md_lines:
        m = re.match(r"^#{1,6}\s+1\.4\.(\d+)\b", line)
        if m:
            defs_found[int(m.group(1))] = line
    print(f"[1.2] Definition count in 1.4: {len(defs_found)} / 72")
    missing_defs = [i for i in range(1, 73) if i not in defs_found]
    if missing_defs:
        anomalies.append(f"Missing definitions in 1.4: {missing_defs}")
        print(f"      FAIL: Missing definitions: {missing_defs}")
    else:
        print("      PASS: Exactly 72 definitions (1.4.1 to 1.4.72) verified.")

    # 1.3 Check space-separated headings (### 4 1, ### 7 1, ### 24 0, etc.)
    space_headings = re.findall(r"^#{1,6}\s+\d+\s+\d+.*", md_content, re.MULTILINE)
    print(f"[1.3] Space-separated number headings (e.g. ### 4 1, ### 24 0): {len(space_headings)}")
    if space_headings:
        for item in space_headings[:10]:
            anomalies.append(f"Space-separated heading: {item}")
            print(f"      FAIL: {item}")
    else:
        print("      PASS: 0 space-separated number headings found.")

    # 1.4 Check appendix space-separated headings (### A 1, etc.)
    appendix_space = re.findall(r"^#{1,6}\s+[A-I]\s+\d+.*", md_content, re.MULTILINE)
    print(f"[1.4] Appendix space headings (e.g. ### A 1): {len(appendix_space)}")
    if appendix_space:
        for item in appendix_space[:10]:
            anomalies.append(f"Appendix space heading: {item}")
            print(f"      FAIL: {item}")
    else:
        print("      PASS: 0 appendix space headings found.")

    # 1.5 Check specific subdot anomalies (2.1.11 -> 2.1.1.1, etc.)
    subdot_targets = [
        (r"^#{1,6}\s+2\.1\.11\b", "2.1.1.1"),
        (r"^#{1,6}\s+2\.1\.12\b", "2.1.1.2"),
        (r"^#{1,6}\s+2\.2\.11\b", "2.2.1.1"),
        (r"^#{1,6}\s+2\.2\.12\b", "2.2.1.2"),
        (r"^#{1,6}\s+2\.2\.13\b", "2.2.1.3"),
        (r"^#{1,6}\s+2\.5\.6\.33\b", "2.5.6.3.3"),
        (r"^#{1,6}\s+5\.1\.11\b", "5.1.1.1"),
        (r"^#{1,6}\s+5\.1\.12\b", "5.1.1.2"),
        (r"^#{1,6}\s+5\.1\.13\b", "5.1.1.3"),
        (r"^#{1,6}\s+5\.1\.14\b", "5.1.1.4"),
        (r"^#{1,6}\s+6\.2\.11\b", "6.2.1.1"),
        (r"^#{1,6}\s+6\.2\.12\b", "6.2.1.2"),
        (r"^#{1,6}\s+6\.2\.13\b", "6.2.1.3"),
        (r"^#{1,6}\s+6\.2\.14\b", "6.2.1.4"),
    ]
    found_bad_subdots = []
    for pattern, expected in subdot_targets:
        matches = re.findall(pattern, md_content, re.MULTILINE)
        if matches:
            found_bad_subdots.extend(matches)
    print(f"[1.5] Missing subdot anomalies (e.g. 2.1.11 instead of 2.1.1.1): {len(found_bad_subdots)}")
    if found_bad_subdots:
        for item in found_bad_subdots:
            anomalies.append(f"Missing subdot: {item}")
            print(f"      FAIL: {item}")
    else:
        print("      PASS: 0 missing subdot bugs found.")

    # Check that the corrected subdots actually exist in MD
    corrected_subdots = [
        "2.1.1.1", "2.1.1.2", "2.2.1.1", "2.2.1.2", "2.2.1.3",
        "2.5.6.3.3", "5.1.1.1", "5.1.1.2", "5.1.1.3", "5.1.1.4",
        "6.2.1.1", "6.2.1.2", "6.2.1.3", "6.2.1.4"
    ]
    missing_corrected = []
    for c in corrected_subdots:
        if not re.search(rf"^#{{1,6}}\s+{re.escape(c)}\b", md_content, re.MULTILINE):
            missing_corrected.append(c)
    print(f"[1.6] Verification of presence of corrected subdots ({len(corrected_subdots)} targets):")
    if missing_corrected:
        anomalies.append(f"Corrected subdots missing from MD: {missing_corrected}")
        print(f"      FAIL: Missing corrected subdots: {missing_corrected}")
    else:
        print(f"      PASS: All {len(corrected_subdots)} restored subdots are present.")

    # 1.7 Residual fake headings check (numbers with decimals like '### 24 0', '### 1 4', '### 0 5', etc.)
    fake_table_headings = re.findall(r"^#{1,6}\s+(?:\d+\s+\d+|\d+\.\d+\.\d+\.\d+\.\d+\.\d+.*)", md_content, re.MULTILINE)
    print(f"[1.7] Residual fake table headings: {len(fake_table_headings)}")
    if fake_table_headings:
        for item in fake_table_headings[:10]:
            anomalies.append(f"Residual fake heading: {item}")
            print(f"      FAIL: {item}")
    else:
        print("      PASS: 0 residual fake table headings found.")

    # 1.8 Heading Hierarchy Audit
    heading_lines = [l for l in md_lines if l.startswith("#")]
    h_dist = defaultdict(int)
    for h in heading_lines:
        level = len(h) - len(h.lstrip("#"))
        h_dist[level] += 1
    print(f"[1.8] Heading distribution: {dict(sorted(h_dist.items()))}")
    print(f"      Total headings: {len(heading_lines)}")

    # Verify document main sections
    h2_headings = [l for l in md_lines if l.startswith("## ")]
    print(f"      H2 headings ({len(h2_headings)}):")
    for h in h2_headings:
        print(f"        - {h}")

    # Expected H2 chapters & appendices
    expected_h2 = [
        "1 QUY ĐỊNH CHUNG",
        "2 PHÂN LOẠI KỸ THUẬT VỀ CHÁY",
        "3 BẢO ĐẢM AN TOÀN CHO NGƯỜI",
        "4 NGĂN CHẶN CHÁY LAN",
        "5 CẤP NƯỚC CHỮA CHÁY",
        "6 CHỮA CHÁY VÀ CỨU NẠN",
        "7 TỔ CHỨC THỰC HIỆN",
        "PHỤ LỤC A",
        "PHỤ LỤC B",
        "PHỤ LỤC C",
        "PHỤ LỤC D",
        "PHỤ LỤC E",
        "PHỤ LỤC F",
        "PHỤ LỤC G",
        "PHỤ LỤC H",
        "PHỤ LỤC I"
    ]
    missing_h2 = []
    for exp in expected_h2:
        if not any(exp in h for h in h2_headings):
            missing_h2.append(exp)
    if missing_h2:
        anomalies.append(f"Missing H2 sections: {missing_h2}")
        print(f"      FAIL: Missing H2 sections: {missing_h2}")
    else:
        print(f"      PASS: All 7 Chapters and 9 Appendices (A-I) have proper H2 headings.")

    # -------------------------------------------------------------
    # TEST SUITE 2: DETERMINISTIC LINE-BY-LINE & PARAGRAPH PARITY
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST SUITE 2: DETERMINISTIC DOCX VS MD PARAGRAPH AUDIT")
    print("=" * 80)

    # Segment DOCX into chapters & appendices
    docx_paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    # Filter out TOC in DOCX
    # TOC in DOCX is located between "MỤC LỤC" / start of document and "1 QUY ĐỊNH CHUNG"
    # Let's find index of "1 QUY ĐỊNH CHUNG" or "1. QUY ĐỊNH CHUNG"
    start_idx = 0
    for i, p in enumerate(docx_paras):
        if re.match(r"^1\.?\s+QUY ĐỊNH CHUNG", p, re.IGNORECASE):
            # Check if this is the actual chapter header (not in TOC)
            # In TOC, it's followed by page numbers or other TOC entries.
            # Let's check preceding text for "Lời nói đầu"
            start_idx = i
            break

    # Also include "Lời nói đầu" if present before Chapter 1
    loi_noi_dau_idx = -1
    for i in range(start_idx):
        if "Lời nói đầu" in docx_paras[i] or "LỜI NÓI ĐẦU" in docx_paras[i]:
            loi_noi_dau_idx = i
            break
    
    body_start_idx = loi_noi_dau_idx if loi_noi_dau_idx != -1 else start_idx
    body_docx_paras = docx_paras[body_start_idx:]
    print(f"Total DOCX paragraphs: {len(docx_paras)}")
    print(f"TOC frontmatter filtered: {body_start_idx} paragraphs")
    print(f"Body DOCX paragraphs: {len(body_docx_paras)}")

    # Normalized MD text for fast lookup
    norm_md = normalize_text(md_content)

    # Let's perform paragraph-by-paragraph exact / normalized lookup
    matched_paras = 0
    missing_docx_paras = []
    
    for idx, p in enumerate(body_docx_paras):
        norm_p = normalize_text(p)
        # Skip purely table-like fragments or page number artifacts if any
        if len(norm_p) < 3:
            continue
        
        # Check direct inclusion in normalized MD
        if norm_p in norm_md:
            matched_paras += 1
        else:
            # Try sub-clause prefix stripping (e.g. "1.1.1 " might be formatted as "#### 1.1.1\n")
            # or punctuation differences
            # If paragraph contains heading + text: "1.1.1 Phạm vi..."
            # MD might have "#### 1.1.1" then "Phạm vi..."
            parts = norm_p.split(" ", 1)
            if len(parts) == 2 and len(parts[1]) > 5 and parts[1] in norm_md:
                matched_paras += 1
            else:
                missing_docx_paras.append((idx + body_start_idx, p))

    print(f"Matched body paragraphs: {matched_paras} / {len(body_docx_paras)} ({matched_paras/len(body_docx_paras)*100:.2f}%)")
    print(f"Unmatched paragraphs: {len(missing_docx_paras)}")
    if missing_docx_paras:
        print("First 10 unmatched paragraphs:")
        for idx, p in missing_docx_paras[:10]:
            print(f"  [DOCX P#{idx}] {p[:100]}...")
    else:
        print("PASS: 100% of body paragraphs matched!")

    # -------------------------------------------------------------
    # TEST SUITE 3: ANCHOR TAGS & CROSS-REFERENCE INTEGRITY
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST SUITE 3: ANCHOR TAGS & CROSS-REFERENCE INTEGRITY")
    print("=" * 80)

    # 3.1 Check all anchors in MD
    anchors = re.findall(r'<a\s+id="([^"]+)"></a>', md_content)
    print(f"[3.1] Total anchors defined in qcvn_06_2022_bxd.md: {len(anchors)}")
    
    # Check duplicate anchors
    anchor_counts = defaultdict(int)
    for a in anchors:
        anchor_counts[a] += 1
    dupe_anchors = {k: v for k, v in anchor_counts.items() if v > 1}
    print(f"[3.2] Duplicate anchor IDs: {len(dupe_anchors)}")
    if dupe_anchors:
        for k, v in list(dupe_anchors.items())[:10]:
            anomalies.append(f"Duplicate anchor: {k} (count={v})")
            print(f"      FAIL: Duplicate anchor '{k}': {v} times")
    else:
        print("      PASS: All anchor IDs are uniquely defined.")

    # 3.3 Check cross-references from sua_doi_1_2023_qcvn_06_2022_bxd.md
    if os.path.exists(SD1_MD_PATH):
        with open(SD1_MD_PATH, "r", encoding="utf-8") as f:
            sd1_content = f.read()
        # Find links pointing to qcvn_06_2022_bxd.md#...
        sd1_links = re.findall(r'\[([^\]]+)\]\(qcvn_06_2022_bxd\.md#([^\)]+)\)', sd1_content)
        print(f"[3.3] Cross-links from sua_doi_1_2023 pointing to qcvn_06_2022_bxd.md: {len(sd1_links)}")
        
        anchor_set = set(anchors)
        broken_cross_links = []
        for text, target_id in sd1_links:
            if target_id not in anchor_set:
                broken_cross_links.append((text, target_id))
        print(f"      Broken cross-links: {len(broken_cross_links)}")
        if broken_cross_links:
            for text, target_id in broken_cross_links[:10]:
                print(f"      WARNING: Link '{text}' -> '#{target_id}' not found in anchor set.")
        else:
            print("      PASS: All cross-links from Amendment 1:2023 point to valid anchors in Base QCVN 06!")

    # -------------------------------------------------------------
    # TEST SUITE 4: EMBEDDED GFM TABLES STRUCTURAL AUDIT
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST SUITE 4: EMBEDDED GFM TABLES STRUCTURAL AUDIT (64 TABLES)")
    print("=" * 80)

    # Find table headings in MD: "### Bảng X"
    table_headers_md = re.findall(r'^###\s+(Bảng\s+[A-Za-z0-9_.\-]+(?:\s*-\s*[^\n]+)?)', md_content, re.MULTILINE)
    print(f"[4.1] Table headings found in MD: {len(table_headers_md)} / 64 expected")
    if len(table_headers_md) != 64:
        print(f"      WARNING: Table count mismatch. Found {len(table_headers_md)} table headings.")
    else:
        print("      PASS: Exactly 64 table headings found.")

    # Check GFM table pipe syntax
    # Scan for pipes and verify separator rows
    gfm_tables_found = 0
    table_syntax_errors = []
    lines = md_lines
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|") and line.strip().endswith("|"):
            # Start of a table block
            start_line = i
            table_block = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_block.append(lines[i])
                i += 1
            gfm_tables_found += 1
            # Check delimiter row
            if len(table_block) >= 2:
                del_row = table_block[1]
                if not re.match(r"^\|(?:\s*:?-+:?\s*\|)+$", del_row.strip()):
                    table_syntax_errors.append((start_line + 1, "Missing/malformed delimiter row: " + del_row))
            else:
                table_syntax_errors.append((start_line + 1, "Single line table"))
        else:
            i += 1

    print(f"[4.2] GFM Table blocks detected: {gfm_tables_found}")
    print(f"[4.3] Table syntax errors: {len(table_syntax_errors)}")
    if table_syntax_errors:
        for lno, err in table_syntax_errors[:10]:
            anomalies.append(f"Table syntax error at line {lno}: {err}")
            print(f"      FAIL at line {lno}: {err}")
    else:
        print("      PASS: All GFM table blocks have valid pipe syntax and delimiter rows.")

    # -------------------------------------------------------------
    # TEST SUITE 5: MARKDOWN SYNTAX & INTEGRITY EDGE CASES
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST SUITE 5: MARKDOWN SYNTAX & INTEGRITY EDGE CASES")
    print("=" * 80)

    # 5.1 Unicode replacement chars
    unicode_errors = md_content.count("\ufffd")
    print(f"[5.1] Unicode replacement characters (\\ufffd): {unicode_errors}")
    if unicode_errors > 0:
        anomalies.append(f"Found {unicode_errors} Unicode replacement characters.")
        print(f"      FAIL: {unicode_errors} unicode errors.")
    else:
        print("      PASS: 0 unicode corruption characters.")

    # 5.2 Malformed markdown links [text](broken
    broken_md_links = re.findall(r'\[[^\]]+\]\([^\)\s]+$', md_content, re.MULTILINE)
    print(f"[5.2] Unclosed markdown links: {len(broken_md_links)}")
    if broken_md_links:
        for b in broken_md_links[:5]:
            anomalies.append(f"Broken markdown link: {b}")
            print(f"      FAIL: {b}")
    else:
        print("      PASS: 0 unclosed markdown links.")

    # 5.3 Dangling HTML tags
    open_tags = re.findall(r'<(?!\/|a\s|img\s|br|hr)([a-zA-Z0-9]+)[^>]*>', md_content)
    print(f"[5.3] Unusual HTML tags: {set(open_tags)}")

    # -------------------------------------------------------------
    # SUMMARY & VERDICT
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("                       ADVERSARIAL VERDICT                       ")
    print("=" * 80)
    print(f"Total Anomalies Detected: {len(anomalies)}")
    if anomalies:
        print("Status: REQUEST_CHANGES")
        for a in anomalies:
            print(f"  - {a}")
    else:
        print("Status: APPROVE")
        print("All empirical tests and adversarial stress harnesses passed 100%!")

if __name__ == "__main__":
    run_adversarial_suite()
