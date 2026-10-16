#!/usr/bin/env python3
"""Clean, offline, source-pinned Lean verifier for Agent #421's contribution.

The source repository may be an ordinary checkout or a bare Git repository.
No network, pre-existing .olean files, or mutable branch refs are used.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(args: list[str], cwd: Path | None = None, env: dict[str, str] | None = None,
        timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True,
                          text=True, timeout=timeout, check=False)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--lean', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True,
                    help='New directory; existing paths are rejected to prevent stale builds.')
    ap.add_argument('--timeout', type=int, default=180)
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    manifest = json.loads((here/'manifest.json').read_text())
    exports = json.loads((here/'exports.json').read_text())
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    build = out/'build'
    build.mkdir()
    logs = out/'logs'
    logs.mkdir()
    report = {
        'agent': 'Agent #421', 'task_id': manifest['task_id'],
        'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'source_commit': manifest['source_commit'],
        'inspected_main': manifest['inspected_main'],
        'verification_level': 'IN_PROGRESS',
        'independent_review': False, 'integrated': False,
        'modules': [], 'axiom_checks': {},
    }
    def save() -> None:
        (out/'verification.json').write_text(json.dumps(report, indent=2)+'\n')
    try:
        version = run([str(args.lean.resolve()), '--version'], timeout=args.timeout)
        report['lean_version_output'] = version.stdout.strip()
        if version.returncode or f"version {manifest['lean_version']}" not in version.stdout:
            raise RuntimeError('Unexpected Lean version or unusable compiler.')
        if manifest['lean_commit'] not in version.stdout:
            raise RuntimeError('Unexpected Lean commit.')
        git_prefix = ['git', '-C', str(args.repo.resolve())]
        for dep in manifest['dependencies']:
            origin = run(git_prefix + ['rev-parse', manifest['source_commit']+':'+dep['source_path']],
                         timeout=args.timeout)
            if origin.returncode or origin.stdout.strip() != dep['git_blob']:
                raise RuntimeError('Pinned commit/path mismatch: '+dep['module'])
            cp = subprocess.run(git_prefix + ['cat-file', 'blob', dep['git_blob']],
                                capture_output=True, timeout=args.timeout, check=False)
            if cp.returncode:
                raise RuntimeError('Pinned dependency blob unavailable: '+dep['module'])
            if digest(cp.stdout) != dep['sha256']:
                raise RuntimeError('Dependency hash mismatch: '+dep['module'])
            (build/(dep['module']+'.lean')).write_bytes(cp.stdout)
        for src in manifest['sources']:
            data = (here/src['file']).read_bytes()
            if digest(data) != src['sha256']:
                raise RuntimeError('Contribution hash mismatch: '+src['module'])
            (build/(src['module']+'.lean')).write_bytes(data)
        # Reject excluded proof shortcuts in the entire imported source closure.
        forbidden = re.compile(r'\b(sorry|admit|native_decide|sorryAx|axiom)\b')
        for file in build.glob('*.lean'):
            hit = forbidden.search(file.read_text())
            if hit:
                raise RuntimeError(f'Excluded token {hit.group(1)} in {file.name}')
        env = os.environ.copy()
        env['LEAN_PATH'] = str(build)
        report['clean_build_directory'] = str(build)
        report['source_manifest_sha256'] = digest((here/'manifest.json').read_bytes())
        report['source_hashes'] = {p.name:digest(p.read_bytes()) for p in sorted(build.glob('*.lean'))}
        for name in manifest['build_order']:
            command = [str(args.lean.resolve()), '-o', name+'.olean', name+'.lean']
            started = time.monotonic()
            cp = run(command, cwd=build, env=env, timeout=args.timeout)
            (logs/(name+'.log')).write_text(cp.stdout+cp.stderr)
            report['modules'].append({'name':name, 'command':command,
                                     'exit_code':cp.returncode,
                                     'seconds':time.monotonic()-started})
            save()
            if cp.returncode:
                raise RuntimeError('Compilation failed: '+name)
        audit = 'import Agent421NoOverflow\n\n' + ''.join(
            '#print axioms '+entry['name']+'\n' for entry in exports)
        (build/'Agent421Audit.lean').write_text(audit)
        cp = run([str(args.lean.resolve()), 'Agent421Audit.lean'], cwd=build,
                 env=env, timeout=args.timeout)
        axiom_log = cp.stdout+cp.stderr
        (logs/'axioms.log').write_text(axiom_log)
        if cp.returncode:
            raise RuntimeError('Axiom audit compilation failed.')
        found = {}
        for match in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", axiom_log):
            found[match.group(1)] = [a.strip() for a in (match.group(2) or '').split(',') if a.strip()]
        allowed = set(manifest['allowed_axioms'])
        for entry in exports:
            name = entry['name']
            if name not in found:
                raise RuntimeError('Missing axiom audit: '+name)
            unexpected = set(found[name])-allowed
            if unexpected:
                raise RuntimeError('Unapproved axioms for '+name+': '+str(unexpected))
        report['axiom_checks'] = found
        report['exported_theorem_count'] = len(exports)
        report['allowed_axioms'] = sorted(allowed)
        report['verification_level'] = 'LEAN_CHECKED'
        report['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        save()
        print(json.dumps({'status':'LEAN_CHECKED','theorems':len(exports),
                          'modules':len(report['modules']),'report':str(out/'verification.json')},indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        report['verification_level'] = 'FAILED_OR_BLOCKED'
        report['error'] = str(exc)
        report['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        save()
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
