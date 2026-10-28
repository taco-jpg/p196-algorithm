#!/usr/bin/env python3
"""Write lattice description file for the C++ tools (own format, own computation of steady carries).
format: p nB m b / gam[p] / W[t][m] x p / cup[t][m] x p / B[t][nB] x p
cup[t][j] = steady ascending carry INTO lattice column j (position nB+j) at time t."""
import sys
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from lib7 import *
def make(rec, out):
    L=Lattice(rec)
    p,nB,m=L.p,L.nB,L.m
    cup=[]
    for t in range(p):
        word=L.Bt[t]+L.Wt[t]*40
        c=0; car=[]
        for x,d in enumerate(word):
            car.append(c); c=1 if d+c>=10 else 0
        tab=[car[nB+m*30+j] for j in range(m)]
        for x in range(nB+m*20,len(word)):
            assert car[x]==tab[(x-nB)%m], 'carry not steady'
        cup.append(tab)
    with open(out,'w') as f:
        f.write(f"{p} {nB} {m} 10\n"+' '.join(map(str,L.g))+'\n')
        for t in range(p): f.write(' '.join(map(str,L.Wt[t]))+'\n')
        for t in range(p): f.write(' '.join(map(str,cup[t]))+'\n')
        for t in range(p): f.write(' '.join(map(str,L.Bt[t]))+'\n')
if __name__=='__main__':
    recs=parse_scc(sys.argv[1])
    for i,r in enumerate(recs):
        make(r, f'/home/claude/research/w7_kink/data/lat{i}.txt')
        print('wrote lat',i,'p',r['p'],'m',len(r['cyc']))
