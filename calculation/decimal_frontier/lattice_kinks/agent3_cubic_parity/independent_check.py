#!/usr/bin/env python3
"""Independent decimal digit-normalization checker; no import from model.py."""
import json,random,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parent
raw=list(map(int,(ROOT/'lat2.txt').read_text().split()))
assert raw[:12]==[8,11,48,10,1,0,1,0,1,0,1,0]
P0=[raw[12+48*t:12+48*(t+1)] for t in range(8)]
MON=[()]+[(j,) for j in range(6)]+list(itertools.combinations(range(6),2))+list(itertools.combinations(range(6),3))
assert len(MON)==42

def normalize(P):
    n=len(P);up=[];down=[]
    for s in (0,1):
        a=s;carry=[]
        for x in P:carry.append(a);a=(x+a)//10
        if a==s:up.append(carry)
        d=s;carry=[0]*n
        for j in range(n-1,-1,-1):carry[j]=d;d=(P[j]+d)//10
        if d==s:down.append(carry)
    assert len(up)==len(down)==1
    a,d=up[0],down[0]
    lo=[(P[j]+a[j])%10 for j in range(n)]
    hi=[(P[j]+d[j])%10 for j in range(n)]
    return lo,hi,a,d

def feat(P):
    lo,hi,a,d=normalize(P);acc=[0]*42;n=len(P)
    for j in range(n):
        k=(j+1)%n
        bits=[P[j]%2,P[k]%2,a[j],d[j],a[k],d[k]]
        for i,m in enumerate(MON):
            val=1
            for h in m:val&=bits[h]
            acc[i]^=val
    return sum(x<<i for i,x in enumerate(acc))

def row(t,P):
    lo,hi,_,_=normalize(P);g=1-(t%2)
    after=[lo[j]+hi[(j-g)%len(P)] for j in range(len(P))]
    v=feat(after)<<(42*((t+1)%8))
    if g:v^=feat(P)<<(42*t)
    return v

def tagged(tag):
    t,j,s,u=tag;P=P0[t].copy()
    if j>=0:
        P[j]+=s
        if u:P[(j+1)%48]+=u
    return row(t,P)

def rank(rows):
    piv={}
    for v in rows:
        while v:
            j=(v&-v).bit_length()-1
            if j not in piv:piv[j]=v;break
            v^=piv[j]
    return len(piv)

def run():
    witness=[tuple(x) for x in json.loads((ROOT/'rank_witness.json').read_text())]
    assert len(witness)==232 and rank(tagged(x) for x in witness)==232
    all_tags=[]
    for t in range(8):
        all_tags.append((t,-1,0,0))
        for j in range(48):
            for s in (-1,1):
                if 0<=P0[t][j]+s<=18:all_tags.append((t,j,s,0))
        for j in range(48):
            for s,u in itertools.product((-1,1),repeat=2):
                if 0<=P0[t][j]+s<=18 and 0<=P0[t][(j+1)%48]+u<=18:all_tags.append((t,j,s,u))
    assert len(all_tags)==2252 and rank(tagged(x) for x in all_tags)==232
    cert=json.loads((ROOT/'graph_certificate.json').read_text())
    assert len(cert['masks'])==13 and rank(cert['masks'])==13
    assert rank(m<<(42*t) for m in cert['masks'] for t in range(8))==104
    # Independent direct graph-edge evaluation of the committed potentials.
    states=[(p,a,d) for p in range(19) for a in (0,1) for d in (0,1)]
    idx={s:i for i,s in enumerate(states)}
    assert states==[tuple(s) for s in cert['states']]
    edge_count=0
    for p,a,d in states:
        u=idx[p,a,d]
        for q in range(19):
            for D in (0,1):
                A=(p+a)//10
                if d!=(q+D)//10:continue
                v=idx[q,A,D];bits=(p%2,q%2,a,d,A,D)
                for mask,(kap,phi) in zip(cert['masks'],cert['proofs']):
                    val=0
                    for i,mon in enumerate(MON):
                        if mask>>i&1:
                            product=1
                            for k in mon:product*=bits[k]
                            val^=product
                    assert val==(kap^phi[u]^phi[v])
                edge_count+=1
    assert edge_count==1444
    rng=random.Random(192003)
    for _ in range(10000):
        P=[rng.randrange(19) for _ in range(48)]
        lo,hi,a,d=normalize(P)
        f=feat(P)
        assert all((f&m).bit_count()%2==0 for m in cert['masks'])
        assert sum(a[j]*(1-a[(j+1)%48]) for j in range(48))==sum(d[j]*(1-d[(j+1)%48]) for j in range(48))
    print('INDEPENDENT PASS: 232/2252 digit-normalized covariance rank, 13 independent graph identities')
    print('INDEPENDENT PASS: all 1444 directed carry edges and 10,000 random digit-normalization controls')
if __name__=='__main__':run()
