#!/usr/bin/env python3
"""Independent arbitrary-precision integer controls for known nondecimal cycles."""
import sys
sys.set_int_max_str_digits(0)
B9=[8,9,10,13,14,12,3,14,10,0,11,7,10,9,7,8,8,14,15,2,9,7,0,5,8,3,8,11,8,6,8,7,5,14,11,3,9,3,8,14,7,12,8,2,0,12,1,5,13,8,1,16,15,9,1,7,6,2,1,15,15]
W9=[1,1,15,15]
B50=[48,52,43,61,26,44,60,28,40,67,63,70,57,33,31,36,26,45,58,32,33,32,34,30,37,73,52,42,62,73,51,44,59,30,37,24]
C50=[62,15,22,32,32,22,15,62]
def val(base,ds):
    n=0
    for x in reversed(ds): n=n*base+x
    return n
def digits(base,n):
    out=[]
    while n: n,x=divmod(n,base); out.append(x)
    return out or [0]
def split_pairword(base,pairs):
    assert pairs==pairs[::-1]
    n=len(pairs); out=[0]*n
    for i in range(n//2):
        x=pairs[i]; assert 0<=x<=2*base-2
        hi=min(x,base-1); lo=x-hi
        out[i]=lo; out[n-i-1]=hi
    if n%2:
        assert pairs[n//2]%2==0
        out[n//2]=pairs[n//2]//2
    assert out[-1]>0
    return val(base,out)
def pairword(base,n):
    d=digits(base,n)
    return [d[i]+d[-1-i] for i in range(len(d))]
def reverse_add(base,n):
    d=digits(base,n)
    return n+val(base,d[::-1])
def check(base,p0,p1,steps,label):
    n=val(base,p0)
    for t in range(steps):
        d=digits(base,n); assert d!=d[::-1],(label,"palindrome",t)
        n=reverse_add(base,n)
    assert n==val(base,p1),(label,"integer return mismatch")
    s=split_pairword(base,p0)
    for t in range(steps):
        d=digits(base,s); assert d!=d[::-1],(label,"split palindrome",t)
        s=reverse_add(base,s)
    assert pairword(base,s)==p1,(label,"pairword return mismatch")
    print("PASS",label,"steps=",steps,"source_digits=",len(digits(base,val(base,p0))),"target_digits=",len(digits(base,n)))
def main():
    for m in (20,40,80,160):
        l=4*m+2
        p0=B9+[W9[i%4] for i in range(l)]+B9[::-1]
        p1=B9+[W9[i%4] for i in range(l+4)]+B9[::-1]
        check(9,p0,p1,10,f"Lean-base9-l={l}")
        p0=B50+[49]*m+C50+[49]*m+B50[::-1]
        p1=B50+[49]*(m+1)+C50+[49]*(m+1)+B50[::-1]
        check(50,p0,p1,4,f"computed-base50-m={m}")
if __name__=="__main__": main()
