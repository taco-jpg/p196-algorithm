#!/usr/bin/env python3
"""Independent finite controls for the all-moduli palindrome residue lemma.

For odd M coprime to 10, d=ord_M(10), n=ceil((M-1)/9), and
k >= d(n+1), construct for every r mod M an exact-length (2k+1)-digit
palindrome P with P == r (mod M). The proof is in IDEAS.md; this script
checks the construction with both integer and LSD-first digit-array residues.
"""
from math import gcd
import random
import sys

sys.set_int_max_str_digits(0)


def order10(M: int) -> int:
    if M == 1:
        return 1
    assert M > 1 and M % 2 == 1 and gcd(M, 10) == 1
    x = 10 % M
    d = 1
    while x != 1:
        x = (x * 10) % M
        d += 1
        if d > M:
            raise AssertionError("order search exceeded group bound")
    return d


def make_palindrome(M: int, r: int, k: int):
    assert M > 1 and M % 2 == 1 and gcd(M, 10) == 1
    r %= M
    d = order10(M)
    n = (M - 1 + 8) // 9
    assert k >= d * (n + 1)

    digits = [0] * (2 * k + 1)  # LSD first
    digits[0] = digits[2 * k] = 1
    w0 = (1 + pow(10, 2 * k, M)) % M
    w = (2 * pow(10, k, M)) % M
    assert gcd(w, M) == 1
    t = ((r - w0) * pow(w, -1, M)) % M
    assert 0 <= t <= M - 1 <= 9 * n

    remaining = t
    chosen = []
    for m in range(1, n + 1):
        i = k - d * m
        assert 1 <= i <= k - 1
        digit = min(9, remaining)
        digits[i] = digits[2 * k - i] = digit
        remaining -= digit
        chosen.append(i)
    assert remaining == 0
    assert len(set(chosen)) == n

    # Independent verifier A: materialize the canonical decimal integer.
    s = "".join(str(x) for x in reversed(digits))
    assert len(s) == 2 * k + 1 and s[0] != "0" and s == s[::-1]
    value = int(s)
    assert value % M == r

    # Independent verifier B: evaluate the LSD-first digit array modulo M.
    digit_residue = sum(d * pow(10, i, M) for i, d in enumerate(digits)) % M
    assert digit_residue == r == value % M

    # The selected paired positions all have weight w mod M.
    assert all((pow(10, i, M) + pow(10, 2 * k - i, M)) % M == w for i in chosen)
    return s


def main():
    rng = random.Random(38010)
    checks = 0
    rows = []
    for j in range(1, 5):
        M = 10**j + 1
        d = order10(M)
        assert d == 2 * j
        n = (M - 1 + 8) // 9
        k = d * (n + 1)
        rows.append((j, M, d, n, k, 2 * k + 1))
        residues = range(M) if M <= 1001 else [0, 1, M // 2, M - 1] + [rng.randrange(M) for _ in range(96)]
        for r in residues:
            make_palindrome(M, r, k)
            checks += 1
    # A finite conjunction of moduli: every residue modulo their LCM is also
    # realized by an odd palindrome of the same sufficiently large length.
    M = 101101  # lcm(11, 101, 1001)
    assert gcd(M, 10) == 1 and M % 2 == 1
    d = order10(M)
    n = (M - 1 + 8) // 9
    k = d * (n + 1)
    for r in [0, 1, 11, 101, 1001, M // 2, M - 1] + [rng.randrange(M) for _ in range(12)]:
        make_palindrome(M, r, k)
        checks += 1
    print("PAPER-LEMMA-CONSTRUCTION-CONTROLS PASS")
    print("checks:", checks)
    print("j M ord10 n k_min L_min")
    for row in rows:
        print(*row)
    print("combined_M=101101", "ord10=", d, "n=", n, "k_min=", k, "L_min=", 2*k+1)


if __name__ == "__main__":
    main()
