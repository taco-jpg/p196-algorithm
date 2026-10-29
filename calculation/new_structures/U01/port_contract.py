#!/usr/bin/env python3
"""Exact all-q one-step port contract for the rooted decimal p8/m48 band.

This is a missing-lemma reduction only: it does not exhibit a centre family,
closed template cycle, or decimal Lychrel number. Uses standard library only.
"""
from __future__ import annotations
import json
import random
import sys
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "p8m48_inputs.json").read_text())
B = tuple(tuple(row) for row in DATA["B"])
W = tuple(tuple(row) for row in DATA["W"])
G = tuple(int(ch) for ch in DATA["overflow"])
EXPECTED_PORT = ((0, 1), (0,), (0, 1), (1,), (0, 1), (1,), (0, 1), (1,))

assert len(B) == len(W) == len(G) == 8
assert all(len(row) == 11 for row in B)
assert all(len(row) == 48 for row in W)
assert all(0 <= x <= 18 for row in B + W for x in row)


def cyclic_carries(w: tuple[int, ...], direction: int) -> list[int]:
    """Exact cyclic carries A (direction=+1) or D (direction=-1)."""
    m = len(w)
    i0 = next(i for i, x in enumerate(w) if x != 9)
    c = [0] * m
    c[(i0 + direction) % m] = int(w[i0] >= 10)
    for s in range(1, m):
        i = (i0 + direction * s) % m
        j = (i + direction) % m
        c[j] = (w[i] + c[i]) // 10
    return c


def phi(w: tuple[int, ...], gamma: int) -> tuple[int, ...]:
    a = cyclic_carries(w, +1)
    d = cyclic_carries(w, -1)
    lo = [(w[i] + a[i]) % 10 for i in range(len(w))]
    hi = [(w[i] + d[i]) % 10 for i in range(len(w))]
    m = len(w)
    return tuple(lo[i] + (hi[(i - 1) % m] if gamma else hi[i]) for i in range(m))


def transfer(states, src, dst, gamma):
    """Folded two-ended carry transfer, including gamma=1's lag digit.

    State: (low carry, high outgoing carry, previous high digit,
            mismatch count capped at 2, age since last mismatch capped at 2).
    """
    states = frozenset(states)
    for x, want in zip(src, dst):
        nxt = set()
        for low, hi, prev, nbad, age in states:
            for inner in (0, 1):
                if (x + inner) // 10 != hi:
                    continue
                ld = (x + low) % 10
                ud = (x + inner) % 10
                got = ld + (ud if gamma == 0 else (1 if prev is None else prev))
                wrong = got != want
                count = min(2, nbad + int(wrong))
                newage = 0 if wrong else min(2, age + 1)
                nxt.add(((x + low) // 10, inner, ud, count, newage))
        states = frozenset(nxt)
    return states


def port_table():
    rows = []
    for t in range(8):
        assert phi(W[t], G[t]) == W[(t + 1) % 8], f"bulk row-cycle failure at phase {t}"
        start = {(0, G[t], None, 0, 2)}
        after_b = transfer(start, B[t], B[(t + 1) % 8], G[t])
        assert len(after_b) == 2, (t, after_b)
        after_w = transfer(after_b, W[t], W[(t + 1) % 8], G[t])
        after_second_w = transfer(after_w, W[t], W[(t + 1) % 8], G[t])
        assert after_w == after_second_w, f"band transfer not idempotent at phase {t}"
        good = tuple(sorted({s[1] for s in after_w if s[3] == 0}))
        assert good == EXPECTED_PORT[t], (t, good, EXPECTED_PORT[t])
        for s in after_w:
            if s[1] in good:
                assert s[3] == 0
            else:
                assert s[3] == 1 and s[4] == 0, (t, s)
        rows.append((t, G[t], good, len(after_w)))
    return rows


def decimal_from_pairs(P: tuple[int, ...]) -> str:
    assert P == P[::-1]
    n = len(P)
    h = n // 2
    high = [min(9, x) for x in P[:h]]
    low = [P[i] - high[i] for i in range(h)]
    middle = [] if n % 2 == 0 else [P[h] // 2]
    assert n % 2 == 0 or P[h] % 2 == 0
    digits = low + middle + high[::-1]  # least-significant first
    assert digits[-1] > 0
    return "".join(str(d) for d in reversed(digits))


def actual_carries(P: tuple[int, ...]) -> list[int]:
    c = [0]
    for x in P:
        c.append((x + c[-1]) // 10)
    return c


def pairword_of_integer(n: int) -> tuple[int, ...]:
    s = str(n)
    return tuple(int(s[-1 - i]) + int(s[i]) for i in range(len(s)))


def bigint_controls():
    """True Python-integer N+reverse(N) checks at q=20/40/80/160 plus small q."""
    rng = random.Random(20261028)
    counts = {(t, u): 0 for t in range(8) for u in (0, 1)}
    cases = 0
    widths = (1, 2, 3, 5, 8, 20, 40, 80, 160)
    for t in range(8):
        for q in widths:
            reps = 20 if q <= 8 else 8
            for j in range(reps):
                left = tuple(rng.randrange(19) for _ in range(j % 9))
                center = left + (() if j % 2 else (2 * rng.randrange(10),)) + left[::-1]
                hword = B[t] + W[t] * q
                P = hword + center + hword[::-1]
                source = decimal_from_pairs(P)
                n = int(source)
                out = n + int(source[::-1])  # genuine arbitrary-precision integer reverse-and-add
                out_s = str(out)
                Q = pairword_of_integer(out)
                gamma = len(out_s) - len(source)
                carries = actual_carries(P)
                assert gamma == G[t] == carries[-1], (t, q, gamma, carries[-1])
                u = carries[len(P) - len(hword)]
                expected_word = B[(t + 1) % 8] + W[(t + 1) % 8] * q
                mismatches = [i for i, (x, y) in enumerate(zip(Q, expected_word)) if x != y]
                if u in EXPECTED_PORT[t]:
                    assert not mismatches, (t, q, u, mismatches[:4])
                else:
                    assert mismatches == [len(hword) - 1], (t, q, u, mismatches[:8])
                counts[t, u] += 1
                cases += 1
    assert all(v > 0 for v in counts.values()), counts
    return cases, counts


if __name__ == "__main__":
    print("phase gamma allowed_center_carry states_after_band")
    for t, gamma, good, size in port_table():
        print(t, gamma, "{" + ",".join(map(str, good)) + "}", size)
    cases, counts = bigint_controls()
    print(f"PASS: exact carry-state induction covers every q >= 1; {cases} bigint controls passed")
    print("PASS: every forbidden port produces exactly one mismatch at the last protected coefficient")
    print("Observed seam-carry counts:", {f"t{t}/u{u}": n for (t, u), n in counts.items()})
    print("NOT a full template return or a decimal Lychrel certificate.")
