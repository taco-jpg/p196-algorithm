#!/usr/bin/env python3
"""Independent finite controls, not an all-width proof or certificate search.

No author module is imported. Successor coefficients are obtained by normalizing
the complete symmetric column word, then pairing the actual output digits.
"""
from itertools import product
from pathlib import Path
import hashlib
import json
import random

HERE = Path(__file__).resolve().parent


def template(c, B, A, C, g=2, h=2):
    left = list(B) + [c] * g + list(A) + [18-c] * h
    return left + list(C) + left[::-1]


def normalize_whole(q):
    digits, carry = [], 0
    for coeff in q:
        carry, digit = divmod(coeff + carry, 10)
        digits.append(digit)
    if carry:
        digits.append(carry)
    return [a+b for a, b in zip(digits, digits[::-1])]


def raw_exterior(c, B, A=(), C=()):
    return normalize_whole(template(c, B, A, C))[:len(B)+1]


def phase_step(c):
    return 2 * (c if c < 10 else c-9)


def strip(c, B):
    B = list(B)
    while B and B[-1] == c:
        B.pop()
    return B


def exterior(c, B):
    return phase_step(c), strip(phase_step(c), raw_exterior(c, B))


def realize(q):
    assert q == q[::-1]
    digits = [0] * len(q)
    for i in range(len(q)//2):
        digits[i] = max(0, q[i]-9)
        digits[-1-i] = min(9, q[i])
    if len(q) % 2:
        assert q[len(q)//2] % 2 == 0
        digits[len(q)//2] = q[len(q)//2]//2
    assert digits[-1] > 0
    return sum(d * 10**i for i, d in enumerate(digits))


def pair_integer(n):
    digits = list(map(int, str(n)))[::-1]
    return [a+b for a, b in zip(digits, digits[::-1])]


def main():
    counts = dict(exhaustive_sources=0, phase_append_identities=0,
                  trim_invariance=0, positive_head_preserved=0,
                  literal_integer_controls=0, noncanonical_controls=0)
    phases = [c for c in range(1,18) if c != 9]
    for c in phases:
        for width in range(4):
            for values in product(range(19), repeat=width):
                B = list(values)
                base = raw_exterior(c, B)
                counts['exhaustive_sources'] += 1
                for j in (1,2):
                    assert raw_exterior(c, B+[c]*j) == base+[phase_step(c)]*j, (c,B,j)
                    counts['phase_append_identities'] += 1
                assert exterior(c, strip(c,B)) == exterior(c,B), (c,B)
                counts['trim_invariance'] += 1
                _, nextB = exterior(c,B)
                if not B or B[0] > 0:
                    assert not nextB or nextB[0] > 0, (c,B,nextB)
                    counts['positive_head_preserved'] += 1
                else:
                    counts['noncanonical_controls'] += 1

    rng = random.Random(11620261015)
    for _ in range(3000):
        c = rng.choice(phases)
        B = [rng.randrange(19) for _ in range(rng.randrange(9))]
        if B:
            B[0] = rng.randrange(1,19)
        A = [rng.randrange(19) for _ in range(rng.randrange(9))]
        center_half = [rng.randrange(19) for _ in range(rng.randrange(5))]
        C = center_half + ([2*rng.randrange(10)] if rng.randrange(2) else []) + center_half[::-1]
        g, h = rng.randrange(2,9), rng.randrange(2,9)
        q = template(c,B,A,C,g,h)
        n = realize(q)
        assert pair_integer(n) == q
        successor = n + int(str(n)[::-1])
        actual = pair_integer(successor)
        assert actual == normalize_whole(q)
        assert actual[:len(B)+1] == raw_exterior(c,B)
        c2 = phase_step(c)
        j = rng.randrange(1,7)
        q2 = template(c,B+[c]*j,A,C,g,h)
        n2 = realize(q2)
        actual2 = pair_integer(n2+int(str(n2)[::-1]))
        assert actual2[:len(B)+j+1] == actual[:len(B)+1]+[c2]*j
        counts['literal_integer_controls'] += 1

    noncanonical_path = []
    c, B = 2, [0]
    for _ in range(7):
        noncanonical_path.append({'c': c, 'B': B})
        c, B = exterior(c,B)
    assert len(noncanonical_path[5]['B']) == 2
    assert len(noncanonical_path[6]['B']) == 3
    result = {
        'status': 'PASS', 'evidence_kind': 'finite independent experiment',
        'counts': counts, 'exhaustive_domain': '1<=c<=17, c!=9; 0<=len(B)<=3; every entry 0..18',
        'identity': 'Br(c,B++c^j)=Br(c,B)++nextPhase(c)^j, tested j=1,2',
        'method': 'full symmetric column-word addition, no author functions imported',
        'literal_random_seed': 11620261015,
        'noncanonical_trajectory': noncanonical_path,
        'noncanonical_scope': 'initial state fails validOuter positive head; it exits cap2 at time6, and is not a cycle counterexample',
        'rejected_prior_claim': 'attempt01 incorrectly conjectured this trajectory closes after six steps; the independent arithmetic control rejected that claim',
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'all_width_proof': False, 'infinite_safe_orbit_or_p196': False,
    }
    (HERE/'independent_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
