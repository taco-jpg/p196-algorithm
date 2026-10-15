#!/usr/bin/env python3
"""Fresh scoped Lean build with pinned source and complete failure evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

BASE = 'eec3d5f3646cab50abad6e610ea19626cd249070'
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SEARCH = [HERE, ROOT / 'proofs/research']
ALLOW = {'propext', 'Classical.choice', 'Quot.sound'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lean', required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--timeout', type=int, default=300)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    lean = str(Path(args.lean).resolve())
    version = subprocess.check_output([lean, '--version'], text=True).strip()
    if 'version 4.19.0,' not in version:
        raise SystemExit('wrong Lean version: ' + version)
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    ordered, visited, active = [], set(), set()

    def visit(module):
        if module.split('.')[0] in {'Std', 'Init', 'Lean'} or module in visited:
            return
        if module in active:
            raise RuntimeError('cyclic local imports: ' + module)
        active.add(module)
        rel = Path(*module.split('.')).with_suffix('.lean')
        candidates = [base / rel for base in SEARCH if (base / rel).is_file()]
        if not candidates:
            raise FileNotFoundError('unresolved module: ' + module)
        src = candidates[0]
        for line in src.read_text().splitlines():
            match = re.match(r'^\s*import\s+(.+)$', line)
            if match:
                for child in match.group(1).split('--', 1)[0].split():
                    visit(child)
        active.remove(module)
        visited.add(module)
        ordered.append((module, rel, src))

    visit('All')
    manifest = {'agent': 121, 'commit': commit, 'base': BASE, 'lean': version,
                'entry': 'All.lean', 'status': 'RUNNING', 'sources': [], 'runs': []}
    fail = 0
    with tempfile.TemporaryDirectory(prefix='agent121-clean-') as tmp:
        build = Path(tmp)
        env = dict(os.environ, LEAN_PATH=str(build))
        for module, rel, src in ordered:
            blob = src.read_bytes()
            own = HERE in src.parents
            rel_repo = src.relative_to(ROOT).as_posix()
            if not own:
                pinned = subprocess.check_output(['git', 'show', BASE + ':' + rel_repo], cwd=ROOT)
                if pinned != blob:
                    raise RuntimeError('changed prerequisite source: ' + rel_repo)
            dest = build / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            manifest['sources'].append({'module': module, 'path': rel_repo,
                'sha256': hashlib.sha256(blob).hexdigest(), 'pinned_base': None if own else BASE})
            command = [lean, '-o', str(rel.with_suffix('.olean')), str(rel)]
            print('BUILD', module, flush=True)
            try:
                proc = subprocess.run(command, cwd=build, env=env, text=True,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=args.timeout)
                text, status = proc.stdout, proc.returncode
            except subprocess.TimeoutExpired as exc:
                text = exc.stdout or ''
                if isinstance(text, bytes):
                    text = text.decode('utf-8', errors='replace')
                text += '\nTIMEOUT after ' + str(args.timeout) + ' seconds\n'
                status = 124
            log = out / (module.replace('.', '_') + '.log')
            log.write_text(text)
            manifest['runs'].append({'module': module, 'command': command,
                'exit_status': status, 'log': log.name,
                'log_sha256': hashlib.sha256(text.encode()).hexdigest()})
            if own or status:
                print(text, end='', flush=True)
            else:
                print('PINNED_FOUNDATION_PASS', module, 'full log retained', flush=True)
            if status:
                fail = status
                break
            if own:
                if re.search(r'\b(?:sorry|admit|native_decide|sorryAx)\b', blob.decode()):
                    raise RuntimeError('excluded shortcut in own source: ' + rel_repo)
                for names in re.findall(r'depends on axioms: \[([^]]*)\]', text):
                    axioms = {x.strip() for x in names.split(',') if x.strip()}
                    if not axioms <= ALLOW:
                        raise RuntimeError('excluded transitive axiom: ' + str(axioms))
        manifest['status'] = 'PASS' if not fail else 'FAIL'
    (out / 'verification.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('BUILD_RESULT', manifest['status'], 'SOURCE_COMMIT', commit, flush=True)
    raise SystemExit(fail)


if __name__ == '__main__':
    main()
