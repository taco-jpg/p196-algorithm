#!/usr/bin/env python3
# Independent Python check of tower death levels: chain of interfaces (Lemma I1), memoised D, for a random sample of towers with small K.
# usage: py_chain.py g L deaths.txt nsample maxK seed
# deaths.txt lines: idx K c|xb|A   (r13c format) ; compares K(py) = D+1 with K(r13c)
import sys, random
from functools import lru_cache
sys.setrecursionlimit(100000)
g=[int(ch) for ch in sys.argv[1]]; L=int(sys.argv[2]); deaths=sys.argv[3]; n=int(sys.argv[4]); maxK=int(sys.argv[5]); seed=int(sys.argv[6])
b=10; NV=19; P=len(g)
def closed_cols(c,xb,A):
    # all closed L-columns above interface (c,xb,A), returns list of (v_tuple, A'_tuple)
    # step function
    def succ(t,v):
        res={}
        for h in (0,1):
            H=(v+h)//b
            if not (A[t]>>H)&1: continue
            if g[t%P]: part=(xb[t]+H)%b
            else: part=(v+h)%b
            y=(v+c[t])%b+part
            res[y]=res.get(y,0)|(1<<h)
        return res
    # backward reach sets to each end digit
    R=[[0]*NV for _ in range(L+1)]
    for v in range(NV): R[L][v]=1<<v
    S=[[None]*NV for _ in range(L)]
    for t in range(L-1,-1,-1):
        for v in range(NV):
            s=succ(t,v); S[t][v]=s
            m=0
            for y in s: m|=R[t+1][y]
            R[t][v]=m
    out=[]
    for v0 in range(NV):
        if not (R[0][v0]>>v0)&1: continue
        col=[v0]; ms=[]
        def dfs(t):
            if t==L:
                if col[L]==v0: out.append((tuple(col[:L]),tuple(ms)))
                return
            for y,m in S[t][col[t]].items():
                if (R[t+1][y]>>v0)&1:
                    col.append(y); ms.append(m); dfs(t+1); col.pop(); ms.pop()
        dfs(0)
    return out
memo={}
def D(c,xb,A):
    key=(c,xb,A)
    if key in memo:
        return memo[key]
    memo[key]=-1 # guard: cycle would loop
    best=0
    for v,ms in closed_cols(c,xb,A):
        c2=tuple((v[t]+c[t])//b for t in range(L))
        xb2=tuple((v[t]%b) if g[t%P] else 0 for t in range(L))
        d=D(c2,xb2,ms)
        best=max(best,d+1)
    memo[key]=best
    return best
lines=[l.split() for l in open(deaths)]
rng=random.Random(seed); rng.shuffle(lines)
checked=0; bad=0; 
for parts in lines:
    if len(parts)<3: continue
    K=int(parts[1]); 
    if K>maxK: continue
    spec=parts[2]; cs,xs,As=spec.split('|'); xb=tuple(int(x) for x in xs.rstrip(',').split(','));c=tuple(int(ch) for ch in cs);A=tuple(int(ch) for ch in As)
    xb=tuple(x%b for x in xb) # xb mod b (exact)
    d=D(c,xb,A)
    if d+1!=K:
        bad+=1; print('DIFF',spec[:60],'py',d+1,'r13c',K)
    checked+=1
    if checked>=n: break
print(f'py_chain: g={sys.argv[1]} L={L}: checked {checked} towers (K<={maxK}), mismatches {bad}')
