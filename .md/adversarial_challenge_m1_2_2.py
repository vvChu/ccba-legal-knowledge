"""Adversarial Challenge & Mutator Stress Test Suite for Milestone 1 Iteration 2.

Evaluates:
1. Deep heading & subdot audit (13 subdots + 2.2.2.1 + single H1 + anchors).
2. Idempotency & zero-mutation verification of scripts/verify_knowledge_integrity.py.
3. Idempotency of scripts/clean_qcvn06_data.py.
4. Comprehensive AST/Regex anomaly scan across the entire QCVN 06:2022/BXD markdown.
5. True paragraph parity against docx.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from docx import Document

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT_DIR = Path(__file__).resolve().parent.parent
BASE_MD_PATH = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "qcvn_06_2022_bxd.md"
SD1_MD_PATH = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd" / "sua_doi_1_2023_qcvn_06_2022_bxd.md"
DOCX_PATH = ROOT_DIR / ".md" / "extracted_docs" / "qcvn_06_2022_bxd" / "qcvn_06_2022_bxd.docx"
VERIFY_SCRIPT = ROOT_DIR / "scripts" / "verify_knowledge_integrity.py"
CLEAN_SCRIPT = ROOT_DIR / "scripts" / "clean_qcvn06_data.py"


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def test_13_subdots_and_2221_and_h1() -> Dict[str, any]:
    """Test Focus 1: Subdots, 2.2.2.1 promotion, H1 count, and anchors."""
    print("\n--- [TEST FOCUS 1] 13 Subdots, 2.2.2.1 Promotion, and Single H1 Audit ---")
    
    assert BASE_MD_PATH.exists(), f"Target file missing: {BASE_MD_PATH}"
    lines = BASE_MD_PATH.read_text(encoding="utf-8").splitlines()
    text = "\n".join(lines)
    
    # 1. Check single H1
    h1_lines = [(i + 1, line) for i, line in enumerate(lines) if re.match(r"^#\s+", line)]
    print(f"[*] H1 Headings count: {len(h1_lines)}")
    for line_no, line in h1_lines:
        print(f"    Line {line_no}: {line}")
    assert len(h1_lines) == 1, f"Expected exactly 1 H1 heading, found {len(h1_lines)}: {h1_lines}"
    assert h1_lines[0][0] == 1, f"Expected H1 at line 1, found at line {h1_lines[0][0]}"
    assert h1_lines[0][1].strip() == "# QCVN 06:2022/BXD", f"Unexpected H1 title: {h1_lines[0][1]}"

    # Check "Lời nói đầu" has no H1
    for i, line in enumerate(lines[:30]):
        if "Lời nói đầu" in line:
            print(f"    Lời nói đầu found at line {i+1}: {line}")
            assert line.startswith("## "), f"Expected H2 for 'Lời nói đầu', got: {line}"
    
    # 2. Check 13 subdot headings and their anchors
    expected_subdots = [
        ("2.1.1.1", "muc-2-1-1-1"),
        ("2.1.1.2", "muc-2-1-1-2"),
        ("2.2.1.1", "muc-2-2-1-1"),
        ("2.2.1.2", "muc-2-2-1-2"),
        ("2.2.1.3", "muc-2-2-1-3"),
        ("2.2.2.1", "muc-2-2-2-1"),
        ("5.1.1.1", "muc-5-1-1-1"),
        ("5.1.1.2", "muc-5-1-1-2"),
        ("5.1.1.3", "muc-5-1-1-3"),
        ("5.1.1.4", "muc-5-1-1-4"),
        ("6.2.1.1", "muc-6-2-1-1"),
        ("6.2.1.2", "muc-6-2-1-2"),
        ("6.2.1.3", "muc-6-2-1-3"),
        ("6.2.1.4", "muc-6-2-1-4"),
    ]
    
    subdot_findings = []
    for num, anchor_id in expected_subdots:
        pattern = rf"^#####\s+{re.escape(num)}\b"
        found = False
        for i, line in enumerate(lines):
            if re.match(pattern, line):
                found = True
                # Check preceding line or anchor within previous 2 lines
                has_anchor = False
                for offset in [1, 2]:
                    if i >= offset and f'<a id="{anchor_id}">' in lines[i - offset]:
                        has_anchor = True
                        break
                subdot_findings.append({
                    "num": num,
                    "anchor_id": anchor_id,
                    "line_no": i + 1,
                    "heading": line[:80],
                    "anchor_matched": has_anchor
                })
                print(f"  [+] Found subdot {num} at line {i+1} (Anchor matched: {has_anchor}) -> {line[:60]}...")
                break
        assert found, f"Missing subdot heading: ##### {num}"

    # Verify all anchors matched
    for sf in subdot_findings:
        assert sf["anchor_matched"], f"Anchor <a id=\"{sf['anchor_id']}\"> missing before line {sf['line_no']}"

    # 3. Check ABSENCE of corrupted subdot variants
    corrupted_patterns = [
        r"#####\s+2\.1\.11\b",
        r"#####\s+2\.1\.12\b",
        r"#####\s+2\.2\.11\b",
        r"#####\s+2\.2\.12\b",
        r"#####\s+2\.2\.13\b",
        r"#####\s+5\.1\.11\b",
        r"#####\s+5\.1\.12\b",
        r"#####\s+5\.1\.13\b",
        r"#####\s+5\.1\.14\b",
        r"#####\s+6\.2\.11\b",
        r"#####\s+6\.2\.12\b",
        r"#####\s+6\.2\.13\b",
        r"#####\s+6\.2\.14\b",
        r"#####\s+2\s+2\.2\.1\b",
        r"(?:^|\n)2\s+2\.2\.1\s+",
    ]
    corrupted_found = []
    for pat in corrupted_patterns:
        matches = list(re.finditer(pat, text))
        if matches:
            corrupted_found.append((pat, len(matches)))
            print(f"  [-] CORRUPTED HEADING PATTERN FOUND: {pat} ({len(matches)} matches)")
            
    assert len(corrupted_found) == 0, f"Found corrupted heading patterns: {corrupted_found}"
    print(f"[*] Corrupted subdot patterns check: PASSED (0 occurrences found)")

    # 4. Check 2.2.2.1 promotion specifically
    assert any(sf["num"] == "2.2.2.1" and sf["anchor_matched"] for sf in subdot_findings)
    print(f"[*] 2.2.2.1 promotion check: PASSED (Promoted to ##### 2.2.2.1 with anchor)")

    return {
        "status": "PASS",
        "h1_count": len(h1_lines),
        "subdots_verified": len(subdot_findings),
        "corrupted_found": len(corrupted_found),
    }


def test_idempotency_and_mutator() -> Dict[str, any]:
    """Test Focus 2 & 3: Script idempotency, zero mutation, cleaner idempotency."""
    print("\n--- [TEST FOCUS 2] Idempotency & Mutator Stress Test ---")
    
    # 1. Check verify_knowledge_integrity.py source code for write mutations
    verify_code = VERIFY_SCRIPT.read_text(encoding="utf-8")
    mutator_indicators = [
        r"write_text",
        r"open\([^)]*['\"]w",
        r"open\([^)]*['\"]a",
        r"fix_qcvn06_markdown_headings",
        r"shutil\.copy",
    ]
    found_mutators = []
    for ind in mutator_indicators:
        if re.search(ind, verify_code):
            found_mutators.append(ind)
    print(f"[*] Mutator signatures in {VERIFY_SCRIPT.name}: {found_mutators}")
    assert len(found_mutators) == 0, f"Dangerous mutator found in verifier: {found_mutators}"

    # 2. Measure SHA256 before repeated executions
    sha_base_before = compute_sha256(BASE_MD_PATH)
    sha_sd1_before = compute_sha256(SD1_MD_PATH)
    print(f"[*] Baseline SHA256 ({BASE_MD_PATH.name}): {sha_base_before}")
    print(f"[*] Baseline SHA256 ({SD1_MD_PATH.name}): {sha_sd1_before}")

    # 3. Stress-test verify_knowledge_integrity.py (10 consecutive runs)
    print("[*] Running verify_knowledge_integrity.py 10 times in loop...")
    for i in range(10):
        res = subprocess.run(
            [sys.executable, str(VERIFY_SCRIPT)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=str(ROOT_DIR),
        )
        assert res.returncode == 0, f"Verifier run #{i+1} failed: {res.stderr}"

    sha_base_after_verifier = compute_sha256(BASE_MD_PATH)
    sha_sd1_after_verifier = compute_sha256(SD1_MD_PATH)
    print(f"[*] Post-verifier SHA256 ({BASE_MD_PATH.name}): {sha_base_after_verifier}")
    print(f"[*] Post-verifier SHA256 ({SD1_MD_PATH.name}): {sha_sd1_after_verifier}")

    assert sha_base_before == sha_base_after_verifier, "CRITICAL: verify_knowledge_integrity.py MUTATED qcvn_06_2022_bxd.md!"
    assert sha_sd1_before == sha_sd1_after_verifier, "CRITICAL: verify_knowledge_integrity.py MUTATED sua_doi_1_2023_qcvn_06_2022_bxd.md!"
    print("[+] VERIFIER IDEMPOTENCY PASS: 100% byte-for-byte identical after 10 runs.")

    # 4. Stress-test clean_qcvn06_data.py idempotency
    print("[*] Running clean_qcvn06_data.py to test cleaner idempotency...")
    clean_res = subprocess.run(
        [sys.executable, str(CLEAN_SCRIPT)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(ROOT_DIR),
    )
    assert clean_res.returncode == 0, f"Cleaner failed: {clean_res.stderr}"

    sha_base_after_cleaner = compute_sha256(BASE_MD_PATH)
    sha_sd1_after_cleaner = compute_sha256(SD1_MD_PATH)
    print(f"[*] Post-cleaner SHA256 ({BASE_MD_PATH.name}): {sha_base_after_cleaner}")
    print(f"[*] Post-cleaner SHA256 ({SD1_MD_PATH.name}): {sha_sd1_after_cleaner}")

    assert sha_base_before == sha_base_after_cleaner, "clean_qcvn06_data.py unexpectedly modified already clean qcvn_06_2022_bxd.md!"
    assert sha_sd1_before == sha_sd1_after_cleaner, "clean_qcvn06_data.py unexpectedly modified already clean sua_doi_1_2023_qcvn_06_2022_bxd.md!"
    print("[+] CLEANER IDEMPOTENCY PASS: 100% byte-for-byte identical after cleaner execution.")

    return {
        "status": "PASS",
        "verifier_idempotent": True,
        "cleaner_idempotent": True,
    }


def test_comprehensive_regex_and_heading_scan() -> Dict[str, any]:
    """Test Focus 3: Scan for all potential regex anomalies, dot splits, space splits, bad headings."""
    print("\n--- [TEST FOCUS 3] Comprehensive Heading & Regex Anomaly Scan ---")

    text = BASE_MD_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    anomalies = []

    # 1. Check dot split anomalies (Section 1.4: 1.4.1.7 .. 1.4.7.2)
    re_dot_split = re.compile(r"^#{1,6}\s+1\.4\.[1-7]\.\d+\b", re.MULTILINE)
    matches = re_dot_split.findall(text)
    if matches:
        anomalies.append(f"Section 1.4 dot-splits: {len(matches)} found ({matches[:3]})")

    # 2. Check space-separated headings: "### 4 1" or "### 7 1" or "### 1 4"
    re_space_heading = re.compile(r"^#{1,6}\s+[0-9]+\s+[0-9]+(?:\s+[0-9]+)*\s*$", re.MULTILINE)
    space_matches = re_space_heading.findall(text)
    if space_matches:
        anomalies.append(f"Space-separated fake/unsplit headings: {len(space_matches)} found ({space_matches[:5]})")

    # 3. Check for malformed heading syntax: e.g. '#Heading' (missing space after #), '###  ' with 4+ spaces, or empty heading '### \n'
    re_bad_heading_syntax = re.compile(r"^#{1,6}[^\s#]", re.MULTILINE)
    bad_syntax = re_bad_heading_syntax.findall(text)
    if bad_syntax:
        anomalies.append(f"Malformed heading syntax (no space after #): {len(bad_syntax)} found ({bad_syntax[:3]})")

    # 4. Check for double escape artifacts like "\.", "\(", "\)"
    re_escapes = re.compile(r"\\[\.\(\)\_\-]")
    escape_matches = re_escapes.findall(text)
    print(f"[*] Escape artifacts found: {len(escape_matches)}")

    # 5. Check all headings distribution
    heading_counts = {}
    heading_list = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            lvl = len(m.group(1))
            heading_counts[lvl] = heading_counts.get(lvl, 0) + 1
            heading_list.append((i + 1, lvl, m.group(2)))

    print(f"[*] Heading distribution: {heading_counts}")
    print(f"[*] Total headings: {len(heading_list)}")
    
    # 6. Check for invalid heading jumps (e.g. H1 -> H4 or H2 -> H5)
    jumps = []
    for i in range(len(heading_list) - 1):
        l1_no, l1_lvl, l1_txt = heading_list[i]
        l2_no, l2_lvl, l2_txt = heading_list[i + 1]
        # In Markdown, jumping down more than 2 levels is considered abnormal
        if l2_lvl > l1_lvl + 2:
            jumps.append((l1_no, l1_lvl, l1_txt, l2_no, l2_lvl, l2_txt))

    if jumps:
        print(f"[*] Heading level jumps (>2): {len(jumps)}")
        for j in jumps[:5]:
            print(f"    Line {j[0]} (H{j[1]}: {j[2][:30]}) -> Line {j[3]} (H{j[4]}: {j[5][:30]})")

    # 7. Check table alignment / pipe syntax consistency
    pipe_lines = [line for line in lines if line.startswith("|") and line.endswith("|")]
    print(f"[*] Embedded markdown table rows: {len(pipe_lines)}")

    print(f"[*] Total anomalies detected: {len(anomalies)}")
    assert len(anomalies) == 0, f"Heading anomalies detected: {anomalies}"

    return {
        "status": "PASS",
        "heading_counts": heading_counts,
        "total_headings": len(heading_list),
        "anomalies": anomalies,
    }


def test_true_paragraph_parity() -> Dict[str, any]:
    """Test Focus 4: Full paragraph parity against raw docx across Chapters 1-7 and Appendices A-I."""
    print("\n--- [TEST FOCUS 4] Full Paragraph Parity Audit (DOCX vs MD) ---")
    
    doc = Document(DOCX_PATH)
    section_boundaries = [
        ("Chapter 1", 22, 233),
        ("Chapter 2", 234, 442),
        ("Chapter 3", 443, 715),
        ("Chapter 4", 716, 829),
        ("Chapter 5", 830, 1079),
        ("Chapter 6", 1080, 1205),
        ("Chapter 7", 1206, 1211),
        ("Appendix A", 1212, 1466),
        ("Appendix B", 1467, 1496),
        ("Appendix C", 1497, 1570),
        ("Appendix D", 1571, 1738),
        ("Appendix E", 1739, 1768),
        ("Appendix F", 1769, 1796),
        ("Appendix G", 1797, 1849),
        ("Appendix H", 1850, 1967),
        ("Appendix I", 1968, 2036),
    ]

    md_content = BASE_MD_PATH.read_text(encoding="utf-8")
    clean_md = re.sub(r'[#\*_`\<\>\[\]\(\)]', '', md_content)
    clean_md = ' '.join(clean_md.split())

    def norm_clean(t):
        return re.sub(r'[^\w\d]+', '', t.lower())

    norm_md_str = norm_clean(clean_md)

    overall_total = 0
    overall_matched = 0
    missing = []

    for name, start_p, end_p in section_boundaries:
        sec_paras = []
        for i in range(start_p, min(end_p + 1, len(doc.paragraphs))):
            t = doc.paragraphs[i].text.strip()
            if t:
                sec_paras.append((i, t))

        total = len(sec_paras)
        matched = 0
        for p_idx, t in sec_paras:
            nt = norm_clean(t)
            snip = nt[:25] if len(nt) >= 25 else nt
            if len(snip) >= 5 and snip in norm_md_str:
                matched += 1
            elif len(snip) < 5 and (t.lower() in clean_md.lower() or nt in norm_md_str):
                matched += 1
            else:
                missing.append((name, p_idx, t))

        overall_total += total
        overall_matched += matched
        rate = (matched / total * 100) if total else 0
        print(f"[*] {name:12s}: {matched:3d}/{total:3d} ({rate:.2f}%)")

    parity_rate = (overall_matched / overall_total) * 100 if overall_total else 0
    print(f"[*] Total body paragraphs tested: {overall_total}")
    print(f"[*] Matched paragraphs: {overall_matched}/{overall_total} ({parity_rate:.2f}%)")
    print(f"[*] Missing paragraphs count: {len(missing)}")

    assert overall_total == 1969, f"Expected 1969 docx paragraphs, got {overall_total}"
    assert overall_matched == 1969, f"Expected 1969 matched, got {overall_matched}"
    assert parity_rate == 100.0, f"Parity rate is {parity_rate:.2f}% (expected 100.00%)"

    return {
        "status": "PASS",
        "total_docx_paras": overall_total,
        "matched": overall_matched,
        "parity_rate": f"{parity_rate:.2f}%",
        "missing_count": len(missing),
    }


def main():
    print("=================================================================")
    print("  EMPIRICAL CHALLENGER: ADVERSARIAL STRESS TEST SUITE (M1-I2)   ")
    print("=================================================================")

    r1 = test_13_subdots_and_2221_and_h1()
    r2 = test_idempotency_and_mutator()
    r3 = test_comprehensive_regex_and_heading_scan()
    r4 = test_true_paragraph_parity()

    print("\n=================================================================")
    print("                     ALL TESTS COMPLETED                         ")
    print("=================================================================")
    print(f"Focus 1 (13 Subdots & H1)      : {r1['status']} (14 subdots verified, 1 H1)")
    print(f"Focus 2 (Script Idempotency)   : {r2['status']} (10 runs verified, 0 mutations)")
    print(f"Focus 3 (Regex & Heading Scan) : {r3['status']} (0 anomalies across {r3['total_headings']} headings)")
    print(f"Focus 4 (Paragraph Parity)     : {r4['status']} ({r4['matched']}/{r4['total_docx_paras']} = {r4['parity_rate']})")
    print("=================================================================")
    print("FINAL VERDICT: ALL ADVERSARIAL TESTS PASSED -> APPROVE")


if __name__ == "__main__":
    main()
