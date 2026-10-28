#!/usr/bin/env python3
"""Counter graph for the lowest B coefficient x in [1,2b-2]:  non-overflow (x+c<=b-1): x'=2x+c ; overflow (x+c>=b): x'=(x mod b)+1, c in {0,1}.
Karp max-cycle-mean of P/G, plus longest-path potential psi with weights +1 (non-ov), -(L-1) (ov), L = bit_length(b)."""
import sys
from fractions import Fraction
def graph(b):
    E=[]
    for x in range(1,2*b-1):
        for c in (0,1):
            if x+c<=b-1: E.append((x,2*x+c,0))
            else: E.append((x,(x%b)+1,1))
    return E
def maxratio(b):
    # binary search on lambda: exists cycle with P - lam*G > 0 ?  use Bellman-Ford positive-cycle detection with Fractions
    E=graph(b); nodes=list(range(1,2*b-1))
    def has_pos(lam):
        d={x:Fraction(0) for x in nodes}
        for it in range(len(nodes)+1):
            ch=False
            for (u,v,g) in E:
                w=Fraction(1)-lam*g
                if d[u]+w>d[v]: d[v]=d[u]+w; ch=True
            if not ch: return False
        return True
    # candidates are rationals P/G with G<=len(nodes): do search via Dinkelbach
    lam=Fraction(1)
    while True:
        # find cycle maximizing P - lam G via longest-path BF with predecessor tracking
        d={x:Fraction(0) for x in nodes}; pred={}
        last=None
        for it in range(len(nodes)+1):
            last=None
            for (u,v,g) in E:
                w=Fraction(1)-lam*g
                if d[u]+w>d[v]: d[v]=d[u]+w; pred[v]=(u,g); last=v
            if last is None: break
        if last is None: return lam
        # extract cycle
        x=last
        for _ in range(len(nodes)): x=pred[x][0]
        cyc=[]; y=x; P=0; G=0
        while True:
            u,g=pred[y]; P+=1; G+=g; y=u
            if y==x: break
        lam=Fraction(P,G)
if __name__=="__main__":
    lo,hi=int(sys.argv[1]),int(sys.argv[2])
    bad=[]
    for b in range(lo,hi+1):
        r=maxratio(b); L=b.bit_length()
        print(b,r,"bitlength",L,"OK" if r==L else "MISMATCH")
        if r!=L: bad.append(b)
    print("mismatches:",bad)
