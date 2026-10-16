#!/usr/bin/env python3
"""Finite controls for the all-width written neutral-exterior lemma."""
import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digits(n, b):
    ds = []
    while n:
        n, r = divmod(n, b)
        ds.append(r)
    return ds or [0]


def inspect(p, b):
    carry, ds = 0, []
    for coefficient in p:
        carry, digit = divmod(coefficient + carry, b)
        assert carry in (0, 1)
        ds.append(digit)
    overflow = carry == 1
    if carry:
        ds.append(carry)
    value = sum(x * b**i for i, x in enumerate(p))
    assert digits(value, b) == ds
    pairs = [x + y for x, y in zip(ds, reversed(ds))]
    witness = None
    if overflow:
        j = next(i for i, x in enumerate(p) if x != b-1)
        assert 1 <= j <= (len(p)-1)//2 and p[j] >= b
        assert ds[j] == p[j]-b and ds[len(p)-j] == 0
        assert pairs[j] == p[j]-b <= b-2
        witness = j
    return [b, p, value, ds, pairs, overflow, witness]


def main():
    records = []
    for b in range(2, 11):
        for h in range(1, 5):
            for middle in itertools.product(range(2*b-1), repeat=h-1):
                half = [b-1, *middle]
                records.append(inspect(half + half[::-1], b))
        records.append(inspect([b-1], b))
        for h in (1, 2):
            for middle in itertools.product(range(2*b-1), repeat=h-1):
                half = [b-1, *middle]
                for center in range(2*b-1):
                    records.append(inspect(half + [center] + half[::-1], b))
    raw = (json.dumps({'columns': ['base', 'input', 'value', 'digits', 'pairs',
                                 'overflow', 'witness'], 'records': records},
                      separators=(',', ':')) + '\n').encode()
    packed = gzip.compress(raw, mtime=0)
    (HERE/'controls.json.gz').write_bytes(packed)
    report = {'result': 'PASS', 'cases': len(records),
              'overflow_cases': sum(r[5] for r in records),
              'scope': 'Finite controls; all-width lemma proved in NEUTRAL_EXTERIOR.md.',
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'compressed_sha256': hashlib.sha256(packed).hexdigest(),
              'compressed_bytes': len(packed),
              'raw_sha256': hashlib.sha256(raw).hexdigest(), 'raw_bytes': len(raw),
              'recovery': 'gzip -dc controls.json.gz > controls.json'}
    (HERE/'verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
