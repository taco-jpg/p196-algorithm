#!/usr/bin/env python3
"""Independent controls for the all-phase T* centre-parity/mass cocycle.

This checks exact length, carry-mass, and overflow identities on four genuine
rooted decimal T* starts. It makes NO claim about finite-horizon Lychrel
survival or a returning seam.
"""
import sys
sys.set_int_max_str_digits(0)

B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [5,18,4,8,1,15,4,0,5]
U = [9,6,12]
J = [5]
C = [10]


def from_pairword(p):
    assert p == p[::-1]
    assert p and p[0] > 0
    assert all(0 <= x <= 18 for x in p)
    d = [0] * len(p)
    for i in range(len(p) // 2):
        d[i] = max(0, p[i] - 9)
        d[-1-i] = min(9, p[i])
    if len(p) % 2:
        assert p[len(p)//2] % 2 == 0
        d[len(p)//2] = p[len(p)//2] // 2
    assert d[-1] > 0
    n = 0
    for x in reversed(d):
        n = 10*n + x
    return n


def template(q, k):
    h = B + W*q + J + U*k
    p = h + C + h[::-1]
    return from_pairword(p), p


def digit_array_step(n):
    # Independent schoolbook addition of LSD-first digit arrays.
    ds = [int(ch) for ch in str(n)[::-1]]
    out, carry, carry_total = [], 0, 0
    for i, digit in enumerate(ds):
        z = digit + ds[-1-i] + carry
        carry = z // 10
        out.append(z % 10)
        carry_total += carry
    gamma = carry
    if carry:
        out.append(carry)
    result = 0
    for digit in reversed(out):
        result = 10*result + digit
    return result, gamma, carry_total, ds, out


def check(q, k, steps=120):
    n, p0 = template(q, k)
    assert len(B) == 34 and len(W) == 9 and len(U) == 3
    assert sum(B) == 307 and sum(W) == 60 and sum(U) == 27
    assert len(str(n)) == len(p0)
    initial_len = len(str(n))
    overflow_count = 0
    for t in range(steps):
        s = str(n)
        fast = n + int(s[::-1])
        slow, gamma, K, ds, out = digit_array_step(n)
        assert fast == slow, (q, k, t, "integer engines disagree")
        assert gamma == int(len(str(slow)) == len(s)+1)
        assert len(str(slow)) - len(s) == gamma
        assert (len(str(slow)) % 2) == ((len(s) % 2) ^ gamma)

        pair = [ds[i] + ds[-1-i] for i in range(len(ds))]
        assert pair == pair[::-1] and pair[0] >= 1
        S = sum(pair)
        next_digits = [int(ch) for ch in str(slow)[::-1]]
        next_pair = [next_digits[i] + next_digits[-1-i]
                     for i in range(len(next_digits))]
        assert next_pair == next_pair[::-1]
        assert S == 2*sum(ds)
        assert sum(next_pair) == 2*sum(next_digits)
        # Exact digit-sum/carry conservation, with final overflow included.
        assert sum(next_pair) == 2*S - 18*K, (q, k, t, S, K)
        assert gamma == int(t % 4 == 0), (q, k, t, gamma)
        overflow_count += gamma
        n = slow

    assert overflow_count == 30
    assert len(str(n)) - initial_len == 30
    return (q, k, initial_len, len(str(n)), overflow_count, steps)


def main():
    rows = [check(q, 5*q) for q in (20, 40, 80, 160)]
    print("q,k,start_digits,end_digits,overflows,steps_checked")
    for row in rows:
        print(",".join(map(str, row)))
    print("PASS: independent Python-bigint and schoolbook digit-array engines agree.")
    print("PASS: exact T* overflow clock and carry-mass identity at all 480 checked edges.")
    print("Scope: algebraic controls only; no survival horizon or returning seam is claimed.")


if __name__ == "__main__":
    main()
