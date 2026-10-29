#!/usr/bin/env python3
"""Independent Python big integers and inverse decoder for two-step eraser."""
import sys
sys.set_int_max_str_digits(0)
from reverse_fibre import inverse_pairword
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
def coeffs(q,centre):
    half=B+W*q
    assert half[-1]==13
    half[-1]=centre
    return half+half[::-1]
def source(p):
    half=p[:len(p)//2]
    low=[min(x,9) for x in half]
    high=[x-y for x,y in zip(half,low)]
    return int(''.join(map(str,high))+''.join(map(str,low[::-1])))
def step(n):return n+int(str(n)[::-1])
def pairword(n):
    s=str(n)
    return [int(s[-1-i])+int(s[i]) for i in range(len(s))]
def main():
    for q in list(range(101))+[300,301]:
        p=coeffs(q,13);r=coeffs(q,4);assert p!=r
        a=source(p);b=source(r)
        a1,b1=step(a),step(b)
        assert a1!=b1
        assert pairword(a1)==pairword(b1)
        assert step(a1)==step(b1)
        assert inverse_pairword(str(a1),len(str(a)))==p
        assert inverse_pairword(str(b1),len(str(b)))==r
        L=39+20*q
        y=list(map(int,str(a1)[::-1]))
        z=list(map(int,str(b1)[::-1]))
        assert [y[L-1],y[L],y[L+1]]==[3,4,8]
        assert [z[L-1],z[L],z[L+1]]==[4,4,7]
        assert not (str(a)==str(a)[::-1] or str(b)==str(b)[::-1])
        assert step(step(source(coeffs(q,5))))!=step(a1)
    print('W07_TWO_STEP_BIGINT_PASS q=0..100,300,301, exact first/second successors, reverse decoder and centre-5 negative control')
if __name__=='__main__':main()
