#!/usr/bin/env python3
"""Sound coefficient-mask proof for all J words of each length 0..50.
Every J coefficient 0..18 and every palindromic C 7..14 is overapproximated.
"""
import sys
from oracle import B,W,U
from abstract import normalize,pair,ALL19,MID,certify_ports
def test(u,clen,jlen):
    h=B+W*14+[0]*jlen+U[u]*100
    p=h+[0]*clen+h[::-1]
    masks=[1<<x for x in p]
    first=len(B)+len(W)*14
    for i in range(first,first+jlen):
        masks[i]=masks[-1-i]=ALL19
    for i in range(clen):
        masks[len(h)+i]=MID if clen%2 and i==clen//2 else ALL19
    cut=first+jlen+119
    ports=[];gamma=[]
    for t in range(120):
        carry=1;inlet=None;digits=[]
        for i,coef in enumerate(masks):
            if i==cut+t:inlet=carry
            digit,carry=normalize(coef,carry)
            digits.append(digit)
        assert inlet in (1,2),(u,clen,jlen,t,"port",inlet)
        assert carry in (1,2),(u,clen,jlen,t,"gamma",carry)
        ports.append(inlet.bit_length()-1)
        g=carry.bit_length()-1
        gamma.append(g)
        if g:digits.append(1<<1)
        masks=[pair(digits[i],digits[-1-i]) for i in range(len(digits))]
    assert gamma==[1,0,0,0]*30
    base=certify_ports(u,clen)["ports"]
    assert ports==[int(x) for x in base],(u,clen,jlen,"ports differ")
    return True
if __name__=="__main__":
    stop=int(sys.argv[1]) if len(sys.argv)>1 else 50
    lo=int(sys.argv[2]) if len(sys.argv)>2 else 7
    hi=int(sys.argv[3]) if len(sys.argv)>3 else 14
    for l in range(lo,hi+1):
        for u in range(3):
            for j in range(stop+1):test(u,l,j)
            print("JPORT_CERT",u,l,"J_length0..",stop,flush=True)
    print("JPORT_CERT_PASS",3*(hi-lo+1)*(stop+1))
