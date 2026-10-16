"""Fresh, sequential Lean 4.19.0 rebuild of accepted Agent6 modules only.

Run: python check.py --lean /path/to/lean --output-dir /path/to/audit
No failed development sources or pre-existing compiled objects are reused.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

MODULES = ('ExteriorCore', 'ExteriorCapTwo', 'ExteriorCoverage', 'ExteriorBridge',
           'ExteriorProjection', 'ExteriorArithmetic', 'ExteriorSharp',
           'ExteriorPotentialObstruction', 'ExteriorAbsorbedObstruction',
           'ExteriorOrdinaryWitnesses')
STANDARD_AXIOMS = {'propext', 'Quot.sound', 'Classical.choice'}


def run(lean: str, output: Path, timeout: int) -> dict:
    exe = shutil.which(lean)
    if exe is None:
        raise FileNotFoundError(f'Lean executable not found: {lean}')
    exe = str(Path(exe).resolve())
    version = subprocess.check_output([exe, '--version'], text=True).strip()
    if 'version 4.19.0,' not in version:
        raise RuntimeError(f'Expected pinned Lean 4.19.0, received: {version}')
    source_dir = Path(__file__).resolve().parent
    output.mkdir(parents=True, exist_ok=True)
    report = {'lean_version': version, 'fresh_directory': True,
              'modules': [], 'status': 'IN_PROGRESS'}
    with tempfile.TemporaryDirectory(prefix='agent6-checked-') as temporary:
        work = Path(temporary)
        env = dict(os.environ, LEAN_PATH=str(work))
        for module in MODULES:
            source = source_dir / (module + '.lean')
            data = source.read_bytes()
            text = data.decode('utf-8')
            if re.search(r'\b(sorry|admit|native_decide|ofReduceBool)\b|^\s*axiom\b|decide\s+\+native', text, re.M):
                raise RuntimeError(f'Forbidden proof shortcut in {source.name}')
            declared = re.findall(r'\btheorem\s+(\w+)', text)
            (work / source.name).write_bytes(data)
            start = time.monotonic()
            process = subprocess.run([exe, '-o', module + '.olean', source.name],
                                     cwd=work, env=env, capture_output=True, text=True,
                                     timeout=timeout)
            log = process.stdout + process.stderr
            (output / (module + '.log')).write_text(log)
            audits = {}
            for name, dependency in re.findall(r"'([^']+)' (depends on axioms: \[[^\]]*\]|does not depend on any axioms)", log):
                axioms = [] if dependency.startswith('does not') else re.findall(r'[\w.]+', dependency.split('[', 1)[1])
                if not set(axioms) <= STANDARD_AXIOMS:
                    raise RuntimeError(f'Unaccepted axioms for {name}: {axioms}')
                audits[name] = axioms
            expected = {'P196.Agent6.' + name for name in declared}
            accepted = process.returncode == 0 and set(audits) == expected
            entry = {'module': module, 'source_sha256': hashlib.sha256(data).hexdigest(),
                     'source_git_blob_sha1': hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest(),
                     'exit_code': process.returncode,
                     'elapsed_seconds': round(time.monotonic()-start, 4),
                     'theorem_count': len(declared), 'axiom_audits': audits,
                     'log_sha256': hashlib.sha256(log.encode()).hexdigest(),
                     'status': 'PASS' if accepted else 'FAIL'}
            report['modules'].append(entry)
            (output / 'verification.json').write_text(json.dumps(report, indent=2)+'\n')
            print(f'{module}: {entry["status"]}; {len(audits)} theorem audits', flush=True)
            if not accepted:
                raise RuntimeError(f'Build/audit failed for {module}:\n{log}')
        report['status'] = 'PASS'
        report['theorem_count'] = sum(row['theorem_count'] for row in report['modules'])
        (output / 'verification.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lean', default='lean')
    parser.add_argument('--output-dir', type=Path, default=Path('fresh-audit'))
    parser.add_argument('--timeout-per-module', type=int, default=120)
    args = parser.parse_args()
    run(args.lean, args.output_dir, args.timeout_per_module)
