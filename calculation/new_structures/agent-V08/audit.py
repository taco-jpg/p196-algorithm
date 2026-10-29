#!/usr/bin/env python3
"""V08 independent full-integer and centre-transfer red-team checks; no GMP or imports."""
from itertools import product
import random

def ds(n,b=10):
    a=[]
    while n:
        a.append(n%b);n//=b
    return a or [0]
def val(a,b=10):
    return sum(x*b**i for i,x in enumerate(a))
def step(n,b=10):
    return n+val(ds(n,b)[::-1],b)
def pairs(n):
    a=ds(n)
    return [a[i]+a[-1-i] for i in range(len(a))]
def realize(p):
    assert p==p[::-1] and p[0]>0
    n=len(p); d=[0]*n
    for i in range(n//2):
        d[i]=max(0,p[i]-9);d[-1-i]=p[i]-d[i]
    if n%2:
        assert p[n//2]%2==0
        d[n//2]=p[n//2]//2
    return val(d)
def centerrun(a,x):
    m=len(a)//2
    if a[m]!=x:return 0
    i=j=m
    while i>=0 and a[i]==x:i-=1
    while j<len(a) and a[j]==x:j+=1
    return j-i-1

def n19():
    for k in range(3,21):
        p=[1,18]+[8]*k+[18,1]
        n=realize(p);n2=step(n)
        assert pairs(n)==p and len(ds(n))==len(ds(n2))
        assert centerrun(pairs(n2),16)==k-2
    rng=random.Random(808)
    nxt={2:4,4:8,8:16,16:14,14:10,10:2}
    for _ in range(10000):
        x=rng.choice(list(nxt));k=rng.randrange(3,21)
        L=[rng.randrange(19) for i in range(rng.randrange(1,9))]
        L[0]=rng.randrange(1,19)
        n=realize(L+[x]*k+L[::-1]);n2=step(n)
        gamma=len(ds(n2))-len(ds(n))
        assert centerrun(pairs(n2),nxt[x])>=k-2+gamma
    print("N19: 18 sharp full-integer counterexamples; 10000 corrected-bound controls PASS")
def n24():
    count=0
    for p,x,z in product(range(1,19),range(19),(0,18)):
        P=[p,x,z,z,x,p];n=realize(P)
        c=0;ins=[]
        for v in P:
            ins.append(c);c=(v+c)//10
        u=ins[-2];v=(x+u)//10;g=(p+v)//10
        a0=p%10;a1=(x+p//10)%10
        h0=(p+v)%10;h1=(x+u)%10
        target=(a0+h0,a1+h1) if g==0 else (a0+1,a1+h0)
        assert tuple(pairs(step(n))[:2])==target
        count+=1
    print("N24:",count,"integer edge checks PASS")
def n27():
    count=0
    for b in range(2,9):
        M=2*(b-1)
        for size in range(4):
            for LL in product(range(M+1),repeat=size):
                if LL and LL[-1]==M:continue
                L=list(LL)
                for q in range(3,7):
                    for e,g in product(range(2),repeat=2):
                        C=L+[M]*q+L[::-1];c=e;D=[]
                        for x in C:
                            s=x+c;D.append(s%b);c=s//b
                        if g==0:T=[D[i]+D[-i-1] for i in range(len(D))]
                        else:
                            v=(b-1)*(1-c)
                            T=[a+z for a,z in zip(D+[v],[v]+D[::-1])]
                        h=centerrun(T,M)
                        c=e
                        for x in L:c=(x+c)//b
                        assert h==q-g-2*(1-g)*(1-c)
                        count+=1
    print("N27:",count,"local front transfers PASS")
def n29():
    for q in (3,4,5,8,12,37,100):
        N=[int("12"+"9"*q+"34"),int("569"+"9"*(q-2)+"855"),
           int("1128"+"9"*(q-2)+"820"),int("1418"+"9"*(q-3)+"8031"),
           int("2727"+"9"*(q-3)+"6172"),int("5444"+"9"*(q-3)+"3444")]
        assert all(step(N[i])==N[i+1] for i in range(5))
        assert all(ds(n)!=ds(n)[::-1] for n in N)
    print("N29: 35 real integer edges PASS")
def n25():
    cnt=0
    for u,v,du,dv in ((45,47,5,7),(50,49,1,3),(60,62,13,2)):
        a=int("1789"+"0"*u+"3141"+"0"*v+"5926"+"0"*u+"5358")
        b=int("1789"+"0"*(u+du)+"3141"+"0"*(v+dv)+"5926"+"0"*(u+du)+"5358")
        for _ in range(20):
            x=ds(a);y=ds(b);na=step(a);nb=step(b)
            assert (x==x[::-1])==(y==y[::-1])
            assert len(ds(na))-len(x)==len(ds(nb))-len(y)
            a,b=na,nb;cnt+=1
    print("N25:",cnt,"integer splicing transitions PASS")
if __name__=="__main__":
    n19();n24();n27();n29();n25()
