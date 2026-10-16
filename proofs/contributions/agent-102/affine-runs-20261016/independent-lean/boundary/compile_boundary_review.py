"""边界模块的独立空构建、逐字审计和完整来源模块审计。"""
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
names = ['Agent102RunDefs', 'Agent102RunWord',
         'Agent102AffineArithmetic', 'Agent102AffineBoundary']
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
previous = json.loads((work / 'full-review-001/manifest.json').read_text())['source_sha256']
declarations = []
theorems = []
source_shas = {}
source_imports = {}
for name in names:
    source = repo / f'{name}.lean'
    target = evidence / source.name
    shutil.copyfile(source, target)
    source_shas[name] = digest(target)
    if name in previous:
        assert source_shas[name] == previous[name], name
    text = target.read_text()
    source_imports[name] = re.findall(r'^import\s+(\S+)', text, re.M)
    assert all(dep in names or dep == 'Std' for dep in source_imports[name])
    for bad in (r'\bsorry\b', r'\badmit\b', r'\bnative_decide\b', r'^\s*axiom\s'):
        assert not re.search(bad, text, re.M), (name, bad)
    stack = []
    for line in text.splitlines():
        if match := re.match(r'^namespace\s+(\S+)', line):
            stack.append(match.group(1))
        elif re.match(r'^end(?:\s+\S+)?\s*$', line):
            assert stack, (name, line)
            stack.pop()
        elif match := re.match(r'^(?:@\[[^\n]*\]\s*)?(theorem|def|structure)\s+([^\s(:]+)', line):
            full = '.'.join(stack + [match.group(2)])
            declarations.append({'name': full, 'kind': match.group(1), 'module': name})
            if match.group(1) == 'theorem':
                theorems.append(full)
    assert not stack, name
assert len(set(item['name'] for item in declarations)) == len(declarations)
boundary = [item for item in declarations if item['module'] == 'Agent102AffineBoundary']
assert sum(item['kind'] == 'theorem' for item in boundary) == 12
assert len(boundary) == 23
literal = evidence / 'BoundaryLiteralAudit.lean'
literal.write_text('import Agent102AffineBoundary\n\n'
    '/- 独立从冻结闭包源枚举全部显式声明，逐字保留名称。 -/\n'
    + ''.join(f'#print axioms {item["name"]}\n' for item in declarations))
origin = evidence / 'BoundaryOriginAudit.lean'
origin.write_text('import Agent102AffineBoundary\nimport Lean\n'
    'open Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n'
    '/- 审计主体沿用仓库原验证器的来源模块枚举与公理限制；未修改原验证器。 -/\n'
    + '\n'.join('#check ' + name for name in theorems) + '\n'
    + 'run_cmd do\n  let env ← getEnv\n  let selected : List String := '
    + json.dumps(names) + '''
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
''')
shutil.copyfile(Path(__file__), evidence / 'compile_boundary_review.py')
lean = base / 'agent102-runtime/lean-4.19.0-linux/bin/lean'
env = os.environ.copy()
env['LEAN_PATH'] = str(build)
version = subprocess.run([str(lean), '--version'], text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout.strip()
results = []
for name in names + ['BoundaryLiteralAudit', 'BoundaryOriginAudit']:
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
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
literal_results = {}
origin_results = []
origin_union = None
unsafe_implementation_axioms = []
if results[-1]['returncode'] == 0 and results[-1]['name'] == 'BoundaryOriginAudit':
    for line in (evidence / 'BoundaryLiteralAudit.log').read_text().splitlines():
        if match := re.fullmatch(r"'([^']+)' does not depend on any axioms", line):
            literal_results[match.group(1)] = []
        elif match := re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line):
            axioms = match.group(2).split(', ') if match.group(2) else []
            assert set(axioms) <= allowed, (match.group(1), axioms)
            literal_results[match.group(1)] = axioms
    assert set(literal_results) == {item['name'] for item in declarations}
    log = (evidence / 'BoundaryOriginAudit.log').read_text()
    summaries = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]*)$', log, re.M)
    origin_results = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : (.*)$', log, re.M)
    assert len(summaries) == 1
    assert int(summaries[0][0]) == len(origin_results)
    assert len({item[1] for item in origin_results}) == len(origin_results)
    assert set(theorems) <= {item[1] for item in origin_results}
    assert {item[0] for item in origin_results} <= set(names)
    origin_union = summaries[0][1]
    unsafe_implementation_axioms = re.findall(
        r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', log, re.M)
    print(f'逐字审计：{len(theorems)} 条显式定理，{len(declarations)} 个显式声明。', flush=True)
    print(f'完整来源审计：{len(origin_results)} 条定理；公理并集 {origin_union}。', flush=True)
    print(f'编译器 unsafe 实现声明：{len(unsafe_implementation_axioms)}。', flush=True)
unchanged = {name: digest(repo / f'{name}.lean') == source_shas[name] for name in names}
assert all(unchanged.values()), unchanged
(evidence / 'literal-results.json').write_text(json.dumps(literal_results, indent=2) + '\n')
(evidence / 'origin-results.json').write_text(json.dumps(origin_results, indent=2) + '\n')
sha = {path.name: digest(path) for path in sorted(evidence.iterdir()) if path.is_file()}
(evidence / 'SHA256SUMS').write_text(''.join(f'{value}  {name}\n' for name, value in sha.items()))
manifest = {
    'reviewer': '/root/word_intervals, Agent #102 的真实子代理',
    'boundary_author': '/root/lean_runtime',
    'role_boundaries': {
        'Agent102RunWord': '本子代理是作者，依赖重建为作者验证。',
        'Agent102RunDefs': '母代理定义，本子代理未修改。',
        'Agent102AffineArithmetic': '其他子代理编写，本子代理未修改。',
        'Agent102AffineBoundary': 'lean_runtime 编写，本子代理只读独立复核。',
    },
    'lean_version': version,
    'lean_executable_sha256': digest(lean),
    'trust': 0,
    'build_directory': str(build),
    'build_directory_initially_empty': True,
    'source_imports': source_imports,
    'source_sha256': source_shas,
    'source_unchanged_after_build': unchanged,
    'literal_declarations': declarations,
    'boundary_explicit_theorem_count': 12,
    'boundary_explicit_declaration_count': 23,
    'closure_explicit_theorem_count': len(theorems),
    'closure_explicit_declaration_count': len(declarations),
    'module_origin_theorem_count': len(origin_results),
    'module_origin_axiom_union': origin_union,
    'unsafe_implementation_axioms': unsafe_implementation_axioms,
    'all_explicit_theorems_covered_by_origin_audit':
        set(theorems) <= {item[1] for item in origin_results},
    'allowed_axioms': sorted(allowed),
    'results': results,
    'files_sha256': sha,
}
(evidence / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(f'证据：{evidence}', flush=True)
print(f'边界源码 SHA256：{source_shas["Agent102AffineBoundary"]}', flush=True)
sys.exit(results[-1]['returncode'])
