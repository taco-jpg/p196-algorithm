#!/usr/bin/env python3
"""N28 base-b carry-gauge theorem: independent integer and coefficient controls."""
import itertools,json,random

def value(a,b):
    return sum(v*b**i for i,v in enumerate(a))

def digits(n,b):
    v=[]
    while n:v.append(n%b);n//=b
    return v or [0]

def add_reverse(a,b):
    c=0;out=[]
    for i in range(len(a)):
        s=a[i]+a[-1-i]+c;out.append(s%b);c=s//b
    if c:out.append(c)
    return out

def normalise(p,b):
    c=0;d=[]
    for x in p:
        s=x+c;d.append(s%b);c=s//b
    if c:d.append(c)
    return d

def pairs(d):return [d[i]+d[-1-i] for i in range(len(d))]

def make_seed(p,b):
    assert p==p[::-1] and len(p)%2==0
    n=len(p);d=[0]*n
    for i in range(n//2):
        d[i]=max(0,p[i]-(b-1))
        d[-i-1]=p[i]-d[i]
        assert 0<=d[i]<b and 0<=d[-i-1]<b
    assert d[-1] and pairs(d)==p
    return d

def predicted(x,z,b):
    n=len(x)
    if z[0]:
        return [x[0]]+[x[i-1]+x[i] for i in range(1,n)]+[x[0]]
    return [2*x[i]+(z[i-1] if i else 0)+(z[i+1] if i+1<n else 0)-2*z[i] for i in range(n)]

def check(b,x,z):
    n=len(x)
    assert n%2==0 and n>=2 and x==x[::-1] and z==z[::-1]
    assert all(1<=v<=b-2 for v in x) and all(v in (0,1) for v in z)
    p=[u+(b-1)*v for u,v in zip(x,z)]
    seed=make_seed(p,b)
    first=add_reverse(seed,b)
    expectation=predicted(x,z,b)
    assert first==normalise(p,b)
    assert pairs(first)==expectation
    assert len(first)==n+z[0]
    second=add_reverse(first,b)
    assert value(second,b)==value(expectation,b)
    # Independent big-integer oracle with its own digit extraction.
    num=value(seed,b)
    assert digits(num,b)==seed
    first_int=num+value(seed[::-1],b)
    second_int=first_int+value(digits(first_int,b)[::-1],b)
    assert first_int==value(first,b) and second_int==value(second,b)
    if z[0]:
        formula=x[0]*(1+b**n)+sum((x[i-1]+x[i])*b**i for i in range(1,n))
        assert second_int==formula
    if z[0] and len(set(x))==1:
        assert second_int==x[0]*(b+1)*(b**n-1)//(b-1)

def run():
    count=0
    for b in range(3,16):
        for n in (2,4,6):
            m=n//2
            for half in itertools.product(range(1,b-1),repeat=m):
                if m==3 and b>7:break
                x=list(half)+list(half[::-1])
                for bits in itertools.product((0,1),repeat=m):
                    z=list(bits)+list(bits[::-1])
                    check(b,x,z);count+=1
    r=random.Random(280474)
    for _ in range(20000):
        b=r.randrange(3,78);m=r.randrange(1,65)
        xh=[r.randrange(1,b-1) for _ in range(m)]
        zh=[r.randrange(2) for _ in range(m)]
        check(b,xh+xh[::-1],zh+zh[::-1]);count+=1
    for _ in range(200):
        m=512;bits=[r.randrange(2) for _ in range(m)];bits[0]=1
        check(10,[8]*(2*m),bits+bits[::-1]);count+=1
    assert predicted([8]*4,[1,0,0,1],10)==[8,16,16,16,8]
    assert predicted([8]*4,[0,1,1,0],10)!=[8,16,16,16,8]
    for seed,one in ((9448,17897),(9988,18887)):
        d=digits(seed,10)
        a=add_reverse(d,10);v=add_reverse(a,10)
        assert value(a,10)==one and value(v,10)==97768
    print(json.dumps({"label":"COMPUTED checker of PAPER PROOF theorem",
      "checked_cases":count,"independent_big_integer_cases":count,
      "bases":"3..77","long_decimal_masks":200,
      "decimal_collision":{"9448":[17897,97768],"9988":[18887,97768]},
      "even_length_fixed_x_mask_count":"2^(n/2-1)"},indent=2))
if __name__=="__main__":run()
