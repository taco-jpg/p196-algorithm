import sys
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from lib7 import *
recs=parse_scc('/home/claude/research/w7_kink/data/p8_scc.txt')
A=Lattice(recs[0]); B=Lattice(recs[1])
m=20; p=8
def dist(X,Y,s,tau,mirror):
    d=0
    for t in range(p):
        for j in range(m):
            jj=(s-j)%m if mirror else (s+j)%m
            if X.Wt[t][j]!=Y.Wt[(t+tau)%p][jj]: d+=1
    return d
best=[]
for mirror in (0,1):
    for s in range(m):
        for tau in range(p):
            best.append((dist(A,B,s,tau,mirror),mirror,s,tau))
best.sort(); print('rec0 vs rec1 best (dist,mirror,s,tau):',best[:6],' of',m*p,'cells')
# self relations
for name,X in (('rec0',A),('rec1',B)):
    b2=[]
    for mirror in (0,1):
        for s in range(m):
            for tau in range(p):
                if mirror==0 and s==0 and tau==0: continue
                b2.append((dist(X,X,s,tau,mirror),mirror,s,tau))
    b2.sort(); print(name,'self best:',b2[:6])
