#!/usr/bin/env python3
"""Exact DFA inclusion test of known base-9 lattice as a positive FORMAT control.
Reads existing repository certificate JSON, but does not claim a new Lychrel result.
"""
from collections import deque
import json
from pathlib import Path
from regular_certificate import decode_pair,pairs_from_digits,reverse_add_digits
B=9
# This file lives under calculation/new_structures/agent-N07;
# parents[0]=agent-N07, parents[1]=new_structures, parents[2]=calculation.
CERT=Path(__file__).resolve().parents[2]/'decimal_frontier/lattice_formats/cert_b9_rec0.json'

class Template:
    def __init__(self,Bcoef,W,l):
        self.B=Bcoef;self.W=W;self.kmin=l//2;self.kmax=self.kmin+len(W)-1;self.odd=bool(l%2)
    def next(self,state,x):
        typ,k=state
        if typ=='ERR':return state
        if typ=='B':
            if k>=len(self.B) or x!=self.B[k]:return None
            return ('W',0) if k+1==len(self.B) else ('B',k+1)
        if x!=self.W[k%len(self.W)]:return None
        nxt=k+1 if k<self.kmax else self.kmin+(k+1-self.kmin)%len(self.W)
        return ('W',nxt)
    def accepts(self,state,centre):
        typ,k=state
        if typ!='W' or k<self.kmin or (k-self.kmin)%2:return False
        if not self.odd:return centre is None
        return centre is not None and self.W[k%len(self.W)]==2*centre

def check_phase(src,dst):
    queue=deque()
    for gamma in (0,1):queue.append((('B',0),('B',0),0,gamma,-1,True,gamma))
    seen=set()
    while queue:
        qsrc,qdst,low,upper,prev,first,gamma=queue.popleft()
        state=(qsrc,qdst,low,upper,prev,first,gamma)
        if state in seen:continue
        seen.add(state)
        if not first:
            if low==upper and src.accepts(qsrc,None):
                assert dst.accepts(qdst,None if gamma==0 else prev),('even-boundary',state)
            for centre in range(B):
                if not src.accepts(qsrc,centre):continue
                z=2*centre+low
                if z//B!=upper:continue
                d=z%B
                ok=(dst.accepts(qdst,d) if gamma==0 else
                    dst.accepts(dst.next(qdst,d+prev) or ('ERR',-1),None))
                assert ok,('odd-boundary',state,centre)
        typ,k=qsrc
        value=src.B[k] if typ=='B' else src.W[k%len(src.W)]
        if first and value==0:continue
        ns=src.next(qsrc,value)
        if ns is None:continue
        for nextupper in (0,1):
            if (value+nextupper)//B!=upper:continue
            lval=(value+low)%B
            upperdigit=(value+nextupper)%B
            out=lval+(upperdigit if gamma==0 else (1 if first else prev))
            nd=dst.next(qdst,out)
            if nd is None:nd=('ERR',-1)
            queue.append((ns,nd,(value+low)//B,nextupper,upperdigit,False,gamma))
    return len(seen)

def main():
    D=json.loads(CERT.read_text())
    assert D['base']==B and len(D['B_t'])==len(D['w_t'])==len(D['gam'])==10
    l=10;models=[]
    for i in range(10):
        models.append(Template(D['B_t'][i],D['w_t'][i],l))
        l+=D['gam'][i]
    assert l==14
    # All-length closure only yields a palindrome-free control when the source
    # languages themselves have a parity witness and contain a concrete seed.
    for phase in range(10):
        assert any(x%2 for x in D['B_t'][phase])
    for offset in range(0,7):
        phase_l=10+4*offset
        for phase in range(10):
            l=phase_l
            Bs=D['B_t'][phase];W=D['w_t'][phase]
            P=Bs+[W[j%len(W)] for j in range(l)]+Bs[::-1]
            assert P==P[::-1]
            half=P[:len(P)//2]
            centre=(P[len(P)//2]//2 if len(P)%2 else None)
            if len(P)%2:assert P[len(P)//2]%2==0
            ds=decode_pair(half,centre,B)
            out=reverse_add_digits(ds,B)
            # Independent arbitrary-precision integer arithmetic, not a transducer.
            def to_num(digits):
                v=0
                for digit in reversed(digits):v=v*B+digit
                return v
            actual=to_num(ds)+to_num(ds[::-1]);plain=[]
            while actual:plain.append(actual%B);actual//=B
            assert plain==out
            next_pair,next_centre=pairs_from_digits(out)
            next_phase=(phase+1)%10
            ell=l+D['gam'][phase]
            BN=D['B_t'][next_phase];WN=D['w_t'][next_phase]
            NP=BN+[WN[j%len(WN)] for j in range(ell)]+BN[::-1]
            assert NP==NP[::-1]
            NH=NP[:len(NP)//2]
            NC=(NP[len(NP)//2]//2 if len(NP)%2 else None)
            assert (next_pair,next_centre)==(NH,NC)
            phase_l+=D['gam'][phase]
    counts=[check_phase(models[i],models[(i+1)%10]) for i in range(10)]
    assert counts==[140,141,142,142,142,142,143,144,144,144],counts
    print('PASS: base9 all-length phase-indexed folded-DFA closure; exact product-state counts',counts,'; 70 independent bigint/digit-list arithmetic controls')

if __name__=='__main__':main()