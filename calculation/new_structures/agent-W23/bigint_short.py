#!/usr/bin/env python3
"""Independent physical Python-bigint verification of five p8/m48 erasers."""
import sys
sys.set_int_max_str_digits(0)
B=(17,5,0,2,1,9,15,18,14,9,3)
W=(4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3)
CHANGES=((20,8,5),(20,8,14),(20,17,5),(20,17,14),(23,7,9))
def seed(q,mask=0,kind=0):
    half=list(B)+list(W)*q+[10,14,1,10]
    for j in range(5):
        if mask>>j & 1:
            cut=11+48*(2+6*j)+CHANGES[kind][0]
            expect=(3,13) if kind==4 else (13,9)
            assert tuple(half[cut:cut+2])==expect
            half[cut:cut+2]=CHANGES[kind][1:]
    d=[0]*(2*len(half)-1)
    for i,p in enumerate(half[:-1]):
        d[i]=max(p-9,0);d[-1-i]=min(p,9)
    d[len(half)-1]=5
    return int(''.join(map(str,d[::-1])))
def ra(n):
    s=str(n);return n+int(s[::-1])
def pairs(n):
    s=str(n);return tuple(int(s[i])+int(s[-1-i]) for i in range(len(s)))
def main():
    for kind in range(5):
        a,b=seed(8),seed(8,1,kind)
        for t in range(3):
            assert a!=b and str(a)!=str(a)[::-1] and str(b)!=str(b)[::-1]
            a,b=ra(a),ra(b)
        assert a!=b and pairs(a)==pairs(b),kind
        assert ra(a)==ra(b),kind
    numbers=[seed(40,m) for m in range(32)];seen=[]
    for t in range(5):
        ss=[str(n) for n in numbers]
        seen.append((t,len(ss[0]),len(set(numbers)),sum(s==s[::-1] for s in ss)))
        if t<4:numbers=list(map(ra,numbers))
    assert seen==[(0,3869,32,0),(1,3870,32,0),(2,3870,32,0),(3,3871,32,0),(4,3871,1,0)]
    print('PASS all five three-step erasers and 32 physical variants; four-step coalescence')
    print(seen)
if __name__=='__main__':main()
