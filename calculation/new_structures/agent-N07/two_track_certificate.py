#!/usr/bin/env python3
"""All-length two-track folded DFA closure checker for decimal/base-b reverse-add.
The input alphabet is the actual ordered pair (low digit, high digit), not their sum.
"""
from collections import deque
from dataclasses import dataclass

@dataclass(frozen=True)
class DFA:
    base: int
    start: int
    table: tuple       # table[state][low*base + high] -> state
    even_accept: frozenset
    odd_accept: frozenset    # accepts any central digit (straightforward to restrict)
    def nxt(self,q,a,z): return self.table[q][a*self.base+z]
    def accept(self,q,centre):
        return q in (self.even_accept if centre is None else self.odd_accept)

def all_positive(b):
    return DFA(b,0,(tuple([0]*(b*b)),),frozenset([0]),frozenset([0]))

def mismatch(b):
    return DFA(b,0,(tuple(int(a!=z) for a in range(b) for z in range(b)),
                    tuple([1]*(b*b))),frozenset([1]),frozenset([1]))

def twotrack_step(pairs,centre,b):
    """Compute successor ordered pairs in outer-to-centre order, exactly."""
    assert pairs or (centre is not None and 0<centre<b)
    if pairs: assert pairs[0][1]>0
    low=[];lowercarry=0
    for a,z in pairs:
        t=a+z+lowercarry
        low.append(t%b);lowercarry=t//b
    outcentre=None
    if centre is not None:
        t=2*centre+lowercarry
        outcentre=t%b;lowercarry=t//b
    high=[0]*len(pairs)
    c=lowercarry
    for i in range(len(pairs)-1,-1,-1):
        a,z=pairs[i];t=a+z+c
        high[i]=t%b;c=t//b
    gamma=c
    if gamma==0:
        return list(zip(low,high)),outcentre,gamma
    if not pairs:return [(outcentre,1)],None,gamma
    nxt=[(low[0],1)]+[(low[i],high[i-1]) for i in range(1,len(pairs))]
    if centre is None:return nxt,high[-1],gamma
    return nxt+[(outcentre,high[-1])],None,gamma

def decode(pairs,centre):
    return [a for a,z in pairs] + ([] if centre is None else [centre]) + [z for a,z in reversed(pairs)]

def fold(ds):
    m=len(ds)//2
    return [(ds[i],ds[-i-1]) for i in range(m)],(ds[m] if len(ds)%2 else None)

def check_closure(dfa,require_mismatch=False):
    """Complete product-BFS for arbitrary lengths. None means closure proved.
    If require_mismatch, a counterexample is returned unless all accepted input
    words contain an unequal digit pair. No length or state cap is imposed.
    """
    b=dfa.base
    roots=[];q=deque();parent={}
    for gamma in (0,1):
        st=(dfa.start,dfa.start,0,gamma,-1,True,False,gamma)
        q.append(st);parent[st]=None
    def path(st):
        pairs=[]
        while parent[st] is not None:
            old,pr=parent[st];pairs.append(pr);st=old
        return pairs[::-1]
    while q:
        st=q.popleft()
        src,dst,l,r,prev,first,seenmis,gamma=st
        if first:
            for c in range(1,b):
                if not dfa.accept(src,c):continue
                s=2*c;g=int(s>=b)
                if g!=gamma:continue
                if require_mismatch:return ('unsafe',[],c)
                ok=(dfa.accept(dst,s) if g==0 else dfa.accept(dfa.nxt(dst,s%b,1),None))
                if not ok:return ('not_closed',[],c)
        else:
            if l==r and dfa.accept(src,None):
                if require_mismatch and not seenmis:return ('unsafe',path(st),None)
                ok=dfa.accept(dst,(None if gamma==0 else prev))
                if not ok:return ('not_closed',path(st),None)
            for c in range(b):
                if not dfa.accept(src,c):continue
                s=2*c+l
                if s//b!=r:continue
                d=s%b
                if require_mismatch and not seenmis:return ('unsafe',path(st),c)
                ok=dfa.accept(dst,d) if gamma==0 else dfa.accept(dfa.nxt(dst,d,prev),None)
                if not ok:return ('not_closed',path(st),c)
        for a in range(b):
            for z in range(1 if first else 0,b):
                p=a+z;sl=p+l;nextl=sl//b;digl=sl%b
                for nextr in (0,1):
                    sr=p+nextr
                    if sr//b!=r:continue
                    digr=sr%b
                    out_hi=(digr if gamma==0 else (1 if first else prev))
                    out=(digl,out_hi)
                    nxt=(dfa.nxt(src,a,z),dfa.nxt(dst,*out),nextl,nextr,digr,False,seenmis or a!=z,gamma)
                    if nxt not in parent:
                        parent[nxt]=(st,(a,z));q.append(nxt)
    return None

if __name__=='__main__':
    for b in (2,3,4,9,10,11):
        assert check_closure(all_positive(b)) is None
        assert check_closure(all_positive(b),True)[0]=='unsafe'
        assert check_closure(mismatch(b),True)[0]=='not_closed'
    p,c=fold([9,6,8,7,6,0,1])
    assert all((a+z)%2==0 for a,z in p) and any(a!=z for a,z in p)
    assert mismatch(10).accept(1,None)
    print('TWO_TRACK_DFA_EXACT_CLOSURE_TESTS_PASS',p,c)