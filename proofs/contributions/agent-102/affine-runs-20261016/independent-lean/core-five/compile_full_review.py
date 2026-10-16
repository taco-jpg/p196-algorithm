"""冻结五模块闭包的独立 trust=0 重建及逐声明公理审计。"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

base = Path('/workspace/scratch/fb513c1676b0')
work = base / 'agent102-word-intervals'
repo = base / 'p196-agent102/proofs'
label = sys.argv[1]
evidence = work / label
build = work / f'{label}-empty-build'
evidence.mkdir(exist_ok=False)
build.mkdir(exist_ok=False)
assert not list(build.iterdir())
names = ['Agent102RunDefs', 'Agent102AffineArithmetic', 'Agent102RunWord',
         'Agent102RunEndpoints', 'Agent102AffineRuns']
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
registry_source = repo / 'Agent102AffineRuns.registry.json'
shutil.copyfile(registry_source, evidence / 'registry-input.json')
registry = json.loads((evidence / 'registry-input.json').read_text())
registered = registry['projects']['agent102-affine-runs']['modules']
decls = []
theorems = []
source_shas = {}
source_imports = {}
for name in names:
    source = repo / f'{name}.lean'
    target = evidence / source.name
    shutil.copyfile(source, target)
    source_shas[name] = digest(target)
    assert source_shas[name] == registered[name]['sha256'], name
    text = target.read_text()
    source_imports[name] = re.findall(r'^import\s+(\S+)', text, re.M)
    assert source_imports[name] == registered[name]['imports'], name
    for bad in (r'\bsorry\b', r'\badmit\b', r'\bnative_decide\b', r'^\s*axiom\s'):
        assert not re.search(bad, text, re.M), (name, bad)
    stack = []
    for line in text.splitlines():
        if m := re.match(r'^namespace\s+(\S+)', line):
            stack.append(m.group(1))
        elif re.match(r'^end(?:\s+\S+)?\s*$', line):
            assert stack, (name, line)
            stack.pop()
        elif m := re.match(r'^(?:@\[[^\n]*\]\s*)?(theorem|def|structure)\s+([^\s(:]+)', line):
            full = '.'.join(stack + [m.group(2)])
            decls.append({'name': full, 'kind': m.group(1), 'module': name})
            if m.group(1) == 'theorem':
                theorems.append(full)
    assert not stack, name
assert len(theorems) == 75, len(theorems)
assert len(set(d['name'] for d in decls)) == len(decls)
registered_claims = registry['claims'][0]['endpoints']
assert set(registered_claims) <= set(theorems)
omitted_from_registry = sorted(set(theorems) - set(registered_claims))
assert all('?' in name for name in omitted_from_registry), omitted_from_registry
audit = evidence / 'FullLiteralAudit.lean'
audit.write_text('import Agent102AffineRuns\n\n'
    '/- 独立从冻结源枚举全部 75 条定理以及所有显式定义、结构；名称逐字保留。 -/\n'
    + ''.join(f'#print axioms {item["name"]}\n' for item in decls))
shutil.copyfile(Path(__file__), evidence / 'compile_full_review.py')
lean = base / 'agent102-runtime/lean-4.19.0-linux/bin/lean'
env = os.environ.copy()
env['LEAN_PATH'] = str(build)
version = subprocess.run([str(lean), '--version'], text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout.strip()
results = []
for name in names + ['FullLiteralAudit']:
    command = [str(lean), '--trust=0', '-o', str(build / f'{name}.olean'),
               str(evidence / f'{name}.lean')]
    process = subprocess.run(command, cwd=evidence, env=env, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = evidence / f'{name}.log'
    log.write_text(process.stdout)
    results.append({'name': name, 'command': command, 'returncode': process.returncode,
                    'log': str(log)})
    print(f'{name}: {process.returncode}', flush=True)
    if process.returncode:
        print(process.stdout, end='', flush=True)
        break
audit_results = {}
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
if results[-1]['returncode'] == 0 and results[-1]['name'] == 'FullLiteralAudit':
    for line in (evidence / 'FullLiteralAudit.log').read_text().splitlines():
        if m := re.fullmatch(r"'([^']+)' does not depend on any axioms", line):
            audit_results[m.group(1)] = []
        elif m := re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line):
            axioms = m.group(2).split(', ') if m.group(2) else []
            assert set(axioms) <= allowed, (m.group(1), axioms)
            audit_results[m.group(1)] = axioms
    assert set(audit_results) == {d['name'] for d in decls}
    print(f'逐字审计：{len(theorems)} 条定理，{len(decls)} 个显式声明，均仅依赖标准公理。', flush=True)
unchanged = {name: digest(repo / f'{name}.lean') == source_shas[name] for name in names}
assert all(unchanged.values()), unchanged
(evidence / 'audit-results.json').write_text(json.dumps(audit_results, indent=2) + '\n')
sha = {path.name: digest(path) for path in sorted(evidence.iterdir()) if path.is_file()}
(evidence / 'SHA256SUMS').write_text(''.join(f'{value}  {name}\n' for name, value in sha.items()))
manifest = {
    'reviewer': '/root/word_intervals, Agent #102 的真实子代理',
    'role_boundaries': {
        'Agent102RunWord': '本子代理是作者，此模块重建为作者验证，不冒称独立来源。',
        'Agent102RunDefs': '母代理定义，复核者未修改。',
        'Agent102AffineArithmetic': '其他子代理编写，复核者未修改。',
        'Agent102RunEndpoints': '母代理编写，本子代理独立复核且未修改。',
        'Agent102AffineRuns': '母代理编写，本子代理独立复核且未修改。',
    },
    'lean_version': version,
    'lean_executable_sha256': digest(lean),
    'trust': 0,
    'build_directory': str(build),
    'build_directory_initially_empty': True,
    'all_project_imports_rebuilt': True,
    'source_imports': source_imports,
    'source_sha256': source_shas,
    'source_unchanged_after_build': unchanged,
    'literal_declarations': decls,
    'theorem_count': len(theorems),
    'registry_named_endpoint_count': len(registered_claims),
    'source_theorems_omitted_from_registry_but_audited': omitted_from_registry,
    'all_literal_declarations_audited': len(audit_results) == len(decls),
    'allowed_axioms': sorted(allowed),
    'results': results,
    'files_sha256': sha,
}
(evidence / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(f'证据：{evidence}', flush=True)
sys.exit(results[-1]['returncode'])
