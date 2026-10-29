#!/usr/bin/env python3
"""Independent physical-digit replay of phase-9 collar endpoints (not a certificate)."""
import itertools, random, sys
from proto import B,W,collar_step,collar_replay,pair
sys.set_int_max_str_digits(0)

def source_digits(h,C):
    p=h+C+h[::-1]
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=max(0,p[i]-9);d[-1-i]=min(9,p[i])
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]>0
    assert [d[i]+d[-1-i] for i in range(len(d))]==p
    return d

def schoolbook(d):
    carry=0;out=[]
    for i in range(len(d)):
        v=d[i]+d[-1-i]+carry
        out.append(v%10);carry=v//10
    if carry:out.append(carry)
    while len(out)>1 and out[-1]==0:out.pop()
    return out

def check(q,k,J,U,C,nsteps=120):
    h=pair(J,U,q,k);d=source_digits(h,C)
    n=int(''.join(map(str,d[::-1])))
    collar=h[:min(300,len(h))] if q==14 else h[:34+9*q+len(J)+3*60]
    overflow=[];min_radius=len(collar)
    for t in range(nsteps):
        # The true pairword is determined by the full physical digits.
        p=[d[i]+d[-1-i] for i in range(len(d))]
        assert p[:len(collar)]==collar,(q,k,J,U,C,t,'collar not equal physical pairword')
        nextcollar,info=collar_step(collar)
        assert nextcollar is not None,(q,k,J,U,C,t,info)
        nd=schoolbook(d)
        bn=n+int(str(n)[::-1])
        assert nd==list(map(int,str(bn)[::-1])),(q,k,J,U,C,t,'two physical implementations diverged')
        overflow.append(len(nd)-len(d))
        assert info[0]==overflow[-1],(q,k,J,U,C,t,'collar/physical overflow mismatch')
        collar=nextcollar;min_radius=min(min_radius,len(collar))
        d=nd;n=bn
    assert len(d)==len(h)*2+len(C)+30
    assert overflow==[0,0,0,1]*30,(q,k,J,U,C,overflow)
    h2=pair(J,U,q,k+5);expected=h2+C+h2[::-1]
    truepair=[d[i]+d[-1-i] for i in range(len(d))]
    pos=next((i for i,(a,b) in enumerate(zip(expected,truepair)) if a!=b),-1)
    if q==14:
        m,info=collar_replay(J,U,q,k)
        assert (m[0],m[1],m[2])==(pos,truepair[pos],expected[pos]),(q,k,J,U,C,pos,m)
    assert pos>=0 and pos<len(collar)
    return (q,k,len(J),tuple(U),len(C),pos,min_radius)

if __name__=='__main__':
    random.seed(1818)
    Ulist=[]
    for a in range(0,19,2):
        Ulist.extend([(9,a,18-a),(a,18-a,9),(18-a,9,a)])
    tests=[]
    for jlen in (3,4):
        for rank in (0,1,2,5,11,16,20,29):
            J=[random.randrange(19) for _ in range(jlen)]
            for C in ([4,14,4],[4,4],[18,0,18],[0,0],[0,2,0]):
                tests.append((14,100,J,list(Ulist[rank]),C))
    for q,k in ((20,80),(40,160),(80,320),(160,640)):
        for jlen in (3,4):
            J=[random.randrange(19) for _ in range(jlen)]
            for C in ([4,14,4],[4,4]):
                tests.append((q,k,J,list(Ulist[(q+jlen)%30]),C))
    for args in tests:
        result=check(*args)
    print('AUDIT_PASS cases=',len(tests),'widths=',sorted(set((t[0],t[1]) for t in tests)),
          'centre_lengths=',sorted(set(len(t[4]) for t in tests)))