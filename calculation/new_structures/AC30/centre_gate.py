#!/usr/bin/env python3
"""Phase9 two-centre gate for all 30 U: true bigint and independent schoolbook replay.

No strict W9 pruning. The all-J conclusion uses the phase9 two-carry
reset-cone separation, not an empirical extrapolation of these controls.
Run in independent batches: python3 calculation/new_structures/AC30/centre_gate.py 0 10
"""
from pathlib import Path
from independent import read, ulist, templ, realize
from phase9_cones import g
from random import Random
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
LATTICE=Path(__file__).resolve().parents[2]/"decimal_frontier"/"lattice_kinks"/"data"/"lat_p12m9.txt"
B0,W0=read(LATTICE)

def digits(n):
    return [int(x) for x in str(n)[::-1]]
def physical_step(d):
    length=len(d);result=[0]*length;carry=0
    for i in range(length):
        z=d[i]+d[length-1-i]+carry
        result[i]=z%10
        carry=z//10
    if carry:result.append(carry)
    return result
def pair(d):
    return [a+b for a,b in zip(d,d[::-1])]
def endpoint(U,C,q=14,k=100,J=(0,0,0,0,0)):
    initial=templ(B0,W0,list(J),U,list(C),q,k)
    target=templ(B0,W0,list(J),U,list(C),q,k+5)
    n=realize(initial);d=digits(n)
    for t in range(120):
        out=physical_step(d)
        old=str(n);next_n=n+int(old[::-1])
        assert len(str(next_n))-len(old)==g(t),(U,C,q,k,t,"clock")
        assert out==digits(next_n),(U,C,q,k,t,"independent engines")
        d,n=out,next_n
    got=pair(d)
    assert len(got)==len(target),(U,C,q,k,"length")
    h=len(got)//2
    near=next((i for i in range(3) if got[h-i]!=target[h-i]),None)
    assert near is not None,(U,C,q,k,J,"unexpected centre match")
    begin=h-len(C)//2
    return near,tuple(got[begin:begin+len(C)]),tuple(got[h-2:h+1]),tuple(target[h-2:h+1])

def main():
    start=int(sys.argv[1]) if len(sys.argv)>1 else 0
    stop=int(sys.argv[2]) if len(sys.argv)>2 else 30
    assert 0<=start<=stop<=30
    rng=Random(20261029+start);rows=[]
    for ix,U in enumerate(ulist()):
        if not start<=ix<stop:continue
        for C in ((4,4),(4,14,4)):
            baseline=endpoint(U,C)
            for q,k in ((20,80),(40,160),(80,320),(160,640)):
                J=tuple(rng.randrange(19) for _ in range(5))
                assert endpoint(U,C,q,k,J)==baseline,(ix,C,q,k,J)
            rows.append((ix,tuple(U),C,baseline))
    print("PASS",len(rows),"U/C pairs;",len(rows)*5,"120-step dual-engine trajectories")
    for ix,U,C,values in rows:
        print("ROW",ix,U,C,"nearest-midpoint-discrepancy",values[0],"observed-low3",values[2],"target-low3",values[3])
    print("Scope: fixed two centres; all-J conclusion uses two-ended carry-cone proof.")
if __name__=="__main__":
    main()
