#!/usr/bin/env python3
"""Exact two-sided decimal carry transfer graph for the p8/m20 lattice."""
from collections import defaultdict
import json, math
W=[
[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13],
[12,11,4,5,12,10,7,8,12,10,3,2,7,10,8,8,9,5,17,11],
[6,3,9,11,5,1,15,17,5,1,7,4,15,0,17,16,18,11,15,4],
[10,9,13,1,7,6,7,14,13,6,8,11,10,6,8,15,16,11,8,10],
[2,0,7,3,14,12,15,9,7,13,17,3,1,13,17,11,14,3,18,1],
[3,2,7,10,8,8,9,5,17,11,12,11,4,5,12,10,7,8,12,10],
[7,4,15,0,17,16,18,11,15,4,6,3,9,11,5,1,15,17,5,1],
[8,11,10,6,8,15,16,11,8,10,10,9,13,1,7,6,7,14,13,6]]
B0=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
def states(g):
    return [(a,r,u) for a in range(2) for r in range(2) for u in (range(10) if g else [0])]
def edges(q,g,pfix=None):
    out=defaultdict(list)
    for a,rprev,uprev in states(g):
        for p in ([pfix] if pfix is not None else range(19)):
            lo=(p+a)%10; anext=(p+a)//10
            for r in range(2):
                hi=(p+r)%10
                if (p+r)//10!=rprev:continue
                if lo+(uprev if g else hi)!=q:continue
                out[(a,rprev,uprev)].append(((anext,r,hi if g else 0),p))
    return out
def matprod(target,g,pword=None):
    ss=states(g);n=len(ss);ix={s:i for i,s in enumerate(ss)}
    M=[[int(i==j) for j in range(n)] for i in range(n)]
    for t,q in enumerate(target):
        E=edges(q,g,None if pword is None else pword[t]);M2=[[0]*n for _ in range(n)]
        for i in range(n):
            row=M[i]
            for s,outs in E.items():
                v=row[ix[s]]
                if v:
                    for to,p in outs:M2[i][ix[to]]+=v
        M=M2
    return M
def trace(M):
    return sum(M[i][i] for i in range(len(M)))
def multiply(A,B):
    n=len(A);C=[[0]*n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k]:
                for j in range(n):
                    if B[k][j]:C[i][j]+=A[i][k]*B[k][j]
    return C
def exact_eigenvalue(M):
    MM=multiply(M,M)
    lam=next(MM[i][j]//M[i][j] for i in range(len(M)) for j in range(len(M)) if M[i][j])
    assert lam>0 and all(MM[i][j]==lam*M[i][j] for i in range(len(M)) for j in range(len(M)))
    return lam
def cycles(target,g):
    n=len(target);e=[edges(q,g) for q in target]
    for start in states(g):
        possible=[set() for _ in range(n+1)];possible[n]={start}
        for k in range(n-1,-1,-1):
            possible[k]={s for s,ss in e[k].items() if any(to in possible[k+1] for to,_ in ss)}
        if start not in possible[0]:continue
        stack=[(0,start,(),(start,))]
        while stack:
            i,s,ps,path=stack.pop()
            if i==n:
                if s==start:yield ps,path
            else:
                for to,p in e[i].get(s,[]):
                    if to in possible[i+1]:stack.append((i+1,to,ps+(p,),path+(to,)))
def run():
    ans=[]
    for t in range(8):
        g=int(t%2==0);target=W[(t+1)%8];M=matprod(target,g)
        lam=exact_eigenvalue(M)
        loops=list(cycles(target,g))
        assert len(loops)==(51200 if g else 2)
        assert len({ps for ps,_ in loops})==len(loops)
        assert all(any(x%2 for x in ps) for ps,_ in loops)
        assert trace(matprod(target,g,W[t]))==1
        ans.append(dict(phase=t,overflow=g,states=len(M),lambda_value=lam,
          trace_M=trace(M),trace_M2=trace(multiply(M,M)),
          distinct_cycle_words=len(loops),entropy_bits_per_column=math.log2(lam)/20 if lam>1 else 0))
    print(json.dumps(ans,indent=2))
if __name__=="__main__":run()
