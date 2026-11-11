#!/usr/bin/env python3
"""Independent enumeration of IF(d0) and births (r13c): compares the set of distinct I' strings with a khr deaths file.
usage: births_check.py g d0 L deathsfile"""
import sys
b=10
g_w, d0, L = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
deaths = sys.argv[4]
g = [int(g_w[t % len(g_w)]) for t in range(L)]
gd = g[:d0]
def step(I, t, v):
    c,xb,A,root = I; T=len(c); tt=t%T
    res = {}
    for h in (0,1):
        H=(v+h)//b
        if not (A[tt]>>H)&1: continue
        gt = g[t % len(g)] if len(g)==L else g[t%L]
        if gt:
            part = 1 if xb[tt]==-1 else (xb[tt]+H)%b
        else:
            part=(v+h)%b
        y=(v+c[tt])%b+part
        if root and y<1: continue
        if y>18: continue
        res.setdefault(y,0); res[y]|=1<<h
    return res
def closed_cols(I, Lc):
    # all closed Lc-walks above I
    root = I[3]
    starts = range(1,19) if root else range(0,19)
    out=[]
    # reach sets
    R=[[0]*19 for _ in range(Lc+1)]
    for v in range(19): R[Lc][v]=1<<v
    for t in range(Lc-1,-1,-1):
        for v in range(19):
            if root and v<1: continue
            m=0
            for y in step(I,t,v): m|=R[t+1][y]
            R[t][v]=m
    path=[0]*(Lc+1)
    def dfs(t):
        if t==Lc:
            if path[Lc]==path[0]: out.append(path[:Lc])
            return
        for y in step(I,t,path[t]):
            if (R[t+1][y]>>path[0])&1:
                path[t+1]=y; dfs(t+1)
    for v0 in starts:
        if (R[0][v0]>>v0)&1:
            path[0]=v0; dfs(0)
    return out
def succ(I, col, Lc):
    c,xb,A,root = I; T0=len(c); cn=[0]*Lc; xn=[0]*Lc; An=[0]*Lc
    for t in range(Lc):
        v=col[t]; vn=col[(t+1)%Lc]; cn[t]=(v+c[t%T0])//b; xn[t]= v if g[t]%2 and True and False else 0
    return None
def succI(I,col,Lc):
    c,xb,A,root = I; T0=len(c); cn=[0]*Lc; xn=[0]*Lc; An=[0]*Lc
    for t in range(Lc):
        v=col[t]; vn=col[(t+1)%Lc]; tt=t%T0; cn[t]=(v+c[tt])//b
        gt=g[t%L] if Lc<=L else 0
        xn[t]= v if gt else 0
        m=0
        for h in (0,1):
            H=(v+h)//b
            if not (A[tt]>>H)&1: continue
            part = (1 if xb[tt]==-1 else (xb[tt]+H)%b) if gt else (v+h)%b
            y=(v+c[tt])%b+part
            if y==vn: m|=1<<h
        An[t]=m
    return (tuple(cn),tuple(xn),tuple(An),False)
root=(tuple([0]*d0),tuple([-1]*d0),tuple(1<<(g[t%L]) for t in range(d0)),True)
seen={root:0}; order=[root]; head=0
while head<len(order):
    I=order[head]; head+=1
    for col in closed_cols(I,d0):
        J=succI(I,col,d0)
        if J not in seen: seen[J]=len(order); order.append(J)
print("IF count",len(order))
births=set()
for I in order:
    for col in closed_cols(I,L):
        if any(col[t]!=col[(t+d0)%L] for t in range(L)):
            J=succI(I,col,L)
            s=''.join(str(x) for x in J[0])+'|'+','.join(str(x) for x in J[1])+'|'+''.join(str(x) for x in J[2])
            births.add(s)
print("distinct births",len(births))
cset=set(l.split()[2] for l in open(deaths))
print("deaths file",len(cset),"equal sets:",births==cset)
