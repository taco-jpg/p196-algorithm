#!/usr/bin/env python3
"""Complete 36-state finite-automaton exclusion of strictly contiguous
one-step-invisible bulk changes in p12/m9 gamma=0 lattice phases.
Python 3 stdlib only. Command: python3 classify.py <lat_p12m9.txt>
No extrapolation from a finite-width SAT solver.
"""
from pathlib import Path
import sys, json
from collections import deque

def read_data(path):
    nums=iter(map(int,Path(path).read_text().split()))
    p,nB,m,b=[next(nums) for _ in range(4)]
    assert (p,nB,m,b)==(12,34,9,10)
    gamma=[next(nums) for _ in range(12)]
    W=[[next(nums) for _ in range(m)] for _ in range(p)]
    cup=[[next(nums) for _ in range(m)] for _ in range(p)]
    B=[[next(nums) for _ in range(nB)] for _ in range(p)]
    assert next(nums,None) is None
    return gamma,W,cup,B

def pair(t,n,W,B):
    h=(n+1)//2
    half=B[t]+[W[t][(i-34)%9] for i in range(34,h)]
    if n&1 and half[-1]%2:
        half[-1]+=1 if half[-1]<18 else -1
    return half+half[:n//2][::-1]

def normalize(P):
    digits=[];C=[0]
    for q in P:
        s=q+C[-1];digits.append(s%10);C.append(s//10)
    if C[-1]:digits.append(C[-1])
    return digits,C

def table(t,n,W,B):
    P=pair(t,n,W,B);O,C=normalize(P)
    assert len(O)==n, ('not gamma0',t,n)
    tab=[]
    for r in range(9):
        i=34+18+r;j=n-1-i
        tab.append((P[i],O[i]+O[j],C[i],C[j+1]))
    for i in range(34+27, n//2-12):
        j=n-1-i
        assert (P[i],O[i]+O[j],C[i],C[j+1])==tab[(i-(34+18))%9],(t,n,i)
    return tab

def transitions(tab,r,a,b):
    q,s,_,_=tab[r]
    for value in range(19):
        if value==q:continue  # strict connected change, NO unchanged bridge cells
        for upper_in in (0,1):
            if (value+upper_in)//10!=b:continue
            if (value+a)%10+(value+upper_in)%10!=s:continue
            yield ((r+1)%9,(value+a)//10,upper_in)

def explore(tab,r):
    # Initially actual carries agree with the baseline immediately outside support.
    a,b=tab[r][2:]
    start=(r,a,b)
    todo=deque(transitions(tab,*start))
    seen=set()
    while todo:
        s=todo.popleft()
        if (s[1],s[2])==tuple(tab[s[0]][2:]):
            return False,len(seen),s  # exact carry reset with every site changed
        if s in seen:continue
        seen.add(s)
        todo.extend(transitions(tab,*s))
    return True,len(seen),None

def main(path):
    gamma,W,cup,B=read_data(path)
    assert gamma==[1,0,0,0]*3
    table_counts=[]
    for t,g in enumerate(gamma):
        if g:continue
        tab=table(t,400,W,B)
        for n in [401,418,419,490,491,800,801,836,837]:
            assert table(t,n,W,B)==tab,(t,n)
        # Independently check stated period carry bits for lower infinite lattice.
        for r,(q,s,a,b) in enumerate(tab):
            assert q==W[t][(18+r)%9]
            assert a==cup[t][(18+r)%9],(t,r,a,cup[t][r])
        per=[]
        for r in range(9):
            ok,visited,witness=explore(tab,r)
            assert ok, ('connected invisible candidate',t,r,witness)
            assert visited<=36,(t,r,visited)
            per.append(visited)
        table_counts.append([t]+per)
        print('PHASE',t,'REACHABLE_NONRETURN_STATES',per,'ZERO_ACCEPTING',flush=True)
    assert len(table_counts)==9
    print('STRICT_CONTIGUOUS_ALL_WIDTH_EXCLUSION_PASS',len(table_counts)*9,'rooted start states')
    print('COUNTS_JSON',json.dumps(table_counts,separators=(',',':')))

if __name__=='__main__':
    data=sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).resolve().parent.parent/'data'/'lat_p12m9.txt')
    main(data)
