#!/usr/bin/env python3
"""S12 exact even-centre mod101 structure; NO certificate."""
from itertools import product
import sys
sys.set_int_max_str_digits(0)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
assert len(B)==34 and len(W)==9
def val(xs,b=10):
    return sum(x*pow(b,i,101) for i,x in enumerate(xs))%101
def mom(xs):
    return (sum((-1)**(i//2)*x for i,x in enumerate(xs) if i%2==0)%101,
            sum((-1)**(i//2)*x for i,x in enumerate(xs) if i%2==1)%101)
def rot(v,n):
    e,o=v
    for _ in range(n%4): e,o=-o,e
    return e%101,o%101
def fold(v,n):
    e,o=v
    return (11*(e+o) if n%2 else 9*(o-e))%101
def pairword(q,k,J,U,C):
    H=B+W*q+list(J)+list(U)*k
    return H+list(C)+H[::-1]
def source(P):
    h=len(P)//2
    lo=[max(x-9,0) for x in P[:h]]
    hi=[P[i]-lo[i] for i in range(h)]
    d=lo+([P[h]//2] if len(P)%2 else [])+hi[::-1]
    assert d[-1] and all(0<=x<=9 for x in d)
    return d
def pair(d):return [d[i]+d[-1-i] for i in range(len(d))]
def nextd(d):
    v=[]; carries=[];c=0
    for i in range(len(d)):
        a=d[i]+d[-1-i]+c
        v.append(a%10);c=a//10;carries.append(c)
    if c:v.append(c)
    return v,carries
def integer(d):return int(''.join(map(str,d[::-1])))
def moments_test():
    classes={(0,0)}
    expected=[1,19,361,703,1369,2035,3025,4015,5329,6643,8281,9191,10201]
    for j,n in enumerate(expected):
        assert len(classes)==n
        if j<12:
            p=pow(10,j,101)
            classes={((a+p*x)%101,(x+10*b)%101) for a,b in classes for x in range(19)}
    for h in range(1,8):
        possible={0}
        for i in range(h):
            w=(pow(10,i,101)+pow(10,2*h-1-i,101))%101
            possible={(a+w*x)%101 for a in possible for x in range(19)}
        assert len(possible)==min(101,18*h+1)
    print('PASS all junction/centre residue counts')
def folded_test():
    for U in [(9,a,18-a) for a in range(0,19,2)]:
        for J,C in [((5,),(1,1)),((4,12),(12,4,4,12)),((18,6,10),(2,8,12,12,8,2))]:
            for q,k in product(range(20,24),range(40,44)):
                P=pairword(q,k,J,U,C);X=P[:len(P)//2];e,o=mom(X)
                assert val(P)==fold((e,o),len(X))
                h=34+9*q+len(J)+3*k
                ce,co=mom(C[:len(C)//2]);ue,uo=mom(U*5)
                de,do=rot(((ue+co-ce)%101,(uo-ce-co)%101),h)
                Q=pairword(q,k+5,J,U,C);Y=Q[:len(Q)//2]
                assert mom(Y)==((e+de)%101,(o+do)%101)
                assert val(Q)==fold(mom(Y),len(Y))
    print('PASS 480 all-class folded insertion controls')
def physical_test():
    samples=list(product(range(20,24),range(40,44)))+[(20,20),(40,40),(80,80),(160,160)]
    for q,k in samples:
        P=pairword(q,k,(5,),(9,2,16),(1,1))
        d=source(P);assert pair(d)==P
        n=integer(d);S=val(P);S0=S;L0=len(P);Ks=[]
        for t in range(120):
            assert val(pair(d))==S
            nd,cs=nextd(d)
            g=len(nd)-len(d)
            assert g==(1 if t%4==0 else 0)
            K=sum(c*pow(-10,i+1,101) for i,c in enumerate(cs))%101
            Sn=val(pair(nd))
            assert Sn==((2+9*g)*S+2*pow(10,len(d)+g-1,101)*K)%101
            assert integer(nd)==n+int(str(n)[::-1])
            d=nd;n=integer(d);S=Sn;Ks.append(K)
        total=(84*S0+57*pow(10,L0,101)*sum(
           pow(7,r,101)*(8*Ks[4*r]+4*Ks[4*r+1]+2*Ks[4*r+2]+Ks[4*r+3])
           for r in range(30)))%101
        assert total==S
    print('PASS 20 genuine 120-step digit-vector/native-bigint controls')
if __name__=='__main__':
    moments_test();folded_test();physical_test()
    print('S12 ALL TESTS PASS; NO RETURN CERTIFICATE CLAIMED')
