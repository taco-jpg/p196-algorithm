"""仅对证据本地控制文件执行一次增量 trust=0 内核检查。"""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import time

base = Path('/workspace/scratch/fb513c1676b0')
workspace = base / 'agent102-word-intervals/parameter-intervals/compact'
evidence = workspace / 'controls-001'
build = workspace / 'controls-001-empty-build'
dependencies = workspace / 'attempt-001-empty-build'
repo = base / 'p196-agent102-intervals/proofs'
build.mkdir(exist_ok=False)
assert not list(build.iterdir())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
accepted = json.loads((workspace / 'attempt-001/manifest.json').read_text())
dependency_record = {}
for name, expected in accepted['sources_sha256'].items():
    current = repo / f'{name}.lean'
    saved = workspace / 'attempt-001' / current.name
    assert sha(current) == sha(saved) == expected, name
    obj = dependencies / f'{name}.olean'
    assert obj.exists(), name
    dependency_record[name] = {'source_sha256': expected, 'olean': str(obj),
                              'olean_sha256': sha(obj)}
source = evidence / 'CompactControls.lean'
before = sha(source)
lean = base / 'agent102-runtime/lean-4.19.0-linux/bin/lean'
command = [str(lean), '--trust=0', '-j1', '-DElab.async=false',
           '-o', str(build / 'CompactControls.olean'), str(source)]
env = os.environ.copy()
env['LEAN_PATH'] = str(build) + ':' + str(dependencies)
started = time.monotonic()
process = subprocess.run(command, cwd=evidence, env=env, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
elapsed = time.monotonic() - started
log = evidence / 'CompactControls.log'
log.write_text(process.stdout)
exports = ['Agent102.ParameterSets.CompactControls.' + s
           for s in ['empty_128', 'reversed_128', 'mixed_128']]
audit_results = {}
for line in process.stdout.splitlines():
    if m := re.fullmatch(r"'([^']+)' does not depend on any axioms", line):
        audit_results[m.group(1)] = []
    elif m := re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line):
        audit_results[m.group(1)] = m.group(2).split(', ') if m.group(2) else []
manifest = {'author': '/root/word_intervals',
            'role': '作者追加的具体控制；不是独立审查或一般复杂度证明',
            'trust': 0, 'lean_version': accepted['lean_version'],
            'command': command, 'LEAN_PATH': env['LEAN_PATH'],
            'returncode': process.returncode, 'elapsed_seconds': elapsed,
            'source_sha256': before, 'dependencies': dependency_record,
            'audit_results': audit_results,
            'execution': '仅一次增量调用；依赖复用本人已 fresh trust=0 验证且源 SHA 再次一致的产物'}
(evidence / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
files = sorted(p for p in evidence.iterdir() if p.is_file())
(evidence / 'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in files))
print('CompactControls exit: ' + str(process.returncode), flush=True)
print(process.stdout, end='', flush=True)
print('单次调用秒数：' + str(elapsed), flush=True)
assert sha(source) == before
if process.returncode == 0:
    assert set(audit_results) == set(exports), audit_results
    assert all(not deps for deps in audit_results.values()), audit_results
raise SystemExit(process.returncode)
