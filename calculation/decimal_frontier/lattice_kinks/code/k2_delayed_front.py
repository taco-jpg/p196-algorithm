#!/usr/bin/env python3
"""A non-erasing one-step front jump of exactly 9k in the decimal p12/m9 lattice, for every k>=2."""
from pathlib import Path
import sys
from k2_gate_extension import load, word, norm, ordinary, bigint_pairs
SWITCH=(9,5,0,15,3,12,14)

def paired(P):
    out,c=norm(P)
    if c[-1]:out.append(c[-1])
    return [out[i]+out[-1-i] for i in range(len(out))],c[-1]

def case(k,W,B):
    assert k>=2
    n=200+30*k
    P=word(1,n,W,B)
    Q=P[:]
    for h,value in enumerate(SWITCH):
        j=59+h
        Q[j]=Q[n-1-j]=value
    j2=59+9*k
    assert P[j2]==4 and j2+30<n//2
    Q[j2]=Q[n-1-j2]=5
    po,gp=paired(P);qo,gq=paired(Q)
    assert gp==gq==0
    initial=[i for i in range(n//2) if Q[i]!=P[i]]
    changed=[i for i in range(n) if po[i]!=qo[i]]
    assert initial[0]==59
    assert changed==[j2,n-1-j2],(k,changed)
    assert qo[j2]-po[j2]==2 and qo[n-1-j2]-po[n-1-j2]==2
    assert ordinary(P)==tuple(po) and ordinary(Q)==tuple(qo)
    return n,j2

def main():
    path=sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).resolve().parents[1]/'data'/'lat_p12m9.txt')
    G,W,c,B=load(path)
    assert G[1]==0
    for k in (2,3,4,5,6,7,8,9,10,20,30,50,100):
        n,j2=case(k,W,B)
        P=word(1,n,W,B);Q=P[:]
        for h,value in enumerate(SWITCH):
            j=59+h;Q[j]=Q[n-1-j]=value
        Q[j2]=Q[n-1-j2]=5
        assert bigint_pairs(P)==ordinary(P)
        assert bigint_pairs(Q)==ordinary(Q)
        print(f'k={k} n={n} first_input=59 first_output={j2} exact_jump={j2-59} successor_defect_nonzero=2 PASS')
    print('ALL-k PAPER PROOF: invisible 7-column carry-return motif at 59 + separated noninvisible 4->5 at 59+9k; every other paired output column agrees.')
if __name__=='__main__':main()
