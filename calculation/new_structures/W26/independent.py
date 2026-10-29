#!/usr/bin/env python3
"""Independent exact replay: pairword recurrence vs schoolbook digits vs Python bigint."""
import sys
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(1000000)

B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
U=[9,4,14]

def rev(a):
    return list(reversed(a))

def template(q,k,J,C):
    h=B+W*q+J+U*k
    return h+C+rev(h)

def realize(p):
    assert p==rev(p)
    d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i])
        lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo
        d[-1-i]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]>0
    return d

def pairword_from_digits(d):
    return [d[i]+d[-1-i] for i in range(len(d))]

def pairword_step(p):
    d=[]
    c=0
    for x in p:
        z=x+c
        d.append(z%10)
        c=z//10
    if c:
        d.append(c)
    return [d[i]+d[-1-i] for i in range(len(d))],c

def schoolbook_step(d):
    out=[]
    c=0
    carry_sum=0
    for i in range(len(d)):
        z=d[i]+d[-1-i]+c
        c=z//10
        carry_sum+=c
        out.append(z%10)
    if c:
        out.append(c)
    return out,carry_sum,len(out)-len(d)

def value(d):
    n=0
    for x in reversed(d):
        n=10*n+x
    return n

def centre(length,pattern):
    r=(length-1)//2
    left=[(pattern+3*i+1)%19 for i in range(r)]
    mid=(2*(pattern+1))%19
    if mid%2:
        mid-=1
    return left+[mid]+left[::-1]

def check(q,k,J,C):
    p=template(q,k,J,C)
    d=realize(p)
    n=value(d)
    assert pairword_from_digits(d)==p
    gamma=[]
    for t in range(120):
        p2,g=pairword_step(p)
        d2,carry_sum,gg=schoolbook_step(d)
        assert g==gg,(q,k,J,C,t,"overflow disagreement")
        assert p2==pairword_from_digits(d2),(q,k,J,C,t,"pair-vs-school")
        reverse_n=int(str(n)[::-1])
        assert value(d2)==n+reverse_n,(q,k,J,C,t,"integer-vs-school")
        n+=reverse_n
        d=d2
        p=p2
        gamma.append(g)
    assert gamma==[1,0,0,0]*30,(q,k,J,C,"wrong overflow clock")
    target=B+W*q
    mismatch=None if p[:len(target)]==target else next(
        (i for i,(a,b) in enumerate(zip(p,target)) if a!=b),
        min(len(p),len(target)))
    return mismatch,len(d)

def main():
    widths=[(14,100),(20,100),(40,160),(80,320),(160,640)]
    junctions=[[0,0,0],[18,18,18]]
    for q,k in widths:
        for length in (3,5,7,9,11,13):
            C=centre(length,pattern=length)
            for J in junctions:
                mismatch,digits=check(q,k,J,C)
                assert mismatch is not None
                print(f"q={q} k={k} |J|={len(J)} J={J} |C|={length} mismatch={mismatch} digits={digits}")
    print("PASS: 60 genuine integer/digit-array/pairword 120-step replays; all clocks are (1000)^30.")

if __name__=="__main__":
    main()