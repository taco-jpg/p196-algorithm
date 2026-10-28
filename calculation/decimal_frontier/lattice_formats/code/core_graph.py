import sys, time, itertools, json
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
from scc_to_tmpl import *
# Deterministic forward map on templates (exterior = SCC record ri), roots = (r, C) seeds. Memoised cycle search.
recs=parse('../out/p8_scc.txt')
ri=int(sys.argv[1]); maxc=int(sys.argv[2]); cap=int(sys.argv[3]); tlimit=float(sys.argv[4])
rec=recs[ri]; p=rec['p']
base=templates(rec,core=())[0]
W=base.Hs[1][1]; m=len(W); Bl=base.Hs[0][1]
color={}   # template -> 1 on path, 2 done ; value after: result tag
nxt_cache={}
t0=time.time()
cycles=[]; nstates=0; dead=0; errs=0; roots=0
def pal(half, odd):
    return tuple(half)+tuple(half[:-1][::-1] if odd else half[::-1])
def run_from(T):
    global nstates, dead, errs
    path=[]; offs=[]
    cur=T
    while True:
        c=color.get(cur)
        if c==2: break
        if c==1:
            i=path.index(cur)
            cyc=path[i:]; o=sum(offs[i:])
            cycles.append((cyc,o,[len(x.core) for x in cyc]))
            break
        if len(cur.core)>cap:
            dead+=1; break
        color[cur]=1; path.append(cur)
        try:
            nx,gm,info=step(cur)
        except (Ambiguous,Unsupported):
            errs+=1; break
        nstates+=1
        offs.append(sum(v[2] for v in gm.values()))
        if not info['differs']:
            print('PALINDROME state'); break
        cur=nx
    for x in path: color[x]=2
for clen in range(0,maxc+1):
    h=(clen+1)//2
    for half in itertools.product(range(19),repeat=h):
        C=pal(half,clen%2==1) if clen>0 else ()
        for r in range(m):
            core=tuple(W[:r])+C+tuple(W[:r][::-1])
            T=Template(10,[('L',Bl),('B',W,0)],core)
            roots+=1
            run_from(T)
        if time.time()-t0>tlimit: break
    print('clen',clen,'done roots',roots,'states',nstates,'dead',dead,'errs',errs,'cycles',len(cycles),'t',round(time.time()-t0,1),flush=True)
    if time.time()-t0>tlimit: print('time cut'); break
for cyc,o,ls in cycles[:10]:
    print('CYCLE len',len(cyc),'gapoff',o,'core lens',ls)
