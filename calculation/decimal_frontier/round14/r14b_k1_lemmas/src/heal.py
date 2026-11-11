import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r14
HOME=os.path.expanduser("~/p196_run/")
K=int(sys.argv[1]) if len(sys.argv)>1 else 12
L = r14.Lat(HOME+"mchk13b/lat/rec0.txt")
T,K,lay=r14.load_layers(HOME+"r14b/data/rec0_o0/K%d.bin"%K)
S=[set(c) for p,c in lay]; ph=[p for p,c in lay]
def lat(p,i): return L.W[p[0]][(p[1]+i)%20]
def front(p,w):
    for i in range(K):
        if w[i]!=lat(p,i): return i
    return K
heal=collections.Counter()  # (t,col,front index) -> count
downs=collections.Counter()
for l,(p,c) in enumerate(lay):
    l2=(l+1)%T; p2=ph[l2]
    t=p[0]; g=L.clk[t]; dh=1 if (g==1 and p[2]==0) else 0
    for w in c:
        f=front(p,w)
        for d,v,nw in L.succ(p,w):
            if nw not in S[l2]: continue
            f2=front(p2,nw)
            # absolute front change in frame units: new front absolute col = f2 + (j shift); compute delta in abs columns
            delta=(f2+dh)-f
            if delta>0 and f<K:
                col=(p[1]+f)%20
                heal[(t,col)]+=1
            if delta<0: downs[(t,(p[1]+f)%20)]+=1
print("K",K)
print("healing events by (t mod 8, column mod 20), counts:")
print("t\\col "+"".join("%8d"%c for c in range(20)))
for t in range(8):
    print("%d     "%t+"".join("%8d"%heal.get((t,c),0) for c in range(20)))
