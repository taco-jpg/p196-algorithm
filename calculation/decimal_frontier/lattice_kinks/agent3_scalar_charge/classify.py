#!/usr/bin/env python3
"""PAPER PROOF arithmetic witness for all-modulus scalar rec2 carry corrections."""
import math
from pathlib import Path
import sys
def classify(path):
    x=list(map(int,Path(path).read_text().split()))
    p,nb,m,b=x[:4]
    assert (p,nb,m,b)==(8,11,48,10)
    assert x[4:12]==[1,0,1,0,1,0,1,0]
    z=x[12:]
    assert len(z)==8*(2*m+nb)
    W=[z[t*m:(t+1)*m] for t in range(8)]
    D=[]
    for row in W:
        solutions=[]
        for end in [0,1]:
            d=[0]*m;d[-1]=end
            for j in range(m-1,0,-1):
                d[j-1]=int(row[j]+d[j]>=10)
            if end==int(row[0]+d[0]>=10):solutions.append(d)
        assert len(solutions)==1
        D.append(solutions[0])
    Q=[sum(v*10**j for j,v in enumerate(row)) for row in W]
    C=[sum(v*10**j for j,v in enumerate(row)) for row in D]
    minor=lambda i,j:Q[i]*C[j]-Q[j]*C[i]
    assert math.gcd(*Q)==99
    assert math.gcd(C[0],C[2])==1
    assert math.gcd(minor(0,1),minor(1,2))==99
    for mod in (2,3,9,11,37,99,101,9999,10000):
        solutions=[a for a in range(mod) if all((q+a*d)%mod==0 for q,d in zip(Q,C))]
        expected=[0] if 99%mod==0 else []
        assert solutions==expected,(mod,solutions)
    print("PAPER PROOF arithmetic: gcd(Q)=99; gcd(D0,D2)=1; gcd(Delta01,Delta12)=99")
    print("Control moduli 2,3,9,11,37,99,101,9999,10000: PASS")
if __name__=="__main__":
    classify(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name("lat2.txt")))
