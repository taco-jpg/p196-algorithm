#!/usr/bin/env python3
"""Independent CPython-int short control for N21 20k mixed-phase packet train.
Tests its low-size specialization without reading or importing the C++ engine.
"""
import sys
sys.set_int_max_str_digits(1000000)
B=(2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11)
W=(1,10,8,5,9,16,0,9,11)
K=(6,1,0,1,11,14,10,6,11,16,1)
N=10000
PREFIX=(0,0,0,1,1,1,1,2,2,2,2,3)
def seed(at):
    half=list(B)+[W[(i-len(B))%9] for i in range(len(B),N//2)]
    for anchor in at:
        half[anchor:anchor+len(K)]=K
    pair=half+half[::-1]
    digits=[0]*N
    for i in range(N//2):
        x=pair[i]
        lo=max(1,x-9) if i==0 else min(x,9)
        hi=x-lo
        if i==0 and hi==0:lo-=1;hi+=1
        assert 0<=lo<=9 and 0<=hi<=9
        digits[i],digits[N-1-i]=lo,hi
    assert digits[-1]>0
    return int(''.join(map(str,digits[::-1])))
def pairword(v):
    s=str(v)
    return [ord(s[i])+ord(s[-1-i])-96 for i in range(len(s))]
def run():
    ns=[seed(()),seed((1000,)),seed((3500,)),seed((1000,3500))]
    for t in range(101):
        s=[str(n) for n in ns]
        assert all(len(x)==N+3*(t//12)+PREFIX[t%12] for x in s),t
        assert all(x!=x[::-1] for x in s),t
        p=[pairword(n) for n in ns]
        assert all(p[0][i]+p[3][i]==p[1][i]+p[2][i] for i in range(len(p[0]))),t
        if t<100:ns=[n+int(str(n)[::-1]) for n in ns]
    print('CPYTHON_INT_CONTROL_PASS four seeds, 100 transitions, full-pairword additivity, nonpalindromes, decimal growth schedule')
if __name__=='__main__':run()
