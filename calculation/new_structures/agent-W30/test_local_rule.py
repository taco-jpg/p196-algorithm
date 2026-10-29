#!/usr/bin/env python3
"""Independent exact random integer-vs-piecewise-affine pairword controls for agent W30."""
import random

def local(x, left, right, overflow):
    assert 9 not in (x, left, right)
    h = lambda v: int(v >= 10)
    if overflow:
        return x - 9 * h(x) + left - 9 * h(left)
    return 2 * x + h(left) + h(right) - 20 * h(x)

def pair(d):
    return [a+b for a,b in zip(d, reversed(d))]

def normalize(P):
    carry = 0
    d = []
    for p in P:
        v = p + carry
        d.append(v % 10)
        carry = v // 10
    if carry:
        d.append(carry)
    return d, carry

def realize(P):
    n = len(P)
    d = [0] * n
    for i in range(n//2):
        lo = max(0, P[i] - 9)
        d[i], d[n - 1 - i] = lo, P[i] - lo
    if n % 2:
        d[n//2] = P[n//2]//2
    assert d[-1] and pair(d) == P
    return d

def run():
    rng = random.Random(300101010)
    covered = {0:0,1:0}
    count = 20000
    for _ in range(count):
        n = rng.randrange(12, 81)
        half = [rng.randrange(19) for _ in range(n//2)]
        half[0] = rng.randrange(1, 19)
        if n%2:
            P = half + [2*rng.randrange(10)] + half[::-1]
        else:
            P = half + half[::-1]
        d = realize(P)
        Dnext, gam = normalize(P)
        old = int(''.join(map(str, reversed(d))))
        truth = old + int(str(old)[::-1])
        assert ''.join(map(str, reversed(Dnext))) == str(truth)
        Pnext = pair(Dnext)
        for i in range(2, n//2-2):
            if 9 in (P[i-1],P[i],P[i+1]):
                continue
            predicted = local(P[i],P[i-1],P[i+1],gam)
            assert Pnext[i] == predicted, (i,gam,P[i-1:i+2],predicted,Pnext[i])
            covered[gam] += 1
    assert all(covered.values())
    # Deliberately corrupted output must fail the same exact local equality.
    assert local(17,3,14,1) != (local(17,3,14,1)+1)%19
    print('PASS 20000 random independently realized whole-number updates; interior local checks:', covered)
    # The full period-40 five-site carrier, including the non-9 and odd conditions.
    W=[17,3,14,3,17]
    rows=[]
    for t in range(40):
        assert 9 not in W and any(v%2 for v in W)
        rows.append(tuple(W))
        gam = (t%2 == 0)
        W=[local(W[i],W[(i-1)%5],W[(i+1)%5],gam) for i in range(5)]
    assert tuple(W) == rows[0]
    assert rows[8] == tuple(rows[0][(i-2)%5] for i in range(5))
    print('PASS period-40 odd 5-site carrier; eight steps translate by +2 mod 5')

if __name__ == '__main__': run()
