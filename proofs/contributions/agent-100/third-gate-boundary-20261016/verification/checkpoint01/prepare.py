#!/usr/bin/env python3
"""Freeze the complete third-gate registry after receiving the Controls source hash; no compilation."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
OLD_REGISTRY_SHA256 = 'ac31d0cfd710df17bc7ab4bc8eba102bc63d9a93875abd19fe0fa904cab5c36c'
SHARED_REPLAY_SHA256 = '575b013fd96475cc869f082af94dbde91493da90e5e447a4da1f23c8884d9bd3'
FROZEN = {
    'Agent100ThirdGateBoundary': '7f6992f08e7f7b75e0a609d54a64f9ac7c2b80344296761be111e740ef48a96c',
    'Agent100ThirdGateNumeric': 'b1ff8e06cf63d34a935f826b806dbd02fcf3808b83511e062f91a3d64da7e3db',
}
PROJECT = 'third-gate-boundary'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def inspect_source(root, name, expected_sha):
    path = root / 'proofs' / (name + '.lean')
    raw = path.read_bytes()
    assert sha(raw) == expected_sha, (name, 'source SHA mismatch')
    text = raw.decode()
    imports = re.findall(r'^import\s+(\S+)\s*$', text, re.M)
    rec = {'path': str(path.relative_to(root)), 'sha256': sha(raw),
           'git_blob': hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest(), 'imports': imports}
    namespaces = re.findall(r'^namespace\s+(\S+)\s*$', text, re.M)
    assert len(namespaces) == 1, (name, 'review namespace extraction manually')
    statements = []
    for match in re.finditer(r'^theorem\s+(\w+)\b([\s\S]*?)\s*:=', text, re.M):
        signature = match.group(0).rsplit(':=', 1)[0].rstrip()
        statements.append({'name': namespaces[0] + '.' + match.group(1),
                           'signature_source': signature, 'signature_sha256': sha(signature.encode())})
    printed = re.findall(r'^#print axioms\s+(\S+)\s*$', text, re.M)
    assert set(printed) == {s['name'] for s in statements}, (name, 'named export inventory mismatch')
    return rec, {'source_path': rec['path'], 'sha256': rec['sha256'], 'git_blob': rec['git_blob'],
                 'theorem_count': len(statements), 'statements': statements}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls-sha256', required=True)
    parser.add_argument('--claim-commit', required=True)
    parser.add_argument('--claim-blob', required=True)
    args = parser.parse_args()
    for value, length in [(args.controls_sha256, 64), (args.claim_commit, 40), (args.claim_blob, 40)]:
        assert re.fullmatch('[0-9a-f]{' + str(length) + '}', value), 'Complete immutable hash required'
    root = Path(subprocess.check_output(['git', '-C', str(HERE), 'rev-parse', '--show-toplevel'], text=True).strip())
    oldroot = root / 'proofs/contributions/agent-100/groupII-overlap-20261016/verification'
    old = oldroot / 'checkpoint02/registry.json'
    assert sha(old.read_bytes()) == OLD_REGISTRY_SHA256
    assert sha((oldroot / 'dependencies/replay.py').read_bytes()) == SHARED_REPLAY_SHA256
    registry = json.loads(old.read_bytes())
    modules = copy.deepcopy(registry['projects']['groupii-full']['modules'])
    del modules['Agent100GroupIIDefect']
    inventory = {}
    frozen = dict(FROZEN, Agent100ThirdGateControls=args.controls_sha256)
    for name, expected in frozen.items():
        modules[name], inventory[name] = inspect_source(root, name, expected)
    assert modules['Agent100ThirdGateBoundary']['imports'] == ['Agent100DoubleGate']
    assert modules['Agent100ThirdGateNumeric']['imports'] == ['Agent100ThirdGateBoundary']
    for name, rec in modules.items():
        raw = (root / rec['path']).read_bytes()
        assert sha(raw) == rec['sha256'], name
        assert hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() == rec['git_blob'], name
        assert re.findall(r'^import\s+(\S+)\s*$', raw.decode(), re.M) == rec['imports'], name
    roots = ['Agent100ThirdGateNumeric', 'Agent100ThirdGateControls']
    seen = set()
    def visit(name):
        if name in ['Init', 'Std', 'Lean'] or name in seen:
            return
        assert name in modules, ('Unexpected missing local import', name)
        seen.add(name)
        for imp in modules[name]['imports']:
            visit(imp)
    for name in roots:
        visit(name)
    assert seen == set(modules) and len(modules) == 12, 'Expected exact 12-module closure'
    registry['projects'] = {PROJECT: {'scope': 'Independent fresh twelve-module build: actual third two-step overlap obstruction at time six, universal ordinary-integer transfer, and kernel boundary controls. No infinite or time-six nonpalindrome assertion.', 'roots': roots, 'modules': modules}}
    claims = [copy.deepcopy(c) for c in registry['claims'] if not c['id'].startswith('checkpoint02-Agent100GroupIIDefect-')]
    for claim in claims:
        claim['id'] = 'third-gate-inherited-' + claim['id']
        claim['project'] = PROJECT
    for name, rec in inventory.items():
        for statement in rec['statements']:
            claims.append({'id': 'third-gate-' + name + '-' + statement['name'].split('.')[-1], 'project': PROJECT, 'endpoints': [statement['name']]})
    registry['claims'] = claims
    registry['catalogue_blockers'] = ['Scoped Agent #100 third-gate checkpoint01 only; global accepted catalogue remains incomplete and unchanged.']
    registry['source_baseline'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    registry['source_provenance_note'] = 'Baseline is the actual worktree HEAD at registry preparation; new files are identified by exact source pins, not presumed members of that baseline commit.'
    registry['claim_commit'] = args.claim_commit
    registry['claim_blob'] = args.claim_blob
    (HERE / 'registry.json').write_text(json.dumps(registry, indent=2) + '\n')
    (HERE / 'statement-inventory.json').write_text(json.dumps({'scope': 'All named theorem exports in three frozen ThirdGate modules', 'modules': inventory}, indent=2) + '\n')
    regsha = sha((HERE / 'registry.json').read_bytes())
    launcher = '''#!/usr/bin/env python3
"""Replay the exact twelve-module third-gate closure in a fresh directory."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
HERE = Path(__file__).resolve().parent
REGISTRY_SHA256 = %r
SHARED_REPLAY_SHA256 = %r
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(subprocess.check_output(['git', '-C', str(HERE), 'rev-parse', '--show-toplevel'], text=True).strip())
    registry = HERE / 'registry.json'
    shared = root / 'proofs/contributions/agent-100/groupII-overlap-20261016/verification/dependencies/replay.py'
    for path, expected in [(registry, REGISTRY_SHA256), (shared, SHARED_REPLAY_SHA256)]:
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned replay component changed: ' + str(path))
    return subprocess.run([sys.executable, str(shared), '--registry', str(registry), '--project', 'third-gate-boundary', '--lean', str(args.lean.resolve()), '--output', str(args.output.resolve())]).returncode
if __name__ == '__main__':
    raise SystemExit(main())
''' % (regsha, SHARED_REPLAY_SHA256)
    (HERE / 'replay.py').write_text(launcher)
    print(json.dumps({'registry_sha256': regsha, 'module_count': len(modules), 'all_named_endpoints': len(claims), 'new_named_endpoints': sum(x['theorem_count'] for x in inventory.values()), 'compiled': False}, indent=2))

if __name__ == '__main__':
    main()
