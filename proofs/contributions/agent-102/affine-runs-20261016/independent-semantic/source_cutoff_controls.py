#!/usr/bin/env python3
"""Supplementary finite controls for the exact reviewed compareCutoff formula."""
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import time

from independent_controls import Affine, at, endpoints, expand, sign, tail_cutoff

HERE = Path(__file__).resolve().parent
REPO = Path('/workspace/scratch/fb513c1676b0/p196-agent102')


def source_bound(left, right):
    fs = endpoints(left) + endpoints(right)
    return max([0] + [abs(f.b) + 1 for _, f in left + right]
               + [abs(f.b) + abs(g.b) + 1 for f in fs for g in fs])


started = time.monotonic()
fs = [Affine(a, b) for a in range(-3, 4) for b in range(-6, 7)]
scalar_checks = 0
for f, g in product(fs, repeat=2):
    bound = abs(f.b) + abs(g.b) + 1
    expected = sign(f.a - g.a) if f.a != g.a else sign(f.b - g.b)
    for offset in [0, 1, 2, 17, 1_000_000]:
        assert sign(f.at(bound + offset) - g.at(bound + offset)) == expected
        scalar_checks += 1

palette = tuple((d, Affine(a, b)) for d, a, b in
                product(range(2), range(-1, 2), range(-1, 2)))
families = [f for count in range(3) for f in product(palette, repeat=count)]
family_checks = 0
largest_bound = 0
for left, right in product(families, repeat=2):
    bound = source_bound(left, right)
    tighter = tail_cutoff(left, right)
    assert bound >= tighter
    largest_bound = max(largest_bound, bound)
    baseline = expand(at(left, tighter)) == expand(at(right, tighter))
    for offset in [0, 1, 21]:
        assert (expand(at(left, bound + offset)) ==
                expand(at(right, bound + offset))) == baseline
        family_checks += 1

source_pins = {}
for name in ['Agent102RunDefs.lean', 'Agent102AffineArithmetic.lean',
             'Agent102RunWord.lean', 'Agent102RunEndpoints.lean']:
    content = (REPO / 'proofs' / name).read_bytes()
    source_pins[name] = hashlib.sha256(content).hexdigest()
    (HERE / 'sources' / (name.removesuffix('.lean') + '.review-snapshot.lean')).write_bytes(content)

report = {
    'status': 'PASS', 'utc': datetime.now(timezone.utc).isoformat(),
    'python': platform.python_version(),
    'source_contract': 'compareCutoff f g = abs(f.intercept)+abs(g.intercept)+1',
    'scope': 'Finite Python controls and exact source snapshots; no Lean execution',
    'scalar_checks': scalar_checks, 'family_pairs': len(families) ** 2,
    'family_checks': family_checks, 'largest_bound': largest_bound,
    'source_sha256': source_pins,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'runtime_seconds': round(time.monotonic() - started, 3),
}
(HERE / 'source-cutoff-controls-result.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
