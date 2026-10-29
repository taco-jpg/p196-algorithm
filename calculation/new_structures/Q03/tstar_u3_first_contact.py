#!/usr/bin/env python3
"""Exact T* first-contact gates for rooted decimal p12/m9 W9/U3.

Run from repository root:
    python3 calculation/new_structures/Q03/tstar_u3_first_contact.py

This checks all 30 charge-zero U3 motifs and all 120 actual temporal phases.
It does not search for a full seam return or claim a decimal Lychrel number.
"""
from collections import Counter
from pathlib import Path
import sys

sys.set_int_max_str_digits(100_000)
ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
rows = [list(map(int, line.split())) for line in DATA.read_text().splitlines()]
assert rows[0] == [12, 34, 9, 10] and rows[1] == [1, 0, 0, 0] * 3
W, B = [tuple(r) for r in rows[2:14]], [tuple(r) for r in rows[26:38]]
assert len(W) == len(B) == 12 and all(len(w) == 9 for w in W) and all(len(b) == 34 for b in B)

def carry(x, c):
    return int(x + c >= 10)

def periodic_carries(word):
    """Unique physical low/reverse carries for a cyclic word containing a non-9."""
    m = len(word)
    assert any(x != 9 for x in word)
    z = 0
    for _ in range(2):
        for x in word:
            z = carry(x, z)
    low = [0] * m
    low[0] = z
    for i in range(1, m):
        low[i] = carry(word[i - 1], low[i - 1])
    z = 0
    for _ in range(2):
        for x in reversed(word):
            z = carry(x, z)
    high = [0] * m
    high[0] = z
    for i in range(m - 1, 0, -1):
        high[i] = carry(word[i], high[(i + 1) % m])
    assert all(carry(word[i], low[i]) == low[(i + 1) % m] for i in range(m))
    assert all(carry(word[i], high[(i + 1) % m]) == high[i] for i in range(m))
    return low, high

def bulk_step(word, overflow):
    low, high = periodic_carries(word)
    m = len(word)
    return tuple((word[i] + low[i]) % 10
                 + ((word[i] + high[(i + 1) % m]) % 10 if not overflow
                    else (word[i - 1] + high[i]) % 10)
                 for i in range(m))

def source_number(p):
    """Canonical decimal integer realizing a symmetric pair-coefficient word."""
    assert p == p[::-1] and p[0] > 0 and all(0 <= x <= 18 for x in p)
    n, d = len(p), [0] * len(p)  # digits LSD first
    for i in range(n // 2):
        d[i], d[n - 1 - i] = max(0, p[i] - 9), min(9, p[i])
    if n % 2:
        assert p[n // 2] % 2 == 0
        d[n // 2] = p[n // 2] // 2
    assert d[-1] > 0
    return int("".join(map(str, reversed(d))))

def reverse_add_bigint(n):
    return n + int(str(n)[::-1])

def reverse_add_digits(n):
    """Independent schoolbook digit-array reverse-and-add."""
    d = list(map(int, str(n)[::-1]))
    out, c = [], 0
    for i, x in enumerate(d):
        s = x + d[-1 - i] + c
        out.append(s % 10)
        c = s // 10
    if c:
        out.append(c)
    return int("".join(map(str, reversed(out))))

def pairword_of(n):
    s = str(n)
    return [int(s[-1 - i]) + int(s[i]) for i in range(len(s))]

def full_carries(p):
    c = [0]
    for x in p:
        c.append(carry(x, c[-1]))
    return c

# Universal Q03 first-contact theorem, gamma=0:
# (q,q',cL,cU) = (4,9,1,0),(9,4,1,0),(9,14,0,1),(14,9,0,1).
NO_OVERFLOW_GATES = {(4, 1, 0): 9, (9, 1, 0): 4,
                     (9, 0, 1): 14, (14, 0, 1): 9}

def first_contact_gate(overflow, q, c_low, c_high, left_neighbor):
    """Only replacement compatible with the exact universal prefix gate, if any."""
    if not overflow:
        return NO_OVERFLOW_GATES.get((q, c_low, c_high))
    if left_neighbor == 9:  # gamma=1 requires the immediately outer coefficient != 9
        return None
    # The lower perturbation's carry difference is reset before reaching its mirror,
    # so the physical incoming carry at the upper changed cell is unchanged.
    if q == 0:
        return 9 if c_low == c_high == 1 else None
    if 1 <= q <= 8:
        return q + 9
    if q == 9:
        if c_low == c_high == 0:
            return 18
        if c_low == c_high == 1:
            return 0
        return None
    if 10 <= q <= 17:
        return q - 9
    if q == 18:
        return 9 if c_high == 0 else None
    return None

def all_u_motifs():
    for a in range(0, 19, 2):
        base = (9, a, 18 - a)
        for r in range(3):
            yield base[r:] + base[:r]

def phase_rows(u):
    result, v = [tuple(u)], tuple(u)
    for t in range(120):
        v = bulk_step(v, int(t % 4 == 0))
        result.append(v)
    assert result[-1] == tuple(u)
    return result

def main():
    motifs = list(all_u_motifs())
    assert len(motifs) == len(set(motifs)) == 30
    motif_set = set(motifs)
    gate_count, signed_count, motif_signed_count = Counter(), Counter(), Counter()
    physical_rows = tested_edits = tested_ports = 0

    for initial in motifs:
        states = phase_rows(initial)
        assert all(v in motif_set for v in states)
        assert all(sum(v) == 27 and v.count(9) == 1
                   and all(x % 2 == 0 for x in v if x != 9) for v in states)
        for t, word in enumerate(states[:-1]):
            overflow = int(t % 4 == 0)
            low, high = periodic_carries(word)
            eligible = []
            for r, q in enumerate(word):
                rep = first_contact_gate(overflow, q, low[r],
                                         high[(r + 1) % 3], word[(r - 1) % 3])
                if rep is not None:
                    eligible.append((r, q, rep, low[r], high[(r + 1) % 3]))
            assert len(eligible) == 1, (initial, t, word, eligible)
            r_gate, q_gate, replacement, cL, cU = eligible[0]
            if overflow:
                assert word[(r_gate + 1) % 3] == 9 and word[(r_gate - 1) % 3] != 9
                assert q_gate % 2 == 0 and abs(replacement - q_gate) == 9
                assert (cL, cU) == ((1, 1) if q_gate <= 8 else (0, 0))
                assert replacement == (q_gate + 9 if q_gate <= 8 else q_gate - 9)
            else:
                assert q_gate == 9 and replacement in (4, 14)
                assert (cL, cU) == ((1, 0) if replacement == 4 else (0, 1))

            # A genuine canonical phase-local source. These are not asserted to
            # be consecutive states of one orbit; only the local gate is tested.
            J, C, q_bands, k_bands = (5,), (10,), 14, 100
            H = list(B[t % 12]) + list(W[t % 12]) * q_bands + list(J) + list(word) * k_bands
            p = H + list(C) + H[::-1]
            n = source_number(p)
            successor = reverse_add_bigint(n)
            assert successor == reverse_add_digits(n)
            baseline_pair = pairword_of(successor)
            assert len(baseline_pair) == len(p) + overflow
            c_full = full_carries(p)
            u_start = len(B[t % 12]) + 9 * q_bands + len(J)
            copy_index = 40
            for rr in range(3):
                j = u_start + 3 * copy_index + rr
                j_reflect = len(p) - 1 - j
                assert c_full[j] == low[rr]
                assert c_full[j_reflect] == high[(rr + 1) % 3]
                tested_ports += 1
                old = p[j]
                low_digit, high_digit = max(0, old - 9), min(9, old)
                for delta in ((-5, 5) if not overflow else (-9, 9)):
                    new = old + delta
                    if not 0 <= new <= 18:
                        continue
                    n2 = n + (max(0, new - 9) - low_digit) * 10**j
                    n2 += (min(9, new) - high_digit) * 10**j_reflect
                    assert len(str(n2)) == len(p)
                    out2 = reverse_add_bigint(n2)
                    assert out2 == reverse_add_digits(n2)
                    pair2 = pairword_of(out2)
                    assert len(pair2) == len(baseline_pair)
                    matches = baseline_pair[:j + 1] == pair2[:j + 1]
                    should_match = (rr == r_gate and new == replacement)
                    assert matches == should_match, (
                        initial, t, word, rr, old, new, eligible, matches, should_match)
                    if should_match:
                        support = [i for i, (a, b) in enumerate(zip(baseline_pair, pair2)) if a != b]
                        if not overflow:
                            sign = (new - old) // 5
                            expected = sorted((j + 1, j_reflect - 1))
                            assert support == expected
                            assert pair2[j + 1] - baseline_pair[j + 1] == sign
                            assert pair2[j_reflect - 1] - baseline_pair[j_reflect - 1] == sign
                        else:
                            sign = (new - old) // 9
                            expected = sorted((j + 1, j + 2, j_reflect - 1, j_reflect))
                            assert support == expected
                            assert pair2[j + 1] - baseline_pair[j + 1] == -10 * sign
                            assert pair2[j + 2] - baseline_pair[j + 2] == sign
                            assert pair2[j_reflect - 1] - baseline_pair[j_reflect - 1] == sign
                            assert pair2[j_reflect] - baseline_pair[j_reflect] == -10 * sign
                    tested_edits += 1
            physical_rows += 1
            gate_count[overflow] += 1
            signed_count[(overflow, replacement - q_gate)] += 1
            motif_signed_count[(initial, overflow, replacement - q_gate)] += 1

    assert physical_rows == 3600 and tested_ports == 10800
    assert gate_count == Counter({0: 2700, 1: 900})
    assert signed_count == Counter({(0, -5): 1350, (0, 5): 1350,
                                    (1, -9): 450, (1, 9): 450})
    for motif in motifs:
        assert motif_signed_count[(motif, 0, -5)] == 45
        assert motif_signed_count[(motif, 0, 5)] == 45
        assert motif_signed_count[(motif, 1, -9)] == 15
        assert motif_signed_count[(motif, 1, 9)] == 15
    print("PASS: 30 distinct U3 rotations x 120 phases = 3,600 interface rows")
    print("PASS: exactly one admissible first-contact site per phase")
    print("PASS: gamma=0: unique 9 -> 4 (ports 1,0) or 9 -> 14 (ports 0,1)")
    print("PASS: gamma=1: cell before 9; even q<=8 -> q+9 (ports 1,1), q>=10 -> q-9 (ports 0,0)")
    print("PASS: periodic carries match all", tested_ports, "actual contact ports")
    print("PASS: bigint and independent digit-array engines agree on", tested_edits, "candidate edits")
    print("PASS: each gate emits its exact reflected +/-1 or (opposite 10, unit) packet")
    print("PASS: gamma0 signs +/-5 each 1,350; gamma1 signs +/-9 each 450")
    print("SCOPE: all-width local necessity only; no full T* return or Lychrel certificate")

if __name__ == "__main__":
    main()
