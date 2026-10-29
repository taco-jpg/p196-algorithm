#!/usr/bin/env python3
"""S20 independent exact-decimal arithmetic controls; not a certificate."""
from pathlib import Path
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
assert len(B)==34 and len(W)==9 and sum(B)==307 and sum(W)==60
source=Path(__file__).resolve().parents[3]/"calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
if source.exists():
    r=list(map(int,source.read_text().split()))
    p,bl,wl,base=r[:4]
    assert (p,bl,wl,base)==(12,34,9,10)
    assert W==r[4+p:4+p+wl] and B==r[4+p+2*p*wl:4+p+2*p*wl+bl]
def template(q,k,J,U,C):
    assert len(U)==3 and sum(U)==27 and C==C[::-1]
    h=B+W*q+J+U*k
    return h+C+h[::-1]
def value(d):
    n=0
    for a in reversed(d):n=10*n+a
    return n
def realize(p):
    d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i]);lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo;d[-1-i]=hi
    if len(d)%2:
        mid=p[len(d)//2]
        assert mid%2==0
        d[len(d)//2]=mid//2
    assert d[-1]
    return d
def schoolbook(d):
    o=[];carry=0;total=0
    for i,x in enumerate(d):
        z=x+d[-1-i]+carry
        carry=z//10
        total+=carry
        o.append(z%10)
    if carry:o.append(carry)
    return o,total
def modval(p):
    s=0;power=1
    for x in p:
        s=(s+x*power)%81
        power=10*power%81
    return s
def projection(p):
    assert p==p[::-1]
    s=sum(p);N=len(p)
    assert ((N-1)*s)%2==0
    return (s+9*((N-1)*s//2))%81
def run(label,J,U,C,q,k):
    p0=template(q,k,J,U,C);d=realize(p0);n=value(d)
    assert [d[i]+d[-1-i] for i in range(len(d))]==p0
    S0=sum(p0);K=0;gamma=[]
    for t in range(120):
        before=2*sum(d);length=len(d)
        nxt,c=schoolbook(d)
        gamma.append(len(nxt)-length)
        assert 2*sum(nxt)==2*before-18*c
        K=(K+pow(2,119-t,9)*c)%9
        n=n+int(str(n)[::-1])
        assert n==value(nxt), (label,q,k,t)
        d=nxt
    assert gamma==[1,0,0,0]*30
    S120=2*sum(d)
    assert (pow(2,120,81)*S0-18*K-S120)%81==0
    pair=[x+d[-1-i] for i,x in enumerate(d)]
    target=template(q,k+5,J,U,C)
    assert projection(p0)==modval(p0)
    assert projection(pair)==modval(pair)
    assert projection(target)==modval(target)
    assert len(target)==len(p0)+30 and sum(target)==S0+270
    assert (modval(target)-modval(p0))%81==(27+54*S0)%81
    need=(8+3*q+5*sum(J)+7*sum(C))%9
    assert need==(7*S0-6)%9
    if pair==target:assert K==need
    print(label,q,k,"carry9",K,"required",need,"return",pair==target)
def main():
    cases={
      "R02":([12,14,9,16,2,4,3,11,10,11,4,11,8,8,10,9,7,9,16],[8,9,10],[5,12,5]),
      "even":([5],[9,2,16],[1,1]),
      "odd":([6],[9,2,16],[12])
    }
    for label,(J,U,C) in cases.items():
        for q,k in ((20,20),(21,23),(40,40),(80,80),(160,160)):
            run(label,J,U,C,q,k)
    for q,k in ((20,20),(21,23),(37,42)):
        a=template(q,k,[1],[9,0,18],[12])
        b=template(q,k+5,[10],[9,0,18],[12])
        assert (modval(b)-modval(a))%81==(27+18+54*sum(a))%81
    print("PASS: 15 ordinary-decimal 120-step replays, independent engines.")
if __name__=="__main__":main()
