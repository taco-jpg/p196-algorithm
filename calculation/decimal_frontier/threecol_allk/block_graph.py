#!/usr/bin/env python3
"""PAPER PROOF finite transfer enumeration for decimal g=(11000)^k.

The exact (bauto3) position automaton uses coefficient x_t in [0,18],
incoming carry L_t, outgoing carry requirement H_t, and upper-partner
Y_t at overflow positions:
  floor((x_t+c_t)/10) = H_t
  x_(t+1) = ((x_t+L_t) mod 10) + (Y_t if g_t=1 else (x_t+c_t) mod 10)
with chosen c_t in {0,1}; for the canonical first column x_0 >= 1.
One five-time-step edge records coefficient start/end and all five carries.
The source proves all steps by enumerating the finite x/c state space;
the PAPER PROOF is in reports/Agent12ThreeColumnAllK.md.
"""
from collections import defaultdict
from itertools import product

B=10
G=(1,1,0,0,0)


def block_edges(L,H,Y,first=False):
    assert len(L)==len(H)==5 and len(Y)==2
    paths=[]
    for z in range(1 if first else 0,19):
        def recurse(t,x,xs,carry):
            if t==5:
                paths.append((z,x,tuple(xs),tuple(carry)))
                return
            for c in (0,1):
                if (x+c)//10!=H[t]:
                    continue
                nx=((x+L[t])%10 +
                    (Y[0 if t==0 else 1] if G[t] else (x+c)%10))
                assert 0 <= nx <= 18
                recurse(t+1,nx,xs+[x],carry+[c])
        recurse(0,z,[],[])
    return paths


def edges_unique(paths):
    d=defaultdict(list)
    for z,w,xs,cs in paths:d[(z,w)].append((xs,cs))
    return d


def expected_relation(edges, groups, multiplier):
    expected={(start,end) for start,ends in groups.items() for end in ends}
    assert set(edges)==expected,(set(edges)^expected)
    assert all(len(v)==multiplier for v in edges.values())


def verify():
    root=edges_unique(block_edges((0,0,0,0,0),G,(1,1),True))
    expected_relation(root,{9:range(8,16)},2)
    assert all(xs==(9,10,1,2,4) for xs,c in root[(9,9)])
    assert {cs for xs,cs in root[9,9]}=={(1,0,0,0,1),(1,1,0,0,1)}
    print('root:',len(root),'edges, multiplicity 2; only start 9, destinations 8..15')
    assert not block_edges((0,1,0,0,0),(1,1,0,0,1),(0,1))
    second=edges_unique(block_edges((0,1,0,0,0),(1,0,0,0,1),(0,0)))
    expected_relation(second,{11:[0,1,2,3,9],12:range(4,12),13:range(12,18)},4)
    assert all(xs==(13,3,4,8,16) for xs,cs in second[(13,13)])
    assert {cs for xs,cs in second[(13,13)]} == {
         (a,b,0,0,1) for a,b in product((0,1),repeat=2)}
    print('second:',len(second),'edges, multiplicity 4; only recurrent state 13')
    total=0
    for a,b in product((0,1),repeat=2):
        third=edges_unique(block_edges((1,0,0,0,1),(a,b,0,0,1),(3+a,3+b)))
        if (a,b) in ((0,0),(1,0)):
            assert not third
        else:
            expected_relation(third,{6 if a==0 else 15:range(13,19)},4)
        total+=len(third)
        if (a,b)==(1,1):
            assert all(xs==(15,10,4,8,17) for xs,cs in third[(15,15)])
            assert {cs for xs,cs in third[(15,15)]} == {
                (a0,b0,0,1,0) for a0,b0 in product((0,1),repeat=2)}
        print('third, second carry',a,b,':',len(third),'edges')
    assert total==12
    # A closed path of k blocks is a directed closed walk. In all three
    # finite graphs the sole directed cycle is the claimed self-loop.
    # The explicit groups above show no other cycles, without a graph solver.
    print('PASS exact 5-step transfer graphs, 4^k third-column carry histories for all k>=1')

if __name__=='__main__':verify()
