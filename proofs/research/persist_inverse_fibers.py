"""Exact inverse transition tables and finite-horizon fiber maximization.

This validates a symbolic transfer-matrix argument; it is not a proof of
existence or nonexistence of decimal Lychrel numbers.
"""
from itertools import product
import json

STATES = tuple(product(range(2), repeat=2))


def matrix(s):
    out = [[0] * 4 for _ in range(4)]
    labels = []
    for j, (a, b) in enumerate(STATES):
        for q in range(19):
            ap, lo = divmod(q + a, 10)
            for bp in range(2):
                bh, hi = divmod(q + bp, 10)
                if bh == b and lo + hi == s:
                    k = STATES.index((ap, bp))
                    out[j][k] += 1
                    labels.append([list((a, b)), list((ap, bp)), q])
    return out, labels


def mul(v, matrix):
    return tuple(sum(v[i] * matrix[i][j] for i in range(4)) for j in range(4))


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def step_word(q):
    carry = 0
    digits = []
    for x in q:
        carry, digit = divmod(x + carry, 10)
        digits.append(digit)
    if carry:
        digits.append(carry)
    return tuple(a + b for a, b in zip(digits, reversed(digits))), carry


def produces_palindrome(q):
    return all(x <= 9 for x in q) or (q[0] == 11 and all(x in (0, 11) for x in q))


def admissible_words(length):
    for outer in range(1, 19):
        for tail in product(range(19), repeat=length // 2 - 1):
            half = (outer,) + tail
            for center in ([()] if length % 2 == 0 else [(c,) for c in range(0, 19, 2)]):
                yield half + center + half[::-1]


def main():
    tables = {s: matrix(s) for s in range(19)}
    E, O, M = (tables[s][0] for s in (2, 3, 9))
    for s in range(1, 18):
        assert tables[s][0] == (M if s == 9 else E if s % 2 == 0 else O)
    for s in (0, 18):
        assert all(tables[s][0][i][j] <= E[i][j] for i in range(4) for j in range(4))

    # Every table different from 0 and 18 is one of E,O,M. The exceptional
    # tables delete paths from E, so cannot improve any nonnegative count.
    # Symbols 2,3,9 realize E,O,M with positive initial q coefficient.
    reachable = {(1, 0, 0, 0)}
    dp = []
    for m in range(1, 13):
        reachable = {mul(v, A) for v in reachable for A in (E, O, M)}
        max_even = max(v[0] + v[3] for v in reachable)
        max_odd = max(max(v[0] + v[1], v[2] + v[3]) for v in reachable)
        assert max_even == max(1, fib(m - 1))
        row = {"half_width": m, "reachable_count_vectors": len(reachable),
               "even_width_max_fiber": max_even, "odd_width_max_fiber": max_odd}
        dp.append(row)
        print(row, flush=True)

    # Sharpness target (11,9,...,9,11), with an even width of 2m.
    sharpness = []
    for m in range(2, 31):
        v = mul((1, 0, 0, 0), tables[11][0])
        for _ in range(m - 1):
            v = mul(v, M)
        assert v[0] + v[3] == fib(m - 1)
        sharpness.append({"half_width": m, "fiber_size": v[0] + v[3]})
    protected = []
    for m in range(1, 11):
        for k in range(1, 11):
            half = (11,) + (9,) * m + (18,) * k
            target = half + half[::-1]
            v = (1, 0, 0, 0)
            for s in half:
                v = mul(v, tables[s][0])
            assert v[0] + v[3] == fib(m)
            q = target
            for _ in range(k):
                assert not produces_palindrome(q)
                q, _ = step_word(q)
            overflow_target = ((5,) + (10,) * m + (14,) + (18,) * (2 * k - 1)
                               + (14,) + (10,) * m + (5,))
            for choices in product((5, 14), repeat=m):
                left = (14,) + choices + (18,) * k
                image, carry = step_word(left + left[::-1])
                assert carry == 1 and image == overflow_target
            q = overflow_target
            for _ in range(k):
                assert not produces_palindrome(q)
                q, _ = step_word(q)
            protected.append({"free_pairs": m, "avoidance_horizon": k,
                              "no_overflow_fiber": fib(m), "overflow_family": 2 ** m})
    overflow_maxima = []
    for length in range(2, 9):
        counts = {}
        for q in admissible_words(length):
            target, carry = step_word(q)
            if carry:
                counts[target] = counts.get(target, 0) + 1
        actual = max(counts.values())
        assert actual == 2 ** (length // 2 - 1)
        overflow_maxima.append({"input_width": length, "maximum_fiber": actual})
    local_overflow_cases = 0
    for p, a, b, s in product(range(19), range(2), range(2), range(19)):
        if not p // 10 <= a <= (p + 1) // 10:
            continue
        candidates = []
        for x, bp in product(range(19), range(2)):
            if not x // 10 <= bp <= (x + 1) // 10:
                continue
            ap, low_digit = divmod(x + a, 10)
            bh, high_digit = divmod(p + bp, 10)
            if bh == b and low_digit + high_digit == s:
                candidates.append((x, ap, bp))
        assert len(candidates) <= 2
        if len(candidates) == 2:
            assert abs(candidates[0][0] - candidates[1][0]) == 9
        local_overflow_cases += 1
    result = {"state_order": STATES, "tables": tables, "exact_dp": dp,
              "non_palindrome_producing_sharpness": sharpness,
              "protected_central_block_families": protected,
              "overflow_exhaustive_maxima": overflow_maxima,
              "overflow_local_cases": local_overflow_cases}
    with open("persist_inverse_fibers_results.json", "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
