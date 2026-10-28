import sys, random
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
def stepB(b,B,k):
    cs = 1 if k>=b else 0; d=(k+cs)%b; kn=2*d
    P = list(B)+[k]*3; n=len(P)
    DB,_ = norm(b,P,0)
    DR,gam = norm(b,P[::-1],cs)
    if not gam: R=[DB[i]+DR[n-1-i] for i in range(n)]
    else: R=[(DB[i] if i<n else d) + (1 if i==0 else DR[n-i]) for i in range(n+1)]
    while R and R[-1]==kn: R.pop()
    return tuple(R), kn, gam
rng=random.Random(3); bad=0; tot=0
for _ in range(20000):
    b=rng.choice([2,3,4,5,7,10,11]); 
    ks=[k for k in range(2*b-1) if k!=b-1]
    k=rng.choice(ks)
    lb=rng.randint(1,7); B=tuple(rng.randint(0,2*b-2) for _ in range(lb))
    if B[0]==0: continue
    # engine
    T=Template(b,[('L',B),('B',(k,),0)],())
    T2,gm,info=step(T)
    exp,kn,gam=stepB(b,B,k)
    got=T2.Hs[0][1] if T2.Hs and T2.Hs[0][0]=='L' else ()
    # engine band block
    bl=[it for it in T2.Hs if it[0]=='B']
    tot+=1
    ok = (got==exp) and bl and bl[0][1]==(kn,) and info['gam']==gam
    if not ok:
        bad+=1
        if bad<6: print('MISMATCH',b,k,B,'engine',fmt(T2),'padded',exp,kn,gam)
print('padded model vs engine:',tot,'cases,',bad,'mismatches')
