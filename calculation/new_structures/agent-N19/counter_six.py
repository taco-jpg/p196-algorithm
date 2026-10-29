#!/usr/bin/env python3
"""Decimal nonregular two-counter centre, complete six-step phase assertions."""
PHASES = [
 ([10],8,0,[5,11],16,0,[8]),
 ([1,9],16,1,[13,7,9],14,1,[15,16]),
 ([3,9,13],14,2,[7,16,9,9],10,2,[12,14]),
 ([7,9,7],10,3,[9,16,13,0,0],2,2,[6,10]),
 ([14,18,15,1],2,4,[0,14,7,1,0],4,2,[13,0]),
 ([5,14,15,7,3],4,5,[2,5,12,8,1,4],8,2,[4]),
 ([11,9,11,15,6],8,5,[4,11,4,17,2,8],16,2,[8]),
]
def fold(k,t):
    l,x,a,m,y,b,r=PHASES[t]
    return l+[x]*(k-a)+m+[y]*(k-b)+r

def pair_step(p):
    c=0;d=[]
    for z in p:
        z+=c;d.append(z%10);c=z//10
    if c:d.append(c)
    return [d[i]+d[-1-i] for i in range(len(d))]

def physical_seed(k):
    a=fold(k,0)
    low=[max(0,x-9) for x in a]
    high=[x-y for x,y in zip(a,low)]
    return int(''.join(map(str,(low+high[::-1])[::-1])))

def check():
    for k in range(5,201):
        p=fold(k,0)+fold(k,0)[::-1]
        n=physical_seed(k)
        for t in range(7):
            assert p[:(len(p)+1)//2]==fold(k,t),(k,t)
            if k<=20 and t<6:
                ss=str(n);assert len(ss)==len(p)
                assert [int(ss[i])+int(ss[-1-i]) for i in range(len(ss))]==p
                n += int(ss[::-1]); ns=str(n)
                assert len(ns)==len(pair_step(p)),(k,t)
                assert [int(ns[-1-i])+int(ns[i]) for i in range(len(ns))]==pair_step(p),(k,t)
            if t<6:p=pair_step(p)
    print('7 exact phase shapes: k=5..200, 196 widths, 1176 pairword steps PASS')
    for k in [201,333,500,750,1000,2000]:
        p=fold(k,0)+fold(k,0)[::-1]
        for t in range(7):
            assert p[:(len(p)+1)//2]==fold(k,t),(k,t)
            if t<6:p=pair_step(p)
    print('6 larger widths through k=2000 PASS')
if __name__=='__main__':check()
