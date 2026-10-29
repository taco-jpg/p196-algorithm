#!/usr/bin/env python3
"""Exact finite carry relation for a folded base-10 pairword."""
import random

def fold_accept(a, odd, extra, target):
    """State=(low incoming carry, high outgoing carry, previous high digit)."""
    h = len(a) - int(odd)
    if len(target) != h + int(odd) + ((extra + (1-int(odd))) // 2):
        return False
    states = {(0, extra, -1)}
    for i in range(h):
        new = set()
        x = a[i]
        for l, r, prev in states:
            low = (x + l) % 10
            ln = (x + l) // 10
            for rn in (0, 1):
                if (x + rn) // 10 != r: continue
                high = (x + rn) % 10
                y = low + high if not extra else low + (1 if i == 0 else prev)
                if y == target[i]: new.add((ln, rn, high))
        states = new
        if not states: return False
    for l, r, prev in states:
        if odd:
            x = a[-1]
            if (x + l) // 10 != r: continue
            center = (x + l) % 10
            final = 2 * center if not extra else center + prev
            if final == target[-1]: return True
        elif l == r:
            if not extra or target[-1] == 2 * prev: return True
    return False

def native_step(d):
    old = [d[i] + d[-1-i] for i in range(len(d))]
    c = 0; out = []
    for x in old:
        x += c; out.append(x % 10); c = x // 10
    if c: out.append(c)
    return out

def test_random(count=20000):
    rng = random.Random(19); seen=set()
    for _ in range(count):
        n = rng.randrange(4, 90)
        d = [rng.randrange(10) for _ in range(n)]
        d[-1] = rng.randrange(1,10)
        a = [d[i]+d[-1-i] for i in range((n+1)//2)]
        d2 = native_step(d)
        target = [d2[i]+d2[-1-i] for i in range((len(d2)+1)//2)]
        gam = len(d2)-n
        if not fold_accept(a, bool(n%2), gam, target): raise AssertionError((n,a,gam,target))
        if fold_accept(a, bool(n%2), 1-gam, target): raise AssertionError('wrong overflow')
        seen.add((n%2,gam))
    assert len(seen)==4,seen
    print('fold_relation: 20000 random digit-list transitions PASS, all 4 modes')

def test_six_cycle(count=20000):
    rng=random.Random(1919);mapping={8:16,16:14,14:10,10:2,2:4,4:8};worst=0
    for _ in range(count):
        n=rng.randrange(30,220);h=(n+1)//2
        k=rng.randrange(3,h-1);x=rng.choice(list(mapping))
        a=[rng.randrange(19) for _ in range(h)];a[0]=rng.randrange(1,19)
        a[-k:]=[x]*k
        P=a+a[:n//2][::-1]
        carry=0;d=[]
        for p in P:
            s=p+carry;d.append(s%10);carry=s//10
        if carry:d.append(carry)
        Q=[d[i]+d[-1-i] for i in range((len(d)+1)//2)]
        k2=0
        for z in reversed(Q):
            if z!=mapping[x]:break
            k2+=1
        if k2<k-1:raise AssertionError((n,k,x,k2))
        worst=min(worst,k2-k)
    print('uniform_core: 20000 random cases PASS k_next>=k-1, worst',worst)
if __name__=='__main__':
    test_random();test_six_cycle()
