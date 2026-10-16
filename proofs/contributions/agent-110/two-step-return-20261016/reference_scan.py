#!/usr/bin/env python3
"""Literal port of P196.Agent6.ExteriorCore.lean, historical ref e775dd342df5.
Finite tests only. No unbounded or Lean verification claimed.
"""
from itertools import product
from collections import defaultdict
def norm(word, incarry):
    result=[]
    e=incarry
    for x in word:
        y=x+e
        result.append(y%10)
        e=y//10
    return tuple(result),e
def trim(c,word):
    end=len(word)
    while end and word[end-1]==c:
        end-=1
    return tuple(word[:end])
def advance(s):
    c,B=s
    k=int(10<=c)
    t=c-9*k
    left,carry_left=norm(B,0)
    right,carry_right=norm(B[::-1],k)
    u=c+carry_left-10*k
    rhs=right[::-1]+(t,) if carry_right==0 else (1,)+right[::-1]
    raw=tuple(x+y for x,y in zip(left+(u,),rhs))
    return (2*t,trim(2*t,raw))
def canon(s):
    c,B=s
    return c in range(2,17,2) and all(x<=18 for x in B) and (not B or B[0]>0) and trim(c,B)==B
assert advance((6,(13,)))==(12,(4,10))
assert advance((12,(4,10)))==(6,(9,1))
assert advance((6,(9,1)))==(12,(18,2))
assert advance((12,(18,2)))==(6,(9,11,5))
assert advance((6,(9,11,5)))==(12,(10,1,7,11))
def bound_scan(maxlen):
    results=[]
    for n in range(maxlen+1):
        count=cycles=same_len=0
        delta=defaultdict(int)
        words=[()] if n==0 else ((head,)+tail for head in range(1,19) for tail in product(range(19),repeat=n-1))
        for B in words:
            s=(6,B)
            if not canon(s):continue
            count+=1
            actual=advance(advance(s))
            delta[len(actual[1])-n]+=1
            if actual==s:cycles+=1
            if len(actual[1])==n:same_len+=1
        results.append((n,count,cycles,same_len,dict(sorted(delta.items()))))
    return results
if __name__=="__main__":
    import sys
    print("original six-state witness: PASS")
    for result in bound_scan(int(sys.argv[1]) if len(sys.argv)>1 else 4):
        print("length,checked,period2,equal-length,lengthDeltaHistogram:",result)
