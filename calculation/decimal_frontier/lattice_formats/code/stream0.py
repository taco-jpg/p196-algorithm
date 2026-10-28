import sys, time
b=int(sys.argv[1]); P=int(sys.argv[2])
xs=list(range(1,2*b-1)); idx={x:i for i,x in enumerate(xs)}
# edges by g: list of (x -> xn)
def succ(x,g):
    out=set()
    for hn in (0,1):
        s=x+hn
        if s//b!=g: continue
        xn=x%b+(1 if g else s%b)
        if 1<=xn<=2*b-2: out.add(xn)
    return out
S={g:{x:succ(x,g) for x in xs} for g in (0,1)}
# state: tuple of masks per x0 (bit xn)
init=tuple(1<<idx[x] for x in xs)
def step(st,g):
    new=[]
    for m in st:
        nm=0; i=0
        mm=m
        while mm:
            if mm&1:
                for xn in S[g][xs[i]]: nm|=1<<idx[xn]
            mm>>=1; i+=1
        new.append(nm)
    return tuple(new)
level={init:1}
t0=time.time()
for t in range(1,P+1):
    nl={}
    for st,c in level.items():
        for g in (0,1):
            ns=step(st,g)
            if any(ns): nl[ns]=nl.get(ns,0)+c
    level=nl
    acc=sum(c for st,c in level.items() if any((m>>i)&1 for i,m in enumerate(st)))
    print(t,'distinct mask-states',len(level),'words with nonempty',sum(level.values()),'accepted closed words',acc, round(time.time()-t0,1),flush=True)
