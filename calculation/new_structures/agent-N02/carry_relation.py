#!/usr/bin/env python3
"""Agent N02: finite-state reverse-add relation on palindromic PAIR halfwords.
Symbols a_j are paired digit sums (0..2b-2), least-significant first.
This is an exact finite-state *relation*, not a claim of a decimal Lychrel number.
"""
from collections import deque
from dataclasses import dataclass
import itertools
import random
import sys


def full_word(a, odd):
    return list(a) + list(reversed(a[:-1] if odd else a))


def literal_step(a, odd, b=10):
    """Independent direct base-b integer calculation; no guessed carries."""
    p = full_word(a, odd)
    z = sum(x*b**j for j,x in enumerate(p))
    ds = []
    while z:
        z,r = divmod(z,b)
        ds.append(r)
    # n can remain the same length or increase by exactly one.
    if len(ds) not in (len(p), len(p)+1):
        raise ValueError(('length',p,ds))
    gam = len(ds)-len(p)
    q = [ds[j]+ds[-j-1] for j in range(len(ds))]
    return gam, tuple(q[:(len(q)+1)//2])


def relation_outputs(a,odd,b=10):
    """Nondeterministic end-to-centre two-sided carry automaton.
    Both possible gamma values are tried, and *only* central-consistent
    paths are accepted. For a physical pairword, there is one output.
    """
    out = set()
    h = len(a)-int(odd)
    for gam in (0,1):
        paths = [(0,gam,None,())]  # carry from low end, from high end, delayed high digit, emitted word
        for j in range(h):
            aj = a[j]
            nxt=[]
            for low,high,prev,word in paths:
                lowdigit=(aj+low)%b
                low2=(aj+low)//b
                for high2 in (0,1):
                    if (aj+high2)//b != high:
                        continue
                    highdigit=(aj+high2)%b
                    z = lowdigit+highdigit if gam==0 else lowdigit+(gam if j==0 else prev)
                    nxt.append((low2,high2,highdigit,word+(z,)))
            paths=nxt
        for low,high,prev,word in paths:
            if odd:
                centre=a[-1]
                if centre % 2: continue
                val=centre+low
                if val//b!=high: continue
                mid=val % b
                # For odd input, the centre is present once, not twice.
                z=(2*mid if gam==0 else mid+(prev if h else gam))
                out.add((gam,word+(z,)))
            elif low==high:
                extra=(2*prev,) if gam==1 else ()
                out.add((gam,word+extra))
    return out

@dataclass
class DFA:
    """A DFA for halfwords. Missing transitions go to an explicit sink."""
    initial: int
    finals: set
    table: list

    def go(self,s,a): return self.table[s][a]


def odd_guard_dfa(b):
    """Accepts nonempty halfwords with first coefficient !=0 and an odd symbol."""
    alpha=2*b-1
    tab=[[3]*alpha for _ in range(4)]
    for a in range(alpha):
        if a:
            tab[0][a] = 2 if a%2 else 1
        tab[1][a] = 2 if a%2 else 1
        tab[2][a] = 2
    return DFA(0,{2},tab)


def guard_check(dfa,b):
    """Conservative, exact regular guard: all accepted strings are nonempty,
    begin nonzero, and contain some odd coefficient.
    """
    q=deque([(dfa.initial,True,False)])
    seen=set(q)
    while q:
        s,first,odd=q.popleft()
        if s in dfa.finals and (first or not odd):
            return False
        for a in range(2*b-1):
            if first and a==0: continue
            x=(dfa.go(s,a),False,odd or a%2==1)
            if x not in seen: seen.add(x);q.append(x)
    # Also forbid accepted strings starting with zero (even if they have odd later).
    q=deque([(dfa.go(dfa.initial,0),False)])
    seen=set(q)
    while q:
        s,first=q.popleft()
        if s in dfa.finals: return False
        for a in range(2*b-1):
            x=(dfa.go(s,a),False)
            if x not in seen:seen.add(x);q.append(x)
    return True


def inclusion_counterexample(source,target,odd,gam,b=10):
    """Exact unbounded-word inclusion R_gamma(L_source) subset L_target.
    Returns None on complete finite-graph acceptance; otherwise a witness.
    For every source halfword whose central parity is physically legal,
    check the unique normalized successor against target DFA.
    """
    # state: (src, dst, low, high, prev_high, first)
    start=(source.initial,target.initial,0,gam,-1,True)
    q=deque([start]); trace={start:()}
    while q:
        state=q.popleft()
        src,dst,low,high,prev,first=state
        a_prefix=trace[state]
        if odd:
            # One final centre cell a_h, necessarily even; check carry meeting.
            for centre in range(0,2*b-1,2):
                if first and centre==0:continue
                if source.go(src,centre) not in source.finals:continue
                w=centre+low
                if w//b != high:continue
                e=w%b
                out_centre=2*e if gam==0 else e+(prev if not first else gam)
                if target.go(dst,out_centre) not in target.finals:
                    return {'input':list(a_prefix+(centre,)),'input_odd':True,'gamma':gam,
                            'output':list(literal_step(a_prefix+(centre,),True,b)[1]),
                            'reason':'output rejected'}
        elif not first and src in source.finals and low==high:
            dst_final=target.go(dst,2*prev) if gam else dst
            if dst_final not in target.finals:
                return {'input':list(a_prefix),'input_odd':False,'gamma':gam,
                        'output':list(literal_step(a_prefix,False,b)[1]),
                        'reason':'output rejected'}
        # Consume a symmetric PAIR at each iteration.
        for aj in range(2*b-1):
            if first and aj==0:continue
            src2=source.go(src,aj)
            ldig=(aj+low)%b
            low2=(aj+low)//b
            for high2 in (0,1):
                if (aj+high2)//b!=high:continue
                hdig=(aj+high2)%b
                out=ldig+hdig if gam==0 else ldig+(gam if first else prev)
                dst2=target.go(dst,out)
                nxt=(src2,dst2,low2,high2,hdig,False)
                if nxt not in trace:
                    trace[nxt]=a_prefix+(aj,)
                    q.append(nxt)
    return None


def finite_certificate(dfas,b):
    """Phase-indexed DFA cycle: keyed by (phase,oddness), each time phase
    increments modulo q. Both possible length increments are checked.
    Soundness is the induction in the report. This function is a finite
    checker (no bounded-word enumeration).
    """
    q=len(dfas)
    for t,row in enumerate(dfas):
        for odd,source in enumerate(row):
            if not guard_check(source,b):
                return {'ok':False,'why':'invalid source-language guard','phase':t,'odd':odd}
            for gam in (0,1):
                target=dfas[(t+1)%q][(odd+gam)%2]
                witness=inclusion_counterexample(source,target,odd,gam,b)
                if witness is not None:
                    return {'ok':False,'phase':t,'odd':odd,'gamma':gam,'witness':witness}
    return {'ok':True,'mode':'finite regular-language induction','phases':q}


def selftest():
    # Exhaustively exercise complete two-sided carry paths on small alphabets.
    counts={}
    for b,max_h in ((2,5),(3,4),(10,3)):
        total=0
        for odd in (False,True):
            for k in range(1,max_h+1):
                for a in itertools.product(range(2*b-1),repeat=k):
                    if a[0]==0 or (odd and a[-1]%2):continue
                    n=len(full_word(a,odd))
                    # Exclude any degenerate zero-length illegal leading number.
                    direct=literal_step(a,odd,b)
                    observed=relation_outputs(a,odd,b)
                    if observed!={direct}:
                        raise AssertionError((b,a,odd,observed,direct))
                    total+=1
        counts[b]=total
    r=random.Random(20261028)
    for b in (9,10,13,50):
        for t in range(1000):
            k=r.randint(1,25)
            odd=bool(r.randrange(2))
            a=[r.randrange(2*b-1) for _ in range(k)]
            a[0]=r.randint(1,2*b-2)
            if odd:
                a[-1]&=~1
                if len(a)==1 and a[0]==0:a[0]=2
            assert relation_outputs(a,odd,b)=={literal_step(a,odd,b)}
    dfa=odd_guard_dfa(10)
    assert guard_check(dfa,10)
    failures=[]
    for odd in (False,True):
        for gam in (0,1):
            ce=inclusion_counterexample(dfa,dfa,odd,gam,10)
            if ce:
                inp=ce['input']
                observed=literal_step(inp,odd,10)
                assert observed==(gam,tuple(ce['output'])), (ce,observed)
                failures.append(ce)
    print('EXHAUSTIVE',counts,'RANDOM',4000)
    print('BROAD_DECIMAL_ODD_GUARD_FAILURES',len(failures),'of 4 parity/overflow modes')
    for x in failures:print('WITNESS',x)
    print('N02_CARRY_TRANSDUCER_SELFTEST_PASS')

if __name__=='__main__': selftest()