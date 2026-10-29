#!/usr/bin/env python3
"""New centre construction: replace fixed centre by unrestricted finite-state
suffix with a specified inward carry at an exterior/centre cut.
Run in repository checkout; --standalone uses the embedded source-exterior control.
"""
import argparse
from collections import deque
from pathlib import Path
import re
from carry_relation import DFA,inclusion_counterexample,literal_step
from independent_digit_check import digits_of_pairword,ordinary_reverse_add,half_of_pairword

P8_PATH='''
17 8 17 8 17 8 17 8
5 13 6 14 8 16 13 12
0 5 11 8 17 16 14 9
1 1 2 4 8 16 14 10
13 5 10 3 6 14 10 6
4 8 16 8 17 14 10 2
14 9 18 16 13 12 6 7
12 8 16 16 14 9 0 6
9 2 5 12 6 11 4 4
8 18 17 13 8 14 9 14
15 14 10 9 0 8 17 7
16 13 8 9 0 0 0 8
17 15 12 11 4 4 8 8
13 12 6 9 0 4 8 16
17 12 5 11 4 4 9 18
9 7 16 12 5 9 9 9
1 11 2 9 9 15 10 0
4 5 11 4 10 0 1 2
4 8 16 9 9 0 1 2
11 6 13 11 2 12 4 5
8 10 1 5 11 4 9 14
16 15 11 3 6 8 17 7
0 7 16 9 18 15 11 10
9 10 0 7 15 15 11 4
14 4 9 10 0 6 14 7
11 7 14 4 9 10 0 5
9 2 4 9 18 8 18 9
11 2 4 8 17 17 15 15
6 8 17 12 4 12 6 12
13 10 1 9 9 14 9 16
18 13 7 8 18 8 18 8
9 8 18 16 12 12 5 14
4 14 9 8 18 12 6 11
7 11 4 14 8 17 16 13
17 15 12 7 15 14 10 8
15 14 9 3 6 12 6 7
9 5 12 3 7 13 8 14
7 17 15 9 9 16 14 13
13 11 4 10 1 10 1 6
'''


def exterior_rows():
    rows=[list(map(int,l.split())) for l in P8_PATH.strip().splitlines()]
    assert len(rows)==39 and all(len(r)==8 for r in rows)
    return [[r[t] for r in rows] for t in range(8)]


def transition_function(a,b=10):
    return ((a+0)//b,(a+1)//b)


def cut_dfa(prefix,odd,allowed,base=10):
    """DFA for prefix ++ free centre, with high-side carry c_(n-K)
    required to lie in allowed. The complete lower half is scanned LSB-first.
    Only physically legal odd-length central coefficients are accepted.
    """
    K=len(prefix); A=2*base-1
    def move(s,a):
        if s[0]=='prefix':
            i,l=s[1:]
            if a!=prefix[i]:return ('sink',)
            ln=(a+l)//base
            return ('prefix',i+1,ln) if i+1<K else ('tail',ln,0,1,-1)
        if s[0]=='sink':return s
        _,l,m0,m1,hold=s
        if odd:
            if hold==-1:return ('tail',l,m0,m1,a)
            f0,f1=transition_function(hold,base)
            m0n=(m0,m1)[f0];m1n=(m0,m1)[f1]
            return ('tail',(hold+l)//base,m0n,m1n,a)
        f0,f1=transition_function(a,base)
        return ('tail',(a+l)//base,(m0,m1)[f0],(m0,m1)[f1],-1)
    def accepting(s):
        if s[0]!='tail':return False
        _,l,m0,m1,hold=s
        if odd:
            if hold<0 or hold%2:return False
            midcarry=(hold+l)//base
            highcut=(m0,m1)[midcarry]
        else:highcut=(m0,m1)[l]
        return highcut in allowed
    states=[('prefix',0,0)]; ids={states[0]:0}; tab=[]; finals=set()
    for s in states:
        i=ids[s]
        if accepting(s):finals.add(i)
        row=[]
        for a in range(A):
            nxt=move(s,a)
            if nxt not in ids:
                ids[nxt]=len(states);states.append(nxt)
            row.append(ids[nxt])
        tab.append(row)
    return DFA(0,finals,tab)


def scan():
    BB=exterior_rows();gamma=[1,0,1,0,1,0,1,0]
    repo=Path(__file__).resolve().parents[3]
    original=repo/'calculation/decimal_frontier/lattice_formats/p8_scc.txt'
    if original.exists():
        first=next(line for line in original.read_text().splitlines() if line.startswith('SCC p=8'))
        parsed=[list(map(int,z.split(','))) for z in re.findall(r'\[([^\]]+)\]',first.split(' path=')[1].split(' cyc=')[0])]
        assert parsed==list(map(list,zip(*BB))), 'embedded prefix mismatches tracked p8_scc'
        print('P8_SOURCE_INTEGRITY_PASS')
    print('N02_DECIMAL_P8_PREFIX',len(BB[0]),'g',gamma)
    # A finite-state alphabet of charge-states; each source language is infinite,
    # and the centre can be nonperiodic and grow without any fixed width.
    data={}
    for t in range(8):
        for odd in (0,1):
            for charge in (0,1):
                src=cut_dfa(BB[t],odd,{charge})
                for gam in (0,1):
                    for destallowed in ({0},{1},{0,1}):
                        dst=cut_dfa(BB[(t+1)%8],(odd+gam)%2,destallowed)
                        ce=inclusion_counterexample(src,dst,bool(odd),gam,10)
                        data[t,odd,charge,gam,tuple(sorted(destallowed))]=ce is None
    # For each source and physical gamma, inspect whether the COMPLETE output
    # language stays in the target prefix and in which charge classes.
    report=[]
    for t in range(8):
      for odd in (0,1):
       for charge in (0,1):
        go=gamma[t]
        allok=data[t,odd,charge,go,(0,1)]
        left=data[t,odd,charge,go,(0,)]
        right=data[t,odd,charge,go,(1,)]
        report.append((t,odd,charge,allok,left,right))
    for t,odd,r,allok,lo,hi in report:
        print('CHARGE',t,odd,r,'prefix',int(allok),'nextCarry0',int(lo),'nextCarry1',int(hi))
    print('N02_DECIMAL_CHARGE_GRAPH_DONE',len(report))

if __name__=='__main__':scan()

def two_step_escape():
    BB=exterior_rows()
    K=len(BB[0])
    src=cut_dfa(BB[0],0,{0})
    target=cut_dfa(BB[1],1,{1})
    witness=inclusion_counterexample(src,target,False,1,10)
    assert witness is not None
    aa=witness['input']
    g1,b1=literal_step(aa,False,10)
    assert g1==1
    # Q1 is the full next pairword, hence can be applied directly to T once more.
    g2,b2=literal_step(b1,True,10)
    assert g2==0
    ok1=list(b1[:K])==BB[1]
    mismatches=[i for i in range(K) if i>=len(b2) or b2[i]!=BB[2][i]]
    assert ok1 and mismatches
    d0=digits_of_pairword(aa,False,10)
    d1=ordinary_reverse_add(d0,10)
    d2=ordinary_reverse_add(d1,10)
    assert half_of_pairword(d1)==b1 and half_of_pairword(d2)==b2
    assert d0!=d0[::-1] and d1!=d1[::-1]
    print('INDEPENDENT_LITERAL_TWO_STEP_REPLAY_PASS',len(d0),len(d1),len(d2))
    print('TWO_STEP_ESCAPE',{
        'seed_pair_half':aa, 'lengths':[2*len(aa),2*len(b1)-1,2*len(b2)-1],
        'overflow':[g1,g2], 'first_output_prefix_ok':ok1,
        'first_bad_after_two':mismatches[0],
        'source_carry_class':0, 'next_required_carry_class':1,
        'next_actual_carry_class':0})

if __name__=='__main__':two_step_escape()