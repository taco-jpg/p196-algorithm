#!/usr/bin/env python3
"""Agent #1 independent post-merge verifier for the thirteen-prefix scope.

Builds unchanged author source with the documented resource settings, then
independently audits every theorem constant in the full twenty-module closure.
No project objects are reused. Finite literal-integer controls are supplementary.
This is not the repository-wide accepted build or a Lychrel-existence proof.
"""
from __future__ import annotations
import argparse
import collections
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import traceback

PIN = '6d56f543933dedb83eee8215f0e7295a5363c02c'
MODULES = ['LychrelDigitSums', 'PalindromeBridge', 'TwoDigitProjection',
           'TwoDigitGrowth', 'TwoDigitNumeric', 'TwoDigitCertificate',
           'TwoDigitCert10', 'TwoDigitCert20', 'TwoDigitCert32', 'TwoDigitCert40',
           'TwoDigitCert41', 'TwoDigitCert60', 'TwoDigitCert64', 'TwoDigitCert65',
           'TwoDigitCert76', 'TwoDigitCert80', 'TwoDigitCert81', 'TwoDigitCert82',
           'TwoDigitCert83', 'TwoDigitMain']
WITNESSES = [(10,100,1,1),(20,1005000,2,5),(32,12090,2,3),(40,1008000,3,5),
             (41,1008400,3,5),(60,1103090,3,5),(64,1203090,3,5),(65,1203290,6,6),
             (76,17590,3,3),(80,1009000,4,5),(81,1009200,4,5),(82,1006500,4,5),
             (83,1009400,4,5)]

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def audit_source() -> str:
    return ('import TwoDigitMain\nimport Lean\nopen Lean Elab Command\n'
            'set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n'
            'run_cmd do\n  let env ← getEnv\n  let selected : List String := '
            + json.dumps(MODULES) + '''
  let mut count := 0
  let mut union : List Name := []
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
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

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo, lean, out = args.repo.resolve(), args.lean.resolve(), args.output.resolve()
    if out.exists():
        raise RuntimeError('Output directory must not exist')
    out.mkdir(parents=True)
    work = out / 'temporary-build'
    wrappers = out / 'temporary-bin'
    wrappers.mkdir()
    (wrappers / 'lean').write_text('#!/bin/sh\nexec ' + str(lean) + ' -j1 -DElab.async=false "$@"\n')
    (wrappers / 'lean').chmod(0o755)
    env = {'PATH': str(wrappers) + ':/usr/bin:/bin', 'HOME': str(out), 'LANG': 'C.UTF-8'}
    report = {'agent': 'Agent #1', 'status': 'RUNNING', 'source_commit': PIN,
              'fresh_project_objects': True, 'scope': 'PR47 twenty-module thirteen-prefix closure only',
              'global_repository_acceptance': False, 'commands': [], 'sources': {},
              'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    def save():
        (out / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    def execute(label, command, cwd):
        with (out / (label + '.log')).open('wb') as log:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=log,
                                    stderr=subprocess.STDOUT, timeout=1200)
        report['commands'].append({'label': label, 'argv': command, 'exit_code': result.returncode,
                                   'log': label + '.log', 'log_sha256': digest((out / (label + '.log')).read_bytes())})
        save()
        if result.returncode:
            raise RuntimeError(label + ' failed with exit ' + str(result.returncode))
    try:
        version = subprocess.check_output([str(lean), '--version'], text=True).strip()
        if 'version 4.19.0,' not in version or '6caaee842e94' not in version:
            raise RuntimeError('Wrong official Lean release')
        report['compiler_version'] = version
        report['compiler_sha256'] = digest(lean.read_bytes())
        report['compiler_arguments'] = ['-j1', '-DElab.async=false']
        pkg = repo / 'proofs/contributions/agent-113/two-digit-prefix'
        paths = {'LychrelDigitSums': 'proofs/research/continuation/LychrelDigitSums.lean',
                 'PalindromeBridge': 'proofs/contributions/agent-104/seven-column-kernel/PalindromeBridge.lean'}
        paths.update({m: str((pkg / (m + '.lean')).relative_to(repo)) for m in MODULES[2:]})
        for module, path in paths.items():
            original = subprocess.check_output(['git', 'show', PIN + ':' + path], cwd=repo)
            if (repo / path).read_bytes() != original:
                raise RuntimeError('Changed source: ' + path)
            report['sources'][module] = {'path': path, 'sha256': digest(original),
                                       'git_blob': subprocess.check_output(['git', 'rev-parse', PIN + ':' + path], cwd=repo, text=True).strip()}
        execute('source-build', ['sh', str(pkg / 'build.sh'), str(repo), str(work)], repo)
        summary = (work / 'build-summary.txt').read_text()
        compiled = [line.split(' exit=')[0] for line in summary.splitlines()
                    if ' exit=' in line and not line.startswith('Audit ')]
        if compiled != MODULES or re.search(r'exit=[1-9]', summary):
            raise RuntimeError('Incomplete source build')
        (work / 'Agent1FullAudit.lean').write_text(audit_source())
        (out / 'Agent1FullAudit.lean').write_text(audit_source())
        env['LEAN_PATH'] = str(work)
        execute('full-module-audit', [str(lean), '-j1', '-DElab.async=false', 'Agent1FullAudit.lean'], work)
        raw = (out / 'full-module-audit.log').read_text()
        totals = re.findall(r'FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]+)', raw)
        if len(totals) != 1 or int(totals[0][0]) < 20:
            raise RuntimeError('Missing complete module-audit summary')
        report['theorem_constants_audited'] = int(totals[0][0])
        report['axiom_union_report'] = totals[0][1]
        report['unsafe_implementation_axiom_count'] = raw.count('UNSAFE_IMPLEMENTATION_AXIOM ')
        report['all_theorem_dependencies_checked_against'] = ['propext', 'Classical.choice', 'Quot.sound']
        def step(n):
            return n + int(str(n)[::-1])
        def palindrome(n):
            return str(n) == str(n)[::-1]
        witnesses = []
        for prefix, seed, depth, exponent in WITNESSES:
            values = [seed]
            for _ in range(depth):
                values.append(step(values[-1]))
            if not (palindrome(values[-1]) and all(not palindrome(n) for n in values[:-1])
                    and values[-1] // 10**exponent == prefix):
                raise RuntimeError('Sharpness control failed')
            witnesses.append({'prefix': prefix, 'seed': seed, 'depth': depth, 'trajectory': values})
        bounds = {prefix: depth for prefix, _, depth, _ in WITNESSES}
        counts = collections.Counter()
        for seed in range(1, 100000):
            value = seed
            for t in range(9):
                text = str(value)
                if len(text) >= 2 and palindrome(value) and int(text[:2]) in bounds:
                    prefix = int(text[:2])
                    if t > bounds[prefix]:
                        raise RuntimeError('Literal arithmetic control violation')
                    counts[prefix] += 1
                value = step(value)
        report['finite_controls'] = {'seed_time_pairs': 899991, 'seeds': [1, 99999], 'times': [0, 8],
                                    'continue_after_palindromes': True, 'observations': dict(counts),
                                    'sharpness': witnesses, 'not_a_substitute_for_unbounded_proof': True}
        report['status'] = 'PASS'
        return 0
    except Exception as error:
        report['status'] = 'FAIL'
        report['error'] = str(error)
        (out / 'failure.txt').write_text(traceback.format_exc())
        return 1
    finally:
        if work.exists():
            logs = out / 'module-logs'
            logs.mkdir(exist_ok=True)
            for path in sorted(work.iterdir()):
                if path.suffix in {'.log', '.txt'} or path.name == 'sources.sha256':
                    shutil.copyfile(path, logs / path.name)
            report['objects'] = {p.name: digest(p.read_bytes()) for p in work.glob('*.olean')}
        report['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        save()
        # Only throwaway compiled products and exact source copies are removed.
        # All substantive logs, audit source, source pins and exit statuses remain.
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(wrappers, ignore_errors=True)
        members = {str(p.relative_to(out)): {'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}
                   for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'FILES.json'}
        (out / 'FILES.json').write_text(json.dumps(members, indent=2) + '\n')

if __name__ == '__main__':
    raise SystemExit(main())
