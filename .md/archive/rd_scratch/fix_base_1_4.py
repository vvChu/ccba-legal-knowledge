import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(".")
BUNDLE_DIR = ROOT_DIR / "legal_docs" / "02_qcvn" / "qcvn_04_2021_bxd"
BASE_MD = BUNDLE_DIR / "qcvn_04_2021_bxd.md"

# List of known definition terms from 1.4.1 to 1.4.30 in QCVN 04:2021/BXD
DEF_TERMS = {
    "1.4.1": "Nhà chung cư",
    "1.4.2": "Cụm nhà chung cư",
    "1.4.3": "Nhà chung cư hỗn hợp",
    "1.4.4": "Phần căn hộ trong nhà chung cư hỗn hợp",
    "1.4.5": "Căn hộ",
    "1.4.6": "Căn hộ chung cư",
    "1.4.7": "Phần chức năng khác",
    "1.4.8": "Căn hộ lưu trú",
    "1.4.9": "Văn phòng kết hợp lưu trú",
    "1.4.10": "Chiều cao nhà",
    "1.4.11": "Chiều cao thông thủy",
    "1.4.12": "Chiều cao phòng cháy chữa cháy (Chiều cao PCCC)",
    "1.4.13": "Diện tích sử dụng căn hộ",
    "1.4.14": "Số tầng nhà",
    "1.4.15": "Tầng áp mái",
    "1.4.16": "Tầng trên mặt đất",
    "1.4.17": "Tầng hầm",
    "1.4.18": "Tầng nửa hầm",
    "1.4.19": "Tầng kỹ thuật",
    "1.4.20": "Gian kỹ thuật",
    "1.4.21": "Phòng ở",
    "1.4.22": "Ban công",
    "1.4.23": "Lô gia",
    "1.4.24": "Không gian sinh hoạt cộng đồng",
    "1.4.25": "Sảnh thang máy",
    "1.4.26": "Khoang đệm",
    "1.4.27": "Khoang cháy",
    "1.4.28": "Tuổi thọ thiết kế",
    "1.4.29": "Tiêu chuẩn lựa chọn áp dụng",
    "1.4.30": "Tài liệu chuẩn"
}

text = BASE_MD.read_text(encoding="utf-8")

for code, term in DEF_TERMS.items():
    # Replace any variation
    # E.g. #### <a id="muc-1-4-X" name="muc-1-4-X"></a>1.4.X  TermText...
    anchor_id = f"muc-{code.replace('.', '-')}"
    pattern = re.compile(
        rf'####\s*<a id="{anchor_id}"[^>]*></a>\s*{re.escape(code)}\s*(?:{re.escape(term)})?\s*\n*(.*?)(?=\n####\s*<a id="muc-1-4-|\n<a id="muc-2">)',
        re.DOTALL
    )
    m = pattern.search(text)
    if m:
        content = m.group(1).strip()
        # Clean any leading term duplication if it got merged
        if content.startswith(term):
            content = content[len(term):].strip()
            
        replacement = f'#### <a id="{anchor_id}" name="{anchor_id}"></a>{code}  {term}\n\n{content}\n\n'
        text = text[:m.start()] + replacement + text[m.end():]

BASE_MD.write_text(text, encoding="utf-8")
print("✅ Successfully formatted all 30 definition terms in base QCVN 04!")
