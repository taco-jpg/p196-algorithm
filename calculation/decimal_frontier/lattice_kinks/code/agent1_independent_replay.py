#!/usr/bin/env python3
"""Independent finite bigint replay for decimal p8 rec0 SAT survivors.

Run from repository root:
  python3 calculation/decimal_frontier/lattice_kinks/code/agent1_independent_replay.py 9 0 36 /path/to/positive_witness.json

The JSON must contain {"initial_layer": [K centre-frame pair digits], "K": K}.
The arithmetic below uses only Python's decimal big integers and a separate
SCC parser. It neither imports SAT encoding nor its carry recurrence.
Not a proof of indefinite palindrome avoidance.
"""
import json
import re
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
G=[1,0,1,0,1,0,1,0]


def exterior():
    lines=(ROOT/'calculation/decimal_frontier/lattice_formats/p8_scc.txt').read_text().splitlines()
    line=next(x for x in lines if x.startswith('SCC p=8 g=10101010 '))
    def extract(prefix, upto=None):
        s=line.split(prefix,1)[1]
        if upto is not None:s=s.split(upto,1)[0]
        cols=[[int(z) for z in tok.split(',')] for tok in re.findall(r'\[([^\]]+)\]',s)]
        return [[col[t] for col in cols] for t in range(8)]
    B=extract(' path=',' cyc=')
    W=extract(' cyc=')
    assert len(B)==8 and len(B[0])==39 and len(W[0])==20
    assert B[0][:4]==[17,5,0,1] and W[0][:4]==[17,3,1,13]
    return B,W


def pair_of_number(N):
    digits=[int(c) for c in str(N)[::-1]]
    return [digits[j]+digits[-1-j] for j in range(len(digits))]


def seed_from_pairs(P):
    n=len(P)
    assert P==P[::-1] and all(0<=x<=18 for x in P)
    d=[0]*n
    for i in range(n//2):
        x=P[i]
        d[i]=min(x,9)
        d[-1-i]=x-d[i]
    if n%2:
        assert P[n//2]%2==0
        d[n//2]=P[n//2]//2
    assert d[-1]>0 and all(0<=x<=9 for x in d)
    return int(''.join(str(x) for x in d[::-1]))


def replay(w,o,H,json_path):
    B,W=exterior()
    n0=400+o
    K=w+6
    half=(n0+1)//2
    p=json.loads(Path(json_path).read_text())
    layer=p['initial_layer']
    assert len(layer)==p['K']==K
    lower=[B[0][j] if j<39 else W[0][(j-39)%20] for j in range(half)]
    assert lower[half-K:half-w]==layer[:6]
    lower[half-K:]=layer
    P=lower+lower[:n0//2][::-1] if n0%2 else lower+lower[::-1]
    N=seed_from_pairs(P)
    assert pair_of_number(N)==P
    palindrome_steps=[]
    for t in range(H+1):
        digits_text = str(N)
        if digits_text == digits_text[::-1]:
            palindrome_steps.append(t)
            raise AssertionError(('unexpected palindrome in finite survivor', t, len(digits_text)))
        q=pair_of_number(N)
        assert q == q[::-1], ('pair-word symmetry',t)
        n=len(q)
        assert n==n0+sum(G[j%8] for j in range(t)),('overflow schedule',t,n)
        half=(n+1)//2
        for j in range(39):
            assert q[j]==B[t%8][j],('B mismatch',t,j,q[j],B[t%8][j])
        for j in range(39,half-K+6):
            assert q[j]==W[t%8][(j-39)%20],('bulk mismatch',t,j)
        if t<H:
            N+=int(str(N)[::-1])
    print(f'PASS width={w} o={o} H={H}, decimal big-integer pair-word and full exterior; palindrome_steps={palindrome_steps}',flush=True)


if __name__=='__main__':
    if len(sys.argv)!=5:
        raise SystemExit('usage: replay.py width phase horizon witness.json')
    replay(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
