#!/usr/bin/env python3
"""Exact positive arithmetic control: a uniform pair-coefficient band has a one-cell erosion rule."""
from random import Random
rng=Random(303030)
cycles=[2,4,8,16,14,10]
assert all(2*((x+(x//10))%10)==cycles[(i+1)%6] for i,x in enumerate(cycles))
checks=0; overflow={0:0,1:0}
for case in range(25000):
    k=rng.randint(6,110)
    a=rng.randint(0,k-5)
    b=rng.randint(a+3,k-1)
    x=cycles[case%6]
    lo=[rng.randrange(10) for _ in range(k)]
    hi=[rng.randrange(10) for _ in range(k)]
    hi[0]=rng.randint(1,9)
    for j in range(a,b+1):
        choices=[u for u in range(10) if 0<=x-u<10 and (j!=0 or x-u!=0)]
        lo[j]=rng.choice(choices)
        hi[j]=x-lo[j]
    centre=''.join(str(rng.randrange(10)) for _ in range(rng.randint(1,60)))
    before=''.join(map(str,hi))+centre+''.join(map(str,reversed(lo)))
    n=int(before)
    after=str(n+int(before[::-1]))
    gamma=len(after)-len(before)
    assert gamma in (0,1)
    Pnext=[int(after[-1-i])+int(after[i]) for i in range(k)]
    target=2*((x+x//10)%10)
    for j in range(a+1,b):
        assert Pnext[j]==target,(case,a,b,x,gamma,j,Pnext[j],target)
        checks+=1
    overflow[gamma]+=1
print('PASS 25000 exact bigint transitions',checks,'interior positions',overflow)
