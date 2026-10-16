from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, time

ROOT = Path('/workspace/scratch/fb513c1676b0/p196-agent102')
OUT = Path('/workspace/scratch/fb513c1676b0/agent102-parent')
LEAN = '/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean'
label = sys.argv[1]
modules = sys.argv[2:]
dest = OUT / label
dest.mkdir(parents=True, exist_ok=False)
env = dict(os.environ)
env['LEAN_PATH'] = str(dest)
results = []
for module in modules:
    source = ROOT / 'proofs' / (module + '.lean')
    data = source.read_bytes()
    (dest / source.name).write_bytes(data)
    cmd = [LEAN, '--trust=0', '-j1', '-DElab.async=false', '-o', module+'.olean', module+'.lean']
    t = time.monotonic()
    r = subprocess.run(cmd, cwd=dest, env=env, capture_output=True, text=True, timeout=240)
    (dest / (module+'.log')).write_text(r.stdout+r.stderr)
    rec = dict(module=module, sha256=hashlib.sha256(data).hexdigest(), command=cmd,
               exit_code=r.returncode, seconds=time.monotonic()-t)
    results.append(rec)
    (dest/'receipt.json').write_text(json.dumps(results,indent=2)+'\n')
    print(module, 'exit',r.returncode,flush=True)
    if r.returncode:
        print(r.stdout+r.stderr,flush=True)
        sys.exit(r.returncode)
