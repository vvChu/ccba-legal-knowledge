"""
CCBA Legal Knowledge — Vietnam Wind Pressure Zone Database & Lookup Solver.
Cơ sở dữ liệu phân vùng áp lực gió W0 cho 63 tỉnh/thành theo Bảng 5.1 QCVN 02:2022/BXD & Bảng 7 TCVN 2737:2023.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from formulas.models import CalculationResult, CalculationStep

VIETNAM_WIND_ZONES_TABLE: dict[str, list[dict[str, Any]]] = {
    "Thành phố Hà Nội": [
        {
            "scope": "Tất cả các quận, thị xã, huyện (không bao gồm các huyện Mỹ Đức, Phú Xuyên, Thường Tín và Ứng Hòa)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Mỹ Đức (xã Đại Hưng, xã Hùng Tiến, xã Hương Sơn, xã Vạn Kim)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Mỹ Đức (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Phú Xuyên (xã Phú Túc, xã Hồng Minh, xã Tri Trung)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Phú Xuyên (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Thường Tín (xã Minh Cường, xã Thống Nhất, xã Tô Hiệu, xã Vạn Điểm, xã Văn Tự)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Thường Tín (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Ứng Hoà (thị trấn Vân Đình, xã Quảng Phú Cầu, xã Liên Bạt, xã Đồng Tiến, xã Sơn Công, xã Hoa Sơn, xã Trường Thịnh, xã Viên Nội, xã Viên An, xã Cao Thành, xã Hoà Xá)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Ứng Hoà (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        }
    ],
    "Thành phố Hồ Chí Minh": [
        {
            "scope": "Tất cả các thành phố, quận, huyện (bao gồm cả thành phố Thủ Đức, không bao gồm huyện Củ Chi)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Củ Chi",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Thành phố Hải Phòng": [
        {
            "scope": "Tất cả các quận, huyện (không bao gồm các huyện Bạch Long Vĩ và Thủy Nguyên)",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 55.0,
            "v10m_50": 39.0
        },
        {
            "scope": "Huyện Bạch Long Vĩ",
            "zone": "V",
            "w0": 185.0,
            "v3s_50": 61.0,
            "v10m_50": 43.0
        },
        {
            "scope": "Huyện Thuỷ Nguyên",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        }
    ],
    "Thành phố Đà Nẵng": [
        {
            "scope": "Tất cả các quận, huyện (không bao gồm các huyện Hòa Vang và Hoàng Sa)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Hòa Vang (xã Hòa Ninh, xã Hòa Phú, xã Hòa Khương)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Hòa Vang (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Hoàng Sa (tất cả các đảo thuộc quần đảo Hoàng Sa)",
            "zone": "V",
            "w0": 185.0,
            "v3s_50": 61.0,
            "v10m_50": 43.0
        }
    ],
    "Thành phố Cần Thơ": [
        {
            "scope": "Tất cả các quận, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "An Giang": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm các huyện Thoại Sơn, Tri Tôn)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Thoại Sơn (thị trấn Phú Hòa, xã Định Mỹ, xã Định Thành, xã Phú Thuận, xã Tây Phú, xã Vĩnh Chánh, xã Vĩnh Phú, xã Vĩnh Trạch)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Thoại Sơn (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Tri Tôn (thị trấn Ba Chúc, thị trấn Tri Tôn, xã Châu Lăng, xã Lạc Quới, xã Lê Trì, xã Núi Tô, xã Tà Đảnh)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Tri Tôn (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Bà Rịa - Vũng Tàu": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm huyện Côn Đảo)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Côn Đảo",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        }
    ],
    "Bạc Liêu": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Bắc Giang": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm huyện Sơn Động)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Sơn Động (thị trấn Tây Yên Tử, xã Dương Hưu, xã Long Sơn, xã Thanh Luận)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Sơn Động (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Bắc Kạn": [
        {
            "scope": "Tất cả các huyện (không bao gồm thành phố Bắc Kạn và huyện Ngân Sơn)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Thành phố Bắc Kạn",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Ngân Sơn",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Bắc Ninh": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm huyện Lương Tài)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Lương Tài (xã Lai Hạ, xã Minh Tân, xã Trung Chính, xã Trung Kênh, xã Trừng Xá)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Lương Tài (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Bến Tre": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Bình Dương": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Bình Định": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm các huyện An Lão, Hoài Ân, Tây Sơn, Vân Canh và Vĩnh Thạnh)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện An Lão (xã An Toàn, xã An Vinh, xã An Nghĩa)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện An Lão (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Hoài Ân (xã Dak Mang, xã Bok Tới, xã Ân Nghĩa, xã Ân Sơn)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Hoài Ân (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Tây Sơn (xã Bình Thuận, xã Tây An, xã Tây Vinh)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Tây Sơn (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Vân Canh (thị trấn Vân Canh, xã Canh Liên, xã Canh Thuận, xã Canh Hòa)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Vân Canh (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Vĩnh Thạnh",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Bình Phước": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Bình Thuận": [
        {
            "scope": "Thành phố Phan Thiết",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Bắc Bình (xã Bình An, xã Bình Tân, xã Hải Ninh, xã Phan Điền, xã Phan Lâm, xã Phan Sơn, xã Phan Thanh, xã Phan Tiến, xã Sông Bình, xã Sông Lũy)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Bắc Bình (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đức Linh",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Hàm Tân",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Hàm Thuận Bắc (thị trấn Phú Long, xã Hồng Sơn, xã Hàm Liêm, xã Hàm Đức, xã Hàm Hiệp, xã Hàm Thắng)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Hàm Thuận Bắc (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Hàm Thuận Nam (xã Hàm Cần, xã Hàm Thạnh, xã Mương Mán, xã Mỹ Thạnh)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Hàm Thuận Nam (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Phú Quý",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Tánh Linh",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Tuy Phong",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Thị xã La Gi",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Cà Mau": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Cao Bằng": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Đắk Lắk": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm huyện M'Đrắk)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện M'Đrắk (thị trấn M'Đrắk, xã Cư M'ta, xã Ea Pil, xã Krông Á, xã Krông Jing)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện M'Đrắk (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Đắk Nông": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Điện Biên": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Đồng Nai": [
        {
            "scope": "Thành phố Biên Hòa",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Thành phố Long Khánh",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Cẩm Mỹ",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Định Quán",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Long Thành",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Nhơn Trạch",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Tân Phú",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Thống Nhất",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Trảng Bom",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Vĩnh Cửu",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Xuân Lộc",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Đồng Tháp": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm các huyện Châu Thành và Lai Vung)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Châu Thành",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Lai Vung (xã Phong Hòa, xã Long Thắng, xã Tân Hòa, xã Định Hòa)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Lai Vung (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Gia Lai": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Hà Giang": [
        {
            "scope": "Thành phố Hà Giang",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Bắc Mê",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Bắc Quang",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đồng Văn",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Hoàng Su Phì",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Mèo Vạc",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Quang Bình",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Quản Bạ",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Vị Xuyên",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Xín Mần",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Yên Minh",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Hà Nam": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm huyện Bình Lục)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Bình Lục",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 55.0,
            "v10m_50": 39.0
        }
    ],
    "Hà Tĩnh": [
        {
            "scope": "Thành phố Hà Tĩnh",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 55.0,
            "v10m_50": 39.0
        },
        {
            "scope": "Thị xã Hồng Lĩnh",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 55.0,
            "v10m_50": 39.0
        },
        {
            "scope": "Thị xã Kỳ Anh",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Can Lộc",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 55.0,
            "v10m_50": 39.0
        },
        {
            "scope": "Huyện Cẩm Xuyên (thị trấn Thiên Cầm, xã Cẩm Dương, xã Yên Hòa, xã Cẩm Lĩnh, xã Cẩm Lộc, xã Cẩm Nhượng, xã Cẩm Trung)",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Cẩm Xuyên (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Đức Thọ",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Hương Khê (xã Hương Lâm, xã Hương Liên, xã Hương Trà, xã Hương Vĩnh, xã Hương Xuân, xã Phú Gia, xã Phú Phong)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Hương Khê (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Hương Sơn (thị trấn Tây Sơn, xã Quang Diệm, xã Sơn Hàm, xã Sơn Hồng, xã Sơn Kim 1, xã Sơn Kim 2, xã Sơn Lĩnh, xã Sơn Tây)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Hương Sơn (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Kỳ Anh",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Nghi Xuân",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Thạch Hà",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Vũ Quang",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Lộc Hà",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        }
    ],
    "Hải Dương": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm huyện Tứ Kỳ)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Tứ Kỳ",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        }
    ],
    "Hậu Giang": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Hòa Bình": [
        {
            "scope": "Tất cả các thành phố, huyện (không bao gồm các huyện Đà Bắc, Lạc Thủy, Mai Châu và Yên Thủy)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đà Bắc (thị trấn Đà Bắc, xã Tân Minh, xã Vầy Nưa, xã Cao Sơn, xã Tú Lý, xã Hiền Lương, xã Toàn Sơn)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đà Bắc (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Lạc Thuỷ (thị trấn Ba Hàng Đồi, xã Hưng Thi, xã Phú Thành, xã Thống Nhất, xã Phú Lão,)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Lạc Thuỷ (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Mai Châu (thị trấn Mai Châu, xã Mai Hạ, xã Mai Hịch, xã Nà Phòn, xã Sơn Thủy, xã Tân Thành, xã Đồng Tân, xã Thành Sơn, xã Vạn Mai)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Mai Châu (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Yên Thuỷ (xã Lạc Lương, xã Lạc Thịnh, xã Lạc Sĩ, xã Đa Phúc)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Yên Thuỷ (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        }
    ],
    "Hưng Yên": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm các huyện Văn Giang và Văn Lâm)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Văn Giang",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Văn Lâm",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Khánh Hòa": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm các huyện Khánh Sơn, Khánh Vĩnh và Trường Sa)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Khánh Sơn",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Khánh Vĩnh",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Trường Sa (tất cả các đảo thuộc quần đảo Trường Sa)",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        }
    ],
    "Kiên Giang": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm các huyện Kiên Hải và thành phố Phú Quốc)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Thành phố Phú Quốc (bao gồm đảo Phú Quốc và các đảo khác thuộc thành phố Phú Quốc), Huyện Kiên Hải",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        }
    ],
    "Kon Tum": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Lai Châu": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Lạng Sơn": [
        {
            "scope": "Tất cả các thành phố, huyện (không bao gồm các huyện Đình Lập và Hữu Lũng)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Đình Lập (xã Bắc Lãng, xã Châu Sơn, xã Đồng Thắng, xã Lâm Ca)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đình Lập (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Hữu Lũng (xã Đồng Tiến, xã Hoà Thắng, xã Minh Hòa, xã Minh Sơn, xã Thanh Sơn, xã Vân Nham)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Hữu Lũng (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Lào Cai": [
        {
            "scope": "Tất cả các thành phố, huyện (không bao gồm thị xã Sa Pa và các huyện Bát Xát và Văn Bàn)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Thị xã Sa Pa",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Bát Xát (Thị trấn Bát Xát, xã Quang Kim, xã Tòng Sành)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Bát Xát (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Văn Bàn (xã Dần Thàng, xã Dương Qùy, xã Hòa Mạc, xã Khánh Yên Hạ, xã Khánh Yên Trung, xã Minh Lương, xã Nậm Chầy, xã Nậm Mả, xã Nậm Xây, xã Nậm Xé, xã Thẩm Dương)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Văn Bàn (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Lâm Đồng": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Long An": [
        {
            "scope": "Thành phố Tân An",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Bến Lức",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Cần Giuộc",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Cần Đước",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Châu Thành",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đức Hoà",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Đức Huệ",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Mộc Hoá",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Tân Hưng",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Tân Thạnh",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Tân Trụ",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Thạnh Hoá",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Thủ Thừa",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Vĩnh Hưng",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Thị xã Kiến Tường",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Nam Định": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        }
    ],
    "Nghệ An": [
        {
            "scope": "Thành phố Vinh",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Thị xã Cửa Lò",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Thị xã Hoàng Mai",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Thị xã Thái Hoà",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Con Cuông",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Diễn Châu",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Đô Lương",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Hưng Nguyên",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Kỳ Sơn",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Nam Đàn",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Nghi Lộc (xã Nghi Thiết, xã Khánh Hợp, xã Nghi Quang, xã Nghi Tiến)",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Nghi Lộc (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Nghĩa Đàn (xã Nghĩa An, xã Nghĩa Đức, xã Nghĩa Hiếu, xã Nghĩa Hồng, xã Nghĩa Hưng, xã Nghĩa Khánh, xã Nghĩa Thành, xã Nghĩa Mai, xã Nghĩa Minh, xã Nghĩa Thịnh, xã Nghĩa Yên)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Nghĩa Đàn (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Quế Phong",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Quỳ Châu (xã Châu Bính, xã Châu Hạnh, xã Châu Hội, xã Châu Nga)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Quỳ Châu (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Quỳ Hợp",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Quỳnh Lưu (xã An Hoà, xã Quỳnh Nghĩa, xã Quỳnh Bảng, xã Quỳnh Đôi, xã Quỳnh Long, xã Quỳnh Lương, xã Quỳnh Minh, xã Quỳnh Thanh, xã Quỳnh Thuận, xã Quỳnh Yên, xã Tiến Thuỷ)",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Quỳnh Lưu (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Tân Kỳ",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Thanh Chương",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Tương Dương",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Yên Thành (xã Đô Thành, xã Đức Thành, xã Hậu Thành, xã Hoa Thành, xã Hồng Thành, xã Hợp Thành, xã Lăng Thành, xã Mã Thành, xã Nhân Thành, xã Phú Thành, xã Phúc Thành, xã Sơn Thành, xã Tân Thành, xã Thọ Thành, xã Tiến Thành, xã Văn Thành, xã Viên Thành, xã Vĩnh Thành)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Yên Thành (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Ninh Bình": [
        {
            "scope": "Thành phố Ninh Bình",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Thành phố Tam Điệp",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Gia Viễn",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Hoa Lư",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Kim Sơn",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Nho Quan",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Yên Khánh",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Yên Mô",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        }
    ],
    "Ninh Thuận": [
        {
            "scope": "Thành phố Phan Rang - Tháp Chàm",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Bác Ái",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Ninh Hải",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Ninh Phước",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Ninh Sơn",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Thuận Bắc",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Thuận Nam",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Phú Thọ": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Phú Yên": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm các huyện Đồng Xuân, Sông Hinh, Sơn Hoà và Tây Hòa)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Đồng Xuân (xã Phú Mỡ, xã Xuân Phước, xã Xuân Quang 1, xã Xuân Quang 2, xã Xuân Quang 3)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đồng Xuân (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Sông Hinh",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Sơn Hoà",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Tây Hòa (xã Hòa Mỹ Đông, xã Hòa Mỹ Tây, xã Hoà Phong, xã Hòa Phú, xã Sơn Thành Đông, xã Sơn Thành Tây)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Tây Hòa (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        }
    ],
    "Quảng Bình": [
        {
            "scope": "Thành phố Đồng Hới",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Thị xã Ba Đồn",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Bố Trạch (xã Bắc Trạch, xã Đại Trạch, xã Đồng Trạch, xã Đức Trạch, xã Hải Phú, xã Lý Trạch, xã Nhân Trạch, xã Thanh Trạch, xã Trung Trạch)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Bố Trạch (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Lệ Thuỷ (xã Ngư Thủy Bắc, xã Ngư Thủy, xã Sen Thủy)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Lệ Thuỷ (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Minh Hoá",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Quảng Ninh",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Quảng Trạch",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Tuyên Hoá",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Quảng Nam": [
        {
            "scope": "Thành phố Tam Kỳ",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Thành phố Hội An",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Thị xã Điện Bàn",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Bắc Trà My (xã Trà Bui, xã Trà Đốc, xã Trà Sơn, xã Trà Tân)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Bắc Trà My (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Duy Xuyên (xã Duy Sơn, xã Duy Phú, xã Duy Hòa, xã Duy Trinh, xã Duy Châu, xã Duy Thu, xã Duy Tân)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Duy Xuyên (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Đại Lộc",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đông Giang",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Hiệp Đức",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Nam Giang",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Nam Trà My",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Nông Sơn",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Núi Thành",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Phước Sơn",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Quế Sơn (thị trấn Hương An, xã Quế Mỹ, xã Quế Phú, xã Quế Xuân 1, xã Quế Xuân 2)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Quế Sơn (các địa danh hành chính còn lại)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Tây Giang",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Thăng Bình",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Tiên Phước",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Phú Ninh (Thị trấn Phú Thịnh, xã Tam Lãnh, xã Tam Lộc, xã Tam Dân, xã Tam Vinh, xã Tam Phước, xã Tam Thái)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Phú Ninh (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        }
    ],
    "Quảng Ngãi": [
        {
            "scope": "Tất cả các thành phố, huyện (không bao gồm các huyện Ba Tơ, Minh Long, Sơn Hà, Sơn Tây và Trà Bồng)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Ba Tơ",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Minh Long",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Sơn Hà",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Sơn Tây (xã Sơn Lập, xã Sơn Tân, xã Sơn Màu, xã Sơn Tinh)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Sơn Tây (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Trà Bồng",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Quảng Ninh": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm thị xã Quảng Yên, các huyện Bình Liêu, Cô Tô và Vân Đồn)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Bình Liêu",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Cô Tô",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Thị xã Quảng Yên",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Vân Đồn",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        }
    ],
    "Quảng Trị": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm các huyện Gio Linh, Hướng Hóa, Triệu Phong, Vĩnh Linh và Cồn Cỏ)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Gio Linh",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Hướng Hoá",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Triệu Phong",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Vĩnh Linh",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Cồn Cỏ",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        }
    ],
    "Sóc Trăng": [
        {
            "scope": "Tất cả thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Sơn La": [
        {
            "scope": "Tất cả thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Tây Ninh": [
        {
            "scope": "Tất cả thành phố, thị xã, huyện",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Thái Bình": [
        {
            "scope": "Tất cả thành phố, thị xã, huyện",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        }
    ],
    "Thái Nguyên": [
        {
            "scope": "Tất cả các thành phố, thị xã, huyện (không bao gồm các huyện Đồng Hỷ, Phú Lương và Võ Nhai)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đồng Hỷ (thị trấn Trại Cau, xã Hợp Tiến, xã Nam Hoà, xã Tân Lợi)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đồng Hỷ (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Phú Lương",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Võ Nhai",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        }
    ],
    "Thanh Hóa": [
        {
            "scope": "Thành phố Thanh Hóa",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Thành phố Sầm Sơn",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Thị xã Bỉm Sơn",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Thị xã Nghi Sơn",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Bá Thước",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Cẩm Thuỷ",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Đông Sơn",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Hà Trung (xã Hà Hải, xã Lĩnh Toại, xã Hà Vinh)",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Hà Trung (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Hậu Lộc",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Hoằng Hoá",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Lang Chánh",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Mường Lát",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Nga Sơn",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Ngọc Lặc",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Như Thanh",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Như Xuân",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Nông Cống",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Quảng Xương (thị trấn Tân Phong, xã Quảng Hòa, xã Quảng Hợp, xã Quảng Long, xã Quảng Ngọc, xã Quảng Phúc, xã Quảng Trạch, xã Quảng Văn, xã Quảng Yên)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Quảng Xương (các địa danh hành chính còn lại)",
            "zone": "IV",
            "w0": 155.0,
            "v3s_50": 56.0,
            "v10m_50": 40.0
        },
        {
            "scope": "Huyện Quan Hoá",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Quan Sơn",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Thạch Thành",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Thọ Xuân (thị trấn Lam Sơn, Thị trấn Sao Vàng, xã Quảng Phú, xã Thọ Diên, xã Thọ Hải, xã Thọ Lâm, xã Thọ Lập, xã Thuận Minh, xã Thọ Xương, xã Xuân Bái, xã Xuân Hòa, xã Xuân Hưng, xã Xuân Phú, xã Xuân Thiên, xã Xuân Tín)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Thọ Xuân (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Thường Xuân",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Thiệu Hóa",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Triệu Sơn",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Vĩnh Lộc",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Yên Định",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        }
    ],
    "Thừa Thiên Huế": [
        {
            "scope": "Thành phố Huế",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Thị xã Hương Thủy",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Thị xã Hương Trà",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện A Lưới",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Nam Đông (xã Thượng Lộ, xã Hương Phú, xã Hương Lộc)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Nam Đông (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Phú Lộc (thị trấn Phú Lộc, xã Lộc Điền, xã Lộc Trì, xã Xuân Lộc, xã Lộc Hoà, xã Lộc Bổn, xã Lộc An, xã Lộc Sơn, xã Vinh Hưng)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Phú Lộc (các địa danh hành chính còn lại)",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Phú Vang",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Phong Điền",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        },
        {
            "scope": "Huyện Quảng Điền",
            "zone": "III",
            "w0": 125.0,
            "v3s_50": 50.0,
            "v10m_50": 36.0
        }
    ],
    "Tiền Giang": [
        {
            "scope": "Tất cả thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Trà Vinh": [
        {
            "scope": "Tất cả thành phố, thị xã, quận, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Tuyên Quang": [
        {
            "scope": "Thành phố Tuyên Quang",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Chiêm Hoá",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Hàm Yên",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Na Hang",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Sơn Dương",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Yên Sơn",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Lâm Bình",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Vĩnh Long": [
        {
            "scope": "Tất cả thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Vĩnh Phúc": [
        {
            "scope": "Tất cả thành phố, thị xã, huyện",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ],
    "Yên Bái": [
        {
            "scope": "Thành phố Yên Bái",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Thị xã Nghĩa Lộ",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Lục Yên",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Mù Căng Chải",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Trạm Tấu",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Trấn Yên",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Văn Chấn (thị trấn Nông trường Liên Sơn, xã Cát Thịnh, xã Gia Hội, xã Nậm Búng, xã Nậm Lành, xã Nghĩa Sơn, xã Sơn Lương, xã Sơn Thịnh, xã Tú Lệ)",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        },
        {
            "scope": "Huyện Văn Chấn (các địa danh hành chính còn lại)",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Văn Yên",
            "zone": "I",
            "w0": 65.0,
            "v3s_50": 36.0,
            "v10m_50": 26.0
        },
        {
            "scope": "Huyện Yên Bình",
            "zone": "II",
            "w0": 95.0,
            "v3s_50": 44.0,
            "v10m_50": 31.0
        }
    ]
}


def _normalize_name(text: str) -> str:
    """Chuẩn hóa tên địa danh: bỏ dấu tiếng Việt, viết thường, loại bỏ tiền tố."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    no_acc = "".join([c for c in nfkd if not unicodedata.combining(c)])
    no_acc = no_acc.replace("đ", "d").replace("Đ", "d").lower().strip()
    no_acc = re.sub(r"^(thanh pho|tinh|quan|huyen|thi xa|phuong|xa|thi tran|dao|quan dao)\s+", "", no_acc)
    no_acc = re.sub(r"[^a-z0-9\s]", " ", no_acc)
    return re.sub(r"\s+", " ", no_acc).strip()


def calc_base_wind_pressure_w0(
    province: str,
    district: str = "",
    commune: str = "",
) -> CalculationResult:
    """Tra cứu áp lực gió cơ sở W0 theo địa danh hành chính (Bảng 5.1 QCVN 02:2022 / Bảng 7 TCVN 2737:2023)."""
    if not province or not province.strip():
        raise ValueError("Tên tỉnh / thành phố không được để trống.")

    norm_prov = _normalize_name(province)
    matched_prov_key = None
    
    for prov_key in VIETNAM_WIND_ZONES_TABLE:
        if norm_prov == _normalize_name(prov_key) or norm_prov in _normalize_name(prov_key):
            matched_prov_key = prov_key
            break

    if not matched_prov_key:
        available = ", ".join(list(VIETNAM_WIND_ZONES_TABLE.keys())[:10]) + "..."
        raise ValueError(f"Không tìm thấy tỉnh/thành phố '{province}'. Một số tỉnh/thành sẵn có: {available}")

    entries = VIETNAM_WIND_ZONES_TABLE[matched_prov_key]
    selected_entry = None
    match_detail = "Mặc định toàn tỉnh/thành"

    norm_dist = _normalize_name(district) if district else ""
    norm_comm = _normalize_name(commune) if commune else ""

    if norm_dist or norm_comm:
        for item in entries:
            scope_raw = item["scope"]
            norm_scope = _normalize_name(scope_raw)
            if norm_comm and norm_comm in norm_scope and "khong bao gom" not in norm_scope:
                selected_entry = item
                match_detail = f"Khớp cụ thể xã/phường: {commune} ({scope_raw})"
                break
            if norm_dist and norm_dist in norm_scope:
                if "khong bao gom" in norm_scope:
                    continue
                selected_entry = item
                match_detail = f"Khớp quận/huyện: {district} ({scope_raw})"
                break

    if not selected_entry:
        for item in entries:
            scope_raw = item["scope"]
            if "tat ca" in _normalize_name(scope_raw) or "toan bo" in _normalize_name(scope_raw):
                selected_entry = item
                match_detail = f"Theo phạm vi chung: {scope_raw}"
                break
        if not selected_entry and entries:
            selected_entry = entries[0]
            match_detail = f"Theo mục đầu tiên: {selected_entry['scope']}"

    if not selected_entry:
        raise ValueError(f"Không tìm thấy dữ liệu phân vùng gió cho {matched_prov_key}.")

    zone = selected_entry["zone"]
    w0 = selected_entry["w0"]
    v3s = selected_entry["v3s_50"]
    v10m = selected_entry["v10m_50"]

    steps = [
        CalculationStep(
            step_number=1,
            description="Tra cứu phân vùng áp lực gió theo địa danh hành chính",
            formula_latex=r"W_0	ext{ tra theo Bảng 5.1 QCVN 02:2022/BXD}",
            substitution=f"Địa danh: {matched_prov_key} -> {match_detail}",
            result_text=f"Vùng gió {zone}: W0 = {w0:g} daN/m2 (V3s,50 = {v3s:g} m/s, V10m,50 = {v10m:g} m/s)",
        )
    ]

    notes = [
        f"Địa danh tra cứu: {matched_prov_key}" + (f", {district}" if district else "") + (f", {commune}" if commune else ""),
        f"Phạm vi áp dụng: {selected_entry['scope']}",
        "Căn cứ: Bảng 5.1 QCVN 02:2022/BXD và Bảng 7 TCVN 2737:2023.",
    ]

    return CalculationResult(
        formula_id="F_WIND_QCVN02_W0_LOOKUP",
        formula_name=f"Áp lực gió cơ sở W0 ({matched_prov_key})",
        standard_reference="Bảng 5.1 QCVN 02:2022/BXD & Bảng 7 TCVN 2737:2023",
        inputs={"province": province, "district": district, "commune": commune},
        outputs={
            "wind_zone": zone,
            "W0_daN_m2": w0,
            "W0_kNm2": round(w0 / 100.0, 4),
            "V3s_50_ms": v3s,
            "V10m_50_ms": v10m,
        },
        unit="daN/m2",
        primary_value=w0,
        steps=steps,
        notes=notes,
        is_compliant=True,
        compliance_message=f"Đã tra cứu thành công áp lực gió cơ sở W0 = {w0:g} daN/m2 cho {matched_prov_key}.",
    )
