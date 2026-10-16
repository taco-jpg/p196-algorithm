"""对已冻结的新接口只执行一次串行 clean trust=0 构建链。"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess

base = Path('/workspace/scratch/fb513c1676b0')
work = base / 'agent102-word-intervals/universal-author'
repo = base / 'p196-agent102-universal/proofs'
evidence = work / 'final-001'
build = work / 'final-001-empty-build'
evidence.mkdir(exist_ok=False)
build.mkdir(exist_ok=False)
assert not list(build.iterdir())
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
frozen = ['Agent102RunDefs', 'Agent102AffineArithmetic', 'Agent102RunWord',
          'Agent102RunEndpoints', 'Agent102AffineRuns', 'Agent102AffineBoundary',
          'Agent102AffineDecision']
preserved_sources = {}
for name in frozen:
    path = repo / f'{name}.lean'
    old = base / 'p196-agent102/proofs' / f'{name}.lean'
    assert digest(path) == digest(old), name
    preserved_sources[name] = digest(path)
modules = ['Agent102RunDefs', 'Agent102RunWord', 'Agent102RunDecision']
source_shas = {}
for name in modules:
    source = repo / f'{name}.lean'
    target = evidence / source.name
    shutil.copyfile(source, target)
    source_shas[name] = digest(target)
new_source = (evidence / 'Agent102RunDecision.lean').read_text()
exports = ['Agent102.compressedEqual', 'Agent102.compressedEqual_eq_true_iff',
           'Agent102.compressedEqual_eq_false_iff', 'Agent102.equalAt',
           'Agent102.equalAt_eq_true_iff', 'Agent102.equalAt_eq_false_iff']
actual = ['Agent102.' + name for name in re.findall(
    r'^(?:def|theorem)\s+([^\s(:]+)', new_source, re.M)]
assert actual == exports, actual
for bad in (r'\bsorry\b', r'\badmit\b', r'\bnative_decide\b', r'^\s*axiom\s'):
    assert not re.search(bad, new_source, re.M), bad
body = new_source.split('def compressedEqual ', 1)[1].split('\ntheorem ', 1)[0]
assert not re.search(r'\b(word|wordAt|positivePart|replicate|equalOnTail)\b', body)
audit = evidence / 'LiteralAudit.lean'
audit.write_text('import Agent102RunDecision\n\n'
    '/- 全部六个新接口的独立逐字公理审计。 -/\n'
    + ''.join(f'#print axioms {name}\n' for name in exports))
shutil.copyfile(Path(__file__), evidence / 'final_build.py')
lean = base / 'agent102-runtime/lean-4.19.0-linux/bin/lean'
env = os.environ.copy()
env['LEAN_PATH'] = str(build)
version = subprocess.run([str(lean), '--version'], text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout.strip()
print('冻结源码 SHA256：' + source_shas['Agent102RunDecision'], flush=True)
results = []
for name in modules + ['LiteralAudit']:
    command = [str(lean), '--trust=0', '-j1', '-DElab.async=false',
               '-o', str(build / f'{name}.olean'), str(evidence / f'{name}.lean')]
    process = subprocess.run(command, cwd=evidence, env=env, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = evidence / f'{name}.log'
    log.write_text(process.stdout)
    results.append({'name': name, 'command': command, 'returncode': process.returncode,
                    'log': str(log)})
    (evidence / 'build-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{name}: {process.returncode}', flush=True)
    if process.returncode:
        print(process.stdout, end='', flush=True)
        break
audit_results = {}
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
if results[-1]['returncode'] == 0 and results[-1]['name'] == 'LiteralAudit':
    for line in (evidence / 'LiteralAudit.log').read_text().splitlines():
        if match := re.fullmatch(r"'([^']+)' does not depend on any axioms", line):
            audit_results[match.group(1)] = []
        elif match := re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line):
            axioms = match.group(2).split(', ') if match.group(2) else []
            assert set(axioms) <= allowed, (match.group(1), axioms)
            audit_results[match.group(1)] = axioms
    assert set(audit_results) == set(exports)
for name, sha in preserved_sources.items():
    assert digest(repo / f'{name}.lean') == sha, name
for name, sha in source_shas.items():
    assert digest(repo / f'{name}.lean') == sha, name
(evidence / 'audit-results.json').write_text(json.dumps(audit_results, indent=2) + '\n')
files = {path.name: digest(path) for path in sorted(evidence.iterdir()) if path.is_file()}
(evidence / 'SHA256SUMS').write_text(''.join(f'{sha}  {name}\n' for name, sha in files.items()))
manifest = {
    'author': '/root/word_intervals, Agent #102 的真实子代理',
    'claim': 'e685d582b0bd1035733a1f86751af54b07e78792',
    'scope_announcement': '6225317747',
    'scope_receipt': '6225373772',
    'worktree_base': 'cba5dc44',
    'lean_version': version,
    'trust': 0,
    'build_directory_initially_empty': True,
    'build_directory': str(build),
    'single_serial_fresh_chain': modules + ['LiteralAudit'],
    'source_sha256': source_shas,
    'seven_frozen_sources_unchanged_sha256': preserved_sources,
    'exports': exports,
    'computational_body_does_not_expand_word': True,
    'correctness_has_no_parameter_cutoff_or_positive_length_assumption': True,
    'results': results,
    'files_sha256': files,
}
(evidence / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print('完整导出审计：' + str(len(audit_results)), flush=True)
print('最终证据：' + str(evidence), flush=True)
raise SystemExit(results[-1]['returncode'])
