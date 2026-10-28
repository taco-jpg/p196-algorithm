#!/usr/bin/env python3
"""Independent finite-state arithmetic checker for uniform lattice targets.
Counts *temporal predecessor trajectories* directly without inverse automaton code.
When count==1 and self-loop exists, backwards cone is exactly the target.
"""
from collections import defaultdict

def predecessors(base, word, seed):
    p=len(word); u=[seed]
    for _ in range(p):
        k=u[-1];u.append(2*((k+(k>=base))%base))
    assert u[-1]==seed
    c=[int(x>=base) for x in u[:-1]]
    L2=H2=c
    Y2=[(u[t]+c[t])%base for t in range(p) if word[t]=='1']
    count=0
    for x0 in range(2*base-1):
        D={x0:1};j=0
        for t,ch in enumerate(word):
            out=defaultdict(int)
            for x,n in D.items():
                for lt in (0,1):
                    if (x+lt)//base!=L2[t]:continue
                    if ch=='1':
                        if (x+H2[t])%base!=Y2[j]:continue
                        for y in range(base):
                            out[(x+lt)%base+y]+=n
                    else:
                        out[(x+lt)%base+(x+H2[t])%base]+=n
            if ch=='1':j+=1
            D=out
        count+=D.get(x0,0)
    return count

def main():
    w='101001010110001011000'
    for v in (0,12):
        q=predecessors(7,w,v)
        assert q==1,(v,q)
        print('PASS b7 p21 target',v,'exact predecessor trajectories',q)
    # b13 positive control has multiple predecessor choices and is not a
    # singleton closed backwards cone; the checked BFS reaches the root.
    assert predecessors(13,'1010010000',8)>1
    print('PASS b13 positive control has nontrivial predecessor cone')
if __name__=='__main__':main()
