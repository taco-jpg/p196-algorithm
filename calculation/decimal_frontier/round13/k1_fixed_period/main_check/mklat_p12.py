#!/usr/bin/env python3
import os
src=os.path.expanduser('~/p196_repo/calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt')
L=[l.split() for l in open(src) if l.strip()]
tp,nB,m,base=map(int,L[0]); clk=L[1]
assert len(L)==2+3*tp
W=L[2:2+tp]; B=L[2+2*tp:2+3*tp]
assert all(len(r)==m for r in W) and all(len(r)==nB for r in B)
with open('lat/p12m9.txt','w') as f:
    f.write(f'{base} {tp} {nB} {m}\n'+' '.join(clk)+'\n')
    for r in B: f.write(' '.join(r)+'\n')
    for r in W: f.write(' '.join(r)+'\n')
print('p12m9 written: base',base,'tp',tp,'nB',nB,'m',m,'clock',''.join(clk))
