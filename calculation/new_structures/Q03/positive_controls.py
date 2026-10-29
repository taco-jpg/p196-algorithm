#!/usr/bin/env python3
"""Independent schoolbook-integer controls for known base9/base50 cycles."""
B9=[8,9,10,13,14,12,3,14,10,0,11,7,10,9,7,8,8,14,15,2,9,7,0,5,8,3,8,11,8,6,8,7,5,14,11,3,9,3,8,14,7,12,8,2,0,12,1,5,13,8,1,16,15,9,1,7,6,2,1,15,15]
B50=[48,52,43,61,26,44,60,28,40,67,63,70,57,33,31,36,26,45,58,32,33,32,34,30,37,73,52,42,62,73,51,44,59,30,37,24]
C50=[62,15,22,32,32,22,15,62]

def val(d,b):
    n=0
    for z in reversed(d):n=n*b+z
    return n

def digits(n,b):
    d=[]
    while n:n,r=divmod(n,b);d.append(r)
    return d or [0]

def canonical(p,b):
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=max(0,p[i]-(b-1))
        d[-1-i]=min(b-1,p[i])
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]!=0
    return val(d,b)

def replay(b,p,m):
    n=canonical(p,b)
    assert len(digits(n,b))==len(p)
    at=[]
    for t in range(21):
        d=digits(n,b)
        assert d!=d[::-1],(b,m,t)
        at.append(len(d))
        n+=val(d[::-1],b)
    assert at[20]-at[0] == (8 if b==9 else 10),(b,m,at)
    return at[0],at[20]

if __name__=='__main__':
    for m in (20,40,80,160):
        h=B9+[1,1,15,15]*m+[1,1]
        print('base9',m,replay(9,h+h[::-1],m))
        p=B50+[49]*m+C50+[49]*m+B50[::-1]
        print('base50',m,replay(50,p,m))
    print('PASS independent base9 and base50 positive controls')
