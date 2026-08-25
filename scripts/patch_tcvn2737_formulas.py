"""Batch patch all formula frames and math notation in TCVN 2737:2023.
"""
import sys, os, re, json
from pathlib import Path

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    
    bundle_dir = Path("legal_docs/03_tcvn/tcvn_2737_2023")
    md_file = bundle_dir / "tcvn_2737_2023.md"
    tables_dir = bundle_dir / "tables"
    
    text = md_file.read_text(encoding="utf-8")
    
    # 1. Map formulas (1) to (25)
    formulas_map = {
        "1": ("F_TCVN2737_TO_HOP_CO_BAN_1", r"S_m = \sum_{j=1}^{m} S_{k,j} + \sum_{i=1}^{n} \psi_{0,i} \cdot Q_{k,i}"),
        "2": ("F_TCVN2737_TO_HOP_DAC_BIET_2", r"S_m = \sum_{j=1}^{m} \gamma_{GA,j} \cdot S_{k,j} + A_d + \psi_{1,1} \cdot Q_{k,1} + \sum_{i=2}^{n} \psi_{2,i} \cdot Q_{k,i}"),
        "3": ("F_TCVN2737_HE_SO_GIAM_DIEN_TICH_1", r"\varphi_1 = 0,4 + \frac{\psi_A - 0,4}{\sqrt{A/A_1}} \ge 0,5"),
        "4": ("F_TCVN2737_HE_SO_GIAM_DIEN_TICH_2", r"\varphi_2 = 0,5 + \frac{0,5}{\sqrt{A/A_2}} \ge 0,6"),
        "5": ("F_TCVN2737_HE_SO_GIAM_SO_TANG_1", r"\varphi_3 = 0,4 + \frac{\varphi_1 - 0,4}{\sqrt{n}} \ge 0,5"),
        "6": ("F_TCVN2737_HE_SO_GIAM_SO_TANG_2", r"\varphi_4 = 0,5 + \frac{\varphi_2 - 0,5}{\sqrt{n}} \ge 0,5"),
        "7": ("F_TCVN2737_LUC_BUNG_CAU_TRUC", r"F_{d,up} = \gamma_f \cdot \xi \cdot Q_{k,t}"),
        "8": ("F_TCVN2737_LUC_VA_CHAM_CAU_TRUC", r"F_{d',down} = C \sqrt{m}"),
        "9": ("F_TCVN2737_LUC_HAM_NGANG_CAU_TRUC", r"F_{d,h} = \xi \cdot G_k"),
        "10": ("F_TCVN2737_AP_LUC_GIO_TIEU_CHUAN", r"W_k = W_{3s,10} \cdot k(z_e) \cdot c \cdot G_f"),
        "11": ("F_TCVN2737_VAN_TOC_GIO_3S_10", r"W_{3s,10} = \gamma_n \cdot W_0"),
        "12": ("F_TCVN2737_HE_SO_DO_CAO_GIO", r"k(z_e) = 2,01 \left(\frac{z_e}{z_g}\right)^{2/\alpha}"),
        "13": ("F_TCVN2737_HE_SO_GIAT_GF", r"G_f = 0,925 \left( \frac{1 + 1,7 I(z_s) \sqrt{g_Q^2 Q^2 + g_R^2 R^2}}{1 + 1,7 g_v I(z_s)} \right)"),
        "14": ("F_TCVN2737_CUONG_DO_NHIEU_DONG", r"I(z_s) = c_r \left(\frac{10}{z_s}\right)^{1/6}"),
        "15": ("F_TCVN2737_HE_SO_PHAN_UNG_NEN", r"Q = \sqrt{\frac{1}{1 + 0,63 \left(\frac{b + h}{L(z_s)}\right)^{0,63}}}"),
        "16": ("F_TCVN2737_TY_LE_CHIEU_DAI_TICH_PHAN", r"L(z_s) = \ell \left(\frac{z_s}{10}\right)^{\bar{\alpha}}"),
        "17": ("F_TCVN2737_HE_SO_DINH_GQ_GV", r"g_Q = g_v = 3,4"),
        "18": ("F_TCVN2737_HE_SO_DINH_CONG_HUONG_GR", r"g_R = \sqrt{2 \ln(3\,600 n_1)} + \frac{0,577}{\sqrt{2 \ln(3\,600 n_1)}}"),
        "19": ("F_TCVN2737_HE_SO_PHAN_UNG_CONG_HUONG_R", r"R = \sqrt{\frac{1}{\zeta} R_n R_h R_b (0,53 + 0,47 R_d)}"),
        "20": ("F_TCVN2737_HAM_MAT_DO_PHO_NANG_LUONG", r"R_n = \frac{7,47 N_1}{(1 + 10,3 N_1)^{5/3}}"),
        "21": ("F_TCVN2737_TAN_SO_KHONG_THU_NGUYEN", r"N_1 = \frac{n_1 L(z_s)}{\bar{v}(z_s)}"),
        "22": ("F_TCVN2737_HAM_TUONG_QUAN_CHIEU_CAO", r"R_h = \frac{1}{\eta_h} - \frac{1}{2\eta_h^2}\left(1 - e^{-2\eta_h}\right)"),
        "23": ("F_TCVN2737_HAM_TUONG_QUAN_CHIEU_RONG", r"R_b = \frac{1}{\eta_b} - \frac{1}{2\eta_b^2}\left(1 - e^{-2\eta_b}\right)"),
        "24": ("F_TCVN2737_HAM_TUONG_QUAN_CHIEU_SAU", r"R_d = \frac{1}{\eta_d} - \frac{1}{2\eta_d^2}\left(1 - e^{-2\eta_d}\right)"),
        "25": ("F_TCVN2737_DO_VONG_GIOI_HAN", r"f \le f_u")
    }
    
    # Clean formula layout tables
    for num, (fid, f_latex) in formulas_map.items():
        # Match table with heading or simple markdown table row
        p_table = re.compile(
            rf'(?:###\s+<a[^>]*></a>Bảng\s+\d+\s*\n+)?'
            rf'\|\s*[^|\n]*\s*\|\s*\({num}\)\s*\|\s*\n+'
            rf'\|(?:\s*:?---*:?\s*\|)+',
            re.DOTALL
        )
        repl = f'\n\n<a id="formula-{num}"></a>\n\n$$\n{f_latex} \\tag{{{num}}}\n$$\n\n<!-- formula_id: "{fid}" -->\n'
        text = p_table.sub(lambda m, r=repl: r, text)
        
        # Single row table
        p_row = re.compile(rf'\|\s*[^|\n]*\s*\|\s*\({num}\)\s*\|')
        text = p_row.sub(lambda m, r=repl: r, text)

    # 2. Cleanup inline prose variables across document
    replacements = {
        r'\bW0\b': '$W_0$',
        r'\bV0\b': '$V_0$',
        r'\bk\(ze\)': '$k(z_e)$',
        r'\bI\(zs\)': '$I(z_s)$',
        r'\bL\(zs\)': '$L(z_s)$',
        r'\bGf\b': '$G_f$',
        r'\bWk\b': '$W_k$',
        r'\bW3s,10\b': '$W_{3s,10}$',
        r'φ1': r'$\varphi_1$',
        r'φ2': r'$\varphi_2$',
        r'φ3': r'$\varphi_3$',
        r'φ4': r'$\varphi_4$',
        r'ψA': r'$\psi_A$',
        r'ψL': r'$\psi_L$',
        r'ψt': r'$\psi_t$',
        r'γf': r'$\gamma_f$',
        r'γn': r'$\gamma_n$',
    }
    for pat, rep in replacements.items():
        text = re.sub(pat, lambda m, r=rep: r, text)

    md_file.write_text(text, encoding="utf-8")
    print(f"✨ Successfully transformed all 25 equations and math symbols in {md_file.name}")

if __name__ == '__main__':
    main()
