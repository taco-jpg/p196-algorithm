#!/usr/bin/env python3
"""Prepare the exact scoped registry after all new module source pins freeze."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import runpy

PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[3]
VERIFIER = REPO / 'proofs/verify_project__214bf7673efe116b.py'
VERIFIER_SHA256 = 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'
PROJECT = 'agent7-allbase-overflow-births'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', default='CanonicalOverflowBirths')
    ap.add_argument('--expect', action='append', required=True, help='Frozen new-module pin: Module=SHA256')
    ap.add_argument('--output', type=Path, default=PACKAGE / 'PROJECT_REGISTRY.json')
    args = ap.parse_args()
    assert sha(VERIFIER) == VERIFIER_SHA256
    code_only = runpy.run_path(str(VERIFIER), run_name='registry_reference')['code_only']
    pins = json.loads((PACKAGE / 'dependencies/SOURCE_PINS.json').read_text())
    dependency_pins = {r['module']: r['sha256'] for r in pins['dependencies']}
    frozen = dict(item.split('=', 1) for item in args.expect)
    assert len(frozen) == len(args.expect)
    sources = {p.stem: p for p in (PACKAGE / 'dependencies').glob('*.lean')}
    sources.update({p.stem: p for p in PACKAGE.glob('*.lean')})
    records, claims, active = {}, [], set()

    def visit(module):
        if module in records:
            return
        if module not in sources:
            assert module.split('.')[0] in {'Std', 'Init', 'Lean'}, module
            return
        assert module not in active, ('import cycle', module)
        active.add(module)
        path = sources[module]
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        expected = dependency_pins.get(module) if module in dependency_pins else frozen[module]
        assert digest == expected, ('source pin mismatch', module, digest, expected)
        code = code_only(data.decode())
        assert not re.search(r'\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b', code), module
        imports = [d for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for d in line.split()]
        for dependency in imports:
            visit(dependency)
        records[module] = {
            'path': str(path.relative_to(REPO)),
            'sha256': digest,
            'git_blob': hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest(),
            'imports': imports,
        }
        if module not in dependency_pins:
            namespaces = re.findall(r'^namespace\s+(\S+)', code, re.M)
            assert namespaces == ['P196.Agent7.AllBaseOverflow'], (module, namespaces)
            public = re.findall(r'^(?:@\[[^\n]*\]\s*)?(?:theorem|lemma)\s+([A-Za-z_][\w.]*)', code, re.M)
            assert public, ('no public theorem', module)
            claims.append({'id': module + '-public-contracts', 'project': PROJECT,
                           'endpoints': [namespaces[0] + '.' + name for name in public]})
        active.remove(module)

    visit(args.root)
    assert set(dependency_pins) <= set(records), 'Missing expected inherited module'
    assert set(frozen) == set(records) - set(dependency_pins), 'Frozen pins must exactly cover all new modules in the root closure'
    registry = {
        'schema_version': 1,
        'catalogue_complete': False,
        'catalogue_blockers': ['This is the isolated Agent 7 all-base overflow-births contribution registry, not a complete repository-wide accepted-scope census.'],
        'toolchain': {'version': '4.19.0', 'commit': '6caaee842e94',
                      'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound']},
        'projects': {PROJECT: {
            'scope': 'For every integer base b>=2, the original actual ordinary normalization of a bounded symmetric tagged coefficient word with computed terminal carry one has width L+1, the shifted adjacent interior pair identity and exact four-row zero/max classifiers, the neutral-neighbor necessary condition, and exact endpoint behavior including the binary exception. Canonical reverse-add specialization uses the unchanged ReverseAdd.reverse_add_normalization on bounded positive finite input digit words with literal coefficient projection. No orbit, lifetime, population or 196 claim is included.',
            'roots': [args.root], 'modules': records,
        }},
        'claims': claims,
        'preparation': {
            'status': 'PREPARED; this registry alone is not an execution or PASS result',
            'prepared_by': 'Agent #7 /root/runtime',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'reference_verifier': str(VERIFIER.relative_to(REPO)),
            'reference_verifier_sha256': VERIFIER_SHA256,
            'dependency_source_pins_sha256': sha(PACKAGE / 'dependencies/SOURCE_PINS.json'),
            'preparer_sha256': sha(Path(__file__)),
        },
    }
    with args.output.open('x') as stream:
        stream.write(json.dumps(registry, indent=2) + '\n')
    print(json.dumps({'output': str(args.output), 'sha256': sha(args.output),
                      'modules': len(records), 'new_public_endpoints': sum(len(c['endpoints']) for c in claims)}, indent=2))


if __name__ == '__main__':
    main()
