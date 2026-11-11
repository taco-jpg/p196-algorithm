#!/usr/bin/env python3
# diagnostic: number of closed L-columns above an interface, widths per phase, random descent
import sys, random
b=10; NV=19
def parse(spec):
    cs,xs,As=spec.split('|'); xb=[int(x) for x in xs.rstrip(',').split(',')]
    return [int(ch) for ch in cs],xb,[int(ch) for ch in As]
def step(g,c,xb,A,t,v,L):
    res={}
    for h in (0,1):
        H=(v+h)//b
        if not (A[t]>>H)&1: continue
        part=((xb[t]+H)%b) if g[t%len(g)] else (v+h)%b
        y=(v+c[t])%b+part
        res[y]=res.get(y,0)|(1<<h)
    return res
def count_closed(g,c,xb,A,L):
    # counts closed L-walks; returns total, per-phase alive digits
    tot=0
    alive=[set() for _ in range(L)]
    for v0 in range(NV):
        # forward DP counts
        cur={v0:1}; layers=[cur]
        for t in range(L):
            nxt={}
            for v,n in cur.items():
                for y in step(g,c,xb,A,t,v,L): nxt[y]=nxt.get(y,0)+n
            cur=nxt; layers.append(cur)
        n=cur.get(v0,0)
        if n==0: continue
        tot+=n
        # backward: nodes on closed walks
        back={v0}
        ok=[None]*(L+1); ok[L]={v0}
        for t in range(L-1,-1,-1):
            s=set()
            for v in layers[t]:
                if any(y in ok[t+1] for y in step(g,c,xb,A,t,v,L)): s.add(v)
            ok[t]=s
            alive[t]|=s
    return tot,alive
def random_column(g,c,xb,A,L,rng):
    # sample a closed column uniformly-ish: pick v0 proportional to count, then walk with pruning
    cands=[]
    for v0 in range(NV):
        cur={v0:1}
        for t in range(L):
            nxt={}
            for v,n in cur.items():
                for y in step(g,c,xb,A,t,v,L): nxt[y]=nxt.get(y,0)+n
            cur=nxt
        if cur.get(v0,0)>0: cands.append(v0)
    if not cands: return None,None
    v0=rng.choice(cands)
    # backward reachability sets to v0
    R=[None]*(L+1); R[L]={v0}
    for t in range(L-1,-1,-1):
        s=set()
        for v in range(NV):
            if any(y in R[t+1] for y in step(g,c,xb,A,t,v,L)): s.add(v)
        R[t]=s
    col=[v0]; ms=[]
    for t in range(L):
        st=step(g,c,xb,A,t,col[-1],L)
        opts=[(y,m) for y,m in st.items() if y in R[t+1]]
        y,m=rng.choice(opts); col.append(y); ms.append(m)
    return col[:L],ms
if __name__=='__main__':
    g=[int(ch) for ch in sys.argv[1]]; L=int(sys.argv[2]); file=sys.argv[3]; nsteps=int(sys.argv[4]) if len(sys.argv)>4 else 40
    for line in open(file):
        if 'iface=' not in line: continue
        spec=line.split('iface=')[1].split()[0]
        c,xb,A=parse(spec)
        print('tower', line[:40].strip())
        rng=random.Random(1)
        for step_i in range(nsteps):
            tot,alive=count_closed(g,c,xb,A,L)
            print(f'  level {step_i}: closed columns = {tot}  widths={[len(a) for a in alive]}'[:220])
            col,ms=random_column(g,c,xb,A,L,rng)
            if col is None: print('   dead'); break
            # successor interface
            c2=[(col[t]+c[t])//b for t in range(L)]
            xb2=[(col[t]%b) if g[t%len(g)] else 0 for t in range(L)]
            c,xb,A=c2,xb2,ms
