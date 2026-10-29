#!/usr/bin/env python3
"""Exact folded-pair transducer and DFA certificate prototype for reverse-add.
A DFA may accept even pair sequences or odd pair sequences with a centre digit.
All indices are least-significant pair first; 'centre' is a digit, not a coefficient.
"""
from collections import deque
from dataclasses import dataclass

@dataclass(frozen=True)
class DFA:
    base: int
    start: int
    table: tuple              # table[state][pair_coefficient] -> state
    even_states: frozenset
    odd_states: frozenset     # accepts any centre digit 0..b-1 at this state
    def nxt(self,q,p): return self.table[q][p]
    def accepts(self,q,centre):
        return q in (self.even_states if centre is None else self.odd_states)


def all_pairs(base):
    return DFA(base,0,(tuple([0]*(2*base-1)),),frozenset([0]),frozenset([0]))

def odd_pairs(base):
    return DFA(base,0,(tuple(int(p%2==1) for p in range(2*base-1)),tuple([1]*(2*base-1))),frozenset([1]),frozenset([1]))


def step_pairs(P,centre,b):
    """Direct folded grade-school formula. P[0] is outermost, centre None for even length.
    Returns (output pair coefficients, output centre digit, overflow gamma).
    """
    assert b>=2 and all(0<=v<=2*b-2 for v in P)
    assert centre is None or 0<=centre<b
    assert P or centre is not None
    assert not P or P[0]>0
    # Resolve low and high carry explicitly, independently from any source digits.
    lo=[]; lc=0
    for p in P:
        x=p+lc
        lo.append(x%b)
        lc=x//b
    if centre is not None:
        cc=(2*centre+lc)%b
        lc=(2*centre+lc)//b
    else: cc=None
    hi=[0]*len(P)
    c=lc
    for i in range(len(P)-1,-1,-1):
        x=P[i]+c
        hi[i]=x%b
        c=x//b
    gamma=c
    if gamma==0:
        return [a+z for a,z in zip(lo,hi)],cc,gamma
    if not P:  # one-digit source becomes two digits
        return [cc+1],None,gamma
    q=[lo[0]+1]+[lo[i]+hi[i-1] for i in range(1,len(P))]
    if centre is None:
        return q,hi[-1],gamma
    return q+[cc+hi[-1]],None,gamma


def discover_bad(dfa,require_odd=False):
    """Exact finite reachability. Find an input in L whose next pairword is outside L.
    With require_odd, independently finds inputs in L without an odd pair witness.
    Return None on success; otherwise one counterexample dictionary. Exhaustive ALL lengths.
    """
    b=dfa.base
    # state=(src DFA, dest DFA, lower carry, upper carry, prev high digit,
    #        first flag, odd witness, gamma)
    queue=deque()
    seen={}
    for gamma in (0,1):
        root=(dfa.start,dfa.start,0,gamma,-1,True,False,gamma)
        seen[root]=None;queue.append(root)
    def emit(st,centre,P):
        src,dst,low,up,prev,first,odd,gamma=st
        if require_odd and not odd:
            return dict(reason='accepts input without an odd pair', pairs=P,centre=centre)
        np,nc,ng=step_pairs(P,centre,b)
        assert ng==gamma
        return dict(reason='not forward closed',pairs=P,centre=centre,next_pairs=np,next_centre=nc,gamma=gamma)
    def path(st):
        ps=[]
        while seen[st] is not None:
            parent,p=seen[st];ps.append(p);st=parent
        return list(reversed(ps))
    while queue:
        st=queue.popleft()
        src,dst,low,up,prev,first,odd,gamma=st
        if first:
            # The sole middle digit of an n=1 input is not a pair.
            for centre in range(1,b):
                if not dfa.accepts(src,centre):continue
                out=2*centre
                og=int(out>=b)
                if og != gamma:continue
                if require_odd:return emit(st,centre,[])
                accepted=(dfa.accepts(dst,2*centre) if og==0 else dfa.accepts(dfa.nxt(dst,(out%b)+1),None))
                if not accepted:return emit(st,centre,[])
        else:
            if up==low and dfa.accepts(src,None):
                if require_odd and not odd:return emit(st,None,path(st))
                if gamma==0: destok=dfa.accepts(dst,None)
                else: destok=dfa.accepts(dst,prev)
                if not destok:return emit(st,None,path(st))
            for centre in range(b):
                if not dfa.accepts(src,centre):continue
                z=2*centre+low; newcentre=z%b; midcarry=z//b
                if midcarry != up:continue
                if require_odd and not odd:return emit(st,centre,path(st))
                if gamma==0: destok=dfa.accepts(dst,newcentre)
                else: destok=dfa.accepts(dfa.nxt(dst,newcentre+prev),None)
                if not destok:return emit(st,centre,path(st))
        # Add another outer pair. The upper carry is guessed backwards from centre.
        for p in range(1 if first else 0,2*b-1):
            ls=p+low; nextlow=ls//b; digitlow=ls%b
            for nextup in (0,1):
                hs=p+nextup
                if hs//b!=up:continue
                digithi=hs%b
                outp = digitlow+digithi if gamma==0 else digitlow+(1 if first else prev)
                s2=(dfa.nxt(src,p),dfa.nxt(dst,outp),nextlow,nextup,digithi,False,odd or p%2==1,gamma)
                if s2 not in seen:
                    seen[s2]=(st,p);queue.append(s2)
    return None


def decode_pair(P,centre,b):
    """Canonical digit-list witness, least-significant first; source for the transducer."""
    low=[max(0,p-(b-1)) for p in P]
    high=[min(b-1,p) for p in P]
    assert not P or high[0]!=0
    return low+([] if centre is None else [centre])+high[::-1]


def reverse_add_digits(ds,b):
    carry=0;out=[]
    for a,z in zip(ds,ds[::-1]):
        q=a+z+carry;out.append(q%b);carry=q//b
    if carry:out.append(carry)
    while len(out)>1 and out[-1]==0:out.pop()
    return out


def pairs_from_digits(ds):
    m=len(ds)//2
    return [ds[i]+ds[-1-i] for i in range(m)], (ds[m] if len(ds)%2 else None)

if __name__=='__main__':
    for b in (2,3,4,9,10,11):
        assert discover_bad(all_pairs(b)) is None
        assert discover_bad(all_pairs(b),require_odd=True)['reason']=='accepts input without an odd pair'
        bad=discover_bad(odd_pairs(b))
        print('base',b,'odd-witness DFA counterexample',bad)
        assert bad and bad['reason']=='not forward closed'
    print('FINITE DFA TRANSDUCER CHECK PASS')