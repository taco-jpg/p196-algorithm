#!/usr/bin/env python3
"""Author increment reusing the seventeen pinned independently checked validity objects."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, time

ROOT = Path('/workspace/p196-agent1-zero-cycle-20261016')
EVIDENCE = ROOT/'proofs/contributions/agent-1/periodic-zero-cycle-20261016/zero-period-author'
BUILD = Path('/workspace/p196-agent1-session-20261016/periodic-zero-period-author-build')
DEPS = Path('/workspace/p196-agent1-session-20261016/periodic-validity-review-clean-001')
REVIEW = ROOT/'proofs/contributions/agent-1/periodic-validity-20261016/review/clean-001'
LEAN = Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
MODULE = 'Agent1PeriodicZeroPeriod'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
attempt = EVIDENCE/sys.argv[1]
attempt.mkdir(parents=True, exist_ok=False)
BUILD.mkdir(parents=True, exist_ok=True)
assert json.loads((REVIEW/'verification.json').read_text())['status'] == 'PASS'
assert sha(LEAN) == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
deps = []
for entry in json.loads((REVIEW/'sources.json').read_text()):
    name = entry['module']
    assert sha(ROOT/entry['path']) == entry['sha256']
    assert sha(DEPS/(name+'.lean')) == entry['sha256']
    hashes = {}
    for suffix in ['.lean','.olean']:
        src, dst = DEPS/(name+suffix), BUILD/(name+suffix)
        hashes[suffix] = sha(src)
        if dst.exists(): assert sha(dst) == hashes[suffix]
        else: shutil.copy2(src,dst)
        assert sha(dst) == hashes[suffix]
    deps.append(dict(entry, reused_files=hashes))
(attempt/'dependencies.json').write_text(json.dumps(dict(
    provenance=str(REVIEW), object_origin=str(DEPS),
    qualification='Author incremental reuse; not a fresh or independent rebuild.', modules=deps), indent=2)+'\n')
source = ROOT/'proofs'/(MODULE+'.lean')
shutil.copy2(source,attempt/source.name)
shutil.copy2(source,BUILD/source.name)
command = [str(LEAN),'--trust=0','-j1','-DElab.async=false','-o',MODULE+'.olean',MODULE+'.lean']
record = dict(command=command,cwd=str(BUILD),LEAN_PATH=str(BUILD),source_sha256=sha(source),
              compiler_sha256=sha(LEAN),started_at_epoch=time.time())
(attempt/'run.json').write_text(json.dumps(record,indent=2)+'\n')
start = time.monotonic()
with (attempt/'compile.log').open('w') as log:
    rc = subprocess.run(command,cwd=BUILD,env=dict(os.environ,LEAN_PATH=str(BUILD)),
                        stdout=log,stderr=subprocess.STDOUT).returncode
record.update(exit_code=rc,seconds=time.monotonic()-start,log_sha256=sha(attempt/'compile.log'),
              finished_at_epoch=time.time())
(attempt/'run.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2)); print((attempt/'compile.log').read_text())
raise SystemExit(rc)
