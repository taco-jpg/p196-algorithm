#!/usr/bin/env python3
"""Find the smallest seeds whose base-b orbit enters the certified power-of-two template cycle
with gap >= 2 + sumGam = 4, before any palindrome. Exploratory; Lean rechecks any seed used."""
import sys
from quotient import qstep, template, value, digits, pairs
def cycle_states(b):
    st=((b,),(b-2,b-2)); out=[]
    while True:
        out.append(st)
        B2,C2,g,u,v=qstep(b,*st); st=(B2,C2)
        if st==out[0]: return out
def match(q,b,states,gmin):
    for (B,C) in states:
        L=len(q); s=len(B); m=len(C)
        if (L-2*s-m)%2 or L-2*s-m<0: continue
        g=(L-2*s-m)//2
        if g>=gmin and list(q)==template(b,B,C,g): return (B,C,g)
    return None
def entry(N,b,states,steps=400):
    for t in range(steps):
        D=digits(b,N)
        if D==D[::-1]: return None
        m=match(pairs(D),b,states,4)
        if m: return (t+1,m)
        N=N+value(b,D[::-1])
    return None
for b in [int(x) for x in sys.argv[1:]]:
    states=cycle_states(b)
    for N in range(1,200000):
        e=entry(N,b,states)
        if e:
            print('base',b,'smallest seed',N,'digits(msd first)',list(reversed(digits(b,N))),'enters after',e[0],'steps at',e[1]); break
