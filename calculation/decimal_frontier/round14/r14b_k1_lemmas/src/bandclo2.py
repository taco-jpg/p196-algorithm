#!/usr/bin/env python3
# bandclo2.py: all-period closure for windows directly below an exact periodic lattice band B (spatial period m, time period 8, clock 10),
# free inputs from below. usage: bandclo2.py ROW(t=0 comma list, length m) Kmax [selftest N]
import sys, random
from collections import defaultdict, deque
BASE=10
clk=[1,0,1,0,1,0,1,0]; tp=8
def cc(v): return 1 if v>=BASE else 0
def cyc_step(row,g):
    m=len(row)
    if all(v==BASE-1 for v in row): return None
    a=[0]*m
    for it in range(3*m):
        for x in range(m): a[(x+1)%m]=1 if row[x]+a[x]>=BASE else 0
    b=[0]*m
    for it in range(3*m):
        for x in range(m-1,-1,-1): b[(x-1)%m]=1 if row[x]+b[x]>=BASE else 0
    e=[(row[x]+a[x])%BASE for x in range(m)]
    r=[(row[x]+b[x])%BASE for x in range(m)]
    return tuple(e[x]+r[(x-g)%m] for x in range(m)), a, b
def band_table(row0):
    m=len(row0)
    rows=[]; UP=[]; DN=[]
    r=tuple(row0)
    for t in range(tp):
        nxt,a,b=cyc_step(r,clk[t])
        rows.append(r); UP.append(a); DN.append(b)
        r=nxt
    assert r==tuple(row0), "no 8-step return"
    # consistency: cyclic carries; DN[t][j] := carry b_j entering column j from above; UP[t][j] := a_j entering column j from below
    return m,rows,UP,DN
def wsucc(u, ph, m, B, UP, DN):
    """u top-first window; ph=(t,je,par); returns list of (head,tops)."""
    t,je,par=ph; g=clk[t]; dh=(g==1 and par==0); tn=(t+1)%tp
    K=len(u)
    w=list(u)[::-1]
    kB=B[t][je]; kBn=B[tn][je]
    # Din = carry entering window top cell (from band cell je going down) = b_{je-1} of band = [B[t][je] + DN[t][je] >= 10]
    Din=1 if kB+DN[t][je]>=BASE else 0
    r=[0]*K; bc=Din
    for i in range(K-1,-1,-1):
        s=w[i]+bc; r[i]=s%BASE; bc=1 if s>=BASE else 0
    RB=(kB+DN[t][je])%BASE
    out=[]
    for a_in in (0,1):
        e=[0]*K; a=a_in
        for i in range(K):
            s=w[i]+a; e[i]=s%BASE; a=1 if s>=BASE else 0
        EB=(kB+a)%BASE
        same = (a==UP[t][je])
        if not same and kB==BASE-1:  # carry would propagate up into the band
            continue
        if g==0:
            if EB+RB!=kBn: continue
            nw=[e[i]+r[i] for i in range(K)]
            tops=[nw[0]]
        elif not dh:
            if EB+r[K-1]!=kBn: continue
            nw=[0]*K
            for i in range(1,K): nw[i]=e[i]+r[i-1]
            tops=[e[0]+rin for rin in range(10)]
        else:
            nw=[e[i+1]+r[i] for i in range(K-1)]+[EB+r[K-1]]
            tops=[nw[0]]
        head=tuple(nw[K-1-i] for i in range(K-1))
        out.append((head,tops))
    return out
def orbits(m):
    tot={}; orbs=[]
    for t0 in range(tp):
        for j0 in range(m):
            for p0 in (0,1):
                s=(t0,j0,p0)
                if s in tot: continue
                o=[]; cur=s
                while cur not in tot:
                    tot[cur]=len(orbs); o.append(cur)
                    t,j,par=cur; g=clk[t]; dh=1 if (g==1 and par==0) else 0
                    cur=((t+1)%tp,(j+dh)%m,(par+g)%2)
                orbs.append(o)
    return orbs
def closure(row0,Kmax):
    m,B,UP,DN=band_table(row0)
    orbs=orbits(m)
    results=[]
    for oi,orb in enumerate(orbs):
        T=len(orb); 
        prevL=[{()} for _ in range(T)]
        for K in range(1,Kmax+1):
            cand=[{p+(v,) for p in prevL[l] for v in range(2*BASE-1)} for l in range(T)]
            succ=[{} for _ in range(T)]
            pred=[defaultdict(list) for _ in range(T)]
            for l,ph in enumerate(orb):
                l2=(l+1)%T; P2=prevL[l2]
                for u in cand[l]:
                    out=set()
                    for head,tops in wsucc(u,ph,m,B,UP,DN):
                        if K==1 or head in P2:
                            for v in tops:
                                nu=head+(v,)
                                if nu in cand[l2]: out.add(nu)
                    succ[l][u]=list(out)
                    for nu in out: pred[l2][nu].append(u)
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
            # SCC with accepting: use simple Tarjan
            nodes=[(l,u) for l in range(T) for u in alive[l]]
            ids={n:i for i,n in enumerate(nodes)}; N=len(nodes)
            adj=[[ids[((l+1)%T,nu)] for nu in succ[l][u] if nu in alive[(l+1)%T]] for (l,u) in nodes]
            index=[-1]*N; low=[0]*N; on=[False]*N; st=[]; comp=[-1]*N; cnt=0; nc=0
            for s in range(N):
                if index[s]!=-1: continue
                work=[(s,0)]
                while work:
                    v,pi=work.pop()
                    if pi==0:
                        index[v]=low[v]=cnt; cnt+=1; st.append(v); on[v]=True
                    rec=False
                    for k in range(pi,len(adj[v])):
                        w=adj[v][k]
                        if index[w]==-1:
                            work.append((v,k+1)); work.append((w,0)); rec=True; break
                        elif on[w]: low[v]=min(low[v],index[w])
                    if rec: continue
                    if low[v]==index[v]:
                        while True:
                            x=st.pop(); on[x]=False; comp[x]=nc
                            if x==v: break
                        nc+=1
                    if work:
                        pv=work[-1][0]; low[pv]=min(low[pv],low[v])
            size=defaultdict(int); accc=set()
            selfl=[False]*N
            for v in range(N):
                size[comp[v]]+=1
                for w in adj[v]:
                    if w==v: selfl[v]=True
            for i,(l,u) in enumerate(nodes):
                t,je,par=orb[l]
                onband=B[t][(je-1)%m]
                if u[0]!=onband: accc.add(comp[i])
            keep=[set() for _ in range(T)]
            for i,(l,u) in enumerate(nodes):
                if comp[i] in accc and (size[comp[i]]>=2 or selfl[i]): keep[l].add(u)
            total=sum(len(k) for k in keep)
            print("orbit",oi,"T",T,"K",K,"accepted-SCC states",total,"closed-walk states",N,flush=True)
            if total==0:
                print("  EMPTY at K=",K,flush=True); break
            prevL=keep
            if K==Kmax: print("  (still nonempty at Kmax)")
def selftest(row0, N_iter, seed=7):
    m,B,UP,DN=band_table(row0)
    rnd=random.Random(seed)
    tested=0; skipped=0; bad=0
    for it in range(N_iter):
        t=rnd.randrange(tp); g_expected=clk[t]
        wb=rnd.randint(4,12)
        K=rnd.randint(1,6)
        lowc=rnd.randint(1,10)
        h=lowc+K+wb
        par=rnd.randint(0,1)
        n=2*h-par
        # band columns: alignment: column index je at window top boundary; band occupies columns je, je+1, ..., je+wb-1 going up
        je=rnd.randrange(m)
        P=[rnd.randrange(19) for _ in range(lowc)]
        win=[rnd.randrange(19) for _ in range(K)]
        band=[B[t][(je+i)%m] for i in range(wb)]
        P=P+win+band
        if par==1 and P[-1]%2==1:
            continue
        d=[0]*n
        for x in range(h):
            mi=n-1-x
            if x==mi: d[x]=P[x]//2
            else:
                lo=max(0,P[x]-9); hi=min(P[x],9); v=rnd.randint(lo,hi); d[x]=v; d[mi]=P[x]-v
        if d[n-1]==0: continue
        Nv=sum(d[i]*10**i for i in range(n))
        M=Nv+int(str(Nv)[::-1])
        g=len(str(M))-n
        n2=n+g; h2=(n2+1)//2; dh=h2-h
        if g!=g_expected: continue
        Md=[(M//10**i)%10 for i in range(n2)]
        P2=[Md[x]+Md[n2-1-x] for x in range(h2)]
        tn=(t+1)%tp
        je2=(je+dh)%m
        # band check: cells [h2-wb, h2) must equal B[tn][je2 + i] 
        if not all(P2[h2-wb+i]==B[tn][(je2+i)%m] for i in range(wb-3)):   # ignore 3 cells near the fold (non-self-mirror alignment)
            skipped+=1; continue
        # also require the band cells immediately above window (first 3 of them) to be exact
        u=tuple(win[K-1-i] for i in range(K))  # top-first
        # new window: cells [h2-wb-K, h2-wb) top-first
        unew=tuple(P2[h2-wb-1-i] for i in range(K))
        ph=(t,je,par)
        found=False
        for head,tops in wsucc(u,ph,m,B,UP,DN):
            if head==unew[:K-1] and unew[K-1] in tops: found=True
        tested+=1
        if not found:
            bad+=1
            print("MISMATCH",t,par,g,dh,je,u,unew,win,band[:6],P2[h2-wb-K:h2-wb+3]); break
    print("selftest",row0,"tested",tested,"skipped",skipped,"bad",bad)

if __name__=="__main__":
    if len(sys.argv)>3 and sys.argv[3]=="selftest":
        selftest([int(x) for x in sys.argv[1].split(",")], int(sys.argv[2])); sys.exit(0)
    row=[int(x) for x in sys.argv[1].split(",")]
    Kmax=int(sys.argv[2])
    if len(sys.argv)>3 and sys.argv[3]=="check":
        m,B,UP,DN=band_table(row); print("band table rows:",B); print("UP",UP); print("DN",DN); sys.exit(0)
    print("band row (t=0):",row)
    closure(row,Kmax)
