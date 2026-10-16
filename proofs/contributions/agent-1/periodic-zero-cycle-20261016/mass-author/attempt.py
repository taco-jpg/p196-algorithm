#!/usr/bin/env python3
"""Retain exact incremental sources, compiler output, status and identities."""
import hashlib, json, os, pathlib, subprocess, sys, time
root = pathlib.Path(__file__).resolve().parents[5]
evidence = pathlib.Path(__file__).resolve().parent
build = pathlib.Path('/tmp/agent1-zero-mass-dev-001')
name, label = sys.argv[1:]
dest = evidence / label
dest.mkdir(exist_ok=False)
source = root / 'proofs' / (name + '.lean')
data = source.read_bytes()
(build / source.name).write_bytes(data)
(dest / source.name).write_bytes(data)
lean = '/workspace/p196-tools/lean-4.19.0-linux/bin/lean'
command = [lean, '--trust=0', '-j1', '-DElab.async=false', '-o', name+'.olean', name+'.lean']
start = time.time()
p = subprocess.run(command, cwd=build, env=dict(os.environ, LEAN_PATH=str(build)),
                   text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(dest / 'compile.log').write_text(p.stdout)
(dest / 'receipt.json').write_text(json.dumps(dict(command=command, exit_code=p.returncode,
    source_sha256=hashlib.sha256(data).hexdigest(), seconds=time.time()-start,
    compiler_sha256=hashlib.sha256(pathlib.Path(lean).read_bytes()).hexdigest(),
    source_drift=source.read_bytes()!=data, dependency_objects_reused=True), indent=2)+'\n')
print(p.stdout, end='')
print('exit', p.returncode)
sys.exit(p.returncode)
