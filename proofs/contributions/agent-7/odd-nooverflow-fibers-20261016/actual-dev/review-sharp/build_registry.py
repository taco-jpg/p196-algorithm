#!/usr/bin/env python3
"""Prepare the scoped odd-fiber registry after checking every source freeze."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy

PACKAGE = Path(__file__).resolve().parents[2]
REPO = PACKAGE.parents[3]
VERIFIER = REPO / 'proofs/verify_project__214bf7673efe116b.py'
VERIFIER_SHA256 = 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'
PROJECT = 'agent7-odd-nooverflow-fibers'
FROZEN = {
    'OddCenter': '72f1c2e64a587e25f85482b6f61ceea0763218d60c7c7cc5eaa7d1d31ca65728',
    'OddActual': '15b8a66e67da8fecaf6e244416825a2a28ecb1e188ac8eccbb53827cfff427bf',
    'OddWords': 'f0827099cffeeab2997c0a572906d8bd370e048aa859beb3bb8189ad5bc217a3',
    'OddCanonical': '46529b9c0bd55a3ae069900789f4747e9de7f58b5c6f82350ee4c657a551e617',
    'OddCounts': '7e7a97c04a065e4060d11c652807ba6e8f3531da505e4336070caf97beabe939',
    'OddCountsFixedCenter': 'cc7fe4bad83f09c1abd4be37f63eaaa901497d568ce0d774243ab91f5e2dc0f0',
    'OddCountsPhase': 'c5bbfdfd2d0ed704b132cb60d13cb14b2c79688b1c44a3c0135ac695a1666cff',
    'OddSharp': 'bc4d4fe2d7655a5bb81ecda5475f3b0abd9dbc91e41cc766dec92b35c5741d57',
    'OddOutputRange': 'a74808c8f2bfaf8c8b40fc76878165913689dc267854e11c8d05ccd64a039e4a',
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', action='append', default=[])
    ap.add_argument('--expect', action='append', default=[])
    ap.add_argument('--output', type=Path, default=PACKAGE / 'PROJECT_REGISTRY.json')
    args = ap.parse_args()
    if sha(VERIFIER.read_bytes()) != VERIFIER_SHA256:
        raise ValueError('Retained canonical verifier source changed')
    code_only = runpy.run_path(str(VERIFIER), run_name='registry_reference')['code_only']
    expected = dict(FROZEN)
    for entry in args.expect:
        module, value = entry.split('=', 1)
        if module in expected and expected[module] != value:
            raise ValueError('Conflicting frozen module: ' + module)
        expected[module] = value
    dependencies = {Path(rec['file']).stem: rec['sha256'] for rec in json.loads((PACKAGE / 'dependencies/SOURCE_PINS.json').read_text())}
    expected.update(dependencies)
    sources = {p.stem: p for p in (PACKAGE / 'dependencies').glob('*.lean')}
    sources.update({p.stem: p for p in PACKAGE.glob('*.lean')})
    roots = args.root or ['OddComplete']
    modules, active, claims = {}, set(), []

    def visit(module):
        if module in modules:
            return
        if module not in sources:
            if module.split('.')[0] in {'Init', 'Std', 'Lean'}:
                return
            raise ValueError('Unregistered local import: ' + module)
        if module in active:
            raise ValueError('Import cycle at ' + module)
        if module not in expected:
            raise ValueError('Missing independently supplied source freeze: ' + module)
        active.add(module)
        path = sources[module]
        data = path.read_bytes()
        if sha(data) != expected[module]:
            raise ValueError('Frozen source hash mismatch: ' + module)
        code = code_only(data.decode())
        if re.search(r'\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b', code):
            raise ValueError('Forbidden source token: ' + module)
        imports = [d for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for d in line.split()]
        for dependency in imports:
            visit(dependency)
        modules[module] = {
            'path': path.relative_to(REPO).as_posix(),
            'sha256': sha(data),
            'git_blob': hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest(),
            'imports': imports,
        }
        if module not in dependencies:
            namespaces = re.findall(r'^namespace\s+(\S+)', code, re.M)
            if len(namespaces) != 1:
                raise ValueError('Namespace structure requires manual endpoint registration: ' + module)
            names = re.findall(r'^(?:@\[[^\n]*\]\s*)?(?:theorem|lemma)\s+([A-Za-z_][\w.]*)', code, re.M)
            if not names:
                raise ValueError('No public theorem endpoints: ' + module)
            claims.append({
                'id': 'agent7-odd-' + module,
                'project': PROJECT,
                'module': module,
                'endpoints': [namespaces[0] + '.' + name for name in names],
            })
        active.remove(module)

    for root in roots:
        visit(root)
    registry = {
        'schema_version': 1,
        'catalogue_complete': False,
        'catalogue_blockers': ['This registry contains one explicitly scoped Agent 7 contribution. It does not assert completeness of the repository accepted-project catalogue.'],
        'prepared_by': 'Agent #7 /root/runtime',
        'retained_verifier': {'path': VERIFIER.relative_to(REPO).as_posix(), 'sha256': VERIFIER_SHA256},
        'toolchain': {
            'version': '4.19.0',
            'commit': '6caaee842e94',
            'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound'],
        },
        'projects': {
            PROJECT: {
                'scope': 'Complete canonical odd-width coefficient-word inverse fibers of the original Agent8.stepWord, with source length 2*m+1, reversal symmetry, coefficients below 19, positive outer coefficient, even literal source center, and zero final scan carry. Exact duplicate-free enumeration for arbitrary requested output lists, global sharp maximum (fib (m+1)+1)/2, fixed encoded-center maxima at positive half-width, and an explicit attaining family. This scope asserts one transition, not all-time orbit nontermination.',
                'roots': roots,
                'modules': modules,
            },
        },
        'claims': claims,
    }
    encoded = (json.dumps(registry, indent=2) + '\n').encode()
    args.output.write_bytes(encoded)
    print(json.dumps({'registry': str(args.output), 'sha256': sha(encoded), 'roots': roots, 'module_count': len(modules), 'new_module_count': len(claims), 'public_endpoints': sum(len(c['endpoints']) for c in claims)}, indent=2))

if __name__ == '__main__':
    main()
