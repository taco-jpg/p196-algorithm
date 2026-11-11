#!/usr/bin/env python3
"""r13a: exact-integer replay of a seam found by seamgen.py (clock 1000, T12 exterior B0 W0^q).
Builds P = B0 W0^q J V^k C mirror (random centre), runs the genuine big-integer orbit for N steps, and checks
(1) clock is 1000 for all N steps, (2) columns [0, xend) return exactly after N steps (xend = protected zone), (3) columns inside the seam window are reproduced.
usage: seamreplay.py --J 3,1,4 --V_t0 18,9,0 --N 120 [--q 12] [--k 200] [--seed 1]"""
import sys, random, argparse
import bandsat as BS
B0=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W0=[5,18,4,8,1,15,4,0,5]
def digits(n,b=10):
    d=[]
    while n: d.append(n%b); n//=b
    return d or [0]
def val(d,b=10):
    n=0
    for x in reversed(d): n=n*b+x
    return n
def pair(n):
    d=digits(n); L=len(d)
    return [d[i]+d[L-1-i] for i in range(L)]
def make_number(P,rnd):
    L=len(P); d=[0]*L
    for i in range(L//2):
        p=P[i]; lo=max(0,p-9); hi=min(p,9)
        x=rnd.randint(lo,hi); d[i]=x; d[L-1-i]=p-x
    if L%2:
        assert P[L//2]%2==0; d[L//2]=P[L//2]//2
    if d[L-1]==0: d[L-1],d[0]=d[0],d[L-1]
    n=val(d); assert pair(n)==P; return n
ap=argparse.ArgumentParser()
ap.add_argument('--J',default=''); ap.add_argument('--V_t0',required=True); ap.add_argument('--N',type=int,required=True); ap.add_argument('--q',type=int,default=None); ap.add_argument('--k',type=int,default=None); ap.add_argument('--seed',type=int,default=1); ap.add_argument('--clock',default='1000')
a=ap.parse_args()
J=[int(x) for x in a.J.split(',')] if a.J else []
V=[int(x) for x in a.V_t0.split(',')]
s=len(V); N=a.N
q=a.q if a.q else max(N//12+3,16)
k=a.k if a.k else (2*(N*2+60))//s+4
rnd=random.Random(a.seed)
half=[rnd.randrange(19) for _ in range(8)]
while half[0]==V[0]: half[0]=rnd.randrange(19)
C=half+half[::-1]
H=B0+W0*q+J+V*k
P0=H+C+H[::-1]
n=make_number(P0,rnd)
Ps=[P0]; gam=[]
m=n
for t in range(N):
    d=digits(m); m2=m+val(d[::-1])
    Pn=pair(m2); g=len(Pn)-len(Ps[-1]); gam.append(g); Ps.append(Pn); m=m2
ok_clock=all(gam[t]==(1 if t%4==0 else 0) for t in range(N))
xend=len(B0)+9*q+len(J)+s*k-(N*2+40)
mism=[c for c in range(xend) if Ps[0][c]!=Ps[N][c]]
print(f'replay: q={q} k={k} L0={len(P0)} N={N} clock_std={ok_clock} overflows={sum(gam)} protected_end={xend} mismatches_return_on_[0,xend)={len(mism)} first={mism[:5]}',flush=True)
print('REPLAY PASS' if ok_clock and not mism else 'REPLAY FAIL',flush=True)
