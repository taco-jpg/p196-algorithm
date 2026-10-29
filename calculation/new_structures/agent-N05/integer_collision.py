#!/usr/bin/env python3
"""Independent ordinary-decimal integer coalescence control for the phase-7 glider.
Run: python3 calculation/new_structures/agent-N05/integer_collision.py
"""
import hashlib
from phase_packet import B0, bulk, pair, realize, revadd

PHASE=7;X=1008;BAND=3000
A=[17,8,0,2]
B=[17,3,10,6]

def make_seed(p):
    left=B0+[bulk(0,34+j) for j in range(BAND)]
    initial=left+[0,0]+left[::-1]
    n=realize(initial)
    for _ in range(PHASE):n=revadd(n)
    word=pair(n)
    assert all(word[X+j]==bulk(PHASE,X+j) for j in range(4))
    for j,v in enumerate(p):word[X+j]=word[-1-X-j]=v
    return realize(word)

x,y=make_seed(A),make_seed(B)
assert x!=y
for step in range(3):
    assert x!=y,step
    assert pair(x)!=pair(y) if step<2 else pair(x)==pair(y)
    x=revadd(x);y=revadd(y)
assert x==y
print('PAIRWORDS_EQUAL_AT_STEP_2; INTEGERS_EQUAL_AT_STEP_3')
print('coalesced_decimal_digits',len(str(x)))
print('coalesced_sha256',hashlib.sha256(str(x).encode()).hexdigest())
for step in range(3,1000):
    s=str(x)
    assert s!=s[::-1]
    x=revadd(x)
print('CONTINUED_997_NONPALINDROMIC_INTEGERS_PASS')
