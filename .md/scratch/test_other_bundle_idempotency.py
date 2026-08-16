import os, sys, hashlib, subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = 'legal_docs/01_vbpl/luat_phong_chay_chua_chay_va_cuu_nan_cuu_ho_2024_55_2024_qh1'

def get_hash(fpath):
    with open(fpath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

md_file = os.path.join(bundle_dir, 'luat_phong_chay_chua_chay_va_cuu_nan_cuu_ho_2024_55_2024_qh1.md')
h1 = get_hash(md_file)

cmd = [sys.executable, 'scripts/gold_standard_processor.py', bundle_dir, '--type', 'vbpl']
subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

h2 = get_hash(md_file)

print('PCCC Bundle MD Hash Before:', h1)
print('PCCC Bundle MD Hash After :', h2)
print('Matches?', h1 == h2)
