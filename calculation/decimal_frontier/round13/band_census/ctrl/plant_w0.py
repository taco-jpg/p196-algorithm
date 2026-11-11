#!/usr/bin/env python3
import os
"""r13a planted positive control: the genuine T12 exterior B0 W0^q (q large) with the true band start y* = 31 (W0 rotation word=(4,0,5,5,18,4,8,1,15)) gives a solution of L for R up to 12.
Check: L instance with free cells fixed to the genuine letters and ports fixed to the genuine carries/high digits is SAT and the model reproduces the genuine letters in the window; and the band is correct on [y,inf) at T=12."""
import sys
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import bandsat as BS, random
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
def pair(n,b=10):
    d=digits(n,b); L=len(d)
    return [d[i]+d[L-1-i] for i in range(L)]
def make_number(P,rnd,b=10):
    L=len(P); d=[0]*L
    for i in range(L//2):
        p=P[i]; lo=max(0,p-(b-1)); hi=min(p,b-1)
        x=rnd.randint(lo,hi); d[i]=x; d[L-1-i]=p-x
    if L%2:
        assert P[L//2]%2==0; d[L//2]=P[L//2]//2
    if d[L-1]==0: d[L-1],d[0]=d[0],d[L-1]
    n=val(d,b); assert pair(n,b)==P; return n
rnd=random.Random(1)
q=14; 
# centre: the mirror of the band directly (any symmetric continuation), keep W band long: use P = B0 W0^q X mirror where X = W0^k (long) + centre
k=40
Cw=[rnd.randrange(19) for _ in range(6)]
H=B0+W0*q+W0*k
P0=H+Cw+Cw[::-1]+H[::-1]
n=make_number(P0,rnd)
T=12
Ps=[]; ALs=[]; HLs=[]; gam=[]
m=n
R=12
y=31
for t in range(T+1):
    P=pair(m); Ps.append(P)
    if t==T: break
    L=len(P)
    c=[0]*(L+1); e=[0]*L
    for i in range(L):
        z=P[i]+c[i]; e[i]=z%10; c[i+1]=1 if z>=10 else 0
    g=c[L]; gam.append(g)
    ALs.append(c[y-R])
    HLs.append(e[L-1-(y-R-1)] if g else None)
    m=m+val(digits(m)[::-1])
assert gam==[1 if t%4==0 else 0 for t in range(T)], gam
word=[4,0,5,5,18,4,8,1,15]
assert Ps[0][y:y+9]==word and Ps[0][y-1]==6
E,X,AL,BE,HL,info=BS.build_L(10,word,gam,R,foreign=True,g_final=0,trim=True,solver='kissat404')
# plant the genuine free cells and ports
for c in range(R): E.add([X[0][c][Ps[0][y-R+c]]])
for s in range(T):
    E.add([AL[s][0] if ALs[s] else -AL[s][0]])
    if gam[s]: E.add([HL[s][HLs[s]]])
r=E.S.solve()
print('planted W0 L instance (genuine letters/ports at y-R..):', 'SAT' if r else 'UNSAT', flush=True)
assert r
m2=set(l for l in E.S.get_model() if l>0)
N=info['N']
mism=sum(1 for s in range(T+1) for c in range(N) if BS.letter_of(m2,X[s][c])!=[Ps[s][y-R+c]])
print('model vs genuine letters mismatches:',mism,'of',(T+1)*N,flush=True)
assert mism==0
print('PLANT PASS',flush=True)
