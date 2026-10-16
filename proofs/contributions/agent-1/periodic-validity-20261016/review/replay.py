#!/usr/bin/env python3
"""Independent clean replay of seventeen pinned periodic validity modules."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--source-root', type=Path, required=True)
p.add_argument('--build-dir', type=Path, required=True)
p.add_argument('--evidence-dir', type=Path, required=True)
p.add_argument('--lean', type=Path, required=True)
a = p.parse_args()
root, build, evidence = a.source_root.resolve(), a.build_dir.resolve(), a.evidence_dir.resolve()
build.mkdir(parents=True, exist_ok=False)
evidence.mkdir(parents=True, exist_ok=False)
review = Path(__file__).resolve().parent
manifest = json.loads((review / 'final-source-identity.json').read_text())['sources']
sha = lambda x: hashlib.sha256(x).hexdigest()
for entry in manifest:
    data = (root / entry['path']).read_bytes()
    assert sha(data) == entry['sha256'], entry['path']
    (build / (entry['module'] + '.lean')).write_bytes(data)
    if entry['module'].startswith('Agent1'):
        (evidence / (entry['module'] + '.lean')).write_bytes(data)
(evidence / 'sources.json').write_text(json.dumps(manifest, indent=2) + '\n')
compiler = {'path': str(a.lean), 'sha256': sha(a.lean.read_bytes()),
            'version': subprocess.check_output([str(a.lean), '--version'], text=True).strip()}
assert 'version 4.19.0' in compiler['version'], compiler
assert compiler['sha256'] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023', compiler
(evidence / 'compiler.json').write_text(json.dumps(compiler, indent=2) + '\n')
env = dict(os.environ, LEAN_PATH=str(build))
results = []

def run(module, output=True):
    cmd = [str(a.lean), '--trust=0', '-j1', '-DElab.async=false']
    if output:
        cmd += ['-o', module + '.olean']
    cmd += [module + '.lean']
    started = time.monotonic()
    proc = subprocess.run(cmd, cwd=build, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (evidence / (module + '.log')).write_bytes(proc.stdout)
    results.append({'module': module, 'command': cmd, 'exit_code': proc.returncode,
                    'seconds': time.monotonic() - started, 'log_sha256': sha(proc.stdout)})
    (evidence / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(module + ': exit ' + str(proc.returncode), flush=True)
    if proc.returncode:
        print(proc.stdout.decode(), flush=True)
        raise SystemExit(proc.returncode)

for entry in manifest:
    run(entry['module'])

selected = ', '.join(json.dumps(e['module']) for e in manifest)
audit = '''import Agent1PeriodicValidity
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := [SELECTED]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
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
        | _ => pure ()
  for mod in selected do
    if !(seen.contains mod) then throwError m!"MODULE_NOT_AUDITED {mod}"
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
'''.replace('SELECTED', selected)
(build / 'ReviewAudit.lean').write_text(audit)
(evidence / 'ReviewAudit.lean').write_text(audit)
run('ReviewAudit', output=False)

exports = []
for entry in manifest:
    if not entry['module'].startswith('Agent1'):
        continue
    source = (build / (entry['module'] + '.lean')).read_text()
    forbidden = re.findall(r'\b(?:sorry|admit|native_decide|sorryAx|axiom)\b|Lean\.ofReduceBool', source)
    assert not forbidden, (entry['module'], forbidden)
    log = (evidence / (entry['module'] + '.log')).read_text()
    namespace = 'Agent1.Periodic' if entry['module'].startswith('Agent1Periodic') else 'Agent1.RepeatedBlock'
    for name in re.findall(r'^theorem\s+(\w+)', source, re.M):
        full = namespace + '.' + name
        assert ("'" + full + "' depends on axioms:") in log or ("'" + full + "' does not depend on any axioms") in log, full
        exports.append(full)
    assert not re.search(r'sorryAx|Lean\.ofReduceBool', log), entry['module']
audit_log = (evidence / 'ReviewAudit.log').read_text()
match = re.search(r'FULL_MODULE_AUDIT theorems=(\d+) union=\[([^\]]*)\]', audit_log)
assert match, 'Missing complete audit summary'
for entry in manifest:
    assert sha((root / entry['path']).read_bytes()) == entry['sha256'], 'Source changed during build: ' + entry['path']
summary = {'status': 'PASS', 'reviewer': 'Agent #1 specialist research_status',
           'source_modules': len(manifest), 'trust': 0, 'compiler': compiler,
           'theorems_audited': int(match.group(1)), 'axiom_union': match.group(2).split(', '),
           'audited_named_exports': exports, 'periodic_exports': [x for x in exports if x.startswith('Agent1.Periodic.')], 'sources_unchanged_at_finish': True,
           'scope': 'Independent fresh seventeen-module replay and source review; reviewer authored no validity mathematical module.'}
(evidence / 'verification.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2), flush=True)
