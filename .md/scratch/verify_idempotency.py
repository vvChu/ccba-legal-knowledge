import os, glob, hashlib, subprocess, sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

bundle_dir = 'legal_docs/01_vbpl/luat_xay_dung_2025_135_2025_qh15'

def get_bundle_hashes():
    hashes = {}
    for root, _, files in os.walk(bundle_dir):
        for file in sorted(files):
            fpath = os.path.join(root, file)
            relpath = os.path.relpath(fpath, bundle_dir)
            with open(fpath, 'rb') as f:
                hashes[relpath] = hashlib.sha256(f.read()).hexdigest()
    return hashes

print('=== 1. SNAPSHOT BEFORE GOLD STANDARD PROCESSOR ===')
before_hashes = get_bundle_hashes()
for f, h in before_hashes.items():
    print(f'  {f:35s}: {h}')

print('\n=== 2. RUNNING GOLD STANDARD PROCESSOR ===')
cmd = [sys.executable, 'scripts/gold_standard_processor.py', bundle_dir, '--type', 'vbpl']
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print('Exit code:', res.returncode)
print('Stdout:', res.stdout)
print('Stderr:', res.stderr)

print('\n=== 3. SNAPSHOT AFTER GOLD STANDARD PROCESSOR ===')
after_hashes = get_bundle_hashes()
for f, h in after_hashes.items():
    print(f'  {f:35s}: {h}')

print('\n=== 4. IDEMPOTENCY COMPARISON ===')
diff_found = False
all_keys = sorted(list(set(before_hashes.keys()) | set(after_hashes.keys())))
for f in all_keys:
    h_before = before_hashes.get(f, 'MISSING')
    h_after = after_hashes.get(f, 'MISSING')
    if h_before != h_after:
        diff_found = True
        print(f'  DIFF in {f}:')
        print(f'    BEFORE: {h_before}')
        print(f'    AFTER : {h_after}')
    else:
        print(f'  MATCH: {f}')

if not diff_found:
    print('\nRESULT: PERFECT IDEMPOTENCY! 0 changes detected after re-running processor.')
else:
    print('\nRESULT: DIFF DETECTED after re-running processor.')
