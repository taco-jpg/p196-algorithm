import sys
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from lib7 import *
recs=parse_scc('/home/claude/research/w7_kink/data/p8_scc.txt')
ri=int(sys.argv[1]); n0=int(sys.argv[2]); steps=int(sys.argv[3])
L=Lattice(recs[ri])
h=(n0+1)//2
P=[L.cell(0,x) for x in range(h)]
P=P+P[:n0//2][::-1]
for t in range(steps):
    P,gam=pairword_step(P)
n=len(P); h=(n+1)//2
lat=[L.cell(steps,x) for x in range(h)]
w=min(x for x in range(h) if P[x]!=lat[x])
print('n',n,'h',h,'wall',w,'core cells (lower half):',h-w)
print(' '.join(f'{v:2d}' for v in P[w-4:h]))
print(' '.join(f'{v:2d}' for v in lat[w-4:h]))
