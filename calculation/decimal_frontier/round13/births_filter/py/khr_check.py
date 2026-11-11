#!/usr/bin/env python3
"""Independent check of relative tower death levels (r13c). Usage: khr_check.py DEATHFILE g L N [seed]
Each line of DEATHFILE: idx K c|x,x,..|A  (L-periodic interface above the fixed birth column).
Tower: full-window transitions recomputed from scratch for every edge (dict-based), closed L-walk node sets by per-node walk search."""
import sys, random, os
b=10
def parse(spec):
    cs,xs,As=spec.split('|'); c=[int(ch) for ch in cs]; xb=[int(v) for v in xs.split(',')]; A=[int(ch) for ch in As]
    return c,xb,A
def trans(w,t,h,c,xb,A,g):
    # w tuple (w1..wr) bottom to top; returns (y tuple, ok)
    r=len(w)
    H=[0]*(r+2); H[r+1]=h
    for i in range(r,0,-1): H[i]=(w[i-1]+H[i+1])//b
    if not (A[t]>>H[1])&1: return None
    L=c[t]; y=[0]*r
    for i in range(1,r+1):
        wi=w[i-1]; carry_in=L; L=(wi+L)//b
        if g[t]:
            lowd=(xb[t] if i==1 else w[i-2]); part=(lowd+H[i])%b
        else:
            part=(wi+H[i+1])%b
        y[i-1]=(wi+carry_in)%b+part
    return tuple(y)
def tower(c,xb,A,g,Lp,maxlev,capnodes=400000):
    # level r set: dict node->(t) ; nodes (w,t); children of kept nodes
    # level 1 nodes
    nodes=set((tuple([v]),t) for t in range(Lp) for v in range(19))
    def closedset(nodes,r):
        # adjacency
        succ={}
        for (w,t) in nodes:
            s=[]
            for h in (0,1):
                y=trans(w,t,h,c,xb,A,g)
                if y is None: continue
                ng=(y,(t+1)%Lp)
                if ng in nodes and ng not in s: s.append(ng)
            succ[(w,t)]=s
        pred={n:[] for n in nodes}
        for n in nodes:
            for m in succ[n]: pred[m].append(n)
        # exact closed L-walk nodes: for each node at layer 0 forward L steps to itself
        # anchor smallest layer
        layer={}
        for n in nodes: layer.setdefault(n[1],[]).append(n)
        if len(layer)<Lp: return set()
        t0=min(range(Lp),key=lambda t:len(layer[t]))
        keep=set()
        for s in layer[t0]:
            # forward sets over L steps recording time-indexed visited sets
            fw=[{s}]
            for i in range(Lp):
                nx=set()
                for n in fw[-1]:
                    nx.update(succ.get(n,[]))
                fw.append(nx)
            if s not in fw[Lp]: continue
            # backward from s at time L
            bw=[None]*(Lp+1); bw[Lp]={s}
            for i in range(Lp-1,-1,-1):
                cur=set()
                for n in fw[i]:
                    if any(m in bw[i+1] for m in succ.get(n,[])): cur.add(n)
                bw[i]=cur
            for i in range(Lp):
                keep.update(fw[i]&bw[i])
        return keep
    r=1
    while True:
        keep=closedset(nodes,r)
        if not keep: return r
        if r>=maxlev: return None
        r+=1
        nextnodes=set()
        for (w,t) in keep:
            for d in range(19): nextnodes.add((w+(d,),t))
        if len(nextnodes)>capnodes: return -r
        nodes=nextnodes

def main():
    df=sys.argv[1]; gw=sys.argv[2]; Lp=int(sys.argv[3]); N=int(sys.argv[4]); seed=int(sys.argv[5]) if len(sys.argv)>5 else 1
    Ng=len(gw); g=[int(gw[t%Ng]) for t in range(Lp)]
    lines=open(df).read().strip().split('\n')
    random.seed(seed); random.shuffle(lines)
    # prefer towers with small death level for python speed
    sel=[l for l in lines if int(l.split()[1])<=int(os.environ.get('MAXD','25'))][:N]
    ok=bad=skip=0
    for l in sel:
        idx,K,spec=l.split(); K=int(K)
        c,xb,A=parse(spec)
        r=tower(c,xb,A,g,Lp,K+2)
        if r is None or r<0: skip+=1; print('SKIP',idx,K,r); continue
        if r==K: ok+=1
        else: bad+=1; print('DIFF',idx,'khr',K,'py',r,spec)
    print(f"CHECK df={df} n={len(sel)} ok={ok} bad={bad} skip={skip}")
main()
