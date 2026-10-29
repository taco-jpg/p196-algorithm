"""Agent-X28: exact change-of-base carry-coboundary audit.

For B = k*(b-1)+1, E_k(d) = k*d digitwise and an ordinary first
reverse-and-add step have IDENTICAL carry words in bases b and B.
Normalized output digits differ by (k-1)*(c_out-c_in).

python3 carry_gauge.py [trials=25000]
"""
import random
import sys


def one_step(d, b):
    carry, outs, edges = 0, [], []
    for i, digit in enumerate(d):
        q = digit + d[-i-1]
        newcarry, out = divmod(q + carry, b)
        edges.append((q, carry, out, newcarry))
        outs.append(out)
        carry = newcarry
    if carry:
        outs.append(carry)
    return outs, edges


def test(trials=25000):
    rng = random.Random(2828)
    for _ in range(trials):
        b = rng.randint(2, 32)
        k = rng.randint(1, 31)
        B = k * (b - 1) + 1
        L = rng.randint(1, 120)
        d = [rng.randrange(b) for i in range(L)]
        d[-1] = rng.randrange(1, b)
        ds, es = one_step(d, b)
        dl, el = one_step([x*k for x in d], B)
        assert len(ds) == len(dl)
        assert len(es) == len(el)
        for (q, c, v, c1), (Q, C, V, C1) in zip(es, el):
            assert Q == k*q and C == c and C1 == c1
            assert V == k*v + (k - 1)*(c1 - c)
            assert 0 <= V < B
        assert dl[-1] == ds[-1] == 1 if len(dl) > L else True
    print(f"SUCCESS: {trials} independent random length/base/carry controls; "
          f"b in [2,32], multiplier k in [1,31]")


if __name__ == '__main__':
    test(int(sys.argv[1]) if len(sys.argv) > 1 else 25000)
