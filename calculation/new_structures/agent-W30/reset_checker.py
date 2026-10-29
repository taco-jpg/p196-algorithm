#!/usr/bin/env python3
"""Independent compact 32-row ×680-bit exact certificate checker.

This checker does NOT import fibre_graph.py or the full-rooted orbit. It uses
12 spatial periods of direct carry recurrence to obtain the unique two-sided
periodic carry fibres, and verifies the exact 680-bit physical prefix witness.
"""
from pathlib import Path
import json,hashlib

def carry(row,reversed_order):
    result=[]
    for start in (0,1):
        c=start; last=[None]*5
        for k in range(60):
            i=(-k if reversed_order else k)%5
            if k>=55:last[i]=c
            c=(row[i]+c)//10
        if c==start:result.append(tuple(last))
    # Technically last c==start only tests after 60 steps, a multiple of five;
    # coefficient!=9 in each 5-cycle ensures unique periodic branch.
    assert len(result)==1,(row,reversed_order,result)
    return result[0]

def check():
    d=json.loads(Path(__file__).with_name('sync_physical.json').read_text())
    bits=d['postbreak_gamma_bits'];assert len(bits)==680
    assert hashlib.sha256(bits.encode()).hexdigest()==d['postbreak_gamma_sha256']
    S={(tuple(x['row']),x['axis']) for x in d['prebreak_rank32_rows']}
    assert len(S)==32 and all(x[1]==4 for x in S)
    complement=lambda x:(tuple(18-v for v in x[0]),x[1])
    assert all(complement(u) in S for u in S)
    # Finite ten-edge lasso: S20 is fixed by (10)^5. With the true 26710-bit
    # alternating prefix, this establishes S26710=S20 for 2,669 repeats.
    lasso=S.copy()
    for g in map(int,d['alternating_overflow_lasso_word']):
        nxt=set()
        for r,axis in lasso:
            l=carry(r,False);h=carry(r,True)
            rr=tuple((r[i]+l[i])%10+(r[(i-g)%5]+h[(i-g)%5])%10 for i in range(5))
            nxt.add((rr,(axis+g)%5))
        lasso=nxt
    assert lasso==S and d['lasso_set_size']==32
    assert d['lasso_repeats_to_t26710']==(26710-d['alternating_overflow_lasso_start'])//10
    ranks=[len(S)]
    for k,g in enumerate(map(int,bits),1):
        Q=set()
        for r,axis in S:
            l=carry(r,False);h=carry(r,True)
            rr=tuple((r[i]+l[i])%10+(r[(i-g)%5]+h[(i-g)%5])%10 for i in range(5))
            ax=(axis+g)%5
            assert all(rr[i]==rr[(ax-i)%5] for i in range(5))
            Q.add((rr,ax))
        S=Q;ranks.append(len(S))
        assert len(S)%2==0 and all(complement(u) in S for u in S)
        assert len(S)>2 or k==680
    assert len(S)==2 and sorted(S)==sorted((tuple(x['row']),x['axis']) for x in d['rank2_complement_pair'])
    print('PASS independent compact 32-row/680-bit reset checker; first rank2 at bit',len(bits),'rank drops',[(i,ranks[i]) for i in range(1,len(ranks)) if ranks[i]<ranks[i-1]])

if __name__=='__main__':check()
