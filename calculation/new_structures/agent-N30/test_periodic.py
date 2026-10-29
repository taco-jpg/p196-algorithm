#!/usr/bin/env python3
from random import Random

R=Random(20261028)
def step(low,high):
    k=len(low)
    ps=[{a+b for a in low[j] for b in high[j]} for j in range(k)]
    c={0}; ll=[]
    for p in ps:
        q={x+z for x in p for z in c}
        ll.append({v%10 for v in q});c={v//10 for v in q}
    c={0,1}; hh=[None]*k
    for j in range(k-1,-1,-1):
        q={x+z for x in ps[j] for z in c}
        hh[j]={v%10 for v in q};c={v//10 for v in q}
    upper=[set() for _ in range(k)]
    if 0 in c:
        for j in range(k):upper[j]|=hh[j]
    if 1 in c:
        upper[0].add(1)
        for j in range(1,k):upper[j]|=hh[j-1]
    return ll,upper

memberships=0; guards=0
for case in range(260):
    k=R.randrange(4,45)
    lo=[{2 if j%2==0 else 6} for j in range(k)]
    hi=[{1 if j==0 else (9 if j%2==0 else 8)} for j in range(k)]
    centre=''.join(str(R.randrange(10)) for _ in range(R.randrange(1,61)))
    n=int(''.join(str(next(iter(s))) for s in hi)+centre+
          ''.join(str(next(iter(s))) for s in lo[::-1]))
    for t in range(90):
        w=str(n)
        assert len(w)>=2*k+1
        for j in range(k):
            assert int(w[-1-j]) in lo[j] and int(w[j]) in hi[j]
            memberships+=1
        if any(lo[j].isdisjoint(hi[j]) for j in range(k)):
            assert w!=w[::-1];guards+=1
        n+=int(w[::-1])
        lo,hi=step(lo,hi)
print('PASS memberships=',memberships,'guarded claims=',guards)
