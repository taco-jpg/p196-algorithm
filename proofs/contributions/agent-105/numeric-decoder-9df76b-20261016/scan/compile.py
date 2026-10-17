from pathlib import Path
import os, subprocess, time, json, hashlib, sys, datetime
root = Path('/workspace/scratch/9df76b503b84/agent105-decoder-work/proofs')
src = root / 'Agent105DecoderScan9df76b.lean'
ev = root / 'contributions/agent-105/numeric-decoder-9df76b-20261016/scan'
label = sys.argv[1]
if not label.isalnum(): raise RuntimeError('invalid label')
if (ev / (label + '.json')).exists(): raise RuntimeError('refusing to overwrite attempt')
(ev / 'build').mkdir(exist_ok=True)
(ev / (label + '.lean')).write_bytes(src.read_bytes())
env = os.environ.copy()
env['LEAN_PATH'] = str(root / 'contributions/agent-105/numeric-decoder-9df76b-20261016/local/build') + ':/workspace/scratch/9df76b503b84/agent105-runtime/base-build'
cmd = ['/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean', '--trust=0', '-o', str(ev / 'build/Agent105DecoderScan9df76b.olean'), str(src)]
t0 = time.time()
p = subprocess.run(cmd, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
(ev / (label + '.log')).write_text(p.stdout)
metadata = {'command': cmd, 'source_sha256': hashlib.sha256(src.read_bytes()).hexdigest(), 'exit_code': p.returncode, 'wall_seconds': time.time() - t0, 'lean_path': env['LEAN_PATH'], 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(ev / (label + '.json')).write_text(json.dumps(metadata, indent=2) + '\n')
print(json.dumps(metadata))
print(p.stdout)
