#!/usr/bin/env python3
"""Independent layer-by-layer 6-step relation product, without enumerating full carry vectors.
Each layer enumerates all coefficient/carry pairs, then composes weighted relations.
"""
from collections import defaultdict,Counter
from itertools import product
G=(1,0,1,1,0,0)

def independent_first_column(b):
    if b==4:return (4,1,3,4,1,2),(1,1,0,0)
    if b==5:return (6,2,4,5,1,3),(0,1,1,0)
    if b==6:return (7,2,5,6,1,3),(1,1,1,1)
    raise ValueError(b)

def matrix_transfer(b,rotation=0):
    result=Counter()
    xbase,forced=independent_first_column(b)
    for a,d in product((0,1),repeat=2):
        cfirst=(a,forced[0],forced[1],d,forced[2],forced[3])
        gi=tuple(G[(t+rotation)%6] for t in range(6))
        hi=tuple(cfirst[(t+rotation)%6] for t in range(6))
        li=tuple(xbase[(t+rotation)%6]//b for t in range(6))
        yi=tuple((xbase[(t+rotation)%6]+cfirst[(t+rotation)%6])%b for t in range(6))
        # Compute the weight of a length-six directed path by multiplying six local matrices.
        weighted={(s,s):1 for s in range(2*b-1)}
        for t in range(6):
            mat=defaultdict(int)
            for z in range(2*b-1):
                for v in range(2):
                    if (z+v)//b!=hi[t]:continue
                    zz=(z+li[t])%b+(yi[t] if gi[t] else (z+v)%b)
                    if 0<=zz<=2*b-2:mat[z,zz]+=1
            nxt=defaultdict(int)
            for (start,z),w in weighted.items():
                for zz in range(2*b-1):
                    m=mat.get((z,zz),0)
                    if m:nxt[start,zz]+=w*m
            weighted=nxt
        for (start,end),mult in weighted.items():
            result[a,d,start,end]+=mult
    return result


def detect_closed_path(tab,b):
    # Any closed walk of arbitrary positive length is equivalent to a directed cycle.
    adj={x:set() for x in range(2*b-1)}
    for (a,d,start,end),count in tab.items():
        if count:adj[start].add(end)
    def visit(x,active,seen):
        if x in active:return True
        if x in seen:return False
        active.add(x)
        for y in adj[x]:
            if visit(y,active,seen):return True
        active.remove(x);seen.add(x);return False
    seen=set()
    return any(visit(x,set(),seen) for x in adj)


def count_closed_walks(tab,b,n):
    # Trace of the nth power of the six-step weighted adjacency matrix.
    # The mode labels and different carry assignments are independent edge choices.
    A=[[0]*(2*b-1) for _ in range(2*b-1)]
    for (a,d,u,v),weight in tab.items():A[u][v]+=weight
    trace=[]
    for start in range(2*b-1):
        vec=[0]*(2*b-1);vec[start]=1
        for k in range(1,n+1):
            vec=[sum(vec[u]*A[u][v] for u in range(2*b-1)) for v in range(2*b-1)]
            if start==0:trace.append(0)
            trace[k-1]+=vec[start]
    return trace

def main():
    from agent16_second_primary import transfer
    for b in (4,5,6):
        for rot in range(6):
            a,_=transfer(b,rot)
            m=matrix_transfer(b,rot)
            assert a==m,(b,rot,a-m,m-a)
            cyclic=detect_closed_path(m,b)
            assert cyclic==(b==4),(b,rot,cyclic)
            traces=count_closed_walks(m,b,20)
            assert all((v>0)==(b==4) for v in traces),(b,rot,traces)
            print(f'PASS b={b} rotation={rot} paths={sum(m.values())} keys={len(m)} cyclic={cyclic}',flush=True)
        tab=matrix_transfer(b)
        if b==5: assert tab==Counter({(0,0,2,8):8,(1,0,6,8):8}),tab
        if b==6: assert not tab,tab
        if b==4:assert sum(tab.values())==28 and detect_closed_path(tab,b)
    print('ALL SECOND-COLUMN CHECKS PASSED')

if __name__=='__main__': main()
