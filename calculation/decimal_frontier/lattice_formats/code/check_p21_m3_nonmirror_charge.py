#!/usr/bin/env python3
"""Independent fixed-point carry/phase/class checker for all 28 nonmirror cycles."""
from collections import Counter,defaultdict
import sys,math
g=[int(v) for v in '001001010101001010101']
def mirror(v):
    return any(all(v[i]==v[(a-i)%3] for i in range(3)) for a in range(3))
def nxt(v,bit):
    if all(x==9 for x in v):return None
    carries=[]
    for rev in (False,True):
        cand=[]
        for init in (0,1):
            carry=init;a=[0]*3
            for j in range(3):
                i=(3-j)%3 if rev else j
                a[i]=carry;carry=(v[i]+carry)//10
            if carry==init:cand.append(a)
        assert len(cand)==1
        carries.append(cand[0])
    a,d=carries
    return tuple((v[i]+a[i])%10+(v[(i-bit)%3]+d[(i-bit)%3])%10 for i in range(3)),a,d
def canonical(seq):
    return min(tuple(tuple(seq[(j+t)%len(seq)][(i+s)%3] for i in range(3))
                     for j in range(len(seq))) for s in range(3) for t in range(len(seq)))
def audit(path):
    seen=set();hist=Counter();families=defaultdict(list);timesteps=0;phasechecks=0
    for line in open(path):
        if line.startswith('#') or not line.strip():continue
        k,lift,expected,*start=map(int,line.split());start=tuple(start)
        assert len(start)==3 and lift==math.lcm(k,2)
        assert start not in seen;seen.add(start)
        assert not mirror(start)
        state=start;seq=[state];cut=[];qs=[0]*3
        for t in range(21*lift):
            bit=g[t%21];v,a,d=nxt(state,bit)
            assert not mirror(state)
            L=[a[j] for j in range(3)]
            H=[(state[j]+d[j])//10 for j in range(3)]
            Y=[(state[(j-1)%3]+d[(j-1)%3])%10 if bit else 0 for j in range(3)]
            for j in range(3):
                jp=(j+1)%3
                assert v[j]==(state[j]+L[j])%10+(Y[j] if bit else (state[j]+H[jp])%10)
                assert L[jp]==(state[j]+L[j])//10 and H[j]==(state[j]+H[jp])//10
                if bit:assert Y[jp]==(state[j]+H[jp])%10
                qs[j]+=pow(5,t,9)*(L[j]-H[j]+bit*Y[j])
            cut.append((L[0],H[0],Y[0],bit));state=v
            if (t+1)%21==0 and (t+1)<k*21:seq.append(state)
            if (t+1)==k*21:assert state==start
            timesteps+=1
        assert state==start and len(seq)==k and len(set(seq))==k
        assert {v%9 for v in qs}=={expected}
        for off in range(21*lift):
            rot=cut[off:]+cut[:off]
            value=sum(pow(5,t,9)*(L-H+bit*Y) for t,(L,H,Y,bit) in enumerate(rot))%9
            assert (value==0)==(expected==0)
            phasechecks+=1
        hist[(k,expected)]+=1
        families[canonical(seq)].append(expected)
    unit=sum(n for (k,q),n in hist.items() if math.gcd(q,9)==1)
    triple=sum(n for (k,q),n in hist.items() if q in (3,6))
    zero=sum(n for (k,q),n in hist.items() if q==0)
    assert sum(hist.values())==28 and (unit,triple,zero)==(8,12,8)
    assert len(families)==12 and sum(all(q!=0 for q in qs) for qs in families.values())==8
    print('independent PASS: primitive nonmirror cycles=28, classes=12, excluded classes=8')
    print('Q units/order9=',unit,'Q order3=',triple,'Q zero=',zero)
    print('physical temporal steps=',timesteps,'time rotations=',phasechecks)
    print('histogram=',dict(sorted(hist.items())))
if __name__=='__main__':audit(sys.argv[1])
