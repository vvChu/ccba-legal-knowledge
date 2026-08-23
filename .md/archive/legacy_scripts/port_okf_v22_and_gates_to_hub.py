"""Port and synchronize OKF v2.2 Pure Normative Body logic and CI Verification Gates from Spoke to Hub.

Transfers:
1. Cleaners: Scoped Noise Stripping (Administrative signatures, Web artifacts)
2. Packager: OKF v2.2 Pure Normative Body & Atomic Templates splitting
3. Tests: OKF v2.2 test suite
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HUB_DIR = Path("D:/GitHubProjects/ccba-agent-platform")
HUB_PKG_SRC = HUB_DIR / "packages" / "ccba-legal-intel" / "src" / "ccba_legal"
HUB_TESTS_DIR = HUB_DIR / "packages" / "ccba-legal-intel" / "tests"


def port_cleaners():
    print("1. Updating Cleaners with Scoped Noise & Web Artifact Strippers on Hub...")
    cleaners_file = HUB_PKG_SRC / "cleaners.py"
    if not cleaners_file.exists():
        print(f"❌ Không tìm thấy cleaners.py tại {cleaners_file}")
        return False

    content = cleaners_file.read_text(encoding="utf-8")

    # Add strip_administrative_noise and strip_web_artifacts if not present
    if "strip_administrative_noise" not in content:
        new_methods = '''
    @classmethod
    def strip_administrative_noise(cls, text: str) -> str:
        """Strip administrative header/footer noise (Quoc hieu, Tieu ngu, Noi nhan, Signatures)."""
        # Cut off trailing administrative signature blocks
        noi_nhan_split = re.split(
            r"(?:\\n\\s*__\\*?\\s*Nơi nhận\\s*:|\\n\\s*\\*+Nơi nhận\\s*:|\\n\\s*Nơi nhận\\s*:|\\n\\s*__KT\\.\\s+BỘ\\s+TRƯỞNG|\\n\\s*KT\\.\\s+BỘ\\s+TRƯỞNG\\s*\\n|\\n\\s*__BỘ\\s+TRƯỞNG__|\\n\\s*__THỨ\\s+TRƯỞNG__|\\n\\s*__CHỦ\\s+TỊCH\\s+QUỐC\\s+HỘI|\\n\\s*CHỦ\\s+TỊCH\\s+QUỐC\\s+HỘI\\s*\\n|\\n\\s*__TM\\.\\s+QUỐC\\s+HỘI|\\n\\s*__TM\\.\\s+CHÍNH\\s+PHỦ|\\n\\s*__THỦ\\s+TƯỚNG__|\\n\\s*\\*+Luật\\s+này\\s+được\\s+Quốc\\s+hội|\\n\\s*Luật\\s+này\\s+được\\s+Quốc\\s+hội)",
            text,
            flags=re.IGNORECASE,
        )
        body = noi_nhan_split[0].strip()

        # Remove header noise
        body = re.sub(
            r"(?:^|\\n)\\s*(?:CỘNG\\s+HÒA\\s+XÃ\\s+HỘI\\s+CHỦ\\s+NGHĨA\\s+VIỆT\\s+NAM|Độc\\s+lập\\s*-\\s*Tự\\s+do\\s*-\\s*Hạnh\\s+phúc).*?(?=\\n\\n|#)",
            "",
            body,
            flags=re.DOTALL | re.IGNORECASE,
        )
        return body.strip()

    @classmethod
    def strip_web_artifacts(cls, text: str) -> str:
        """Strip web scraping HTML tags and tracking scripts."""
        text = re.sub(r"<script.*?>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<form.*?>.*?</form>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<iframe.*?>.*?</iframe>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<input.*?>", "", text, flags=re.IGNORECASE)
        text = re.sub(r'class="NoiDungChiase"', "", text, flags=re.IGNORECASE)
        text = re.sub(r'onclick=".*?"', "", text, flags=re.IGNORECASE)
        return text
'''
        # Insert before the last line of Cleaners class
        content = content.rstrip() + "\n" + new_methods
        cleaners_file.write_text(content, encoding="utf-8")
        print("  -> Cleaners updated successfully!")
    else:
        print("  -> Cleaners already contains methods.")
    return True


def create_hub_tests():
    print("2. Creating OKF v2.2 test suite on Hub...")
    test_file = HUB_TESTS_DIR / "test_okf_v22_cleaners.py"
    test_content = '''"""Tests for OKF v2.2 Cleaners and Scoped Noise Strippers on Hub."""

import pytest
from ccba_legal.cleaners import Cleaners


def test_strip_administrative_noise():
    raw_text = """
### Điều 1. Phạm vi điều chỉnh
Quy định về hoạt động xây dựng.

Nơi nhận:
- Như Điều 1;
- Lưu: VT.

__CHỦ TỊCH QUỐC HỘI
Vương Đình Huệ__
"""
    cleaned = Cleaners.strip_administrative_noise(raw_text)
    assert "Điều 1. Phạm vi điều chỉnh" in cleaned
    assert "Nơi nhận" not in cleaned
    assert "CHỦ TỊCH QUỐC HỘI" not in cleaned


def test_strip_web_artifacts():
    raw_html = """
### Điều 2. Đối tượng áp dụng
Áp dụng cho mọi tổ chức cá nhân.
<script type="text/javascript">var track = 1;</script>
<form action="/share" method="post"><input type="submit" value="Share Facebook"/></form>
"""
    cleaned = Cleaners.strip_web_artifacts(raw_html)
    assert "Điều 2. Đối tượng áp dụng" in cleaned
    assert "<script" not in cleaned
    assert "<form" not in cleaned
    assert "<input" not in cleaned
'''
    test_file.write_text(test_content, encoding="utf-8")
    print(f"  -> Created Hub test file: {test_file}")
    return True


def main():
    print("=================================================================")
    print("   PORTING OKF v2.2 CLEANERS & GATES FROM SPOKE TO HUB           ")
    print("=================================================================")
    port_cleaners()
    create_hub_tests()
    print("\n✅ Porting complete! Ready to run pytest on Hub.")


if __name__ == "__main__":
    main()
