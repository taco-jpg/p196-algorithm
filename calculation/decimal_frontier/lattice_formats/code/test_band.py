import sys, random, itertools
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
b=10
def fc(w): return norm(b,w,0)[1], norm(b,w,1)[1]
def succ(w,gam):
    m=len(w); f0,f1=fc(w)
    if f0==0 and f1==1: return None
    g0,g1=fc(w[::-1])
    if g0==0 and g1==1: return None
    dl,_=norm(b,w,f0); du,_=norm(b,w[::-1],g0)
    if gam==0: nw=tuple(dl[i]+du[m-1-i] for i in range(m))
    else: nw=tuple(dl[i]+du[(m-i)%m] for i in range(m))
    return primitive(nw)[0]
def rot_eq(a,c):
    return len(a)==len(c) and any(a[i:]+a[:i]==c for i in range(len(a)))
rng=random.Random(11); tot=0; bad=0; byg={0:0,1:0}
for _ in range(6000):
    m=rng.randint(1,4)
    w=tuple(rng.randint(0,18) for _ in range(m))
    if w[0]==0 and False: continue
    if primitive(w)[0]!=w: continue
    lb=rng.randint(1,5); B=tuple(rng.randint(0,18) for _ in range(lb))
    if B[0]==0: continue
    T=Template(b,[('L',B),('B',w,0)],rng.choice([(),(3,),(4,4)]))
    try: T2,gm,info=step(T)
    except (Ambiguous,Unsupported) as e: continue
    s=succ(w,info['gam'])
    if s is None: continue
    bl=[it for it in T2.Hs if it[0]=='B']
    tot+=1; byg[info['gam']]+=1
    if not bl or not rot_eq(bl[0][1],s):
        bad+=1
        if bad<8: print('MISMATCH w',w,'gam',info['gam'],'succ',s,'engine',fmt(T2),'from',fmt(T))
print('band successor formula vs engine:',tot,'cases',bad,'mismatches',byg)
