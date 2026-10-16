#!/usr/bin/env python3
"""Unbounded-width terminal-column necessary-condition control (WIP).
Independent of full-width MILP. Every true canonical two-step cycle with
initial phase six and width>=2 would induce one of these finite tuples, if
the last-column projection bridge described in RESEARCH.md is proved.
This is NOT a Lean proof or a solver certificate.
"""
from collections import Counter

def solve():
    checked=Counter()
    hits=[]
    for q in (0,1,2):
        r=2-q
        for mu1 in (0,1):
            for mu2 in (0,1):
                for x in range(19):
                    if x==6:
                        continue
                    for a in (0,1):
                        lam1=(x+a)//10
                        d1=(x+a)%10
                        e0=x%10
                        last1=12+lam1 if mu1==0 else 6+lam1+e0
                        if q==0 and last1==12:
                            continue
                        if q>0 and last1!=12:
                            continue
                        ps=[d1+e0] if mu1==0 else [d1+d for d in range(10)]
                        if q==0:
                            ws=[last1]
                        elif q==1:
                            ws=[p for p in ps if p!=12]
                        else:
                            if 12 not in ps:
                                continue
                            ws=[w for w in range(19) if w!=12]
                        for w in ws:
                            if w<0 or w>18:
                                continue
                            for b in (0,1):
                                lam2=(w+b)//10
                                e20=(w+1)%10
                                last2=5+lam2 if mu2==0 else 2+lam2+e20
                                if r>0 and last2!=6:
                                    continue
                                if r==0:
                                    checked[(q,mu1,mu2)]+=1
                                    if last2==x:
                                        hits.append((q,mu1,mu2,x,a,b,w))
                                    continue
                                ps2=[(w+b)%10+e20] if mu2==0 else [(w+b)%10+f for f in range(10)]
                                for p2 in ps2:
                                    checked[(q,mu1,mu2)]+=1
                                    if (r==1 and p2==x) or (r==2 and p2==6):
                                        hits.append((q,mu1,mu2,x,a,b,w,p2))
    return checked,hits

if __name__=="__main__":
    counts,hits=solve()
    for q in range(3):
        for mu1 in range(2):
            for mu2 in range(2):
                print("q,mu1,mu2,candidate-count",q,mu1,mu2,counts[(q,mu1,mu2)])
    print("feasible-candidate-count",len(hits))
    if hits:
        print("COUNTEREXAMPLE TUPLES",hits[:20])
        raise SystemExit(1)
    print("PASS: finite necessary conditions exclude canonical phase6 two-cycles; Lean bridge still WIP")
