import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(".")
Q06_DIR = ROOT / "legal_docs" / "02_qcvn" / "qcvn_06_2022_bxd"
BASE_FILE = Q06_DIR / "qcvn_06_2022_bxd.md"
HN_FILE = Q06_DIR / "qcvn_06_2022_bxd_hop_nhat_2023.md"

def standardize_14(file_path):
    text = file_path.read_text(encoding="utf-8")
    
    # Locate section 1.4
    # From <a id="muc-1-4"></a>\s*### 1.4  Giải thích từ ngữ up to <a id="muc-1-5"> or next section
    m = re.search(r'(<a id="muc-1-4"></a>\s*### 1\.4\s+Giải thích từ ngữ[\s\S]*?)(?=<a id="muc-1-5">|<a id="muc-2">)', text)
    if not m:
        print(f"Error: Section 1.4 not found in {file_path}")
        return
    
    sec_text = m.group(1)
    
    # Regex to find definition blocks:
    # Pattern: #### <a id="muc-1-4-(\d+)" name="muc-1-4-\1"></a>1\.4\.\1\s*\n\s*([^\n#]+)\s*\n\s*([\s\S]*?)(?=(?:#### <a id="muc-1-4-|\Z))
    def repl(match):
        num = match.group(1)
        anchor = f"muc-1-4-{num}"
        term = match.group(2).strip()
        body = match.group(3).strip()
        return f'#### <a id="{anchor}" name="{anchor}"></a>1.4.{num}  {term}\n\n{body}\n\n'
    
    pattern = r'#### <a id="muc-1-4-(\d+)"(?: name="[^"]*")?></a>1\.4\.\1\s*\n\s*([^\n#<]+)\s*\n\s*([\s\S]*?)(?=(?:#### <a id="muc-1-4-|\Z))'
    
    # Test how many matches
    matches = list(re.finditer(pattern, sec_text))
    print(f"Found {len(matches)} definitions in {file_path.name}")
    
    new_sec_text = re.sub(pattern, repl, sec_text)
    new_text = text[:m.start(1)] + new_sec_text + text[m.end(1):]
    file_path.write_text(new_text, encoding="utf-8")
    print(f"✅ Successfully standardized section 1.4 in {file_path.name}")

standardize_14(BASE_FILE)
standardize_14(HN_FILE)
