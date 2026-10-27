#!/usr/bin/env python3
"""Independent arithmetic check of R+1 to R prefix graph homomorphism.
PAPER proof is in reports/agent-6-T1-compactness.md, not in this test.
"""
from random import Random

def edges(a):
    n=len(a)
    out=set()
    for upper in (0,1):
        h=[0]*(n+1)
        h[n]=upper
        for i in range(n-1,-1,-1):
            h[i]=(a[i]+h[i+1])//10
        lo=0
        word=[]
        for i in range(n):
            digit=(a[i]+lo)%10
            lo=(a[i]+lo)//10
            rev=1 if h[0] and i==0 else ((a[i-1]+h[i])%10 if h[0] else (a[i]+h[i+1])%10)
            word.append(digit+rev)
        out.add((h[0],tuple(word)))
    return out

def main():
    rng=Random(61027)
    for _ in range(100000):
        n=rng.randrange(2,16)
        a=(rng.randrange(1,19),)+tuple(rng.randrange(19) for _ in range(n-1))
        coarse=edges(a[:-1])
        for g,word in edges(a):
            assert (g,word[:-1]) in coarse,(a,g,word)
    print("PREFIX_PROJECTION_HOMOMORPHISM PASS 100000 random source words; no counterexample")

if __name__=="__main__":
    main()
