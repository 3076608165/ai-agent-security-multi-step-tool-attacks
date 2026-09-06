import base64, json, re, pathlib

# 1. clean v9 exfil source (truncate decoded to EXPECTED_BYTES=26823)
src = open('pull_current/attack_decoded.py', 'rb').read()[:26823].decode('utf-8')

# 2. flip the two frontier knobs
src = src.replace('PROBE_HOPS = 0', 'PROBE_HOPS = 1')
src = src.replace('REPLAY_COST_COEF = 0.95', 'REPLAY_COST_COEF = 2.0')
assert 'PROBE_HOPS = 1' in src and 'REPLAY_COST_COEF = 2.0' in src
compile(src, 'attack.py', 'exec')
print('patched + compiled OK, len', len(src))

# 3. build notebook cell (implicit-concat base64)
b = base64.b64encode(src.encode('utf-8')).decode('ascii')
chunks = [b[i:i+64] for i in range(0, len(b), 64)]
chunk_lines = '\n'.join('    ' + repr(c) for c in chunks)

cell = '''# AI Agent Security submission - writes attack.py (base64, corruption-proof) + placeholder submission.csv
import base64, csv, os, pathlib
EXPECTED_BYTES = %d
ATTACK_B64 = (
%s
)
data = base64.b64decode(ATTACK_B64)
assert len(data) == EXPECTED_BYTES, f'attack.py corrupted on paste: {len(data)} != {EXPECTED_BYTES}'
src = data.decode('utf-8')
compile(src, 'attack.py', 'exec')
out = pathlib.Path('/kaggle/working/attack.py')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(src, encoding='utf-8')
print(f'Wrote {out} ({len(data)} bytes)  [expected {EXPECTED_BYTES}]')

with open('/kaggle/working/submission.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['Id', 'Score'])
    for rid in ['gpt_oss_public', 'gpt_oss_private', 'gemma_public', 'gemma_private']:
        w.writerow([rid, 0])
print('Wrote placeholder /kaggle/working/submission.csv (overwritten by the official rerun)')

if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
    from kaggle_evaluation.jed_attack_134815.jed_attack_inference_server import (
        JEDAttackInferenceServer,
    )
    JEDAttackInferenceServer().run()
else:
    print('Not a competition rerun; server startup skipped for normal notebook save/run.')
''' % (len(src.encode('utf-8')), chunk_lines)

# 4. notebook json (reuse structure from pull_current, enable GPU)
nb = json.load(open('pull_current/notebook3497b27639.ipynb', encoding='utf-8'))
nb['cells'] = [{'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [cell]}]

meta = json.load(open('pull_current/kernel-metadata.json', encoding='utf-8'))
meta['enable_gpu'] = True
meta['enable_internet'] = False

outdir = pathlib.Path('push_gpu_probe')
outdir.mkdir(exist_ok=True)
json.dump(nb, open(outdir/'notebook3497b27639.ipynb', 'w', encoding='utf-8'), indent=1)
json.dump(meta, open(outdir/'kernel-metadata.json', 'w', encoding='utf-8'), indent=2)
print('wrote', outdir, 'enable_gpu:', meta['enable_gpu'])
