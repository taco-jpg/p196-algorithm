#!/usr/bin/env python3
"""Rebuild the complete pinned project closure in a new directory and audit it."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parents[3]
SCOPE = json.loads((HERE / 'SCOPE.json').read_text())
LEAN = shutil.which(os.environ.get('LEAN', 'lean'))
if LEAN is None:
    raise SystemExit('Set LEAN to the official Lean 4.19.0 executable.')
BUILD = Path(tempfile.mkdtemp(prefix='agent112-eventual-'))
print(f'Fresh build directory: {BUILD}', flush=True)
version = subprocess.check_output([LEAN, '--version'], text=True).strip()
if f'version {SCOPE["lean_version"]}' not in version or SCOPE['lean_commit_prefix'] not in version:
    raise SystemExit(f'Unexpected Lean version: {version}')
records: list[dict] = []
report = {'version': version, 'source_commit': SCOPE['proof_source_commit'],
          'build_directory': str(BUILD), 'modules': records, 'status': 'RUNNING'}

def save_report() -> None:
    (BUILD / 'REPORT.json').write_text(json.dumps(report, indent=2) + '\n')

with (BUILD / 'BUILD.log').open('w') as log:
    log.write(version + '\n')
    for row in SCOPE['modules']:
        source = ROOT / row['path']
        raw = source.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != row['sha256']:
            raise SystemExit(f'Source hash mismatch: {source}')
        (BUILD / (row['module'] + '.lean')).write_bytes(raw)
        log.write(f'{digest}  {row["module"]}.lean\n')
    shutil.copyfile(HERE / 'AuditAll.lean', BUILD / 'AuditAll.lean')
    for module in [row['module'] for row in SCOPE['modules']] + ['AuditAll']:
        start = time.monotonic()
        command = [LEAN, '-o', module + '.olean', module + '.lean']
        with (BUILD / (module + '.log')).open('w') as out:
            try:
                proc = subprocess.run(command, cwd=BUILD,
                    env={**os.environ, 'LEAN_PATH': str(BUILD)},
                    stdout=out, stderr=subprocess.STDOUT, timeout=300)
                rc = proc.returncode
            except subprocess.TimeoutExpired:
                rc = 124
        record = {'module': module, 'command': command, 'exit': rc,
                  'seconds': round(time.monotonic() - start, 3)}
        records.append(record)
        save_report()
        text = (BUILD / (module + '.log')).read_text()
        log.write(json.dumps(record) + '\n' + text)
        log.flush()
        print(f'{module}: exit={rc}', flush=True)
        if rc != 0:
            report['status'] = 'FAIL'
            save_report()
            raise SystemExit(f'{module} failed; see {BUILD}')
    text = (BUILD / 'AuditAll.log').read_text()
    found: dict[str, list[str]] = {}
    pattern = r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
    for match in re.finditer(pattern, text):
        found[match.group(1)] = [s.strip() for s in (match.group(2) or '').split(',') if s.strip()]
    expected = set(SCOPE['audited_declarations'])
    if set(found) != expected:
        raise SystemExit('Incomplete axiom audit: ' + repr(expected - set(found)))
    forbidden = {name: axioms for name, axioms in found.items()
                 if set(axioms) - set(SCOPE['allowed_axioms'])}
    if forbidden:
        raise SystemExit('Excluded transitive axioms: ' + repr(forbidden))
    report.update(status='PASS', audited_declarations=found)
    save_report()
    log.write('PASS: complete fresh source build and transitive axiom allowlist audit.\n')
print(f'PASS: {len(expected)} declarations audited; evidence in {BUILD}', flush=True)
