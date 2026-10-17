#!/usr/bin/env python3
"""Actual author compile/audit of Agent107DFAChecker, retaining every attempt."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

REPO = Path('/workspace/scratch/94808c4aecb2/p196-agent107-horn')
LEAN = Path('/workspace/scratch/94808c4aecb2/agent107-runtime/lean-4.19.0-linux/bin/lean')
BUILD = Path('/tmp/agent107-runtime/task2-checker-build')
DEPENDENCIES = [Path('/workspace/scratch/94808c4aecb2/agent107-horn-build'), Path('/workspace/scratch/94808c4aecb2/agent107-runtime/reviewer-empty-_z2f9ejb'), Path('/workspace/scratch/94808c4aecb2/agent107-runtime/baseline')]
EXPECTED_DFA_SHA = 'd0fe8accc9d80110230ea3b4061f554d8d9d9dc5b8ea1a89f44e7d2fc977969e'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    attempt = int(sys.argv[1])
    out = Path(__file__).parent / f'checker-{attempt:03d}'
    out.mkdir(parents=True, exist_ok=False)
    BUILD.mkdir(parents=True, exist_ok=True)
    data = (REPO / 'proofs/Agent107DFAChecker.lean').read_bytes()
    defs = (REPO / 'proofs/Agent107DFA.lean').read_bytes()
    assert digest(defs) == EXPECTED_DFA_SHA
    for target in [out, BUILD]:
        (target / 'Agent107DFAChecker.lean').write_bytes(data)
    (out / 'Agent107DFA.lean').write_bytes(defs)
    env = os.environ.copy()
    env['LEAN_PATH'] = ':'.join(str(p) for p in [BUILD, *DEPENDENCIES])
    record = {
        'executor': 'Agent #107 lean_runtime checker author (not root; not independent checker review)',
        'started_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
        'source': 'proofs/Agent107DFAChecker.lean',
        'source_sha256': digest(data),
        'source_git_blob': hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest(),
        'source_snapshot_policy': 'Exact source bytes copied before actual compilation; every attempt kept in a fresh directory.',
        'dependency_DFA_source_sha256': digest(defs),
        'dependency_objects': {str(p): digest(p.read_bytes()) for folder in DEPENDENCIES for p in sorted(folder.glob('*.olean'))},
        'dependency_note': 'DFA object reused from root explicit trust-zero author build; task-1 closure objects reused from semantic_review explicit trust-zero clean build and lean_runtime explicit trust-zero foundation build. This is author verification, not an independent review.',
        'lean_path': env['LEAN_PATH'],
        'lean_sha256': digest(LEAN.read_bytes()),
        'commands': [],
        'status': 'RUNNING',
    }
    def save():
        (out / 'execution.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    def run(label, argv):
        start = time.monotonic()
        with (out / f'{label}.stdout.log').open('wb') as stdout, (out / f'{label}.stderr.log').open('wb') as stderr:
            rc = subprocess.run(argv, cwd=BUILD, env=env, stdout=stdout, stderr=stderr).returncode
        record['commands'].append({'label': label, 'argv': argv, 'cwd': str(BUILD), 'exit_code': rc, 'seconds': round(time.monotonic() - start, 6), 'stdout_sha256': digest((out / f'{label}.stdout.log').read_bytes()), 'stderr_sha256': digest((out / f'{label}.stderr.log').read_bytes())})
        save()
        print(label, 'exit', rc, flush=True)
        return rc
    save()
    command = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false', '-o', 'Agent107DFAChecker.olean', 'Agent107DFAChecker.lean']
    rc = run('compiler', command)
    if rc == 0:
        audit = '''import Agent107DFAChecker
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "Agent107DFAChecker" then
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
          if axl.any (fun ax => !([``propext, ``Classical.choice, ``Quot.sound].contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
'''
        for target in [out, BUILD]:
            (target / 'CheckerModuleOriginAudit.lean').write_text(audit)
        rc = run('audit', [str(LEAN), '--trust=0', '-j1', '-DElab.async=false', 'CheckerModuleOriginAudit.lean'])
        record['olean_sha256'] = digest((BUILD / 'Agent107DFAChecker.olean').read_bytes())
    record.update({'status': 'PASS' if rc == 0 else 'FAIL', 'exit_code': rc, 'finished_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
    assert (REPO / 'proofs/Agent107DFAChecker.lean').read_bytes() == data
    save()
    print(json.dumps({'attempt': attempt, 'status': record['status'], 'source_sha256': record['source_sha256'], 'evidence': str(out)}, ensure_ascii=False), flush=True)
    return rc

if __name__ == '__main__':
    sys.exit(main())
