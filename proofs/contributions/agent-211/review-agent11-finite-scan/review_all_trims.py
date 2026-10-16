from itertools import product
def K(x): return 1 if x>=10 else 0
def T(x): return x-9*K(x)
def norm(w,e):
    o=[]
    for x in w: o.append((x+e)%10); e=(x+e)//10
    return o,e
def add(a,b): return [x+y for x,y in zip(a,b)]
def lead(w,x):
    n=0
    while n<len(w) and w[n]==x: n+=1
    return n
def raw_parts(s):
    c,B,A,C=s; d=18-c
    DB,e0=norm(B,0); DA,e1=norm(A,K(c)); DC,e2=norm(C,K(d))
    DRA,e3=norm(A[::-1],K(d)); DRB,g=norm(B[::-1],K(c))
    u0=c+e0-10*K(c); u1=d+e1-10*K(d); u2=d+e2-10*K(d); u3=c+e3-10*K(c)
    if g==0:
        Br=add(DB+[u0],DRB[::-1]+[T(c)])
        Ar=add([T(c)]+DA+[u1],[u3]+DRA[::-1]+[T(d)])
        q=[T(d)]+DC+[u2]
    else:
        Br=add(DB+[u0],[1]+DRB[::-1])
        Ar=add(DA+[u1],[u3]+DRA[::-1])
        q=DC+[u2]
    return 2*T(c),Br,Ar,add(q,q[::-1])
def all_trim_variants(s):
    c,Br,Ar,Cr=raw_parts(s); d=18-c
    maxj=lead(Br[::-1],c)
    maxj1=lead(Ar,c)
    maxk=min(lead(Cr,d),lead(Cr[::-1],d),len(Cr)//2)
    for j in range(maxj+1):
        B=Br[:len(Br)-j]
        for j1 in range(maxj1+1):
            A1=Ar[j1:]
            for j2 in range(lead(A1[::-1],d)+1):
                A=A1[:len(A1)-j2]
                for k in range(maxk+1):
                    C=Cr[k:len(Cr)-k]
                    yield (c,B,A,C)
def states(phases,vals,maxba,maxc,sym):
    mids=range(0,19,2)
    for c in phases:
        for lb in range(maxba+1):
            for la in range(maxba+1):
                for B in product(vals,repeat=lb):
                    for A in product(vals,repeat=la):
                        for lc in range(maxc+1):
                            if not sym:
                                for C in product(vals,repeat=lc): yield(c,list(B),list(A),list(C))
                            else:
                                for h in product(vals,repeat=lc//2):
                                    if lc%2==0: yield(c,list(B),list(A),list(h+h[::-1]))
                                    else:
                                        for m in mids: yield(c,list(B),list(A),list(h+(m,)+h[::-1]))
def audit(S):
    U={ (s[0],tuple(s[1]),tuple(s[2]),tuple(s[3])) for s in S }
    mp={ (s[0],tuple(s[1]),tuple(s[2]),tuple(s[3])):s for s in S }
    edges={u:set() for u in U}
    for s in S:
        u=(s[0],tuple(s[1]),tuple(s[2]),tuple(s[3]))
        for q in all_trim_variants(s):
            v=(q[0],tuple(q[1]),tuple(q[2]),tuple(q[3]))
            if v in U: edges[u].add(v)
    color={}
    def dfs(u):
        color[u]=1
        for v in edges[u]:
            if color.get(v,0)==0 and dfs(v): return True
            if color.get(v,0)==1: return True
        color[u]=2
        return False
    cyc=any(color.get(u,0)==0 and dfs(u) for u in U)
    return len(U),sum(map(len,edges.values())),max(map(len,edges.values()),default=0),cyc
def states_ba(phases,vals,maxb,maxa,maxc):
    """Symmetric-C state domain with independent B and A length bounds."""
    for c in phases:
        for lb in range(maxb+1):
            for la in range(maxa+1):
                for B in product(vals,repeat=lb):
                    for A in product(vals,repeat=la):
                        for lc in range(maxc+1):
                            for h in product(vals,repeat=lc//2):
                                if lc%2==0: yield(c,list(B),list(A),list(h+h[::-1]))
                                else:
                                    for m in range(0,19,2): yield(c,list(B),list(A),list(h+(m,)+h[::-1]))
if __name__=='__main__':
    import sys
    sys.setrecursionlimit(1000000)
    v1=range(19); v2=(0,1,8,9,10,17,18)
    if len(sys.argv)==5 and sys.argv[1]=='two-phase':
        # two-phase {6,12} extension: two-phase MAXB MAXA MAXC
        mb,ma,mc=map(int,sys.argv[2:])
        print('two_phase_B%d_A%d_C%d'%(mb,ma,mc),audit(list(states_ba([6,12],v2,mb,ma,mc))))
        raise SystemExit
    D=[('all16_len1',[1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17],v1,1,1,False),
       ('six_len2',[2,4,8,16,14,10],v2,2,2,True),
       ('two_len2',[6,12],v2,2,2,True)]
    for n,p,v,ba,cc,sy in D:
        print(n,audit(list(states(p,v,ba,cc,sy))))
