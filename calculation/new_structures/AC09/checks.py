#!/usr/bin/env python3
"""AC09: independently compare physical Python bigint n+reverse(n) to folded pairword."""
import sys
sys.set_int_max_str_digits(0)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
US=((9,16,2),(16,2,9),(2,9,16))
def template(u,C,q,k):
    H=B+W*q+[5]+list(u)*k
    return H+list(C)+H[::-1]
def realize(P):
    d=[0]*len(P)
    for i in range(len(P)//2):
        h=min(9,P[i]);d[i]=P[i]-h;d[-i-1]=h
    if len(P)%2:d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]>0
    return int(''.join(map(str,d[::-1])))
def pair(n):
    s=list(map(int,str(n)))
    return [s[i]+s[-i-1] for i in range(len(s))][::-1]
def step(p):
    carry=0;d=[]
    for x in p:
        z=x+carry;d.append(z%10);carry=z//10
    if carry:d.append(carry)
    return [d[i]+d[-i-1] for i in range(len(d))],carry
def test():
    counter=0
    for u in US:
        for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
            for C in ([2]*7,[8]*8):
                p=template(u,C,q,k);n=realize(p);gamma=[]
                assert pair(n)==p
                for t in range(120):
                    s=str(n);n+=int(s[::-1]);gamma.append(len(str(n))-len(s))
                    p,c=step(p)
                    assert pair(n)==p and gamma[-1]==c,(u,C,q,k,t)
                    counter+=1
                assert ''.join(map(str,gamma))=='1000'*30
                print("PASS",u,"C length",len(C),"q",q,"k",k)
    assert counter==3600
    print("TOTAL_INDEPENDENT_INTEGER_TRANSITIONS",counter)
if __name__=='__main__':test()
