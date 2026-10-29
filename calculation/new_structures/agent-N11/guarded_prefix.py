#!/usr/bin/env python3
"""Independent randomized check of exact guarded one-step prefix contraction.
For pairwords P, Q with common lower prefix length K+1 and P[K] != 9,
check equal overflow and equal first K next pair coefficients.
"""
import random

def make(p):
    # Pairword p_i=d_i+d_(n-1-i), MSB-first representation of integer.
    return ''.join(str(min(9,x)) for x in p) + ''.join(str(max(0,x-9)) for x in reversed(p))

def next_word(s):
    a=str(int(s)+int(s[::-1]))
    n=len(s)
    return len(a)-n,[int(a[i])+int(a[-1-i]) for i in range(len(a)//2)]

def run(N=12000):
    rng=random.Random(47411)
    checked=0
    cases={}
    for t in range(N):
        K=rng.randrange(2,30)
        s1=K+2+rng.randrange(1,40)
        s2=K+2+rng.randrange(1,40)
        common=[rng.randrange(19) for _ in range(K+1)]
        common[0]=rng.randrange(1,19)
        common[K]=rng.choice([x for x in range(19) if x!=9])
        if t%3==0: common[:K]=[9]*K
        if t%7==0: common[0]=rng.randrange(10,19)
        p=common+[rng.randrange(19) for _ in range(s1-K-1)]
        q=common+[rng.randrange(19) for _ in range(s2-K-1)]
        if p==q: continue
        a,b=make(p),make(q)
        g1,x=next_word(a)
        g2,y=next_word(b)
        assert g1==g2,(t,K,g1,g2,p,q)
        assert x[:K]==y[:K],(t,K,g1,x[:K],y[:K],p,q)
        checked+=1
        cases[(g1,K)] = cases.get((g1,K),0)+1
    print('GUARDED PREFIX randomized independent controls PASS',checked,'different-length/centre seed pairs','gamma categories',sorted({g for g,k in cases}))
if __name__=='__main__':run()
