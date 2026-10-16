#!/usr/bin/env python3
"""Finish a fixture-only failed review without rebuilding unchanged project modules.

The first execution's complete successful project compilation is retained and
every inherited source, object and command is pinned in the continuation report.
Only corrected reviewer fixtures are compiled; the complete public/module-origin
axiom audit is then executed over the exact combined import closure.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import time

PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[3]
LEAN = Path('/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean')
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--from-attempt', type=Path, required=True)
    ap.add_argument('--fixture', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    prior = args.from_attempt.resolve()
    previous = json.loads((prior / 'verification.json').read_text())
    registry_path = PACKAGE / 'PROJECT_REGISTRY.json'
    registry = json.loads(registry_path.read_text())
    spec = registry['projects']['agent7-allbase-overflow-births']
    assert previous['status'] == 'FAIL'
    fixture = args.fixture.resolve()
    fixture_module = fixture.stem
    commands = {item['module']: item for item in previous['commands']}
    assert commands[fixture_module]['exit_code'] != 0
    assert set(previous['source_records']) == set(spec['modules']) | {fixture_module}
    assert all(commands[m]['exit_code'] == 0 for m in spec['modules'])
    assert previous['lean_sha256'] == sha(LEAN) == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
    version = subprocess.check_output([str(LEAN), '--version'], text=True).strip()
    assert version == previous['lean_version']
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = output / 'source'; source.mkdir()
    logs = output / 'logs'; logs.mkdir()
    records = {}
    project_order = [m for m in previous['build_order'] if m != fixture_module]
    for module in project_order:
        registered = spec['modules'][module]
        record = dict(previous['source_records'][module])
        original = REPO / registered['path']
        retained = prior / 'source' / (module + '.lean')
        obj = prior / 'source' / (module + '.olean')
        assert sha(original) == sha(retained) == registered['sha256'] == record['sha256']
        assert commands[module]['log_sha256'] == sha(prior / 'logs' / (module + '.log'))
        assert '--trust=0' in commands[module]['command']
        (source / retained.name).write_bytes(retained.read_bytes())
        (source / obj.name).write_bytes(obj.read_bytes())
        record['object_sha256'] = sha(obj)
        record['object_compiled_in'] = str(prior)
        records[module] = record
    reference = runpy.run_path(str(REPO / 'proofs/verify_project__214bf7673efe116b.py'), run_name='continuation_reference')
    code = reference['code_only'](fixture.read_text())
    assert not re.search(r'\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b', code)
    imports = [d for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for d in line.split()]
    assert imports == ['CanonicalOverflowBirths']
    spaces = re.findall(r'^namespace\s+(\S+)', code, re.M)
    assert spaces == ['P196.Agent7.AllBaseOverflow.Review']
    names = re.findall(r'^(?:@\[[^\n]*\]\s*)?(?:theorem|lemma)\s+([A-Za-z_][\w.]*)', code, re.M)
    data = fixture.read_bytes()
    records[fixture_module] = {
        'original': str(fixture), 'sha256': sha(fixture),
        'git_blob': hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest(),
        'imports': imports, 'public_theorems': [spaces[0] + '.' + name for name in names],
    }
    (source / fixture.name).write_bytes(data)
    order = project_order + [fixture_module]
    report = {
        'reviewer': 'Agent #7 /root/runtime',
        'status': 'RUNNING', 'started_at': datetime.now(timezone.utc).isoformat(),
        'kind': 'Continuation of a fixture-only failure after a complete fresh successful frozen-project compilation',
        'registry_sha256': sha(registry_path),
        'project_roots': spec['roots'], 'roots': [*spec['roots'], fixture_module],
        'source_records': records, 'build_order': order,
        'lean_version': version, 'lean_sha256': sha(LEAN),
        'inherited_project_compilation': {
            'attempt': str(prior), 'report_sha256': sha(prior / 'verification.json'),
            'original_overall_status': previous['status'],
            'reason_for_original_failure': 'Reviewer BoundaryContracts finite membership elimination; all 13 frozen project source modules exited zero.',
            'fresh_project_objects_in_prior_attempt': previous['fresh_project_objects'],
            'source_changes': False, 'modules': project_order,
            'commands': [commands[m] for m in project_order],
            'object_policy': 'Only the 13 successfully compiled project objects are copied; the failed reviewer fixture object is never copied or imported.',
        },
        'commands': [],
    }
    def save():
        (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    env = dict(os.environ); env['LEAN_PATH'] = str(source)
    def run(module, compile_object=True):
        cmd = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false']
        if compile_object:
            cmd += ['-o', module + '.olean']
        cmd += [module + '.lean']
        start = time.monotonic()
        with (logs / (module + '.log')).open('wb') as stream:
            result = subprocess.run(cmd, cwd=source, env=env, stdout=stream, stderr=subprocess.STDOUT)
        report['commands'].append({'module': module, 'command': cmd, 'cwd': str(source),
                                   'exit_code': result.returncode, 'elapsed_seconds': time.monotonic() - start,
                                   'log_sha256': sha(logs / (module + '.log'))})
        save(); print(module + ' exit=' + str(result.returncode), flush=True)
        if result.returncode:
            raise RuntimeError((logs / (module + '.log')).read_text())
    try:
        save()
        run(fixture_module)
        public = [name for module in order for name in records[module]['public_theorems']]
        assert len(public) == len(set(public))
        audit = '\n'.join('import ' + m for m in report['roots']) + '\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n'
        audit += '\n'.join('#print axioms ' + name for name in public) + '\n'
        audit += 'run_cmd do\n  let env ← getEnv\n  let selected : List String := ' + json.dumps(order) + '''
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          let axs ← liftCoreM (Lean.collectAxioms name)
          if axs.toList.any (fun a => !(allowed.contains a)) then throwError m!"DISALLOWED_AXIOMS {mod} {name}: {axs.toList}"
          count := count + 1
          logInfo m!"AUDIT_THEOREM {mod} {name}: {axs.toList}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count}"
'''
        (source / 'PublicAudit.lean').write_text(audit)
        run('PublicAudit', False)
        text = (logs / 'PublicAudit.log').read_text()
        printed = re.findall(r"^'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)$", text, re.M)
        assert len(printed) == len(public) and {n for n, _ in printed} == set(public)
        for name, axes in printed:
            assert set(re.split(r'\s*,\s*', axes.strip()) if axes.strip() else []) <= ALLOWED, name
        constants = re.findall(r'^AUDIT_THEOREM (\S+) (\S+): (.*)$', text, re.M)
        count = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+)$', text, re.M)
        assert len(count) == 1 and int(count[0]) == len(constants)
        assert len({name for _, name, _ in constants}) == len(constants)
        for module, record in records.items():
            assert sha(Path(record['original'])) == record['sha256']
            assert sha(source / (module + '.lean')) == record['sha256']
            obj_hash = sha(source / (module + '.olean'))
            if module != fixture_module:
                assert record['object_sha256'] == obj_hash
            record['object_sha256'] = obj_hash
        module_counts = {module: sum(m == module for m, _, _ in constants) for module in order}
        report.update(status='PASS', public_theorem_count=len(public),
                      project_public_theorem_count=sum(len(records[m]['public_theorems']) for m in project_order),
                      fixture_public_theorem_count=len(names), module_origin_theorem_count=len(constants),
                      module_origin_counts=module_counts,
                      project_module_origin_theorem_count=sum(module_counts[m] for m in project_order),
                      allowed_axioms=sorted(ALLOWED),
                      unsafe_implementation_axioms=re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', text, re.M))
    except Exception as exc:
        report['status'] = 'FAIL'; report['error'] = str(exc)
        print(str(exc), flush=True)
    report['finished_at'] = datetime.now(timezone.utc).isoformat(); save()
    raise SystemExit(0 if report['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
