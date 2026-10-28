#!/usr/bin/env python3
"""Counter automaton for x = lowest pair sum.  Non-overflow: x<=b-1, c in {0,1}: x' = 2x+c (needs x+c<=b-1).
Overflow: x+c>=b : x' = (x mod b)+1.  Compute max cycle ratio P/G over cycles with G>=1 and min ratio."""
import sys
from fractions import Fraction
import itertools
def edges(b):
    E=[]
    for x in range(1,2*b-1):
        for c in (0,1):
            if x+c<b: E.append((x,2*x+c,0))
            else: E.append((x,(x%b)+1,1))
    return E
def best_ratio(b):
    # enumerate simple cycles by DFS (graph small) and compute extremes of P/G
    E=edges(b); adj={}
    for u,v,g in E: adj.setdefault(u,set()).add((v,g))
    nodes=sorted(adj)
    best_max=(Fraction(0),None); best_min=(Fraction(10**9),None)
    # simple cycles via DFS from each smallest node
    for s in nodes:
        stack=[(s,[s],[])]
        while stack:
            u,path,gs=stack.pop()
            for v,g in adj.get(u,()):
                if v==s:
                    G=sum(gs)+g; P=len(path)
                    if G>=1:
                        r=Fraction(P,G)
                        if r>best_max[0]: best_max=(r,(path,gs+[g]))
                        if r<best_min[0]: best_min=(r,(path,gs+[g]))
                elif v>s and v not in path:
                    stack.append((v,path+[v],gs+[g]))
    return best_max,best_min
if __name__=="__main__":
    for b in range(2,40):
        mx,mn=best_ratio(b)
        L=(b-1).bit_length()  # floor(log2(b-1))+1
        print(b,"L=",L,"max P/G (counter only)=",mx[0],"min=",mn[0])
