"""Independent physical decimal controls, no reuse of the C++ census engine."""
import sys
sys.set_int_max_str_digits(0)
from probe import U,C1,C2,template,succ
def digits(n):return [int(x) for x in str(n)[::-1]]
def pair(d):return [d[i]+d[-1-i] for i in range(len(d))]
def realize(p):
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=max(0,p[i]-9)
        d[-1-i]=p[i]-d[i]
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]>0 and pair(d)==p
    return int(''.join(map(str,d[::-1])))
def verify(j,u,c,q,k):
    p=template(j,u,c,q,k);n=realize(p);g=[]
    for t in range(120):
        old=digits(n)
        assert pair(old)==p
        n2=n+int(str(n)[::-1])
        expected,overflow=succ(p)
        manual=[];carry=0
        for z in p:
            z+=carry;manual.append(z%10);carry=z//10
        if carry:manual.append(carry)
        assert digits(n2)==manual
        assert len(digits(n2))-len(old)==overflow
        assert pair(digits(n2))==expected
        n=n2;p=expected;g.append(overflow)
    target=template(j,u,c,q,k+5)
    i=next((i for i,(x,y) in enumerate(zip(p,target)) if x!=y),-1)
    assert len(p)==len(target) and g==[0,1,0,0]*30
    return i
if __name__=='__main__':
    for q,k in ((14,100),(20,80),(40,160),(80,320),(160,640)):
        for j in ([0,0,0],[18,18,18],[0,1,2,3],[18,17,16,15]):
            for u in (U[0],U[14],U[29]):
                for c in (C1,C2):
                    print(q,k,j,u,c,'mismatch',verify(j,u,c,q,k))
    print('INDEPENDENT_CHECKS_PASSED')
