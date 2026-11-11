#!/usr/bin/env python3
# bandclo.py: all-period closure of the BAND-ANCHORED top relaxation R^U_K:
# window = the K cells directly below an exact uniform band (band above the window on-band for all time),
# free inputs from below (a_in, r_in), accepting state = window top cell off-band.
# usage: bandclo.py BAND_CYCLE(comma list) OFFSET CLOCK_PAR_START Kmax [selftest N]
import sys, random
from collections import defaultdict, deque
BASE=10
def c(v): return 1 if v>=BASE else 0
clk8=[1,0,1,0,1,0,1,0]
def make(bandcycle, off):
    p=len(bandcycle)
    L=8
    from math import gcd
    tp=8*p//gcd(8,p)
    band=[bandcycle[(t+off)%p] for t in range(tp)]
    clk=[clk8[t%8] for t in range(tp)]
    return tp, band, clk
def succs(tp, band, clk, ph, u):
    t,par=ph
    g=clk[t]; dh=(g==1 and par==0); tn=(t+1)%tp
    return wsucc(u, band[t], band[tn], g, dh)
def wsucc(u, kB, kBn, g, dh):
    """u = window (top-first) cells tuple, kB/kBn band values now/next; returns list of (head, tops)."""
    Din=c(kB)
    K=len(u)
    w=list(u)[::-1]  # bottom-based
    r=[0]*K; b=Din
    for i in range(K-1,-1,-1):
        s=w[i]+b; r[i]=s%BASE; b=1 if s>=BASE else 0
    RB=(kB+Din)%BASE
    out=[]
    for a_in in (0,1):
        e=[0]*K; a=a_in
        for i in range(K):
            s=w[i]+a; e[i]=s%BASE; a=1 if s>=BASE else 0
        EB=(kB+a)%BASE
        nw=[0]*K
        if g==0:
            if EB+RB!=kBn: continue
            for i in range(K): nw[i]=e[i]+r[i]
            tops=[nw[0]]
        elif not dh:
            if EB+r[K-1]!=kBn: continue
            for i in range(1,K): nw[i]=e[i]+r[i-1]
            tops=[e[0]+rin for rin in range(10)]
        else:
            for i in range(K-1): nw[i]=e[i+1]+r[i]
            nw[K-1]=EB+r[K-1]
            tops=[nw[0]]
        head=tuple(nw[K-1-i] for i in range(K-1))  # top-first, excluding bottom cell
        out.append((head,tops))
    return out
def closure(tp,band,clk,par0,Kmax,verbose=True):
    # phases: (t,par) orbit from (0,par0)
    # orbit
    orb=[]; cur=(0,par0); seen=set()
    while cur not in seen:
        seen.add(cur); orb.append(cur)
        t,par=cur; g=clk[t]; cur=((t+1)%tp,(par+g)%2)
    T=len(orb); idx={p:i for i,p in enumerate(orb)}
    prevL=[{()} for _ in range(T)]  # level 0: empty window
    res=[]
    for K in range(1,Kmax+1):
        # candidates: parent (top K-1 cells) + new bottom cell v
        cand=[set() for _ in range(T)]
        for l in range(T):
            for p in prevL[l]:
                for v in range(2*BASE-1):
                    cand[l].add(p+(v,))
        # edges
        succ=[{} for _ in range(T)]
        pred=[defaultdict(list) for _ in range(T)]
        for l,ph in enumerate(orb):
            l2=(l+1)%T
            P2=prevL[l2]
            for u in cand[l]:
                out=set()
                for head,tops in succs(tp,band,clk,ph,u):
                    if K==1 or head in P2:
                        for v in tops:
                            nu=head+(v,)
                            if nu in cand[l2]: out.add(nu)
                succ[l][u]=list(out)
        for l in range(T):
            l2=(l+1)%T
            for u,o in succ[l].items():
                for nu in o: pred[l2][nu].append(u)
        # trim to bi-infinite core
        alive=[set(cand[l]) for l in range(T)]
        outd=[{u:len(succ[l][u]) for u in cand[l]} for l in range(T)]
        ind=[{u:len(pred[l].get(u,[])) for u in cand[l]} for l in range(T)]
        q=deque((l,u) for l in range(T) for u in cand[l] if outd[l][u]==0 or ind[l][u]==0)
        while q:
            l,u=q.popleft()
            if u not in alive[l]: continue
            alive[l].discard(u)
            l2=(l+1)%T; l0=(l-1)%T
            for nu in succ[l][u]:
                if nu in alive[l2]:
                    ind[l2][nu]-=1
                    if ind[l2][nu]==0: q.append((l2,nu))
            for pu in pred[l].get(u,[]):
                if pu in alive[l0]:
                    outd[l0][pu]-=1
                    if outd[l0][pu]==0: q.append((l0,pu))
        # SCCs (iterative Tarjan) on alive
        nodes=[(l,u) for l in range(T) for u in alive[l]]
        ids={n:i for i,n in enumerate(nodes)}
        N=len(nodes)
        adj=[[ids[((l+1)%T,nu)] for nu in succ[l][u] if nu in alive[(l+1)%T]] for (l,u) in nodes]
        index=[-1]*N; low=[0]*N; on=[False]*N; stk=[]; comp=[-1]*N; cnt=0; nc=0
        for s in range(N):
            if index[s]!=-1: continue
            work=[(s,0)]
            while work:
                v,pi=work.pop()
                if pi==0:
                    index[v]=low[v]=cnt; cnt+=1; stk.append(v); on[v]=True
                rec=False
                for k in range(pi,len(adj[v])):
                    w=adj[v][k]
                    if index[w]==-1:
                        work.append((v,k+1)); work.append((w,0)); rec=True; break
                    elif on[w]: low[v]=min(low[v],index[w])
                if rec: continue
                if low[v]==index[v]:
                    while True:
                        x=stk.pop(); on[x]=False; comp[x]=nc
                        if x==v: break
                    nc+=1
                if work:
                    pv=work[-1][0]; low[pv]=min(low[pv],low[v])
        # accepted SCCs: an SCC with >=2 nodes (or self loop) containing a state with top cell off-band
        size=defaultdict(int)
        accc=set(); acccnt=defaultdict(int)
        for i,(l,u) in enumerate(nodes):
            size[comp[i]]+=1
        selfl=[False]*N
        for v in range(N):
            for w in adj[v]:
                if w==v: selfl[v]=True
        for i,(l,u) in enumerate(nodes):
            ph=orb[l]
            kB=band[ph[0]]
            if u[0]!=kB:
                accc.add(comp[i])
        keep=[set() for _ in range(T)]
        for i,(l,u) in enumerate(nodes):
            cid=comp[i]
            if (size[cid]>=2 or selfl[i]) and cid in accc:
                keep[l].add(u)
        total=sum(len(k) for k in keep)
        res.append((K,total,len(nodes)))
        if verbose: print("K",K,"accepting-SCC states",total,"all closed-walk states",len(nodes),"accepting SCCs",len(accc),flush=True)
        if total==0:
            print("EMPTY at K=",K,flush=True)
            return K,res
        prevL=keep
    return None,res

def selftest(n_iter, seed=1):
    rnd=random.Random(seed)
    bands=[0,18,6,12,2,4,8,16,14,10]
    def ds(v): return v-9 if v>=10 else v
    tested=skipped=0
    for it in range(n_iter):
        n=rnd.randint(8,40)
        h=(n+1)//2
        wb=rnd.randint(2,5); K=rnd.randint(1,6)
        if h-wb-K<1: continue
        k=rnd.choice(bands); k2=2*ds(k)
        P=[rnd.randrange(19) for _ in range(h-wb)]+[k]*wb
        if n%2==1: P[-1]=P[-1]-(P[-1]%2)  # top cell even for odd n (band cells are even)
        # digits
        d=[0]*n
        for x in range(h):
            m=n-1-x
            if x==m:
                d[x]=P[x]//2
            else:
                lo=max(0,P[x]-9); hi=min(P[x],9)
                v=rnd.randint(lo,hi); d[x]=v; d[m]=P[x]-v
        if d[n-1]==0:
            continue
        N=sum(d[i]*10**i for i in range(n))
        M=N+int(str(N)[::-1])
        g=len(str(M))-n
        n2=n+g; h2=(n2+1)//2; dh=h2-h
        P2=[]
        Md=[(M//10**i)%10 for i in range(n2)]
        for x in range(h2):
            P2.append(Md[x]+Md[n2-1-x])
        # band on-band after the step?
        if not all(P2[x]==k2 for x in range(h2-wb,h2)):
            skipped+=1; continue
        # window now/next (top-first)
        u=tuple(P[h-wb-1-i] for i in range(K))
        unew=tuple(P2[h2-wb-1-i] for i in range(K))
        found=False
        for head,tops in wsucc(u,k,k2,g,dh==1):
            if head==unew[:K-1] and unew[K-1] in tops:
                found=True
        tested+=1
        if not found:
            print("MISMATCH",n,g,dh,u,unew,k,P); return False
    print("selftest ok: tested",tested,"skipped(band broke)",skipped)
    return True

if __name__=="__main__":
    if sys.argv[1]=="selftest":
        selftest(int(sys.argv[2])); sys.exit(0)
    bandcycle=[int(x) for x in sys.argv[1].split(",")]
    off=int(sys.argv[2]); par0=int(sys.argv[3]); Kmax=int(sys.argv[4])
    tp,band,clk=make(bandcycle,off)
    print("band",bandcycle,"offset",off,"tp",tp,"par0",par0)
    closure(tp,band,clk,par0,Kmax)
