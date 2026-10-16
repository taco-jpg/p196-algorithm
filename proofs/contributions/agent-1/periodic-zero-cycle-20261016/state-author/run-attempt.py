#!/usr/bin/env python3
"""Retain strict author-module attempts against the frozen provided dependency build."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = ROOT / 'proofs/Agent1PeriodicZeroState.lean'
DEPENDENCIES = Path('/workspace/p196-agent1-session-20261016/periodic-zero-period-author-build')
LEAN = Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
PERIOD_SHA = '3761744f62cabdf25cf69f8e2990ce81eec9ac75cfb2273a5e80974304795a8a'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    label = sys.argv[1]
    assert re.fullmatch(r'[a-zA-Z0-9_-]+', label)
    out = HERE / label
    out.mkdir(exist_ok=False)
    raw = SOURCE.read_bytes()
    (out / SOURCE.name).write_bytes(raw)
    pins = {}

    def visit(name):
        if name in pins or name in {'Std', 'Lean', 'Init'}:
            return
        path = DEPENDENCIES / (name + '.lean')
        obj = DEPENDENCIES / (name + '.olean')
        data = path.read_bytes()
        pins[name] = {'source': str(path), 'sha256': sha(data),
                      'object': str(obj), 'object_sha256': sha(obj.read_bytes())}
        for dep in re.findall(r'^import\s+(\S+)', data.decode(), re.M):
            visit(dep)

    visit('Agent1PeriodicZeroPeriod')
    assert pins['Agent1PeriodicZeroPeriod']['sha256'] == PERIOD_SHA
    assert sha((ROOT / 'proofs/Agent1PeriodicZeroPeriod.lean').read_bytes()) == PERIOD_SHA
    version = subprocess.check_output([str(LEAN), '--version'], text=True).strip()
    assert 'version 4.19.0,' in version and 'commit 6caaee842e94' in version
    env = {'PATH': str(LEAN.parent) + ':/usr/bin:/bin', 'LANG': 'C.UTF-8',
           'LEAN_PATH': str(out) + ':' + str(DEPENDENCIES)}
    argv = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false',
            '-o', SOURCE.stem + '.olean', SOURCE.name]
    started = time.monotonic()
    with (out / 'compile.log').open('wb') as stream:
        try:
            rc = subprocess.run(argv, cwd=out, env=env, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=600).returncode
        except subprocess.TimeoutExpired:
            rc = 124
    unchanged = SOURCE.read_bytes() == raw and all(
        sha(Path(pin['source']).read_bytes()) == pin['sha256'] and
        sha(Path(pin['object']).read_bytes()) == pin['object_sha256'] for pin in pins.values())
    report = {'status': 'PASS' if rc == 0 and unchanged else 'FAIL', 'exit_code': rc,
              'seconds': time.monotonic() - started, 'command': argv, 'environment': env,
              'compiler_version': version, 'compiler_sha256': sha(LEAN.read_bytes()),
              'source_sha256': sha(raw), 'source_git_blob': hashlib.sha1(
                  b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(),
              'source_snapshot': str(out / SOURCE.name), 'dependencies': pins,
              'source_and_dependencies_unchanged': unchanged,
              'fresh_dependency_build': False,
              'scope': 'Strict author increment; provided frozen dependency objects reused.'}
    (out / 'receipt.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['status', 'exit_code', 'seconds', 'source_sha256']}))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
