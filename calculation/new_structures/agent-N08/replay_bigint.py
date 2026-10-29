#!/usr/bin/env python3
"""Independent big-integer control: no imports from the transducer/checker."""
import sys

def accepts(t,p):
    if t==0:return p=="11211"
    phase=(t-1)%4
    if phase==0:
        k=(len(p)-4)//2
        return k>=1 and len(p)==2*k+4 and p=="2"+"1"*k+"00"+"1"*k+"2"
    if phase==1:
        k=(len(p)-5)//2
        return k>=1 and len(p)==2*k+5 and p=="10"+"1"*(k-1)+"202"+"1"*(k-1)+"01"
    if phase==2:
        k=(len(p)-5)//2
        return k>=1 and len(p)==2*k+5 and p=="2"+"1"*k+"020"+"1"*k+"2"
    k=(len(p)-6)//2
    return k>=1 and len(p)==2*k+6 and p=="10"+"1"*(k-1)+"2112"+"1"*(k-1)+"01"

def replay(steps):
    n=22; overflow=0
    for t in range(steps):
        digits=bin(n)[2:]
        assert digits!=digits[::-1],("PALINDROME",t)
        pair="".join(str(int(a)+int(b)) for a,b in zip(digits,digits[::-1]))
        assert accepts(t,pair),("PAIRWORD",t,len(pair),pair[:100])
        nn=n+int(digits[::-1],2)
        gam=int(nn.bit_length()>n.bit_length())
        if t>=1:assert gam==(1,0,1,0)[(t-1)%4]
        overflow+=gam;n=nn
    print("BASE2_BIGINT",steps,"PASS","final_bits",n.bit_length(),"overflow",overflow)

if __name__=="__main__":replay(int(sys.argv[1]) if len(sys.argv)>1 else 20000)
