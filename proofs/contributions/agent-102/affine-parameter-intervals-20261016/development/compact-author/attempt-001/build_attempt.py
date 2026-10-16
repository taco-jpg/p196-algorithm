"""保存本轮原始源码，并以独占的空输出目录串行执行 trust=0 构建。"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

base = Path('/workspace/scratch/fb513c1676b0')
workspace = base / 'agent102-word-intervals/parameter-intervals/compact'
repo = base / 'p196-agent102-intervals/proofs'
attempt = sys.argv[1]
assert re.fullmatch(r'(attempt|final)-[0-9]{3}', attempt)
evidence = workspace / attempt
build = workspace / f'{attempt}-empty-build'
evidence.mkdir(exist_ok=False)
build.mkdir(exist_ok=False)
assert not list(build.iterdir())
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
modules = ['Agent102RunDefs', 'Agent102ParameterIntervalDefs',
           'Agent102ParameterIntervalAlgebra', 'Agent102ParameterIntervalCompact']
source_shas = {}
for name in modules:
    source = repo / f'{name}.lean'
    target = evidence / source.name
    shutil.copyfile(source, target)
    source_shas[name] = digest(target)
exports = ['prune', 'fastInter', 'fastComplement', 'fastInterAll',
           'Interval.inhabited_singleton_of_contains', 'holds_prune',
           'holds_fastInter', 'holds_fastComplement', 'holds_fastInterAll']
body = (evidence / 'Agent102ParameterIntervalCompact.lean').read_text()
actual = re.findall(r'^(?:@\[[^\]]*\]\s*)?(?:def|theorem)\s+([^\s(:]+)', body, re.M)
assert actual == exports, actual
for bad in [r'\bsorry\b', r'\badmit\b', r'\bnative_decide\b', r'^\s*axiom\s']:
    assert not re.search(bad, body, re.M), bad
exports = ['Agent102.ParameterSets.' + n for n in exports]
(evidence / 'LiteralAudit.lean').write_text(
    'import Agent102ParameterIntervalCompact\n\n' +
    ''.join(f'#print axioms {n}\n' for n in exports))
shutil.copyfile(Path(__file__), evidence / 'build_attempt.py')
lean = base / 'agent102-runtime/lean-4.19.0-linux/bin/lean'
env = os.environ.copy()
env['LEAN_PATH'] = str(build)
version = subprocess.run([str(lean), '--version'], text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         check=True).stdout.strip()
print('源码 SHA256：' + source_shas[modules[-1]], flush=True)
results = []
for name in modules + ['LiteralAudit']:
    command = [str(lean), '--trust=0', '-j1', '-DElab.async=false',
               '-o', str(build / f'{name}.olean'), str(evidence / f'{name}.lean')]
    process = subprocess.run(command, cwd=evidence, env=env, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = evidence / f'{name}.log'
    log.write_text(process.stdout)
    results.append({'name': name, 'command': command,
                    'returncode': process.returncode, 'log': str(log)})
    (evidence / 'build-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{name}: {process.returncode}', flush=True)
    if process.returncode:
        print(process.stdout, end='', flush=True)
        break
audit_results = {}
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
if results[-1]['name'] == 'LiteralAudit' and results[-1]['returncode'] == 0:
    for line in (evidence / 'LiteralAudit.log').read_text().splitlines():
        if m := re.fullmatch(r"'([^']+)' does not depend on any axioms", line):
            audit_results[m.group(1)] = []
        elif m := re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line):
            axioms = m.group(2).split(', ') if m.group(2) else []
            assert set(axioms) <= allowed, (m.group(1), axioms)
            audit_results[m.group(1)] = axioms
    assert set(audit_results) == set(exports)
(evidence / 'audit-results.json').write_text(json.dumps(audit_results, indent=2) + '\n')
unchanged = {n: digest(repo / f'{n}.lean') == h for n, h in source_shas.items()}
manifest = {
    'author': '/root/word_intervals',
    'claim': '47e808147f5f0a0dc5ec7340b062112018288c32',
    'receipt': '6225773147', 'scope': '6225680857',
    'worktree_base': '9361e8a8', 'lean_version': version, 'trust': 0,
    'initially_empty_build_directory': str(build),
    'sources_sha256': source_shas, 'source_unchanged_at_end': unchanged,
    'exports': exports, 'results': results,
    'audit_results': audit_results,
    'role': 'Compact 与既有 Algebra 均为本人作者；RunDefs 与 ParameterIntervalDefs 为只读依赖',
}
(evidence / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
files = {p.name: digest(p) for p in sorted(evidence.iterdir()) if p.is_file()}
(evidence / 'SHA256SUMS').write_text(''.join(f'{h}  {n}\n' for n,h in files.items()))
print('导出公理审计数：' + str(len(audit_results)), flush=True)
print('证据：' + str(evidence), flush=True)
assert all(unchanged.values()), unchanged
raise SystemExit(results[-1]['returncode'])
