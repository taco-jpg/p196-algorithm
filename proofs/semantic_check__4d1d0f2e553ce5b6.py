#!/usr/bin/env python3
"""Independent finite semantic cross-check; this is not a Lean proof."""
from itertools import product
from pathlib import Path
import hashlib, json

HERE = Path(__file__).resolve().parent

def actual(q):
    carry, digits = [0], []
    for x in q:
        digits.append((x + carry[-1]) % 10)
        carry.append((x + carry[-1]) // 10)
    if carry[-1]:
        digits.append(carry[-1])
    return carry, digits, [x+y for x,y in zip(digits, reversed(digits))]

def local_scan(q, counts):
    L = len(q)
    a, digits, out = actual(q)
    assert all(c in (0,1) for c in a)
    if a[-1] == 0:
        counts['no_overflow_words'] += 1
        for i,x in enumerate(q):
            aa,bb = a[i],a[L-1-i]
            rhs18 = (x in (8,18) and aa+bb == 2) or (x == 9 and aa+bb == 0)
            rhs0 = (x in (0,10) and aa+bb == 0) or (x == 9 and aa+bb == 2)
            assert (out[i] == 18) == rhs18
            assert (out[i] == 0) == rhs0
            assert (out[i] == 18 and x != 18) == ((x == 8 and aa == bb == 1) or (x == 9 and aa == bb == 0))
            assert (out[i] == 0 and x != 0) == ((x == 10 and aa == bb == 0) or (x == 9 and aa == bb == 1))
            if i == L-1-i:
                assert (out[i] == 18 and x != 18) == (x == 8 and aa == 1)
                assert (out[i] == 0 and x != 0) == (x == 10 and aa == 0)
    else:
        counts['overflow_words'] += 1
        assert out[0] == out[L] == 1 + q[0] % 10
        assert all(out[j] not in (0,18) for j in (0,L))
        for i in range(1,L):
            x,y,b,d = q[i-1],q[i],a[i],a[L-i]
            rhs0 = (x == y == 0) or (x == y == 9 and b == d == 1) or (x == 9 and y == 10 and b == 0) or (x == 10 and y == 9 and d == 0)
            rhs18 = (x == y == 18) or (x == y == 9 and b == d == 0) or (x == 9 and y == 8 and b == 1) or (x == 8 and y == 9 and d == 1)
            assert (out[i] == 0) == rhs0
            assert (out[i] == 18) == rhs18
            if out[i] == 0 and (x,y) != (0,0) or out[i] == 18 and (x,y) != (18,18):
                assert 9 in (x,y)
            if x != 9 and y != 9:
                assert (out[i] == 0) == (x == y == 0)
                assert (out[i] == 18) == (x == y == 18)
    counts['physical_columns'] += L

def number(ds):
    return sum(d * 10 ** i for i,d in enumerate(ds))

def step(n):
    return n + int(str(n)[::-1])

def run():
    counts = dict(no_overflow_words=0,overflow_words=0,physical_columns=0)
    for L in range(1,7):
        if L == 1:
            words = ([c] for c in range(2,19,2))
        else:
            half = L//2
            choices = [range(1,19)] + [range(19)]*(half-1)
            words = (list(h) + ([c] if L%2 else []) + list(reversed(h))
                     for h in product(*choices) for c in (range(0,19,2) if L%2 else [0]))
        for q in words:
            assert q == q[::-1] and q[0] > 0
            local_scan(q, counts)
    family_examples=[]
    for g in range(2,101):
        q = [1,10,8]+[18]*g+[8,10,1]
        L = len(q)
        a,ds,out = actual(q)
        expected=[3,0,18,17]+[18]*(g-2)+[17,18,0,3]
        assert a[-1] == 0 and len(out) == g+6 and out == expected
        assert out[1] == out[-2] == 0 and out[2] == out[-3] == 18 and out[3] == out[-4] == 17
        d = [max(x-9,0) if i<L-1-i else min(x,9) if i>L-1-i else x//2 for i,x in enumerate(q)]
        assert d[-1] > 0 and all(0 <= x <= 9 for x in d)
        assert [x+y for x,y in zip(d,reversed(d))] == q
        n=number(d)
        assert step(n) == number(ds)
        orbit=[n,step(n),step(step(n))]
        assert all(str(n) != str(n)[::-1] for n in orbit)
        if g in (2,3,4): family_examples.append(dict(g=g,source=q,target=out,n=n,three_values=orbit))
    report=dict(status='PASS',kind='Finite independent semantic cross-check, not a proof',
                words_widths='all admissible symmetric words with 1 <= L <= 6',
                counts=counts,family_g_range=[2,100],family_examples=family_examples,
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'semantic_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__': run()
