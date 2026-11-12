from scan_centre import *
from collections import defaultdict
k=[k for k in range(len(comps)) if cyc[k] and len(comps[k])==20][0]
cn=[order[v] for v in cycle_walk(edges,comp_of,comps[k][0])]
P=80
g,F,phi=fold_frame(P,0)
cells=lattice_cells(B,cn)
H=sheared_node(B,F,phi,cells,0)
a,b,c,d=H
al=F.alpha; ga=F.gamma
s=[a[t]+b[t] for t in range(P)]
cp=[1 if s[t]+c[t]>=B else 0 for t in range(P)]
print('alpha',''.join(map(str,al[:16])),'gamma',''.join(map(str,ga[:16])))
print('H.s',s[:24]); print('H.d',d[:24])
# count partial histories per level via DP keyed by (a0,b0,a,b)
cur=defaultdict(int)
for a0 in range(10):
    for b0 in range(10): cur[(a0,b0,a0,b0)]=1
for t in range(P):
    nxt=defaultdict(int)
    for (a0,b0,x,y),cnt in cur.items():
        sp=x+y
        if al[t]==1 and (sp+cp[t])%B!=a[(t+1)%P]: continue
        dt=d[t]
        if dt!=2:
            if sp==9: dopts=(dt,)
            else:
                if (1 if sp>=B else 0)!=dt: continue
                dopts=(0,1) if ga[t]==0 else (2,)
        else:
            dopts=(0,1) if sp==9 else (2,)
        for dp in dopts:
            if ga[t]==0: nb=(sp+dp)%B
            else:
                actual=dt if dt!=2 else (dp if sp==9 else (1 if sp>=B else 0))
                nb=(s[t]+actual)%B
            if al[t]==0:
                nxt[(a0,b0,(sp+cp[t])%B,nb)]+=cnt
            else:
                for na in range(B): nxt[(a0,b0,na,nb)]+=cnt
    cur=nxt
    if t<24 or t%8==7: print('t',t,'al',al[t],'ga',ga[t],'distinct states',len(cur),'partial histories',sum(cur.values()))
fin=sum(cnt for (a0,b0,x,y),cnt in cur.items() if (a0,b0)==(x,y))
print('full periodic histories:',fin)
