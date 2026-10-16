#!/usr/bin/env python3
"""Independent reviewer: initial fresh dependency build, then named snapshots."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

REPO = Path('/workspace/scratch/50e90e07524e/p196-agent106')
CONTRIB = REPO / 'proofs/contributions/agent-106/run-births'
EVIDENCE = CONTRIB / 'review/nooverflow-reviewer'
BUILD = Path('/workspace/scratch/50e90e07524e/review106-nooverflow-fresh')
LEAN = Path('/workspace/scratch/50e90e07524e/runtime/lean-4.19.0-linux/bin/lean')
PRELOAD = '/workspace/scratch/50e90e07524e/runtime/readlink_self.so'
BASE = REPO / 'proofs/research/continuation/LychrelDigitSums.lean'

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def execute(name, src, report):
    target = BUILD / (name + '.lean')
    shutil.copyfile(src, target)
    env = dict(os.environ, LEAN_PATH=str(BUILD), LD_PRELOAD=PRELOAD)
    env.pop('LEAN_SRC_PATH', None)
    env.pop('LEAN_SYSROOT', None)
    cmd = [str(LEAN), '-j1', '-DElab.async=false', '-o', name + '.olean', name + '.lean']
    start = time.monotonic()
    proc = subprocess.run(cmd, cwd=BUILD, env=env, text=True, capture_output=True)
    log = EVIDENCE / (name + '.log')
    log.write_text(proc.stdout + proc.stderr)
    item = dict(module=name, source_path=str(src.relative_to(REPO)),
        source_sha256=digest(target), log_sha256=digest(log),
        command=cmd, exit_code=proc.returncode, seconds=time.monotonic()-start)
    report['modules'].append(item)
    (EVIDENCE/'rebuild.json').write_text(json.dumps(report, indent=2)+'\n')
    assert digest(src) == item['source_sha256'], 'Source changed during compilation'
    assert proc.returncode == 0, name + ' failed; see its log'
    assert not any(x in log.read_text() for x in ['sorryAx', 'error:', 'Lean.ofReduceBool', 'Lean.trustCompiler'])
    print(name, 'PASS', item['source_sha256'], flush=True)

if sys.argv[1:] == ['initial']:
    assert not BUILD.exists(), 'Initial build directory must not exist'
    BUILD.mkdir()
    report = dict(reviewer='nooverflow_births', build_dir=str(BUILD), initially_empty=True,
        lean_sha256=digest(LEAN), preload_sha256=digest(PRELOAD),
        script_sha256=digest(__file__), modules=[])
    env = dict(os.environ, LD_PRELOAD=PRELOAD)
    report['version'] = subprocess.check_output([str(LEAN), '--version'], env=env, text=True).strip()
    assert 'version 4.19.0,' in report['version']
    execute('BaseBirths', CONTRIB/'BaseBirths.lean', report)
    execute('LychrelDigitSums', BASE, report)
else:
    report = json.loads((EVIDENCE/'rebuild.json').read_text())
    for old in report['modules']:
        assert digest(BUILD/(old['module']+'.lean')) == old['source_sha256']
        assert digest(REPO/old['source_path']) == old['source_sha256']
    for name in sys.argv[1:]:
        execute(name, CONTRIB/(name+'.lean'), report)
