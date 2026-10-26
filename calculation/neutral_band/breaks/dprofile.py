import random, collections
def digs(b,x):
    d=[]
    while x: d.append(x%b); x//=b
    return d
def carries(b,W):
    c=[0]
    for w in W: c.append(1 if w+c[-1]>=b else 0)
    return c
def Tstep(b,x):
    d=digs(b,x); L=len(d); W=[d[i]+d[L-1-i] for i in range(L)]
    c=carries(b,W); v=[(W[i]+c[i])%b for i in range(L)]+([1] if c[L] else [])
    return sum(t*b**i for i,t in enumerate(v)), W, c
rng=random.Random(5)
tab=collections.Counter()
for b in (10,):
  for trial in range(3000):
    L=rng.randint(6,14)
    x=rng.randrange(b**(L-1),b**L)
    for t in range(3):
        y,W,c=Tstep(b,x)
        d=digs(b,y)
        if len(d)<4: break
        y2,W2,c2=Tstep(b,y)
        L1=len(W); L2=len(W2)
        # D profile of current step and next step
        D=[c[i]-c[L1-i] for i in range(L1+1)]
        D2=[c2[i]-c2[L2-i] for i in range(L2+1)]
        # overflow of current step: L2 = L1+gam
        g=c[L1]
        if g==0:  # same length, compare D2_i vs D_i, D_{i+1}
            for i in range(1,L1//2):
                tab[(D[i],D[i+1],D2[i])]+=1
        x=y
for k in sorted(tab): print(k,tab[k])
