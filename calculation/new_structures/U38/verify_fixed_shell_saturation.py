#!/usr/bin/env python3
"""Controls for residue saturation with a fixed finite palindrome shell."""
from math import gcd
import random
import sys
sys.set_int_max_str_digits(0)


def order10(M: int) -> int:
    assert M > 1 and M % 2 == 1 and gcd(M, 10) == 1
    x, d = 10 % M, 1
    while x != 1:
        x = x * 10 % M
        d += 1
        if d > M:
            raise AssertionError("order search exceeded group bound")
    return d


def construct(M: int, residue: int, k: int, shell: list[int]) -> str:
    assert M > 1 and M % 2 == 1 and gcd(M, 10) == 1
    assert shell and 1 <= shell[0] <= 9 and all(0 <= x <= 9 for x in shell)
    residue %= M
    d, n, s = order10(M), (M - 1 + 8) // 9, len(shell)
    assert k >= d * n + s
    assert s <= k

    digits = [0] * (2 * k + 1)
    for i, x in enumerate(shell):
        digits[i] = digits[2 * k - i] = x
    digits[k] = 0
    fixed_residue = sum(x * (pow(10, i, M) + pow(10, 2 * k - i, M))
                        for i, x in enumerate(shell)) % M
    w = (2 * pow(10, k, M)) % M
    assert gcd(w, M) == 1
    t = ((residue - fixed_residue) * pow(w, -1, M)) % M
    assert 0 <= t <= M - 1 <= 9 * n

    remaining, chosen = t, []
    for m in range(1, n + 1):
        i = k - d * m
        assert s <= i <= k - 1
        x = min(9, remaining)
        digits[i] = digits[2 * k - i] = x
        remaining -= x
        chosen.append(i)
    assert remaining == 0 and len(set(chosen)) == n

    # Independent checks: canonical integer, palindrome/shell, and digit-array residue.
    dec = "".join(str(x) for x in reversed(digits))
    assert len(dec) == 2 * k + 1 and dec[0] != "0" and dec == dec[::-1]
    assert [int(dec[-1-i]) for i in range(s)] == shell
    value = int(dec)
    digit_residue = sum(x * pow(10, i, M) for i, x in enumerate(digits)) % M
    assert value % M == digit_residue == residue
    assert all((pow(10, i, M) + pow(10, 2*k-i, M)) % M == w for i in chosen)
    return dec


def main():
    rng = random.Random(38011)
    checks = 0
    cases = []
    for M, shells, exhaustive in [
        (11, [[1], [3, 0, 9], [8, 2, 0, 7]], True),
        (101, [[4, 7, 2]], True),
        (1001, [[6, 1, 0, 4]], True),
        (101101, [[9, 0, 4]], False),
    ]:
        d, n = order10(M), (M - 1 + 8) // 9
        for shell in shells:
            k = d * n + len(shell)
            residues = range(M) if exhaustive else [0, 1, M//2, M-1] + [rng.randrange(M) for _ in range(16)]
            for r in residues:
                construct(M, r, k, shell)
                checks += 1
            cases.append((M, len(shell), k, 2*k+1, "all" if exhaustive else "sample"))
    print("FIXED-SHELL RESIDUE-SATURATION CONTROLS PASS")
    print("checks:", checks)
    for row in cases:
        print(*row)


if __name__ == "__main__":
    main()
