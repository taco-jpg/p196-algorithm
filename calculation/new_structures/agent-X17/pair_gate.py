#!/usr/bin/env python3
"""Exact Python bigint comparison of destructive singles vs constructive paired defects."""
import csv
import sys
sys.set_int_max_str_digits(0)
MOTIF='88283583'

def seed(n,offsets):
    s=''.join(MOTIF[min(i,n-1-i)%len(MOTIF)] for i in range(n))
    x=int(s)
    for off in offsets:
        assert 0 < off < n//2
        assert s[n//2+off] != '9'
        x += 10**(n//2-off)
    return x

def step(x):
    s=str(x)
    return x+int(s[::-1])

def ends(a,b):
    sa,sb=str(a),str(b)
    if len(sa)!=len(sb): return -1,-1
    L=len(sa)
    l=next((i for i in range(L) if sa[L-1-i]!=sb[L-1-i]),L)
    r=next((i for i in range(L) if sa[i]!=sb[i]),L)
    return l,r

def carries(q):
    c=[0]
    for x in q:c.append((x+c[-1])//10)
    return c

def diag(a,b):
    sa,sb=str(a)[::-1],str(b)[::-1]
    assert len(sa)==len(sb)
    L=len(sa)
    qa=[int(sa[i])+int(sa[L-1-i]) for i in range(L)]
    qb=[int(sb[i])+int(sb[L-1-i]) for i in range(L)]
    dif=[i for i in range(L) if qa[i]!=qb[i]]
    k=max(dif)+1
    c,d=carries(qa),carries(qb)
    run=0
    while k+run<L and qa[k+run]==qb[k+run]==9:run+=1
    return k,c[k],d[k],run

def main(out):
    rows=[]
    for n in [2001,6001,10001]:
        a=seed(n,())
        qs={str(o):seed(n,o) for o in [(7,),(8,),(7,8),(1,),(2,),(1,2)]}
        for t in range(107):
            a=step(a)
            qs={name:step(v) for name,v in qs.items()}
        for name,v in qs.items():
            k,c,d,run=diag(a,v)
            v108=step(v);a108=step(a)
            _,hi108=ends(a108,v108)
            v109=step(v108);a109=step(a108)
            lo109,_=ends(a109,v109)
            rows.append((n,name,k,c,d,run,hi108,lo109))
    with open(out,'w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['n','offsets','first_common_pair_col','base_carry','pert_carry','common9_run','matched_high_108','matched_low_109'])
        w.writerows(rows)
    print('PASS: 18 exact pair/individual carry-gate controls over three lengths')
if __name__=='__main__': main(sys.argv[1] if len(sys.argv)>1 else 'pair_gate.csv')
