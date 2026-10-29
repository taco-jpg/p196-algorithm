#!/usr/bin/env python3
"""Independent physical-decimal control: Python unbounded n += reverse(n)."""
import random,sys
sys.set_int_max_str_digits(0)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
U=[[9,4,14],[4,14,9],[14,9,4]]
J=[5]
def centre(idx,length):
    c=[0]*length
    for i in range(length//2):
        c[i]=c[-i-1]=idx%19
        idx//=19
    if length%2:
        c[length//2]=2*(idx%10)
        idx//=10
    assert idx==0
    return c
def tmpl(q,k,u,c):
    h=B+W*q+J+U[u]*k
    return h+c+h[::-1]
def realize(p):
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i]);lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo;d[-i-1]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]!=0
    return int(''.join(map(str,d[::-1])))
def replay(q,k,u,c):
    n=realize(tmpl(q,k,u,c))
    gamma=[]
    palindrome_count=0
    for t in range(120):
        s=str(n)
        palindrome_count+=(s==s[::-1])
        nxt=n+int(s[::-1])
        gamma.append(len(str(nxt))-len(s))
        n=nxt
    d=list(map(int,str(n)[::-1]))
    got=[a+b for a,b in zip(d,d[::-1])]
    tar=tmpl(q,k+5,u,c)
    first=next((i for i in range(min(len(got),len(tar))) if got[i]!=tar[i]),None)
    return got,tar,first,''.join(map(str,gamma)),palindrome_count
if __name__=="__main__":
    random.seed(20261029)
    controls=0
    for length in range(7,15):
        for u in range(3):
            total=19**(length//2)*(10 if length%2 else 1)
            for code in (0,total-1,random.randrange(total)):
                c=centre(code,length)
                for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
                    got,tar,first,g,pc=replay(q,k,u,c)
                    assert g=="1000"*30 and pc==0 and len(got)==len(tar)
                    assert got!=tar
                    if q==14 and k==100:
                        sf=400
                        mismatch=next((i for i in range(sf,len(got)-sf) if got[i]!=tar[i]),None)
                        assert mismatch is not None
                    controls+=1
        print("BIGINT_PASS",length,controls)
    print("PYTHON_BIGINT_PASS",controls)
