#!/usr/bin/env python3
"""r13a: exact big-integer replay of a full template candidate: P = X + band + C + mirror.
band letters: at offset o >= 0 after X the letter is Vtau[(re + o) mod s] (Vtau = band row at time 0, rotation re at column w=|X|);
the centre word C starts after band length L0 = t_a + s*m where t_a = ((rc - re) mod s), with rc the rotation of the centre instance's window word.
Template parameter k = m: after N steps the expected word is the same with m -> m + j.  Replay: exact integers, big k.
usage: fullreplay.py --X x0,x1,... --Vtau a,b,c --re r --rc r --C c... --N 24 --j 1 --mstart 60 --returns 3 [--clock 1000]"""
import sys, argparse
ap=argparse.ArgumentParser()
ap.add_argument('--X',required=True); ap.add_argument('--Vtau',required=True); ap.add_argument('--re',type=int,required=True); ap.add_argument('--rc',type=int,required=True); ap.add_argument('--C',default=''); ap.add_argument('--N',type=int,required=True); ap.add_argument('--j',type=int,required=True); ap.add_argument('--mstart',type=int,default=60); ap.add_argument('--returns',type=int,default=3); ap.add_argument('--clock',default='1000'); ap.add_argument('--b',type=int,default=10)
a=ap.parse_args()
b=a.b
X=[int(x) for x in a.X.split(',')] if a.X else []
V=[int(x) for x in a.Vtau.split(',')]; s=len(V)
C=[int(x) for x in a.C.split(',')] if a.C else []
def word(m):
    ta=(a.rc-a.re)%s
    L=ta+s*m
    band=[V[(a.re+o)%s] for o in range(L)]
    H=X+band
    return H+C+H[::-1]
def digits(n):
    d=[]
    while n: d.append(n%b); n//=b
    return d or [0]
def val(d):
    n=0
    for x in reversed(d): n=n*b+x
    return n
def pair(n):
    d=digits(n); L=len(d)
    return [d[i]+d[L-1-i] for i in range(L)]
def tonumber(P):
    L=len(P); d=[0]*L
    for i in range(L//2):
        p=P[i]; x=min(p,b-1); d[i]=x; d[L-1-i]=p-x
    if L%2: 
        if P[L//2]%2: raise ValueError('odd middle letter')
        d[L//2]=P[L//2]//2
    if d[L-1]==0: d[0],d[L-1]=d[L-1],d[0]
    assert d[L-1]>=1, 'leading digit 0 not fixable'
    n=val(d); assert pair(n)==P; return n
n=tonumber(word(a.mstart))
ok=True
m=a.mstart
for ret in range(a.returns):
    for t in range(a.N):
        n=n+val(digits(n)[::-1])
    Pn=pair(n); m+=a.j
    tgt=word(m)
    same=Pn==tgt
    print(f'return {ret+1}: after {a.N*(ret+1)} steps, m={m}: length {len(Pn)} (target {len(tgt)}): {"MATCH" if same else "MISMATCH"}',flush=True)
    if not same:
        d=[i for i in range(min(len(Pn),len(tgt))) if Pn[i]!=tgt[i]]
        print('  first differences',d[:8],'of',len(d)); ok=False
        break
print('FULLREPLAY', 'PASS' if ok else 'FAIL')
