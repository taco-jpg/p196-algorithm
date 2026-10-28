import sys, time
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
from scc_to_tmpl import *
recs=parse('../out/p8_scc.txt')
ri=int(sys.argv[1]); r=int(sys.argv[2]); C=tuple(int(x) for x in sys.argv[3].split(',')) if sys.argv[3] else (); periods=int(sys.argv[4])
rec=recs[ri]; p=rec['p']
base=templates(rec,core=())[0]
W=base.Hs[1][1]
core=tuple(W[:r])+C+tuple(W[:r][::-1])
T=Template(10,[('L',base.Hs[0][1]),('B',W,0)],core)
print(fmt(T)[:200])
cur=T; seen={}; gapoff=0; offs=[]
for t in range(p*periods):
    if cur in seen:
        print('CYCLE at step',t,'= step',seen[cur]); break
    seen[cur]=(t,gapoff)
    nxt,gm,info=step(cur)
    # gm: newpid -> (oldpid,mult,off)
    gapoff+=sum(v[2] for v in gm.values())
    if not info['differs']: print('PALINDROME at step',t); break
    cur=nxt
    if (t+1)%p==0:
        print((t+1)//p,'core',len(cur.core),'|B|',len(cur.Hs[0][1]),'gapoff',gapoff,'mult',[v[1] for v in gm.values()],flush=True)
