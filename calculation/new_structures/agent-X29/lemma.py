#!/usr/bin/env python3
"""Exhaustive small flank + randomized large flank checks for central-18 pumping."""
import random,itertools
from construct import split,step,pairs

def check(left,core):
 P=list(left)+[18]*core+list(left[::-1]);Q=list(left)+[18]*(core+2)+list(left[::-1])
 a=pairs(step(split(P)));b=pairs(step(split(Q)))
 m=len(a)//2
 return b==a[:m]+[18,18]+a[m:]
for length in (1,2,3):
 ct=0
 for left in itertools.product(range(1,19),*([range(19)]*(length-1))):
  for core in (5,6,7):
   assert check(left,core),(left,core)
   ct+=1
 print('exhaustive length',length,'cases',ct)
rng=random.Random(62929)
for i in range(20000):
 left=[rng.randrange(1,19)]+[rng.randrange(19) for _ in range(rng.randrange(1,100))]
 assert check(left,rng.randrange(5,100))
print('PASS 20k random and exhaustive short flank checks, central length >=5')
