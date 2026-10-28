#!/usr/bin/env python3
"""Exhaust the exact 5-step, fourth-column transfer for g=(11000)^k.

All input third-column histories come from the all-k three-column theorem.
The independent whole-period C++ checker implements the p-step recurrence
without this 5-step transfer construction.
"""
from collections import defaultdict
from itertools import product

G=(1,1,0,0,0)
S=(6,7,8,9,15,16,17,18)
EXPECTED=((0,0,0,4,0,0,0,0),
          (4,4,4,0,0,0,0,0),
          (0,0,0,4,4,4,0,0),
          (0,0,0,4,2,2,2,2),
          (0,0,0,4,0,0,0,0),
          (4,4,4,0,0,0,0,0),
          (0,0,0,4,4,4,0,0),
          (0,0,0,4,0,0,4,4))

def edges_for_label(a,b):
    L=(1,1,0,0,1); H=(a,b,0,1,0); Y=(5+a,b)
    edges=[]
    for x0 in range(19):
        def walk(t,x,h):
            if t==5:
                edges.append((x0,x,tuple(h)));return
            for c in (0,1):
                if (x+c)//10 != H[t]:continue
                d=(x+L[t])%10 + (Y[0 if t==0 else 1] if G[t] else (x+c)%10)
                if not 0<=d<=18:raise ArithmeticError('out of range')
                walk(t+1,d,h+[c])
        walk(0,x0,[])
    return edges

def multiply(A,B):
    n=len(A);return [[sum(A[i][k]*B[k][j] for k in range(n))
                      for j in range(n)] for i in range(n)]

def power_trace(A,k):
    n=len(A);v=[[int(i==j) for j in range(n)] for i in range(n)]
    for _ in range(k):v=multiply(v,A)
    return sum(v[i][i] for i in range(n))

def charpoly(A):
    # Exact integer Newton identities: monic characteristic polynomial.
    n=len(A)
    powers=[0]+[power_trace(A,k) for k in range(1,n+1)]
    coeff=[1]
    for k in range(1,n+1):
        s=sum(coeff[k-j]*powers[j] for j in range(1,k+1))
        assert s%k==0,(k,s)
        coeff.append(-s//k)
    return coeff

def sccs(vertices, edges):
    outs={v:set() for v in vertices};back={v:set() for v in vertices}
    for a,b in edges:
        outs[a].add(b);back[b].add(a)
    seen=set();order=[]
    def visit(v):
        seen.add(v)
        for w in outs[v]:
            if w not in seen:visit(w)
        order.append(v)
    for v in vertices:
        if v not in seen:visit(v)
    seen=set();groups=[]
    for v in reversed(order):
        if v in seen:continue
        stack=[v];seen.add(v);group=[]
        while stack:
            z=stack.pop();group.append(z)
            for w in back[z]:
                if w not in seen:seen.add(w);stack.append(w)
        groups.append(set(group))
    return groups

def run():
    labeled=set();weighted=defaultdict(int);labels={}
    for a,b in product((0,1),repeat=2):
        paths=edges_for_label(a,b)
        for z,w,h in paths:
            labeled.add((z,w,a,b));weighted[z,w]+=1
            labels.setdefault((z,w,a,b),set()).add(h)
        print(f'label ({a},{b}): {len(paths)} exact 5-step coefficient/carry paths')
    assert len(labeled)==51 and len(weighted)==50 and sum(weighted.values())==182
    matrix=tuple(tuple(weighted[u,v] for v in S) for u in S)
    assert matrix==EXPECTED,(matrix,EXPECTED)
    nontriv=[]
    for comp in sccs(set(range(19)),weighted):
        cyclic=len(comp)>1 or any((v,v) in weighted for v in comp)
        if cyclic:nontriv.append(comp)
    assert nontriv==[set(S)] or (len(nontriv)==1 and nontriv[0]==set(S)), nontriv
    assert charpoly(matrix)==[1,-12,8,96,0,0,0,0,0]
    tprev,tcur=2,8
    for k in range(1,13):
        if k==1:tk=tcur
        else:
            tk=8*tcur+24*tprev;tprev,tcur=tcur,tk
        expected=4**k+tk
        got=power_trace(matrix,k)
        assert got==expected,(k,got,expected)
        print(f'k={k} four-column closed histories={got}')
    print('PASS: 51 distinct labeled edges, 8-state recurrent SCC, exact characteristic polynomial')

if __name__=='__main__':run()
