"""Finite-core pumping PAPER PROOF controls, standalone Python 3.

Usage from repo root:
  python3 calculation/decimal_frontier/finite_core_pumping/finite_core_check.py .

Symbolic finite-edge tests are independently cross-checked by integer
reverse-and-add, canonical base conversion, and exact pair-word equality.
Does not check Lean and does not claim a decimal certificate.
"""
from pathlib import Path
import random
import re
import sys


def norm(word, base, carry=0):
    out = []
    for x in word:
        carry, digit = divmod(x + carry, base)
        out.append(digit)
    return out, carry


def band(W, n):
    assert W and n >= 0
    return [W[i % len(W)] for i in range(n)]


def templ(B, W, C, n):
    X = band(W, n)
    return B + X + C + X[::-1] + B[::-1]


def zipadd(A, B):
    assert len(A) == len(B)
    return [x + y for x, y in zip(A, B)]


def signature(b, B, W, C, rho):
    assert b >= 2 and B and B[0] and W and 0 <= rho < len(W)
    assert C == C[::-1] and all(0 <= x <= 2*(b-1) for x in B+W+C)
    U = W[:rho]
    DB, e = norm(B, b)
    X, c = norm(W, b, e)
    Y, c2 = norm(W, b, c)
    T, d = norm(U+C+U[::-1], b, c)
    Z0, h = norm(W[::-1], b, d)
    Z, h2 = norm(W[::-1], b, h)
    DR, gam = norm(B[::-1], b, h)
    assert c == c2 and h == h2 and gam in (0, 1)
    A = DB + X
    R = Z[gam:] + Z[:gam]
    M = Y + T + Z0 + Z[:gam]
    F = Z[gam:] + DR + ([1] if gam else [])
    assert len(A) == len(F) and len(Y) == len(R)
    return dict(A=A, Y=Y, M=M, R=R, F=F,
                H=zipadd(A,F[::-1]), Q=zipadd(Y,R[::-1]),
                K=zipadd(M,M[::-1]), gamma=gam)


def edge(b, source, target, delta):
    B,W,C,rho = source
    B2,Q,C2,rho2 = target
    if not Q or len(W)!=len(Q) or not B2 or B2[0]==0 or C2!=C2[::-1]:
        return False
    if any(x<0 or x>2*(b-1) for x in B2+Q+C2):
        return False
    m=len(W); n=2*m+rho+delta
    if n<0 or rho2!=n%m:
        return False
    try:
        S=signature(b,B,W,C,rho)
    except AssertionError:
        return False
    if S['A']==S['F'][::-1] or S['Q']!=Q:
        return False
    H,K=S['H'],S['K']
    E=band(Q,n); K2=E+C2+E[::-1]
    if H[:len(B2)]==B2:
        T=H[len(B2):]
        return T+Q==Q+T and K2==T+K+T[::-1]
    if B2[:len(H)]==H:
        T=B2[len(H):]
        return T+Q==Q+T and K==T+K2+T[::-1]
    return False


def mkbase9(C0, rho0, shifts):
    B0=[8,9,10,13,14,12,3,14,10,0,11,7,10,9,7,8,8,14,15,2,
        9,7,0,5,8,3,8,11,8,6,8,7,5,14,11,3,9,3,8,14,7,12,8,
        2,0,12,1,5,13,8,1,16,15,9,1,7,6,2,1,15,15]
    S0=(B0,[1,1,15,15],C0,rho0)
    current=S0; edges=[]
    for delta in shifts:
        B,W,C,rho=current
        s=signature(9,B,W,C,rho)
        assert len(s['H'])==len(B0)+len(W)
        B2=s['H'][:-len(W)]
        T=s['H'][-len(W):]
        Q=s['Q']
        assert T+Q==Q+T
        n=2*len(W)+rho+delta
        K2=T+s['K']+T[::-1]
        E=band(Q,n)
        assert K2[:n]==E and K2[-n:]==E[::-1]
        C2=K2[n:-n]
        target=(B2,Q,C2,(rho+delta)%len(W))
        assert edge(9,current,target,delta)
        edges.append((current,target,delta))
        current=target
    assert current==S0 and sum(s for _,_,s in edges)>=0
    return edges


def base26():
    Q=[24,28,19,36,30,15,19,12]
    R=[49,4,40,21,9,31,38,25]
    A=[32,20,20,32]; B=[12,41,41,12]
    C=[38,28,32,28,38]; D=[25,6,14,6,25]
    states=[(Q,[25],A,0),(R,[25],B,0),(Q,[25],C,0),(R,[25],D,0)]
    shifts=[0,0,0,1]
    result=[(states[i],states[(i+1)%4],shifts[i]) for i in range(4)]
    assert all(edge(26,*e) for e in result)
    altered=(states[1][0],states[1][1],[12,41,40,12],states[1][3])
    assert not edge(26,states[0],altered,0)
    return result


def from_digits(D, b):
    n=0
    for x in D[::-1]:
        n=b*n+x
    return n


def to_digits(n,b):
    D=[]
    while n:
        n,r=divmod(n,b)
        D.append(r)
    return D


def replay(b, edges, l0, steps):
    N=from_digits(templ(*edges[0][0][:3],l0),b)
    length=l0
    m=len(edges[0][0][1])
    for t in range(steps):
        src,dst,delta=edges[t%len(edges)]
        assert length>=2*m and length % m == src[3]
        P=templ(*src[:3],length)
        assert N==from_digits(P,b),('template',t)
        D=to_digits(N,b)
        assert D!=D[::-1],('palindrome',t)
        expected=zipadd(D,D[::-1])
        N2=N+from_digits(D[::-1],b)
        assert N2==from_digits(expected,b),('integer',t)
        length+=delta
        assert expected==templ(*dst[:3],length),('pair',t)
        N=N2
    return length


def base13_existing(repo,variant,steps=300):
    p=repo/'lean/P196/AbsorbingBand'/('Base13.lean' if variant==0 else 'Base13b.lean')
    txt=p.read_text()
    Bs=[]
    for j in range(10):
        m=re.search(r'def B%d : List Nat := \[([^\]]+)\]' % j,txt)
        assert m
        Bs.append([int(x) for x in re.findall(r'\d+',m.group(1))])
    c=16 if variant==0 else 8
    l=1; N=from_digits(Bs[0]+[c]+Bs[0][::-1],13); g=[]
    for t in range(steps):
        B=Bs[t%10]; P=B+[c if t%2==0 else 24-c]*l+B[::-1]
        assert N==from_digits(P,13)
        D=to_digits(N,13)
        assert D!=D[::-1]
        N2=N+from_digits(D[::-1],13)
        assert N2==from_digits(zipadd(D,D[::-1]),13)
        gam=int(len(D)>len(P))
        if t<10:g.append(str(gam))
        N=N2; l+=gam
    assert ''.join(g)=='1010010000'
    return len(Bs[0])


def randomized(n=2000):
    rng=random.Random(190474)
    for i in range(n):
        b=rng.randint(2,36); m=rng.randint(1,7)
        W=[rng.randint(0,2*b-2) for _ in range(m)]
        B=[rng.randint(1,2*b-2)]+[rng.randint(0,2*b-2) for _ in range(rng.randint(0,7))]
        h=[rng.randint(0,2*b-2) for _ in range(rng.randint(0,6))]
        C=h+h[::-1] if rng.randrange(2) else h+[rng.randint(0,2*b-2)]+h[::-1]
        rho=rng.randrange(m); S=signature(b,B,W,C,rho)
        for k in (0,1,3,8):
            P=templ(B,W,C,m*(k+2)+rho)
            D=to_digits(from_digits(P,b),b)
            assert D==S['A']+S['Y']*k+S['M']+S['R']*k+S['F'],('digits',i,k)
            assert zipadd(D,D[::-1])==S['H']+S['Q']*k+S['K']+S['Q'][::-1]*k+S['H'][::-1],('pairs',i,k)
    return n*4


def main():
    repo=Path(sys.argv[1] if len(sys.argv)>1 else '.')
    base26_edges=base26()
    assert replay(26,base26_edges,2,600)==152
    shift=[0,1,0,0,0,0,1,0,0,0]*2
    small=mkbase9([],1,shift)
    assert max(len(s[0][2]) for s in small)<=1
    assert replay(9,small,9,2000)==409
    large=mkbase9([15,15],2,[1,1,0,0,0,0,0,0,0,0]*2)
    assert replay(9,large,10,2000)==410
    if (repo/'lean/P196/AbsorbingBand/Base13.lean').exists():
        assert base13_existing(repo,0)==75 and base13_existing(repo,1)==55
        print('BASE13_CONTROLS_PASS: 75/55, 300 steps each')
    else:
        print('BASE13_CONTROLS_UNAVAILABLE: supply repo root as argument')
    cases=randomized()
    print('PAPER_PROOF_CONTROLS_PASS: b9 2x2000, b26 600, random digit/pair checks',cases)


if __name__=='__main__':
    main()
