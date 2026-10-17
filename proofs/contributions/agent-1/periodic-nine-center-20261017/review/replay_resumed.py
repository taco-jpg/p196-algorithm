#!/usr/bin/env python3
"""Independent fresh replay of the pinned periodic nine-center dependency closure."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import time

def lean_code_tokens(source):
    """Mask nested Lean comments and string contents before the auxiliary scan."""
    out, i, depth = [], 0, 0
    while i < len(source):
        if depth:
            if source.startswith('/-', i):
                depth += 1
                out.extend('  ')
                i += 2
            elif source.startswith('-/', i):
                depth -= 1
                out.extend('  ')
                i += 2
            else:
                out.append('\n' if source[i] == '\n' else ' ')
                i += 1
        elif source.startswith('/-', i):
            depth = 1
            out.extend('  ')
            i += 2
        elif source.startswith('--', i):
            j = source.find('\n', i)
            j = len(source) if j == -1 else j
            out.extend(' ' * (j - i))
            i = j
        elif source[i] == '"':
            out.append(' ')
            i += 1
            while i < len(source):
                ch = source[i]
                out.append('\n' if ch == '\n' else ' ')
                i += 1
                if ch == '\\' and i < len(source):
                    out.append('\n' if source[i] == '\n' else ' ')
                    i += 1
                elif ch == '"':
                    break
            else:
                raise AssertionError('Unterminated Lean string in source scan')
        else:
            out.append(source[i])
            i += 1
    assert depth == 0, 'Unterminated Lean block comment in source scan'
    return ''.join(out)


p = argparse.ArgumentParser()
p.add_argument('--source-root', type=Path, required=True)
p.add_argument('--build-dir', type=Path, required=True)
p.add_argument('--evidence-dir', type=Path, required=True)
p.add_argument('--lean', type=Path, required=True)
p.add_argument('--memory-mib', type=int, default=8192)
p.add_argument('--module-timeout-seconds', type=int, default=600)
p.add_argument('--stack-kib', type=int, default=0)
a = p.parse_args()
root, build, evidence = a.source_root.resolve(), a.build_dir.resolve(), a.evidence_dir.resolve()
build.mkdir(parents=True, exist_ok=False)
evidence.mkdir(parents=True, exist_ok=False)
review = Path(__file__).resolve().parent
identity = json.loads((review / 'resumed-source-identity.json').read_text())
manifest = identity['sources']
assert identity['roots'] == ['Agent1PeriodicNinesCenter']
assert identity['source_commit'] and identity['source_paths_match_published_commit']
sha = lambda x: hashlib.sha256(x).hexdigest()
(evidence / 'compiled-sources').mkdir()
(evidence / 'replay.py').write_bytes(Path(__file__).read_bytes())
(evidence / 'final-source-identity.json').write_bytes((review / 'resumed-source-identity.json').read_bytes())
for entry in manifest:
    data = (root / entry['path']).read_bytes()
    assert sha(data) == entry['sha256'], entry['path']
    assert data == subprocess.check_output(['git', 'show', identity['source_commit'] + ':' + entry['path']], cwd=root), entry['path']
    (build / (entry['module'] + '.lean')).write_bytes(data)
    (evidence / 'compiled-sources' / (entry['module'] + '.lean')).write_bytes(data)
    if entry['module'].startswith('Agent1'):
        (evidence / (entry['module'] + '.lean')).write_bytes(data)
(evidence / 'sources.json').write_text(json.dumps(manifest, indent=2) + '\n')
compiler = {'path': str(a.lean), 'sha256': sha(a.lean.read_bytes()),
            'version': subprocess.check_output([str(a.lean), '--version'], text=True).strip()}
assert 'version 4.19.0' in compiler['version'], compiler
assert compiler['sha256'] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023', compiler
(evidence / 'compiler.json').write_text(json.dumps(compiler, indent=2) + '\n')
env = dict(os.environ, LEAN_PATH=str(build))
assert a.memory_mib > 0 and a.module_timeout_seconds > 0 and a.stack_kib >= 0
resource_limits = {'address_space_mib_per_child': a.memory_mib,
                   'timeout_seconds_per_command': a.module_timeout_seconds,
                   'lean_stack_kib': a.stack_kib or 'compiler default'}
(evidence / 'resource-limits.json').write_text(json.dumps(resource_limits, indent=2) + '\n')
results = []

def limit_child():
    cap = a.memory_mib * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))

def run(module, output=True):
    cmd = [str(a.lean), '--trust=0', '-j1', '-DElab.async=false']
    if a.stack_kib:
        cmd += ['-s', str(a.stack_kib)]
    if output:
        cmd += ['-o', module + '.olean']
    cmd += [module + '.lean']
    started = time.monotonic()
    timed_out = False
    try:
        proc = subprocess.run(cmd, cwd=build, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, preexec_fn=limit_child,
                              timeout=a.module_timeout_seconds)
        output_bytes, code = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        output_bytes = (exc.stdout or b'') + b'\nREVIEW_COMMAND_TIMEOUT\n'
        code = 124
    (evidence / (module + '.log')).write_bytes(output_bytes)
    results.append({'module': module, 'command': cmd, 'exit_code': code,
                    'timed_out': timed_out, 'resource_limits': resource_limits,
                    'seconds': time.monotonic() - started, 'log_sha256': sha(output_bytes)})
    (evidence / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(module + ': exit ' + str(code), flush=True)
    if code:
        print('Failed command output retained at ' + str(evidence / (module + '.log')), flush=True)
        raise SystemExit(code)

for entry in manifest:
    run(entry['module'])

selected = ', '.join(json.dumps(e['module']) for e in manifest)
audit = '''import Agent1PeriodicNinesCenter
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := [SELECTED]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut defs := 0
  let mut union : List Name := []
  let mut defUnion : List Name := []
  let mut seen : List String := []
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
          if !(seen.contains mod.toString) then seen := mod.toString :: seen
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | .defnInfo v =>
          if v.safety != .safe then
            logInfo m!"NONSAFE_DEFINITION {mod} {name}"
          else
            defs := defs + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            for ax in axl do
              if !(defUnion.contains ax) then defUnion := ax :: defUnion
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_DEFINITION_AXIOMS {mod} {name} : {axl}"
            logInfo m!"AUDIT_SAFE_DEFINITION {mod} {name} : {axl}"
        | .opaqueInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_OPAQUE {mod} {name}"
          else
            defs := defs + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            for ax in axl do
              if !(defUnion.contains ax) then defUnion := ax :: defUnion
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_OPAQUE_AXIOMS {mod} {name} : {axl}"
            logInfo m!"AUDIT_SAFE_OPAQUE {mod} {name} : {axl}"
        | _ => pure ()
  for mod in selected do
    if !(seen.contains mod) then throwError m!"MODULE_NOT_AUDITED {mod}"
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
  logInfo m!"FULL_DEFINITION_AUDIT definitions={defs} union={defUnion}"
'''.replace('SELECTED', selected)
for entry in manifest:
    if not entry['module'].startswith('Agent1'):
        continue
    ns = ('Agent1.Periodic.SafetyBoundary' if entry['module'] == 'Agent1PeriodicSafetyBoundary'
          else 'Agent1.Periodic' if entry['module'].startswith('Agent1Periodic')
          else 'Agent1.RepeatedBlock')
    src = (build / (entry['module'] + '.lean')).read_text()
    for name in re.findall(r'^theorem\s+(\w+)', lean_code_tokens(src), re.M):
        audit += '\n#check ' + ns + '.' + name + '\n'

root_public_definitions = []
new_modules = identity['new_modules']
for module in new_modules:
    source = (build / (module + '.lean')).read_text()
    root_public_definitions += ['Agent1.Periodic.' + name for name in re.findall(r'^(?:noncomputable\s+)?(?:def|abbrev|structure|inductive)\s+(\w+)', lean_code_tokens(source), re.M)]
for name in root_public_definitions:
    audit += '\n#check ' + name + '\n#print axioms ' + name + '\n'
for name in identity['new_module_theorems']:
    audit += '\n#print axioms ' + name + '\n'

(build / 'ReviewAudit.lean').write_text(audit)
(evidence / 'ReviewAudit.lean').write_text(audit)
run('ReviewAudit', output=False)

# BEGIN POSTCHECK

exports = []
for entry in manifest:
    if not entry['module'].startswith('Agent1'):
        continue
    source = (build / (entry['module'] + '.lean')).read_text()
    forbidden = re.findall(r'\b(?:sorry|admit|native_decide|sorryAx|axiom)\b|Lean\.ofReduceBool', lean_code_tokens(source))
    assert not forbidden, (entry['module'], forbidden)
    log = (evidence / (entry['module'] + '.log')).read_text()
    namespace = ('Agent1.Periodic.SafetyBoundary' if entry['module'] == 'Agent1PeriodicSafetyBoundary' else 'Agent1.Periodic' if entry['module'].startswith('Agent1Periodic') else 'Agent1.RepeatedBlock')
    for name in re.findall(r'^theorem\s+(\w+)', lean_code_tokens(source), re.M):
        full = namespace + '.' + name
        assert ("'" + full + "' depends on axioms:") in log or ("'" + full + "' does not depend on any axioms") in log, full
        exports.append(full)
    assert not re.search(r'sorryAx|Lean\.ofReduceBool', log), entry['module']
audit_log = (evidence / 'ReviewAudit.log').read_text()
match = re.search(r'FULL_MODULE_AUDIT theorems=(\d+) union=\[([^\]]*)\]', audit_log)
assert match, 'Missing complete audit summary'
definition_match = re.search(r'FULL_DEFINITION_AUDIT definitions=(\d+) union=\[([^\]]*)\]', audit_log)
assert definition_match, 'Missing safe definition audit summary'
for entry in manifest:
    assert sha((root / entry['path']).read_bytes()) == entry['sha256'], 'Source changed during build: ' + entry['path']
summary = {'status': 'PASS', 'reviewer': 'Agent #1 specialist center_review_resume',
           'source_modules': len(manifest), 'trust': 0, 'compiler': compiler,
           'new_public_definitions_type_checked': root_public_definitions,
           'theorems_audited': int(match.group(1)), 'axiom_union': match.group(2).split(', '),
           'safe_definitions_audited': int(definition_match.group(1)),
           'safe_definition_axiom_union': definition_match.group(2).split(', '),
           'nonsafe_definitions_inventoried': re.findall(r'NONSAFE_DEFINITION (\S+) (\S+)', audit_log),
           'unsafe_opaques_inventoried': re.findall(r'UNSAFE_OPAQUE (\S+) (\S+)', audit_log),
           'unsafe_implementation_axioms_inventoried': re.findall(r'UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)', audit_log),
           'audited_named_exports': exports, 'periodic_exports': [x for x in exports if x.startswith('Agent1.Periodic.')], 'sources_unchanged_at_finish': True,
           'source_commit': identity['source_commit'], 'scope': 'Independent fresh periodic nine-center closure replay. Current reviewer authored none of the new or dependency math modules. Earlier preparer symbolic_scope disclosed prior frozen dependency authorship; preparation is preserved and execution is newly performed.'}
safe_names = set(re.findall(r'AUDIT_SAFE_DEFINITION (\S+) (\S+)', audit_log))
cstages, unsafe_rec, unknown = [], [], []
for mod, name in summary['nonsafe_definitions_inventoried']:
    if re.search(r'\._cstage[12](?:\.|$)', name):
        cstages.append([mod, name])
    elif name.endswith('._unsafe_rec'):
        base = name[:-len('._unsafe_rec')]
        unsafe_rec.append({'module': mod, 'implementation': name, 'safe_base': base,
                           'safe_base_audited': (mod, base) in safe_names})
    else:
        unknown.append([mod, name])
inventory = {'status': 'PASS' if not unknown and all(x['safe_base_audited'] for x in unsafe_rec) and not summary['unsafe_opaques_inventoried'] else 'REVIEW_REQUIRED',
             'nonsafe_count': len(summary['nonsafe_definitions_inventoried']),
             'cstage_helpers': len(cstages), 'unsafe_rec_helpers': len(unsafe_rec),
             'unsafe_rec_base_checks': unsafe_rec, 'unclassified_nonsafe': unknown,
             'unsafe_axioms': summary['unsafe_implementation_axioms_inventoried'],
             'unsafe_opaques': summary['unsafe_opaques_inventoried'],
             'meaning': 'Implementation inventory is separate from checked theorem/safe-definition dependencies.'}
(evidence / 'implementation-inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
assert inventory['status'] == 'PASS', inventory
(evidence / 'verification.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k not in ['nonsafe_definitions_inventoried', 'audited_named_exports', 'periodic_exports']}, indent=2), flush=True)

