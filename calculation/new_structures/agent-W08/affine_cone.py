#!/usr/bin/env python3
"""W08: universal three-renewal carry-cone certificate (Python standard library)."""
import argparse
import json

B = [17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W = [17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]


def shield(cut):
    u = [1] * cut
    for j, v in ((13,7), (20,7), (30,6)):
        if j < cut:
            u[j] = v
    return [8,0,0] + u


def step_of_known_prefix(p, total_length):
    """Sound for ALL palindromic 0..18 pairwords extending prefix p.

    Two carry guesses at entry of known mirrored high suffix dominate all possible
    completions. Returns only consecutive pair positions certain in both guesses.
    """
    L = len(p)
    assert 2*L <= total_length, (L,total_length)
    def norm(word, carry):
        out=[]
        for x in word:
            z=x+carry
            out.append(z%10)
            carry=z//10
        return out,carry
    low,_=norm(p,0)
    high0,g0=norm(p[::-1],0)
    high1,g1=norm(p[::-1],1)
    assert g0==g1, 'unknown centre could change decimal length'
    g=g0
    if not g:
        assert high0[-1] != 0 and high1[-1] != 0, 'leading zero ambiguity'
    out=[]
    for i in range(L):
        if g and i==0:
            a=b=1
        else:
            j=L-i-(0 if g else 1)
            a,b=high0[j],high1[j]
        if a != b:
            break
        out.append(low[i]+a)
    return out,total_length+g,g


def certificate(cut=144, steps=264, centre_length=0):
    assert cut>=31 and centre_length>=0
    A=shield(cut)
    known=B+W+A
    n=2*len(known)+centre_length
    phase={}
    checkpoints={}
    overflow=[]
    known_lengths=[]
    for t in range(steps+1):
        known_lengths.append(len(known))
        assert len(known)>=39, ('root lost',t)
        if t<8:phase[t]=known[:39]
        assert known[:39]==phase[t%8], ('root phase lost',t)
        assert any(x%2 for x in known[:39]), ('palindrome witness lost',t)
        if t in (88,176,264):
            assert len(known)>=59 and known[39:59]==W, ('band renewal failed',t)
            checkpoints[t]=len(known)
        if t==steps:break
        known,n,g=step_of_known_prefix(known,n)
        assert g==(t%2==0), ('overflow schedule lost',t,g)
        overflow.append(g)
    return {'cut':cut,'steps':steps,'start_known':62+cut,'end_known':len(known),
        'checkpoints':checkpoints,'overflow_ones':sum(overflow),
        'odd_witness_indices':[next(i for i,x in enumerate(phase[t]) if x%2) for t in range(8)],
        'known_lengths_88':[known_lengths[t] for t in (0,88,176,264) if t<=steps]}

if __name__ == '__main__':
    a=argparse.ArgumentParser();a.add_argument('--cut',type=int,default=144)
    a.add_argument('--steps',type=int,default=264)
    a.add_argument('--centre-length',type=int,default=0)
    args=a.parse_args()
    print(json.dumps(certificate(args.cut,args.steps,args.centre_length),sort_keys=True))
