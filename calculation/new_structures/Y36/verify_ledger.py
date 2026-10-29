#!/usr/bin/env python3
"""Independent true-integer/digit-array controls for the p8 rec0 E/J ledger.

Run: python3 calculation/new_structures/Y36/verify_ledger.py
Only the Python standard library is used. This verifies representative
variant-2 entries and T14's 160/240/320 checkpoints. The exhaustive finite
packet counts for up to four edits are produced by exhaustive.cpp.
"""
import sys
sys.set_int_max_str_digits(1_000_000)

B39 = [17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W0 = [17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
V7 = [9,11,5,1,15,17,5,1,7,4,15,0,17,16,18,11,15,4,6,3]
J0 = [18,0,1,1]
C = [5,5]

# The 1-based emitter-list entries congruent to 2 mod 4.
VARIANTS = [
    ("E", 1, 3, 12),
    ("E", 5, 11, 2),
    ("E", 9, 1, 10),
    ("E", 13, 3, 12),
    ("E", 17, 9, 18),
    ("J", 0, 18, 9),
]


def template_pairword(q, k, E, J):
    half = B39 + W0 * q + E + J + V7 * k
    return half + C + half[::-1]


def pairword(d):
    return [d[i] + d[-1-i] for i in range(len(d))]


def source_digits(P):
    """Construct a canonical decimal N whose digit-pairword is P."""
    assert len(P) % 2 == 0 and P == P[::-1]
    d = [0] * len(P)
    for i in range(len(P) // 2):
        low = min(P[i], 9)
        d[i] = low
        d[-1-i] = P[i] - low
    assert d[-1] > 0 and all(0 <= x <= 9 for x in d)
    assert pairword(d) == P
    return d


def step_digits(d):
    """Schoolbook N + reverse(N), with digits stored least-significant first."""
    out = []
    carry = 0
    for i, x in enumerate(d):
        z = x + d[-1-i] + carry
        out.append(z % 10)
        carry = z // 10
    if carry:
        out.append(carry)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def int_from_digits(d):
    return int("".join(map(str, d[::-1])))


def digits_from_int(n):
    return list(map(int, str(n)[::-1]))


def max_word_run(half, word):
    n = len(half)
    matches = [False] * (n + 1)
    for i in range(n - len(word) + 1):
        matches[i] = half[i:i+len(word)] == word
    run = [0] * (n + len(word) + 1)
    best = (0, None)
    for i in range(n - 1, -1, -1):
        if matches[i]:
            run[i] = 1 + run[i + len(word)]
        if run[i] > best[0]:
            best = (run[i], i)
    return best


def replay(q, k, variant, steps):
    E, J = W0.copy(), J0.copy()
    if variant is not None:
        side, i, old, new = variant
        assert (E if side == "E" else J)[i] == old
        (E if side == "E" else J)[i] = new
    P0 = template_pairword(q, k, E, J)
    d = source_digits(P0)
    n = int_from_digits(d)
    assert digits_from_int(n) == d
    assert pairword(d) == P0
    gamma = []
    p1 = None
    checkpoints = {}
    for t in range(steps + 1):
        if t == 1:
            p1 = pairword(d)
        if t in (160, 240, 320):
            pw = pairword(d)
            half = pw[:len(pw)//2]
            count = q + 1 if t in (160, 240) else q + 2
            target = B39 + W0 * count
            first_mismatch = next(
                (i for i in range(min(len(pw), len(target))) if pw[i] != target[i]),
                None,
            )
            checkpoints[t] = {
                "prefix_match": first_mismatch is None and len(pw) >= len(target),
                "first_mismatch": first_mismatch,
                "offset_from_cut": None if first_mismatch is None else first_mismatch-len(target),
                "v7_run": max_word_run(half, V7)[0],
                "half_length": len(half),
                "overflows": sum(gamma[:t]),
            }
        if t == steps:
            break
        # Independent implementation 1: actual arbitrary-precision integer.
        s = str(n)
        assert s == "".join(map(str, d[::-1]))
        n_next = n + int(s[::-1])
        # Independent implementation 2: schoolbook digit-vector arithmetic.
        d_next = step_digits(d)
        assert d_next == digits_from_int(n_next), (q, k, variant, t)
        gamma.append(int(len(d_next) > len(d)))
        n, d = n_next, d_next
    return p1, checkpoints


def main():
    all_ok = True
    for q in (20, 40, 80, 160):
        k = q
        base_p1, base_cp = replay(q, k, ("E", 9, 1, 10), 320)
        for variant in VARIANTS:
            p1, cp = replay(q, k, variant, 160)
            same = p1 == base_p1
            expected = variant[0] == "E" and variant[1] in (1, 5, 9, 13)
            got = cp[160]
            ok = (
                same == expected
                and got["prefix_match"] == expected
                and got["v7_run"] == k - 8
                and got["overflows"] == 80
            )
            all_ok &= ok
            print(
                f"q=k={q} {variant}: first-successor-equivalent={same}; "
                f"W20-prefix={got['prefix_match']}; V7-run={got['v7_run']}; "
                f"overflows={got['overflows']}; {'PASS' if ok else 'FAIL'}"
            )
        for t in (160, 240, 320):
            c = base_cp[t]
            print(
                f"T14 q=k={q} t={t}: W-prefix={c['prefix_match']}; "
                f"mismatch-offset={c['offset_from_cut']}; V7-run={c['v7_run']}; "
                f"overflows={c['overflows']}"
            )
    assert all_ok
    print("ALL INDEPENDENT INTEGER / DIGIT-ARRAY CONTROLS PASSED")


if __name__ == "__main__":
    main()
