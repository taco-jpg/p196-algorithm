#!/usr/bin/env python3
"""Independent ordinary decimal integer test of all 2^k three-step fibres."""
import argparse, itertools
from pathlib import Path

def load(path):
    it=iter(map(int,Path(path).read_text().split()))
    p,nb,m,b=(next(it) for _ in range(4))
    assert (p,nb,m,b)==(12,34,9,10)
    gamma=[next(it) for _ in range(p)]
    W=[[next(it) for _ in range(m)] for _ in range(p)]
    for _ in range(p*m):next(it) # carry rows
    B=[[next(it) for _ in range(nb)] for _ in range(p)]
    assert next(it,None)is None
    return gamma,W,B

def pairword(t,n,W,B):
    out=[0]*n
    for i in range((n+1)//2):
        q=B[t][i] if i<34 else W[t][(i-34)%9]
        if n&1 and i==n//2 and q&1:q+=1 if q<18 else -1
        out[i]=out[n-1-i]=q
    return out

def seed(P):
    n=len(P); d=[0]*n
    for i in range((n+1)//2):
        q=P[i]
        if i==n-1-i:
            assert q%2==0; d[i]=q//2
        else:
            hi=max(q-9,1 if i==0 else 0)
            lo=q-hi
            assert 0<=lo<=9 and 1<=hi<=9 if i==0 else 0<=hi<=9 and 0<=lo<=9
            d[i]=lo;d[n-1-i]=hi
    assert d[-1]!=0
    return int(''.join(str(x) for x in reversed(d)))

def pair_of_number(n):
    s=str(n)
    return tuple(int(a)+int(b) for a,b in zip(reversed(s),s))

def R(n):return n+int(str(n)[::-1])

def run(k,phase=3,residue=0):
    gamma,W,B=load(Path(__file__).resolve().parent/'lattice_input.txt')
    assert (phase,residue)==(3,0)
    n=200+18*k
    assert gamma[3]==0 and gamma[4]==1
    P=pairword(phase,n,W,B)
    js=[52+9*i for i in range(k)]
    assert js[-1]+30<n//2
    motif=(8,10,12)
    for j in js:
        assert (j-34)%9==0
        assert all(P[j+a]!=motif[a] for a in range(3))
    baseline=seed(P); target=R(R(R(baseline)))
    states_at_2=set()
    result_count=0
    for mask in range(1<<k):
        q=P[:]
        for b,j in enumerate(js):
            if mask>>b&1:
                for a,v in enumerate(motif):q[j+a]=q[n-j-a-1]=v
        integer=seed(q)
        assert pair_of_number(integer)==tuple(q)
        t1=R(integer); t2=R(t1); t3=R(t2)
        assert len(str(t1))==n
        assert len(str(t2))==n+1
        assert t3==target,(k,mask,t3-target)
        assert t2 not in states_at_2,(k,mask,'collision before third step')
        states_at_2.add(t2)
        result_count+=1
    assert result_count==2**k and len(states_at_2)==2**k
    print(f'INDEPENDENT_BIGINT_FIBRE_PASS k={k} length={n} distinct_at_second={result_count} one_third_integer=True')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('k',nargs='?',type=int,default=12)
    a=parser.parse_args();run(a.k)
