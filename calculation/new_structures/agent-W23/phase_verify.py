#!/usr/bin/env python3
"""Pure Python physical base-10 checks of all 14 W23 clocked erasers, q=8 and q=100."""
import sys
sys.set_int_max_str_digits(0)
B=(17,5,0,2,1,9,15,18,14,9,3)
W=(4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3)
CASES={
0:[(20,(13,9),(8,5),3),(20,(13,9),(8,14),3),(20,(13,9),(17,5),3),(20,(13,9),(17,14),3),(23,(3,13),(7,9),3)],
3:[(44,(12,9),(14,16),4),(47,(7,12),(5,14),4)],
4:[(44,(5,9),(1,4),3),(44,(5,9),(1,13),3),(44,(5,9),(10,4),3),(44,(5,9),(10,13),3),(47,(15,5),(11,9),3)],
7:[(20,(6,9),(4,2),4),(23,(11,6),(13,4),4)]}
def initial(q):
    h=list(B)+list(W)*q+[10,14,1,10]
    d=[0]*(2*len(h)-1)
    for i,p in enumerate(h[:-1]):
        d[i]=max(p-9,0);d[-i-1]=min(p,9)
    d[len(h)-1]=5
    return int(''.join(map(str,d[::-1])))
def reverse_add(n):
    return n+int(str(n)[::-1])
def pairword(n):
    s=str(n)
    return [int(s[i])+int(s[-1-i]) for i in range(len(s))]
def realize(p):
    n=len(p);d=[0]*n
    assert p==p[::-1]
    for i in range(n//2):
        d[i]=max(0,p[i]-9);d[-1-i]=min(9,p[i])
    if n%2:
        assert p[n//2]%2==0
        d[n//2]=p[n//2]//2
    assert d[-1]>0
    return int(''.join(map(str,d[::-1])))
def test(q):
    root=initial(q);seen=0
    for phase in range(8):
        for off,before,after,T in CASES.get(phase,()):
            src=pairword(root)
            cut=11+48*2+off
            assert tuple(src[cut:cut+2])==before,(q,phase,off,src[cut:cut+2])
            src[cut:cut+2]=after
            src[-cut-2:-cut]=after[::-1]
            a,b=realize(src),root
            assert a!=b
            for t in range(T):
                assert a!=b and str(a)!=str(a)[::-1] and str(b)!=str(b)[::-1]
                a,b=reverse_add(a),reverse_add(b)
            assert a!=b and pairword(a)==pairword(b),(q,phase,off)
            assert reverse_add(a)==reverse_add(b),(q,phase,off)
            seen+=1
        root=reverse_add(root)
    assert seen==14
    print(f"PASS q={q}: 14 physical phase-clocked erasers with exact pairword reset")
if __name__=='__main__':
    test(8);test(100)
