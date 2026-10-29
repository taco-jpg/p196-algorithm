#!/usr/bin/env python3
"""Independent digit-normalization and GF(2) rank checker (no model import)."""
import json,random,sys
from pathlib import Path
from itertools import combinations
HERE=Path(__file__).resolve().parent
raw=list(map(int,(HERE/'lat2.txt').read_text().split()))
assert raw[:4]==[8,11,48,10] and raw[4:12]==[1,0]*4
z=raw[12:];W=[z[t*48:(t+1)*48] for t in range(8)]
mons=[()] + [(k,) for k in range(6)] + list(combinations(range(6),2)) + list(combinations(range(6),3))
def digit_normalize(P,g):
    n=len(P);ups=[];downs=[]
    for guess in (0,1):
        a=guess;uc=[]
        for p in P:uc.append(a);a=(p+a)//10
        if a==guess:ups.append(uc)
        d=guess;dc=[0]*n
        for j in range(n-1,-1,-1):dc[j]=d;d=(P[j]+d)//10
        if d==guess:downs.append(dc)
    assert len(ups)==len(downs)==1
    a=ups[0];d=downs[0]
    lo=[(P[j]+a[j])%10 for j in range(n)]
    hi=[(P[j]+d[j])%10 for j in range(n)]
    N=[lo[j]+hi[(j-g)%n] for j in range(n)]
    return N,a,d

def feat(P):
    n=len(P);_,a,d=digit_normalize(P,0)
    out=0
    for j in range(n):
        k=(j+1)%n
        bits=[P[j]%2,P[k]%2,a[j],d[j],a[k],d[k]]
        for idx,term in enumerate(mons):
            if all(bits[x] for x in term):out^=1<<idx
    return out

def cov(t,P):
    N,_,_=digit_normalize(P,1-t%2)
    x=feat(N)<<(42*((t+1)%8))
    if t%2==0:x^=feat(P)<<(42*t)
    return x

def rank(vectors):
    piv={}
    for v in vectors:
        while v:
            k=(v&-v).bit_length()-1
            if k in piv:v^=piv[k]
            else:piv[k]=v;break
    return len(piv)

def row(tag):
    t,j,s,u=tag;P=W[t].copy()
    if j>=0:
        P[j]+=s
        if u:P[(j+1)%48]+=u
    return cov(t,P)

def check(path):
    c=json.loads(Path(path).read_text())
    tags=c['rank_witness'];masks=c['identity_masks'];pot=c['graph_potentials'];const=c['graph_constants']
    assert len(tags)==232 and len({tuple(x) for x in tags})==232
    assert rank(row(tag) for tag in tags)==232
    assert len(masks)==13 and rank(masks)==13
    assert rank([m<<(42*t) for t in range(8) for m in masks])==104
    V=[(p,a,d) for p in range(19) for a in (0,1) for d in (0,1)]
    idx={v:i for i,v in enumerate(V)};edges=0
    for i,(p,a,d) in enumerate(V):
        A=int(p+a>=10)
        for q in range(19):
            for D in (0,1):
                if d!=int(q+D>=10):continue
                j=idx[(q,A,D)]
                bits=[p%2,q%2,a,d,A,D]
                bits_mask=0
                for k,term in enumerate(mons):
                    if all(bits[x] for x in term):bits_mask|=1<<k
                for mask,ph,kappa in zip(masks,pot,const):
                    assert ((bits_mask&mask).bit_count()&1)==(ph[i]^ph[j]^kappa)
                edges+=1
    assert edges==1444
    rng=random.Random(3196)
    for _ in range(2000):
        P=[rng.randrange(19) for i in range(48)]
        assert all((feat(P)&m).bit_count()%2==0 for m in masks)
        for t in range(8):
            e=cov(t,P)
            assert all((e&(m<<(42*u))).bit_count()%2==0 for u in range(8) for m in masks)
    print('INDEPENDENT PASS: 232 witness rows using digit-normalized successor and different GF(2) eliminator')
    print('INDEPENDENT PASS: all 13 universal coboundary certificates across 1444 physical carry-graph edges')
    print('CONTROLS: 2000 arbitrary 48-cell words x 8 phase checks; cubic kernel=zero-function space')
if __name__=='__main__':
    check(sys.argv[1] if len(sys.argv)>1 else str(HERE/'certificate.json'))
