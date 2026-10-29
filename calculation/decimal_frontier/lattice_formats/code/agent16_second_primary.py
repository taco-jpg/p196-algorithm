#!/usr/bin/env python3
"""Complete 6-step second-column transfer from g=(101100)^k, b=4/5/6.
No caps; all possible c_t and starting coefficients, six rotations.
"""
from collections import Counter
from itertools import product

FIRST = {4:(4,1,3,4,1,2), 5:(6,2,4,5,1,3), 6:(7,2,5,6,1,3)}
FORCED = {4:(1,1,0,0), 5:(0,1,1,0), 6:(1,1,1,1)}
G=(1,0,1,1,0,0)

def transfer(base,rotation=0):
    b=base; xfirst=FIRST[b]; forced=FORCED[b]
    result=Counter();witness={}
    for a,d in product((0,1),repeat=2):
        H=(a,forced[0],forced[1],d,forced[2],forced[3]);L=tuple(x//b for x in xfirst)
        Y={0:(xfirst[0]+a)%b,2:(xfirst[2]+1)%b,3:(xfirst[3]+d)%b}
        h=H[rotation:]+H[:rotation];l=L[rotation:]+L[:rotation];g=G[rotation:]+G[:rotation]
        y={t:Y[(t+rotation)%6] for t in range(6) if g[t]}
        for start in range(2*b-1):
            for c in product((0,1),repeat=6):
                z=start;zs=[]
                for t in range(6):
                    if not 0<=z<=2*b-2 or (z+c[t])//b!=h[t]:break
                    zs.append(z)
                    z=(z+l[t])%b+(y[t] if g[t] else (z+c[t])%b)
                else:
                    if not 0<=z<=2*b-2:continue
                    key=(a,d,start,z)
                    result[key]+=1;witness[key]=(zs,c)
    return result,witness

if __name__=='__main__':
    for b in (4,5,6):
        table,_=transfer(b)
        print('b',b,'paths',sum(table.values()),'keys',len(table))
        for k,v in sorted(table.items()):print(' ',k,'mult',v)
        print('rotations: ',[(q,sum(transfer(b,q)[0].values())) for q in range(6)])
