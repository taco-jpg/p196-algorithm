import random,sys
sys.path.insert(0,'.')
from cone import centre_step,us
def evolve(U,C,K=100):
    s=list(U)*K+list(C)+list(U[::-1])*K
    for t in range(120):
        s,_=centre_step(s,1 if t%4==0 else 0)
    return s
def target(U,C,K):
    return list(U)*K+list(C)+list(U[::-1])*K
def mism(U,C):
    s=evolve(U,C); m=len(C)
    tg=target(U,C,105); a=(len(tg)-len(s))//2; tg=tg[a:a+len(s)]
    a0=(len(s)-m)//2
    rads=[]
    for j,(x,y) in enumerate(zip(s,tg)):
        if x!=y:
            p=j-a0; rads.append(-p if p<0 else (0 if p<m else p-m+1))
    return (min(rads),max(rads),len(rads)) if rads else None, len(s)
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 1)
U_all=us()
for L in map(int,sys.argv[1].split(',')):
    out=[]
    for trial in range(12):
        U=random.choice(U_all)
        h=[random.randrange(19) for _ in range((L+1)//2)]
        if L%2: h[-1]&=~1
        C=h+h[::-1] if L%2==0 else h+h[-2::-1]
        r,core=mism(U,C)
        out.append(r)
    print(L,'core',core,out)
