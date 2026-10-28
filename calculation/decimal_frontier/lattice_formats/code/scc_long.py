import sys, time
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
from scc_to_tmpl import *
recs=parse(sys.argv[1]); ri=int(sys.argv[2]); steps=int(sys.argv[3])
rec=recs[ri]
T=templates(rec,core=())[0]
cur=T; seen={}
t0=time.time()
for t in range(steps):
    key=cur
    if key in seen:
        print('CYCLE: template at step',t,'equals step',seen[key]); break
    seen[key]=t
    cur,gm,info=step(cur)
    if t%rec['p']==rec['p']-1:
        print(t+1,'|B|',len(cur.Hs[0][1]) if cur.Hs[0][0]=='L' else 0,'core',len(cur.core),'lit',cur.lit_size(),'items',[(it[0],len(it[1])) for it in cur.Hs],flush=True)
    if time.time()-t0>15: print('time cut'); break
