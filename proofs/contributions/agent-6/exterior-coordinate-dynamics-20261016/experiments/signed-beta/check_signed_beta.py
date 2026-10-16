#!/usr/bin/env python3
"""Independent finite controls for Agent6's signed exterior-coordinate law.

Literal map: P196.Agent7.Finite.outerNext from OuterFinite.lean,
SHA256 3376873da457c698850f604ddda82aeba3e67f4196e5c33d8142bed945c5f3f6.
Coordinate law is checked independently against scans, not used to advance.
These controls are finite experiments, not Lean proofs or cycle exclusions.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import random
import time

PHASES = (2, 4, 6, 8, 10, 12, 14, 16)


def normalize(word, carry):
    digits = []
    for x in word:
        carry, digit = divmod(x + carry, 10)
        digits.append(digit)
    return digits, carry


def outer_next(c, word):
    k = int(c >= 10)
    t = max(c - 9 * k, 0)
    left, carry_left = normalize(word, 0)
    right, gamma = normalize(reversed(word), k)
    u = max(c + carry_left - 10 * k, 0)
    other = list(reversed(right)) + [t] if gamma == 0 else [1] + list(reversed(right))
    raw = [a + b for a, b in zip(left + [u], other)]
    while raw and raw[-1] == 2 * t:
        raw.pop()
    return 2 * t, tuple(raw)


def low(word):
    return sum(x * 10**i for i, x in enumerate(word))


def high(word):
    acc = 0
    for x in word:
        acc = 10 * acc + x
    return acc


def reverse_digits(n, value):
    result = 0
    for _ in range(n):
        value, digit = divmod(value, 10)
        result = 10 * result + digit
    return result


def beta_num(c, word):
    return 9 * low(word) - c * 10**len(word)


def rho_num(c, word):
    return 9 * high(word) + c


def increment(c, word):
    n, k = len(word), int(c >= 10)
    denominator = 10**n
    t = max(c - 9 * k, 0)
    x = high(word) + k
    rev = reverse_digits(n, x)
    if x // denominator == 0:
        return 9 * rev - t * denominator
    return 9 + 90 * rev - 10 * t * denominator


def record(c, word):
    denominator = 10**len(word)
    nxt = outer_next(c, word)
    gamma = normalize(reversed(word), int(c >= 10))[1]
    rho = Fraction(rho_num(c, word), 9 * denominator)
    return {
        "c": c, "word": list(word), "next_c": nxt[0], "next_word": list(nxt[1]),
        "beta_num": beta_num(c, word), "next_beta_num": beta_num(*nxt),
        "increment": increment(c, word), "gamma": gamma,
        "rho": str(rho), "rho_floor": rho.numerator // rho.denominator,
        "rho_at_least_one": rho >= 1,
    }


def check_one(c, word):
    nxt = outer_next(c, word)
    delta = increment(c, word)
    assert beta_num(*nxt) == beta_num(c, word) + delta, record(c, word)
    k = int(c >= 10)
    gamma = normalize(reversed(word), k)[1]
    denominator = 10**len(word)
    if c // 9 == k:
        assert gamma == rho_num(c, word) // (9 * denominator), record(c, word)
        assert (gamma != 0) == (9 * denominator <= rho_num(c, word)), record(c, word)
        if all(x <= 18 for x in word):
            assert gamma <= 1, record(c, word)
            assert (gamma == 1) == (9 * denominator <= rho_num(c, word)), record(c, word)
    if c in PHASES:
        assert delta != 0, record(c, word)
        assert delta % 9 == (-c) % 9, record(c, word)
    return gamma


def main():
    started = time.time()
    counts = {"exhaustive_states": 0, "random_unbounded_states": 0, "gamma_gt_one": 0}
    for length in range(4):
        for word in product(range(19), repeat=length):
            for c in range(41):
                gamma = check_one(c, word)
                counts["exhaustive_states"] += 1
                counts["gamma_gt_one"] += gamma > 1
    rng = random.Random(196006)
    for _ in range(10000):
        c = rng.randrange(301)
        word = tuple(rng.randrange(201) for _ in range(rng.randrange(21)))
        gamma = check_one(c, word)
        counts["random_unbounded_states"] += 1
        counts["gamma_gt_one"] += gamma > 1

    telescopes = []
    for c in PHASES:
        for word in ((), (1,), (3,), (10,), (13,), (2, 17), (9, 1), (9, 11, 5)):
            initial = c, word
            state, summed = initial, 0
            for steps in range(1, 25):
                summed += increment(*state)
                state = outer_next(*state)
                assert state[0] in PHASES
                assert summed == beta_num(*state) - beta_num(*initial)
            telescopes.append({"initial": [c, list(word)], "steps": 24,
                               "endpoint": [state[0], list(state[1])], "signed_sum": summed})

    examples = [record(c, word) for c, word in (
        (2, (1,)), (2, (3,)), (2, (10,)), (2, (13,)),
        (9, (9,)), (18, ()), (2, (20,)), (0, (0,)),
        (6, (9, 1)), (6, (9, 11, 5)),
    )]
    result = {
        "status": "FINITE_CONTROLS_PASS", "not_a_lean_proof": True,
        "source_pin": "fba03a902e0f6b198cbf8f42efa8d11f8f2ba7a6",
        "original_map_sha256": "3376873da457c698850f604ddda82aeba3e67f4196e5c33d8142bed945c5f3f6",
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "exhaustive_domain": "0<=c<=40; 0<=length<=3; every coefficient in0..18; no canonicality filter",
        "random_domain": "10000 samples; seed196006; 0<=c<=300; 0<=length<=20; coefficients in0..200",
        "counts": counts, "telescoped_segments": len(telescopes), "segment_length": 24,
        "examples": examples, "telescopes": telescopes,
        "seconds": round(time.time() - started, 3),
    }
    path = Path(__file__).with_name("signed-beta-controls.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "counts", "telescoped_segments", "seconds", "examples")}, indent=2))


if __name__ == "__main__":
    main()
