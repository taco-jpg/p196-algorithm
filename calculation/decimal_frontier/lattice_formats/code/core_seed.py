import sys, time, itertools
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
from scc_to_tmpl import *
# seeds: band phase r (extra W[:r]) + short palindromic core C; evolve; record core length after k periods
recs=parse('../out/p8_scc.txt')
ri=int(sys.argv[1]); maxc=int(sys.argv[2]); periods=int(sys.argv[3]); tlimit=float(sys.argv[4])
rec=recs[ri]; p=rec['p']
base=templates(rec,core=())[0]
W=base.Hs[1][1]; m=len(W)
def pal(half, odd):
    return tuple(half)+tuple(half[:-1][::-1] if odd else half[::-1])
t0=time.time()
best=[]
cnt=0
for clen in range(0,maxc+1):
    h=(clen+1)//2
    for half in itertools.product(range(19),repeat=h):
        C=pal(half,clen%2==1) if clen>0 else ()
        for r in range(m):
            core=tuple(W[:r])+C+tuple(W[:r][::-1])
            # pair word: B W^g core rev(W)^g rev(B): core must be palindrome: yes
            T=Template(10,[('L',base.Hs[0][1]),('B',W,0)],core)
            cur=T; ok=True; lens=[]
            try:
                for t in range(p*periods):
                    cur,gm,info=step(cur)
                    if (t+1)%p==0: lens.append(len(cur.core))
            except (Ambiguous,Unsupported) as e:
                lens=['ERR']
            cnt+=1
            best.append((lens[-1] if lens and lens[-1]!='ERR' else 9999,clen,r,C,lens))
        if time.time()-t0>tlimit: break
    if time.time()-t0>tlimit: print('time cut'); break
best.sort(key=lambda x:(x[0] if isinstance(x[0],int) else 9999))
print('seeds',cnt)
for b in best[:15]: print(b)
