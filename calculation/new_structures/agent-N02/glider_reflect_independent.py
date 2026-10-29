#!/usr/bin/env python3
"""Independent Python integers for the new transient outward-drifting suffix.
Source p8 lattice is parsed from repository, not from C++ constants.
"""
import sys
from pathlib import Path
from glider_independent import original_data,frontier
C=(8,13,14,8,9,17,16,8,5,7,1,8,4,14,12,10,1,9,0,4,18,1,17,9,10,14,3,10,4,14,1,0,5,5,4,1,7,9,17,11,5,4,7,6,10,8,4)

def seed(q,path,cyc):
    half=[r[0] for r in path]+[r[0] for r in cyc]*q+list(C)
    d=[0]*(2*len(half))
    for j,v in enumerate(half):
        d[j]=min(v,9);d[-1-j]=v-d[j]
    assert d[-1]>0
    return int(''.join(str(x) for x in d[::-1]))

def main(root):
    path,cyc=original_data(root)
    for q in (1,2,3,5,8,12):
        n=seed(q,path,cyc);first_front=None;sample={}
        for t in range(88*q+413):
            ss=str(n)
            assert ss!=ss[::-1],('palindrome',q,t)
            j=frontier(n,t,path,cyc)
            if t==0:first_front=j
            if t in (88,176,264,352,440) and j>=39:sample[t]=j-first_front
            if j<39:
                assert (t,j)==(88*q+412,38),(q,t,j)
                break
            n2=n+int(ss[::-1]);assert len(str(n2))-len(ss)==int(t%2==0)
            n=n2
        else:raise AssertionError(('no break',q))
        assert [sample.get(t) for t in (88,176,264,352,440) if t<88*q+412]==[0,1,0,1,-7][:len(sample)],(q,sample)
        print('REFLECT_PYINT_PASS q',q,'first_bad',88*q+412,'gain',408,'front_deltas',sample)

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[3])
