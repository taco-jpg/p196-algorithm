import sys, subprocess
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from lib7 import *
recs=parse_scc('/home/claude/research/w7_kink/data/p8_scc.txt')
L=Lattice(recs[0])
n=400; h=200; w=1; K=13
P=[L.cell(0,x) for x in range(h)]; P=P+P[::-1]
t=0
buf=P[h-K:h]
print('lattice window cell',buf[-1])
cases=[]
for t in range(0,6):
    # full evolution state at time t, buffer
    n=len(P); h=(n+1)//2
    buf=P[h-K:h]
    out=subprocess.run(['./wtest','/home/claude/research/w7_kink/data/lat0.txt'],input=f"{t} {n} {w} {K} "+' '.join(map(str,buf))+'\n',capture_output=True,text=True).stdout.strip()
    P2,g=pairword_step(P)
    h2=(len(P2)+1)//2
    nb=[P2[h2-K+i] for i in range(K)]
    lat=[L.cell(t+1,h2-K+i) for i in range(K)]
    print('t',t,'n',n,'cpp:',out)
    print('   truth newbuf',nb)
    print('   lattice     ',lat)
    P=P2
