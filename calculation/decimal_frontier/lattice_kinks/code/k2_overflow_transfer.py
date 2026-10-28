#!/usr/bin/env python3
"""Exact complete overflow-phase finite-support response for p12/m9 decimal lattice.
Needs only sibling k2_gate_extension.py and the checked-in lattice data file.
"""
from collections import deque
from pathlib import Path
import sys
from k2_gate_extension import load, word, norm, ordinary, bigint_pairs

def table(t,W,B,n=400):
    P=word(t,n,W,B);O,c=norm(P)
    assert c[-1]==1
    return [(P[i],P[i-1],O[i]+O[n-i],c[i],c[n-i+1],c[i+1],c[n-i])
            for i in (34+18+r for r in range(9))]

def step(tab,r,a,b,prev,first=False):
    q,_,S,*_=tab[r]
    for x in range(19):
        if first and x==q:continue
        for upper_in in (0,1):
            if (prev+upper_in)//10!=b:continue
            if (x+a)%10+(prev+upper_in)%10!=S:continue
            yield ((r+1)%9,(x+a)//10,upper_in,x),x

def shortest(tab,r):
    q,prev,S,a,b,*_=tab[r]
    queue=deque([(state,[x]) for state,x in step(tab,r,a,b,prev,True)])
    seen=set()
    while queue:
        state,path=queue.popleft(); rr,aa,bb,v=state
        if (aa,bb,v)==(tab[rr][3],tab[rr][4],tab[rr][1]):return path,len(seen)
        if state in seen:continue
        seen.add(state)
        for nxt,x in step(tab,rr,aa,bb,v):queue.append((nxt,path+[x]))
    return None,len(seen)

def full_pairs(P):
    O,c=norm(P)
    if c[-1]:O.append(c[-1])
    return tuple(O[i]+O[-1-i] for i in range(len(O))),c[-1]

def run(path):
    gam,W,cup,B=load(path)
    assert [t for t,g in enumerate(gam) if g]==[0,4,8]
    excluded=[]
    for t in (0,4,8):
        tab=table(t,W,B)
        for n in (400,401,418,419,490,491):
            P=word(t,n,W,B);O,c=norm(P)
            assert c[-1]==1
            for r in range(9):
                for k in range(3):
                    i=34+18+r+9*k
                    assert (P[i],P[i-1],O[i]+O[n-i],c[i],c[n-i+1],c[i+1],c[n-i])==tab[r]
        successes=[];sizes=[]
        for r in range(9):
            witness,visited=shortest(tab,r);sizes.append(visited)
            if witness is None:
                excluded.append((t,r));continue
            successes.append((r,witness))
            assert len(witness)==2
            assert witness[1]==tab[(r+1)%9][0] # original q at next site; only first site changed
            for n in (200,201,210,211,400,401,418,419,700,701,1800,1801):
                original=word(t,n,W,B);expected=ordinary(original)
                for k in range(8):
                    j=34+18+r+9*k
                    if j+len(witness)+12>=n//2:continue
                    changed=original[:]
                    for u,x in enumerate(witness):changed[j+u]=changed[n-1-j-u]=x
                    assert changed!=original
                    assert full_pairs(original)==full_pairs(changed)
                    assert ordinary(changed)==expected
                    if n in (200,400,701,1800) and k==0:
                        assert bigint_pairs(original)==bigint_pairs(changed)==expected
        assert len(successes)==8 and len(sizes)==9
        print('PHASE',t,'EXCLUDED',[r for r in range(9) if all(r!=rr for rr,_ in successes)],
              'SUCCESSFUL_FIRST_RESIDUES_AND_MOTIFS',successes,
              'EXPLORED_STATES',sizes,flush=True)
    assert excluded==[(0,7),(4,4),(8,1)]
    print('COMPLETE: 27 phase/residue starts; exact 9*2*2*19=684 state transfer; 3 first-defect exclusions, 24 realizable one-site motifs, independent digit-list and big-integer controls PASS')

if __name__=='__main__':
    path=sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).resolve().parents[1]/'data'/'lat_p12m9.txt')
    run(path)
