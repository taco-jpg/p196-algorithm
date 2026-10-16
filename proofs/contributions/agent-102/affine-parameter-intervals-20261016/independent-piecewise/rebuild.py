#!/usr/bin/env python3
"""Reviewer-owned clean build. Explicit frozen root and compact hashes are required."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_theorems(text):
    scope, names = [], []
    for raw in text.splitlines():
        line = raw.strip()
        match = re.fullmatch(r'namespace\s+(\S+)', line)
        if match:
            scope.append(('namespace', match.group(1)))
            continue
        if re.fullmatch(r'section(?:\s+\S+)?', line):
            scope.append(('section', ''))
            continue
        if re.fullmatch(r'end(?:\s+\S+)?', line):
            if scope:
                scope.pop()
            continue
        match = re.match(r'^(?:@\[[^\]]*\]\s*)?(?:protected\s+)?theorem\s+([^\s(:]+)', line)
        if match:
            names.append('.'.join([name for kind, name in scope if kind == 'namespace'] + [match.group(1)]))
    return names


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--proofs', type=Path, required=True)
    parser.add_argument('--root-sha', required=True)
    parser.add_argument('--compact-sha', required=True)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    proofs, output, lean = args.proofs.resolve(), args.output.resolve(), args.lean.resolve()
    if output.exists():
        parser.error('a new output directory is required')
    expected = {
        'Agent102RunDefs': '1544d22e098c659f804e27faab228f4ebb13c8f9d8fc290c6d90f413286cefcf',
        'Agent102ParameterIntervalDefs': 'c06e197c31e902f19345d3e6b390621021f1326d56e7af532302cfae3491949d',
        'Agent102AffineInequalityIntervals': '21def6712029812bc607e5c3c64550ad111ec146da499405b652e26206e86d04',
        'Agent102ParameterIntervalAlgebra': 'd10cb78bc87e8aff81f24358e0d52fd9592c1dce55d9dc507417835cd7e9a65a',
        'Agent102AffineArithmetic': 'a36d4a0e572ab083cb8408ee71a5d2281bc838df508ce184e6a313a23b9a3df2',
        'Agent102ParameterIntervalCompact': args.compact_sha,
        'Agent102PiecewiseCounts': args.root_sha,
    }
    order, snapshots = [], {}

    def visit(module):
        if module in snapshots:
            return
        if module not in expected:
            raise RuntimeError('unexpected project dependency: ' + module)
        path = proofs / (module + '.lean')
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected[module], module
        snapshots[module] = data
        for dep in re.findall(r'^import\s+(\S+)\s*$', data.decode(), re.M):
            if dep.startswith('Agent102'):
                visit(dep)
        order.append(module)

    visit('Agent102PiecewiseCounts')
    assert set(order) == set(expected)
    output.mkdir(parents=True)
    source, build, logs = output / 'source', output / 'build', output / 'logs'
    source.mkdir(); build.mkdir(); logs.mkdir()
    for module in order:
        (source / (module + '.lean')).write_bytes(snapshots[module])
    controls = Path(__file__).resolve().parent / 'ReviewerControls.lean'
    shutil.copy2(controls, source / controls.name)
    entries = []
    for module in order + ['ReviewerControls']:
        entries.extend({'module': module, 'name': name} for name in public_theorems((source / (module + '.lean')).read_text()))
    (source / 'LiteralAudit.lean').write_text('import ReviewerControls\n\n' + '\n'.join('#print axioms ' + item['name'] for item in entries) + '\n')
    selected = '[' + ', '.join('"' + module + '"' for module in order + ['ReviewerControls']) + ']'
    (source / 'ModuleOriginAudit.lean').write_text('''import ReviewerControls
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ''' + selected + '''
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
    (source / 'ExecutableDependencyAudit.lean').write_text('''import ReviewerControls
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ''' + selected + '''
  let forbidden : List Name := [``List.range, ``List.replicate,
    ``Agent102.word, ``Agent102.wordAt, ``Agent102.ParameterSets.CountExpr.value]
  for root in [``Agent102.ParameterSets.CountExpr.pieces,
      ``Agent102.ParameterSets.comparisonRegion, ``Agent102.ParameterSets.ltRegion,
      ``Agent102.ParameterSets.leRegion, ``Agent102.ParameterSets.eqRegion] do
    let mut pending : List Name := [root]
    let mut seen : List Name := []
    let mut count := 0
    while !pending.isEmpty do
      let name := pending.head!
      pending := pending.tail!
      if seen.contains name then continue
      seen := name :: seen
      if forbidden.contains name then throwError m!"FORBIDDEN_EXECUTABLE_DEP {root} {name}"
      if let some info := env.find? name then
        if let some idx := env.getModuleIdxFor? name then
          let mod := env.allImportedModuleNames[idx.toNat]!
          if selected.contains mod.toString then
            count := count + 1
            logInfo m!"EXECUTABLE_PROJECT_DEP {root} {mod} {name}"
            for dep in info.type.getUsedConstants do pending := dep :: pending
            if let some value := info.value? true then
              for dep in value.getUsedConstants do pending := dep :: pending
    logInfo m!"EXECUTABLE_DEPENDENCY_CHECK {root} project_constants={count} forbidden=0"
''')
    order += ['ReviewerControls', 'LiteralAudit', 'ModuleOriginAudit', 'ExecutableDependencyAudit']
    for module in order:
        shutil.copy2(source / (module + '.lean'), build / (module + '.lean'))
    pins = {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(source.iterdir())}
    (output / 'SOURCE_PINS.json').write_text(json.dumps(pins, indent=2) + '\n')
    (output / 'EXPLICIT_THEOREMS.json').write_text(json.dumps(entries, indent=2) + '\n')
    env = os.environ.copy(); env['LEAN_PATH'] = '.'
    version = subprocess.run([str(lean), '--version'], capture_output=True, text=True, timeout=15, check=True).stdout.strip()
    assert 'version 4.19.0' in version and '6caaee842e94' in version
    (output / 'ENVIRONMENT.json').write_text(json.dumps({'lean': str(lean), 'version': version,
        'lean_sha256': sha(lean), 'LEAN_PATH': '.', 'preexisting_project_olean_used': False,
        'kind': 'independent clean root PiecewiseCounts review; reviewer authored scalar and arithmetic dependencies'}, indent=2) + '\n')
    results = []
    for module in order:
        command = [str(lean), '--trust=0', '-j1', '-DElab.async=false', '-o', module + '.olean', module + '.lean']
        started = time.monotonic()
        with (logs / (module + '.log')).open('w') as log:
            try:
                result = subprocess.run(command, cwd=build, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=90)
                code = result.returncode
            except subprocess.TimeoutExpired:
                log.write('\nREVIEW_TIMEOUT_90_SECONDS\n'); code = 124
        row = {'module': module, 'argv': command, 'cwd': str(build), 'LEAN_PATH': '.',
               'returncode': code, 'seconds': round(time.monotonic() - started, 3)}
        results.append(row)
        (output / 'verification.json').write_text(json.dumps(results, indent=2) + '\n')
        print(json.dumps(row), flush=True)
        if code:
            print((logs / (module + '.log')).read_text(), flush=True)
            return code
    return 0


if __name__ == '__main__':
    sys.exit(main())
