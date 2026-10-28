import sys
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from lib7 import *
recs=parse_scc('/home/claude/research/w7_kink/data/p8_scc.txt')
for ri,rec in enumerate(recs):
    L=Lattice(rec)
    lam=[sum(L.Wt[t]) for t in range(L.p)]
    bs=[sum(L.Bt[t]) for t in range(L.p)]
    print('rec',ri,'m',L.m,'S',L.S,'Lambda_t',lam,'mod3',[x%3 for x in lam],'mod9',[x%9 for x in lam],'sumB',bs)
