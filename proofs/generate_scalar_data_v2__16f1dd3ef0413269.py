#!/usr/bin/env python3
"""Agent #103 v2 emitter for the frozen scalar job tables.

Data model: imported unchanged from the original
`2026-10-15-scalar-finite-certificate-formal/generate_scalar_data.py`
(`models()`, which pins and checks the source certificate SHA-256).
Only the Lean *representation* of each lookup table changes: instead of one
nested `if` term per table (up to ~600 KB on one line, which exceeded Lean's
default heartbeat budget for JobData8 and elaborates in roughly quadratic
time), each table is split into consecutive chunks of at most CHUNK entries.
Each chunk is its own small definition containing the same balanced
comparison tree on absolute indices, and a balanced dispatch tree on chunk
boundaries selects the chunk. Every table denotes the same function
Nat -> Nat as before (value at i for i < N, 0 otherwise). Soundness of the
final theorem does not depend on these values: all local conditions are
kernel-checked against whatever the tables contain.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
ORIGINAL = REPO / 'proofs/contributions/2026-10-15-scalar-finite-certificate-formal'
ORIGINAL_GENERATOR_SHA256 = None  # recorded at run time in generation_v2.json
CHUNK = 256

spec = importlib.util.spec_from_file_location('generate_scalar_data', ORIGINAL / 'generate_scalar_data.py')
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)


def tree(values, lo, hi):
    """Same balanced comparison tree as the original `array`, on absolute indices."""
    part = values[lo:hi]
    if not part:
        return '0'
    if all(v == part[0] for v in part):
        return str(part[0])
    mid = (lo + hi) // 2
    return f'(if i < {mid} then {tree(values, lo, mid)} else {tree(values, mid, hi)})'


def array(name, values):
    n = len(values)
    if n <= CHUNK:
        return f'def {name} (i : Nat) : Nat := if i < {n} then {tree(values, 0, n)} else 0\n'
    starts = list(range(0, n, CHUNK))
    out = ''
    for k, lo in enumerate(starts):
        hi = min(lo + CHUNK, n)
        out += f'def {name}_c{k} (i : Nat) : Nat := {tree(values, lo, hi)}\n'

    def dispatch(a, b):  # chunk index range [a, b)
        if b - a == 1:
            return f'{name}_c{a} i'
        m = (a + b) // 2
        return f'(if i < {starts[m]} then {dispatch(a, m)} else {dispatch(m, b)})'
    out += f'def {name} (i : Nat) : Nat := if i < {n} then {dispatch(0, len(starts))} else 0\n'
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, default=HERE / 'generated')
    args = ap.parse_args()
    original.array = array          # every emitted table uses the v2 representation
    data = original.models()        # pinned-source data model, unchanged
    args.output.mkdir(parents=True, exist_ok=True)
    inventory = []
    for identity in range(16):
        d = data[identity]; j = d['job']
        s = 'import JobCatalog\nnamespace ScalarJobData\nopen ScalarFinite\n'
        for name, values in [('meta', d['meta']), ('components', d['component']),
                             ('nextCodes', d['next']), ('ranks', j['weighted_sink_ranks'])]:
            s += array(f'{name}{identity}', values)
        s += f'def component{identity} (v : Nat) : Nat := components{identity} v\n'
        clauses = ''.join(f'if c={link["component"]} then {link["child_job"]+1} else ' for link in j['children'])
        s += f'def childCode{identity} (c : Nat) : Nat := ' + clauses + '0\n'
        s += f'''def data{identity} : Data where
  size := {len(d['meta'])}
  phase v := (meta{identity} v)%7
  last v := (meta{identity} v)/7%19
  low v := (meta{identity} v)/133
  next u bit := nextCodes{identity} (2*u+bit)

def ranking{identity} : Ranking where
  component := component{identity}
  cyclic c := decide (childCode{identity} c ≠ 0)
  weight c := if childCode{identity} c=0 then 1 else jobBound (childCode{identity} c-1)
  rank c := ranks{identity} c
  bound := jobBound {identity}
'''
        if 'lift' in d:
            lift = d['lift']
            s += array(f'members{identity}', lift['members'])
            s += array(f'inverse{identity}', lift['inverse'])
            s += f'def member{identity} (i : Nat) : Nat := members{identity} i\n'
            s += f'def memberIndex{identity} (u : Nat) : Nat := inverse{identity} u\n'
        s += 'end ScalarJobData\n'
        f = args.output / f'JobData{identity}.lean'
        f.write_text(s)
        inventory.append(dict(job=identity, vertices=len(d['meta']), bytes=len(s.encode()),
                              sha256=hashlib.sha256(s.encode()).hexdigest()))
    (args.output / 'generation_v2.json').write_text(json.dumps(dict(
        source_certificate_sha256=original.EXPECTED,
        original_generator_sha256=hashlib.sha256((ORIGINAL / 'generate_scalar_data.py').read_bytes()).hexdigest(),
        v2_generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        chunk=CHUNK, jobs=inventory,
        scope='Same table values as the original emitter, chunked representation; generated data is not a proof.'),
        indent=2) + '\n')
    print(json.dumps([(x['job'], x['bytes']) for x in inventory]))


if __name__ == '__main__':
    main()
