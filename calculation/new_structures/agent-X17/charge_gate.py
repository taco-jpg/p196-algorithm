#!/usr/bin/env python3
"""Exact Python-bigint charge gate for one-cell palindrome perturbations."""
import csv
import sys

sys.set_int_max_str_digits(0)
MOTIF = "88283583"
N = 10001

def step(x):
    s = str(x)
    return x + int(s[::-1])

def mirror(x):
    s = str(x)
    return s == s[::-1]

def carry(seq):
    c = [0]
    for q in seq:
        c.append((q + c[-1]) // 10)
    return c

def matched(a, b):
    sa, sb = str(a), str(b)
    if len(sa) != len(sb):
        return (-1, -1)
    width = len(sa)
    l = next((i for i in range(width) if sa[-1-i] != sb[-1-i]), width)
    r = next((i for i in range(width) if sa[i] != sb[i]), width)
    return l, r

def main(dst):
    p = int(''.join(MOTIF[min(i, N-i-1) % 8] for i in range(N)))
    assert mirror(p)
    base = [p]
    for _ in range(109):
        base.append(step(base[-1]))
    rows=[]
    for off in range(1, 16):
        q = p + 10 ** (N//2-off)
        assert not mirror(q)
        for t in range(107):
            q = step(q)
        a = str(base[107])[::-1]
        b = str(q)[::-1]
        assert len(a) == len(b)
        L = len(a)
        src = [int(a[i])+int(a[L-1-i]) for i in range(L)]
        dsts = [int(b[i])+int(b[L-1-i]) for i in range(L)]
        dif = [i for i in range(L) if src[i] != dsts[i]]
        assert dif
        k = max(dif)+1
        cs, ct = carry(src),carry(dsts)
        run=0
        while k+run < L and src[k+run] == 9:
            run += 1
        stop=src[k+run] if k+run<L else -1
        q=step(q)
        l108,r108=matched(base[108],q)
        q=step(q)
        l109,r109=matched(base[109],q)
        rows.append((off,min(dif),max(dif),k,cs[k],ct[k],run,stop,l108,r108,l109,r109))
    fields=('offset','pair_diff_min','pair_diff_max','first_equal_pair_col',
            'baseline_carry_at_col','pert_carry_at_col','neutral9_run',
            'first_stopper','same_lsd_108','same_msd_108',
            'same_lsd_109','same_msd_109')
    assert rows[0][4:7] == (0,1,4920)
    assert rows[2][4:7] == (0,0,4916)
    assert rows[0][9] == 60 and rows[2][9] >= 4900
    with open(dst,'w',newline='') as f:
        wr=csv.writer(f)
        wr.writerow(fields)
        wr.writerows(rows)
    print('PASS: off=1 transmits differential carry, off=3 neutralises it; 15 exact bigint controls')

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'charge_gate.csv')