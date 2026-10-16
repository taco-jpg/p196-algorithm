"""Exact quadratic spectral coordinate for decimal pair-sum dynamics.
Research aid only: does not establish a decimal Lychrel number.
All arithmetic and verification below are integers.
"""
from itertools import product
import random

def qstep(q):
    carry=0; cs=[]; digits=[]
    for x in q:
        z=x+carry; digits.append(z%10); carry=z//10; cs.append(carry)
    if carry: digits.append(carry)
    return tuple(a+b for a,b in zip(digits,reversed(digits))), tuple(cs), carry

def rec(a,b,count):
    out=[a,b]
    while len(out)<count: out.append(20*out[-1]-out[-2])
    return out[:count]

def coordinate(q):
    L=len(q); m=L//2
    if L%2:
        t=rec(2,20,m+1)
        return q[m]+sum(q[i]*t[m-i] for i in range(m))
    r=rec(1,19,m)
    return sum(q[i]*r[m-1-i] for i in range(m))

def carry_coordinates(cs):
    L=len(cs); m=L//2
    if L%2:
        t=rec(2,20,m+1); u=rec(0,1,m+1)
        H=cs[m]+sum((cs[i]+cs[L-1-i])*(t[m-i]//2) for i in range(m))
        J=sum((cs[L-1-i]-cs[i])*u[m-i] for i in range(m))
    else:
        r=rec(1,19,m); s=rec(1,21,m)
        H=sum((cs[i]+cs[L-1-i])*r[m-1-i] for i in range(m))
        J=sum((cs[L-1-i]-cs[i])*s[m-1-i] for i in range(m))
    return H,J

def predicted(q,cs,h):
    A=coordinate(q); H,J=carry_coordinates(cs)
    if len(q)%2:
        return A-9*H+99*J if h else 2*A+198*J
    return 22*A-99*H+99*J if h else 2*A+9*J

def verify(q):
    q=tuple(q)
    assert q==q[::-1] and q[0]>0
    nq,cs,h=qstep(q)
    assert coordinate(nq)==predicted(q,cs,h), (q,nq,cs)
    # Carry asymmetry is confined to neutral (9) columns.
    assert all(cs[i]==cs[-1-i] or q[i]==9 for i in range(len(q)))
    if 9 not in q: assert carry_coordinates(cs)[1]==0

def main():
    tested=0
    for L in range(1,8):
        m=(L+1)//2
        for p in product(range(19),repeat=m):
            if not p[0] or (L%2 and p[-1]%2): continue
            q=p+p[-2::-1] if L%2 else p+p[::-1]
            verify(q); tested+=1
    rng=random.Random(196)
    for _ in range(10000):
        L=rng.randrange(2,200); m=(L+1)//2
        p=[rng.randrange(19) for _ in range(m)]; p[0]=rng.randrange(1,19)
        if L%2: p[-1]=2*rng.randrange(10)
        q=p+p[-2::-1] if L%2 else p+p[::-1]
        verify(q); tested+=1
    print(f'Exact identities verified on {tested} canonical symmetric q words.')
    n=196
    for k in range(16):
        digits=tuple(map(int,str(n)[::-1]));q=tuple(a+b for a,b in zip(digits,digits[::-1]))
        nq,cs,h=qstep(q); H,J=carry_coordinates(cs)
        print(dict(k=k,n=n,L=len(q),A=coordinate(q),H=H,J=J,overflow=h))
        n+=int(str(n)[::-1])
if __name__=='__main__': main()
