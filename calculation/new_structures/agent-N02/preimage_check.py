#!/usr/bin/env python3
"""Independent word and integer controls for N02 all-length regular preimages.
Uses literal place-value arithmetic and ordinary-digit replay, never the
nondeterministic carry transducer to compute the expected successor.
"""
import itertools
import random
from carry_relation import odd_guard_dfa,literal_step
from regular_preimage import preimage,dfa_prefix,shortest,run
from decimal_cut_probe import exterior_rows
from independent_digit_check import digits_of_pairword,ordinary_reverse_add,half_of_pairword

def accepts(d,word):
    s=d.initial
    for a in word:s=d.go(s,a)
    return s in d.finals

def check_preimage():
    r=random.Random(20261029);checks=0
    base=10
    targets=[odd_guard_dfa(base),dfa_prefix([17,5],False),dfa_prefix([9,0],True)]
    for odd in (0,1):
      for gam in (0,1):
       for T in targets:
        pre=preimage(T,bool(odd),gam)
        for k in (1,2,3,4,5,6,12):
         for j in range(220):
          a=[r.randrange(19) for _ in range(k)]
          a[0]=r.randrange(1,19)
          if odd:a[-1]&=~1
          if odd and k==1 and a[0]==0:a[0]=2
          got=accepts(pre,a)
          gamma,y=literal_step(a,odd,base)
          expect=gamma==gam and accepts(T,y)
          assert got==expect,(odd,gam,a,got,expect)
          checks+=1
    print('N02_PREIMAGE_RANDOM_LITERAL_PASS',checks)

def check_decimal():
    # A real 80-digit number whose pairword lower half is the known p8 rec0 prefix.
    BB=exterior_rows();a=BB[0]+[0];d=digits_of_pairword(a,False,10)
    for t in range(2):
        d=ordinary_reverse_add(d,10)
        out=half_of_pairword(d)
        if t==0:assert list(out[:39])==BB[1]
        if t==1:assert list(out[:39])!=BB[2]
    print('N02_DECIMAL_TWO_STEP_LITERAL_PASS',len(d))

def has_unbounded_language(d):
    from collections import deque
    n=len(d.table)
    reverse=[set() for _ in range(n)]
    for s,row in enumerate(d.table):
        for t in row:reverse[t].add(s)
    live=set(d.finals);q=deque(live)
    while q:
        for s in reverse[q.popleft()]:
            if s not in live:live.add(s);q.append(s)
    seen=set();ongoing=set()
    def dfs(s):
        seen.add(s);ongoing.add(s)
        for t in set(d.table[s]):
            if t not in live:continue
            if t in ongoing:return True
            if t not in seen and dfs(t):return True
        ongoing.remove(s)
        return False
    return d.initial in live and dfs(d.initial)

def check_depth6():
    D=run(6)
    B=exterior_rows()
    overflow=[1,0,1,0,1,0,1,0]
    total=0
    for t in range(8):
        for odd in (0,1):
            word=shortest(D[t][odd])
            assert word is not None and has_unbounded_language(D[t][odd])
            d=digits_of_pairword(word,bool(odd),10)
            for i in range(6):
                assert d!=d[::-1]
                prior=len(d)
                d=ordinary_reverse_add(d,10)
                assert len(d)-prior==overflow[(t+i)%8]
                pair=half_of_pairword(d)
                assert tuple(pair[:39])==tuple(B[(t+i+1)%8])
                total+=1
    print('N02_DEPTH6_ALL_PHASE_INDEPENDENT_DIGIT_REPLAY_PASS',total,'ALL_16_LANGUAGES_UNBOUNDED')

if __name__=='__main__':
    check_preimage();check_decimal();check_depth6()