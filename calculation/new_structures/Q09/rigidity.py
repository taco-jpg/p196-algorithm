#!/usr/bin/env python3
"""Q09 independent p8/m20 rooted-exterior all-centre rigidity controls.
Run: python3 calculation/new_structures/Q09/rigidity.py
"""
import sys
from itertools import permutations
from random import Random
sys.set_int_max_str_digits(0)
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
witnesses={1:(5,1,0),3:(1,0,1),6:(14,0,1),7:(12,1,0),14:(17,1,0),29:(13,0,1),30:(18,1,0)}
assert len(B)==39 and B[-1]==13 and len(W)==20

def carries(P):
    c=0;out=[]
    for p in P:
        out.append(c);c=(p+c)//10
    return out,c
def physical(P):
    assert P==P[::-1] and len(P)%2==0
    d=[0]*len(P)
    for i in range(len(P)//2):
        d[i]=max(0,P[i]-9);d[-1-i]=P[i]-d[i]
    assert d[-1]>0
    return sum(x*10**i for i,x in enumerate(d))
def pairs(n):
    d=list(map(int,str(n)[::-1]))
    return [d[i]+d[-1-i] for i in range(len(d))]

rng=Random(909477)
cores=[[]]
for m in (20,40,80,160):
    H=W*m;cores.append(H+H[::-1])
    h=[rng.randrange(19) for _ in range(m)]
    cores.append(h+h[::-1])
    cores.append(h+[2*rng.randrange(10)]+h[::-1])
for C in cores:
    P=B+C+B[::-1]
    assert P==P[::-1]
    cs,final=carries(P)
    for i,(p,lo,hi) in witnesses.items():
        assert B[i]==p and (cs[i],cs[-1-i])==(lo,hi)
    if len(C)%2==0:
        n=physical(P)
        assert pairs(n)==P
        assert n+int(str(n)[::-1])==sum(p*10**i for i,p in enumerate(P))
    print("ALL-CENTRE CONTROL",len(C),"PASS")
R={p%10 for p,lo,hi in witnesses.values()}
assert R=={1,2,3,4,5,7,8}
survivors=[]
for mid in permutations(range(1,9)):
    pi=(0,)+mid+(9,)
    if all(pi[r+1]==pi[r]+1 for r in R):survivors.append(pi)
assert survivors==[tuple(range(10))]
print("40320 POSSIBLE CARRY-STATE PERMUTATIONS: ONLY IDENTITY PASSES WITNESSES")
pi=(0,1,3,2,4,5,6,7,8,9)
for m in (20,40,80,160):
    H=B+W*m;P=H+H[::-1]
    cs,final=carries(P)
    Q=[]
    for p,c in zip(P,cs):
        Q.append(pi[(p+c)%10]+10*((p+c)//10)-c)
    assert all(0<=q<=18 for q in Q) and Q!=Q[::-1]
    a=[];c=0
    for p in P:
        a.append((p+c)%10);c=(p+c)//10
    z=[];c2=0
    for q in Q:
        z.append((q+c2)%10);c2=(q+c2)//10
    assert c==c2 and z==[pi[d] for d in a]
    print("NONTRIVIAL DUAL BREAKS MIRROR",m,"PASS")
