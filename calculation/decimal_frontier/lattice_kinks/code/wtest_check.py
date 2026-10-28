import sys, random, subprocess
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from lib7 import *
ri=int(sys.argv[1]); N=int(sys.argv[2])
recs=parse_scc('/home/claude/research/w7_kink/data/p8_scc.txt')
L=Lattice(recs[ri]); rng=random.Random(11+ri)
cases=[]; truth=[]
for it in range(N):
    t=rng.randrange(L.p)
    n=rng.randint(300,400)
    h=(n+1)//2
    w=rng.randint(1,12); M=12; K=w+M
    # lower half: lattice below h-w, random window (biased to include 9s and lattice-like cells)
    low=[L.cell(t,x) for x in range(h-w)]
    win=[]
    for i in range(w):
        r=rng.random()
        if r<0.2: win.append(9)
        elif r<0.5: win.append(L.cell(t,h-w+i))
        else: win.append(rng.randint(0,18))
    if n%2==1: win[-1]-= win[-1]%2
    half=low+win
    P=half+half[:n//2][::-1]
    assert len(P)==n and P==P[::-1]
    P2,gam=pairword_step(P)
    n2=len(P2); h2=(n2+1)//2
    assert gam==L.g[t], (gam, L.g[t])
    buf=half[h-K:h]
    cases.append(f"{t} {n} {w} {K} "+' '.join(map(str,buf)))
    # truth
    fz=K-w
    esc=False
    for i2 in range(2,fz):
        if P2[h2-K+i2]!=L.cell(t+1,h2-K+i2): esc=True
    newbuf=[P2[h2-K+i2] for i2 in range(K)]
    truth.append((esc,h2-h,newbuf))
out=subprocess.run(['./wtest','/home/claude/research/w7_kink/data/lat%d.txt'%ri],input='\n'.join(cases)+'\n',capture_output=True,text=True).stdout.strip().split('\n')
bad=0; nesc=0
for k,(line,(esc,dh,nb)) in enumerate(zip(out,truth)):
    v=list(map(int,line.split()))
    r,dhc=v[0],v[1]
    if bool(r)!=esc: bad+=1; print('FLAG mismatch',cases[k],r,esc); continue
    nesc+=esc
    if not esc:
        if dhc!=dh: bad+=1; print('dh mismatch'); continue
        if v[2+2:]!=nb[2:]: bad+=1; print('buf mismatch',cases[k],v[2:],nb)
print('rec',ri,'cases',N,'escapes',nesc,'bad',bad)
