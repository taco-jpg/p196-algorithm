#!/usr/bin/env python3
"""Independent folded two-ended carry transducers, even palindromic pairwords.

Carries in states are guessed on the upper side, verified against true central
carry after the full lower half. No ordinary integer addition is performed here.
"""
from random import Random
from dyadic import pairword, predicted_first_half, predicted_second_half, next_pair


def even_to_even_gamma0(src,tgt,b=10):
    assert len(src)==len(tgt)
    states={(0,0)} # (lower carry in, upper carry out) at outer edge
    for p,q in zip(src,tgt):
        new=set()
        for c,f in states:
            for next_f in (0,1):
                v=p+next_f
                if v//b!=f:continue
                u=p+c
                if u%b + v%b != q:continue
                new.add((u//b,next_f))
        states=new
    return any(c==f for c,f in states)


def even_to_odd_gamma1(src,tgt,b=10):
    assert len(tgt)==len(src)+1
    p=src[0];q=tgt[0]
    states=set()
    for next_f in (0,1):
        if (p+next_f)//b==1 and (p%b)+1==q:
            states.add((p//b,next_f,(p+next_f)%b))
    for p,q in zip(src[1:],tgt[1:-1]):
        new=set()
        for c,f,prev_v in states:
            for next_f in (0,1):
                v=p+next_f;u=p+c
                if v//b!=f:continue
                if (u%b)+prev_v!=q:continue
                new.add((u//b,next_f,v%b))
        states=new
    return any(c==f and 2*v==tgt[-1] for c,f,v in states)


def test():
    r=Random(153415)
    positives=negatives=0
    for h in range(1,15):
        P=pairword(h)
        Q,_=next_pair(P)
        H=P[:len(P)//2]
        T=predicted_first_half(h)
        assert even_to_even_gamma0(H,T)
        assert not even_to_even_gamma0(H,T[:-1]+[(T[-1]+1)%19])
        positives+=1;negatives+=1
        if h>=2:
            R,_=next_pair(Q)
            H1=Q[:len(Q)//2]
            T2=predicted_second_half(h)
            assert even_to_odd_gamma1(H1,T2)
            assert not even_to_odd_gamma1(H1,T2[:-1]+[(T2[-1]+1)%19])
            positives+=1;negatives+=1
    for i in range(2000):
        # The 0/1 external carry must agree with actual normalisation.
        m=r.randrange(1,25)
        H=[r.randrange(0,19) for _ in range(m)]
        P=H+H[::-1]
        Q,d=next_pair(P)
        gamma=len(d)-len(P)
        if gamma==0:
            assert even_to_even_gamma0(H,Q[:m])
        else:
            assert gamma==1
            assert even_to_odd_gamma1(H,Q[:m+1])
        positives+=1
    print('FOLDED_CARRY_PASS',positives,'positive relations;',negatives,'single-digit mutation rejection controls')
if __name__=='__main__':test()
