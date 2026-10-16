#!/usr/bin/env python3
"""Independent bounded controls for a quantified decimal image claim.

All checks here are finite controls, NOT a formal proof for all natural numbers.
Python 3 standard library only; deterministic with fixed seed.
"""
import hashlib
import json
import random
import sys
from pathlib import Path


def reverse_arithmetic(n: int) -> int:
    assert n > 0
    result = 0
    while n:
        result = result * 10 + n % 10
        n //= 10
    return result


def reverse_string(n: int) -> int:
    return int(str(n)[::-1])


def step(n: int) -> int:
    return n + reverse_arithmetic(n)


def candidate(k: int, residue: int, lead: int) -> int:
    assert k >= 1
    assert 0 <= residue < 10**k
    assert 1 <= lead <= 9
    return lead * 10**k + residue


def check() -> dict:
    checked_forward = 0
    checked_witnesses = 0
    rng = random.Random(11219620261016)

    # Independent decimal implementations and the necessary restriction.
    for n in range(1, 200001):
        rev = reverse_arithmetic(n)
        assert rev == reverse_string(n)
        lead = int(str(n)[0])
        assert 1 <= lead <= 9
        assert rev % 10 == lead
        for k in range(1, 5):
            p = 10**k
            a = n % p
            value = (n + rev) % 10
            assert value == (a + lead) % 10, (n, k, a, value)
            assert value != a % 10, (n, k, a, value)
            checked_forward += 1

    coverages = {}
    for k in range(1, 7):
        p = 10**k
        if k <= 3:
            residues = list(range(p))  # complete residue sets for 10, 100, 1000
        else:
            residues = sorted(set([0, 1, 9, 10, p//2, p-2, p-1] +
                                  [rng.randrange(p) for _ in range(150)]))
        for a in residues:
            image = set()
            for c in range(1, 10):
                m = candidate(k, a, c)
                assert m % p == a
                assert int(str(m)[0]) == c
                assert reverse_arithmetic(m) % 10 == c
                observed = step(m) % 10
                assert observed == (a + c) % 10
                image.add(observed)
                checked_witnesses += 1
            assert image == set(range(10)) - {a % 10}, (k, a, image)
            assert len(image) == 9
        coverages[str(k)] = len(residues)

    # K>=1 is essential; at K=0 the residue-0 claim would be false.
    assert 19 % (10**0) == 0 and step(19) % 10 == 0
    # a<10^K is essential for the asserted raw remainder value.
    assert not (123 % 10 == 10)

    script = Path(__file__).read_bytes()
    return {
        "status": "FINITE_CONTROLS_PASS_NOT_A_LEAN_PROOF",
        "python_version": sys.version.split()[0],
        "random_seed": 11219620261016,
        "ordinary_inputs_checked": 200000,
        "forward_mod10_checks": checked_forward,
        "constructed_witness_checks": checked_witnesses,
        "residues_tested_by_k": coverages,
        "reverse_implementations": ["base10_arithmetic", "decimal_string"],
        "negative_controls": ["k=0 fails excluded-residue assertion", "raw a>=10^k has no preimage"],
        "sha256_of_this_checker": hashlib.sha256(script).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))