#!/usr/bin/env python3
"""Retain each actual author attempt; full independent verification is separate."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import time

EVIDENCE = Path(__file__).resolve().parent
CONTRIBUTION = EVIDENCE.parent.parent
WORKSPACE = Path('/workspace/scratch/4ce7c54d31f6')
LEAN = WORKSPACE / 'lean-runtime/lean-4.19.0-linux/bin/lean'
BUILD = WORKSPACE / 'agent3-depth-aggregate-build'
CACHE = WORKSPACE / 'agent3-history-build'
SOURCE = CONTRIBUTION / 'SharpHistoryTheorem.lean'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    BUILD.mkdir(exist_ok=True)
    number = 1
    while (EVIDENCE / f'attempt-{number:03d}.json').exists():
        number += 1
    tag = f'attempt-{number:03d}'
    before = sha(SOURCE)
    shutil.copyfile(SOURCE, EVIDENCE / f'{tag}.lean.txt')
    shutil.copyfile(SOURCE, BUILD / SOURCE.name)
    env = dict(os.environ)
    env['LEAN_PATH'] = ':'.join(map(str, [BUILD, WORKSPACE / 'agent3-actual-depth-build', CONTRIBUTION / 'development/dead-prefix/build', WORKSPACE / 'agent3-depth-family-build', CACHE]))
    command = [str(LEAN), '--trust=0', '-o', 'SharpHistoryTheorem.olean', SOURCE.name]
    start = time.time()
    result = subprocess.run(command, cwd=BUILD, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    (EVIDENCE / f'{tag}.log').write_text(result.stdout)
    record = {'stage': 'author incremental compilation; not independent clean rebuild',
              'source': str(SOURCE), 'source_sha256': before,
              'lean': str(LEAN), 'lean_sha256': sha(LEAN),
              'unchanged_dependency_cache': str(CACHE),
              'dependency_source_commit': '89287c9d3eb7dd801c2b1a59eff03140d47d24ec',
              'command': command, 'cwd': str(BUILD), 'LEAN_PATH': env['LEAN_PATH'],
              'exit_code': result.returncode, 'elapsed_seconds': time.time() - start,
              'source_unchanged': before == sha(SOURCE)}
    (EVIDENCE / f'{tag}.json').write_text(json.dumps(record, indent=2) + '\n')
    print(result.stdout, end='')
    if result.returncode or not record['source_unchanged']:
        return result.returncode or 1
    declarations = re.findall(r'^(?:theorem|def)\s+(\w+)', SOURCE.read_text(), re.M)
    audit = 'import SharpHistoryTheorem\n' + '\n'.join(
        '#print axioms P196.Agent3.ThreeLayer.' + name for name in declarations) + '\n'
    (EVIDENCE / 'SharpHistoryAudit.lean').write_text(audit)
    (BUILD / 'SharpHistoryAudit.lean').write_text(audit)
    ac = [str(LEAN), '--trust=0', 'SharpHistoryAudit.lean']
    ar = subprocess.run(ac, cwd=BUILD, env=env, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True)
    (EVIDENCE / 'axiom-audit.log').write_text(ar.stdout)
    record.update({'audit_command': ac, 'audit_exit_code': ar.returncode,
                   'explicit_declarations': declarations,
                   'audit_log_sha256': sha(EVIDENCE / 'axiom-audit.log'),
                   'status': 'LEAN-CHECKED' if ar.returncode == 0 else 'AUDIT-FAILED'})
    (EVIDENCE / 'verification.json').write_text(json.dumps(record, indent=2) + '\n')
    print(ar.stdout, end='')
    return ar.returncode


if __name__ == '__main__':
    raise SystemExit(main())
