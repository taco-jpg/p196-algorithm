"""Exact prefix carry identities and checks for a proposed stack invariant.
This is an exploratory obstruction, not a decimal Lychrel proof.
"""
from itertools import product
from creative_regular_invariant import fold, unfold, qstep, valid
import json


def prefix_balance(w):
    q = unfold(w)
    L = len(q)
    c = [0]
    for a in q:
        c.append((a + c[-1]) // 10)
    h = c[-1]
    out = unfold(qstep(w))
    Q = [0]
    for a in q:
        Q.append(Q[-1] + a)
    for j in range(1, L + 1):
        if h == 0:
            expected = 2 * Q[j] - 9 * sum(c[i] + c[L-i] for i in range(1,j)) - 10*c[j] + c[L-j]
        else:
            expected = Q[j] + Q[j-1] - 9 * sum(c[i] + c[L-i+1] for i in range(1,j)) - 10*c[j] + c[L-j+1]
        assert sum(out[:j]) == expected, (w,j,out,expected)
    if q[0] >= 10:
        assert h == 1 and out[0] == q[0] - 9


def dyck(w):
    s = 0
    seen = False
    for q in w[0]:
        s += q-9
        seen |= q != 9
        if s < 0: return False
    return w[1] is None and s == 0 and seen

if __name__ == '__main__':
    count = 0
    for m in range(4):
        for p in product(range(19),repeat=m):
            for c in [None]+list(range(0,19,2)):
                w=(p,c)
                if not valid(w): continue
                prefix_balance(w)
                count += 1
    w=((10,8),None)
    assert dyck(w) and not dyck(qstep(w))
    assert 1719 + int(str(1719)[::-1]) == 10890
    print(json.dumps({'checked_words':count,'dyck_counterexample':{'input':w,'output':qstep(w),'decimal_input':1719,'decimal_output':10890},'claim':'Exact prefix formulas verified on finite test domain; ordinary Dyck cone is not closed. No Lychrel existence claim.'},indent=2))
