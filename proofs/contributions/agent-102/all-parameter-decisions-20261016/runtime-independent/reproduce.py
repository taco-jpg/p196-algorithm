#!/usr/bin/env python3
"""Rebuild a preserved source snapshot in a new, isolated output directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--lean', type=Path, required=True)
    args = parser.parse_args()
    source = args.snapshot.resolve()
    output = args.output.resolve()
    lean = args.lean.resolve()
    modules = [
        'Agent102RunDefs', 'Agent102AffineArithmetic', 'Agent102RunWord',
        'Agent102RunEndpoints', 'Agent102AffineRuns', 'Agent102AffineDecision',
        'Agent102AffineBoundary', 'Agent102RunDecision',
        'Agent102AffineAllParameters', 'Agent102AllParameterControls',
    ]
    for audit in ['LiteralAudit', 'ModuleOriginAudit', 'ExecutableDependencyAudit']:
        if (source / (audit + '.lean')).is_file():
            modules.append(audit)
    if output.exists():
        parser.error('output already exists; a new directory is required')
    pins = {}
    for module in modules:
        path = source / (module + '.lean')
        data = path.read_bytes()
        pins[path.name] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
    pinfile = source.parent / 'SOURCE_PINS.json'
    if pinfile.is_file():
        expected = json.loads(pinfile.read_text())
        for name, pin in pins.items():
            if name not in expected or expected[name] != pin:
                parser.error('source hash mismatch: ' + name)
    output.mkdir(parents=True)
    build = output / 'build'
    logs = output / 'logs'
    build.mkdir()
    logs.mkdir()
    for module in modules:
        shutil.copy2(source / (module + '.lean'), build / (module + '.lean'))
    (output / 'SOURCE_PINS.json').write_text(json.dumps(pins, indent=2) + '\n')
    environment = os.environ.copy()
    environment['LEAN_PATH'] = '.'
    version = subprocess.run([str(lean), '--version'], capture_output=True, text=True,
                             timeout=15, check=True).stdout.strip()
    if 'version 4.19.0' not in version or '6caaee842e94' not in version:
        raise RuntimeError('unexpected Lean version: ' + version)
    (output / 'environment.json').write_text(json.dumps({
        'lean': str(lean), 'version': version,
        'lean_sha256': hashlib.sha256(lean.read_bytes()).hexdigest(),
        'source': str(source), 'flags': ['--trust=0', '-j1', '-DElab.async=false'],
        'LEAN_PATH': '.', 'preexisting_olean_used': False,
    }, indent=2) + '\n')
    results = []
    for module in modules:
        command = [str(lean), '--trust=0', '-j1', '-DElab.async=false',
                   '-o', module + '.olean', module + '.lean']
        started = time.monotonic()
        logfile = logs / (module + '.log')
        with logfile.open('w') as log:
            try:
                result = subprocess.run(command, cwd=build, env=environment,
                                        stdout=log, stderr=subprocess.STDOUT, timeout=90)
                code = result.returncode
            except subprocess.TimeoutExpired:
                log.write('\nREPRODUCE_TIMEOUT_90_SECONDS\n')
                code = 124
        row = {'module': module, 'command': command, 'cwd': str(build),
               'LEAN_PATH': '.', 'returncode': code,
               'seconds': round(time.monotonic() - started, 3)}
        results.append(row)
        (output / 'verification.json').write_text(json.dumps(results, indent=2) + '\n')
        print(json.dumps(row), flush=True)
        if code:
            print(logfile.read_text(), flush=True)
            return code
    return 0


if __name__ == '__main__':
    sys.exit(main())
