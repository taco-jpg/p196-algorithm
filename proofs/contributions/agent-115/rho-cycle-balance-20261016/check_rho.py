#!/usr/bin/env python3
"""Exact finite controls for Agent115 high-real-coordinate balance (WIP theorem).

Faithful independent implementation of P196.Agent7.Finite.outerNext,
using Python arbitrary integers and Fraction, not output from Lean sources.
This is a finite test and is NOT proof of the universal statement.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path
import random
import sys

PHASES = (2, 4, 6, 8, 10, 12, 14, 16)


def normalize(word: tuple[int, ...], incoming: int) -> tuple[tuple[int, ...], int]:
    digits = []
    carry = incoming
    for x in word:
        digits.append((x + carry) % 10)
        carry = (x + carry) // 10
    return tuple(digits), carry


def low_value(word: tuple[int, ...]) -> int:
    return sum(x * 10**i for i, x in enumerate(word))


def high_value(word: tuple[int, ...]) -> int:
    out = 0
    for x in word:
        out = 10 * out + x
    return out


def fixed_reverse(n: int, value: int) -> int:
    return sum(((value // (10**i)) % 10) * (10 ** (n-i-1)) for i in range(n))


def literal_outer_next(c: int, word: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    """Exact line-by-line translation of OuterFinite.outerNext."""
    k = 1 if c >= 10 else 0
    t = c - 9*k
    ldigits, lcarry = normalize(word, 0)
    rdigits, rcarry = normalize(word[::-1], k)
    u = c + lcarry - 10*k
    right = rdigits[::-1] + (t,) if rcarry == 0 else (1,) + rdigits[::-1]
    raw = tuple(x + y for x, y in zip(ldigits + (u,), right))
    cprime = 2*t
    while raw and raw[-1] == cprime:
        raw = raw[:-1]
    return cprime, raw


def rho(c: int, word: tuple[int, ...]) -> Fraction:
    return Fraction(9 * high_value(word) + c, 9 * 10**len(word))


def phi(c: int, word: tuple[int, ...]) -> tuple[int, Fraction]:
    n = len(word)
    D = 10**n
    k = 1 if c >= 10 else 0
    t = c - 9*k
    V = low_value(word)
    H = high_value(word)
    u = c + V//D - 10*k
    gamma = (H+k)//D
    psi = Fraction(90*fixed_reverse(n,V) + 9*u + t, 90*D)
    return gamma, psi


def one_case(c: int, word: tuple[int, ...]):
    assert c in PHASES
    assert all(0 <= x <= 18 for x in word)
    gamma, psi = phi(c, word)
    assert gamma in (0,1), (c, word, gamma)
    assert psi > 0, (c, word, psi)
    nxt = literal_outer_next(c, word)
    actual = rho(*nxt)
    predicted = psi + (rho(c,word) if gamma == 0 else rho(c,word)/10)
    assert actual == predicted, (c, word, nxt, actual, predicted)
    assert all(0 <= x <= 18 for x in nxt[1])
    return gamma, psi, nxt


def main():
    rng = random.Random(11520261016)
    sha = hashlib.sha256()
    ncases = 0
    gamma_counts = [0,0]
    ncanonical = 0
    examples = {}
    for n in range(4):
        for c in PHASES:
            for word in product(range(19), repeat=n):
                if n and (word[0] == 0 or word[-1] == c):
                    continue
                gamma, psi, nxt = one_case(c,word)
                sha.update((str((c,word,gamma,nxt))+"\n").encode())
                ncases += 1
                ncanonical += 1
                gamma_counts[gamma] += 1
                label = f'length{n}_gamma{gamma}'
                if label not in examples:
                    examples[label] = {'c':c, 'B':list(word), 'next_c':nxt[0], 'next_B':list(nxt[1]),
                                       'rho_before':str(rho(c,word)), 'rho_after':str(rho(*nxt)),
                                       'psi':str(psi)}
    random_cases = 7000
    invalid_cases = 0
    for _ in range(random_cases):
        n = rng.randint(0,52)
        c = rng.choice(PHASES)
        word = tuple(rng.randrange(19) for _ in range(n))
        if n and (word[0] == 0 or word[-1] == c):
            invalid_cases += 1
        gamma, psi, nxt = one_case(c,word)
        sha.update((str((c,word,gamma,nxt))+"\n").encode())
        ncases += 1
        gamma_counts[gamma] += 1
    # Independent finite-orbit telescope: no assumption of a return is made.
    orbit_trials = 500
    orbit_edges = 0
    for _ in range(orbit_trials):
        n = rng.randint(0,18)
        c = rng.choice(PHASES)
        B = tuple(rng.randrange(19) for _ in range(n))
        start = rho(c,B)
        psis = Fraction(0)
        overflow_rhos = Fraction(0)
        for j in range(16):
            gamma, psi, nxt = one_case(c,B)
            orbit_edges += 1
            psis += psi
            if gamma:
                overflow_rhos += rho(c,B)
            c,B = nxt
            assert rho(c,B) - start == psis - Fraction(9,10)*overflow_rhos
    report = {
      'evidence_label':'exact finite Python controls; NOT Lean proof',
      'original_map':'P196.Agent7.Finite.outerNext',
      'phases': list(PHASES),
      'exhaustive_canonical_max_length':3,
      'exhaustive_canonical_count':ncanonical,
      'sampled_noncanonical_inputs':invalid_cases,
      'seed':11520261016,
      'random_cases':random_cases,
      'cases_total':ncases,
      'high_carry_counts':{'0':gamma_counts[0],'1':gamma_counts[1]},
      'failed_cases':0,
      'literal_case_stream_sha256':sha.hexdigest(),
      'finite_telescope_trials':orbit_trials,
      'finite_telescope_edges':orbit_edges,
      'finite_telescope_mismatches':0,
      'selected_examples':examples,
      'python_version':sys.version.split(' ')[0]
    }
    dest = Path(__file__).parent/'evidence'/'controls.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('selected_examples',)},indent=2))

if __name__ == '__main__':
    main()
