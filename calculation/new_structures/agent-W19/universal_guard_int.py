#!/usr/bin/env python3
"""Independent ordinary Python-bigint checks of universal guarded packet erasure."""
import random
R = random.Random(191913)
C = ((14,9,9,0),(0,14,9,0))
def seed_from_p(e,q,center,guards,mask):
    h=list(e)
    for j,g in enumerate(guards):
        h.extend((g,13))
        h.extend(C[(mask>>j)&1])
    h.extend(q)
    lo=[min(x,9) for x in h]
    hi=[x-y for x,y in zip(h,lo)]
    mid=[] if center is None else [center//2]
    assert center is None or center%2==0
    return int(''.join(map(str,(lo+mid+hi[::-1])[::-1])))
def trial(case,m,e,q,center,guards):
    stages=[set() for _ in range(4)]
    for mask in range(1<<m):
        n=seed_from_p(e,q,center,guards,mask)
        for t in range(4):
            stages[t].add(n)
            if t<3:
                s=str(n)
                n+=int(s[::-1])
    sizes=list(map(len,stages))
    assert sizes==[1<<m,1<<m,1<<m,1],(case,sizes)
    return sum(sizes)
if __name__=='__main__':
    checks=0;choices=0
    for j in range(150):
        m=1+R.randrange(7)
        e=[10+R.randrange(8)]+[R.randrange(19) for _ in range(R.randrange(20))]
        q=[R.randrange(19) for _ in range(R.randrange(30))]
        center=None if j%2 else 2*R.randrange(10)
        guards=[6+R.randrange(3) for _ in range(m)]
        checks+=trial(j,m,e,q,center,guards)
        choices+=(1<<m)
    print('BIGINT_UNIVERSAL_CONTEXT_PASS cases=150 masks='+str(choices)+' four_state_checks='+str(checks))
