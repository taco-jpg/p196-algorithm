"""Construct finite exact-length palindromes in every compatible residue.

Standalone standard-library controls; imports no archive discovery modules.
The proof is astra_modular_fixed_modulus_theorem.md.
"""
from __future__ import annotations

from collections import Counter
from math import gcd
from pathlib import Path
import json
import time


def parameters(modulus: int) -> dict[str, int]:
    if modulus < 1:
        raise ValueError("The modulus must be positive")
    q = modulus
    alpha = beta = 0
    while q % 2 == 0:
        q //= 2
        alpha += 1
    while q % 5 == 0:
        q //= 5
        beta += 1
    u = modulus // q
    k = max(1, alpha, beta)
    r = 1
    if q > 1:
        residue = 10 % q
        while residue != 1:
            residue = residue * 10 % q
            r += 1
    return dict(modulus=modulus, alpha=alpha, beta=beta, u=u, q=q,
                k=k, r=r, bound=2*k+4*q*r)


def digit_residue(digits_lsd: list[int], modulus: int) -> int:
    """Independent streaming evaluation, with no huge integer conversion."""
    value = 0
    for digit in reversed(digits_lsd):
        value = (10 * value + digit) % modulus
    return value


def compatible(modulus: int, residue: int, length: int) -> bool:
    return not (modulus % 10 == 0 and residue % 10 == 0) and (
        length % 2 == 1 or residue % gcd(modulus, 11) == 0)


def build(modulus: int, residue: int, length: int) -> list[int]:
    p = parameters(modulus)
    u, q, k, r = (p[key] for key in ("u", "q", "k", "r"))
    if length < p["bound"]:
        raise ValueError("Length is below the sufficient theorem bound")
    if not compatible(modulus, residue, length):
        raise ValueError("The class has a necessary palindrome obstruction")
    suffix = residue % u
    if suffix % 10 == 0:
        suffix += u
    assert 0 < suffix < 10**k and suffix % 10 != 0
    digits = [0] * length
    a = suffix
    for i in range(k):
        digits[i] = digits[length-1-i] = a % 10
        a //= 10
    assert a == 0
    if q == 1:
        return digits

    c0 = (1 + pow(10, length-1, q)) % q
    c1 = (10 + pow(10, length-2, q)) % q
    target = (residue - digit_residue(digits, q)) % q
    g = gcd(q, gcd(c0, c1))
    assert g == (gcd(q, 11) if length % 2 == 0 else 1)
    assert target % g == 0
    c1_gcd = gcd(c1, q)
    reduced_q = q // c1_gcd
    inverse = pow(c1 // c1_gcd, -1, reduced_q) if reduced_q > 1 else 0
    xy = None
    for x in range(q):
        remainder = (target - x*c0) % q
        if remainder % c1_gcd == 0:
            y = ((remainder // c1_gcd)*inverse) % reduced_q
            xy = x, y
            break
    assert xy is not None
    x, y = xy
    pool0 = [i for i in range(k, k+q*r) if i % r == 0]
    pool1 = [i for i in range(k+q*r, k+2*q*r) if i % r == 1 % r]
    assert len(pool0) == len(pool1) == q
    assert set(pool0).isdisjoint(pool1)
    for i in pool0[:x] + pool1[:y]:
        assert k <= i <= (length-2)//2
        assert digits[i] == digits[length-1-i] == 0
        digits[i] = digits[length-1-i] = 1
    return digits


def verify(digits: list[int], modulus: int, residue: int, length: int) -> None:
    assert len(digits) == length
    assert digits[0] != 0 and digits[-1] != 0
    assert all(isinstance(digit, int) and 0 <= digit <= 9 for digit in digits)
    assert digits == digits[::-1]
    assert digit_residue(digits, modulus) == residue % modulus
    if length % 2 == 0:
        assert digit_residue(digits, 11) == 0


def controls() -> dict:
    started = time.monotonic()
    counts = Counter()
    special = []
    for modulus in range(1, 41):
        p = parameters(modulus)
        for length in (p["bound"], p["bound"]+1, p["bound"]+3):
            for residue in range(modulus):
                if compatible(modulus, residue, length):
                    verify(build(modulus, residue, length), modulus, residue, length)
                    counts["small_compatible_constructed"] += 1
                else:
                    try:
                        build(modulus, residue, length)
                    except ValueError:
                        counts["small_incompatible_rejected"] += 1
                    else:
                        raise AssertionError("An incompatible class was accepted")

    # Pure 2/5 parts; order=1; powers of 11; factors shared with length clocks.
    for modulus in (1, 3, 9, 81, 99, 101, 121, 242, 625, 1000, 1331):
        p = parameters(modulus)
        done = 0
        for length in (p["bound"], p["bound"]+1):
            residues = (0, 1, 2, 5, 10, 11, 22, 33, modulus-1)
            for residue in dict.fromkeys(x % modulus for x in residues):
                if compatible(modulus, residue, length):
                    verify(build(modulus, residue, length), modulus, residue, length)
                    done += 1
        special.append(dict(**p, constructed=done))
        counts["special_constructed"] += done

    # Ordinary integer arithmetic independently checks eventual 11 and last-zero facts.
    for n in range(1, 100000):
        s = str(n)
        reverse = int(s[::-1])
        nxt = n + reverse
        assert reverse % 11 == ((-1)**(len(s)-1) * n) % 11
        if len(s) % 2 == 0 or n % 11 == 0:
            assert nxt % 11 == 0
        if n % 10 == 0:
            assert nxt % 10 != 0
        nxt_s = str(nxt)
        if len(s) % 2 == 0 and len(nxt_s) > len(s) and nxt_s == nxt_s[::-1]:
            assert nxt % 121 == 0
            counts["even_width_palindromic_overflow_controls"] += 1
        counts["integer_dynamics_controls"] += 1

    for j in range(3, 20):
        n = 196 + 4*10**j
        assert n + int(str(n)[::-1]) == 200 + 1091*10**(j-2)
        counts["adic_counterexample_controls"] += 1

    # Check the constructive necessity proof for the residue-update classification.
    for modulus in range(1, 501):
        if 99 % modulus == 0:
            for n in range(1, 10000):
                factor = 1 if len(str(n)) % 2 else 10
                assert int(str(n)[::-1]) % modulus == factor*n % modulus
            counts["autonomous_moduli_positive_controls"] += 1
        else:
            length = max(3, len(str(modulus)) + 2)
            base = 10**(length-1)
            if gcd(modulus, 10) != 1:
                a = ((base + modulus-1)//modulus)*modulus
                b = ((2*base + modulus-1)//modulus)*modulus
                pairs = [(a,b)]
            else:
                n = base+9
                pairs = [(n,n+modulus), (n+1,n+modulus+1)]
            assert all(len(str(a)) == len(str(b)) == length and
                       a % modulus == b % modulus for a,b in pairs)
            assert any(int(str(a)[::-1]) % modulus != int(str(b)[::-1]) % modulus
                       for a,b in pairs)
            counts["nonautonomous_moduli_counterexamples"] += 1

    return dict(status="all passed", counts=dict(counts), special_moduli=special,
                seconds=time.monotonic()-started,
                qualification="Controls verify the construction and identities; no Lychrel witness is asserted.")


if __name__ == "__main__":
    result = controls()
    out = Path(__file__).with_name("astra_modular_palindrome_builder_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
