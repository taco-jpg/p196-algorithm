import sys, random
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from lib7 import *
recs=parse_scc('/home/claude/research/w7_kink/data/p8_scc.txt')
ri=int(sys.argv[1]); N=int(sys.argv[2]); steps=int(sys.argv[3])
L=Lattice(recs[ri]); rng=random.Random(5)
up=0; tot=0; examples=[]
for it in range(N):
    t0=rng.randrange(L.p); n=rng.randint(200,260); h=(n+1)//2
    w=rng.randint(1,25)
    mode=rng.random()
    low=[L.cell(t0,x) for x in range(h-w)]
    win=[]
    for i in range(w):
        r=rng.random()
        if mode<0.3 and r<0.5: win.append(L.cell(t0,h-w+i))   # partially lattice-like
        elif mode<0.5 and r<0.2: win.append(9)
        else: win.append(rng.randint(0,18))
    if n%2==1: win[-1]-=win[-1]%2
    half=low+win; P=half+half[:n//2][::-1]
    t=t0; wall=None; hist=[]
    for s in range(steps):
        P,g=pairword_step(P); t+=1
        nn=len(P); hh=(nn+1)//2
        wl=None
        for x in range(hh):
            if P[x]!=L.cell(t,x): wl=x;break
        hist.append(wl)
    # wall must be defined
    for a,bq in zip(hist,hist[1:]):
        if a is None or bq is None: continue
        tot+=1
        if bq>a: up+=1
        if bq>a and len(examples)<5: examples.append((it,hist))
print('rec',ri,'transitions',tot,'wall-moved-up events',up)
for e in examples[:3]: print(e)
