#!/usr/bin/env python3
"""Finite-state decision procedure for folded-pair regular invariants.

Input DFA: pair symbols 0..18, then one of 'E' or 'O0','O2',...'O18'.
The initial outer symbol must be >=1, and an O-centre with no outer
symbol must be >=2 (a positive one-digit decimal seed).

For any deterministic DFA, checks two regular-language obligations:
   (1) L ∩ PrePal = ∅
   (2) F(L) minus L = ∅
These are finite product-graph BFS searches. Both empty plus seed in L
implies an infinite non-palindromic decimal orbit (paper proof in report).
"""
from collections import deque
from transducer import fold, pairs, normalize, successor_is_pal, relation, unfold

class DFA:
    def __init__(self, initial, delta, final):
        self.initial = initial
        self.delta = delta
        self.final = final
    def run(self, outer, centre):
        q=self.initial
        for x in outer:
            q=self.delta(q,x)
        return self.final(self.delta(q,'E' if centre is None else f'O{centre}'))

# Three smoke-test languages. Every calculation here works on any DFA.
ALL=DFA(0,lambda q,x:0,lambda q:True)
EMPTY=DFA(0,lambda q,x:0,lambda q:False)
ODD=DFA(0,lambda q,x:(q | (int(isinstance(x,int) and x%2==1))),lambda q:q==1)


def check_dfa(dfa, safety=False, statecap=200000):
    # (gin,gout,c,t,prev,started,gamma); for safety gout not used.
    begins=[(dfa.initial,dfa.initial,0,g,-1,0,g) for g in (0,1)]
    todo=deque(begins)
    parent={st:None for st in begins}
    expanded=0
    while todo:
        st=todo.popleft()
        qi,qo,c,t,prev,started,g=st
        expanded+=1
        if expanded>statecap:
            return {'status':'CAPPED','states':expanded}
        # EOS source even: both halves have identical carry at centre.
        if started and c==t:
            ni=dfa.delta(qi,'E')
            if dfa.final(ni):
                if safety:
                    return witness(parent,st,None,g,safety)
                else:
                    dest_symbol='E' if g==0 else f'O{2*prev}'
                    if not dfa.final(dfa.delta(qo,dest_symbol)):
                        return witness(parent,st,None,g,safety)
        # EOS source odd: centre is an actual doubled decimal digit.
        for centre in range(0 if started else 2,19,2):
            d=(centre+c)%10
            if (centre+c)//10 != t:continue
            ni=dfa.delta(qi,f'O{centre}')
            if not dfa.final(ni):continue
            if safety:
                if g==0 or d==(prev if started else 1):
                    return witness(parent,st,centre,g,safety)
            else:
                if g==0:
                    no=dfa.delta(qo,f'O{2*d}')
                else:
                    finalpair=d+(prev if started else 1)
                    no=dfa.delta(dfa.delta(qo,finalpair),'E')
                if not dfa.final(no):
                    return witness(parent,st,centre,g,safety)
        for x in range(1 if not started else 0,19):
            low=(x+c)%10; nc=(x+c)//10
            for nt in (0,1):
                if (x+nt)//10 != t:continue
                high=(x+nt)%10
                digitout=(low+high) if g==0 else (low+1 if not started else low+prev)
                if safety:
                    if g==0 and low!=high:continue
                    if g==1 and low!=(1 if not started else prev):continue
                ni=dfa.delta(qi,x)
                no=qo if safety else dfa.delta(qo,digitout)
                nxt=(ni,no,nc,nt,high,1,g)
                if nxt not in parent:
                    parent[nxt]=(st,x)
                    todo.append(nxt)
    return {'status':'PASS','states':expanded}


def witness(parent,st,centre,g,safety):
    outer=[];cur=st
    while parent[cur] is not None:
        prev,x=parent[cur];outer.append(x);cur=prev
    outer.reverse()
    source=(outer,centre)
    out=normalize(unfold(*source))
    dest=fold(pairs(out))
    assert len(out)==(2*len(outer)+(centre is not None)+g)
    if safety:
        assert successor_is_pal(source) and out==out[::-1]
    else:
        assert relation(source,dest)
    return {'status':'COUNTEREXAMPLE', 'source':source, 'successor':dest,
            'gamma':g,'normalized_digits_lsb':out,'safety':safety,'states':len(parent)}


def main():
    for name,dfa in [('EMPTY',EMPTY),('ALL',ALL),('ODD',ODD)]:
        for safety in [True,False]:
            r=check_dfa(dfa,safety=safety)
            print(name,('SAFETY' if safety else 'CLOSURE'),r)
            assert r['status'] in ('PASS','COUNTEREXAMPLE')
    assert check_dfa(EMPTY,True)['status']=='PASS'
    assert check_dfa(EMPTY,False)['status']=='PASS'
    assert check_dfa(ALL,True)['status']=='COUNTEREXAMPLE'
    assert check_dfa(ALL,False)['status']=='PASS' # All is inductive, but not safe.
    assert check_dfa(ODD,True)['status']=='COUNTEREXAMPLE'  # Odd input pair does not imply nonpalindromic successor.
    assert check_dfa(ODD,False)['status']=='COUNTEREXAMPLE'
    print('DFA_PRODUCT_PASS')

if __name__=='__main__':main()
