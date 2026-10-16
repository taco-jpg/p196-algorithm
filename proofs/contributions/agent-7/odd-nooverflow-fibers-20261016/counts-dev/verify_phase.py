#!/usr/bin/env python3
"""Freshly rebuild the six-phase formulas against the frozen fixed-center checkpoint."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
PINNED = ROOT / 'fixed-002' / 'source'
LEAN = Path('/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean')
attempt = 1
while (ROOT / f'phase-{attempt:03d}').exists():
    attempt += 1
OUT = ROOT / f'phase-{attempt:03d}'
SRC = OUT / 'source'
SRC.mkdir(parents=True)
modules = ['InverseFibers','PathCounts','WordBridge','OddCenter','OddCounts','OddCountsFixedCenter','OddCountsPhase']
sources = {}
for module in modules:
    src = (ROOT if module == modules[-1] else PINNED) / f'{module}.lean'
    dest = SRC / src.name
    shutil.copyfile(src, dest)
    sources[module] = {'original':str(src),'snapshot':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
env = dict(os.environ)
env['LEAN_PATH'] = str(SRC)
records = []
for module in modules:
    cmd = [str(LEAN),'--trust=0','-j1','-DElab.async=false','-o',f'{module}.olean',f'{module}.lean']
    start = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(cmd,cwd=SRC,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log = OUT / f'{module}.log'
    log.write_text(result.stdout)
    records.append({'module':module,'command':cmd,'cwd':str(SRC),'started_at':start,'exit_code':result.returncode,'log':str(log),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
    print(f'{module}: exit {result.returncode}',flush=True)
    if module == modules[-1] or result.returncode:
        print(result.stdout,end='',flush=True)
    if result.returncode:
        break
report = {'timestamp':datetime.now(timezone.utc).isoformat(),'lean':str(LEAN),'lean_sha256':hashlib.sha256(LEAN.read_bytes()).hexdigest(),'source_snapshots':sources,'records':records,'all_passed':len(records)==len(modules) and all(r['exit_code']==0 for r in records)}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('REPORT '+str(OUT/'verification.json'),flush=True)
raise SystemExit(0 if report['all_passed'] else 1)
