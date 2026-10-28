import sys
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from lib7 import *
recs=parse_scc('/home/claude/research/w7_kink/data/p8_scc.txt')
ri=int(sys.argv[1]); n0=int(sys.argv[2]); steps=int(sys.argv[3])
L=Lattice(recs[ri])
h=(n0+1)//2
P=[L.cell(0,x) for x in range(h)]
P=P+P[:n0//2][::-1]
assert len(P)==n0 and P==P[::-1]
t=0
wall_hist=[]
for t in range(steps):
    P,gam=pairword_step(P)
    n=len(P); h=(n+1)//2
    lat=[L.cell(t+1,x) for x in range(h)]
    # first mismatch in lower half
    w=None
    for x in range(h):
        if P[x]!=lat[x]: w=x;break
    wall_hist.append((t+1,n,gam,w, None if w is None else h-w))
    if t<40 or (t+1)%8==0:
        print(t+1,'n',n,'gam',gam,'wall',w,'width',None if w is None else h-w)
