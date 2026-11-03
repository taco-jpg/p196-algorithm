# Language of h-labels (inner carry into the K-head) on cycles of the K-head graph, pattern 0001
import sys, math, collections
exec(open(sys.argv[1]).read().split('# K=1 nodes')[0].replace('pat=[int(c) for c in sys.argv[1]]','pat=[0,0,0,1]').replace("Kmax=int(sys.argv[2]) if len(sys.argv)>2 else 30","Kmax=0").replace("b=int(sys.argv[3]) if len(sys.argv)>3 else 10","b=10"))
Kmax=int(sys.argv[2])
cands=[((x,),ph) for x in range(1,NX) for ph in range(P)]
S=None
for K in range(1,Kmax+1):
    nodes=cands if K==1 else [(pre+(xk,),ph) for (pre,ph) in S for xk in range(NX)]
    nodeset=set(nodes); out={}; lab={}
    for (x,ph) in nodes:
        for h in (0,1):
            y,g=trans(x,h)
            if g==pat[ph]:
                n=(y,(ph+1)%P)
                if n in nodeset: out.setdefault((x,ph),[]).append(n); lab[((x,ph),n)]=lab.get(((x,ph),n),set())|{h}
    comps=cyc_core(out)
    S=[n for c,gp in comps for n in c]
    cs={n:i for i,(c,gp) in enumerate(comps) for n in c}
    byph=collections.Counter()
    for (u,v),hs in lab.items():
        if u in cs and v in cs and cs[u]==cs[v]:
            for h in hs: byph[(u[1],h)]+=1
    print(K,len(S),dict(sorted(byph.items())),flush=True)
