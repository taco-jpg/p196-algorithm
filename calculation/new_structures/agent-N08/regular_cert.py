#!/usr/bin/env python3
"""Reachability-based exact inclusion of folded-palindrome regular languages.

The checker is NOT a bounded-length replay. Its product graph proves inclusion
for arbitrarily long accepted strings via ordinary finite graph reachability.
"""
from collections import deque
from paired_transducer import transitions,terminals,step_digits,fold

class DFA:
    def __init__(self,arcs,ends):
        self.arcs=arcs
        self.ends=ends
    def next(self,state,symbol):
        return self.arcs.get(state,{}).get(symbol,-1)
    def accepts(self,half,centre):
        state=0
        for p in half:
            state=self.next(state,p)
            if state==-1:return False
        return centre in self.ends.get(state,set())

# Seed 22 in base 2: after its first step the following phase grammar repeats.
# A_k = 2 1^k 00 1^k 2         (k>=1), centre even
# B_k = 10 1^(k-1) 202 1^(k-1) 01, centre 0
# C_k = 2 1^k 020 1^k 2, centre 2
# D_k = 10 1^(k-1) 2112 1^(k-1) 01, centre even
A=DFA({0:{2:1},1:{1:2},2:{1:2,0:3}},{3:{None}})
B=DFA({0:{1:1},1:{0:2},2:{1:2,2:3}},{3:{0}})
C=DFA({0:{2:1},1:{1:2},2:{1:2,0:3}},{3:{2}})
D=DFA({0:{1:1},1:{0:2},2:{1:2,2:3},3:{1:4}},{4:{None}})

def inclusion(b,source,target,gamma,require_empty=False):
    """Accept iff ALL valid successful input/output paths satisfy inclusion.

    require_empty=True checks that no source input has the chosen gamma.
    This includes the centre/carry agreement, which cannot be omitted.
    """
    root=(0,(0,gamma,-1),0)
    seen={root};todo=deque([root]);edges=0;endpaths=0
    while todo:
        qi,carry,qo=todo.popleft()
        for cent in source.ends.get(qi,()):
            for extra,cent2 in terminals(b,gamma,carry,cent):
                endpaths+=1
                qt=qo
                for symbol in extra:qt=target.next(qt,symbol)
                if require_empty or cent2 not in target.ends.get(qt,set()):
                    return False,(qi,carry,qo,cent,extra,cent2)
        for symbol,qi2 in source.arcs.get(qi,{}).items():
            for carry2,out in transitions(b,gamma,carry,symbol):
                triple=(qi2,carry2,target.next(qo,out))
                edges+=1
                if triple not in seen:seen.add(triple);todo.append(triple)
    return True,(len(seen),edges,endpaths)

def check():
    phases=(A,B,C,D)
    for i,gamma in enumerate((1,0,1,0)):
        ok,summary=inclusion(2,phases[i],phases[(i+1)%4],gamma)
        assert ok,(i,summary)
        no_wrong,wrong=inclusion(2,phases[i],phases[(i+1)%4],1-gamma,True)
        assert no_wrong,(i,wrong)
        print("REGULAR_EDGE",i,"gamma",gamma,"PASS",summary,"wrong-gamma",wrong)
    # The seed's first step lands in A_1.
    _,P1,gamma=step_digits([1,1,2,1,1],2)
    assert gamma==1 and A.accepts(*fold(P1))
    # Every word in A/C has a forced '1' after the first coefficient;
    # every word in B/D begins with '1'. Thus every pairword has odd coeff.
    print("BASE2_SEED22_EXACT_REGULAR_CERTIFICATE","PASS")

if __name__=="__main__":check()
